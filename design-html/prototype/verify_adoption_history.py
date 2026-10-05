from pathlib import Path
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
BASE='http://127.0.0.1:8765/'
OUT=Path(__file__).resolve().parent/('evidence/baseline' if '--baseline' in sys.argv else 'evidence/current')
def begin(p):
 p.goto(BASE+'prototype/review.html');p.evaluate("localStorage.clear();sessionStorage.clear();localStorage.setItem('dujia-prototype-relationship',JSON.stringify({bound:true,partner:'阿舟'}))");p.goto(BASE+'pages/m07-p04.html');p.locator('.adopt').click();p.wait_for_url('**/m07-p02.html');p.locator('#pet-name').fill('星星');p.locator('#invite').click();p.wait_for_url('**/m07-p01.html');return p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-pet'))")
def unchanged(p,before):assert p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-pet'))")==before
def system_back(p):
 before=begin(p);p.go_back();p.wait_for_url('**/m03-p01.html');unchanged(p,before)
def repeated_back(p):
 before=begin(p)
 for _ in range(3):p.go_back();p.wait_for_url('**/m03-p01.html');p.wait_for_timeout(500);unchanged(p,before)
def top_then_back(p):
 before=begin(p);p.locator('.pet-back,.back').first.click();p.wait_for_url('**/m03-p01.html');p.go_back();p.wait_for_url('**/m03-p01.html');unchanged(p,before)
def unsaved(p):
 p.goto(BASE+'prototype/review.html');p.evaluate("localStorage.clear();sessionStorage.clear();localStorage.setItem('dujia-prototype-relationship',JSON.stringify({bound:true,partner:'阿舟'}))");p.goto(BASE+'pages/m07-p04.html');p.locator('.adopt').click();p.wait_for_url('**/m07-p02.html');p.locator('#pet-name').fill('还没有提交');p.go_back();expect(p.locator('dialog[open]')).to_be_visible();p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('dialog[open]')).to_have_count(0);p.wait_for_function('history.state?.prototypeGuard && !history.state?.prototypeOverlay');expect(p.locator('#pet-name')).to_have_value('还没有提交');p.go_back();p.get_by_role('button',name='放弃修改',exact=True).click();p.wait_for_url('**/m07-p04.html');assert p.evaluate("localStorage.getItem('dujia-prototype-pet')") is None
def direct_pending(p):
 before=begin(p);p.goto(BASE+'pages/m07-p02.html');p.wait_for_url('**/m07-p01.html');unchanged(p,before)
cases={'pending-browser-back-home':system_back,'pending-repeated-back-stale-form-and-start':repeated_back,'pending-top-back-then-browser-back':top_then_back}
if '--baseline' not in sys.argv:cases.update({'unsaved-browser-back-keeps-or-discards':unsaved,'direct-pending-form-still-routes-to-waiting':direct_pending})
def main():
 rows=[]
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for name,run in cases.items():
   c=b.new_context(viewport={'width':390,'height':844});p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
   try:run(p);assert not errors,errors;row=dict(case=name,passed=True)
   except Exception:row=dict(case=name,passed=False,failure=traceback.format_exc()[-1600:])
   row.update(errors=errors,url=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True);c.close()
  b.close()
 (OUT/'adoption-history-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 raise SystemExit(0 if all(v['passed'] for v in rows) else 1)
if __name__=='__main__':main()
