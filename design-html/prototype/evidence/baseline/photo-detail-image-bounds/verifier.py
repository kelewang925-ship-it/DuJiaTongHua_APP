"""Photo-frame image containment on the real detail page, with scoped behavior replay."""
import argparse, hashlib, json, traceback
from pathlib import Path
from urllib.parse import quote
from playwright.sync_api import sync_playwright, expect
from audit_current_runtime import data
from audit_runtime import INIT
from audit_hidden_overlays import declarations
from verify_pet_controls import ROOT, DEMO, BASE, source

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def seed(page, image=None):
    page.goto(BASE+'prototype/review.html')
    values=data(True)
    item=next(r for r in values['dujia-prototype-records'] if r['type']=='photo')
    if image is not None: item['image']=image
    item['caption']='照片的长说明仍应可以独立阅读。'*40
    page.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',values)
    page.goto(BASE+'pages/m03-p12.html?id='+item['id'])
    page.evaluate('document.fonts.ready')

def bounds(page):
    return page.evaluate('''()=>Object.fromEntries(['.photo','.photo img','.caption','.meta'].map(s=>{
      const r=document.querySelector(s).getBoundingClientRect();return [s,{top:r.top,bottom:r.bottom,left:r.left,right:r.right,height:r.height}];}))''')

def contained(r):
    image=r['.photo img'];frame=r['.photo']
    assert image['top']>=frame['top']-.5 and image['bottom']<=frame['bottom']+.5,r
    assert image['left']>=frame['left']-.5 and image['right']<=frame['right']+.5,r
    assert image['bottom']<=r['.caption']['top'],r
    assert r['.caption']['bottom']<=r['.meta']['top'],r

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['baseline','current'],required=True);args=parser.parse_args()
    out=ROOT/f'evidence/{args.stage}/photo-detail-image-bounds';out.mkdir(parents=True,exist_ok=True)
    cases=[('geometry',(width,w,h)) for width in [320,360,390,414,430] for w,h in [(80,100),(160,90),(100,100)]]
    if args.stage=='current':
        cases += [('image-retry',None)]
        catalog=json.loads((ROOT/'evidence/current/page-contracts.json').read_text(encoding='utf-8'))
        controls=next(r for r in catalog['pages'] if r['id']=='m03-p12')['control_evidence']
        assert len(controls)==6
        cases += [('control',c) for c in controls]
        cases += [('dirty',method) for method in ['button','back']]+[('privacy',None)]
    fixture=declarations('verify_record_controls.py');files=source();rows=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for kind,value in cases:
            width=value[0] if kind=='geometry' else 390
            context=browser.new_context(viewport={'width':width,'height':844},reduced_motion='reduce')
            context.add_init_script(INIT);page=context.new_page();page.set_default_timeout(6500);page.set_default_navigation_timeout(20000)
            errors=[];page.on('pageerror',lambda e:errors.append(str(e)));row=dict(kind=kind,value=value,passed=False,errors=errors)
            try:
                if kind=='geometry':
                    _,w,h=value
                    image='data:image/svg+xml,'+quote(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="pink"/></svg>')
                    seed(page,image);page.wait_for_function('document.querySelector(".photo img")?.naturalWidth>0')
                    before=page.evaluate('({...localStorage})');row['bounds']=bounds(page)
                    if width==390 and w==80:page.screenshot(path=str(out/'390-portrait.png'),full_page=True)
                    contained(row['bounds']);caption=page.locator('.caption');caption.focus();caption.evaluate('e=>e.scrollTop=e.scrollHeight');assert caption.evaluate('e=>e.scrollTop>0')
                    assert page.evaluate('({...localStorage})')==before
                elif kind=='image-retry':
                    count=[0]
                    def serve(route):
                        count[0]+=1
                        if count[0]==1:route.abort()
                        else:route.fulfill(content_type='image/svg+xml',body='<svg xmlns="http://www.w3.org/2000/svg" width="80" height="100"><rect width="80" height="100" fill="pink"/></svg>')
                    page.route('**/photo-bounds-test.svg',serve);seed(page,BASE+'photo-bounds-test.svg');before=page.evaluate('({...localStorage})')
                    retry=page.get_by_role('button',name='重试图片',exact=True);expect(retry).to_be_visible();retry.click();page.wait_for_function('document.querySelector(".photo img")?.naturalWidth>0');expect(retry).to_have_count(0);contained(bounds(page));assert count[0]==2 and page.evaluate('({...localStorage})')==before
                elif kind=='control':fixture['control'](page,'m03-p12',value,value['contract'])
                elif kind=='dirty':fixture['dirty'](page,'m03-p12',value)
                elif kind=='privacy':fixture['privacy'](page,'m03-p12')
                assert not errors;row['passed']=True
            except Exception:row['error']=traceback.format_exc()
            rows.append(row);context.close();assert source()==files
            print(('PASS ' if row['passed'] else 'FAIL ')+kind+' '+str(value),flush=True)
        browser.close()
    report=dict(files=files,script_sha256=sha(Path(__file__)),fixture_script_sha256=sha(ROOT/'verify_record_controls.py'),expected_cases=len(cases),results=rows,accepted_pages=0)
    (out/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
