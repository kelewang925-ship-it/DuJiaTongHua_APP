"""Real OTP/reset/register controls across held submit delays and failing local writes."""
import argparse,copy,hashlib,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from verify_pet_controls import ROOT,DEMO,BASE,source
from verify_submission_changes import HOLD

CHALLENGE='dujia-prototype-challenge';REGISTER_DRAFT='dujia-prototype-register-draft'
MODES=['unchanged','expired','deleted','phone-changed','purpose-changed','reissued','corrupt']
COLLECTIONS=['records','moments','anniversaries','capsules','works','books']
QUOTA=['dujia-profile','dujia-prototype-session']+['dujia-prototype-'+v for v in COLLECTIONS if v!='works']
CASES=[(k,m) for k in ['verify-recovery','verify-register','reset'] for m in MODES]+[('reset','verified-revoked')]+[(k,'actual-resend') for k in ['verify-recovery','verify-register']]+[(k,'quota:'+key) for k in ['register-direct','register-verify'] for key in QUOTA]+[(k,'fresh') for k in ['register-direct','register-verify']]
def state(p):return p.evaluate("({local:{...localStorage},session:{...sessionStorage}})")
def challenge(p):return p.evaluate("JSON.parse(sessionStorage.getItem('dujia-prototype-challenge'))")
def fill_code(p):
 for field,n in zip(p.locator('.code input').all(),'284631'):field.fill(n)
def seed(p,kind):
 p.goto(BASE+'prototype/review.html');fixture=data(False);fixture['dujia-profile']={'nickname':'原资料','saying':'必须保留'};fixture['dujia-prototype-session']={'loggedIn':False,'phone':'13812345678'}
 if kind.startswith('register-'):
  for n in COLLECTIONS+['creations']:fixture.pop('dujia-prototype-'+n,None)
 p.evaluate("v=>{localStorage.clear();sessionStorage.clear();for(const[k,d]of Object.entries(v))localStorage.setItem(k,JSON.stringify(d));const now=Date.now();window.__authFixtureNow=now;sessionStorage.setItem('dujia-prototype-challenge',JSON.stringify({purpose:'recovery',phone:'13812345678',code:'284631',expiresAt:now+60000,resendAt:0,verified:false}))}",fixture)
 purpose='register' if 'register' in kind else 'recovery';verified=kind=='reset';p.evaluate("v=>{const k='dujia-prototype-challenge',c=JSON.parse(sessionStorage.getItem(k));Object.assign(c,v);sessionStorage.setItem(k,JSON.stringify(c))}",dict(purpose=purpose,verified=verified,completeRegistration=purpose=='register',nickname='新用户'))
 page='m01-p03' if kind=='register-direct' else 'm01-p05' if kind=='reset' else 'm01-p07';p.goto(BASE+'pages/'+page+'.html')
 if page=='m01-p03':
  for n,v in [('nickname','新用户'),('phone','13812345678'),('password','Demo1234'),('code','284631')]:p.locator('[name='+n+']').fill(v)
  p.locator('[type=checkbox]').check()
 elif page=='m01-p05':p.locator('[name=password]').fill('Demo1234');p.locator('[name=confirm]').fill('Demo1234')
 else:fill_code(p)
 p.evaluate(HOLD)
 return '#register .submit' if page=='m01-p03' else '#reset .submit' if page=='m01-p05' else '#verify-form .verify'
def mutate(p,mode):
 p.evaluate("""mode=>{const k='dujia-prototype-challenge';if(mode==='unchanged')return;if(mode==='expired'){const now=Date.now;const offset=60001;Date.now=()=>now()+offset;return}if(mode==='deleted'){sessionStorage.removeItem(k);return}if(mode==='corrupt'){sessionStorage.setItem(k,'{"broken":');return}const c=JSON.parse(sessionStorage.getItem(k));if(mode==='phone-changed')c.phone='13987654321';else if(mode==='purpose-changed')c.purpose=c.purpose==='register'?'recovery':'register';else if(mode==='reissued'){c.expiresAt+=1234;c.resendAt=Date.now()+48000;c.verified=false}else if(mode==='verified-revoked')c.verified=false;else throw Error(mode);sessionStorage.setItem(k,JSON.stringify(c))}""",mode)
