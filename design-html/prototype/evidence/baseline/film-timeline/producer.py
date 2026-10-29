"""Real source IDs/count/order must drive the film timeline, not the three baked nodes."""
import argparse,hashlib,json,re,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations

ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def dependencies():
    text=(DEMO/'custom/m05-p05.html').read_text(encoding='utf-8');files={'custom/m05-p05.html','pages/m05-p05.html','assets/m05-p05-art.webp','assets/font.ttf','assets/prototype-components.css','assets/book-v2/paper.webp'}
    files.update('assets/'+p for p in re.findall(r'(?:src|href)="\.\./assets/([^"]+)"',text))
    return {p:sha(DEMO/p) for p in sorted(files)}

def prepare(p,fixture,count):
    fixture['seed'](p,'m05-p05');ids=[f'film-source-{i}' for i in reversed(range(count))]
    p.evaluate('ids=>{const records=PrototypeRecords.all(),base=records.find(r=>r.type==="diary"),photo=records.find(r=>r.type==="photo");localStorage.setItem("dujia-prototype-records",JSON.stringify(Array.from({length:7},(_,i)=>({...base,id:"film-source-"+i,title:"片段"+i+"："+"真正可编辑的长标题".repeat(5),date:"2026-10-05",image:i%2?photo.image:null}))));const works=PrototypeWorkshop.all();works.find(w=>w.id==="work-film").sourceIds=ids;localStorage.setItem("dujia-prototype-works",JSON.stringify(works));}',ids)
    p.reload();p.evaluate('document.fonts.ready');return ids

def pick(p,kind,ids=None,cancel=False):
    p.get_by_role('button',name='选择共同片段',exact=True).click();p.get_by_role('button',name={'diary':'共同日记','photo':'相册照片','moment':'重要时刻'}[kind],exact=True).click()
    if ids is not None:
        for i in ids:p.locator('dialog input[value="'+i+'"]').check()
    p.get_by_role('button',name='取消' if cancel else '使用这些素材',exact=True).click()

