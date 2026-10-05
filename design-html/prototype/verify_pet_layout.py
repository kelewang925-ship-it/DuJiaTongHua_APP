from pathlib import Path
import json
from playwright.sync_api import sync_playwright
OUT=Path(__file__).resolve().parent/'evidence/current';OUT.mkdir(parents=True,exist_ok=True)
rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for width in [320,360,390,414,431]:
  c=b.new_context(viewport={'width':width,'height':844},reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4000);p.goto('http://127.0.0.1:8765/prototype/review.html')
  p.evaluate('localStorage.setItem("dujia-prototype-relationship",JSON.stringify({bound:true,partner:"阿舟"}));localStorage.setItem("dujia-profile",JSON.stringify({nickname:"小满"}));sessionStorage.setItem("dujia-prototype-today","2026-10-05")')
  for n in range(1,12):
   logs=[dict(id='play-example',type='play',text='丢球球',actor='小满',date='2026-10-05',delta=dict(energy=-12,mood=8,affinity=3)),dict(id='reward-example',type='reward',text='主粮 ×1、礼物 ×1',actor='小满',date='2026-10-05')]
   pet=dict(id='pet-layout',name='团团',kind='小狗',status='pending' if n==1 else 'active',requestedBy='小满',adoptedDate='2026-10-05',energy=4 if n==7 else 82,satiety=76,mood=70,affinity=3,food=[12,5,0],gifts=1,coins=0,stars=0,owned=[],outfit=None,room={},claims=[],logs=logs,care=True,lastInteraction='play-example',lastReward='reward-example',settings={})
   p.evaluate('(pet)=>localStorage.setItem("dujia-prototype-pet",JSON.stringify(pet))',None if n in [2,4] else pet)
   errors=[];handler=lambda e:errors.append(str(e));p.on('pageerror',handler)
   try:
    p.goto(f'http://127.0.0.1:8765/pages/m07-p{n:02}.html'+('?food=2' if n==9 else '?cost=5' if n==7 else ''));p.locator('.pet-load').wait_for(state='detached');p.evaluate('document.fonts.ready');p.evaluate('document.documentElement.style.setProperty("--ui-safe-top","44px");document.documentElement.style.setProperty("--ui-safe-bottom","34px")')
    metrics=p.evaluate('()=>{const s=document.querySelector(".screen").getBoundingClientRect();return {width:document.documentElement.scrollWidth,safeTop:s.y,safeBottom:document.documentElement.scrollHeight-s.bottom,buttons:[...document.querySelectorAll("button")].filter(e=>!e.disabled&&e.getClientRects().length).map(e=>{e.scrollIntoView({block:"center"});let r=e.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return {text:e.textContent,hit:hit===e||e.contains(hit),width:r.width,height:r.height};})};}')
    assert metrics['width']==width and metrics['safeTop']>=44 and metrics['safeBottom']>=33,metrics
    assert all(v['hit'] for v in metrics['buttons']),metrics['buttons'];assert not errors,errors
    overlaps=p.evaluate('()=>{const t=document.querySelector("h1").getBoundingClientRect();return [...document.querySelectorAll(".pet-back,.pet-top-action,.back")].filter(e=>e.getClientRects().length).map(e=>{const b=e.getBoundingClientRect();return {text:e.textContent,overlap:b.left<t.right&&b.right>t.left&&b.top<t.bottom&&b.bottom>t.top};});}');assert not any(v['overlap'] for v in overlaps),overlaps
    p.screenshot(path=str(OUT/f'pet-m07-p{n:02}-{width}.png'),full_page=True);row={'page':f'm07-p{n:02}','width':width,'passed':True,'metrics':metrics}
   except Exception as e:row={'page':f'm07-p{n:02}','width':width,'passed':False,'failure':repr(e)[:1600],'errors':errors}
   rows.append(row);(OUT/'pet-layout-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');print(('PASS ' if row['passed'] else 'FAIL ')+f'm07-p{n:02} {width}',flush=True);p.remove_listener('pageerror',handler)
  c.close()
 b.close()
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
