"""Tag damage preservation and explicit recovery through real browser controls."""
import json,sys,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from verify_pet_controls import ROOT,BASE,source
OUT=ROOT/('evidence/baseline' if '--baseline' in sys.argv else 'evidence/current');files=source();rows=[]
KEY='dujia-prototype-tags';PREFIX='dujia-prototype-tag-recovery-';TAG=dict(id='kept-tag',name='保留标签',scope='shared')
def seed(p,value,page='m06-p05.html'):
 d=data(True);d['dujia-prototype-session']=dict(loggedIn=True,phone='13812345678');d['dujia-prototype-preferences']=dict(autoBackup=False,reduceMotion=True)
 p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v));}',d)
 p.evaluate('([k,r])=>{if(r===null)localStorage.removeItem(k);else localStorage.setItem(k,r);}',[KEY,value]);p.goto(BASE+'pages/'+page)
def raw(p):return p.evaluate('k=>localStorage.getItem(k)',KEY)
def archives(p):return p.evaluate('pre=>Object.keys(localStorage).filter(k=>k.startsWith(pre)).map(k=>JSON.parse(localStorage.getItem(k)))',PREFIX)
def prompt(p):expect(p.get_by_role('dialog',name='标签需要恢复',exact=True)).to_be_visible()
def repair(p):
 p.get_by_role('button',name='恢复可读标签',exact=True).click();expect(p.get_by_role('dialog',name='保留原始副本并恢复标签？',exact=True)).to_be_visible();expect(p.get_by_role('button',name='取消',exact=True)).to_be_focused()
 button=p.get_by_role('button',name='确认恢复',exact=True);assert button.evaluate('b=>b.dataset.variant==="danger"&&b.dataset.danger==="true"&&b.getBoundingClientRect().height>=44');button.click()
def damage(p,value,page):
 seed(p,value,page);p.wait_for_timeout(350);assert raw(p)==value,'opening page changed original';prompt(p);assert not archives(p)
 p.get_by_role('button',name='恢复可读标签',exact=True).click();p.get_by_role('button',name='取消',exact=True).click();prompt(p);assert raw(p)==value
 with p.expect_download()as download:p.get_by_role('button',name='导出原始标签',exact=True).click()
 assert Path(download.value.path()).read_text(encoding='utf-8')==value;prompt(p)
 with p.expect_event('load'):repair(p)
 expect(p.locator('dialog')).to_have_count(0);assert archives(p)==[value];assert isinstance(json.loads(raw(p)),list)
 assert not p.evaluate('PrototypePreferences.tagHealth().issues.length')
variants={'broken-json':'{标签原文','wrong-root':'{}','null-item':json.dumps([TAG,None],ensure_ascii=False),'duplicate-id':json.dumps([TAG,TAG],ensure_ascii=False),'invalid-name':json.dumps([TAG,dict(id='bad',name={},scope='personal')],ensure_ascii=False),'invalid-scope':json.dumps([{**TAG,'scope':None}],ensure_ascii=False),'duplicate-name':json.dumps([TAG,{**TAG,'id':'other'}],ensure_ascii=False),'missing-id':json.dumps([{**TAG,'id':''}],ensure_ascii=False)}
def main():
 with sync_playwright()as pw:
  b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for case,value in variants.items():
   for page in ['m06-p05.html','m06-p11.html']:
    c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',accept_downloads=True);p=c.new_page();p.set_default_timeout(3000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
    try:damage(p,value,page);assert not errors;row=dict(passed=True)
    except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1800:])
    row.update(case=case,page=page,errors=errors,effective=p.url,original_after=raw(p));rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+case+' '+page,flush=True);c.close()
  b.close()
 assert files==source();(OUT/'tag-recovery-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
if __name__=='__main__':main()
