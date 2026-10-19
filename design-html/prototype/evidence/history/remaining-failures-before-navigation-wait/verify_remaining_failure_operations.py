"""User actions, actual failure consumption, unchanged data and successful retry."""
import base64
import json
import traceback
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from audit_current_runtime import data
from book_test_helpers import fixture

OUT=Path(__file__).resolve().parent/'evidence/current'
BASE='http://127.0.0.1:8765/'


def go(p,page,query=''):
    p.goto(BASE+'pages/'+page+'.html'+query)


def seed(p,populated=True):
    p.goto(BASE+'prototype/review.html')
    p.evaluate("d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem('dujia-prototype-today','2026-10-05');sessionStorage.setItem('dujia-prototype-peer-response','manual');for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v));}",data(populated))


def stored(p):
    return p.evaluate('JSON.stringify(Object.fromEntries(Object.entries(localStorage).sort()))')


def fail(p,operation,action,unchanged=True):
    before=stored(p)
    p.evaluate("op=>{document.querySelectorAll('.prototype-toast').forEach(e=>e.remove());sessionStorage.setItem('dujia-prototype-fail-next',op)}",operation)
    action()
    p.wait_for_function("op=>sessionStorage.getItem('dujia-prototype-fail-next')!==op",arg=operation)
    expect(p.locator('.prototype-toast')).to_be_visible()
    if unchanged:assert stored(p)==before,operation+' wrote data on failure'


def login(p):
    seed(p,False);go(p,'m01-p02');p.locator('[name=phone]').fill('13812345678');p.locator('[name=password]').fill('Demo1234')
    p.evaluate("sessionStorage.setItem('dujia-prototype-fail-next','credentials')")
    p.locator('button[form=form]').click();p.wait_for_url('**/m01-p06.html')
    assert not p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-session')).loggedIn")
    p.locator('#password').fill('Demo1234');button=p.locator('.retry')
    fail(p,'login',button.click);expect(p.locator('#password')).to_have_value('Demo1234')
    button.click();p.wait_for_url('**/m02-p01.html');assert p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-session')).loggedIn")


def send_code(p):
    seed(p,False);go(p,'m01-p03');p.locator('[name=phone]').fill('13812345678');button=p.locator('#send-code')
    fail(p,'send-code',button.click);assert p.evaluate("sessionStorage.getItem('dujia-prototype-challenge')")is None
    button.click();expect(button).to_be_disabled();assert p.evaluate("JSON.parse(sessionStorage.getItem('dujia-prototype-challenge')).phone")=='13812345678'


def register(p):
    seed(p,False);go(p,'m01-p03');p.locator('[name=nickname]').fill('失败后仍在');p.locator('[name=phone]').fill('13812345678');p.locator('#password').fill('Demo1234');p.locator('input[type=checkbox]').check();p.locator('.submit').click();p.wait_for_url('**/m01-p07.html')
    for i,c in enumerate('284631'):p.locator('.code input').nth(i).fill(c)
    fail(p,'register',p.locator('.verify').click)
    assert not p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-session')).loggedIn")
    p.locator('.verify').click();p.wait_for_url('**/m02-p01.html');assert p.evaluate("JSON.parse(localStorage.getItem('dujia-profile')).nickname")=='失败后仍在'


def reset(p):
    seed(p,False);go(p,'m01-p04');p.locator('[name=phone]').fill('13812345678');p.locator('.next').click();p.wait_for_url('**/m01-p07.html')
    for i,c in enumerate('284631'):p.locator('.code input').nth(i).fill(c)
    p.locator('.verify').click();p.wait_for_url('**/m01-p05.html');p.locator('#password').fill('Newdemo123');p.locator('#confirm').fill('Newdemo123')
    fail(p,'reset',p.locator('.submit').click);expect(p.locator('#confirm')).to_have_value('Newdemo123')
    p.locator('.submit').click();p.wait_for_url('**/m01-p08.html');assert 'Newdemo123'not in stored(p)


def invitation(p):
    seed(p,False);go(p,'m02-p03')
    for i in range(4):p.locator('.code input').nth(i).fill('XH7K9M2Q'[i*2:i*2+2])
    fail(p,'invite',p.locator('.preview').click);expect(p.locator('.code input').first).to_have_value('XH')
    p.locator('.preview').click();p.wait_for_url('**/m02-p04.html')


def remind(p):
    seed(p,False);go(p,'m02-p07');button=p.locator('#remind');fail(p,'remind',button.click);button.click()
    expect(p.locator('.prototype-toast')).to_contain_text('已提醒');assert p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-invite')).autoAt")>0


def preference(p):
    seed(p);go(p,'m06-p09');button=p.get_by_role('switch',name='另一半回应',exact=True);old=button.get_attribute('aria-checked')
    fail(p,'settings-preference',button.click);expect(button).to_have_attribute('aria-checked',old);button.click();expect(button).to_have_attribute('aria-checked','false'if old=='true'else'true')


