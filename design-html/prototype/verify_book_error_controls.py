from pathlib import Path
import json,traceback,sys
from playwright.sync_api import sync_playwright,expect
from book_test_helpers import seed,go,fixture,fail,value
OUT=Path(__file__).resolve().parent/('evidence/baseline' if '--baseline' in sys.argv else 'evidence/current')
row={}
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');c=b.new_context(viewport={'width':320,'height':844});p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 try:
  initial=fixture();seed(p,books=[initial]);fail(p,'book-load');go(p,5,'?id=book-state')
  for attempt in range(2):
   expect(p.locator('.prototype-component-state[role=alert]')).to_be_visible();expect(p.locator('.next')).to_be_disabled();assert value(p)==[initial];p.get_by_role('button',name='重新加载',exact=True).click();expect(p.locator('.book-load')).to_have_count(0);expect(p.locator('.next')).to_be_enabled()
   if attempt==0:fail(p,'book-load');p.reload()
  p.locator('.next').click();p.wait_for_url('**/m08-p06.html*');assert value(p)[0]['id']=='book-state';assert not errors,errors;row=dict(case='failed-load-disables-task-repeat-retry-restores-controls',passed=True)
 except Exception:row=dict(case='failed-load-disables-task-repeat-retry-restores-controls',passed=False,failure=traceback.format_exc()[-1900:])
 row.update(errors=errors,url=p.url);c.close();b.close()
(OUT/'book-error-control-results.json').write_text(json.dumps([row],ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print(('PASS ' if row['passed'] else 'FAIL ')+row['case'],flush=True)
raise SystemExit(0 if row['passed'] else 1)
