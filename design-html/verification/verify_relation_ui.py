from pathlib import Path
import json
from playwright.sync_api import sync_playwright
r=Path('design-html').resolve(); results=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 page=b.new_page(viewport={'width':320,'height':740})
 def go(id):page.goto((r/'pages'/f'{id}.html').as_uri());page.evaluate('document.fonts.ready')
 go('m02-p03')
 page.locator('.code input').first.fill('a');assert page.locator('.code input').first.input_value()=='A'
 assert page.locator('.code input').nth(1).evaluate('(e)=>e===document.activeElement')
 page.locator('.code input').first.evaluate("e=>e.dispatchEvent(new ClipboardEvent('paste',{clipboardData:new DataTransfer()}))")
 page.evaluate("()=>{const d=new DataTransfer();d.setData('text','xh7k');document.querySelector('.code input').dispatchEvent(new ClipboardEvent('paste',{clipboardData:d}))}")
 assert page.locator('.code input').evaluate_all('(els)=>els.map(e=>e.value).join(\"\")')=='XH7K'
 page.locator('.preview').click();page.wait_for_url('**/m02-p04.html');page.locator('.confirm').click();page.wait_for_url('**/m02-p05.html');page.locator('.secondary').click();page.wait_for_url('**/m02-p06.html')
 results.append('320px invitation uppercase/paste/auto-focus and preview-confirm-profile route passed')
 value='很长的情侣昵称'*30;page.locator('#nickname').fill(value);page.locator('.save').click();assert page.locator('#toast').is_visible();page.reload();assert page.locator('#nickname').input_value()==value
 assert page.evaluate('document.documentElement.scrollWidth')==320
 page.evaluate('localStorage.clear()');results.append('320px long profile input saved and restored without horizontal growth')
 go('m02-p07');page.locator('#remind').click();assert page.locator('#toast').is_visible();results.append('Waiting reminder retains demo feedback')
 go('m02-p02');page.locator('#copy').click();page.locator('#toast').wait_for(state='visible',timeout=5000)
 with page.expect_download() as download:page.locator('#save').click()
 assert download.value.suggested_filename.endswith('.svg');results.append('Invitation copy fallback and editable SVG card download passed')
 for i in range(1,10):
  id=f'm02-p{i:02}';go(id)
  page.locator('.screen').screenshot(path=str(r/'ui-audit/evidence/after'/f'{id}-320.png'))
  page.evaluate("document.documentElement.style.setProperty('--ui-safe-top','44px');document.documentElement.style.setProperty('--ui-safe-bottom','34px')")
  m=page.evaluate("()=>{const r=document.querySelector('.screen').getBoundingClientRect();return {y:r.y,h:r.height,doc:document.documentElement.scrollHeight,w:document.documentElement.scrollWidth}}")
  assert m['y']>=44 and m['doc']>=m['h']+77 and m['w']==320,(id,m)
 results.append('All 9 screens at 320px with simulated 44/34px safe area passed')
 b.close()
(r/'ui-audit/relation-interaction-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print('\n'.join(results))
