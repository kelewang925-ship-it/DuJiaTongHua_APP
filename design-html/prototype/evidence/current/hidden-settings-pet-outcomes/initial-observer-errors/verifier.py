"""Concrete settings and pet choice consumers, including deferred outfit/room saves."""
import hashlib,json,re,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import MODULES,declarations
from audit_runtime import INIT
from verify_pet_controls import ROOT,source

OUT=ROOT/'evidence/current/hidden-settings-pet-outcomes'
UNLOCK={74:('bow','格纹蝴蝶结',20,0),75:('star-bow','星星领结',0,0),76:('peach-hat','蜜桃帽子',0,0),77:('crown','星光皇冠',0,30),79:('plaid-rug','格纹地毯',20,0),80:('moon-rug','月亮地毯',0,0)}
CASES=[(44,'请求解除关联'),*[(i,'编辑标签') for i in [47,48,49]],(50,'开通演示会员'),(54,'确认退出'),(58,'确认退出'),(61,'查看恢复原始副本'),(62,'确认清理'),*[(i,'解锁并选择') for i in UNLOCK],*[(83,s) for s in ['共同日记','共同照片','共同重要时刻']],*[(95,s) for s in ['小狗 · 正在共同照顾','小猫 · 首次领养可选','小兔 · 首次领养可选','小狐狸 · 首次领养可选']],(96,'确认暂停'),(99,'修改宠物名字')]
CACHE=['dujia-prototype-search-history','dujia-prototype-last-query','dujia-diary-list-state','dujia-photo-album-state']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stores(p):return p.evaluate('({local:{...localStorage},session:{...sessionStorage}})')
def read(p,key):return p.evaluate('k=>JSON.parse(localStorage.getItem(k))',key)
def only(before,after,key):
    a=dict(before['local']);b=dict(after['local']);a.pop(key,None);b.pop(key,None);assert a==b,'Unrelated local data changed'

