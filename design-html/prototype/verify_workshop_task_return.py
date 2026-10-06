"""Generated result exits completed task history; data is created through UI."""
import json,traceback,sys
from playwright.sync_api import sync_playwright,expect
from verify_pet_controls import source,ROOT,BASE,store
OUT=ROOT/('evidence/baseline' if '--baseline' in sys.argv else 'evidence/current');files=source();rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for retry in [False,True]:
  for mode in ['button','browser']:
   c=b.new_context(viewport=dict(width=390,height=844));p=c.new_page();p.set_default_timeout(5000);p.set_default_navigation_timeout(10000);errors=[];navigations=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('framenavigated',lambda f:navigations.append(f.url) if f==p.main_frame else None)
   try:
    p.goto(BASE+'pages/m05-p01.html');p.locator('.start').click();p.wait_for_url('**/m05-p02.html');p.get_by_role('button',name='自由写一段回忆',exact=True).click();p.locator('#go').click();p.wait_for_url('**/m05-p03.html*');p.locator('#story').fill('原样保留的完成作品')
    if retry:p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","work-generate")')
    p.locator('#generate').click()
    if retry:p.wait_for_url('**/m05-p07.html*');p.get_by_role('button',name='重新生成',exact=True).click()
    p.wait_for_url('**/m05-p08.html*');before=store(p)
    if mode=='button':p.locator('.back').click();p.wait_for_url('**/m05-p09.html');p.locator('.prototype-work-back').click();p.wait_for_url('**/m05-p01.html')
    else:p.go_back();p.wait_for_url('**/m05-p09.html');p.go_back();p.wait_for_url('**/m05-p01.html')
    assert store(p)==before;assert not errors;row=dict(passed=True)
   except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1600:])
   row.update(case=('retry-' if retry else 'success-')+mode,errors=errors,effective=p.url,navigations=navigations);rows.append(row);print(('PASS ' if row['passed'] else 'FAIL ')+row['case'],flush=True);c.close()
 b.close()
assert files==source();(OUT/'workshop-task-return-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(v['passed']for v in rows)else 1)
