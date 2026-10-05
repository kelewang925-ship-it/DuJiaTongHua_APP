"""Actual nested controls in account/relationship overlays, in isolated local fixtures."""
from pathlib import Path
import json,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from execution_source import current_source_fingerprint

ROOT=Path(__file__).resolve().parent;BASE='http://127.0.0.1:8765/'
def snapshot(p):
    return p.locator('dialog[open]').evaluate('e=>({title:e.querySelector("h2").textContent,type:e.classList.contains("prototype-sheet")?"sheet":"modal",controls:[...e.querySelectorAll("button,input,select,textarea")].map(c=>({tag:c.tagName,type:c.type,label:c.getAttribute("aria-label")||c.textContent.trim(),disabled:c.disabled}))})')

def run(p,c):
    page,action=c['page'],c['action'];p.goto(BASE+'prototype/review.html')
    p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v));sessionStorage.setItem("dujia-prototype-peer-response","manual");}',data(False))
    p.goto(BASE+'pages/'+page+'.html');before=p.evaluate('JSON.stringify({...localStorage})');overlays=[]
    if action.startswith('terms-'):
        p.get_by_role('link',name=c['label'],exact=True).click();overlays.append(snapshot(p))
        p.get_by_role('button',name='知道了',exact=True).click();expect(p.locator('dialog')).to_have_count(0)
        assert p.url.endswith(page+'.html') and p.evaluate('JSON.stringify({...localStorage})')==before
    elif action.startswith('verify-'):
        p.locator('#switch').click();overlays.append(snapshot(p))
        if action=='verify-phone':
            p.get_by_role('button',name='重新填写手机号',exact=True).click();p.wait_for_url('**/m01-p04.html')
        else:
            p.get_by_role('button',name='查看演示验证码',exact=True).click();expect(p.locator('dialog h2')).to_have_text('演示验证码');expect(p.locator('dialog')).to_contain_text('284631');overlays.append(snapshot(p))
            p.get_by_role('button',name='知道了',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert p.url.endswith(page+'.html')
        assert p.evaluate('JSON.stringify({...localStorage})')==before
    elif action.startswith('share-'):
        p.locator('#share').click();overlays.append(snapshot(p))
        if action=='share-copy':
            p.get_by_role('button',name='复制邀请链接',exact=True).click();expect(p.locator('.prototype-toast')).to_have_text('已复制');assert p.evaluate('navigator.clipboard.readText()')==BASE+'pages/m02-p03.html?code=XH7K9M2Q';assert p.evaluate('JSON.stringify({...localStorage})')==before
        elif action=='share-save':
            with p.expect_download() as info:p.locator('dialog[open]').get_by_role('button',name='保存邀请卡',exact=True).click()
            d=info.value;assert d.suggested_filename=='独家童话邀请卡.svg';assert 'XH7K-9M2Q' in Path(d.path()).read_text(encoding='utf-8');assert p.evaluate('JSON.stringify({...localStorage})')==before
        else:
            p.get_by_role('button',name='查看邀请进度',exact=True).click();p.wait_for_url('**/m02-p07.html');invite=p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-invite'))");assert invite['status']=='pending' and invite['autoAt']>0
    elif action.startswith('date-'):
        selector='#met' if action in ['date-met','date-cancel'] else '#anniversary';old=p.locator(selector).input_value();p.locator(selector).click();overlays.append(snapshot(p))
        p.locator('dialog input[type=date]').fill('2026-03-02')
        if action=='date-cancel':
            p.get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog')).to_have_count(0);expect(p.locator(selector)).to_have_value(old)
        else:
            if action in ['date-month','date-year']:p.locator('dialog select').select_option('monthly' if action=='date-month' else 'yearly')
            p.get_by_role('button',name='使用这个日期' if action=='date-met' else '使用这个纪念日',exact=True).click();expect(p.locator('dialog')).to_have_count(0)
            expect(p.locator(selector)).to_have_value({'date-met':'2026年3月2日','date-month':'每月 2 日','date-year':'每年 3 月 2 日'}[action])
            p.locator('button.back').click();expect(p.locator('dialog h2')).to_have_text('是否放弃当前修改？');overlays.append(snapshot(p));p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('dialog')).to_have_count(0)
            expect(p.locator(selector)).to_have_value({'date-met':'2026年3月2日','date-month':'每月 2 日','date-year':'每年 3 月 2 日'}[action])
        assert p.evaluate('JSON.stringify({...localStorage})')==before
    elif action=='resend':
        button=p.locator('#resend');expect(button).to_be_disabled()
        p.locator('.code input').first.fill('1')
        p.evaluate("const k='dujia-prototype-challenge';const c=JSON.parse(sessionStorage.getItem(k));c.resendAt=Date.now()-1;sessionStorage.setItem(k,JSON.stringify(c));")
        expect(button).to_be_enabled();button.click();expect(p.locator('.prototype-toast')).to_contain_text('284631');expect(button).to_be_disabled()
        assert all(not v for v in p.locator('.code input').evaluate_all('es=>es.map(e=>e.value)'))
        assert p.evaluate('JSON.stringify({...localStorage})')==before
    else:raise AssertionError(action)
    return overlays

cases=[{'page':p,'action':'terms-'+str(i),'label':label} for p in ['m01-p02','m01-p03'] for i,label in enumerate(['《用户协议》','《隐私政策》'])]+[{'page':'m01-p07','action':a} for a in ['verify-phone','verify-code','resend']]+[{'page':'m02-p02','action':a} for a in ['share-copy','share-save','share-wait']]+[{'page':'m02-p06','action':a} for a in ['date-met','date-month','date-year','date-cancel']]
rows=[]
fingerprint=current_source_fingerprint()
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for case in cases:
        context=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce',accept_downloads=True);context.grant_permissions(['clipboard-read','clipboard-write'],origin=BASE[:-1]);p=context.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
        try:
            overlays=run(p,case);assert not errors,errors;row={**case,'passed':True,'overlays':overlays}
        except Exception:row={**case,'passed':False,'failure':traceback.format_exc()[-2200:]}
        row.update(errors=errors,effective=p.url,source_fingerprint=fingerprint);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+case['page']+' '+case['action'],flush=True);context.close()
    browser.close()
assert current_source_fingerprint()==fingerprint, 'Source changed during overlay execution'
(ROOT/'evidence/current/onboarding-overlay-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
