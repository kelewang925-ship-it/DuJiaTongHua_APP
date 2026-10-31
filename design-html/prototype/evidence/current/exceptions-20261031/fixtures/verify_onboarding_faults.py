"""Exercise recovery from stale errors and failed local mutations in real Chrome."""
from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright,expect

parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');args=parser.parse_args()
OUT=Path(__file__).resolve().parent/'evidence'/('baseline' if args.baseline else 'current')
OUT.mkdir(parents=True,exist_ok=True)
def go(page,id):page.goto('http://127.0.0.1:8765/pages/'+id+'.html')
def seed(page,key,value):page.evaluate('([k,v])=>sessionStorage.setItem(k,JSON.stringify(v))',[key,value])
def fail(page,operation):page.evaluate('(v)=>sessionStorage.setItem("dujia-prototype-fail-next",v)',operation)
def otp_resend(page):
 go(page,'m01-p07');seed(page,'dujia-prototype-challenge',{'purpose':'recovery','phone':'13812345678','code':'284631','expiresAt':1,'resendAt':1});page.reload()
 for i,c in enumerate('284631'):page.locator('.code input').nth(i).fill(c)
 page.locator('.verify').click();expect(page.locator('.prototype-code-error')).to_contain_text('过期')
 page.locator('#resend').click();expect(page.locator('#resend')).to_be_disabled()
 expect(page.locator('.prototype-code-error')).to_be_hidden()
 assert all(v=='' for v in page.locator('.code input').evaluate_all('(xs)=>xs.map(x=>x.value)'))
 for i,c in enumerate('284631'):page.locator('.code input').nth(i).fill(c)
 fail(page,'verify');page.locator('.verify').click();expect(page.locator('.prototype-toast')).to_contain_text('重试')
 assert page.url.endswith('m01-p07.html')
 assert page.evaluate('JSON.parse(sessionStorage.getItem("dujia-prototype-challenge")).verified') is False
 page.locator('.verify').click();page.wait_for_url('**/m01-p05.html')
def invite_paste(page):
 go(page,'m02-p03')
 for i in range(4):page.locator('.code input').nth(i).fill('ZZ')
 page.locator('.preview').click();expect(page.locator('#error')).to_be_visible()
 page.locator('.code input').first.evaluate('e=>{const d=new DataTransfer();d.setData("text/plain","XH7K-9M2Q");e.dispatchEvent(new ClipboardEvent("paste",{clipboardData:d,bubbles:true,cancelable:true}));}')
 expect(page.locator('#error')).to_be_hidden()
 assert page.locator('.code input[aria-invalid=true]').count()==0
 page.locator('.preview').click();page.wait_for_url('**/m02-p04.html')
def peer_expiry(page):
 go(page,'m02-p02');page.evaluate('sessionStorage.setItem("dujia-prototype-peer-response","expired")')
 page.locator('#share').click();page.get_by_role('button',name='查看邀请进度',exact=True).click();page.wait_for_url('**/m02-p08.html',timeout=6000)
 assert page.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-invite")).status')=='expired'
 page.locator('.reenter').click();page.locator('.preview').click();page.wait_for_url('**/m02-p08.html')
def failed_mutations(page):
 go(page,'m02-p04');fail(page,'bind');page.locator('.confirm').click();expect(page.locator('.prototype-toast')).to_contain_text('重试')
 assert page.evaluate('localStorage.getItem("dujia-prototype-relationship")') is None
 page.locator('.confirm').click();page.wait_for_url('**/m02-p05.html');page.locator('.secondary').click();page.wait_for_url('**/m02-p06.html')
 before=page.evaluate('localStorage.getItem("dujia-prototype-relationship")');page.locator('#nickname').fill('失败仍保留');fail(page,'profile')
 page.locator('.save').click();expect(page.locator('.prototype-toast')).to_contain_text('重试');assert page.locator('#nickname').input_value()=='失败仍保留'
 assert page.evaluate('localStorage.getItem("dujia-prototype-relationship")')==before
 page.locator('.save').click();page.wait_for_url('**/m02-p05.html');go(page,'m02-p06');assert page.locator('#nickname').input_value()=='失败仍保留'

results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'otp-expiry-resend-retry':otp_resend,'invite-paste-clears-error':invite_paste,'peer-expiry-persists':peer_expiry,'bind-profile-failure-retry':failed_mutations}.items():
  context=browser.new_context(viewport={'width':390,'height':844});page=context.new_page();page.set_default_timeout(4000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  try:run(page);assert not errors,errors;row={'case':name,'passed':True}
  except Exception as error:row={'case':name,'passed':False,'failure':str(error)[:1200]}
  row.update(errors=errors,final_url=page.url);results.append(row);page.screenshot(path=str(OUT/f'fault-{name}.png'),full_page=True);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);context.close()
 browser.close()
(OUT/'onboarding-fault-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
raise SystemExit(0 if all(r['passed'] for r in results) else 1)
