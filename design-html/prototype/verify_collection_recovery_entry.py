"""One keyboard-reachable recovery entry per damaged collection, without hiding another root."""
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from verify_pet_controls import ROOT,BASE,source
from audit_current_runtime import data
files=source();rows=[];out=ROOT/('evidence/baseline'if '--baseline'in sys.argv else'evidence/current');out.mkdir(parents=True,exist_ok=True)
def seed(p,k,page):
 d=data(True);d['dujia-prototype-session']={'loggedIn':True};d['dujia-prototype-preferences']={'reduceMotion':True,'autoBackup':False};p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',d);p.evaluate('k=>localStorage.setItem("dujia-prototype-"+k,"{broken")',k);p.goto(BASE+'pages/'+page);expect(p.locator('dialog')).to_be_visible();p.get_by_role('button',name='稍后处理',exact=True).click()
def entry(p,k,name,page,w):
 seed(p,k,page);button=p.get_by_role('button',name='恢复'+name,exact=True);expect(button).to_have_count(1);button.scroll_into_view_if_needed();button.focus();p.keyboard.press('Enter');expect(p.get_by_role('dialog',name=name+'需要恢复',exact=True)).to_be_visible();p.keyboard.press('Escape');expect(button).to_be_focused();assert p.evaluate('document.documentElement.scrollWidth<=innerWidth');p.screenshot(path=str(out/f'recovery-entry-{k}-{w}.png'),full_page=True)
def multiple(p):
 seed(p,'books','m08-p16.html?id=book-state');p.evaluate('localStorage.setItem("dujia-prototype-pet","{broken");PrototypeUI.read("dujia-prototype-pet")');expect(p.get_by_role('dialog',name='宠物需要恢复',exact=True)).to_be_visible();p.get_by_role('button',name='稍后处理',exact=True).click();expect(p.get_by_role('button',name='恢复宠物',exact=True)).to_have_count(1);expect(p.get_by_role('button',name='恢复回忆册',exact=True)).to_have_count(1);p.get_by_role('button',name='恢复宠物',exact=True).click();expect(p.get_by_role('dialog',name='宠物需要恢复',exact=True)).to_be_visible()
def external(p):
 seed(p,'books','m08-p16.html?id=book-state');p.evaluate('localStorage.setItem("dujia-prototype-books","[]")');p.get_by_role('button',name='恢复回忆册',exact=True).click();p.wait_for_load_state('load');expect(p.get_by_role('button',name='返回书架',exact=True)).to_be_visible();expect(p.get_by_role('button',name='恢复回忆册',exact=True)).to_have_count(0)
cases={}
for k,name,page in [('pet','宠物','m07-p25.html'),('books','回忆册','m08-p16.html?id=book-state')]:
 for w in [320,360,390,414,430]:cases[k+'-'+str(w)]=(w,lambda p,k=k,name=name,page=page,w=w:entry(p,k,name,page,w))
for k,name,page in [('moments','时刻','m04-p03.html?id=missing'),('anniversaries','纪念日','m04-p10.html?id=missing'),('capsules','胶囊','m04-p15.html?id=missing')]:cases[k]=(390,lambda p,k=k,name=name,page=page:entry(p,k,name,page,390))
cases['multiple-damaged-roots']=(390,multiple);cases['external-repair-reloads-empty']=(390,external)
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,(w,run)in cases.items():
  c=b.new_context(viewport=dict(width=w,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row=dict(passed=True)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1600:])
  row.update(case=name,errors=errors);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+name,flush=True);c.close()
 b.close()
assert source()==files;(out/'collection-recovery-entry-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']and not r['errors']for r in rows)else 1)
