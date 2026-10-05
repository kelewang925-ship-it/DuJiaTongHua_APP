from pathlib import Path
import json,traceback
from playwright.sync_api import sync_playwright
from pet_test_helpers import seed,value,go
OUT=Path(__file__).resolve().parent/'evidence/current';OUT.mkdir(parents=True,exist_ok=True);rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for width in [320,375,390,414,430]:
  c=b.new_context(viewport={'width':width,'height':844},reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4000)
  seed(p,stars=0,ownedRoom=['奶油小床','格纹地毯'],room={'地毯':'花朵地毯','小床':'奶油小床','墙饰':'花朵墙饰','摆件':'花朵花瓶'},lastRoom='room-one',logs=[dict(id='first',type='adopt',text='共同领养了团团',actor='阿舟',date='2026-09-01'),dict(id='room-one',type='room',text='更换了奶油小床',actor='小满',date='2026-10-04',after={'地毯':'花朵地毯','小床':'奶油小床','墙饰':'花朵墙饰','摆件':'花朵花瓶'}),dict(id='manual-one',type='note',text='成长故事'*100,actor='小满',date='2026-10-04',comments=[dict(id='reply-one',author='阿舟',text='温柔回应'*60)]),dict(id='blocked',type='source',text='关联了共同记录',actor='小满',date='2026-10-03',sourceId='gone-record')])
  for n in range(12,26):
   errors=[];handler=lambda e:errors.append(str(e));p.on('pageerror',handler)
   try:
    query={14:'?id=room-one',17:'?id=blocked',19:'?id=manual-one'}.get(n,'');go(p,n,query);p.locator('.pet-load').wait_for(state='detached');p.evaluate('document.fonts.ready');p.evaluate('document.documentElement.style.setProperty("--ui-safe-top","44px");document.documentElement.style.setProperty("--ui-safe-bottom","34px")')
    metrics=p.evaluate('()=>{const s=document.querySelector(".screen").getBoundingClientRect();return {width:document.documentElement.scrollWidth,top:s.y,bottom:document.documentElement.scrollHeight-s.bottom,buttons:[...document.querySelectorAll("button")].filter(e=>!e.disabled&&e.getClientRects().length).map(e=>{e.scrollIntoView({block:"center"});const r=e.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return {text:e.textContent,hit:hit===e||e.contains(hit),width:r.width,height:r.height};})};}')
    assert metrics['width']==width and metrics['top']>=44 and metrics['bottom']>=33,metrics
    assert all(v['hit'] for v in metrics['buttons']),metrics['buttons'];assert not errors,errors
    overlaps=p.evaluate('()=>{const t=document.querySelector("h1").getBoundingClientRect();return [...document.querySelectorAll(".pet-back,.pet-life-extra,.back")].filter(e=>e.getClientRects().length).map(e=>{const r=e.getBoundingClientRect();return {text:e.textContent,overlap:r.left<t.right&&r.right>t.left&&r.top<t.bottom&&r.bottom>t.top};});}');assert not any(v['overlap'] for v in overlaps),overlaps
    p.screenshot(path=str(OUT/f'pet-life-m07-p{n:02}-{width}.png'),full_page=True);row={'page':f'm07-p{n:02}','width':width,'passed':True,'metrics':metrics}
   except Exception:row={'page':f'm07-p{n:02}','width':width,'passed':False,'failure':traceback.format_exc()[-1800:],'errors':errors,'url':p.url}
   rows.append(row);(OUT/'pet-life-layout-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');print(('PASS ' if row['passed'] else 'FAIL ')+f'm07-p{n:02} {width}',flush=True);p.remove_listener('pageerror',handler)
  c.close()
 b.close()
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
