from pathlib import Path
import json,traceback
from playwright.sync_api import sync_playwright,expect
from book_test_helpers import seed,go,fixture,records
IMAGE='data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="80" height="100"><rect width="80" height="100" fill="%239abc87"/></svg>'

OUT=Path(__file__).resolve().parent/'evidence/current';rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for width in [320,375,390,414,430]:
  c=b.new_context(viewport={'width':width,'height':844},reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000)
  book=fixture();book.update(name='一本拥有二十字以内长书名的共同回忆册',theme='旅行手札',coverPhoto=dict(kind='photo',id='cover-photo'));photo=dict(id='cover-photo',type='photo',title='共同封面',image=IMAGE,date='2026-10-04',visibility='shared',status='published');seed(p,books=[book],records=records()+[photo])
  for number in [1,5,15,16,21]:
   errors=[];handler=lambda e:errors.append(str(e));p.on('pageerror',handler)
   try:
    go(p,number,'?id=book-state'+('&page=page-state' if number==16 else ''));p.wait_for_function('document.querySelector(".screen").getAttribute("aria-busy")==="false"');p.evaluate('document.fonts.ready');p.evaluate('document.documentElement.style.setProperty("--ui-safe-top","44px");document.documentElement.style.setProperty("--ui-safe-bottom","34px")')
    if number!=16:expect(p.locator('.book-cover-photo img')).to_have_attribute('src',IMAGE);p.wait_for_function('[...document.querySelectorAll(".book-cover-photo img")].every(i=>i.complete&&i.naturalWidth>0)')
    if number in [5,15,21]:
     box=p.locator('.book-cover-photo').bounding_box();screen=p.locator('.screen').bounding_box();assert box['x']>screen['x'] and box['y']>=screen['y']+screen['height']*.09 and box['width']<screen['width']*.8,(box,screen)
    metrics=p.evaluate('''()=>({width:document.documentElement.scrollWidth,buttons:[...document.querySelectorAll('.screen button')].filter(e=>!e.disabled&&e.getClientRects().length).map(e=>{e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect(),h=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return {text:e.textContent,hit:h===e||e.contains(h)}})})''')
    assert metrics['width']==width and all(v['hit'] for v in metrics['buttons']),metrics;assert not errors,errors
    p.screenshot(path=str(OUT/f'book-cover-p{number:02}-{width}.png'),full_page=True);row=dict(page=f'm08-p{number:02}',width=width,passed=True,metrics=metrics)
   except Exception:row=dict(page=f'm08-p{number:02}',width=width,passed=False,failure=traceback.format_exc()[-2000:],errors=errors)
   rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+f'p{number} {width}',flush=True);p.remove_listener('pageerror',handler)
  c.close()
 b.close()
OUT.mkdir(parents=True,exist_ok=True);(OUT/'book-cover-layout-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(v['passed'] for v in rows) else 1)
