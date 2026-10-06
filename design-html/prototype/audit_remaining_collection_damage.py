"""Readonly damage observations, not acceptance tests: other business collections."""
import json,traceback
from playwright.sync_api import sync_playwright
from audit_current_runtime import data
from verify_pet_controls import ROOT,BASE,source
files=source();rows=[];base=data(True)
cases={'moments':['m04-p01.html','m04-p16.html'],'anniversaries':['m04-p07.html','m04-p05.html'],'capsules':['m04-p12.html','m04-p05.html'],'books':['m08-p01.html','m08-p16.html?id=book-state&page=page-state'],'pet':['m07-p03.html','m07-p25.html'],'tags':['m06-p05.html','m06-p11.html']}
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for kind,pages in cases.items():
  key='dujia-prototype-'+kind;value=base.get(key,[]);variants={'broken-json':'{broken','wrong-root':'[]'if kind=='pet'else'{}','null-child':json.dumps({**value,'logs':[None]}if kind=='pet'else(value if isinstance(value,list)else[])+[None],ensure_ascii=False)}
  for variant,raw in variants.items():
   for page in pages:
    c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));failure=None
    try:
     p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v));}',base);p.evaluate('([k,v])=>localStorage.setItem(k,v)',[key,raw]);p.goto(BASE+'pages/'+page);p.wait_for_timeout(900);stored=p.evaluate('(k)=>localStorage.getItem(k)',key);text=p.locator('body').inner_text()[:2200];recovery=p.get_by_role('button',name='恢复',exact=False).all_text_contents();row=dict(raw_preserved=stored==raw,stored=stored,text=text,recovery_buttons=recovery)
    except Exception:row=dict(failure=traceback.format_exc()[-1800:])
    row.update(kind=kind,variant=variant,page=page,effective=p.url,errors=errors);rows.append(row);print('OBS '+kind+' '+variant+' '+page+' errors='+str(len(errors)),flush=True);c.close()
 b.close()
assert files==source();(ROOT/'evidence/current/remaining-collection-damage-observations.json').write_text(json.dumps(dict(files=files,scope='Read-only diagnostic observations; no actions executed and no acceptance claims',results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Observations',len(rows),'script errors',sum(len(r['errors'])for r in rows),'changed raw',sum(r.get('raw_preserved')is False for r in rows))
