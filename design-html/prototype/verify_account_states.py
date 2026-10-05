"""Validate inline errors, loading, retry safety and modal geometry at mobile widths."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

OUT=Path(__file__).resolve().parent/'evidence'/'current'
OUT.mkdir(parents=True,exist_ok=True)
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for width in [320,375,390,414,430]:
  context=browser.new_context(viewport={'width':width,'height':932});page=context.new_page();errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8765/pages/m01-p02.html');page.evaluate('document.fonts.ready')
  phone=page.locator('input[name=phone]');password=page.locator('#password');button=page.locator('button[form=form]')
  phone.fill('12');password.focus()
  assert phone.get_attribute('aria-invalid')=='true'
  metrics=page.evaluate("""()=>{const error=document.querySelector('.prototype-field-error');const r=error.getBoundingClientRect();const overlap=e=>{const b=e.getBoundingClientRect();return Math.min(r.right,b.right)-Math.max(r.left,b.left)>1&&Math.min(r.bottom,b.bottom)-Math.max(r.top,b.top)>1};return {error:error.textContent,overlapping:[...document.querySelectorAll('button,input')].filter(overlap).map(e=>e.id||e.className||e.name),width:document.documentElement.scrollWidth}}""")
  page.screenshot(path=str(OUT/f'account-validation-{width}.png'),full_page=True)
  assert not metrics['overlapping'],(width,metrics)
  assert metrics['width']==width
  phone.fill('13812345678');password.fill('demo1234');assert phone.get_attribute('aria-invalid')=='false'
  page.evaluate("sessionStorage.setItem('dujia-prototype-fail-next','login')")
  button.click();assert button.is_disabled() and button.get_attribute('aria-busy')=='true'
  page.screenshot(path=str(OUT/f'account-loading-{width}.png'),full_page=True)
  page.wait_for_timeout(750)
  assert page.url.endswith('m01-p02.html') and not button.is_disabled()
  assert password.input_value()=='demo1234' and phone.input_value()=='13812345678'
  assert page.evaluate("localStorage.getItem('dujia-prototype-session')") is None
  assert '重试' in page.locator('.prototype-toast').inner_text()
  page.get_by_role('link',name='《隐私政策》',exact=True).click();dialog=page.locator('dialog[open]')
  assert dialog.count()==1
  rect=dialog.bounding_box();assert rect['x']>=0 and rect['x']+rect['width']<=width
  page.screenshot(path=str(OUT/f'account-modal-{width}.png'),full_page=True)
  page.keyboard.press('Tab');assert dialog.evaluate('e=>e.contains(document.activeElement)')
  page.keyboard.press('Escape');page.locator('dialog[open]').wait_for(state='hidden');assert page.locator('dialog[open]').count()==0
  button.click();page.wait_for_url('**/m02-p01.html')
  session=page.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-session'))")
  assert session['loggedIn'] and 'password' not in session
  assert not errors,errors
  results.append({'width':width,'validation':True,'loading':True,'failed_login_preserves_input':True,'no_false_save':True,'retry_navigation':True,'no_password_storage':True,'modal_bounds_focus_close':True})
  print(f'PASS account states at {width}px',flush=True);context.close()
 browser.close()
(OUT/'account-state-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
