"""Account script delivery failure must never fall back to credential GET submission."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

out=Path(__file__).resolve().parent/'evidence/current'
out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 context=browser.new_context(viewport={'width':390,'height':844});failure={'remaining':1}
 def deliver(route):
  if failure['remaining']:
   failure['remaining']-=1;route.abort()
  else:route.continue_()
 context.route('**/assets/prototype-account.js',deliver)
 page=context.new_page();page.goto('http://127.0.0.1:8765/pages/m01-p02.html')
 page.locator('input[name=phone]').fill('13812345678');page.locator('#password').fill('demo1234')
 page.get_by_role('button',name='登录并回到故事里',exact=True).click();page.wait_for_timeout(500)
 assert '?' not in page.url,'Native form submission exposed form values in the URL when controller script failed'
 assert page.locator('.prototype-reload').is_visible(),'Missing recovery action for the script failure'
 page.screenshot(path=str(out/'account-script-failure.png'),full_page=True)
 page.locator('.prototype-reload').click();page.wait_for_load_state('load')
 page.wait_for_function("document.querySelector('#form').dataset.prototypeReady==='true'")
 page.locator('#password').fill('demo1234');page.get_by_role('button',name='登录并回到故事里',exact=True).click()
 page.wait_for_url('**/m02-p01.html')
 browser.close()
(out/'account-script-failure-results.json').write_text(json.dumps({'script_failure_does_not_submit_values':True,'visible_reload_recovers':True,'recovered_login_passes':True},indent=2),encoding='utf-8')
print('PASS script failure: no credential GET, visible reload, recovered login')
