"""Real Chromium filechooser requests before selection must cancel an obsolete pending save."""
import argparse,hashlib,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import MODULES,declarations
from verify_pet_controls import ROOT,DEMO,BASE,source
from verify_pending_image_reads import SPECS,GET,CASES
from verify_submission_changes import seed,HOLD
from verify_pending_page_guard import TEXT
from verify_image_pending_exit import fields
from verify_image_read_order import A,uri
from verify_overlay_form_saves import storage

TRIGGERS={'diary-publish':'#add-photo','diary-draft':'#add-photo','photo-edit':'#photo-hit','photo-top':'#photo-hit','moment':'#cover-button','capsule-draft':'.add-photo','profile':'.change','book-supplement':'label.photo'}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');parser.add_argument('--cases');parser.add_argument('--modes',default='cancel,success,decode-failure');args=parser.parse_args();names=args.cases.split(',') if args.cases else list(TRIGGERS)
 out=ROOT/('evidence/baseline/file-chooser-pending' if args.baseline else 'evidence/current/file-chooser-pending');out.mkdir(parents=True,exist_ok=True);files=source();styles={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEMO/'assets').glob('*.css')};fixtures={k:declarations(v) for k,v in MODULES.items()};rows=[]
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for name in names:
   for mode in args.modes.split(','):
    c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(case=name,mode=mode)
    try:
     seed(p,fixtures,name);case=CASES[name];input,preview,property=SPECS[name];before=storage(p);original_fields=fields(p);url=p.url;original=p.evaluate('arg=>{const d=JSON.parse(localStorage.getItem(arg.key)),text=arg.text;return ('+GET[name]+')?.[arg.property]??null}',dict(key=case['key'],text=TEXT,property=property));p.evaluate(HOLD);submit=p.locator(case['submit']);submit.click();expect(submit).to_have_attribute('aria-busy','true')
     with p.expect_file_chooser() as info:p.locator(TRIGGERS[name]).click()
     chooser=info.value;assert p.locator(input).evaluate('e=>e.files.length')==0;p.evaluate('window.__releaseSubmissionTimers()');p.wait_for_function('arg=>location.href!==arg.url||document.querySelector(arg.selector)?.getAttribute("aria-busy")!=="true"',arg=dict(url=url,selector=case['submit']))
     row['unchanged_before_chooser_result']=storage(p)==before;assert row['unchanged_before_chooser_result'],'Pending save wrote before the file chooser returned';assert p.url==url and fields(p)==original_fields;expect(submit).to_be_enabled()
     if mode=='cancel':chooser.set_files([]);expected=original
     else:
      data=A if mode=='success' else b'not an SVG';chooser.set_files(dict(name='chooser.svg',mimeType='image/svg+xml',buffer=data));expected=uri(A) if mode=='success' else original
      if mode=='success':p.wait_for_function('arg=>{const e=document.querySelector(arg.selector);return e&&(e.tagName==="IMG"?e.src===arg.src:e.style.backgroundImage.includes(arg.src))}',arg=dict(selector=preview,src=uri(A)))
      else:expect(p.locator('.prototype-toast')).to_contain_text('图片')
     expect(submit).to_be_enabled();assert storage(p)==before and fields(p)==original_fields;submit.click();expect(submit).to_have_attribute('aria-busy','true');p.evaluate('window.__releaseSubmissionTimers()');p.wait_for_function('url=>location.href!==url',arg=url);p.wait_for_load_state('domcontentloaded')
     expression='arg=>{const d=JSON.parse(localStorage.getItem(arg.key)),text=arg.text;const v='+GET[name]+';return !!v&&(v[arg.property]??null)===arg.image&&('+case['predicate']+')}'
     assert p.evaluate(expression,dict(key=case['key'],text=TEXT,property=property,image=expected));saved=storage(p);p.reload();assert storage(p)==saved;assert not errors,errors;row.update(passed=True,explicit_retry_and_reload_consistent=True)
    except Exception:row.update(passed=False,failure=traceback.format_exc()[-2300:])
    row['errors']=errors;rows.append(row);c.close();assert source()==files
    (out/'results.json').write_text(json.dumps(dict(files=files,styles=styles,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=rows,scope='Eight real upload affordances and Chromium filechooser request; release550ms save delay before supplying any result, then cancel/valid/invalid image and explicit retry. Headless browser boundary, not a real OS dialog.',accepted_pages=0),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(('PASS ' if row['passed'] else 'FAIL ')+name+' '+mode,flush=True)
  b.close()
 print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
 raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
