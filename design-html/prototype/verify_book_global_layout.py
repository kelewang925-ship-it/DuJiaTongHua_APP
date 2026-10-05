from pathlib import Path
import json,traceback
from playwright.sync_api import sync_playwright,expect
from book_test_helpers import seed,fixture,records,BASE
OUT=Path(__file__).resolve().parent/'evidence/current';rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for width in [320,375,390,414,430]:
  c=b.new_context(viewport={'width':width,'height':844},reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000);book=fixture();book['name']='这是一本拥有较长名字的共同回忆册';draft=fixture('book-draft');draft.update(status='draft',name='还没有完成等待继续编辑的回忆册');seed(p,books=[book,draft],records=records())
  for page in ['m03-p02','m06-p04','m06-p11']:
   errors=[];handler=lambda e:errors.append(str(e));p.on('pageerror',handler)
   try:
    p.goto(BASE+'pages/'+page+'.html');p.evaluate('document.fonts.ready')
    if page=='m06-p04':expect(p.locator('.prototype-settings-drafts')).to_contain_text(draft['name'])
    if page=='m03-p02':
     expect(p.locator('.reading')).to_contain_text(book['name']);title=p.locator('.reading strong').bounding_box();card=p.locator('.reading').bounding_box();assert title['x']+title['width']<=card['x']+card['width'],(title,card)
    p.evaluate('document.documentElement.style.setProperty("--ui-safe-top","44px");document.documentElement.style.setProperty("--ui-safe-bottom","34px")')
    metrics=p.evaluate('''()=>({width:document.documentElement.scrollWidth,controls:[...document.querySelectorAll('button,a')].filter(e=>!e.disabled&&e.getClientRects().length).map(e=>{e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return {text:e.textContent,hit:hit===e||e.contains(hit)}})})''');assert metrics['width']==width and all(v['hit'] for v in metrics['controls']),metrics;assert not errors,errors
    p.screenshot(path=str(OUT/f'book-global-{page}-{width}.png'),full_page=True);row=dict(page=page,width=width,passed=True,metrics=metrics)
   except Exception:row=dict(page=page,width=width,passed=False,failure=traceback.format_exc()[-2000:],errors=errors)
   rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+page+' '+str(width),flush=True);p.remove_listener('pageerror',handler)
  c.close()
 b.close()
OUT.mkdir(parents=True,exist_ok=True);(OUT/'book-global-layout-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(v['passed'] for v in rows) else 1)
