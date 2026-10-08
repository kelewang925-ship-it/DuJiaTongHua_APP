"""Recover unreadable date without calling the surviving anniversary deleted."""
import json,sys,traceback
from playwright.sync_api import sync_playwright,expect
from verify_time_collection_recovery import seed,prompt,repair,raw,archives,key
from audit_current_runtime import data
from verify_pet_controls import ROOT,BASE,source
OUT=ROOT/('evidence/baseline'if '--baseline'in sys.argv else'evidence/current');files=source();rows=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 try:
  item={**data(True)[key('anniversaries')][0],'date':{}};value=json.dumps([item],ensure_ascii=False);seed(p,'anniversaries',value,'m04-p10.html?id='+item['id']);prompt(p,'anniversaries');assert raw(p,'anniversaries')==value
  with p.expect_request_finished(lambda r:r.resource_type=='document'and r.url==BASE+'pages/m04-p10.html?id='+item['id']):repair(p,'anniversaries')
  p.wait_for_load_state('load')
  expect(p.get_by_role('button',name='编辑纪念日',exact=True)).to_be_visible();expect(p.get_by_text('纪念日日期需要修正',exact=True)).to_be_visible();p.get_by_role('button',name='编辑纪念日',exact=True).click();p.wait_for_url('**/m04-p09.html*');expect(p.locator('[name=name]')).to_have_value(item['name']);p.locator('[name=date]').click();p.get_by_label('选择纪念日日期',exact=True).fill('2099-01-01');p.get_by_role('button',name='使用这个日期',exact=True).click();p.locator('.submit').click();p.wait_for_url('**/m04-p10.html*');saved=json.loads(raw(p,'anniversaries'))[0];assert saved['id']==item['id']and saved['name']==item['name']and saved['date']=='2099-01-01'and archives(p,'anniversaries')==[value];assert not errors;row=dict(passed=True)
 except Exception:row=dict(passed=False,failure=traceback.format_exc()[-2200:])
 row.update(case='date-structure-recovery-edit-save',errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+row['case'],flush=True);b.close()
assert files==source();(OUT/'anniversary-date-recovery-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
