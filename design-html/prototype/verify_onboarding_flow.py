"""Real cross-page onboarding flows, including failure states and browser back."""
from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright,expect

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');args=parser.parse_args()
OUT=ROOT/'evidence'/('baseline' if args.baseline else 'current');OUT.mkdir(parents=True,exist_ok=True)
results=[]
def go(page,id):page.goto('http://127.0.0.1:8765/pages/'+id+'.html');page.evaluate('document.fonts.ready')
def code(page,value='284631'):
 for i,c in enumerate(value):page.locator('.code input').nth(i).fill(c)
def invite(page,value='XH7K9M2Q'):
 assert page.locator('.code input').first.get_attribute('maxlength')=='2','Eight-character invite must fit all four groups'
 for i in range(4):page.locator('.code input').nth(i).fill(value[i*2:i*2+2])
def register(page):
 go(page,'m01-p03');page.locator('input[name=nickname]').fill('星星');page.locator('input[name=phone]').fill('13812345678');page.locator('#password').fill('Demo1234')
 page.locator('button.submit').click();page.wait_for_url('**/m01-p07.html',timeout=3500)
 code(page);page.locator('button.verify').click();page.wait_for_url('**/m02-p01.html',timeout=3500)
 saved=page.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-session'))")
 assert saved['loggedIn'] and saved['phone']=='13812345678'
 assert 'Demo1234' not in page.evaluate("JSON.stringify({...localStorage,...sessionStorage})")
def recovery(page):
 go(page,'m01-p04');page.locator('input[name=phone]').fill('13812345678');page.locator('button.next').click();page.wait_for_url('**/m01-p07.html',timeout=3500)
 code(page,'111111');page.locator('button.verify').click();expect(page.locator('.prototype-code-error')).to_be_visible();expect(page.locator('.prototype-code-error')).to_contain_text('验证码',timeout=2000)
 assert page.url.endswith('m01-p07.html')
 code(page);page.locator('button.verify').click();page.wait_for_url('**/m01-p05.html',timeout=3500)
 page.locator('#password').fill('Newdemo123');page.locator('#confirm').fill('Wrong1234');page.locator('button.submit').click()
 expect(page.locator('#confirm')).to_have_attribute('aria-invalid','true');expect(page.locator('.prototype-component-error[role=alert]:visible')).to_contain_text('一致',timeout=2000)
 page.locator('#confirm').fill('Newdemo123');page.locator('button.submit').click();page.wait_for_url('**/m01-p08.html',timeout=3500)
 page.locator('button.login').click();page.wait_for_url('**/m01-p02.html')
 assert 'Newdemo123' not in page.evaluate("JSON.stringify({...localStorage,...sessionStorage})")
def binding(page):
 go(page,'m02-p03');invite(page);page.locator('button.preview').click();page.wait_for_url('**/m02-p04.html',timeout=3500)
 page.get_by_role('button',name='暂不接受',exact=True).click();page.wait_for_url('**/m02-p01.html')
 assert page.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-relationship')||'null')?.bound") is not True
 go(page,'m02-p03');invite(page);page.locator('button.preview').click();page.wait_for_url('**/m02-p04.html',timeout=3500)
 page.locator('button.confirm').click();page.wait_for_url('**/m02-p05.html',timeout=3500)
 assert page.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-relationship')).bound") is True
 page.locator('button.primary').click();page.wait_for_url('**/m03-p05.html')
def expired(page):
 go(page,'m02-p03');page.evaluate("localStorage.setItem('dujia-prototype-invite',JSON.stringify({code:'XH7K9M2Q',expiresAt:1,status:'pending'}))")
 invite(page);page.locator('button.preview').click();page.wait_for_url('**/m02-p08.html',timeout=3500)
 page.locator('button.reenter').click();page.wait_for_url('**/m02-p03.html');invite(page,'ZZZZZZZZ');page.locator('button.preview').click()
 expect(page.locator('#error')).to_be_visible();expect(page.locator('#error')).to_contain_text('邀请码',timeout=2000)
