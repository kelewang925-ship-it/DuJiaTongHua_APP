"""A slow editor load must not allow the generation timer to navigate a second time."""
import json,sys,time,traceback
from playwright.sync_api import sync_playwright,expect
from verify_workshop_states import cancel,seed,go
from verify_pet_controls import ROOT,source
OUT=ROOT/('evidence/baseline'if '--baseline'in sys.argv else'evidence/current');files=source();requests=[];errors=[]
def failed_cancel(p,continue_work=False):
 seed(p,'generating',duration=30000);go(p,'m05-p06','?id=state-work');p.get_by_role('button',name='取消生成',exact=True).click();p.evaluate('()=>{const k="dujia-prototype-works",v=JSON.parse(localStorage.getItem(k));v[0].dueAt=Date.now()-1;localStorage.setItem(k,JSON.stringify(v));window.originalWorkSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k==="dujia-prototype-works")throw new DOMException("full","QuotaExceededError");return originalWorkSet.call(this,k,v);};}');p.get_by_role('button',name='保留草稿并取消',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('未能保存');p.evaluate('()=>{Storage.prototype.setItem=originalWorkSet;}');p.wait_for_timeout(750);assert '/m05-p06.html'in p.url;assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-works"))[0].status')=='generating';p.get_by_role('button',name='取消生成',exact=True).click();p.get_by_role('button',name='继续生成'if continue_work else'保留草稿并取消',exact=True).click()
 if continue_work:p.wait_for_url('**/m05-p08.html?id=state-work');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-works"))[0].status')=='ready'
 else:p.wait_for_url('**/m05-p03.html?id=state-work');expect(p.locator('#story')).to_have_value('我们一起看星星。我们一起许愿。');assert p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-works"))[0].status')=='draft'
rows=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name in ['slow-editor-single-navigation','cancel-save-failure-retry','cancel-save-failure-continue']:
  c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(6000);requests=[];errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:requests.append(dict(url=r.url,kind=r.resource_type,at=time.time()))if r.resource_type=='document'else None)
  def slow(route):time.sleep(.7);route.continue_()
  try:
   if name=='slow-editor-single-navigation':p.route('**/pages/m05-p03.html?id=state-work',slow);cancel(p);editors=[r for r in requests if'/m05-p03.html?id=state-work'in r['url']];assert len(editors)==1,editors
   else:failed_cancel(p,name.endswith('continue'))
   assert not errors;row=dict(passed=True)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-2400:])
  row.update(case=name,requests=requests,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+name,flush=True);c.close()
 b.close()
assert files==source();(OUT/'work-cancel-navigation-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
