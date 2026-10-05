from pathlib import Path
import json,traceback
from playwright.sync_api import sync_playwright,expect
from book_test_helpers import seed,go,fixture

OUT=Path(__file__).resolve().parent/'evidence/current';rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for width in [320,375,390,414,430]:
  c=b.new_context(viewport={'width':width,'height':844},reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000);seed(p,books=[fixture()])
  p.evaluate('''()=>{const canvas=document.createElement('canvas');canvas.width=120;canvas.height=80;const ctx=canvas.getContext('2d');ctx.fillStyle='#bc7190';ctx.fillRect(0,0,120,80);const image=canvas.toDataURL();localStorage.setItem('dujia-prototype-records',JSON.stringify([{id:'photo-variant',type:'photo',title:'共同照片的长标题',body:'共同照片正文',image,date:'2026-10-04',visibility:'shared',status:'published'}]));const books=JSON.parse(localStorage.getItem('dujia-prototype-books'));books[0].pages[0]={id:'page-state',chapterId:'chapter-state',template:'照片故事',source:{kind:'photo',id:'photo-variant'},body:'长长的独立说明'.repeat(60),photos:[1,2,3].map(v=>({source:{kind:'photo',id:'photo-variant'},crop:{x:40,y:60,zoom:1.5}})),stickers:['🌸','⭐'],supplements:[{id:'supplement-long',author:'小满',date:'2026-10-05',text:'这是一段长长的真实补页'.repeat(40),image},{id:'supplement-emoji',author:'阿舟',date:'2026-10-05',emoji:'⭐'}]};localStorage.setItem('dujia-prototype-books',JSON.stringify(books));}''')
  for n in [16,20]:
   errors=[];handler=lambda e:errors.append(str(e));p.on('pageerror',handler)
   try:
    go(p,n,'?id=book-state&page=page-state');expect(p.locator('.book-reading-images img')).to_have_count(3);p.evaluate('document.fonts.ready');p.evaluate('document.documentElement.style.setProperty("--ui-safe-top","44px");document.documentElement.style.setProperty("--ui-safe-bottom","34px")');p.locator('.book-reading-area').focus();p.keyboard.press('PageDown');p.wait_for_function('document.querySelector(".book-reading-area").scrollTop>0');assert p.evaluate('[...document.querySelectorAll(".book-reading-images img")].every(v=>v.complete&&v.naturalWidth>0)');assert p.evaluate('document.documentElement.scrollWidth')==width
    if n==20:expect(p.locator('.book-supplement-images img')).to_have_count(1)
    assert not errors,errors;p.screenshot(path=str(OUT/f'book-image-p{n}-{width}.png'),full_page=True);row={'page':f'm08-p{n}','width':width,'passed':True}
   except Exception:row={'page':f'm08-p{n}','width':width,'passed':False,'failure':traceback.format_exc()[-1800:],'errors':errors}
   rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+f'image p{n} {width}',flush=True);p.remove_listener('pageerror',handler)
  c.close()
 b.close()
OUT.mkdir(parents=True,exist_ok=True);(OUT/'book-image-variant-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(v['passed'] for v in rows) else 1)
