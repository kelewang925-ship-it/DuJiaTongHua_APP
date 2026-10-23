"""Actual workshop album saves across native Image.decode waits and a second private page."""
import argparse,hashlib,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from verify_pet_controls import ROOT,DEMO,BASE,source
from verify_image_read_order import A,uri
from verify_overlay_form_saves import storage,quota

KEY='dujia-prototype-records';ID='work-photo-work-ready'
CASES=['normal-fallback','normal-photo','concurrent-export-edit','unrelated-insert','source-hidden','work-edited','work-deleted','decode-error-retry','quota-retry','repeat-existing']
GATE="""()=>{const decode=HTMLImageElement.prototype.decode;window.__decodeJobs=[];window.__decodeDone=[];HTMLImageElement.prototype.decode=function(){const image=this;return new Promise((resolve,reject)=>{const index=window.__decodeJobs.length;window.__decodeJobs.push(()=>decode.call(image).then(()=>{window.__decodeDone.push({index,ok:true});resolve()},error=>{window.__decodeDone.push({index,ok:false});reject(error)}))})};window.__releaseDecode=i=>window.__decodeJobs[i]()}"""

def records(p):return p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-records'))")
def result(p):return next((v for v in records(p) if v['id']==ID),None)
def start(p,index):p.locator('#save').click();p.wait_for_function('i=>window.__decodeJobs.length===i+1',arg=index);expect(p.locator('#save')).to_have_attribute('aria-busy','true')
def finish(p,index):p.evaluate('i=>window.__releaseDecode(i)',index);p.wait_for_function('i=>window.__decodeDone.some(v=>v.index===i)',arg=index);expect(p.locator('#save')).to_be_enabled()
def photo_source(p,image):p.evaluate("image=>{const k='dujia-prototype-works',w=JSON.parse(localStorage.getItem(k));w.find(v=>v.id==='work-ready').sourceKind='photo';w.find(v=>v.id==='work-ready').sourceIds=['work-photo'];localStorage.setItem(k,JSON.stringify(w));const rk='dujia-prototype-records',r=JSON.parse(localStorage.getItem(rk));r.find(v=>v.id==='work-photo').image=image;localStorage.setItem(rk,JSON.stringify(r))}",image)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--baseline',action='store_true');args=ap.parse_args();files=source();styles={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEMO/'assets').glob('*.css')};fixture=declarations('verify_workshop_controls.py');out=ROOT/('evidence/baseline/work-album-decode' if args.baseline else 'evidence/current/work-album-decode');out.mkdir(parents=True,exist_ok=True);rows=[]
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  for name in CASES:
   c=b.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');p=c.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(case=name)
   try:
    fixture['seed'](p,'m05-p08')
    if name in ['normal-photo','decode-error-retry']:photo_source(p,uri(A) if name=='normal-photo' else 'data:image/png;base64,bm90YW5pbWFnZQ==');p.reload()
    p.evaluate(GATE);other=c.new_page();other.goto(p.url);other.evaluate(GATE)
    if name=='quota-retry':quota(p,KEY)
    before=storage(p);start(p,0)
    if name=='concurrent-export-edit':
     start(other,0);finish(other,0);assert result(other);other.goto(BASE+'pages/m03-p11.html?id='+ID);other.locator('[name=caption]').fill('另一页保存的照片心情');other.locator('#done').click();other.wait_for_url('**/m03-p12.html?id='+ID);expect(other.locator('.caption')).to_have_text('另一页保存的照片心情');changed=storage(p);finish(p,0);assert storage(p)==changed,'Delayed album export overwrote the already exported and edited photo';assert result(p)['caption']=='另一页保存的照片心情';row['external_edit_preserved']=True
    else:
     if name=='unrelated-insert':other.evaluate("()=>{const k='dujia-prototype-records',v=JSON.parse(localStorage.getItem(k));v.push({id:'external-record',type:'diary',title:'外部日记',body:'保持',status:'published',visibility:'shared'});localStorage.setItem(k,JSON.stringify(v))}")
     elif name=='source-hidden':other.evaluate("()=>{const k='dujia-prototype-records',v=JSON.parse(localStorage.getItem(k));v.find(v=>v.id==='work-diary').visibility='private';localStorage.setItem(k,JSON.stringify(v))}")
     elif name in ['work-edited','work-deleted']:other.evaluate("remove=>{const k='dujia-prototype-works';let v=JSON.parse(localStorage.getItem(k));if(remove)v=v.filter(v=>v.id!=='work-ready');else v.find(v=>v.id==='work-ready').story='外部作品';localStorage.setItem(k,JSON.stringify(v))}",name=='work-deleted')
     changed=storage(p);finish(p,0)
     if name in ['source-hidden','work-edited','work-deleted']:
      assert storage(p)==changed and result(p) is None;expect(p.locator('.prototype-toast[role=alert]')).to_be_visible();row['stale_export_rejected']=True
     elif name in ['decode-error-retry','quota-retry']:
      assert storage(p)==before and result(p) is None
      expect(p.locator('.prototype-toast[role=alert]')).to_contain_text('图片暂时无法读取，请重试保存' if name=='decode-error-retry' else '空间不足')
      if name=='decode-error-retry':other.evaluate("image=>{const k='dujia-prototype-records',v=JSON.parse(localStorage.getItem(k));v.find(v=>v.id==='work-photo').image=image;localStorage.setItem(k,JSON.stringify(v))}",uri(A))
      start(p,1);finish(p,1);assert result(p);row['explicit_retry_saved_once']=True
     else:
      saved=result(p);assert saved and saved['image'].startswith('data:image/png;base64,');expect(p.locator('.prototype-toast')).to_contain_text('已保存到共同相册')
      if name=='unrelated-insert':assert next(v for v in records(p) if v['id']=='external-record')['body']=='保持'
      if name=='repeat-existing':
       saved=storage(p);p.locator('#save').click();expect(p.locator('#save')).to_be_enabled();assert p.evaluate('window.__decodeJobs.length')==1 and storage(p)==saved;row['repeat_did_not_decode_or_write']=True
    if result(p):assert sum(v['id']==ID for v in records(p))==1
    saved=storage(p);p.reload();assert storage(p)==saved;assert not errors,errors;row.update(passed=True,reload_consistent=True)
   except Exception:row.update(passed=False,failure=traceback.format_exc()[-2500:])
   row['errors']=errors;rows.append(row);c.close();assert source()==files
   (out/'results.json').write_text(json.dumps(dict(files=files,styles=styles,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=rows,scope='Real save buttons, native decode held/released; actual second export and photo edit; local source/work mutations explicitly simulated in private same-origin page.',accepted_pages=0),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True)
  b.close()
 raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
