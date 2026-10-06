"""Actual work collection damage: original preservation and explicit recovery contracts."""
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from verify_pet_controls import ROOT,BASE,source,store
OUT=ROOT/('evidence/baseline'if '--baseline'in sys.argv else'evidence/current');files=source();rows=[];KEY='dujia-prototype-works';PREFIX='dujia-prototype-work-recovery-'
def seed(p,raw,page='m05-p09.html'):
 d=data(True);d['dujia-prototype-session']=dict(loggedIn=True,phone='13812345678');d['dujia-prototype-preferences']=dict(autoBackup=False,reduceMotion=True)
 p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v));}',d);p.evaluate('([k,r])=>localStorage.setItem(k,r)',[KEY,raw]);p.goto(BASE+'pages/'+page)
def raw(p):return p.evaluate('(k)=>localStorage.getItem(k)',KEY)
def archives(p):return p.evaluate('(prefix)=>Object.keys(localStorage).filter(k=>k.startsWith(prefix)).map(k=>JSON.parse(localStorage.getItem(k)))',PREFIX)
def prompt(p):expect(p.get_by_role('dialog',name='作品需要恢复',exact=True)).to_be_visible()
def repair(p):
 p.get_by_role('button',name='恢复可读作品',exact=True).click();expect(p.get_by_role('dialog',name='保留原始副本并恢复作品？',exact=True)).to_be_visible();expect(p.get_by_role('button',name='取消',exact=True)).to_be_focused();button=p.get_by_role('button',name='确认恢复',exact=True);assert button.evaluate('b=>b.dataset.variant==="danger"&&b.dataset.danger==="true"&&b.classList.contains("prototype-component-button")&&b.getBoundingClientRect().height>=44');button.click()
def damaged(p,value,page):
 seed(p,value,page);prompt(p);assert raw(p)==value;assert not archives(p)
 p.get_by_role('button',name='恢复可读作品',exact=True).click();p.get_by_role('button',name='取消',exact=True).click();prompt(p);assert raw(p)==value
 with p.expect_download()as download:p.get_by_role('button',name='导出原始作品',exact=True).click()
 from pathlib import Path
 assert Path(download.value.path()).read_text(encoding='utf-8')==value;prompt(p)
 with p.expect_event('load'):repair(p)
 expect(p.locator('dialog')).to_have_count(0);assert archives(p)==[value];assert isinstance(json.loads(raw(p)),list)
work=data(True)[KEY][0];variants={'broken-json':'{broken','wrong-root':'{}','null-item':json.dumps([work,None],ensure_ascii=False),'duplicate-id':json.dumps([work,work],ensure_ascii=False),'nested-source':json.dumps([{**work,'sourceIds':[None,{},'kept-source']}],ensure_ascii=False),'invalid-story':json.dumps([{**work,'story':{}}],ensure_ascii=False)}
def main():
 with sync_playwright()as pw:
  b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for case,value in variants.items():
   for page in ['m05-p01.html','m05-p09.html','m05-p08.html?id=audit-work']:
    c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',accept_downloads=True);p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
    try:damaged(p,value,page);assert not errors;row=dict(passed=True)
    except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1600:])
    row.update(case=case,page=page,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+case+' '+page,flush=True);c.close()
  b.close()
 assert files==source();(OUT/'workshop-recovery-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)

if __name__=="__main__":main()
