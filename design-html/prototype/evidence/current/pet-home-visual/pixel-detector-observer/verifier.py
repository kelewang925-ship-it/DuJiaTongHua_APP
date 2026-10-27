"""Pet home text/illustration exclusion bands plus actual initial control regression."""
import argparse,hashlib,json,time,traceback
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from audit_runtime import INIT,OBSERVE
from verify_pet_controls import ROOT,source

MEASURE="""()=>{
 const s=document.querySelector('.screen').getBoundingClientRect(),rect=e=>{const r=e.getBoundingClientRect();return{x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom}},glyph=e=>{const r=document.createRange();r.selectNodeContents(e);const b=r.getBoundingClientRect();return{y:b.y,bottom:b.bottom}};
 return {screen:rect(document.querySelector('.screen')),care:[...document.querySelectorAll('.care')].map(e=>({...rect(e),text:e.textContent,overflow:getComputedStyle(e).overflow})),labels:[...document.querySelectorAll('.actions button')].map(e=>({label:e.textContent,box:rect(e),text:glyph(e)}))};
}"""
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(path,value):
    tmp=path.with_suffix('.tmp');payload=json.dumps(value,ensure_ascii=False,indent=2)+'\n'
    for attempt in range(30):
        try:tmp.write_text(payload,encoding='utf-8');tmp.replace(path);return
        except PermissionError:
            if attempt==29:raise
            time.sleep(.1)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['baseline','current'],required=True);args=parser.parse_args()
    out=ROOT/f'evidence/{args.stage}/pet-home-visual';out.mkdir(exist_ok=True);files=source();fixture=declarations('verify_pet_controls.py');rows=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        def context():
            c=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');c.add_init_script(INIT);return c
        def save():write(out/'results.json',dict(files=files,script_sha256=sha(Path(__file__)),fixture_script_sha256=sha(ROOT/'verify_pet_controls.py'),results=rows,accepted_pages=0,scope='Pet home only: five widths, normal/long care text, illustration exclusion bands and initial controls; not original design human acceptance'))
        for width in [320,360,390,414,430]:
            for long in [False,True]:
                c=context();p=c.new_page();p.set_viewport_size({'width':width,'height':844});p.set_default_timeout(6500);p.set_default_navigation_timeout(20000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
                row=dict(kind='layout',width=width,long=long,passed=False,errors=errors)
                try:
                    fixture['seed'](p,'m07-p03')
                    if long:
                        p.evaluate('()=>{const k="dujia-prototype-pet",pet=JSON.parse(localStorage.getItem(k));pet.logs=[{id:"long-note",type:"note",text:"今天的小心情".repeat(70),actor:"小满",date:"2026-10-06",at:Date.now(),story:true},...pet.logs];localStorage.setItem(k,JSON.stringify(pet))}');p.reload();expect(p.locator('.screen')).to_have_attribute('aria-busy','false')
                    before=p.evaluate('JSON.stringify({...localStorage})');geo=p.evaluate(MEASURE);row['geometry']=geo
                    p.screenshot(path=str(out/f'{width}-{"long" if long else "normal"}.png'),full_page=True)
                    screen=geo['screen'];left,right=geo['care']
                    # Artwork measurement: peer avatar occupies about 52%-65% width.
                    # Labels belong below icon artwork, around source y1470/1825.
                    assert left['right']<=screen['x']+.505*screen['width'],'Care text enters peer avatar band'
                    assert right['right']<=screen['x']+.955*screen['width'],'Care text exits its paper card'
                    for care in [left,right]:assert care['bottom']<=screen['y']+.715*screen['height'],'Care text exits care card vertically'
                    for label in geo['labels']:
                        assert label['text']['y']>=screen['y']+.805*screen['height'],'Action label overlaps illustration: '+label['label']
                        assert label['text']['bottom']<=screen['y']+.84*screen['height'],'Action label exits card: '+label['label']
                    image=Image.open(out/f'{width}-{"long" if long else "normal"}.png').convert('RGB')
                    region=(round(screen['x']+.42*screen['width']),round(screen['y']+.65*screen['height']),round(screen['x']+.465*screen['width']),round(screen['y']+.69*screen['height']))
                    blue=sum(b>r+15 and b>g+3 for r,g,b in image.crop(region).get_flattened_data())
                    row['care_blue_icon_pixels']=blue;assert blue<=2,'Decorative water icon crosses live care text'
                    if long:assert '今天的小心情'*70 in left['text'] and len(left['text'])>400
                    assert p.evaluate('JSON.stringify({...localStorage})')==before and not errors;row['passed']=True
                except Exception:row['error']=traceback.format_exc()
                rows.append(row);c.close();assert source()==files;save();print(('PASS ' if row['passed'] else 'FAIL ')+str(width)+' '+str(long),flush=True)
        c=context();p=c.new_page();fixture['seed'](p,'m07-p03');controls=[v for v in p.evaluate(OBSERVE)['controls'] if v['visible'] and not v['disabled']];c.close()
        for v in controls:
            c=context();p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(kind='control',label=v['label'],selector=v['selector'],passed=False,errors=errors)
            try:
                kind=fixture['contract']('m07-p03',v);fixture['control'](p,'m07-p03',v,kind);assert not errors;row.update(contract=kind,passed=True)
            except Exception:row['error']=traceback.format_exc()
            rows.append(row);c.close();assert source()==files;save();print(('PASS ' if row['passed'] else 'FAIL ')+v['label'],flush=True)
        browser.close()
    print(json.dumps(dict(cases=len(rows),passed=sum(r['passed'] for r in rows))))
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
if __name__=='__main__':main()
