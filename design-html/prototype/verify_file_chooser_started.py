"""Shared helper contract: block file activation once an operation started, restore it after success/failure."""
import argparse,hashlib,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from verify_pet_controls import ROOT,DEMO,BASE,source
from verify_submission_changes import HOLD

SETUP="""kind=>{const UI=PrototypeUI,screen=document.createElement('section'),form=document.createElement('form'),field=document.createElement('input'),file=document.createElement('input'),save=UI.components.button('提交'),pick=UI.components.button('选图',()=>file.click());field.setAttribute('aria-label','输入');field.value='原值';file.type='file';file.accept='image/*';file.hidden=true;form.append(field);screen.append(form);document.body.append(screen);if(kind==='external'){screen.append(file,save,pick)}else form.append(file,save,pick);save.type='button';pick.type='button';const guard=UI.guard(kind==='external'?form:screen,{value:()=>field.value});window.__writes=0;window.__started=false;window.__outcome=null;save.id='chooser-save';pick.id='chooser-pick';save.onclick=()=>UI.busy(save,'处理中…',async()=>{window.__started=true;await new Promise(r=>window.__finish=r);if(window.__fail)throw Error('模拟操作失败');window.__writes++;guard.commit();return true}).then(v=>window.__outcome=v);}"""

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');args=parser.parse_args();out=ROOT/('evidence/baseline/file-chooser-started' if args.baseline else 'evidence/current/file-chooser-started');out.mkdir(parents=True,exist_ok=True);files=source();styles={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEMO/'assets').glob('*.css')};rows=[]
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for kind in ['external','nested-form']:
   for fail in [False,True]:
    c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000);errors=[];choosers=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('filechooser',lambda e:choosers.append(e));row=dict(scope=kind,failure=fail)
    try:
     p.goto(BASE+'prototype/components.html');p.evaluate(SETUP,kind);p.get_by_label('输入').fill('保留输入');p.evaluate(HOLD);p.evaluate('window.__fail='+str(fail).lower());p.locator('#chooser-save').click();p.evaluate('window.__releaseSubmissionTimers()');p.wait_for_function('window.__started');p.locator('#chooser-pick').click();p.evaluate('Promise.resolve()');row['chooser_count_while_started']=len(choosers);assert not choosers,'File chooser opened during an operation that already started';expect(p.locator('.prototype-toast')).to_have_text('正在完成保存，请稍候');expect(p.get_by_label('输入')).to_have_value('保留输入');assert p.evaluate('window.__writes')==0
     p.evaluate('window.__finish()');p.wait_for_function('window.__outcome!==null');expect(p.locator('#chooser-save')).to_be_enabled();assert p.evaluate('window.__writes')==(0 if fail else 1)
     with p.expect_file_chooser() as info:p.locator('#chooser-pick').click()
     info.value.set_files([]);assert len(choosers)==1;assert not errors,errors;row.update(passed=True,restored_after_operation=True)
    except Exception:row.update(passed=False,error=traceback.format_exc()[-2100:])
    row['errors']=errors;rows.append(row);c.close();assert source()==files;print(('PASS ' if row['passed'] else 'FAIL ')+kind+' '+str(fail),flush=True)
  b.close()
 (out/'results.json').write_text(json.dumps(dict(files=files,styles=styles,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=rows,scope='Four synthetic shared contracts, not four real app screens; actual Chromium chooser event activation and restore checked',accepted_pages=0),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
