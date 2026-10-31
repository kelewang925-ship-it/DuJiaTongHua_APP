"""Collection count, breed action and full pet title must occupy separate regions."""
import argparse,hashlib,json,re,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations

ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
NAMES=['团团','一二三四五六七八九十甲乙','MochiWWWWWWW']

def dependencies():
    files={'custom/m07-p22.html','pages/m07-p22.html','assets/m07-p22-art.webp','assets/font.ttf'}
    files.update('assets/'+v for v in re.findall(r'(?:src|href)="\.\./assets/([^"]+)"',(DEMO/'pages/m07-p22.html').read_text(encoding='utf-8')))
    return {n:sha(DEMO/n) for n in sorted(files)}

def geometry(p):
    return p.evaluate('''()=>{const sels=['.title','.count','.pet-life-extra','.subtitle','.tabs','.pet-back'];return Object.fromEntries(sels.map(s=>{const e=document.querySelector(s),r=e.getBoundingClientRect();return [s,{x:r.x,y:r.y,w:r.width,h:r.height,fit:e.scrollWidth<=e.clientWidth+1&&e.scrollHeight<=e.clientHeight+1}]}))}''')

def overlap(a,b):return min(a['x']+a['w'],b['x']+b['w'])>max(a['x'],b['x'])+.5 and min(a['y']+a['h'],b['y']+b['h'])>max(a['y'],b['y'])+.5

def layout(p,name):
    g=geometry(p)
    for a,b in [('.count','.pet-life-extra'),('.title','.count'),('.title','.pet-life-extra'),('.title','.pet-back'),('.title','.subtitle'),('.pet-life-extra','.tabs')]:assert not overlap(g[a],g[b]),f'{a} overlaps {b}: {g[a]} / {g[b]}'
    for s in ['.title','.count','.pet-life-extra']:assert g[s]['fit'],s+' clips full text'
    assert ''.join(p.locator('.title').inner_text().split())==name+'的收藏图鉴'
    assert g['.pet-life-extra']['h']>=44 and g['.pet-life-extra']['w']>=44
    count=p.evaluate('()=>{const pet=PrototypePet.read(),l=PrototypePetLife;return [l.catalog.filter(v=>l.owns(pet,v)).length+l.achievements(pet).filter(v=>v.claimed).length,l.catalog.length+l.achievements(pet).length]}')
    assert p.locator('.count').inner_text()=='已收藏 '+str(count[0])+' / '+str(count[1])
    return g

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stage',choices=['baseline','current'],required=True);args=ap.parse_args();out=ROOT/f'evidence/{args.stage}/pet-collection-header';out.mkdir(parents=True,exist_ok=True);assert not (out/'results.json').exists()
    files=dependencies();fixture=declarations('verify_pet_controls.py');rows=[]
    cases=[('layout',(w,n)) for w in [320,360,390,414,430] for n in NAMES]
    if args.stage=='current':
        catalog=json.loads((ROOT/'evidence/current/page-contracts.json').read_text(encoding='utf-8'))
        cases += [('control',v) for r in catalog['pages'] if r['id']=='m07-p22' for v in r['control_evidence']]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=browser.version
        for kind,value in cases:
            c=browser.new_context(viewport={'width':value[0] if kind=='layout' else 390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));r={'kind':kind,'value':value,'passed':False}
            try:
                if kind=='control':fixture['control'](p,'m07-p22',value,value['contract'])
                else:
                    width,name=value;fixture['seed'](p,'m07-p22');p.evaluate('name=>{const pet=PrototypePet.read();pet.name=name;localStorage.setItem("dujia-prototype-pet",JSON.stringify(pet))}',name);p.reload();expect(p.locator('.screen')).to_have_attribute('aria-busy','false');expect(p.locator('.pet-load')).to_have_count(0);p.evaluate('document.fonts.ready');before=fixture['store'](p)
                    if width in [320,390]:p.screenshot(path=str(out/f'{width}-{NAMES.index(name)}.png'),full_page=True)
                    r['geometry']=layout(p,name);assert fixture['store'](p)==before
                assert not errors;r['passed']=True
            except Exception:r['failure']=traceback.format_exc()
            r['page_errors']=errors;rows.append(r);c.close();assert dependencies()==files;print(('PASS ' if r['passed'] else 'FAIL ')+kind+' '+str(value),flush=True)
        browser.close()
    (out/'results.json').write_text(json.dumps({'dependencies':files,'producer_sha256':sha(Path(__file__)),'fixture_sha256':sha(ROOT/'verify_pet_controls.py'),'browser':version,'scope':'p22 count/action/title at five widths with short and full long names; initial controls only in current run. Not full catalog skin, other inline issues or 114-page acceptance.','results':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.stage=='baseline':
        (out/'producer.py').write_bytes(Path(__file__).read_bytes())
        for n in files:
            dst=out/'source'/n;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((DEMO/n).read_bytes())
    print(sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