def release(p):p.evaluate('window.__releaseSubmissionTimers()')
def success(p,kind):
 p.wait_for_url('**/'+('m01-p08.html' if kind=='reset' else 'm01-p05.html' if kind=='verify-recovery' else 'm02-p01.html'))
 if kind=='reset':assert p.evaluate("sessionStorage.getItem('dujia-prototype-reset-complete')") and challenge(p) is None
 elif kind=='verify-recovery':assert challenge(p)['verified'] is True
 else:assert p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-session')).loggedIn") is True and challenge(p) is None
 saved=state(p);p.reload();assert state(p)==saved

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--baseline',action='store_true');args=ap.parse_args();out=ROOT/('evidence/baseline/auth-submit-context' if args.baseline else 'evidence/current/auth-submit-context');out.mkdir(parents=True,exist_ok=True);files=source();styles={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEMO/'assets').glob('*.css')};rows=[]
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for kind,mode in CASES:
   c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(kind=kind,mode=mode)
   try:
    submit=seed(p,kind);original=challenge(p);url=p.url
    if mode.startswith('quota:'):
     key=mode.removeprefix('quota:');p.evaluate("key=>{const set=Storage.prototype.setItem;window.__authQuota=0;Storage.prototype.setItem=function(k,v){if(this===localStorage&&k===key&&!window.__authQuota++){throw new DOMException('Injected quota failure','QuotaExceededError')}return set.call(this,k,v)}}",key)
     p.locator(submit).click();before=state(p);release(p);expect(p.locator(submit)).to_be_enabled();assert p.url==url and state(p)==before,'Failed registration left partial account/content state';expect(p.locator('.prototype-toast[role=alert]')).to_be_visible();assert p.evaluate('window.__authQuota')>=1;row['rollback_preserved_all_state']=True
     p.locator(submit).click();release(p);success(p,kind)
    elif mode=='fresh':
     p.locator(submit).click();release(p);success(p,kind);assert p.evaluate("localStorage.getItem('dujia-prototype-creations')") is None
     for n in COLLECTIONS:assert p.evaluate("key=>localStorage.getItem(key)",'dujia-prototype-'+n)=='[]',n
     row['actual_content_keys_initialized']=True
    else:
     p.locator(submit).click();expect(p.locator(submit)).to_have_attribute('aria-busy','true')
     if mode=='actual-resend':
      p.locator('#resend').click();p.evaluate('window.__submissionTimers.splice(1,1)[0]()');expect(p.locator('#resend')).not_to_have_attribute('aria-busy','true');assert challenge(p)!=original;fill_code(p)
     else:mutate(p,mode)
     changed=state(p);release(p)
     if mode=='unchanged':success(p,kind);row['normal_completed']=True
     else:
      expect(p.locator(submit)).to_be_enabled();assert p.url==url and state(p)==changed,'Stale verification/reset changed state or navigated'
      if kind=='reset':expect(p.locator('[name=password]')).to_have_value('Demo1234');expect(p.locator('[name=confirm]')).to_have_value('Demo1234')
      else:assert ''.join(p.locator('.code input').evaluate_all('v=>v.map(e=>e.value)'))=='284631'
      expect(p.locator('.prototype-toast[role=alert]')).to_be_visible();row['stale_submit_rejected_with_input']=True
      repaired={**original};p.evaluate("v=>{v.expiresAt=Date.now()+60000;sessionStorage.setItem('dujia-prototype-challenge',JSON.stringify(v))}",repaired);p.locator(submit).click();release(p);success(p,kind);row['explicit_retry_completed']=True
    assert not errors,errors;row['passed']=True
   except Exception:row.update(passed=False,failure=traceback.format_exc()[-2300:])
   row['errors']=errors;rows.append(row);c.close();assert source()==files
   (out/'results.json').write_text(json.dumps(dict(files=files,styles=styles,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=rows,scope='Real OTP/reset/registration controls; only550ms busy delay held, Date.now offset for expiry; actual resend and actual local quota failures; challenge mutations are explicit same-page sessionStorage simulations.',accepted_pages=0),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(('PASS ' if row['passed'] else 'FAIL ')+kind+' '+mode,flush=True)
  b.close()
 print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
 raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
