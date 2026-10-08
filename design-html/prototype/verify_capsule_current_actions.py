"""Actions must use current capsule dates/content, not the loaded page snapshot."""
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from verify_pet_controls import ROOT,BASE,source
files=source();rows=[];out=ROOT/('evidence/baseline'if '--baseline'in sys.argv else'evidence/current');out.mkdir(parents=True,exist_ok=True)
def seed(p):
 d=data(True);d['dujia-prototype-session']={'loggedIn':True};d['dujia-prototype-preferences']={'autoBackup':False,'reduceMotion':True};d['dujia-prototype-capsules']=[dict(id='current-cap',name='当前信件',message='ORIGINAL-SEALED',opening='2026-10-06',status='sealed',reminder=True)]
 for k in ['moments','anniversaries','works','books']:d['dujia-prototype-'+k]=[]
 p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-06");for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',d);p.goto(BASE+'pages/m04-p15.html?id=current-cap');expect(p.get_by_role('button',name='打开这份心意',exact=True)).to_be_visible()
def change(p,fields):p.evaluate('f=>{const v=JSON.parse(localStorage.getItem("dujia-prototype-capsules"));Object.assign(v[0],f);localStorage.setItem("dujia-prototype-capsules",JSON.stringify(v))}',fields)
def value(p):return p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-capsules"))[0]')
def gate(p,invalid=False):
 seed(p);change(p,dict(opening='2026-02-30'if invalid else'2026-10-08',message='PEER-SEALED'));before=value(p);p.get_by_role('button',name='打开这份心意',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('日期'if invalid else'约定');assert value(p)==before and 'PEER-SEALED'not in p.locator('body').inner_text();p.reload()
 if invalid:expect(p.get_by_role('button',name='修正开启日期',exact=True)).to_be_visible()
 else:expect(p.get_by_role('button',name='打开这份心意',exact=True)).to_have_count(0)
def peer(p,opened=False):
 seed(p);fields=dict(message='PEER-CONTENT',name='更新的标题')
 if opened:fields.update(status='opened',openedAt=1791244800000)
 change(p,fields);before=value(p);p.get_by_role('button',name='打开这份心意',exact=True).click();p.wait_for_url('**/m04-p14.html?id=current-cap');expect(p.locator('.letter-body')).to_have_text('PEER-CONTENT');actual=value(p)
 if opened:assert actual==before
 else:assert {k:v for k,v in actual.items()if k not in ['status','openedAt','updatedAt']}=={k:v for k,v in before.items()if k not in ['status','openedAt','updatedAt']}
def toggle(p):
 seed(p);change(p,dict(opening='2026-10-08',message='PEER-CONTENT'));before=value(p);p.locator('.reminder input').click();expect(p.locator('.reminder input')).not_to_be_checked();actual=value(p);assert actual=={**before,'reminder':False}
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'future-date-gates-stale-open':gate,'invalid-date-gates-stale-open':lambda p:gate(p,True),'open-current-peer-content':peer,'already-opened-no-second-write':lambda p:peer(p,True),'reminder-keeps-current-date-content':toggle}.items():
  c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row=dict(passed=True)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1500:])
  row.update(case=name,errors=errors);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+name,flush=True);c.close()
 b.close()
assert source()==files;(out/'capsule-current-action-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
