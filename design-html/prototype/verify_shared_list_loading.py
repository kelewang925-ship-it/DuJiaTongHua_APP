"""Observe real transient skeletons and recover real failure branches, without timer changes."""
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from audit_runtime import INIT
from verify_pet_controls import ROOT,BASE,source

CASES=[
 ('m03-p04','?q=共同','.prototype-search-results','record-search','重试搜索','正在翻找回忆…',None),
 ('m03-p06','','.prototype-diary-list','diary-load','重新加载日记','正在打开日记…','.prototype-diary-refresh'),
 ('m03-p10','','.prototype-photo-grid','photo-load','重试加载','正在打开相册…','.prototype-photo-refresh'),
 ('m04-p01','','.prototype-moment-cards','moment-load','重试加载时刻册','正在打开时刻册…','.prototype-moment-refresh'),
 ('m04-p07','','.prototype-anniversary-entries','anniversary-load','重试加载纪念日','正在打开纪念日…','.prototype-anniversary-refresh'),
 ('m04-p12','','.cards','capsule-load','重试加载胶囊','正在打开胶囊架…',None),
 ('m05-p09','','.prototype-work-list','work-load','重试加载创作','正在翻开创作集…','.prototype-work-refresh'),
 ('m06-p04','','.prototype-settings-drafts','settings-drafts-load','重试加载草稿','正在收拾草稿箱…','.prototype-settings-refresh'),
 ('m07-p03','','.screen','pet-load','重新加载','正在读取小伙伴的记录…',None),
 ('m07-p18','','.screen','pet-life-load','重新加载','正在打开宠物的共同回忆…',None),
]
# Observe insertion before the actual 400ms timeout expires. No clocks or product timer mocks.
PROBE="""window.loadingProbe=[];new MutationObserver(()=>{
 for(const node of document.querySelectorAll('.prototype-component-loading')) {
  if(node.dataset.loadingObserved)continue;node.dataset.loadingObserved='true';
  const parent=node.closest('[aria-busy=true]'),style=getComputedStyle(node),rect=node.getBoundingClientRect();
  window.loadingProbe.push({label:node.textContent,role:node.getAttribute('role'),live:node.getAttribute('aria-live'),
    skeletons:node.querySelectorAll('.prototype-component-skeleton[aria-hidden=true]').length,
    busy:!!parent,layout:rect.width>0&&rect.height>0&&style.visibility!=='hidden',
    disabled:[...document.querySelectorAll('button:disabled')].map(b=>b.className)});
 }
}).observe(document,{childList:true,subtree:true,attributes:true,attributeFilter:['aria-busy']});"""

def fixture(scenario,page):
    d=data(scenario!='empty');d['dujia-prototype-session']={'loggedIn':True}
    if page.startswith('m07-'):
        d=data(True);d['dujia-prototype-session']={'loggedIn':True}
        if scenario=='empty':d['dujia-prototype-pet']['logs']=[]
    if page=='m06-p04' and scenario!='empty':d['dujia-prototype-records'][0]['status']='draft'
    return d

def main():
    before=source();results=[];baseline='--baseline'in sys.argv
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for page_id,query,target,key,retry,label,refresh in CASES:
            for scenario in ['populated','empty','failure-retry']:
                if '--empty-routes'in sys.argv and (scenario!='empty' or page_id not in ['m03-p10','m04-p01','m04-p07']):continue
                context=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce')
                context.add_init_script(INIT);context.add_init_script(PROBE)
                p=context.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
                row={'page':page_id,'scenario':scenario}
                try:
                    p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-06");for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',fixture(scenario,page_id))
                    if scenario=='failure-retry':p.evaluate('key=>sessionStorage.setItem("dujia-prototype-fail-next",key)',key)
                    p.goto(BASE+'pages/'+page_id+'.html'+query)
                    p.wait_for_timeout(650)
                    if scenario=='failure-retry':
                        button=p.get_by_role('button',name=retry,exact=True);expect(button).to_be_visible();button.click();p.wait_for_timeout(650);expect(button).to_have_count(0)
                        row['failure_retry_recovered']=True
                    expect(p.locator('.prototype-component-loading')).to_have_count(0)
                    assert p.locator('[aria-busy=true]').count()==0
                    empty_route={'m03-p10':'m03-p09','m04-p01':'m04-p02','m04-p07':'m04-p08'}.get(page_id) if scenario=='empty' else None
                    assert (empty_route or page_id)+'.html'in p.url
                    if refresh and not empty_route:expect(p.locator(refresh)).to_be_enabled()
                    assert not errors,errors
                    probes=p.evaluate('window.loadingProbe');row['loading_observations']=probes
                    if empty_route:
                        assert not probes
                        expect(p.get_by_role('button',name={'m03-p09':'添加第一张照片','m04-p02':'新建重要时刻','m04-p08':'添加第一个纪念日'}[empty_route],exact=True)).to_be_visible()
                        row['empty_redirect_verified']=empty_route
                    assert len(probes)==(0 if empty_route else 2 if scenario=='failure-retry'else 1),probes
                    for probe in probes:
                        assert label in probe['label'] and probe['role']=='status' and probe['live']=='polite'
                        assert probe['skeletons']==3 and probe['busy']and probe['layout'],probe
                        if refresh:assert any(refresh[1:]in v.split()for v in probe['disabled']),probe
                    row['passed']=True
                except Exception:row.update(passed=False,failure=traceback.format_exc()[-2200:])
                row['errors']=errors;results.append(row);context.close();assert source()==before
                print(page_id+' '+scenario+' '+('PASS'if row['passed']else'FAIL'),flush=True)
        browser.close()
    dest=ROOT/('evidence/baseline/shared-list-loading-empty-route-selector.json'if '--empty-routes'in sys.argv else'evidence/baseline/shared-list-loading-before.json'if baseline else'evidence/current/shared-list-loading-results.json')
    dest.write_text(json.dumps({'files':before,'results':results,'scope':'10 data-load functions: actual transient DOM, empty/populated and semantic failure/retry, same 400ms timers'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'cases':len(results),'passed':sum(r['passed']for r in results)}))
    raise SystemExit(0 if all(r['passed']for r in results)else 1)

if __name__=='__main__':main()
