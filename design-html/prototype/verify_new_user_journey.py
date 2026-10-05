"""Continuous first-user flow. No business fixtures, clearing, or page jumps after entry."""
from pathlib import Path
import hashlib,json,sys,traceback
from playwright.sync_api import sync_playwright,expect

ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent;BASE='http://127.0.0.1:8765/'
OUT=ROOT/'evidence'/('baseline' if '--baseline' in sys.argv else 'current')
CONTENT=['records','moments','anniversaries','capsules','works','books']
def source():return {p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in list((DEMO/'custom').glob('*.html'))+list((DEMO/'assets').glob('prototype-*.*'))}
def records(p):return p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-records')||'[]')")
def no_content(p):
    values=p.evaluate("ks=>ks.map(k=>JSON.parse(localStorage.getItem('dujia-prototype-'+k)||'[]'))",CONTENT)
    assert all(isinstance(v,list) and not v for v in values),values
def step(p,steps,label,shot=False):
    p.evaluate('document.fonts.ready');steps.append({'step':label,'url':p.url,'records':len(records(p))})
    if shot:p.screenshot(path=str(OUT/('new-user-'+label+'.png')),full_page=True)
def publish(p,title,body):
    p.locator('[name=title]').fill(title);p.locator('[name=body]').fill(body)
    p.locator('#diary .submit').click();p.wait_for_url('**/m03-p06.html')

