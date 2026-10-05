from pathlib import Path
import json,traceback,sys
from playwright.sync_api import sync_playwright
from book_test_helpers import seed,go,fixture,records

OUT=Path(__file__).resolve().parent/'evidence/current';OUT.mkdir(parents=True,exist_ok=True);rows=[]
PAGES=[*range(1,10),13,14,15,16,21]
if '--home-only' in sys.argv:
 PAGES=[1];rows=[v for v in json.loads((OUT/'book-layout-results.json').read_text(encoding='utf-8')) if v['page']!='m08-p01']
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for width in [320,375,390,414,430]:
  c=b.new_context(viewport={'width':width,'height':844},reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000)
  seed(p,books=[fixture()],records=records())
  for n in PAGES:
   errors=[];handler=lambda e:errors.append(str(e));p.on('pageerror',handler)
   try:
    query='?id=book-state'+('&page=page-state' if n in [9,16] else '')
    go(p,n,query);p.wait_for_function('document.querySelector(".screen").getAttribute("aria-busy")==="false"');p.evaluate('document.fonts.ready');p.evaluate('document.documentElement.style.setProperty("--ui-safe-top","44px");document.documentElement.style.setProperty("--ui-safe-bottom","34px")')
    metrics=p.evaluate('''()=>{const s=document.querySelector('.screen').getBoundingClientRect();return {width:document.documentElement.scrollWidth,top:s.y,bottom:document.documentElement.scrollHeight-s.bottom,buttons:[...document.querySelectorAll('button')].filter(e=>!e.disabled&&e.getClientRects().length).map(e=>{e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return {text:e.textContent,hit:hit===e||e.contains(hit),width:r.width,height:r.height};})};}''')
    assert metrics['width']==width and metrics['top']>=44 and metrics['bottom']>=33,metrics
    assert all(v['hit'] for v in metrics['buttons']),metrics['buttons'];assert not errors,errors
    p.screenshot(path=str(OUT/f'book-first-m08-p{n:02}-{width}.png'),full_page=True);row={'page':f'm08-p{n:02}','width':width,'passed':True,'metrics':metrics}
   except Exception:row={'page':f'm08-p{n:02}','width':width,'passed':False,'failure':traceback.format_exc()[-2000:],'errors':errors,'url':p.url}
   rows.append(row);(OUT/'book-layout-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(('PASS ' if row['passed'] else 'FAIL ')+f'm08-p{n:02} {width}',flush=True);p.remove_listener('pageerror',handler)
  c.close()
 b.close()
raise SystemExit(0 if all(v['passed'] for v in rows) else 1)