def flow(p,name,fixture):
    ids=prepare(p,fixture,3);before=fixture['store'](p)
    if name=='cancel-selection':pick(p,'diary',['film-source-6'],cancel=True);assert p.locator('.film-clip').evaluate_all('ns=>ns.map(e=>e.dataset.sourceId)')==ids;assert fixture['store'](p)==before
    elif name=='selection-limit':
        pick(p,'diary',[f'film-source-{i}' for i in range(7)]);expect(p.locator('.prototype-toast')).to_contain_text('1～6');assert p.locator('.film-clip').evaluate_all('ns=>ns.map(e=>e.dataset.sourceId)')==ids;assert fixture['store'](p)==before
    elif name=='remove-save-order':
        p.locator('[data-source-id="film-source-1"]').click();expect(p.locator('.film-sequence')).to_have_text(['1','2']);p.get_by_role('button',name='暂存创作草稿',exact=True).click();p.wait_for_url('**/m05-p09.html');saved=p.evaluate('PrototypeWorkshop.find("work-film").sourceIds');assert saved==['film-source-2','film-source-0'];p.goto('http://127.0.0.1:8765/pages/m05-p05.html?id=work-film');assert p.locator('.film-clip').evaluate_all('ns=>ns.map(e=>e.dataset.sourceId)')==saved
    elif name=='select-generate':
        pick(p,'diary',['film-source-1','film-source-4']);expect(p.locator('.film-sequence')).to_have_text(['1','2']);assert fixture['store'](p)==before;p.locator('#generate').click();p.wait_for_url('**/m05-p06.html?id=work-film');saved=p.evaluate('PrototypeWorkshop.find("work-film")');assert saved['sourceIds']==['film-source-1','film-source-4'] and saved['status']=='generating'
    elif name=='private-reference':
        p.evaluate('()=>{const records=PrototypeRecords.all();records.find(r=>r.id==="film-source-1").visibility="private";records.find(r=>r.id==="film-source-1").image="/never-request-private-film.png";localStorage.setItem("dujia-prototype-records",JSON.stringify(records));}');requests=[];p.on('request',lambda r:requests.append(r.url));p.reload();expect(p.locator('.film-clip')).to_have_count(2);expect(p.locator('.film-sequence')).to_have_text(['1','2']);before=fixture['store'](p);p.locator('#generate').click();expect(p.locator('.prototype-toast')).to_contain_text('不可见');assert fixture['store'](p)==before;assert not any('never-request-private-film' in r for r in requests)
    elif name=='image-failure':
        p.evaluate('()=>{const records=PrototypeRecords.all();records.find(r=>r.id==="film-source-1").image="/missing-film-image.png";localStorage.setItem("dujia-prototype-records",JSON.stringify(records));}');p.reload();before=fixture['store'](p);expect(p.locator('.film-preview[data-kind=unavailable]')).to_have_count(1);p.locator('[data-source-id="film-source-1"]').click();expect(p.locator('.film-clip')).to_have_count(2);assert fixture['store'](p)==before
    elif name.startswith('dirty-'):
        pick(p,'diary',['film-source-6']);back=lambda:p.go_back() if name.endswith('browser') else p.locator('.back').click();back();expect(p.locator('dialog h2')).to_have_text('是否放弃当前修改？');p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('[data-source-id="film-source-6"]')).to_have_count(1);back();p.get_by_role('button',name='放弃修改',exact=True).click();p.wait_for_function('!location.pathname.endsWith("m05-p05.html")');assert fixture['store'](p)==before
    else:raise AssertionError(name)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['baseline','current'],required=True);args=parser.parse_args();out=ROOT/f'evidence/{args.stage}/film-timeline';out.mkdir(parents=True,exist_ok=True);assert not (out/'results.json').exists(),'Preserve earlier reports before re-running'
    fixture=declarations('verify_workshop_controls.py');files=dependencies();cases=[('layout',(w,n)) for w in [320,360,390,414,430] for n in [0,1,3,6]]
    if args.stage=='current':
        catalog=json.loads((ROOT/'evidence/current/page-contracts.json').read_text(encoding='utf-8'));cases += [('control',r) for r in next(p for p in catalog['pages'] if p['id']=='m05-p05')['control_evidence']]
        cases += [('flow',n) for n in ['cancel-selection','selection-limit','remove-save-order','select-generate','private-reference','image-failure','dirty-button','dirty-browser']]
    rows=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=browser.version
        for kind,value in cases:
            context=browser.new_context(viewport={'width':value[0] if kind=='layout' else 390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=context.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row={'kind':kind,'value':value,'passed':False}
            try:
                if kind=='control':fixture['control'](p,'m05-p05',value,value['contract'])
                elif kind=='flow':flow(p,value,fixture)
                else:
                    width,count=value;ids=prepare(p,fixture,count);before=fixture['store'](p)
                    if width==390:p.screenshot(path=str(out/f'{count}-clips.png'),full_page=True)
                    expect(p.locator('.clips')).to_have_attribute('data-film-count',str(count))
                    assert p.locator('.film-clip').evaluate_all('ns=>ns.map(e=>e.dataset.sourceId)')==ids
                    assert p.locator('.film-sequence').all_text_contents()==[str(i+1) for i in range(count)]
                    assert p.locator('.art-clips').evaluate('e=>!getComputedStyle(e).backgroundImage.includes("m05-p05-art")'),'The three unrelated baked timeline nodes remain visible'
                    if count:
                        expect(p.locator('.film-preview')).to_have_count(count);expect(p.locator('.film-preview[data-kind=note]')).to_have_count((count+1)//2)
                        assert p.locator('.film-clip').evaluate_all('nodes=>nodes.every(e=>e.scrollWidth<=e.clientWidth+1&&e.getBoundingClientRect().height>=44)')
                        last=p.locator('.film-clip').last;last.scroll_into_view_if_needed();last.focus();expect(last).to_be_focused();assert p.locator('.clips').evaluate('e=>e.scrollWidth<=e.clientWidth+1')
                        if count==6:assert p.locator('.clips').evaluate('e=>e.scrollHeight>e.clientHeight&&e.scrollTop>0')
                        images=p.locator('.film-preview img')
                        if images.count():p.wait_for_function('()=>[...document.querySelectorAll(".film-preview img")].every(i=>i.complete&&i.naturalWidth>0)')
                    else:expect(p.locator('.film-empty')).to_have_count(1)
                    assert fixture['store'](p)==before
                assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc()
            row['page_errors']=errors;rows.append(row);context.close();assert dependencies()==files;print(('PASS ' if row['passed'] else 'FAIL ')+kind+' '+str(value),flush=True)
        browser.close()
    (out/'results.json').write_text(json.dumps({'dependency_files':files,'producer_sha256':sha(Path(__file__)),'fixture_sha256':sha(ROOT/'verify_workshop_controls.py'),'browser':version,'results':rows,'scope':'One film editor timeline, five widths,0/1/3/6 actual source IDs in stored order, original initial controls and eight named selection/privacy/image/save/return outcomes. Not full114 or human acceptance.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.stage=='baseline':(out/'producer.py').write_bytes(Path(__file__).read_bytes())
    print('Film timeline:',sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
