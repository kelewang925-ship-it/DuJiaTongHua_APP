"""Local session/invite corruption and OTP qualification must be recoverable."""
from pathlib import Path
import hashlib,json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent;BASE='http://127.0.0.1:8765/';SESSION='dujia-prototype-session';INVITE='dujia-prototype-invite';CHALLENGE='dujia-prototype-challenge'
OUT=ROOT/'evidence'/('baseline' if '--baseline' in sys.argv else 'current')
def source():return {p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in list((DEMO/'custom').glob('*.html'))+list((DEMO/'assets').glob('prototype-*.*'))}
def seed(p,key,raw,page,temporary=False):
    p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',data(True));p.evaluate('([k,v,temp])=>(temp?sessionStorage:localStorage).setItem(k,v)',[key,raw,temporary]);p.goto(BASE+'pages/'+page+'.html')
def get(p,key,temp=False):return p.evaluate('([k,temp])=>(temp?sessionStorage:localStorage).getItem(k)',[key,temp])
def heal(p):
    expect(p.locator('dialog h2')).to_have_text('资料需要恢复');p.get_by_role('button',name='恢复可读资料',exact=True).click();p.get_by_role('button',name='确认恢复',exact=True).click()
def local_bad(p,key,raw,page):
    seed(p,key,raw,page);before=get(p,'dujia-prototype-records');pair=get(p,'dujia-prototype-relationship');expect(p.locator('dialog h2')).to_have_text('资料需要恢复')
    with p.expect_download() as info:p.get_by_role('button',name='导出原始资料',exact=True).click()
    assert Path(info.value.path()).read_text(encoding='utf-8')==raw
    with p.expect_event('load'):heal(p)
    assert get(p,'dujia-prototype-records')==before and get(p,'dujia-prototype-relationship')==pair
    copies=p.evaluate('Object.keys(localStorage).filter(k=>k.startsWith("dujia-prototype-account-recovery-")).map(k=>JSON.parse(localStorage.getItem(k)))');assert copies==[raw]
    if key==SESSION:assert json.loads(get(p,key))['loggedIn'] is False
    else:assert isinstance(json.loads(get(p,key))['code'],str);expect(p.locator('#code')).to_have_text('XH7K-9M2Q')
def challenge_bad(p):
    raw=json.dumps({'purpose':'recovery','phone':{},'code':'284631','expiresAt':9999999999999});seed(p,CHALLENGE,raw,'m01-p07',True);expect(p.get_by_text('验证资料无法读取',exact=True)).to_be_visible();assert get(p,CHALLENGE,True)==raw
    p.get_by_role('button',name='去注册',exact=True).click();p.wait_for_url('**/m01-p03.html');assert get(p,CHALLENGE,True)==raw;p.locator('[name=phone]').fill('13812345678');p.locator('#send-code').click();expect(p.locator('.prototype-toast')).to_contain_text('284631');assert json.loads(get(p,CHALLENGE,True))['purpose']=='register'
def wrong_purpose(p):
    raw=json.dumps({'purpose':'recovery','phone':'13812345678','code':'284631','expiresAt':9999999999999,'verified':False});seed(p,CHALLENGE,raw,'m01-p03',True);before=get(p,SESSION)
    for name,value in [('nickname','星星'),('phone','13812345678'),('password','Demo1234'),('code','284631')]:p.locator('[name='+name+']').fill(value)
    p.locator('[type=checkbox]').check();p.locator('button.submit').click();expect(p.locator('[name=code]')).to_have_attribute('aria-invalid','true');assert get(p,SESSION)==before and p.url.endswith('m01-p03.html')
def expired_reset(p):
    raw=json.dumps({'purpose':'recovery','phone':'13812345678','code':'284631','expiresAt':1,'verified':True});seed(p,CHALLENGE,raw,'m01-p05',True);p.locator('[name=password]').fill('Demo1234');p.locator('[name=confirm]').fill('Demo1234');p.locator('button.submit').click();expect(p.locator('dialog h2')).to_have_text('先验证你的手机号');assert get(p,CHALLENGE,True)==raw and p.evaluate('sessionStorage.getItem("dujia-prototype-reset-complete")') is None
