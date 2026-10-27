"""Real local-byte labels must stay above the painted meter, with original actions."""
import argparse,hashlib,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from audit_runtime import INIT
from verify_pet_controls import ROOT,source

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['baseline','current'],required=True);args=parser.parse_args()
    out=ROOT/f'evidence/{args.stage}/storage-quantity-layout';out.mkdir(parents=True,exist_ok=True);fixture=declarations('verify_settings_controls.py')
    cases=[('geometry',(width,size)) for width in [320,360,390,414,430] for size in [0,300000,1500000]]
    if args.stage=='current':
        catalog=json.loads((ROOT/'evidence/current/page-contracts.json').read_text(encoding='utf-8'));controls=next(r for r in catalog['pages'] if r['id']=='m06-p11')['control_evidence'];assert len(controls)==6
        cases += [('control',c) for c in controls]
    files=source();rows=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=browser.version
        for kind,value in cases:
            context=browser.new_context(viewport={'width':value[0] if kind=='geometry' else 390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai',accept_downloads=True);context.add_init_script(INIT)
            page=context.new_page();page.set_default_timeout(6500);page.set_default_navigation_timeout(20000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));row=dict(kind=kind,value=value,passed=False,errors=errors)
            try:
                if kind=='geometry':
                    width,size=value;fixture['seed'](page,'m06-p11')
                    if size:page.evaluate('n=>localStorage.setItem("dujia-layout-probe","x".repeat(n))',size);page.reload();page.evaluate('document.fonts.ready')
                    before=page.evaluate('({...localStorage})');expect(page.locator('.quantity small')).to_have_text('本地演示数据')
                    exact=page.evaluate('()=>{const n=PrototypePreferences.bytes();return n<1048576?(n/1024).toFixed(1)+" KB":(n/1048576).toFixed(1)+" MB"}')
                    assert page.locator('.quantity').evaluate('e=>e.firstChild.textContent')==exact
                    boxes=page.evaluate('''()=>Object.fromEntries(['.screen','.used','.quantity','.quantity small'].map(s=>{const r=document.querySelector(s).getBoundingClientRect();return[s,{left:r.left,right:r.right,top:r.top,bottom:r.bottom,height:r.height}]}))''')
                    s,u,q,n=[boxes[k] for k in ['.screen','.used','.quantity','.quantity small']];row.update(bounds=boxes,formatted_bytes=exact,reserved_meter_top_ratio=.52)
                    if width==390 and size in [0,1500000]:page.screenshot(path=str(out/f'390-{size}.png'),full_page=True)
                    # The original painted track begins at roughly52% of the artboard.
                    # Reserve half a percent above it; no text may enter this band.
                    assert max(q['bottom'],n['bottom'])<=s['top']+.515*s['height'],boxes
                    assert q['top']>=u['bottom']+2 and n['top']>=q['top']-1 and n['bottom']<=q['bottom']+1,boxes
                    assert q['left']>=s['left'] and q['right']<=s['right'] and n['right']<=s['right']-.04*value[0],boxes
                    assert page.evaluate('({...localStorage})')==before
                else:fixture['control'](page,'m06-p11',value,value['contract'])
                assert not errors;row['passed']=True
            except Exception:row['error']=traceback.format_exc()
            rows.append(row);context.close();assert source()==files;print(('PASS ' if row['passed'] else 'FAIL ')+kind+' '+str(value),flush=True)
        browser.close()
    (out/'results.json').write_text(json.dumps(dict(files=files,script_sha256=sha(Path(__file__)),fixture_script_sha256=sha(ROOT/'verify_settings_controls.py'),browser=version,locale='zh-CN',timezone='Asia/Shanghai',dpr=1,height=844,reduced_motion='reduce',expected_cases=len(cases),results=rows,accepted_pages=0),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
if __name__=='__main__':main()
