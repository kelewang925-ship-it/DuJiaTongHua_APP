"""Image-only dirty state while native I/O is pending: keep, fail and discard during delayed navigation."""
import argparse,hashlib,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import MODULES,declarations
from verify_pet_controls import ROOT,DEMO,BASE,source
from verify_image_read_order import GATE,A,uri,choose,finish,shown
from verify_pending_image_reads import SPECS,GET,CASES
from verify_pending_page_guard import prepare,TEXT
from verify_overlay_form_saves import storage

NAMES=['diary-publish','photo-top','moment','capsule-draft','profile','book-supplement']
def fields(p):return p.locator('.screen').evaluate('e=>JSON.stringify([...e.querySelectorAll("input:not([type=file]),textarea,select")].map(v=>[v.id,v.name,v.value,v.checked]))')
def leave(p,method):p.go_back() if method=='browser' else p.locator('.back').first.click()

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');parser.add_argument('--methods',default='button,browser');parser.add_argument('--modes',default='keep-success,keep-failure,discard-held');args=parser.parse_args();out=ROOT/('evidence/baseline/image-pending-exit' if args.baseline else 'evidence/current/image-pending-exit');out.mkdir(parents=True,exist_ok=True);files=source();styles={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEMO/'assets').glob('*.css')};fixtures={k:declarations(v) for k,v in MODULES.items()};rows=[]
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for name in NAMES:
   for method in args.methods.split(','):
    for mode in args.modes.split(','):
     c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(5000);errors=[];native=[];p.on('pageerror',lambda e:errors.append(str(e)))
     def browser_dialog(d):native.append(dict(type=d.type,message=d.message));d.dismiss()
     p.on('dialog',browser_dialog);row=dict(case=name,method=method,mode=mode)
     try:
      case=CASES[name];fixtures[case['group']]['seed'](p,case.get('seed_page',case['page']))
      if 'editor' in case:p.goto(BASE+'pages/'+case['editor'])
      editor=p.url;p.goto(BASE+'pages/m03-p02.html');source_url=p.url;p.goto(editor,referer=source_url)
      original=fields(p);before=storage(p);url=p.url;p.evaluate(GATE);data=b'not a valid SVG' if mode=='keep-failure' else A;choose(p,SPECS[name][0],data,'pending.svg');assert p.evaluate('window.__imageJobs.length')==1;assert fields(p)==original
      leave(p,method);dialog=p.locator('dialog[open]');expect(dialog.locator('h2')).to_have_text('是否放弃当前修改？');assert storage(p)==before;row['pending_image_only_protected']=True
      if mode=='discard-held':
       p.evaluate('()=>{const go=history.go.bind(history);window.__heldImageExit=null;history.go=delta=>{window.__heldImageExit=()=>go(delta)}}')
       dialog.get_by_role('button',name='放弃修改',exact=True).click();p.wait_for_function('!!window.__heldImageExit');finish(p,0,A);assert not shown(p,name,uri(A)),'Discarded read still filled the old editor';assert storage(p)==before;row['late_result_ignored']=True
       p.evaluate('window.__heldImageExit()');p.wait_for_function('url=>location.href!==url',arg=url);p.wait_for_load_state('domcontentloaded');assert storage(p)==before;p.reload();assert storage(p)==before
      else:
       dialog.get_by_role('button',name='继续编辑',exact=True).click();expect(dialog).to_have_count(0);assert p.url==url and fields(p)==original;finish(p,0,data)
       if mode=='keep-failure':
        expect(p.locator('.prototype-toast')).to_contain_text('图片');assert fields(p)==original;leave(p,method);p.wait_for_function('url=>location.href!==url',arg=url);p.wait_for_load_state('domcontentloaded');expect(p.locator('dialog[open]')).to_have_count(0);assert storage(p)==before;p.reload();assert storage(p)==before;row['failure_restores_clean_state']=True
       else:
        assert shown(p,name,uri(A));leave(p,method);expect(dialog.locator('h2')).to_have_text('是否放弃当前修改？');dialog.get_by_role('button',name='继续编辑',exact=True).click();expect(dialog).to_have_count(0);assert shown(p,name,uri(A));prepare(p,name);p.locator(case['submit']).click();p.wait_for_function('url=>location.href!==url',arg=url);p.wait_for_load_state('domcontentloaded')
        expression='arg=>{const d=JSON.parse(localStorage.getItem(arg.key)),text=arg.text;const v='+GET[name]+';return !!v&&v[arg.property]===arg.image&&('+case['predicate']+')}'
        assert p.evaluate(expression,dict(key=case['key'],text=TEXT,property=SPECS[name][2],image=uri(A)));saved=storage(p);p.reload();assert storage(p)==saved;row['continued_and_saved']=True
      assert not native,native;assert not errors,errors;row['passed']=True
     except Exception:row.update(passed=False,failure=traceback.format_exc()[-2400:])
     row.update(errors=errors,native_dialogs=native);rows.append(row);c.close();assert source()==files
     (out/'results.json').write_text(json.dumps(dict(files=files,styles=styles,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=rows,scope='Six actual image-only editors x top/browser exits x keep-success/keep-failure/discard with deferred real history.go navigation; native FileReader and Image callbacks retained',accepted_pages=0),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(('PASS ' if row['passed'] else 'FAIL ')+name+' '+method+' '+mode,flush=True)
  b.close()
 print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
 raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
