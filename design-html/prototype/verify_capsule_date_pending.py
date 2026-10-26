"""A pending date save must respect closing/discard and keep-editing decisions."""
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from verify_pet_controls import ROOT,BASE,source
files=source();out=ROOT/('evidence/baseline'if '--baseline'in sys.argv else'evidence/current');rows=[];out.mkdir(parents=True,exist_ok=True)
def seed(p):
 d=data(True);d['dujia-prototype-session']={'loggedIn':True};d['dujia-prototype-preferences']={'autoBackup':False,'reduceMotion':True}
 for k in ['moments','anniversaries','works','books']:d['dujia-prototype-'+k]=[]
 d['dujia-prototype-capsules']=[dict(id='pending-date',name='等待中的信',message='SEALED-PENDING',opening='2026-02-30',status='sealed',reminder=True)]
 p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-06");for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',d);p.goto(BASE+'pages/m04-p15.html?id=pending-date');p.get_by_role('button',name='修正开启日期',exact=True).click();field=p.get_by_label('新的开启日期',exact=True);field.fill('2026-10-08');return field

def value(p):return p.evaluate('localStorage.getItem("dujia-prototype-capsules")')
def close(p,keep=False):
 field=seed(p);before=value(p);p.get_by_role('button',name='保存开启日期',exact=True).click();p.keyboard.press('Escape');expect(p.locator('.prototype-sheet-discard')).to_be_visible();p.wait_for_timeout(850);assert value(p)==before,'Pending write happened while close decision was unresolved';expect(p.locator('.prototype-sheet-discard')).to_be_visible();p.get_by_role('button',name='继续编辑'if keep else'放弃修改',exact=True).click()
 if keep:
  expect(field).to_have_value('2026-10-08');expect(field).to_be_enabled();expect(p.get_by_role('button',name='保存开启日期',exact=True)).to_be_enabled();assert value(p)==before;p.get_by_role('button',name='保存开启日期',exact=True).click();expect(p.locator('dialog')).to_have_count(0);expect(p.locator('.countdown')).to_contain_text('2');assert json.loads(value(p))[0]['opening']=='2026-10-08'
 else:expect(p.locator('dialog')).to_have_count(0);p.wait_for_timeout(750);assert value(p)==before;expect(p.get_by_role('button',name='修正开启日期',exact=True)).to_be_focused()
def locked(p):
 field=seed(p);p.get_by_role('button',name='保存开启日期',exact=True).click();expect(field).to_be_disabled();expect(p.locator('dialog')).to_have_count(0);expect(p.locator('.countdown')).to_contain_text('2')
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'pending-close-discard-no-write':close,'pending-close-continue-then-save':lambda p:close(p,True),'pending-input-locked':locked}.items():
  c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row=dict(passed=True)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1700:])
  row.update(case=name,errors=errors);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+name,flush=True);c.close()
 b.close()
assert source()==files;(out/'capsule-date-pending-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
