"""Real stored dates across one to seven digits, with original countdown actions."""
import argparse,hashlib,json,traceback
from datetime import date,timedelta
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from audit_runtime import INIT
from audit_hidden_overlays import declarations
from verify_pet_controls import ROOT,BASE,source

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def seed(p,days):
    values=data(True);item=dict(id='countdown-fit',name='完整天数与日历区域验证'*8,date=(date(2026,10,5)+timedelta(days=days)).isoformat(),repeat=False,enabled=True,reminderDays=3)
    values['dujia-prototype-anniversaries']=[item]
    p.goto(BASE+'prototype/review.html');p.evaluate('d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-05");for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',values)
    p.goto(BASE+'pages/m04-p10.html?id=countdown-fit');p.evaluate('document.fonts.ready')

def geometry(p,days):
    expect(p.locator('.number')).to_have_text(str(abs(days)));expect(p.locator('.still')).to_have_text('还有' if days>0 else '已经过')
    boxes=p.evaluate('''()=>Object.fromEntries(['.screen','.number','.days','.date'].map(s=>{let r=document.querySelector(s).getBoundingClientRect();return[s,{left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height}]}))''')
    s,n,u,d=[boxes[k] for k in ['.screen','.number','.days','.date']]
    assert n['right']+2<=u['left'],boxes
    assert n['left']>=s['left']+.2*s['width'] and u['right']<=s['left']+.8*s['width'],boxes
    assert max(n['bottom'],u['bottom'])<=d['top'],boxes
    assert p.locator('.number').evaluate('e=>e.scrollWidth<=e.clientWidth+1')
    return boxes

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['baseline','current'],required=True);args=parser.parse_args()
    out=ROOT/f'evidence/{args.stage}/countdown-value-layout';out.mkdir(parents=True,exist_ok=True)
    cases=[('geometry',(width,days)) for width in [320,360,390,414,430] for days in [1,80,365,3650,36500,365000,2000000,-36500]]
    fixture=declarations('verify_time_controls.py')
    if args.stage=='current':
        catalog=json.loads((ROOT/'evidence/current/page-contracts.json').read_text(encoding='utf-8'))
        controls=next(r for r in catalog['pages'] if r['id']=='m04-p10')['control_evidence'];assert len(controls)==5
        cases += [('control',c) for c in controls]+[('resize',2000000),('today',0)]
    files=source();rows=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=browser.version
        for kind,value in cases:
            context=browser.new_context(viewport={'width':value[0] if kind=='geometry' else 390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');context.add_init_script(INIT)
            p=context.new_page();p.set_default_timeout(6500);p.set_default_navigation_timeout(20000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(kind=kind,value=value,passed=False,errors=errors)
            try:
                if kind in ['geometry','resize']:
                    days=value[1] if kind=='geometry' else value;seed(p,days);before=p.evaluate('({...localStorage})');row['bounds']=geometry(p,days)
                    if kind=='geometry' and value[0]==390 and days in [1,80,3650,2000000]:p.screenshot(path=str(out/f'390-{days}.png'),full_page=True)
                    if kind=='resize':
                        for width in [320,430,360]:p.set_viewport_size({'width':width,'height':844});geometry(p,days)
                    assert p.evaluate('({...localStorage})')==before
                elif kind=='control':fixture['control'](p,'m04-p10',value,value['contract'])
                else:
                    seed(p,0);p.wait_for_url('**/m04-p11.html*');expect(p.locator('.actions')).to_be_visible();expect(p.locator('.date')).to_have_text('2026-10-05')
                assert not errors;row['passed']=True
            except Exception:row['error']=traceback.format_exc()
            rows.append(row);context.close();assert source()==files;print(('PASS ' if row['passed'] else 'FAIL ')+kind+' '+str(value),flush=True)
        browser.close()
    (out/'results.json').write_text(json.dumps(dict(files=files,script_sha256=sha(Path(__file__)),fixture_script_sha256=sha(ROOT/'verify_time_controls.py'),browser=version,locale='zh-CN',timezone='Asia/Shanghai',dpr=1,height=844,reduced_motion='reduce',expected_cases=len(cases),results=rows,accepted_pages=0),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
if __name__=='__main__':main()
