"""Three time collections: preserve originals, cancel, download and explicitly recover."""
import json,sys,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from verify_pet_controls import ROOT,BASE,source
OUT=ROOT/('evidence/baseline'if '--baseline'in sys.argv else'evidence/current');files=source();rows=[]
KINDS={'moments':('时刻',['m04-p01.html','m04-p16.html']),'anniversaries':('纪念日',['m04-p07.html','m04-p05.html']),'capsules':('胶囊',['m04-p12.html','m04-p05.html'])}
def key(kind):return 'dujia-prototype-'+kind
def prefix(kind):return 'dujia-prototype-'+kind+'-recovery-'
def seed(p,kind,value,page):
 d=data(True);d['dujia-prototype-session']=dict(loggedIn=True,phone='13812345678');d['dujia-prototype-preferences']=dict(autoBackup=False,reduceMotion=True)
 p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v));}',d);p.evaluate('([k,r])=>localStorage.setItem(k,r)',[key(kind),value]);p.goto(BASE+'pages/'+page)
def raw(p,kind):return p.evaluate('k=>localStorage.getItem(k)',key(kind))
def archives(p,kind):return p.evaluate('pre=>Object.keys(localStorage).filter(k=>k.startsWith(pre)).map(k=>JSON.parse(localStorage.getItem(k)))',prefix(kind))
def prompt(p,kind):expect(p.get_by_role('dialog',name=KINDS[kind][0]+'需要恢复',exact=True)).to_be_visible()
def repair(p,kind):
 name=KINDS[kind][0];p.get_by_role('button',name='恢复可读'+name,exact=True).click();expect(p.get_by_role('dialog',name='保留原始副本并恢复'+name+'？',exact=True)).to_be_visible();expect(p.get_by_role('button',name='取消',exact=True)).to_be_focused();p.get_by_role('button',name='确认恢复',exact=True).click()
def damage(p,kind,value,page):
 seed(p,kind,value,page);assert raw(p,kind)==value;prompt(p,kind);assert not archives(p,kind);name=KINDS[kind][0]
 p.get_by_role('button',name='恢复可读'+name,exact=True).click();p.get_by_role('button',name='取消',exact=True).click();prompt(p,kind);assert raw(p,kind)==value
 with p.expect_download()as download:p.get_by_role('button',name='导出原始'+name,exact=True).click()
 assert Path(download.value.path()).read_text(encoding='utf-8')==value
 with p.expect_event('load'):repair(p,kind)
 assert archives(p,kind)==[value];assert not p.evaluate('k=>PrototypeUI.collectionHealth(k).issues.length',key(kind));expect(p.locator('dialog')).to_have_count(0)
def main():
 with sync_playwright()as pw:
  b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for kind,(name,pages)in KINDS.items():
   item=data(True)[key(kind)][0];field='story'if kind=='moments'else'repeat'if kind=='anniversaries'else'message'
   variants={'broken-json':'{'+name+'原文','wrong-root':'{}','null-item':json.dumps([item,None],ensure_ascii=False),'duplicate-id':json.dumps([item,item],ensure_ascii=False),'invalid-field':json.dumps([{**item,field:{}}],ensure_ascii=False),'missing-id':json.dumps([{**item,'id':''}],ensure_ascii=False)}
   for case,value in variants.items():
    for page in pages:
     c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',accept_downloads=True);p=c.new_page();p.set_default_timeout(1200 if '--baseline'in sys.argv else 4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
     try:damage(p,kind,value,page);assert not errors;row=dict(passed=True)
     except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1600:])
     row.update(kind=kind,case=case,page=page,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+kind+' '+case+' '+page,flush=True);c.close()
  b.close()
 assert source()==files;(OUT/'time-collection-recovery-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
if __name__=='__main__':main()
