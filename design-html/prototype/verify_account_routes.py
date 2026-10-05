"""Behavior gates for the first broken account flow; baseline failures are expected."""
from pathlib import Path
import argparse
import json
from playwright.sync_api import sync_playwright

OUT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--baseline',action='store_true',help='Record the initial known failures separately')
args=parser.parse_args()
evidence=OUT/'evidence'/('baseline' if args.baseline else 'current')
evidence.mkdir(parents=True,exist_ok=True)
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for case in ['login','register-entry','recovery-entry','verification-direct-back','legal-modal']:
  context=browser.new_context(viewport={'width':390,'height':844})
  context.add_init_script("document.addEventListener('submit', e=>console.debug('prototype-submit',e.target.id,e.defaultPrevented))")
  page=context.new_page();errors=[];resources=[];console=[];failed=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('requestfailed',lambda r:failed.append({'url':r.url,'failure':r.failure}))
  page.on('response',lambda r:resources.append({'url':r.url,'status':r.status}) if r.url.endswith('.js') else None)
  page.on('console',lambda m:console.append(m.text) if m.text.startswith('prototype-submit') else None)
  source='m01-p07' if case=='verification-direct-back' else 'm01-p02'
  page.goto('http://127.0.0.1:8765/pages/'+source+'.html');page.evaluate('document.fonts.ready')
  readiness=page.evaluate("({shared:!!window.PrototypeUI,passwordNamed:document.querySelector('#password')?.getAttribute('aria-label')})")
  expected=[]
  if case=='login':
   page.locator('input[name=phone]').fill('13812345678');page.locator('#password').fill('demo1234')
   page.get_by_role('button',name='登录并回到故事里',exact=True).click()
   expected=['m02-p01.html','m03-p01.html']
  elif case=='register-entry':
   page.get_by_role('button',name='创建账号',exact=True).click();expected=['m01-p03.html']
  elif case=='recovery-entry':
   page.get_by_role('button',name='忘记密码？',exact=True).click();expected=['m01-p04.html']
  elif case=='verification-direct-back':
   page.get_by_role('button',name='返回',exact=True).click();expected=['m01-p04.html','m01-p03.html','m01-p02.html']
  else:
   page.get_by_role('link',name='《用户协议》',exact=True).click()
  page.wait_for_timeout(1200)
  passed=any(page.url.split('?')[0].endswith(route) for route in expected) and not errors
  if case=='legal-modal':
   passed=page.locator('dialog[open]').count()==1
   if passed:
    page.keyboard.press('Escape');page.locator('dialog[open]').wait_for(state='hidden');passed=page.locator('dialog[open]').count()==0 and page.get_by_role('link',name='《用户协议》',exact=True).evaluate('e=>e===document.activeElement')
  page.screenshot(path=str(evidence/f'account-{case}.png'),full_page=True)
  results.append({'case':case,'source':source,'expected_routes':expected,'actual_url':page.url,'passed':passed,'errors':errors,'readiness':readiness,'script_responses':resources,'request_failures':failed,'submit_events':console,'phase':'baseline-known-defect' if args.baseline else 'implementation-verification'})
  context.close()
 browser.close()
(evidence/'account-route-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
for row in results:print(('PASS' if row['passed'] else 'FAIL')+' '+row['case']+' '+row['actual_url'])
raise SystemExit(0 if all(row['passed'] for row in results) else 1)
