"""Ordinary confirmations and edit forms retain explicit primary variants."""
import json,traceback
from playwright.sync_api import sync_playwright,expect
from verify_danger_confirmations import seed,inspect
from verify_pet_controls import ROOT,source,store,BASE
OUT=ROOT/'evidence/current';files=source();rows=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 for case in ['account-intro','logout','pet-pause','phone-edit','pet-rename']:
  c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:
   seed(p,'account-delete'if case in ['account-intro','logout','phone-edit']else'pet-delete')
   if case=='pet-pause':p.goto(BASE+'pages/m07-p24.html')
   before=store(p)
   if case=='account-intro':p.locator('.delete').click();label='继续身份确认'
   elif case=='logout':p.locator('.logout').click();label='确认退出'
   elif case=='pet-pause':p.locator('#unlink').click();label='确认暂停'
   elif case=='phone-edit':p.locator('.phone').click();label='保存'
   else:p.get_by_role('button',name='更多',exact=True).click();p.get_by_role('button',name='修改宠物名字',exact=True).click();label='保存宠物名字'
   button=p.locator('dialog').get_by_role('button',name=label,exact=True);metrics=inspect(p,button);assert metrics['variant']=='primary'and metrics['danger']is None and metrics['shared'],metrics
   cancel=p.locator('dialog').get_by_role('button',name='继续使用'if case=='logout'else'继续照顾'if case=='pet-pause'else'取消',exact=True);
   if case in ['phone-edit','pet-rename']:expect(p.locator('dialog h2')).to_be_focused()
   else:expect(cancel).to_be_focused()
   cancel.click();expect(p.locator('dialog')).to_have_count(0);assert store(p)==before;assert not errors;row=dict(passed=True,metrics=metrics)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-2000:])
  row.update(case=case,errors=errors);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+case,flush=True);c.close()
 b.close()
assert files==source();(OUT/'danger-primary-contract-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
