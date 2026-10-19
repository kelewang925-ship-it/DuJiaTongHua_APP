"""Search, capsule and generation failure boundaries using isolated local fixtures."""
import json
import traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
OUT=Path(__file__).resolve().parent/'evidence/current';BASE='http://127.0.0.1:8765/'

def go(p,name,query=''):p.goto(BASE+'pages/'+name+'.html'+query)
def seed(p):
    p.goto(BASE+'prototype/review.html')
    p.evaluate("d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem('dujia-prototype-today','2026-10-05');for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}",data(True))
def state(p):return p.evaluate('JSON.stringify(Object.fromEntries(Object.entries(localStorage).sort()))')
def inject(p,op):p.evaluate("op=>{document.querySelectorAll('.prototype-toast').forEach(e=>e.remove());sessionStorage.setItem('dujia-prototype-fail-next',op)}",op)
def failed(p,op,action):
    before=state(p);inject(p,op);action();p.wait_for_function("op=>sessionStorage.getItem('dujia-prototype-fail-next')!==op",arg=op)
    expect(p.locator('.prototype-toast')).to_be_visible();assert state(p)==before

def search(p):
    seed(p);inject(p,'record-search');go(p,'m03-p04','?q=共同');expect(p.get_by_text('暂时无法查找，请再试一次',exact=True)).to_be_visible()
    before=state(p);p.get_by_role('button',name='重试搜索',exact=True).click();expect(p.locator('.prototype-search-results')).to_contain_text('共同日记');assert state(p)==before

def capsule_date(p):
    seed(p);p.evaluate("()=>{const rows=JSON.parse(localStorage.getItem('dujia-prototype-capsules'));rows.find(r=>r.id==='audit-sealed').opening='invalid';localStorage.setItem('dujia-prototype-capsules',JSON.stringify(rows))}")
    go(p,'m04-p15','?id=audit-sealed');p.get_by_role('button',name='修正开启日期',exact=True).click();field=p.get_by_label('新的开启日期',exact=True);field.fill('2026-12-25');button=p.get_by_role('button',name='保存开启日期',exact=True)
    failed(p,'capsule-date',button.click);expect(field).to_have_value('2026-12-25');button.click();expect(p.locator('dialog[open]')).to_have_count(0)
    item=p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-capsules')).find(r=>r.id==='audit-sealed')");assert item['opening']=='2026-12-25'and item['status']=='sealed'and item['message']=='仍然封存的内容'

def capsule_save(p):
    seed(p);p.evaluate("()=>{const rows=JSON.parse(localStorage.getItem('dujia-prototype-capsules'));rows[1].status='draft';localStorage.setItem('dujia-prototype-capsules',JSON.stringify(rows))}")
    go(p,'m04-p13','?id=audit-sealed');field=p.locator('[name=message]');field.fill('失败后仍封存的信件');button=p.get_by_role('button',name='封存这份心意',exact=True)
    failed(p,'capsule-save',button.click);expect(field).to_have_value('失败后仍封存的信件');button.click();p.wait_for_url('**/m04-p15.html?id=audit-sealed')
    assert p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-capsules')).find(r=>r.id==='audit-sealed').status")=='sealed'

def capsule_open(p):
    seed(p);p.evaluate("()=>{const rows=JSON.parse(localStorage.getItem('dujia-prototype-capsules'));rows[1].opening='2026-10-05';localStorage.setItem('dujia-prototype-capsules',JSON.stringify(rows))}")
    go(p,'m04-p15','?id=audit-sealed');button=p.get_by_role('button',name='打开这份心意',exact=True);failed(p,'capsule-open',button.click);expect(p.locator('.letter-body')).to_have_count(0)
    button.click();p.wait_for_url('**/m04-p14.html?id=audit-sealed');expect(p.locator('.letter-body')).to_have_text('仍然封存的内容')

def generation(p):
    seed(p);go(p,'m05-p03','?id=audit-work');p.locator('#story').fill('失败后重新生成的真实故事');inject(p,'work-generate');p.locator('#generate').click();p.wait_for_url('**/m05-p07.html*',timeout=10000)
    before=p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-works'))[0]");assert before['status']=='failed'and before['story']=='失败后重新生成的真实故事'
    p.get_by_role('button',name='重新生成',exact=True).click();p.wait_for_url('**/m05-p08.html*',timeout=10000)
    after=p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-works'))[0]");assert after['status']=='ready'and after['id']==before['id']and after['story']==before['story']

rows=[]
with sync_playwright()as pw:
    b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for name,run in {'search-failure-retry':search,'capsule-date-failure-retry-sealed':capsule_date,'capsule-save-failure-retains-input':capsule_save,'capsule-open-failure-keeps-secret':capsule_open,'generation-failure-retry-same-work':generation}.items():
        c=b.new_context(viewport=dict(width=390,height=844));p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
        try:run(p);assert not errors;row=dict(case=name,passed=True)
        except Exception:row=dict(case=name,passed=False,failure=traceback.format_exc()[-2300:])
        row.update(errors=errors,final_url=p.url);rows.append(row);(OUT/'last-failures-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(('PASS 'if row['passed']else'FAIL ')+name,flush=True);c.close()
    b.close()
raise SystemExit(0 if all(row['passed']for row in rows)else 1)
