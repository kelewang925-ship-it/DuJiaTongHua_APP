from pathlib import Path
import json,traceback,sys
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
BASE='http://127.0.0.1:8765/'
OUT=Path(__file__).resolve().parent/('evidence/baseline' if '--baseline' in sys.argv else 'evidence/current')
CASES=[('m03-p05','返回日记列表','m03-p06'),('m03-p08','返回日记列表','m03-p06'),('m03-p11','返回相册','m03-p09'),('m03-p12','返回相册','m03-p09'),('m08-p04','返回书架','m08-p02'),('m08-p16','返回书架','m08-p02'),('m08-p21','返回书架','m08-p02')]
rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for width in ([390] if '--baseline' in sys.argv else [320,375,390,414,430]):
  for page,label,target in CASES+[('m08-p05','重新加载','m08-p05')]:
   c=b.new_context(viewport={'width':width,'height':844},reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
   try:
    p.goto(BASE+'prototype/review.html');fixture=data(page=='m08-p05');p.evaluate("data=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(data))localStorage.setItem(k,JSON.stringify(v));}",fixture);before=p.evaluate('JSON.stringify({...localStorage})')
    if page=='m08-p05':p.evaluate("sessionStorage.setItem('dujia-prototype-fail-next','book-load')")
    p.goto(BASE+'pages/'+page+'.html?id='+('book-state' if page=='m08-p05' else 'gone'))
    state=p.locator('.prototype-component-state[role=alert]');expect(state).to_be_visible();button=state.get_by_role('button',name=label,exact=True);button.scroll_into_view_if_needed();box=button.bounding_box();assert box['width']>=44 and box['height']>=44
    assert p.evaluate('document.documentElement.scrollWidth')==width
    hit=button.evaluate("e=>{const r=e.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return hit===e||e.contains(hit)}");assert hit
    p.screenshot(path=str(OUT/f'shared-state-{page}-{width}.png'),full_page=True);button.click();p.wait_for_url('**/'+target+'.html*')
    if page=='m08-p05':expect(p.locator('.prototype-component-state[role=alert]')).to_have_count(0);expect(p.locator('.next')).to_be_visible()
    assert p.evaluate('JSON.stringify({...localStorage})')==before;assert not errors,errors;row=dict(page=page,width=width,passed=True)
   except Exception:row=dict(page=page,width=width,passed=False,failure=traceback.format_exc()[-1700:])
   row.update(errors=errors,url=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+page+' '+str(width),flush=True);c.close()
 b.close()
(OUT/'shared-state-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
