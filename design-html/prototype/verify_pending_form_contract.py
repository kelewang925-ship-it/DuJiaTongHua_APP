"""Shared helper contracts for the operation-start boundary, clean cancellation and detached buttons."""
import json,hashlib,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from verify_pet_controls import ROOT,DEMO,BASE,source
from verify_pending_form_cancel import HOLD

SETUP="""()=>{const UI=PrototypeUI;const form=document.createElement('form');const input=document.createElement('input');input.setAttribute('aria-label','测试输入');input.value='原值';const submit=UI.components.button('保存');submit.type='submit';form.append(input,submit);const protect=UI.protectSheet(form);window.__form=form;window.__protect=protect;window.__writes=0;window.__started=false;window.__outcome=null;form.onsubmit=e=>{e.preventDefault();window.__attempt=UI.busy(submit,'保存中…',async()=>{window.__started=true;await new Promise(resolve=>window.__finish=resolve);if(window.__fail)throw Error('模拟实际操作失败');window.__writes++;protect.commit();await UI.back();return true}).then(result=>window.__outcome=result)};window.__modal=UI.sheet({title:'异步边界测试',content:form,actions:[],beforeClose:protect.beforeClose})}"""

def main():
 files=source();rows=[];styles={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEMO/'assets').glob('*.css')}
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for method,fail in [(m,f) for m in ['button','escape','back'] for f in [False,True]]+ [('clean',False),('detached',False)]:
   c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(method=method,failure_injected=fail)
   try:
    p.goto(BASE+'prototype/components.html');p.evaluate(SETUP);dialog=p.locator('dialog[open]');field=dialog.get_by_label('测试输入');submit=dialog.get_by_role('button',name='保存',exact=True)
    if method in ['clean','detached']:
     p.evaluate(HOLD);submit.click()
     if method=='clean':dialog.get_by_role('button',name='取消',exact=True).click();expect(dialog).to_have_count(0)
     else:p.evaluate('window.__form.remove()')
     p.evaluate('window.__pendingRelease()');p.wait_for_function('window.__outcome===false');assert p.evaluate('window.__writes===0&&!window.__started')
    else:
     field.fill('保留的输入');p.evaluate('window.__fail='+str(fail).lower());submit.click();p.wait_for_function('window.__started')
     if method=='button':dialog.get_by_role('button',name='取消',exact=True).click()
     elif method=='escape':p.keyboard.press('Escape')
     else:p.go_back()
     expect(p.locator('.prototype-toast')).to_have_text('正在完成保存，请稍候');expect(dialog).to_have_count(1);expect(dialog.locator('.prototype-sheet-discard')).to_have_count(0);expect(field).to_have_value('保留的输入');assert p.evaluate('window.__writes===0')
     p.evaluate('window.__finish()')
     if fail:
      p.wait_for_function('window.__outcome===false');expect(submit).to_be_enabled();expect(field).to_have_value('保留的输入');expect(p.locator('.prototype-toast')).to_have_text('模拟实际操作失败')
      dialog.get_by_role('button',name='取消',exact=True).click();expect(dialog.locator('.prototype-sheet-discard')).to_be_visible();dialog.get_by_role('button',name='继续编辑',exact=True).click();expect(field).to_have_value('保留的输入')
      p.evaluate('window.__fail=false;window.__started=false;window.__outcome=null');submit.click();p.wait_for_function('window.__started');p.evaluate('window.__finish()');expect(dialog).to_have_count(0)
     else:expect(dialog).to_have_count(0)
     p.wait_for_function('window.__outcome===true');assert p.evaluate('window.__writes===1')
    assert not errors,errors;row['passed']=True
   except Exception:row.update(passed=False,failure=traceback.format_exc()[-2000:])
   row['errors']=errors;rows.append(row);c.close();assert source()==files;print(('PASS ' if row['passed'] else 'FAIL ')+method+' '+str(fail),flush=True)
  b.close()
 out=ROOT/'evidence/current/pending-form-cancel';out.mkdir(exist_ok=True)
 (out/'contract-results.json').write_text(json.dumps(dict(files=files,styles=styles,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=rows,scope='Synthetic shared-helper contracts only; actual page forms covered separately',accepted_pages=0),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
