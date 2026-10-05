from pathlib import Path
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from book_test_helpers import seed,records,BASE
OUT=Path(__file__).resolve().parent/('evidence/baseline' if '--baseline' in sys.argv else 'evidence/current')
def switch_all(p):
 seed(p,records=records());p.evaluate("localStorage.setItem('dujia-prototype-moments','[]')");p.goto(BASE+'pages/m03-p02.html');length=p.evaluate('history.length')
 for label,prefix in [('重要时刻','m04-p02'),('工坊','m05-p01'),('宠物','m07-p04'),('我的','m06-p01'),('首页','m03-p02')]:
  p.get_by_role('navigation',name='主导航',exact=True).get_by_role('button',name=label,exact=True).click();p.wait_for_url('**/'+prefix+'.html*');expect(p.get_by_role('navigation',name='主导航',exact=True).get_by_role('button',name=label,exact=True)).to_have_attribute('aria-current','page');assert p.evaluate('history.length')==length
def empty_and_details(p):
 seed(p);p.goto(BASE+'pages/m03-p01.html');p.get_by_role('navigation',name='主导航',exact=True).get_by_role('button',name='宠物',exact=True).click();p.wait_for_url('**/m07-p04.html*');expect(p.get_by_role('navigation',name='主导航',exact=True)).to_be_visible();p.goto(BASE+'pages/m03-p05.html');expect(p.get_by_role('navigation',name='主导航',exact=True)).to_have_count(0)
def missing_work_back(p):
 seed(p);p.goto(BASE+'pages/m05-p08.html');p.locator('.back[aria-label="返回我的创作"]').click();p.wait_for_url('**/m05-p09.html*')
rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for name,run in {'all-five-tabs-active-and-replace-history':switch_all,'first-empty-pet-entry-and-detail-navigation':empty_and_details,'missing-work-top-back-fallback':missing_work_back}.items():
  c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:run(p);assert not errors,errors;row=dict(case=name,passed=True)
  except Exception:row=dict(case=name,passed=False,failure=traceback.format_exc()[-2200:])
  row.update(errors=errors,url=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
 b.close()
OUT.mkdir(parents=True,exist_ok=True);(OUT/'primary-navigation-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(v['passed'] for v in rows) else 1)
