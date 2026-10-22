"""Real forms: cancel during the existing 550ms pending window; release timer before discard decision."""
import argparse,hashlib,json,traceback
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import MODULES,declarations
from verify_overlay_form_saves import SPECS,CANDIDATES,TEXT,fill,snapshot,storage
from verify_overlay_exit_paths import close
from verify_pet_controls import ROOT,DEMO,BASE,source

HOLD="""()=>{const original=window.setTimeout;window.__pendingRelease=null;window.setTimeout=function(callback,delay,...args){if(delay===550&&!window.__pendingRelease){window.__pendingRelease=()=>original(callback,0,...args);return -550;}return original(callback,delay,...args)}}"""

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');parser.add_argument('--indices');parser.add_argument('--methods',default='button,escape,back,backdrop,drag,keep');args=parser.parse_args()
 indices=[int(v) for v in args.indices.split(',')] if args.indices else list(SPECS)
 out=ROOT/('evidence/baseline/pending-form-cancel' if args.baseline else 'evidence/current/pending-form-cancel');out.mkdir(parents=True,exist_ok=True)
 raw=(ROOT/'evidence/current/hidden-overlay-observations.json').read_bytes();candidates=json.loads(raw)['results'];fixtures={k:declarations(v) for k,v in MODULES.items()};files=source();rows=[]
 styles={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEMO/'assets').glob('*.css')}
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for index in indices:
   for method in args.methods.split(','):
    c=browser.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));item=candidates[index];values,key,predicate=SPECS[index];row=dict(index=index,page=item['page'],method=method)
    try:
     fixtures[item['group']]['seed'](p,item['page']);p.locator(item['selector']).click();dialog=p.locator('dialog[open]');expect(dialog.locator('h2')).to_have_text(item['overlays'][0]['title']);form=dialog.locator('form');fill(form,values);candidate=snapshot(form);before=storage(p);url=p.url;submit=form.locator('[type=submit]')
     p.evaluate(HOLD);submit.click();expect(submit).to_have_attribute('aria-busy','true');assert p.evaluate('!!window.__pendingRelease')
     if method=='escape':p.keyboard.press('Escape')
     else:close(p,'button' if method=='keep' else method)
     warning=dialog.locator('.prototype-sheet-discard');expect(warning).to_be_visible();p.evaluate('window.__pendingRelease()')
     # A turn of the real task queue, followed by the busy finally, proves the pending callback returned.
     p.wait_for_function('()=>new Promise(resolve=>setTimeout(resolve,50))')
     row['storage_unchanged_before_decision']=storage(p)==before
     if not args.baseline:expect(submit).not_to_have_attribute('aria-busy','true')
     warning.get_by_role('button',name='继续编辑' if method=='keep' else '放弃修改',exact=True).click()
     if method=='keep':
      expect(form).to_be_visible();expect(submit).to_be_enabled();assert snapshot(form)==candidate;assert storage(p)==before;assert p.url==url
      submit.click();expect(dialog).to_have_count(0)
      if index in CANDIDATES:
       assert storage(p)==before;parent,preview=CANDIDATES[index];expect(p.locator(preview)).to_contain_text(TEXT);p.locator(parent).click()
      p.wait_for_function('arg=>{const d=JSON.parse(localStorage.getItem(arg.key)),text=arg.text;return '+predicate+'}',arg=dict(key=key,text=TEXT))
      if index in [84,118,122]:p.wait_for_url('**/m07-p18.html*' if index==84 else '**/m08-p13.html*' if index==118 else '**/m08-p14.html*')
      row['retry_persisted']=True
     else:
      expect(dialog).to_have_count(0);row['storage_unchanged_after_discard']=storage(p)==before;assert row['storage_unchanged_after_discard'],'Discard still wrote to storage';assert p.url==url
      p.reload();assert storage(p)==before;row['reload_consistent']=True
     assert row['storage_unchanged_before_decision'],'Operation wrote while discard choice was pending';assert not errors,errors;row['passed']=True
    except Exception:row.update(passed=False,failure=traceback.format_exc()[-1900:])
    row['errors']=errors;rows.append(row);c.close();assert source()==files
    report=dict(files=files,styles=styles,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),locator_candidates_sha256=hashlib.sha256(raw).hexdigest(),locator_candidates_only=True,timer_instrumentation='Only the existing 550ms pending timer is held; actual operations and storage remain unchanged',results=rows,accepted_pages=0)
    (out/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(('PASS ' if row['passed'] else 'FAIL ')+str(index)+' '+method,flush=True)
  browser.close()
 print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
 raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

from pathlib import Path
if __name__=='__main__':main()
