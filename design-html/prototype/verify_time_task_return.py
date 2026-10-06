"""Return paths after UI-created time tasks, plus the normal reminder entry."""
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from verify_pet_controls import ROOT,BASE,source,store
OUT=ROOT/('evidence/baseline'if '--baseline'in sys.argv else 'evidence/current');files=source();rows=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for case in ['anniversary-edited-button','anniversary-edited-browser','capsule-sealed-button','capsule-sealed-browser','capsule-draft-list-button','reminder-entry-empty']:
  c=b.new_context(viewport=dict(width=390,height=844));p=c.new_page();p.set_default_timeout(3500);errors=[];navigations=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('framenavigated',lambda f:navigations.append(f.url)if f==p.main_frame else None)
  try:
   if case.startswith('anniversary'):
    p.goto(BASE+'pages/m04-p08.html');p.locator('.add').click();p.wait_for_url('**/m04-p09.html');p.locator('[name=name]').fill('初次约定');p.locator('.submit').click();p.wait_for_url('**/m04-p07.html');p.locator('.entries').get_by_role('button',name='初次约定',exact=False).click();p.wait_for_url('**/m04-p11.html*');p.get_by_role('button',name='编辑纪念日',exact=True).click();p.wait_for_url('**/m04-p09.html*');p.locator('[name=name]').fill('更新后的约定');p.locator('.submit').click();p.wait_for_url('**/m04-p11.html*');before=store(p)
    if case.endswith('button'):p.get_by_role('button',name='返回纪念日列表',exact=True).click();p.wait_for_url('**/m04-p07.html')
    else:p.go_back();p.wait_for_url('**/m04-p11.html*');expect(p.locator('h1')).to_have_text('更新后的约定')
   elif case.startswith('capsule'):
    p.goto(BASE+'pages/m04-p12.html');p.locator('.new').click();p.wait_for_url('**/m04-p13.html');p.locator('[name=name]').fill('保存后的心意');p.locator('[name=message]').fill('这份信不能返回未完成的新建任务。')
    if case=='capsule-draft-list-button':p.get_by_role('button',name='暂存草稿',exact=True).click();p.wait_for_url('**/m04-p12.html');before=store(p);p.locator('.back').click();p.wait_for_url('**/m04-p02.html')
    else:
     p.get_by_role('button',name='封存这份心意',exact=True).click();p.wait_for_url('**/m04-p15.html*');before=store(p)
     if case.endswith('button'):p.locator('.back').click()
     else:p.go_back()
     p.wait_for_url('**/m04-p12.html')
   else:
    p.goto(BASE+'pages/m04-p02.html');before=store(p);p.get_by_role('button',name='共同提醒',exact=True).click();p.wait_for_url('**/m04-p06.html');expect(p.get_by_text('暂时没有新提醒',exact=True)).to_be_visible()
   assert store(p)==before;assert not errors;row=dict(passed=True)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-1700:])
  row.update(case=case,errors=errors,effective=p.url,navigations=navigations);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+case,flush=True);c.close()
 b.close()
assert files==source();(OUT/'time-task-return-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
