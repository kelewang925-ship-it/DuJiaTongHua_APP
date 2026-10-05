from pathlib import Path
import json,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
OUT=Path(__file__).resolve().parent/'evidence/current'
BASE='http://127.0.0.1:8765/'
CASES=[('m03-p01',False),('m03-p02',True),('m04-p01',True),('m04-p02',False),('m05-p01',True),('m06-p01',True),('m07-p01',True),('m07-p03',True),('m07-p04',False)]
rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for width in [320,375,390,414,430]:
  for page,populated in CASES:
   c=b.new_context(viewport={'width':width,'height':844},reduced_motion='reduce');p=c.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
   try:
    p.goto(BASE+'prototype/review.html');fixture=data(populated)
    if page=='m07-p01':fixture['dujia-prototype-pet']['status']='pending'
    p.evaluate("data=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(data))localStorage.setItem(k,JSON.stringify(v));}",fixture)
    p.goto(BASE+'pages/'+page+'.html');p.wait_for_timeout(750);p.evaluate('document.fonts.ready');assert p.url.split('?')[0].endswith(page+'.html'),p.url
    expect(p.get_by_role('navigation',name='主导航',exact=True)).to_be_visible()
    p.evaluate('document.documentElement.style.setProperty("--ui-safe-top","44px");document.documentElement.style.setProperty("--ui-safe-bottom","34px")')
    metrics=p.evaluate('''()=>{const nav=document.querySelector('.prototype-primary-nav');const check=e=>{const r=e.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return {label:e.textContent.trim(),width:r.width,height:r.height,hit:hit===e||e.contains(hit)}};const controls=[...document.querySelectorAll('.screen button,.screen a')].filter(e=>!e.disabled&&e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden').map(e=>{e.scrollIntoView({block:'center'});return check(e)});return {width:document.documentElement.scrollWidth,navBottom:nav.getBoundingClientRect().bottom,padding:getComputedStyle(nav).paddingBottom,tabs:[...nav.querySelectorAll('button')].map(check),controls}}''')
    assert metrics['width']==width,metrics
    assert all(t['width']>=44 and t['height']>=44 and t['hit'] for t in metrics['tabs']),metrics
    assert float(metrics['padding'].replace('px',''))>=34,metrics
    assert all(t['hit'] for t in metrics['controls']),metrics
    assert not errors,errors
    if width==320:p.screenshot(path=str(OUT/f'primary-navigation-{page}-{width}.png'),full_page=True)
    row=dict(page=page,width=width,passed=True,metrics=metrics)
   except Exception:row=dict(page=page,width=width,passed=False,failure=traceback.format_exc()[-2800:],errors=errors)
   rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+page+' '+str(width),flush=True);c.close()
 b.close()
(OUT/'primary-navigation-layout-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
