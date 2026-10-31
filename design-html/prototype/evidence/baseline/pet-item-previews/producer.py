"""Current item illustration and ownership state must follow the existing catalog."""
import argparse,hashlib,json,re,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
OUTFITS=['scarf','bow','star-bow','peach-hat','crown','cape','vest','bell']
ROOM=['flower-rug','plaid-rug','moon-rug','picnic-rug','wood-bed','cream-bed','flower-wall','frame-wall','vase','lamp']

def dependencies():
    files={'assets/font.ttf','assets/prototype-components.css','assets/book-v2/paper.webp'}
    for n in [13,16,12,15]:
        page=f'm07-p{n}';files.add(f'pages/{page}.html');files.update('assets/'+v for v in re.findall(r'(?:src|href)="\.\./assets/([^"]+)"',(DEMO/f'pages/{page}.html').read_text(encoding='utf-8')))
    for n in [13,16]:files.update([f'custom/m07-p{n}.html',f'assets/m07-p{n}-art.webp'])
    return {n:sha(DEMO/n) for n in sorted(files)}

def prepare(p,f,id,mode):
    n=13 if id in OUTFITS else 16;f['seed'](p,f'm07-p{n}');p.evaluate('''mode=>{const pet=PrototypePet.read(),L=PrototypePetLife;pet.logs=[];pet.coins=mode==='ready'?999:0;pet.stars=mode==='ready'?999:0;pet.affinity=0;pet.owned=mode==='owned'?L.catalog.filter(v=>v.type==='outfit').map(v=>v.name):[];pet.ownedRoom=mode==='owned'?L.catalog.filter(v=>v.type==='room').map(v=>v.name):[];localStorage.setItem('dujia-prototype-pet',JSON.stringify(pet))}''',mode);p.goto(f'http://127.0.0.1:8765/pages/m07-p{n}.html?item='+id);expect(p.locator('.screen')).to_have_attribute('aria-busy','false');p.evaluate('document.fonts.ready')

def check(p,id):
    value=p.evaluate('id=>{const L=PrototypePetLife,pet=PrototypePet.read(),item=L.find(id);return {item,state:L.owns(pet,item)?"已拥有":L.allowed(pet,item)&&pet.coins>=(item.coins||0)&&pet.stars>=(item.stars||0)?"可解锁":"未解锁"}}',id);item,state=value['item'],value['state'];name=item['name']+' · '+state+' · 物品示意';image=p.get_by_role('img',name=name,exact=True)
    assert image.count()==1,'No labeled current-item preview; source uses a fixed illustration'
    expect(image).to_be_visible();assert image.evaluate('e=>e.tagName.toLowerCase()==="svg"&&e.querySelectorAll("path,circle,ellipse,rect").length>1'),'Item preview must be editable vector content'
    expect(p.locator('.pet-item-state')).to_have_text(state)
    assert p.locator('.pet-item-preview').evaluate('e=>{const r=e.getBoundingClientRect(),s=document.querySelector(".screen").getBoundingClientRect(),i=e.querySelector("svg").getBoundingClientRect();return e.scrollWidth<=e.clientWidth+1&&e.scrollHeight<=e.clientHeight+1&&i.left>=r.left&&i.right<=r.right&&i.top>=r.top&&i.bottom<=r.bottom&&r.left>=s.left+s.width*.05&&r.right<=s.right-s.width*.05}'),'Preview content escapes source card'
    expect(p.locator('.crown' if id in OUTFITS else '.item')).to_have_text(item['name'])
    assert p.locator('.pet-item-preview').get_by_role('button').count()==0
    if id not in OUTFITS:expect(p.locator('.pet-room-art-caption')).to_have_text('小屋氛围示意 · 所选物品见下方');expect(p.locator('.stars')).to_be_hidden()
    return value

def flow(p,f,id):
    prepare(p,f,id,'ready');check(p,id);n=13 if id in OUTFITS else 16;p.locator('.task' if n==13 else '.cta').click();p.wait_for_url('**/m07-p'+('12' if n==13 else '15')+'.html')
    if n==16:p.locator('[data-tab="摆件"]').click()
    button=p.locator('[data-item="'+id+'"]');button.click();p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","pet-unlock")');p.get_by_role('button',name='解锁并选择',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert p.evaluate('PrototypePet.read().'+('coins' if n==13 else 'stars'))==999;button.click();p.get_by_role('button',name='解锁并选择',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('已解锁');assert p.evaluate('PrototypePet.read().'+('coins' if n==13 else 'stars'))==979;p.goto(f'http://127.0.0.1:8765/pages/m07-p{n}.html?item='+id);expect(p.locator('.screen')).to_have_attribute('aria-busy','false');check(p,id);expect(p.locator('.pet-item-state')).to_have_text('已拥有');before=f['store'](p);p.reload();expect(p.locator('.screen')).to_have_attribute('aria-busy','false');check(p,id);assert f['store'](p)==before

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stage',choices=['baseline','current'],required=True);args=ap.parse_args();out=ROOT/f'evidence/{args.stage}/pet-item-previews';out.mkdir(parents=True,exist_ok=True);assert not (out/'results.json').exists();files=dependencies();f=declarations('verify_pet_controls.py');rows=[]
    cases=[('layout',(id,390,mode)) for id,mode in [('crown','owned'),('bow','blocked'),('lamp','owned'),('wood-bed','blocked')]]
    if args.stage=='current':
        cases=[('layout',(id,390,mode)) for id in OUTFITS+ROOM for mode in ['blocked','owned']]+[('layout',(id,w,'ready')) for id in ['crown','lamp'] for w in [320,390,430]]+[('layout',(id,w,mode)) for id in ['crown','lamp'] for w in [320,430] for mode in ['blocked','owned']]
        catalog=json.loads((ROOT/'evidence/current/page-contracts.json').read_text(encoding='utf-8'));cases += [('control',(r['id'],v)) for r in catalog['pages'] if r['id'] in ['m07-p13','m07-p16'] for v in r['control_evidence']];cases += [('flow',id) for id in ['bow','lamp']]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for kind,value in cases:
            c=b.new_context(viewport={'width':value[1] if kind=='layout' else 390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));r={'kind':kind,'value':value,'passed':False}
            try:
                if kind=='control':page,v=value;f['control'](p,page,v,v['contract'])
                elif kind=='flow':flow(p,f,value)
                else:
                    id,width,mode=value;prepare(p,f,id,mode);before=f['store'](p)
                    if width==390 and (mode=='blocked' or id in ['crown','lamp']):p.screenshot(path=str(out/f'{id}-{mode}.png'),full_page=True)
                    r['model']=check(p,id);assert f['store'](p)==before
                assert not errors;r['passed']=True
            except Exception:r['failure']=traceback.format_exc()
            r['page_errors']=errors;rows.append(r);c.close();assert dependencies()==files;print(('PASS ' if r['passed'] else 'FAIL ')+kind+' '+str(value),flush=True)
        b.close()
    (out/'results.json').write_text(json.dumps({'dependencies':files,'producer_sha256':sha(Path(__file__)),'fixture_sha256':sha(ROOT/'verify_pet_controls.py'),'browser':version,'results':rows,'scope':'p13/p16 all18 selected-item vector previews and actual unlock/ownership labels,50 layouts,4 original controls,2 real unlock failure/retry flows. Room hero explicitly decorative; p12/p15 full previews and full114 acceptance remain open.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.stage=='baseline':
        (out/'producer.py').write_bytes(Path(__file__).read_bytes())
        for n in files:
            dst=out/'source'/n;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((DEMO/n).read_bytes())
    print(sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
