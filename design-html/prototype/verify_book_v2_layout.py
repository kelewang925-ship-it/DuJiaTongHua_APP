"""All 21 V2 routes at five widths, plus landscape; inspect actual controls and paper."""
from pathlib import Path
import json,traceback
from playwright.sync_api import sync_playwright
from book_test_helpers import seed,go,fixture,records

OUT=Path(__file__).resolve().parent/'evidence/current/book-v2';OUT.mkdir(parents=True,exist_ok=True)
rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for width in [320,375,390,414,430,844]:
  c=b.new_context(viewport={'width':width,'height':390 if width==844 else 844},reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000)
  for n in ([16] if width==844 else range(1,22)):
   errors=[];handler=lambda e:errors.append(str(e));p.on('pageerror',handler)
   try:
    sample=fixture();sample['selected'].append({'kind':'diary','id':'pending-source'})
    source_records=records()+[dict(id='pending-source',type='diary',title='等待编排的日记',body='把这段共同回忆放进书里。',date='2026-10-04',visibility='shared',status='published',author='小满')]
    seed(p,books=[sample],records=source_records)
    go(p,n,'?id=book-state'+('&page=page-state' if n in [9,16,17,18,19,20] else ''))
    p.wait_for_function('document.querySelector(".screen").getAttribute("aria-busy")==="false"');p.evaluate('document.fonts.ready')
    if n==20:p.wait_for_timeout(180);p.keyboard.press('Escape');p.wait_for_timeout(80)
    metrics=p.evaluate('''()=>{const root=document.querySelector('.screen');const visible=e=>e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden'&&!e.closest('[inert]');return {width:document.documentElement.scrollWidth,buttons:[...root.querySelectorAll('button,input,textarea,select')].filter(e=>!e.disabled&&visible(e)).map(e=>{e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return {text:e.textContent||e.getAttribute('aria-label'),hit:hit===e||e.contains(hit),width:r.width,height:r.height};}),paper:[...root.querySelectorAll('.v2-reader-sheets .v2-paper-content')].map(e=>({height:e.clientHeight,scroll:e.scrollHeight}))};}''')
    assert metrics['width']==width,metrics
    assert all(x['hit'] for x in metrics['buttons']),[x for x in metrics['buttons'] if not x['hit']]
    assert not errors,errors
    if n==16:
     assert all(x['scroll']<=x['height']+2 for x in metrics['paper']),metrics['paper']
    if width==390 and n in [1,4,5,6,9,13,15,16,19,21] or width==844:
     p.evaluate('window.scrollTo(0,0)');p.screenshot(path=str(OUT/f'page-{n:02}-{width}.png'),full_page=True)
    row={'page':n,'width':width,'passed':True,'metrics':metrics}
   except Exception:row={'page':n,'width':width,'passed':False,'failure':traceback.format_exc()[-1800:],'errors':errors}
   rows.append(row);p.remove_listener('pageerror',handler)
  c.close();print(f'{width}px: '+str(sum(r['passed'] for r in rows if r['width']==width))+'/'+str(sum(r['width']==width for r in rows)),flush=True)
 b.close()
(OUT/'layout-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
