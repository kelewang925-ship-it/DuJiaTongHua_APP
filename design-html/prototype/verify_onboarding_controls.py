"""Execute each currently available initial account/relationship control against an explicit contract.
These are one representative state per control, not all conditions or final page acceptance.
"""
from pathlib import Path
import json, traceback
from playwright.sync_api import sync_playwright, expect
from audit_current_runtime import data
from execution_source import current_source_fingerprint

ROOT=Path(__file__).resolve().parent
BASE='http://127.0.0.1:8765/'
# Exact initial labels from runtime inventory; expected results are declared, never inferred from onclick.
RULES={
 'm01-p01':{'登录并开始':'route:m01-p02','创建账号':'route:m01-p03'},
 'm01-p02':{'返回':'route:m01-p01','显示密码':'eye:password','忘记密码？':'route:m01-p04','登录并回到故事里':'login:m02-p01','创建账号':'route:m01-p03','《用户协议》':'modal:《用户协议》','《隐私政策》':'modal:《隐私政策》'},
 'm01-p03':{'返回欢迎页':'route:m01-p01','获取验证码':'send:register','显示密码':'eye:password','《用户协议》':'modal:《用户协议》','《隐私政策》':'modal:《隐私政策》','创建账号':'register:m01-p07','去登录':'route:m01-p02'},
 'm01-p04':{'返回':'route:m01-p02','获取验证码':'send:recovery','下一步':'recovery:m01-p07','返回登录':'route:m01-p02'},
 'm01-p05':{'返回找回密码':'route:m01-p04','显示新密码':'eye:password','显示确认密码':'eye:confirm','确认并重置':'reset:m01-p08'},
 'm01-p06':{'返回':'route:m01-p02','显示密码':'eye:password','再试一次':'retry:m02-p01','找回密码':'route:m01-p04'},
 'm01-p07':{'返回':'route:m01-p04','验证并继续':'verify:m01-p05','没收到验证码？换个方式':'sheet:换一种验证方式'},
 'm01-p08':{'返回登录':'route:m01-p02'},
 'm02-p01':{'返回登录':'route:m01-p02','邀请 TA 加入\n生成专属邀请码':'route:m02-p02','输入 TA 的邀请码\n接受一份特别邀请':'route:m02-p03'},
 'm02-p02':{'返回建立关系':'route:m02-p01','✦ 复制邀请码 ✦':'clipboard:XH7K-9M2Q','发送给微信好友':'sheet:分享邀请','保存邀请卡':'download:独家童话邀请卡.svg'},
 'm02-p03':{'返回':'route:m02-p01','查看邀请内容':'invite:m02-p04','请让 TA 分享给你':'route:m02-p01'},
 'm02-p04':{'返回':'route:m02-p03','确认建立关系':'bind:m02-p05','暂不接受':'cancel:m02-p01'},
 'm02-p05':{'去写第一篇共同日记 ♡':'route:m03-p05','完善情侣资料':'route:m02-p06'},
 'm02-p06':{'返回':'route:m02-p05','保存小资料':'profile:m02-p01','相遇日期':'picker:选择相遇日期','共同纪念日':'picker:选择共同纪念日'},
 'm02-p07':{'返回邀请卡':'route:m02-p02','提醒 TA 看看':'remind:已提醒 TA 查看邀请','复制邀请链接':'clipboard-link:m02-p03.html?code=XH7K9M2Q'},
 'm02-p08':{'请 TA 重新邀请':'renew:m02-p01','重新输入邀请码':'route:m02-p03'},
 'm02-p09':{'回到我们的首页':'route:m03-p01','查看关系设置':'route:m02-p06'}
}

def storage(p):return p.evaluate('JSON.stringify({...localStorage})')

