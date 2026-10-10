"""Check the new transient skeleton geometry on its 10 actual surfaces at 5 widths."""
import json,traceback
from playwright.sync_api import sync_playwright
from verify_shared_list_loading import CASES,fixture,PROBE
from verify_pet_controls import ROOT,BASE,source

METRICS=PROBE.replace('busy:!!parent,layout:', '''geometry:{left:rect.left,right:rect.right,width:rect.width,viewport:innerWidth,
 children:[...node.querySelectorAll('.prototype-component-skeleton')].map(e=>{const r=e.getBoundingClientRect();return {left:r.left,right:r.right,height:r.height,width:r.width}})},busy:!!parent,layout:''')

def main():
    files=source();rows=[]
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for width in [320,360,390,414,430]:
            for page_id,query,*_ in CASES:
                context=browser.new_context(viewport={'width':width,'height':844},reduced_motion='reduce');context.add_init_script(METRICS)
                p=context.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row={'page':page_id,'width':width}
                try:
                    p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-06");for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',fixture('populated',page_id))
                    p.goto(BASE+'pages/'+page_id+'.html'+query);p.wait_for_timeout(650)
                    observations=p.evaluate('window.loadingProbe');row['observations']=observations
                    assert len(observations)==1 and not errors
                    probe=observations[0];g=probe['geometry'];assert probe['layout']and g['left']>=-1 and g['right']<=width+1,g
                    assert len(g['children'])==3
                    assert all(c['height']>0 and c['width']>0 and c['left']>=g['left']-1 and c['right']<=g['right']+1 for c in g['children']),g
                    row['passed']=True
                except Exception:row.update(passed=False,failure=traceback.format_exc()[-1800:])
                row['errors']=errors;rows.append(row);context.close();assert source()==files
            print(str(width)+'px: '+str(sum(r['passed']for r in rows if r['width']==width))+'/10',flush=True)
        browser.close()
    (ROOT/'evidence/current/shared-loading-widths.json').write_text(json.dumps({'files':files,'results':rows,'scope':'Transient skeleton horizontal bounds and positive child dimensions; not full-page safe-area/keyboard acceptance'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'cases':len(rows),'passed':sum(r['passed']for r in rows)}))
    raise SystemExit(0 if all(r['passed']for r in rows)else 1)

if __name__=='__main__':main()