def update(p):
    seed(p);go(p,'m06-p12');button=p.locator('.updates');fail(p,'settings-update',button.click);expect(p.locator('dialog[open]')).to_have_count(0)
    button.click();expect(p.get_by_role('heading',name='版本信息',exact=True)).to_be_visible()


def logout(p):
    seed(p);p.evaluate("localStorage.setItem('dujia-prototype-session',JSON.stringify({loggedIn:true,phone:'13812345678'}))");go(p,'m06-p07');p.locator('.logout').click()
    fail(p,'settings-logout',p.get_by_role('button',name='确认退出',exact=True).click)
    assert p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-session')).loggedIn")
    records=p.evaluate("localStorage.getItem('dujia-prototype-records')");p.locator('.logout').click();p.get_by_role('button',name='确认退出',exact=True).click();p.wait_for_url('**/m01-p01.html');assert p.evaluate("localStorage.getItem('dujia-prototype-records')")==records


def tag(p):
    seed(p);go(p,'m06-p05');p.get_by_role('button',name='新建标签',exact=True).click();p.get_by_label('标签名称',exact=True).fill('失败后新增')
    fail(p,'settings-tag',p.get_by_role('button',name='保存标签',exact=True).click);expect(p.get_by_label('标签名称',exact=True)).to_have_value('失败后新增')
    p.get_by_role('button',name='保存标签',exact=True).click();expect(p.get_by_role('button',name='失败后新增',exact=True)).to_be_visible()


def export(p,kind):
    seed(p)
    if kind=='book':
        p.evaluate("b=>localStorage.setItem('dujia-prototype-books',JSON.stringify([b]))",fixture());go(p,'m08-p21','?id=book-state');button=p.get_by_role('button',name='导出这本回忆册',exact=True)
    elif kind=='pet':go(p,'m07-p24');button=p.locator('#export')
    else:go(p,'m06-p11');button=p.locator('#export')
    downloads=[];p.on('download',lambda d:downloads.append(d));fail(p,kind+'-export',button.click);assert not downloads
    with p.expect_download()as download:button.click()
    payload=json.loads(Path(download.value.path()).read_text(encoding='utf-8'));assert payload


def save(p,kind):
    seed(p)
    if kind=='diary':
        go(p,'m03-p05');field=p.locator('[name=title]');field.fill('失败后保留的日记');p.locator('[name=body]').fill('实际正文');button=p.locator('.submit');key='records'
    elif kind=='moment':
        go(p,'m04-p04','?id=audit-moment');field=p.locator('[name=name]');field.fill('失败后保留的时刻');button=p.locator('.submit');key='moments'
    elif kind=='anniversary':
        go(p,'m04-p09','?id=audit-anniversary');field=p.locator('[name=name]');field.fill('失败后保留的纪念日');button=p.locator('.submit');key='anniversaries'
    else:
        go(p,'m03-p11','?id=audit-photo');field=p.locator('[name=caption]');field.fill('失败后保留的照片');button=p.locator('#done');key='records'
    text=field.input_value();fail(p,kind+'-save',button.click);expect(field).to_have_value(text);button.click()
    p.wait_for_function("([key,text])=>JSON.parse(localStorage.getItem('dujia-prototype-'+key)).some(r=>[r.title,r.name,r.caption].includes(text))",arg=[key,text])


def comment(p):
    seed(p);go(p,'m04-p03','?id=audit-moment');p.get_by_role('button',name='回应这个时刻',exact=True).click();field=p.get_by_label('回应这个时刻',exact=True);field.fill('失败后保留的回应')
    button=p.get_by_role('button',name='发送回应',exact=True);fail(p,'moment-comment',button.click);expect(field).to_have_value('失败后保留的回应');button.click();expect(p.locator('dialog[open]')).to_have_count(0)
    assert p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-moments'))[0].comments.some(c=>c.text==='失败后保留的回应')")


cases={'credentials-and-login-retry':login,'send-code-failure-retry':send_code,'register-failure-retry':register,'reset-failure-retry':reset,'invite-failure-retry':invitation,'remind-failure-retry':remind,'preference-failure-retry':preference,'version-failure-retry':update,'logout-failure-keeps-records':logout,'tag-failure-retains-input':tag,'moment-comment-failure-retry':comment}
for kind in ['book','pet','settings']:cases[kind+'-export-failure-no-download-retry']=lambda p,k=kind:export(p,k)
for kind in ['diary','moment','anniversary','photo']:cases[kind+'-save-failure-retains-input-retry']=lambda p,k=kind:save(p,k)
rows=[]
with sync_playwright()as pw:
    browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for name,run in cases.items():
        context=browser.new_context(viewport=dict(width=390,height=844),accept_downloads=True);p=context.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda error:errors.append(str(error)))
        try:run(p);assert not errors;row=dict(case=name,passed=True)
        except Exception:row=dict(case=name,passed=False,failure=traceback.format_exc()[-2400:])
        row.update(errors=errors,final_url=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+name,flush=True);context.close()
    browser.close()
(OUT/'remaining-failures-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(row['passed']for row in rows)else 1)
