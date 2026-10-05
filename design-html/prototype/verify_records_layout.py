"""Check real control hit positions on home/search/diary at five mobile widths."""
from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright
OUT=Path(__file__).resolve().parent/'evidence/current';rows=[]
parser=argparse.ArgumentParser();parser.add_argument('--photos',action='store_true');args=parser.parse_args()
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for width in [320,375,390,414,430]:
  for number in (range(9,13) if args.photos else range(1,9)):
   id=f'm03-p{number:02}';c=b.new_context(viewport={'width':width,'height':932},reduced_motion='reduce');p=c.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
   p.goto(f'http://127.0.0.1:8765/pages/{id}.html');p.evaluate('document.fonts.ready');p.wait_for_timeout(500)
   p.evaluate('document.documentElement.style.setProperty("--ui-safe-top","44px");document.documentElement.style.setProperty("--ui-safe-bottom","34px")')
   blocked=[];controls=p.locator('button,a,input:not([type=file]),textarea,select')
   for i in range(controls.count()):
    e=controls.nth(i)
    if not e.is_visible():continue
    e.scroll_into_view_if_needed()
    metric=e.evaluate('(e)=>{const r=e.getBoundingClientRect();const hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return {name:e.getAttribute("aria-label")||e.textContent||e.name,width:r.width,height:r.height,reachable:hit===e||e.contains(hit)}}')
    if not metric['reachable']:blocked.append(metric)
   overflow=p.evaluate('document.documentElement.scrollWidth')>width
   p.screenshot(path=str(OUT/f'records-layout-{id}-{width}.png'),full_page=True)
   rows.append({'page':id,'width':width,'safe_top':44,'safe_bottom':34,'reduced_motion':True,'passed':not errors and not blocked and not overflow,'blocked':blocked,'overflow':overflow,'errors':errors});c.close()
  print(f'Checked records layout {width}px',flush=True)
 b.close()
(OUT/('photo-layout-results.json' if args.photos else 'records-layout-results.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
failed=[r for r in rows if not r['passed']];print(json.dumps(failed,ensure_ascii=False),flush=True)
raise SystemExit(1 if failed else 0)
