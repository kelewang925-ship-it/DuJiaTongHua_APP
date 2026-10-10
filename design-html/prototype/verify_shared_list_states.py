"""Exercise real list Empty/Error actions and geometry with isolated local seeds."""
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from verify_shared_list_loading import CASES,fixture
from verify_pet_controls import ROOT,BASE,source

EMPTY=[
 ('search','m03-p04','重新搜索','m03-p03','没有找到相关记录'),
 ('diary','m03-p06','写第一篇日记','m03-p05','还没有日记'),
 ('diary-draft','m03-p06','写第一篇日记','m03-p05','还没有草稿'),
 ('diary-filter','m03-p06','清除筛选',None,'没有符合条件的日记'),
 ('photo-filter','m03-p10','清除筛选',None,'没有符合条件的照片'),
 ('capsule-sealed','m04-p12','写给未来的我们','m04-p13','还没有等待开启的胶囊'),
 ('capsule-opened','m04-p12','写给未来的我们','m04-p13','还没有已经开启的胶囊'),
 ('capsule-draft','m04-p12','写给未来的我们','m04-p13','还没有胶囊草稿'),
 ('work','m05-p09','开始一次创作','m05-p02','这里暂时没有作品'),
 ('work-favorites','m05-p09','查看全部作品',None,'还没有收藏的作品'),
 ('drafts','m06-p04','写第一篇日记','m03-p05','还没有草稿'),
 ('pet-stories','m07-p18','写一页成长故事',None,'第一段故事还在等你'),
]

def main():
    files=source();baseline='--baseline'in sys.argv;widths=[390]if baseline else[320,360,390,414,430];rows=[]
    specs=[(p,'error',p,query,retry,None,None,key)for p,query,target,key,retry,label,refresh in CASES]
    specs += [(name,'empty',page,'?q=不存在'if name=='search'else'',action,dest,title,None)for name,page,action,dest,title in EMPTY]
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for width in widths:
            for name,kind,page_id,query,action,dest,title,key in specs:
                context=browser.new_context(viewport={'width':width,'height':844},reduced_motion='reduce');p=context.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
                row={'case':name,'kind':kind,'page':page_id,'width':width}
                try:
                    d=fixture('populated'if kind=='error'or name in ['diary-filter','photo-filter','work-favorites']else'empty',page_id)
                    if name=='diary-filter':d['dujia-prototype-records']=[v for v in d['dujia-prototype-records']if v['visibility']=='shared']
                    if name=='photo-filter':
                        for v in d['dujia-prototype-records']:v['tags']=[]
                    p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-06");for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',d)
                    if key:p.evaluate('k=>sessionStorage.setItem("dujia-prototype-fail-next",k)',key)
                    if name.startswith('diary-'):p.evaluate('d=>sessionStorage.setItem("dujia-diary-list-state",JSON.stringify(d))',{'tab':'draft'if name=='diary-draft'else'all','visibility':'private'if name=='diary-filter'else'all'})
                    if name=='photo-filter':p.evaluate('sessionStorage.setItem("dujia-photo-album-state",JSON.stringify({tab:2,visibility:"all"}))')
                    p.goto(BASE+'pages/'+page_id+'.html'+query);p.wait_for_timeout(650)
                    if name in ['capsule-opened','capsule-draft']:p.locator('.tabs button').nth(1 if name=='capsule-opened'else 2).click()
                    if name=='work-favorites':p.locator('.folder').click()
                    state=p.locator('.prototype-component-state[data-kind='+kind+']');assert state.count()==1,'Expected shared '+kind+' state'
                    if title:expect(state.get_by_role('heading',name=title,exact=True)).to_be_visible()
                    assert state.get_attribute('role')==('alert'if kind=='error'else'region')
                    button=state.get_by_role('button',name=action,exact=True);expect(button).to_be_visible();button.scroll_into_view_if_needed()
                    geometry=button.evaluate('(e)=>{const r=e.getBoundingClientRect();const p=e.closest(".prototype-component-state").getBoundingClientRect();return {left:r.left,right:r.right,width:r.width,height:r.height,stateLeft:p.left,stateRight:p.right}}');row['geometry']=geometry
                    assert geometry['height']>=44 and geometry['width']>=44 and geometry['left']>=-1 and geometry['right']<=width+1,geometry
                    before=p.evaluate('JSON.stringify({...localStorage})');button.click()
                    if kind=='error':
                        p.wait_for_timeout(650);expect(state).to_have_count(0);expect(p.locator('.prototype-component-loading')).to_have_count(0)
                        assert p.evaluate('JSON.stringify({...localStorage})')==before,'Retry modified saved data'
                        visible={'m03-p04':'共同日记','m03-p06':'共同日记','m03-p10':'共同照片','m04-p01':'共同重要时刻','m04-p07':'未来的纪念日','m04-p12':'未来的信','m05-p09':'实际工坊作品','m06-p04':'共同日记','m07-p03':'团团','m07-p18':'实际成长故事'}[page_id]
                        assert visible in p.locator('.screen').inner_text(),visible
                    elif dest:expect(p).to_have_url(__import__('re').compile(dest+r'\.html(?:\?|$)'))
                    elif name=='pet-stories':expect(p.get_by_role('dialog')).to_be_visible();expect(p.get_by_role('textbox')).to_be_visible()
                    else:
                        expect(state).to_have_count(0);assert ('共同照片'if name=='photo-filter'else'实际工坊作品'if name=='work-favorites'else'共同日记')in p.locator('.screen').inner_text()
                    assert not errors,errors;row['passed']=True
                except Exception:row.update(passed=False,failure=traceback.format_exc()[-2300:])
                row['errors']=errors;rows.append(row);context.close();assert source()==files
            print(str(width)+'px '+str(sum(r['passed']for r in rows if r['width']==width))+'/22',flush=True)
        browser.close()
    path=ROOT/('evidence/baseline/shared-list-states-before.json'if baseline else'evidence/current/shared-list-states-results.json')
    path.write_text(json.dumps({'files':files,'results':rows,'scope':'10 load Error retries plus 12 Empty contexts, real actions and five-width action geometry'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'cases':len(rows),'passed':sum(r['passed']for r in rows)}));raise SystemExit(0 if all(r['passed']for r in rows)else 1)

if __name__=='__main__':main()
