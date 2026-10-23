"""Native FileReader gate: choose image after submitting, before the existing busy callback begins."""
import argparse,hashlib,json,traceback,base64
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import MODULES,declarations
from verify_pet_controls import ROOT,DEMO,BASE,source
from verify_pending_page_guard import CASES,TEXT
from verify_submission_changes import seed,HOLD
from verify_overlay_form_saves import storage

READ_GATE="""()=>{const read=FileReader.prototype.readAsDataURL;window.__imageReads=[];window.__releaseImageReads=()=>{for(const job of window.__imageReads.splice(0))job()};FileReader.prototype.readAsDataURL=function(blob){window.__imageReads.push(()=>read.call(this,blob))}}"""
SPECS={
 'diary-publish':('#file','#preview-image','image'),
 'diary-draft':('#file','#preview-image','image'),
 'photo-edit':('#file','#selected','image'),
 'photo-top':('#file','#selected','image'),
 'moment':('#cover-file','#cover-preview','cover'),
 'capsule-draft':('#photo','.prototype-capsule-preview','photo'),
 'profile':('#avatar','#avatar-preview','avatar'),
 'book-supplement':('input[type=file]','.book-supplement-preview img','image')}
CASES['book-supplement']=dict(group='book',page='m08-p19',submit='.submit',fields={'.message':TEXT},key='dujia-prototype-books',predicate='d.find(v=>v.id==="book-state").pages.find(v=>v.id==="page-second").supplements.filter(v=>v.text===text).length===1')

GET={
 'diary-publish':'d.find(v=>v.title===text&&v.status==="published")',
 'diary-draft':'d.find(v=>v.title===text&&v.status==="draft")',
 'photo-edit':'d.find(v=>v.id==="audit-photo")','photo-top':'d.find(v=>v.id==="audit-photo")',
 'moment':'d.find(v=>v.name===text)','capsule-draft':'d.find(v=>v.name===text)',
 'profile':'d','book-supplement':'d.find(v=>v.id==="book-state").pages.find(v=>v.id==="page-second").supplements?.find(v=>v.text===text)'}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');parser.add_argument('--cases');args=parser.parse_args();names=args.cases.split(',') if args.cases else list(SPECS)
 out=ROOT/('evidence/baseline/pending-image-read' if args.baseline else 'evidence/current/pending-image-read');out.mkdir(parents=True,exist_ok=True);files=source();styles={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEMO/'assets').glob('*.css')};fixtures={k:declarations(v) for k,v in MODULES.items()};png=fixtures['record']['PNG'];image='data:image/png;base64,'+base64.b64encode(png).decode();rows=[]
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for name in names:
   for mode in ['success','decode-failure']:
    c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(case=name,mode=mode)
    try:
     seed(p,fixtures,name);case=CASES[name];file,preview,property=SPECS[name];before=storage(p);url=p.url
     original=p.evaluate('arg=>{const d=JSON.parse(localStorage.getItem(arg.key)),text=arg.text;const v='+GET[name]+';return v?.[arg.property]??null}',dict(key=case['key'],text=TEXT,property=property))
     p.evaluate(HOLD);p.evaluate(READ_GATE);submit=p.locator(case['submit']);submit.click();expect(submit).to_have_attribute('aria-busy','true');p.locator(file).set_input_files(dict(name='new-photo.png',mimeType='image/png',buffer=png if mode=='success' else b'not a decodable PNG'));assert p.evaluate('window.__imageReads.length')==1
     p.evaluate('window.__releaseSubmissionTimers()');p.wait_for_function('arg=>location.href!==arg.url||document.querySelector(arg.selector)?.getAttribute("aria-busy")!=="true"',arg=dict(url=url,selector=case['submit']))
     row['unchanged_while_image_reading']=storage(p)==before;assert row['unchanged_while_image_reading'],'Saved previous image while replacement still reading';assert p.url==url
     # The same real save entry remains gated by its existing reading state.
     if submit.is_enabled():submit.click()
     assert p.evaluate('window.__submissionTimers.length')==0;assert storage(p)==before;row['save_during_read_blocked']=True
     p.evaluate('window.__releaseImageReads()')
     if mode=='success':
      p.wait_for_function('arg=>{const e=document.querySelector(arg.selector);return e&&(e.tagName==="IMG"?e.src===arg.image:e.style.backgroundImage.includes(arg.image))}',arg=dict(selector=preview,image=image))
     else:expect(p.locator('.prototype-toast')).to_contain_text('图片')
     expect(submit).to_be_enabled();assert storage(p)==before;submit.click();expect(submit).to_have_attribute('aria-busy','true');p.evaluate('window.__releaseSubmissionTimers()')
     expected=image if mode=='success' else original
     predicate='arg=>{const d=JSON.parse(localStorage.getItem(arg.key)),text=arg.text;const v='+GET[name]+';return !!v&&(v[arg.property]??null)===arg.image&&('+case['predicate']+');}'
     p.wait_for_function(predicate,arg=dict(key=case['key'],text=TEXT,property=property,image=expected));p.wait_for_function('url=>location.href!==url',arg=url);p.wait_for_load_state('domcontentloaded');saved=storage(p);p.reload();assert storage(p)==saved;row['explicit_retry_and_reload_consistent']=True
     assert not errors,errors;row['passed']=True
    except Exception:row.update(passed=False,failure=traceback.format_exc()[-2300:])
    row['errors']=errors;rows.append(row);c.close();assert source()==files
    (out/'results.json').write_text(json.dumps(dict(files=files,styles=styles,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=rows,scope='Eight actual save entries x native image decode success/failure; hold real FileReader.readAsDataURL plus550ms busy timers only, retain actual image decode/business/storage/navigation',accepted_pages=0),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(('PASS ' if row['passed'] else 'FAIL ')+name+' '+mode,flush=True)
  b.close()
 print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
 raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
