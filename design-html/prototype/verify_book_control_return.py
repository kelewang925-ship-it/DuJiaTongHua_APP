"""Supplement edit explicit return preserves chosen task context."""
import json,traceback,sys
from playwright.sync_api import sync_playwright,expect
from verify_book_controls import seed,source,store,OUT,ROOT
files=source();rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for dirty in [False,True]:
  c=b.new_context(viewport=dict(width=390,height=844));p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:
   seed(p,'m08-p19');before=store(p)
   if dirty:p.locator('.message').fill('未提交的补页')
   p.locator('.back').click()
   if dirty:
    expect(p.locator('dialog h2')).to_have_text('是否放弃当前修改？');p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('.message')).to_have_value('未提交的补页');p.locator('.back').click();p.get_by_role('button',name='放弃修改',exact=True).click()
   p.wait_for_url('**/m08-p18.html*');assert 'id=book-state' in p.url and 'page=page-second' in p.url;assert store(p)==before;assert not errors;row=dict(passed=True)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1300:])
  row.update(case='supplement-return-'+('dirty-discard' if dirty else 'clean'),errors=errors,effective=p.url);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+row['case'],flush=True);c.close()
 b.close()
assert files==source();out=ROOT/('evidence/baseline' if '--baseline' in sys.argv else 'evidence/current');(out/'book-control-return-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
