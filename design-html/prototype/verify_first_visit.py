from pathlib import Path
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
BASE='http://127.0.0.1:8765/'
OUT=Path(__file__).resolve().parent/('evidence/baseline' if '--baseline' in sys.argv else 'evidence/current')
CONTENT=['records','moments','anniversaries','capsules','works','books']
def fresh(p):
 p.goto(BASE+'prototype/review.html');p.evaluate('localStorage.clear();sessionStorage.clear()')
def no_content(p):
 values=p.evaluate("keys=>Object.fromEntries(keys.map(k=>[k,JSON.parse(localStorage.getItem('dujia-prototype-'+k)||'[]')]))",CONTENT)
 assert all(isinstance(v,list) and not v for v in values.values()),values
def visit(p,page,target):
 fresh(p);p.goto(BASE+'pages/'+page+'.html');p.wait_for_timeout(900);assert p.url.split('?')[0].endswith(target+'.html'),p.url;no_content(p)
def create_only_one(p):
 fresh(p);p.goto(BASE+'pages/m03-p01.html');p.locator('.choice.diary').click();p.wait_for_url('**/m03-p05.html');no_content(p);p.locator('[name=title]').fill('第一篇真实记录');p.locator('[name=body]').fill('自己写下的第一篇内容');p.locator('#diary .submit').click();p.wait_for_url('**/m03-p06.html');values=p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-records'))");assert len(values)==1 and values[0]['title']=='第一篇真实记录',values;p.goto(BASE+'pages/m03-p02.html');expect(p.locator('.prototype-home-record')).to_have_count(1)
def preserve(p):
 fresh(p);fixture=data(True);p.evaluate("data=>{for(const[k,v]of Object.entries(data))localStorage.setItem(k,JSON.stringify(v));}",fixture)
 for page in ['m03-p06','m03-p10','m04-p01','m04-p07']:
  p.goto(BASE+'pages/'+page+'.html');p.wait_for_timeout(650)
  for key in ['records','moments','anniversaries']:
   assert p.evaluate("k=>JSON.parse(localStorage.getItem(k))",'dujia-prototype-'+key)==fixture['dujia-prototype-'+key]
def pending(p,origin):
 fresh(p);fixture=data(True);fixture['dujia-prototype-pet']['status']='pending';fixture['dujia-prototype-pet']['requestedBy']='小满';p.evaluate("data=>{for(const[k,v]of Object.entries(data))localStorage.setItem(k,JSON.stringify(v));}",fixture)
 p.goto(BASE+'pages/'+origin+'.html');p.goto(BASE+'pages/m07-p01.html');p.locator('.pet-back,.back').first.click();p.wait_for_url('**/m03-p02.html');assert p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-pet')).status")=='pending'
def pending_after_adopt(p):
 fresh(p);p.evaluate("localStorage.setItem('dujia-prototype-relationship',JSON.stringify({bound:true,partner:'阿舟'}))");p.goto(BASE+'pages/m07-p04.html');p.locator('.adopt').click();p.wait_for_url('**/m07-p02.html');p.locator('#pet-name').fill('星星');p.locator('#invite').click();p.wait_for_url('**/m07-p01.html');p.locator('.pet-back,.back').first.click();p.wait_for_url('**/m03-p01.html');assert p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-pet')).status")=='pending';no_content(p)
cases={}
for page,target in [('m03-p02','m03-p01'),('m03-p05','m03-p05'),('m03-p06','m03-p06'),('m03-p10','m03-p09'),('m04-p01','m04-p02'),('m04-p07','m04-p08'),('m04-p05','m04-p06'),('m04-p12','m04-p12'),('m05-p09','m05-p09'),('m06-p04','m06-p04'),('m07-p03','m07-p04'),('m08-p01','m08-p02')]:
 cases['fresh-'+page]=lambda p,page=page,target=target:visit(p,page,target)
cases.update({'first-diary-no-fabricated-content':create_only_one,'existing-content-unchanged':preserve,'pending-top-back-direct':lambda p:pending(p,'m03-p02'),'pending-top-back-form-origin':lambda p:pending(p,'m07-p02')})
cases['pending-after-real-adoption-top-back']=pending_after_adopt
if '--pending-extra-only' in sys.argv:cases={'pending-after-real-adoption-top-back':pending_after_adopt}
rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in cases.items():
  c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row=dict(case=name,passed=True)
  except Exception:row=dict(case=name,passed=False,failure=traceback.format_exc()[-1600:])
  row.update(errors=errors,url=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 b.close()
(OUT/('first-pending-extra-results.json' if '--pending-extra-only' in sys.argv else 'first-visit-results.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