def main():
    OUT.mkdir(exist_ok=True);files=source();obspath=ROOT/'evidence/current/hidden-overlay-observations.json';observed=json.loads(obspath.read_text(encoding='utf-8'))
    fixtures={k:declarations(v) for k,v in MODULES.items()};rows=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for index,label in CASES:
            context=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');context.add_init_script(INIT)
            page=context.new_page();page.set_default_timeout(6000);page.set_default_navigation_timeout(20000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            row=dict(observation_index=index,control_label=label,passed=False,errors=errors)
            try:
                original=observed['results'][index];fixtures[original['group']]['seed'](page,original['page'])
                if index in UNLOCK:
                    page.evaluate('()=>{const k="dujia-prototype-pet",p=JSON.parse(localStorage.getItem(k));p.coins=100;p.stars=100;p.affinity=200;localStorage.setItem(k,JSON.stringify(p))}');page.reload();expect(page.locator('.screen')).to_have_attribute('aria-busy','false')
                    row['fixture']='100 coins,100 stars,200 affinity; existing story condition retained'
                if index==61:page.evaluate('localStorage.setItem("dujia-prototype-record-recovery-g3",JSON.stringify("original recovery bytes"))')
                if index==62:page.evaluate('keys=>{for(const k of keys){localStorage.setItem(k,"cached-local");sessionStorage.setItem(k,"cached-session")}}',CACHE)
                before=stores(page);url=page.url
                tags=page.evaluate('PrototypePreferences.tags()') if index in [47,48,49] else None
                page.locator(original['selector']).click();dialog=page.locator('dialog[open]')
                expect(dialog.locator('h2')).to_have_text(original['overlays'][0]['title'])
                dialog.get_by_role('button',name=label,exact=True).click()
                if index==44:
                    page.wait_for_function('JSON.parse(localStorage.getItem("dujia-prototype-relationship")).unlinkPending?.id')
                    old=json.loads(before['local']['dujia-prototype-relationship']);new=read(page,'dujia-prototype-relationship');assert new['bound']==old['bound']
                    pending=new.pop('unlinkPending');assert pending['createdAt']>0;assert new==old
                    only(before,stores(page),'dujia-prototype-relationship');row['result']='unlink request persisted; relationship remains bound and all original profile/content retained'
                elif index in [47,48,49]:
                    expect(dialog.locator('h2')).to_have_text('编辑标签');form=dialog.locator('form');target=next(t for t in tags if t['name']==original['overlays'][0]['title'])
                    wanted='改名'+str(index);expect(form.get_by_label('标签名称',exact=True)).to_have_value(target['name'])
                    form.get_by_label('标签名称',exact=True).fill(wanted);form.get_by_role('button',name='保存标签',exact=True).click();expect(dialog).to_have_count(0)
                    found=page.evaluate('PrototypePreferences.tags()');assert next(t for t in found if t['id']==target['id'])['name']==wanted
                    records=read(page,'dujia-prototype-records');assert all(target['name'] not in r.get('tags',[]) for r in records)
                    old=dict(before['local']);new=stores(page)['local']
                    for key in ['dujia-prototype-tags','dujia-prototype-records']:old.pop(key,None);new.pop(key,None)
                    assert old==new;row['result']='edit form prefilled; same tag id renamed; referenced record tags renamed, unrelated data preserved'
                elif index==50:
                    page.wait_for_function('JSON.parse(localStorage.getItem("dujia-prototype-membership"))?.expiresAt>Date.now()')
                    expect(page.locator('.open')).to_be_disabled();only(before,stores(page),'dujia-prototype-membership');row['result']='local demo membership expiry persisted; purchase button disabled; no unrelated data change'
                elif index in [54,58]:
                    page.wait_for_url('**/m01-p01.html*');new=read(page,'dujia-prototype-session');old=json.loads(before['local']['dujia-prototype-session']);old['loggedIn']=False;assert old==new
                    assert page.evaluate('sessionStorage.getItem("dujia-prototype-challenge")') is None
                    only(before,stores(page),'dujia-prototype-session');row.update(destination='m01-p01',result='logout preserves content and session fields; clears login flag/challenge; welcome page reached')
                elif index==61:
                    expect(dialog.locator('h2')).to_have_text('恢复原始副本');expect(dialog).to_contain_text('1 份原始副本')
                    expect(dialog.get_by_role('button',name=re.compile('^原始副本 1'))).to_have_count(1)
                    dialog.get_by_role('button',name='关闭',exact=True).click();expect(dialog).to_have_count(0);assert stores(page)==before
                    row['result']='opens recovery archive chooser with seeded original copy; closing preserves all local/session data'
                elif index==62:
                    expect(page.locator('.prototype-toast')).to_contain_text('浏览记录缓存已清理');after=stores(page)
                    for location in ['local','session']:
                        old=dict(before[location]);new=dict(after[location])
                        for key in CACHE:old.pop(key,None);assert key not in new
                        assert old==new
                    row['result']='only four declared cache keys removed from both stores; records/images/drafts preserved'
                elif index in UNLOCK:
                    item,name,coins,stars=UNLOCK[index];key='dujia-prototype-pet';ownership='owned' if index<79 else 'ownedRoom'
                    page.wait_for_function('([k,field,name])=>JSON.parse(localStorage.getItem(k))[field]?.includes(name)',[key,ownership,name])
                    pet=read(page,key);old=json.loads(before['local'][key]);assert pet['coins']==old['coins']-coins and pet['stars']==old['stars']-stars
                    assert pet.get('outfit')==old.get('outfit') and pet.get('room')==old.get('room')
                    expect(page.locator(f'[data-item="{item}"]')).to_have_attribute('aria-pressed','true')
                    only(before,stores(page),key)
                    page.locator('#save' if index<79 else '.save').click()
                    if index<79:
                        page.wait_for_function('name=>JSON.parse(localStorage.getItem("dujia-prototype-pet")).outfit===name',name)
                    else:
                        page.wait_for_url('**/m07-p14.html*');assert name in read(page,key)['room'].values()
                    final=read(page,key);assert final['coins']==100-coins and final['stars']==100-stars
                    assert len([v for v in final['logs'] if v['type']=='unlock' and v.get('itemId')==item])==1
                    row['result']='ownership and exact resource cost saved once; selection initially preview only; explicit parent save persists outfit/room'
                elif index==83:
                    expected={'共同日记':('audit-diary','record'),'共同照片':('audit-photo','record'),'共同重要时刻':('audit-moment','moment')}[label]
                    page.wait_for_function('([id,kind])=>JSON.parse(localStorage.getItem("dujia-prototype-pet")).logs.some(v=>v.sourceId===id&&v.sourceKind===kind)',list(expected))
                    logs=read(page,'dujia-prototype-pet')['logs'];assert len([v for v in logs if v.get('sourceId')==expected[0] and v.get('sourceKind')==expected[1]])==1
                    only(before,stores(page),'dujia-prototype-pet');row['result']='exact selected shared record linked once with correct source kind; other data preserved'
                elif index==95:
                    breed=label.split(' · ')[0];expect(dialog.locator('h2')).to_have_text(breed+(' · 已共同领养' if breed=='小狗' else ' · 尚未领养'))
                    expect(dialog.locator('[role=img]')).to_have_attribute('aria-label',breed+'领养插画')
                    dialog.get_by_role('button',name='了解了',exact=True).click();expect(dialog).to_have_count(0);assert stores(page)==before and page.url==url
                    row['result']='selected breed information and matching illustration shown; existing pet and growth never replaced'
                elif index==96:
                    page.wait_for_url('**/m07-p25.html*');old=json.loads(before['local']['dujia-prototype-pet']);pet=read(page,'dujia-prototype-pet');assert pet['care'] is False
                    for key in ['name','kind','owned','ownedRoom','food','coins','stars','room','outfit']:assert pet.get(key)==old.get(key)
                    assert all(v in pet['logs'] for v in old['logs']);only(before,stores(page),'dujia-prototype-pet');row.update(destination='m07-p25',result='care paused; identity/inventory/growth retained; settings page reached')
                elif index==99:
                    expect(dialog.locator('h2')).to_have_text('宠物名字');form=dialog.locator('form');expect(form.get_by_label('宠物名字',exact=True)).to_have_value(read(page,'dujia-prototype-pet')['name'])
                    form.get_by_label('宠物名字',exact=True).fill('小星星');form.locator('button[type=submit]').click();expect(dialog).to_have_count(0)
                    old=json.loads(before['local']['dujia-prototype-pet']);pet=read(page,'dujia-prototype-pet');assert pet.pop('name')=='小星星';old.pop('name');pet.pop('updatedAt',None);old.pop('updatedAt',None);assert pet==old
                    only(before,stores(page),'dujia-prototype-pet');row['result']='rename form prefilled; exact name persisted; all other pet/content fields retained'
                assert not errors;row['passed']=True
            except Exception:row['error']=traceback.format_exc()
            rows.append(row);context.close();assert source()==files
            report=dict(files=files,script_sha256=sha(Path(__file__)),observations_sha256=sha(obspath),fixture_scripts={v:sha(ROOT/v) for v in MODULES.values()},expected_cases=len(CASES),results=rows,accepted_pages=0)
            temporary=OUT/'results.json.tmp';temporary.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temporary.replace(OUT/'results.json')
            print(('PASS ' if row['passed'] else 'FAIL ')+str(index)+' '+label,flush=True)
        browser.close()
    print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
if __name__=='__main__':main()
