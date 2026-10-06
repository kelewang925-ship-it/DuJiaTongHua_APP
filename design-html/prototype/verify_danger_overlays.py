"""Actual destructive overlays: keyboard, dismissal, viewport and safe cancel contracts."""
import json,traceback
from playwright.sync_api import sync_playwright,expect
from verify_danger_confirmations import CASES,seed,opened,inspect
from verify_pet_controls import ROOT,source,store
OUT=ROOT/'evidence/current';OUT.mkdir(exist_ok=True);shots=OUT/'danger-layout';shots.mkdir(exist_ok=True);files=source();rows=[]

def done(p,case):
 if case in ['record-repair','account-repair']:
  expect(p.get_by_role('button',name='恢复可读记录'if case=='record-repair'else'恢复可读资料',exact=True)).to_be_visible();p.get_by_role('button',name='稍后处理',exact=True).click()
 expect(p.locator('dialog')).to_have_count(0)

with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
 jobs=[(case,390,method)for case in CASES[:14]for method in ['escape','backdrop','history']]+[(case,width,'layout')for case in ['diary','account-delete','pet-delete','sheet-discard']for width in [320,360,390,414,430]]
 for case,width,method in jobs:
  c=b.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(4500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  try:
   before=seed(p,case);p.evaluate('document.documentElement.style.setProperty("--ui-safe-bottom","34px")');dialog,danger,cancel=opened(p,case);expect(cancel).to_be_focused();assert store(p)==before
   if method=='layout':
    for control in dialog.locator('button:visible').all():
     r=control.bounding_box();assert r['width']>=44 and r['height']>=44 and r['x']>=0 and r['x']+r['width']<=width+.5 and r['y']>=0 and r['y']+r['height']<=844.5,r
    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
    assert inspect(p,danger)['variant']=='danger';assert inspect(p,danger)['color']=='rgb(152, 91, 80)'
    controls=dialog.locator('button:visible:not(:disabled),input:visible:not(:disabled),textarea:visible:not(:disabled),select:visible:not(:disabled),a[href]:visible');controls.first.focus();p.keyboard.press('Shift+Tab');expect(controls.last).to_be_focused();p.keyboard.press('Tab');expect(controls.first).to_be_focused()
    p.evaluate('document.fonts.ready');p.screenshot(path=str(shots/f'{case}-{width}.png'))
    cancel.click()
    if case=='sheet-discard':expect(p.get_by_role('textbox',name='意见反馈',exact=True)).to_have_value('未保存的反馈')
    else:done(p,case)
   else:
    trigger={ 'book':p.locator('.show-delete'),'unlink':p.locator('.unlink'),'cache':p.locator('#cache')}.get(case)
    if method=='escape':p.keyboard.press('Escape')
    elif method=='backdrop':p.mouse.click(4,4)
    else:p.go_back()
    done(p,case)
    if trigger is not None:expect(trigger).to_be_focused()
   assert store(p)==before;assert not errors;row=dict(passed=True)
  except Exception:row=dict(passed=False,failure=traceback.format_exc()[-2200:])
  row.update(case=case,width=width,method=method,errors=errors,effective=p.url);rows.append(row);print(('PASS 'if row['passed']else'FAIL ')+case+' '+str(width)+' '+method,flush=True);c.close()
 b.close()
assert files==source();(OUT/'danger-overlay-results.json').write_text(json.dumps(dict(files=files,results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['passed']for r in rows)else 1)
