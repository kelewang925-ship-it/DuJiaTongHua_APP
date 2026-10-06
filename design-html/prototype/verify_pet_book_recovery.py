"""Real choices/download/confirmation for both remaining structured roots."""
import json,sys,traceback,copy
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from verify_pet_controls import ROOT,BASE,source
files=source();rows=[];out=ROOT/'evidence'/('baseline'if '--baseline'in sys.argv else'current')
base=data(True);base['dujia-prototype-session']=dict(loggedIn=True,phone='13812345678');base['dujia-prototype-preferences']=dict(reduceMotion=True,autoBackup=False)
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for kind,name,pages in [('pet','宠物',['m07-p03.html','m06-p11.html']),('books','回忆册',['m08-p01.html','m06-p11.html'])]:
  original=copy.deepcopy(base['dujia-prototype-'+kind]);child=copy.deepcopy(original)
  if kind=='pet':
   child['logs']+=[None];duplicate=copy.deepcopy(original);duplicate['logs']*=2;field=copy.deepcopy(original);field['food']={};missing=copy.deepcopy(original);missing.pop('id')
  else:
   child+=[None];duplicate=original*2;field=copy.deepcopy(original);field[0]['pages']={};missing=copy.deepcopy(original);missing[0].pop('id')
  variants={'broken-json':'{broken','wrong-root':'{"pet":{"id":"previous-pet"}}'if kind=='pet'else'{}','null-child':json.dumps(child,ensure_ascii=False),'duplicate-id':json.dumps(duplicate,ensure_ascii=False),'nested-field':json.dumps(field,ensure_ascii=False),'missing-id':json.dumps(missing,ensure_ascii=False)}
  for variant,raw in variants.items():
   for page in pages:
    c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',accept_downloads=True);p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));key='dujia-prototype-'+kind
    try:
     p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',base);p.evaluate('([k,v])=>localStorage.setItem(k,v)',[key,raw]);p.goto(BASE+'pages/'+page);expect(p.get_by_role('dialog',name=name+'需要恢复',exact=True)).to_be_visible();p.get_by_role('button',name='稍后处理',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert p.evaluate('(k)=>localStorage.getItem(k)',key)==raw
     assert p.evaluate('([k,v])=>PrototypeUI.write(k,v)',[key,None if kind=='pet'else[]])is False
     p.get_by_role('button',name='恢复'+name,exact=True).first.click()
     with p.expect_download()as dl:p.get_by_role('button',name='导出原始'+name,exact=True).click()
     assert Path(dl.value.path()).read_text(encoding='utf-8')==raw
     p.get_by_role('button',name='恢复可读'+name,exact=True).click();expect(p.get_by_role('dialog',name='保留原始副本并恢复'+name+'？',exact=True)).to_be_visible();assert p.evaluate('(k)=>localStorage.getItem(k)',key)==raw;
     with p.expect_request_finished(lambda r:r.resource_type=='document'and r.url==BASE+'pages/'+page):p.get_by_role('button',name='确认恢复',exact=True).click()
     if kind=='pet'and page=='m07-p03.html'and variant in ['broken-json','wrong-root','missing-id']:
      p.wait_for_url('**/m07-p04.html');expect(p.get_by_role('button',name='一起领养',exact=True)).to_be_visible()
     p.wait_for_load_state('load');p.wait_for_function('typeof PrototypeUI!=="undefined"');p.wait_for_function('(k)=>Object.keys(localStorage).some(v=>v.startsWith(k+"-recovery-"))',arg=key)
     expect(p.locator('dialog')).to_have_count(0);assert p.evaluate('(k)=>localStorage.getItem(k)',key)!=raw;assert not p.evaluate('(k)=>PrototypeUI.collectionHealth(k).issues',key);copies=p.evaluate('(k)=>Object.keys(localStorage).filter(v=>v.startsWith(k+"-recovery-")).map(v=>JSON.parse(localStorage.getItem(v)))',key);assert raw in copies
     row=dict(passed=True,original_downloaded=True,copy_retained=True)
    except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1600:])
    row.update(case=kind+'-'+variant+'-'+page,errors=errors);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+row['case'],flush=True);c.close()
 b.close()
assert source()==files;out.mkdir(parents=True,exist_ok=True);(out/'pet-book-recovery-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(r['passed']and not r['errors']for r in rows)else 1)