def existing(page):
 go(page,'m02-p03');page.evaluate("localStorage.setItem('dujia-prototype-relationship',JSON.stringify({bound:true,partner:'阿舟',id:'pair-keep'}))")
 invite(page);page.locator('button.preview').click();page.wait_for_url('**/m02-p09.html',timeout=3500)
 assert page.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-relationship')).id")=='pair-keep'
def profile(page):
 go(page,'m02-p06');page.evaluate("localStorage.setItem('dujia-prototype-relationship',JSON.stringify({bound:true,partner:'阿舟'}))");page.reload()
 page.locator('#nickname').fill('星星与晚风');page.locator('button.back').click()
 expect(page.locator('dialog[open]')).to_be_visible(timeout=2000);page.get_by_role('button',name='继续编辑',exact=True).click();expect(page.locator('dialog[open]')).to_have_count(0)
 assert page.locator('#nickname').input_value()=='星星与晚风'
 page.locator('#met').click();expect(page.locator('dialog.prototype-sheet[open]')).to_be_visible(timeout=2000)
 page.locator('dialog input[type=date]').fill('2026-03-01');page.get_by_role('button',name='使用这个日期',exact=True).click();expect(page.locator('dialog[open]')).to_have_count(0)
 page.locator('button.save').click();page.wait_for_url('**/m02-p05.html',timeout=3500)
 go(page,'m02-p06');assert page.locator('#nickname').input_value()=='星星与晚风';assert '3' in page.locator('#met').input_value()
def browser_back(page):
 go(page,'m01-p02');page.get_by_role('link',name='《用户协议》',exact=True).click();expect(page.locator('dialog[open]')).to_be_visible()
 page.go_back();expect(page.locator('dialog[open]')).to_have_count(0);assert page.url.endswith('m01-p02.html')
 go(page,'m02-p05');page.locator('button.secondary').click();page.wait_for_url('**/m02-p06.html');page.locator('#nickname').fill('未保存名字')
 page.go_back();expect(page.locator('dialog[open]')).to_be_visible(timeout=2000);page.get_by_role('button',name='继续编辑',exact=True).click()
 expect(page.locator('dialog[open]')).to_have_count(0);assert page.url.endswith('m02-p06.html');assert page.locator('#nickname').input_value()=='未保存名字'
 page.go_back();expect(page.locator('dialog[open]')).to_be_visible(timeout=2000);page.get_by_role('button',name='放弃修改',exact=True).click();page.wait_for_url('**/m02-p05.html',timeout=3500)
def share_wait(page):
 go(page,'m02-p02');page.locator('#share').click();expect(page.locator('dialog.prototype-sheet[open]')).to_be_visible(timeout=2000)
 page.get_by_role('button',name='查看邀请进度',exact=True).click();page.wait_for_url('**/m02-p07.html',timeout=3500)
 page.wait_for_url('**/m02-p05.html',timeout=5000)
 assert page.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-relationship')).bound") is True

cases={'registration-and-verification':register,'recovery-and-reset':recovery,'accept-cancel-confirm-and-first-diary':binding,'expired-and-invalid-invite':expired,'already-bound-keeps-relationship':existing,'profile-dirty-sheet-save-reopen':profile,'browser-back-modal-and-dirty-form':browser_back,'share-sheet-wait-peer-confirmation':share_wait}
import hashlib
DEMO=Path(__file__).resolve().parents[1]
def source():return {p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in list((DEMO/'custom').glob('*.html'))+list((DEMO/'assets').glob('prototype-*.*'))}
source_files=source()
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in cases.items():
  context=browser.new_context(viewport={'width':390,'height':844});page=context.new_page();page.set_default_timeout(3500);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  try:run(page);assert not errors,errors;row={'case':name,'passed':True,'errors':[]}
  except Exception as error:row={'case':name,'passed':False,'failure':str(error)[:1000],'errors':errors}
  page.screenshot(path=str(OUT/f'onboarding-{name}.png'),full_page=True);row['final_url']=page.url;results.append(row)
  print(('PASS' if row['passed'] else 'FAIL')+' '+name,flush=True);context.close()
 browser.close()
assert source_files==source(), 'Source changed during account regression'
(OUT/'onboarding-flow-source.json').write_text(json.dumps({'files':source_files},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'onboarding-flow-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
raise SystemExit(0 if all(r['passed'] for r in results) else 1)