def register_cannot_recover(p):
    raw=json.dumps({'purpose':'register','phone':'13812345678','code':'284631','expiresAt':9999999999999});seed(p,CHALLENGE,raw,'m01-p04',True)
    p.locator('[name=phone]').fill('13812345678');p.locator('[name=code]').fill('284631');p.locator('button.next').click();expect(p.locator('[name=code]')).to_have_attribute('aria-invalid','true');assert get(p,CHALLENGE,True)==raw and p.url.endswith('m01-p04.html')
def missing_resend(p):
    raw=json.dumps({'purpose':'recovery','phone':'13812345678','code':'284631','expiresAt':9999999999999,'resendAt':0});seed(p,CHALLENGE,raw,'m01-p07',True);p.evaluate('k=>sessionStorage.removeItem(k)',CHALLENGE);p.locator('#resend').click();expect(p.locator('.prototype-toast')).to_contain_text('重新填写手机号');assert get(p,CHALLENGE,True) is None

def invalid_invite_actions(p):
    raw=json.dumps({'code':{},'status':'pending','expiresAt':9999999999999});seed(p,INVITE,raw,'m02-p07');p.get_by_role('button',name='稍后处理',exact=True).click();p.locator('#remind').click();expect(p.locator('.prototype-toast')).to_contain_text('未能准备邀请');assert get(p,INVITE)==raw
    p.goto(BASE+'pages/m02-p08.html');p.get_by_role('button',name='稍后处理',exact=True).click();p.locator('.again').click();expect(p.locator('dialog h2')).to_have_text('资料需要恢复');assert get(p,INVITE)==raw

def healthy_expired(p):
    raw=json.dumps({'code':'XH7K9M2Q','status':'expired','expiresAt':1});seed(p,INVITE,raw,'m02-p03');p.evaluate('localStorage.setItem("dujia-prototype-relationship",JSON.stringify({bound:false}))');p.reload();p.locator('.preview').click();p.wait_for_url('**/m02-p08.html');assert get(p,INVITE)==raw;expect(p.locator('dialog')).to_have_count(0)
def challenge_layout(p,width):
    p.set_viewport_size({'width':width,'height':844});raw='null';seed(p,CHALLENGE,raw,'m01-p07',True)
    for name in ['去注册','找回密码']:
        button=p.get_by_role('button',name=name,exact=True);button.scroll_into_view_if_needed();box=button.bounding_box();assert box['height']>=44 and box['x']>=0 and box['x']+box['width']<=width
    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth');p.screenshot(path=str(OUT/f'challenge-error-{width}.png'),full_page=True);assert get(p,CHALLENGE,True)==raw
cases={'null-session':lambda p:local_bad(p,SESSION,'null','m06-p08'),'session-phone-object':lambda p:local_bad(p,SESSION,json.dumps({'loggedIn':True,'phone':{}}),'m06-p08'),'invite-code-object':lambda p:local_bad(p,INVITE,json.dumps({'code':{},'expiresAt':9999999999999,'status':'pending'}),'m02-p02'),'invalid-challenge-phone':challenge_bad,'recovery-otp-cannot-register':wrong_purpose,'expired-verified-otp-cannot-reset':expired_reset}
if '--baseline' not in sys.argv:
    cases.update({'register-otp-cannot-recover':register_cannot_recover,'missing-challenge-resend':missing_resend,'corrupt-invite-actions-preserve-original':invalid_invite_actions,'healthy-expired-invite-business-exit':healthy_expired})
    for width in [320,360,390,414,430]:cases['challenge-error-layout-'+str(width)]=lambda p,width=width:challenge_layout(p,width)
rows=[];hashes=source()
with sync_playwright() as pw:
    b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for name,run in cases.items():
        c=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce',accept_downloads=True);p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
        try:run(p);assert not errors,errors;row={'case':name,'passed':True}
        except Exception:row={'case':name,'passed':False,'failure':traceback.format_exc()[-2100:]}
        row.update(errors=errors,effective=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
    b.close()
assert hashes==source()
(OUT/'session-invite-results.json').write_text(json.dumps({'files':hashes,'results':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
raise SystemExit(0 if all(row['passed'] for row in rows) else 1)
