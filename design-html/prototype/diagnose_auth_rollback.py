import json,hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from verify_auth_submit_context import seed,release
from verify_pet_controls import ROOT,source
def state(p):return p.evaluate("({local:JSON.stringify({...localStorage}),session:JSON.stringify({...sessionStorage})})")
rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for kind in ['register-direct','register-verify']:
  c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();selector=seed(p,kind);p.evaluate("()=>{const set=Storage.prototype.setItem;window.__authQuota=0;Storage.prototype.setItem=function(k,v){if(this===localStorage&&k==='dujia-prototype-moments'&&!window.__authQuota++)throw new DOMException('Injected quota failure','QuotaExceededError');return set.call(this,k,v)}}");p.locator(selector).click();before=state(p);release(p);expect(p.locator(selector)).to_be_enabled();after=state(p);parsed=lambda v:{k:json.loads(vv) for k,vv in v.items()};a,before_parsed=parsed(after),parsed(before);rows.append(dict(kind=kind,before=before,after=after,values_equal=a==before_parsed,changed_keys={scope:[k for k in set(a[scope])|set(before_parsed[scope]) if a[scope].get(k)!=before_parsed[scope].get(k)] for scope in a}));c.close()
 b.close()
out=ROOT/'evidence/history/auth-registration-rollback-diagnostic';out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(dict(files=source(),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps([{k:v for k,v in r.items() if k not in ['before','after']} for r in rows]))
