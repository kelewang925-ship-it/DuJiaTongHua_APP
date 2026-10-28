"""Pet rest heading follows real renamed pet data, independently of book edits."""
import argparse,hashlib,json,re,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from audit_runtime import INIT
from verify_pet_controls import ROOT,DEMO

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dependencies():
    html=(DEMO/'custom/m07-p07.html').read_text(encoding='utf-8')
    files={'custom/m07-p07.html','pages/m07-p07.html','assets/ui-foundation.css','assets/font.ttf','assets/m07-p07-art.webp'}
    files|={'assets/'+p for p in re.findall(r'(?:src|href)="\.\./assets/(prototype-[^"]+)"',html)}
    return {p:sha(DEMO/p) for p in sorted(files)}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['baseline','current'],required=True);args=parser.parse_args()
    out=ROOT/f'evidence/{args.stage}/pet-rest-name';out.mkdir(parents=True,exist_ok=True);fixture=declarations('verify_pet_controls.py')
    cases=[('name',(width,name)) for width in [320,360,390,414,430] for name in ['奶糖','Nomi','一二三四五六七八九十甲乙']]
    if args.stage=='current':
        catalog=json.loads((ROOT/'evidence/current/page-contracts.json').read_text(encoding='utf-8'));controls=next(r for r in catalog['pages'] if r['id']=='m07-p07')['control_evidence'];assert len(controls)==3
        cases += [('control',v) for v in controls]
        cases += [('shared-name',f'm07-p{n:02d}') for n in range(1,12)]
    files=dependencies();rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for kind,value in cases:
            context=b.new_context(viewport={'width':value[0] if kind=='name' else 390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');context.add_init_script(INIT)
            p=context.new_page();p.set_default_timeout(6500);p.set_default_navigation_timeout(20000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(kind=kind,value=value,passed=False,errors=errors)
            try:
                if kind=='name':
                    width,name=value;fixture['seed'](p,'m07-p07')
                    p.evaluate('name=>{const p=JSON.parse(localStorage.getItem("dujia-prototype-pet"));p.name=name;localStorage.setItem("dujia-prototype-pet",JSON.stringify(p))}',name)
                    p.reload();expect(p.locator('.screen')).to_have_attribute('aria-busy','false');expect(p.locator('.pet-load')).to_have_count(0);p.evaluate('document.fonts.ready');before=p.evaluate('({...localStorage})')
                    row['actual_title']=p.locator('.sleep-title').inner_text()
                    if width==390:p.screenshot(path=str(out/('390-'+('long' if len(name)==12 else name)+'.png')),full_page=True)
                    expect(p.locator('.sleep-title')).to_have_text(name+'想先睡一会儿');expect(p.locator('.energy-note')).to_contain_text(name)
                    expect(p.locator('.art-top')).to_have_attribute('aria-label',name+'在软垫上睡觉')
                    boxes=p.evaluate('''()=>Object.fromEntries(['.screen','.sleep-title','.sleep-copy','.disabled-title'].map(s=>{const r=document.querySelector(s).getBoundingClientRect();return[s,{left:r.left,right:r.right,top:r.top,bottom:r.bottom}]}))''');row['bounds']=boxes
                    s,h,c,d=[boxes[k] for k in ['.screen','.sleep-title','.sleep-copy','.disabled-title']]
                    assert h['left']>=s['left'] and h['right']<=s['right'] and h['bottom']+2<=c['top'] and c['bottom']+2<=d['top'],boxes
                    header=p.locator('.title').bounding_box();banner=p.locator('.banner').bounding_box();note=p.locator('.energy-note').bounding_box();rest=p.locator('.rest-message').bounding_box()
                    assert header['y']+header['height']+2<=banner['y'] and header['x']+header['width']<=width,header
                    assert note['x']+note['width']<=width and note['y']+note['height']+4<=rest['y'],note
                    for selector in ['.title','.energy-note']:assert p.locator(selector).evaluate('e=>e.scrollHeight<=e.clientHeight+1 && e.scrollWidth<=e.clientWidth+1')
                    assert p.evaluate('({...localStorage})')==before
                elif kind=='shared-name':
                    fixture['seed'](p,value)
                    p.evaluate('()=>{const pet=JSON.parse(localStorage.getItem("dujia-prototype-pet"));pet.name="奶糖";localStorage.setItem("dujia-prototype-pet",JSON.stringify(pet))}')
                    p.reload();expect(p.locator('.screen')).to_have_attribute('aria-busy','false');expect(p.locator('.pet-load')).to_have_count(0)
                    assert value+'.html' in p.url
                    row['h2_texts']=p.locator('h2').all_text_contents()
                    assert all('糯米' not in t for t in row['h2_texts']),row['h2_texts']
                else:fixture['control'](p,'m07-p07',value,value['contract'])
                assert not errors;row['passed']=True
            except Exception:row['error']=traceback.format_exc()
            rows.append(row);context.close();assert dependencies()==files;print(('PASS ' if row['passed'] else 'FAIL ')+kind+' '+str(value),flush=True)
        b.close()
    (out/'results.json').write_text(json.dumps(dict(dependency_files=files,scope='Pet rest page and direct dependencies only;unrelated concurrent book changes excluded. No full114 replay claim.',script_sha256=sha(Path(__file__)),fixture_script_sha256=sha(ROOT/'verify_pet_controls.py'),browser=version,locale='zh-CN',timezone='Asia/Shanghai',dpr=1,expected_cases=len(cases),results=rows,accepted_pages=0),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
if __name__=='__main__':main()