def run(p,context,c):
    id=c['id'];kind,target=c['contract'].split(':',1)
    p.goto(BASE+'prototype/review.html')
    p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v));sessionStorage.setItem("dujia-prototype-peer-response","manual");}',data(False))
    if id=='m01-p05':p.evaluate("sessionStorage.setItem('dujia-prototype-challenge',JSON.stringify({purpose:'recovery',verified:true,phone:'13812345678',expiresAt:Date.now()+600000,code:'284631'}))")
    p.goto(BASE+'pages/'+id+'.html');p.evaluate('document.fonts.ready')
    control=p.locator(c['selector']);expect(control).to_be_visible();expect(control).to_be_enabled()
    before=storage(p)
    if kind in ['login','send','register','recovery']:
        p.locator('[name=phone]').fill('13812345678')
    if kind in ['login','retry','register','reset']:
        p.locator('#password').fill('Demo1234')
    if kind=='register':
        p.locator('[name=nickname]').fill('星星');p.locator('input[type=checkbox]').check();p.locator('[name=code]').fill('')
    if kind=='reset':p.locator('#confirm').fill('Demo1234')
    if kind=='verify':
        for index,value in enumerate('284631'):p.locator('.code input').nth(index).fill(value)
    if kind=='profile':
        p.locator('#nickname').fill('星星与晚风')
        # Existing date defaults are valid; the corresponding controls are separately exercised.
    if kind=='download':
        with p.expect_download() as info:control.click()
        download=info.value;assert download.suggested_filename==target
        payload=Path(download.path()).read_text(encoding='utf-8');assert '<svg' in payload and 'XH7K-9M2Q' in payload
        assert storage(p)==before
        return {'download_name':download.suggested_filename,'svg_bytes':len(payload.encode('utf-8'))}
    if kind=='input':
        typ=control.get_attribute('type') or 'text'
        if typ=='checkbox':
            initial=control.is_checked();control.set_checked(not initial);assert control.is_checked() != initial
        else:
            control.click()
            expect(control).to_be_focused()
            value=('2' if id=='m01-p07' else 'xh' if id=='m02-p03' else '13812345678' if '手机号' in c['label'] else '284631' if '验证码' in c['label'] else 'Demo1234' if typ=='password' else '星星')
            control.fill(value);expect(control).to_have_value(value.upper() if id=='m02-p03' else value)
        assert storage(p)==before
        return {'native_edit':True}
    control.click()
    if kind in ['route','login','register','recovery','reset','retry','verify','invite','bind','cancel','profile','renew']:
        p.wait_for_url('**/'+target+'.html*')
        if kind in ['login','retry']:assert p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-session')).loggedIn") is True
        elif kind in ['register','recovery']:assert p.evaluate("JSON.parse(sessionStorage.getItem('dujia-prototype-challenge')).purpose")==('register' if kind=='register' else 'recovery')
        elif kind=='reset':assert p.evaluate("sessionStorage.getItem('dujia-prototype-reset-complete')")
        elif kind=='verify':assert p.evaluate("JSON.parse(sessionStorage.getItem('dujia-prototype-challenge')).verified") is True
        elif kind=='invite':assert p.evaluate("sessionStorage.getItem('dujia-prototype-incoming-invite')")=='XH7K9M2Q'
        elif kind=='bind':assert p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-relationship')).bound") is True
        elif kind=='cancel':assert p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-relationship')).bound") is False
        elif kind=='profile':assert p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-relationship')).profile.nickname")=='星星与晚风'
        elif kind=='renew':assert p.evaluate("localStorage.getItem('dujia-prototype-invite')") is None
    elif kind=='eye':
        expect(p.locator('#'+target)).to_have_attribute('type','text');control.click();expect(p.locator('#'+target)).to_have_attribute('type','password');assert storage(p)==before
    elif kind in ['modal','sheet','picker']:
        expect(p.locator('dialog[open] h2')).to_have_text(target)
        if kind!='modal':expect(p.locator('dialog.prototype-sheet[open]')).to_be_visible()
        if kind=='picker':expect(p.locator('dialog input[type=date]')).to_be_visible()
        p.keyboard.press('Escape');expect(p.locator('dialog')).to_have_count(0)
        expect(control).to_be_focused();assert storage(p)==before
    elif kind=='send':
        expect(p.locator('.prototype-toast')).to_contain_text('284631');expect(control).to_be_disabled()
        challenge=p.evaluate("JSON.parse(sessionStorage.getItem('dujia-prototype-challenge'))");assert challenge['purpose']==target and challenge['phone']=='13812345678';assert storage(p)==before
    elif kind in ['clipboard','clipboard-link']:
        expect(p.locator('.prototype-toast')).to_have_text('已复制')
        copied=p.evaluate('navigator.clipboard.readText()');assert copied==target if kind=='clipboard' else copied.endswith(target)
        assert storage(p)==before
    elif kind=='remind':
        expect(p.locator('.prototype-toast')).to_have_text(target)
        invite=p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-invite'))");assert invite['autoAt']>p.evaluate('Date.now()');assert p.url.endswith(id+'.html')
    else:raise AssertionError('Unsupported contract: '+c['contract'])
    assert 'Demo1234' not in p.evaluate('JSON.stringify({...localStorage,...sessionStorage})')
    return {'effective':p.url}

def main():
    fingerprint=current_source_fingerprint()
    rows=json.loads((ROOT/'evidence/current/current-runtime-inventory.json').read_text(encoding='utf-8'));cases=[]
    for row in rows:
        if row['scenario']!='empty' or row['id'] not in RULES:continue
        assert row['effective'].split('/')[-1].split('?')[0]==row['id']+'.html'
        for control in row['observed']['controls']:
            if not control['visible'] or control['disabled']:continue
            contract=RULES[row['id']].get(control['label'])
            if contract is None and control['native_input']:contract='input:native'
            assert contract, (row['id'],control['label'],'missing explicit contract')
            cases.append({'id':row['id'],'selector':control['selector'],'label':control['label'],'contract':contract,'scenario':'initial-empty-fixture'})
    assert len({c['id'] for c in cases})==17
    results=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for index,case in enumerate(cases):
            context=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce',accept_downloads=True)
            context.grant_permissions(['clipboard-read','clipboard-write'],origin=BASE[:-1]);page=context.new_page();page.set_default_timeout(4500);errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            try:
                details=run(page,context,case);assert not errors,errors;result={**case,'passed':True,'details':details}
            except Exception:result={**case,'passed':False,'failure':traceback.format_exc()[-2200:]}
            result.update(errors=errors,effective=page.url,source_fingerprint=fingerprint);results.append(result);context.close()
            print(('PASS ' if result['passed'] else 'FAIL ')+case['id']+' '+case['label'].replace('\n',' / '),flush=True)
    assert current_source_fingerprint()==fingerprint, 'Source changed during control execution'
    out=ROOT/'evidence/current/onboarding-control-results.json';out.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(f'Executed {len(results)} initial controls across 17 pages; {sum(r["passed"] for r in results)} passed',flush=True)
    raise SystemExit(0 if all(r['passed'] for r in results) else 1)

if __name__=='__main__':main()
