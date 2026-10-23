"""Real native image decode order; latest chosen file and explicit removal must win."""
import argparse,hashlib,json,traceback,base64
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import MODULES,declarations
from verify_pet_controls import ROOT,DEMO,BASE,source
from verify_pending_image_reads import SPECS,GET,CASES
from verify_submission_changes import seed,HOLD
from verify_pending_page_guard import TEXT
from verify_overlay_form_saves import storage

GATE="""()=>{const read=FileReader.prototype.readAsDataURL,ImageClass=window.Image;window.__imageJobs=[];window.__imageDone=[];FileReader.prototype.readAsDataURL=function(blob){window.__imageJobs.push(()=>read.call(this,blob))};window.__releaseImage=i=>window.__imageJobs[i]();window.Image=function(...args){const image=new ImageClass(...args);for(const type of ['load','error'])image.addEventListener(type,()=>window.__imageDone.push({src:image.src,type}));return image};window.Image.prototype=ImageClass.prototype}"""
A=b'<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"><rect width="16" height="16" fill="pink"/></svg>'
B=b'<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"><rect width="16" height="16" fill="blue"/></svg>'
def uri(data):return 'data:image/svg+xml;base64,'+base64.b64encode(data).decode()
def choose(p,selector,data,name):p.locator(selector).set_input_files(dict(name=name,mimeType='image/svg+xml',buffer=data))
def finish(p,index,data):p.evaluate('i=>window.__releaseImage(i)',index);p.wait_for_function('src=>window.__imageDone.some(v=>v.src===src)',arg=uri(data))
def shown(p,name,image):
 if name=='world-avatar':return p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-relationship")).profile?.avatar')==image
 selector=SPECS[name][1]
 if not p.locator(selector).is_visible():return False
 return p.locator(selector).evaluate('(e,image)=>e.tagName==="IMG"?e.src===image:e.style.backgroundImage.includes(image)',image)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');parser.add_argument('--cases');parser.add_argument('--modes',default='old-success,old-error,older-first,latest-error,remove');args=parser.parse_args();names=args.cases.split(',') if args.cases else ['diary-publish','photo-top','moment','capsule-draft','profile','book-supplement','world-avatar']
 out=ROOT/('evidence/baseline/image-read-order' if args.baseline else 'evidence/current/image-read-order');out.mkdir(parents=True,exist_ok=True);files=source();styles={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEMO/'assets').glob('*.css')};fixtures={k:declarations(v) for k,v in MODULES.items()};rows=[]
 cases=[(n,m) for n in names for m in args.modes.split(',') if m!='remove' or n in ['diary-publish','capsule-draft']]
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for name,mode in cases:
   c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(case=name,mode=mode)
   try:
    if name=='world-avatar':fixtures['settings']['seed'](p,'m06-p03');selector='input[type=file]'
    else:seed(p,fixtures,name);selector=SPECS[name][0]
    p.evaluate(GATE);before=storage(p)
    if mode=='older-first':p.evaluate(HOLD)
    if mode=='remove':
     choose(p,selector,B,'latest.svg');finish(p,0,B);assert shown(p,name,uri(B));choose(p,selector,A,'pending.svg');p.locator('#remove' if name=='diary-publish' else '.prototype-capsule-remove').click();finish(p,1,A)
     expect(p.locator('#preview' if name=='diary-publish' else '.prototype-capsule-preview')).to_be_hidden();expected=None
    elif mode=='latest-error':
     choose(p,selector,A,'original.svg');finish(p,0,A);assert shown(p,name,uri(A));broken=b'not an SVG';choose(p,selector,broken,'broken.svg');finish(p,1,broken)
     assert shown(p,name,uri(A)),'Failed replacement removed the previous valid image';expect(p.locator('.prototype-toast[role=alert]')).to_be_visible();expected=uri(A);row['previous_valid_image_retained']=True
    elif mode=='older-first':
     choose(p,selector,A,'older.svg');choose(p,selector,B,'latest.svg');finish(p,0,A);assert storage(p)==before,'Older read wrote before latest read completed'
     if name!='world-avatar':
      submit=p.locator(CASES[name]['submit'])
      if submit.is_enabled():submit.click()
      assert p.evaluate('window.__submissionTimers.length')==0,'Older completion cleared latest reading state'
     finish(p,1,B);assert shown(p,name,uri(B));expected=uri(B);row['latest_read_kept_pending']=True
    else:
     older=A if mode=='old-success' else b'not an SVG';choose(p,selector,older,'older.svg');choose(p,selector,B,'latest.svg');finish(p,1,B);assert shown(p,name,uri(B));finish(p,0,older);row['latest_still_shown']=shown(p,name,uri(B));assert row['latest_still_shown'],'Older image overwrote the latest selection';expect(p.locator('.prototype-toast[role=alert]')).to_have_count(0);expected=uri(B)
    if name=='world-avatar':p.reload();assert shown(p,name,expected)
    else:
     case=CASES[name];url=p.url;p.locator(case['submit']).click()
     if mode=='older-first':p.evaluate('window.__releaseSubmissionTimers()')
     p.wait_for_function('url=>location.href!==url',arg=url);p.wait_for_load_state('domcontentloaded')
     expression='arg=>{const d=JSON.parse(localStorage.getItem(arg.key)),text=arg.text;const v='+GET[name]+';return !!v&&(v[arg.property]??null)===arg.image&&('+case['predicate']+')}'
     assert p.evaluate(expression,dict(key=case['key'],text=TEXT,property=SPECS[name][2],image=expected));saved=storage(p);p.reload();assert storage(p)==saved
    assert not errors,errors;row.update(passed=True,persisted_and_reload_consistent=True)
   except Exception:row.update(passed=False,failure=traceback.format_exc()[-2100:])
   row['errors']=errors;rows.append(row);c.close();assert source()==files
   (out/'results.json').write_text(json.dumps(dict(files=files,styles=styles,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=rows,scope='Native FileReader releases newer before older; real Image load/error observed; real preview and persisted result checked',accepted_pages=0),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(('PASS ' if row['passed'] else 'FAIL ')+name+' '+mode,flush=True)
  b.close()
 print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
 raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
