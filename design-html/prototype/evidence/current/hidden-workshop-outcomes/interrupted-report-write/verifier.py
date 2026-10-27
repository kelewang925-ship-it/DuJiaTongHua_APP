"""Photo tag and workshop hidden choices with real consumer/persistence assertions."""
import hashlib,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import MODULES,declarations
from audit_runtime import INIT
from verify_pet_controls import ROOT,source

OUT=ROOT/'evidence/current/hidden-workshop-outcomes'
CASES=[(14,'apply'),(14,'cancel'),*[(i,'favorite') for i in [30,33,36,39]],(28,'source'),(34,'photos'),*[(35,k) for k in ['diary','photo','moment']],(37,'cancel-generation'),(38,'copy'),(38,'copy-denied')]
LABELS={'diary':'共同日记','photo':'相册照片','moment':'重要时刻'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def store(p):return p.evaluate('({...localStorage})')
def read(p,k):return p.evaluate('k=>JSON.parse(localStorage.getItem(k))',k)
def unchanged_except(before,after,key):
    a=dict(before);b=dict(after);a.pop(key,None);b.pop(key,None);assert a==b

def main():
    OUT.mkdir(exist_ok=True);files=source();obspath=ROOT/'evidence/current/hidden-overlay-observations.json';observed=json.loads(obspath.read_text(encoding='utf-8'))
    fixtures={k:declarations(v) for k,v in MODULES.items()};rows=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for index,mode in CASES:
            context=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce',permissions=['clipboard-read','clipboard-write']);context.add_init_script(INIT)
            page=context.new_page();page.set_default_timeout(6000);page.set_default_navigation_timeout(20000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            row=dict(observation_index=index,mode=mode,passed=False,errors=errors)
            try:
                original=observed['results'][index];fixtures[original['group']]['seed'](page,original['page'])
                if original['group']=='workshop':
                    page.evaluate('localStorage.setItem("dujia-prototype-works",JSON.stringify(PrototypeWorkshop.all()))')
                if index==34:
                    page.evaluate('()=>{const k="dujia-prototype-records",r=JSON.parse(localStorage.getItem(k));r.push({...r.find(v=>v.id==="work-photo"),id:"work-photo-two",title:"另一张共同照片"});localStorage.setItem(k,JSON.stringify(r))}')
                if index==35:
                    page.evaluate('()=>{const k="dujia-prototype-works",r=JSON.parse(localStorage.getItem(k));r.find(v=>v.id==="work-film").sourceIds=[];localStorage.setItem(k,JSON.stringify(r))}');page.reload()
                before=store(page);url=page.url
                if mode=='copy-denied':page.evaluate('()=>{navigator.clipboard.writeText=async()=>{throw new DOMException("QA denied","NotAllowedError")}}')
                page.locator(original['selector']).click();dialog=page.locator('dialog[open]');expect(dialog.locator('h2')).to_have_text(original['overlays'][0]['title'])
                if index==14:
                    field=dialog.get_by_label('编辑照片标签',exact=True);field.fill('旅行、晴天、旅行')
                    label='使用这些标签' if mode=='apply' else '取消';row.update(control_label=label,native_controls=['编辑照片标签'])
                    old=page.locator('[name=tag]').input_value();dialog.get_by_role('button',name=label,exact=True).click();expect(dialog).to_have_count(0)
                    expect(page.locator('[name=tag]')).to_have_value('旅行、晴天、旅行' if mode=='apply' else old);assert store(page)==before
                    if mode=='apply':
                        fixtures['record']['image'](page);expect(page.locator('#selected')).to_be_visible();page.locator('[name=caption]').fill('标签保存照片')
                        page.get_by_role('button',name='保存照片',exact=True).click();page.wait_for_url('**/m03-p10.html*')
                        photos=read(page,'dujia-prototype-records');assert len(photos)==1 and photos[0]['tags']==['旅行','晴天']
                        unchanged_except(before,store(page),'dujia-prototype-records')
                    row['result']='editable sheet tags stay candidate until parent photo save; deduplicated tags persisted' if mode=='apply' else 'cancel discards sheet input and preserves parent candidate/all local data'
                elif mode=='favorite':
                    row['control_label']='收藏作品';key='dujia-prototype-works';old=json.loads(before[key]);identifier={'30':'work-free','33':'work-photos','36':'work-film','39':'work-ready'}[str(index)]
                    dialog.get_by_role('button',name='收藏作品',exact=True).click();expect(dialog).to_have_count(0)
                    page.wait_for_function('id=>JSON.parse(localStorage.getItem("dujia-prototype-works")).find(v=>v.id===id).favorite===true',arg=identifier)
                    new=read(page,key);expected=[{**v,'favorite':True} if v['id']==identifier else v for v in old];assert new==expected
                    unchanged_except(before,store(page),key)
                    page.locator(original['selector']).click();page.locator('dialog[open]').get_by_role('button',name='取消收藏',exact=True).click();expect(page.locator('dialog[open]')).to_have_count(0)
                    assert read(page,key)==[{**v,'favorite':False} if v['id']==identifier else v for v in old]
                    row['result']='favorite toggles exact target both ways; draft/body/source fields, other works and unrelated data preserved'
                elif index in [28,34,35]:
                    if index==35:
                        label=LABELS[mode];row['control_label']=label;dialog.get_by_role('button',name=label,exact=True).click();expect(dialog.locator('h2')).to_have_text('选择共同素材')
                        wanted='work-'+mode;dialog.locator('input[value="'+wanted+'"]').check()
                    elif index==28:
                        row.update(control_label='使用这段回忆',native_controls=['source']);wanted='work-diary';dialog.locator('input[value=work-diary]').check()
                    else:
                        row.update(control_label='使用这些素材',native_controls=['source']);wanted='work-photo-two'
                        expect(dialog.locator('input[value=work-photo]')).to_be_checked();dialog.locator('input[value=work-photo]').uncheck();dialog.locator('input[value=work-photo-two]').check()
                    dialog.get_by_role('button',name='使用这段回忆' if index==28 else '使用这些素材',exact=True).click();expect(dialog).to_have_count(0)
                    if index==28:
                        page.wait_for_url('**/m05-p03.html*');new=read(page,'dujia-prototype-works');old=json.loads(before['dujia-prototype-works']);assert len(new)==len(old)+1
                        added=next(v for v in new if v['id'] not in {w['id'] for w in old});assert added['sourceIds']==[wanted] and added['sourceKind']=='diary' and added['status']=='draft'
                        assert all(v in new for v in old);row['destination']='m05-p03'
                    else:
                        assert store(page)==before,'Chooser wrote before parent save'
                        page.get_by_role('button',name='暂存创作草稿',exact=True).click();page.wait_for_url('**/m05-p09.html*')
                        identifier='work-photos' if index==34 else 'work-film';value=next(v for v in read(page,'dujia-prototype-works') if v['id']==identifier)
                        assert value['sourceIds']==[wanted] and value['sourceKind']==('photo' if index==34 else mode)
                        old=json.loads(before['dujia-prototype-works']);new=read(page,'dujia-prototype-works');assert [v for v in old if v['id']!=identifier]==[v for v in new if v['id']!=identifier]
                        row['destination']='m05-p09'
                    unchanged_except(before,store(page),'dujia-prototype-works');row['result']='exact radio/checkbox source consumed; new draft for start action, existing editors defer write until explicit parent draft save'
                elif index==37:
                    row['control_label']='保留草稿并取消';dialog.get_by_role('button',name=row['control_label'],exact=True).click();page.wait_for_url('**/m05-p03.html*')
                    new=read(page,'dujia-prototype-works');old=json.loads(before['dujia-prototype-works']);target=next(v for v in new if v['id']=='work-running');was=next(v for v in old if v['id']=='work-running')
                    assert target['status']=='draft'
                    for k,v in was.items():
                        if k not in ['status','updatedAt']:assert target[k]==v
                    assert [v for v in old if v['id']!='work-running']==[v for v in new if v['id']!='work-running'];unchanged_except(before,store(page),'dujia-prototype-works')
                    row.update(destination='m05-p03',result='generating work becomes draft with all input/source fields retained; editor reached; other works preserved')
                elif index==38:
                    row.update(control_label='复制作品链接',native_controls=['当前原型作品链接']);field=dialog.get_by_label('当前原型作品链接',exact=True)
                    expect(field).to_have_value(url);expect(field).to_have_attribute('readonly','');field.select_text();expect(field).to_be_focused()
                    dialog.get_by_role('button',name=row['control_label'],exact=True).click()
                    if mode=='copy':
                        expect(dialog).to_have_count(0);expect(page.locator('.prototype-toast')).to_contain_text('作品链接已复制');assert page.evaluate('navigator.clipboard.readText()')==url
                    else:
                        expect(dialog.locator('h2')).to_have_text('复制作品链接');expect(dialog.get_by_label('当前原型作品链接',exact=True)).to_have_value(url)
                        expect(dialog.get_by_label('当前原型作品链接',exact=True)).to_be_focused();dialog.get_by_role('button',name='关闭',exact=True).click();expect(dialog).to_have_count(0)
                    assert store(page)==before and page.url==url;row['result']='actual same-device URL copied; rejection exposes selected readonly URL for manual copy; data preserved'
                assert not errors;row['passed']=True
            except Exception:row['error']=traceback.format_exc()
            rows.append(row);context.close();assert source()==files
            report=dict(files=files,script_sha256=sha(Path(__file__)),observations_sha256=sha(obspath),fixture_scripts={v:sha(ROOT/v) for v in MODULES.values()},expected_cases=len(CASES),results=rows,accepted_pages=0)
            tmp=OUT/'results.json.tmp';tmp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');tmp.replace(OUT/'results.json')
            print(('PASS ' if row['passed'] else 'FAIL ')+str(index)+' '+mode,flush=True)
        browser.close()
    print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
if __name__=='__main__':main()
