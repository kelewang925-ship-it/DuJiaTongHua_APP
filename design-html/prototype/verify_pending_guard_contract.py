"""Synthetic guard scopes and asynchronous operation-start navigation contracts."""
import json,hashlib,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from verify_pet_controls import ROOT,DEMO,BASE,source

SETUP="""kind=>{const UI=PrototypeUI,outer=document.createElement('section'),form=document.createElement('form'),input=document.createElement('input'),submit=UI.components.button('提交任务');input.setAttribute('aria-label','边界输入');input.value='原内容';submit.type='button';form.append(input);outer.append(form);document.body.append(outer);if(kind==='form-external')outer.append(submit);else form.append(submit);const root=kind==='form-external'?form:outer,guard=UI.guard(root,{value:()=>input.value,fallback:'components.html?left=1'}),link=document.createElement('a');link.href='components.html?left=1';link.textContent='离开编辑';link.id='contract-leave';outer.append(link);window.__contractStarted=false;window.__contractFail=false;submit.id='contract-submit';submit.onclick=()=>{window.__contractResult=undefined;window.__contractStarted=false;UI.busy(submit,'提交中…',async()=>{window.__contractStarted=true;await new Promise(r=>window.__contractFinish=r);if(window.__contractFail)throw Error('边界写入失败');UI.write('guard-contract-writes',(UI.read('guard-contract-writes',0)||0)+1);await guard.complete('components.html?saved=1');return true}).then(v=>window.__contractResult=v)};}"""

def main():
 files=source();styles={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEMO/'assets').glob('*.css')};rows=[]
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for kind in ['form-external','screen-with-form']:
   for method in ['back','link','browser']:
    for fail in [False,True]:
     c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(scope=kind,exit=method,failure=fail)
     try:
      p.goto(BASE+'prototype/components.html');p.evaluate(SETUP,kind);url=p.url;field=p.get_by_label('边界输入');field.fill('原样保留');p.evaluate('window.__contractFail='+str(fail).lower());submit=p.locator('#contract-submit');submit.click();p.wait_for_function('window.__contractStarted')
      if method=='back':p.evaluate('void PrototypeUI.back()')
      elif method=='link':p.locator('#contract-leave').click()
      else:p.go_back()
      expect(p.locator('.prototype-toast')).to_have_text('正在完成保存，请稍候');expect(p.locator('dialog[open]')).to_have_count(0);assert p.url==url;expect(field).to_have_value('原样保留');assert p.evaluate('localStorage.getItem("guard-contract-writes")') is None
      p.evaluate('window.__contractFinish()')
      if fail:
       p.wait_for_function('window.__contractResult===false');expect(submit).to_be_enabled();expect(field).to_have_value('原样保留');p.evaluate('void PrototypeUI.back()');dialog=p.locator('dialog[open]');expect(dialog.locator('h2')).to_have_text('是否放弃当前修改？');dialog.get_by_role('button',name='继续编辑',exact=True).click();expect(dialog).to_have_count(0);expect(field).to_have_value('原样保留');p.evaluate('window.__contractFail=false');submit.click();p.wait_for_function('window.__contractStarted');p.evaluate('window.__contractFinish()')
      p.wait_for_url('**/components.html?saved=1');assert p.evaluate('JSON.parse(localStorage.getItem("guard-contract-writes"))')==1;p.reload();assert p.evaluate('JSON.parse(localStorage.getItem("guard-contract-writes"))')==1;assert not errors,errors;row['passed']=True
     except Exception:row.update(passed=False,error=traceback.format_exc()[-2000:])
     row['errors']=errors;rows.append(row);c.close();assert source()==files;print(('PASS ' if row['passed'] else 'FAIL ')+kind+' '+method+' '+str(fail),flush=True)
  b.close()
 out=ROOT/'evidence/current/pending-page-guard';out.mkdir(exist_ok=True);(out/'contract-results.json').write_text(json.dumps(dict(files=files,styles=styles,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=rows,scope='12 synthetic helper contracts; not 12 actual app pages',accepted_pages=0),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