def serial(p,steps):
    p.goto(BASE+'pages/m01-p01.html');assert p.evaluate('localStorage.length')==0
    step(p,steps,'fresh-welcome')
    p.get_by_role('button',name='创建账号',exact=True).click();p.wait_for_url('**/m01-p03.html')
    p.locator('[name=nickname]').fill('星星');p.locator('[name=phone]').fill('13812345678');p.locator('#password').fill('Demo1234');p.locator('input[type=checkbox]').check();p.locator('[name=code]').fill('')
    p.get_by_role('button',name='创建账号',exact=True).click();p.wait_for_url('**/m01-p07.html')
    for i,v in enumerate('284631'):p.locator('.code input').nth(i).fill(v)
    p.get_by_role('button',name='验证并继续',exact=True).click();p.wait_for_url('**/m02-p01.html')
    session=p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-session'))");assert session['loggedIn'] and session['phone']=='13812345678';no_content(p);step(p,steps,'registered')
    p.locator('.choice.accept').click();p.wait_for_url('**/m02-p03.html')
    for i in range(4):p.locator('.code input').nth(i).fill('XH7K9M2Q'[i*2:i*2+2])
    p.get_by_role('button',name='查看邀请内容',exact=True).click();p.wait_for_url('**/m02-p04.html');p.get_by_role('button',name='确认建立关系',exact=True).click();p.wait_for_url('**/m02-p05.html')
    pair=p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-relationship'))");assert pair['bound'] and pair['id'];no_content(p)
    expect(p.locator('.names .pink')).to_have_text('星星');expect(p.locator('.names .green')).to_have_text(pair['partner'])
    expected_date=p.evaluate("at=>new Date(at).toLocaleDateString('zh-CN',{year:'numeric',month:'long',day:'numeric'})",pair['acceptedAt']);expect(p.locator('.date strong')).to_have_text(expected_date)
    step(p,steps,'bound',True)
    p.get_by_role('button',name='先逛逛我们的首页',exact=True).click();p.wait_for_url('**/m03-p01.html');no_content(p);step(p,steps,'first-empty-home',True)
    p.locator('.choice.diary').click();p.wait_for_url('**/m03-p05.html');expect(p.locator('[name=title]')).to_have_value('');expect(p.locator('[value=shared]')).to_be_enabled()
    p.locator('[name=title]').fill('第一篇共同日记');p.locator('[name=body]').fill('注册和关联后，亲手写下我们的第一篇故事。');before_failure=p.evaluate('JSON.stringify({...localStorage})')
    # Only a one-shot failure flag, never a business data fixture.
    p.evaluate("sessionStorage.setItem('dujia-prototype-fail-next','diary-save')")
    p.locator('#diary .submit').click();expect(p.locator('.prototype-toast')).to_contain_text('重试');expect(p.locator('[name=title]')).to_have_value('第一篇共同日记');assert p.evaluate('JSON.stringify({...localStorage})')==before_failure;step(p,steps,'first-save-failed-input-kept',True)
    p.locator('.back').click();expect(p.locator('dialog h2')).to_have_text('是否放弃当前修改？');p.locator('dialog').get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('dialog')).to_have_count(0)
    publish(p,'第一篇共同日记','注册和关联后，亲手写下我们的第一篇故事。');saved=records(p);assert len(saved)==1 and saved[0]['visibility']=='shared' and saved[0]['author']=='星星';id=saved[0]['id'];step(p,steps,'first-saved-list',True)
    p.get_by_role('button',name='第一篇共同日记',exact=False).click();p.wait_for_url('**/m03-p08.html?id=*');expect(p.locator('.body-text')).to_contain_text('亲手写下');step(p,steps,'first-detail')
    p.locator('.edit').click();p.wait_for_url('**/m03-p05.html?id=*');expect(p.locator('[name=title]')).to_have_value('第一篇共同日记');p.locator('[name=title]').fill('第一次更新我们的故事');p.locator('#diary .submit').click();p.wait_for_url('**/m03-p08.html?id=*');assert len(records(p))==1 and records(p)[0]['id']==id
    p.reload();expect(p.locator('h1')).to_have_text('第一次更新我们的故事');step(p,steps,'edited-and-reloaded',True)
    p.locator('.back').click();p.wait_for_url('**/m03-p06.html');p.locator('.back').click();p.wait_for_url('**/m03-p02.html');expect(p.locator('.prototype-home-record')).to_have_count(1);step(p,steps,'updated-home',True)
    p.locator('.prototype-home-record').click();p.wait_for_url('**/m03-p08.html?id=*')
    p.get_by_role('button',name='更多操作',exact=True).click();p.locator('dialog').get_by_role('button',name='删除日记',exact=True).click();p.locator('dialog').get_by_role('button',name='取消',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert records(p)[0]['id']==id
    p.get_by_role('button',name='更多操作',exact=True).click();p.locator('dialog').get_by_role('button',name='删除日记',exact=True).click();p.locator('dialog').get_by_role('button',name='确认删除',exact=True).click();p.wait_for_url('**/m03-p06.html');p.reload();expect(p.get_by_text('还没有日记',exact=True)).to_be_visible();assert records(p)==[];step(p,steps,'deleted-list',True)
    p.locator('.back').click();p.wait_for_url('**/m03-p01.html');no_content(p);assert p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-relationship')).id")==pair['id'];assert 'Demo1234' not in p.evaluate('JSON.stringify({...localStorage,...sessionStorage})');step(p,steps,'empty-home-after-delete',True)

def list_home(p,steps):
    p.goto(BASE+'pages/m03-p01.html');no_content(p);p.locator('.choice.diary').click();p.wait_for_url('**/m03-p05.html');publish(p,'从首页开始的日记','保存后应回到首页入口，而不是完成的编辑任务。');step(p,steps,'return-contract-saved')
    p.locator('.back').click();p.wait_for_url('**/m03-p02.html');expect(p.locator('.prototype-home-record')).to_have_count(1);step(p,steps,'return-contract-home')

cases={'new-user-continuous-registration-binding-diary-crud':serial,'diary-created-list-home-return':list_home}
rows=[];hashes=source()
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for name,run in cases.items():
        context=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');p=context.new_page();p.set_default_timeout(4500);errors=[];steps=[];p.on('pageerror',lambda e:errors.append(str(e)))
        try:run(p,steps);assert not errors,errors;row={'case':name,'passed':True}
        except Exception:row={'case':name,'passed':False,'failure':traceback.format_exc()[-2500:]}
        row.update(errors=errors,steps=steps,effective=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);context.close()
    browser.close()
assert hashes==source(), 'Source changed during continuous journey'
result={'scope':'Two real journeys, including one new registered user. No business data fixture or route jump after initial entry; not all product modules or conditions.','files':hashes,'results':rows}
target=ROOT/'evidence/baseline/new-user-identity-baseline-results.json' if '--identity-baseline' in sys.argv else OUT/'new-user-journey-results.json'
target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
