from pathlib import Path
import json,traceback
from playwright.sync_api import sync_playwright,expect
from pet_test_helpers import seed,go,value
OUT=Path(__file__).resolve().parent/'evidence/current';OUT.mkdir(parents=True,exist_ok=True);rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for width in [320,375,390,414,430]:
  c=b.new_context(viewport={'width':width,'height':844},reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:
   seed(p,logs=[dict(id='source-one',type='source',sourceId='diary-source',sourceKind='record',actor='小满',date='2026-10-05',text='关联了共同记录')]);p.evaluate('localStorage.setItem("dujia-prototype-records",JSON.stringify([{id:"diary-source",type:"diary",title:"共同散步日记",body:"今日的温柔".repeat(100),visibility:"shared",status:"published",author:"阿舟"}]))');go(p,19,'?id=source-one');expect(p.get_by_role('button',name='查看关联记录',exact=True)).to_be_visible();link=p.get_by_role('button',name='查看关联记录',exact=True);link.scroll_into_view_if_needed();assert link.evaluate('e=>{const r=e.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return hit===e||e.contains(hit)}');assert p.evaluate('document.documentElement.scrollWidth')==width;assert p.locator('.note').evaluate('e=>e.scrollHeight>e.clientHeight');p.screenshot(path=str(OUT/f'pet-life-source-{width}.png'),full_page=True);link.click();p.wait_for_url('**/m03-p08.html?id=diary-source');expect(p.locator('.title')).to_have_text('共同散步日记');assert not errors,errors;row={'case':'source-detail-inline-link','width':width,'passed':True}
  except Exception:row={'case':'source-detail-inline-link','width':width,'passed':False,'failure':traceback.format_exc()[-1800:],'errors':errors}
  rows.append(row);(OUT/'pet-life-variant-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');print(('PASS ' if row['passed'] else 'FAIL ')+str(width),flush=True);c.close()
 b.close()
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
