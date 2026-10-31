"""Resource requirements and owned inventories must agree with the shared pet model."""
import argparse,hashlib,json,re,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
MODES=['default','empty','enough','owned','large']

def dependencies():
    files={'assets/font.ttf','assets/prototype-components.css','assets/book-v2/paper.webp'}
    for n in [13,16]:
        page=f'm07-p{n}';files.update([f'custom/{page}.html',f'pages/{page}.html',f'assets/{page}-art.webp']);files.update('assets/'+v for v in re.findall(r'(?:src|href)="\.\./assets/([^"]+)"',(DEMO/f'pages/{page}.html').read_text(encoding='utf-8')))
    return {n:sha(DEMO/n) for n in sorted(files)}

def prepare(p,f,n,mode):
    f['seed'](p,f'm07-p{n}');p.evaluate('''mode=>{const pet=PrototypePet.read();if(mode==='empty')pet.owned=[];if(mode==='enough')pet.stars=30;if(mode==='large')pet.stars=123456789012;if(mode==='owned'){pet.owned=PrototypePetLife.catalog.filter(v=>v.type==='outfit').map(v=>v.name);pet.ownedRoom=PrototypePetLife.catalog.filter(v=>v.type==='room').map(v=>v.name)}localStorage.setItem('dujia-prototype-pet',JSON.stringify(pet))}''',mode);p.reload();expect(p.locator('.screen')).to_have_attribute('aria-busy','false');p.evaluate('document.fonts.ready')

def check(p,n):
    item_id='crown' if n==13 else 'lamp';values=p.evaluate('id=>{const pet=PrototypePet.read(),L=PrototypePetLife,item=L.find(id);return {pet,item,owned:L.catalog.filter(v=>v.type===item.type&&L.owns(pet,v)),has:L.owns(pet,item)}}',item_id)
    item,pet,owned=values['item'],values['pet'],values['owned'];remaining=p.locator('.remaining');detail=p.locator('.details' if n==13 else '.unlock')
    if values['has']:expect(remaining).to_have_text('已拥有 · 无需再次解锁')
    else:
        expect(remaining).to_contain_text('需要 '+str(item['stars'])+' 星星');expect(remaining).to_contain_text('当前 '+str(pet['stars']));expect(remaining).to_contain_text('还需 '+str(max(0,item['stars']-pet['stars']))+' 星星')
    assert remaining.evaluate('e=>e.scrollWidth<=e.clientWidth+1&&e.scrollHeight<=e.clientHeight+1'),'Requirement text overflows'
    assert detail.evaluate('e=>e.scrollWidth<=e.clientWidth+1&&e.scrollHeight<=e.clientHeight+1'),'Resource explanation overflows'
    assert remaining.evaluate('e=>{const r=e.getBoundingClientRect(),s=document.querySelector(".screen").getBoundingClientRect(),d=document.querySelector(".details,.unlock").getBoundingClientRect();return r.left>=s.left+s.width*.49&&r.right<=s.left+s.width*.94&&r.bottom+1<=d.top}'),'Requirement escapes card or overlaps explanation'
    assert detail.evaluate('e=>{const r=e.getBoundingClientRect(),s=document.querySelector(".screen").getBoundingClientRect(),b=document.querySelector(".task,.cta").getBoundingClientRect();return r.right<=s.left+s.width*.94&&r.bottom+1<=b.top}'),'Explanation overlaps action or escapes card'
    inventory=p.get_by_role('list',name='已拥有的装扮' if n==13 else '已拥有的小屋物品',exact=True);expect(inventory).to_be_visible();expect(inventory.get_by_role('listitem')).to_have_count(len(owned))
    for row,item in zip(inventory.get_by_role('listitem').all(),owned):expect(row).to_contain_text(item['name'])
    expect(p.locator('.owned-title' if n==13 else 'h2.owned')).to_have_text('已拥有 · '+str(len(owned)))
    if not owned:expect(inventory).to_contain_text('还没有装扮')
    else:last=inventory.get_by_role('listitem').last;last.scroll_into_view_if_needed();expect(last).to_be_visible()
    assert inventory.evaluate('e=>e.scrollWidth<=e.clientWidth+1&&getComputedStyle(e).backgroundColor!=="rgba(0, 0, 0, 0)"'),'Inventory must cover misleading baked ownership artwork'
    cta=p.locator('.task' if n==13 else '.cta');expect(cta).to_have_text('返回选择' if values['has'] or pet['stars']>=values['item']['stars'] else '去做任务')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stage',choices=['baseline','current'],required=True);args=ap.parse_args();out=ROOT/f'evidence/{args.stage}/pet-resource-panels';out.mkdir(parents=True,exist_ok=True);assert not (out/'results.json').exists();files=dependencies();f=declarations('verify_pet_controls.py');rows=[]
    cases=[('layout',(n,w,m)) for n in [13,16] for w in [320,390,430] for m in MODES]
    if args.stage=='current':
        catalog=json.loads((ROOT/'evidence/current/page-contracts.json').read_text(encoding='utf-8'));cases += [('control',(r['id'],v)) for r in catalog['pages'] if r['id'] in ['m07-p13','m07-p16'] for v in r['control_evidence']];cases += [('return',(n,m)) for n in [13,16] for m in ['enough','owned']]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for kind,value in cases:
            c=b.new_context(viewport={'width':value[1] if kind=='layout' else 390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));r={'kind':kind,'value':value,'passed':False}
            try:
                if kind=='control':page,v=value;f['control'](p,page,v,v['contract'])
                else:
                    n,mode=(value[0],value[2]) if kind=='layout' else value;prepare(p,f,n,mode);before=f['store'](p)
                    if kind=='return':p.locator('.task' if n==13 else '.cta').click();p.wait_for_url('**/m07-p'+('12' if n==13 else '15')+'.html');assert f['store'](p)==before
                    else:
                        if value[1]==390:p.screenshot(path=str(out/f'm07-p{n}-{mode}.png'),full_page=True)
                        check(p,n);assert f['store'](p)==before
                assert not errors;r['passed']=True
            except Exception:r['failure']=traceback.format_exc()
            r['page_errors']=errors;rows.append(r);c.close();assert dependencies()==files;print(('PASS ' if r['passed'] else 'FAIL ')+kind+' '+str(value),flush=True)
        b.close()
    (out/'results.json').write_text(json.dumps({'dependencies':files,'producer_sha256':sha(Path(__file__)),'fixture_sha256':sha(ROOT/'verify_pet_controls.py'),'browser':version,'results':rows,'scope':'p13 crown/p16 lamp requirements and real owned inventories,3 widths x5 resource/ownership states;original controls and return-to-selection flows. Other selected-item previews, long-name headers, full114 acceptance remain open.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.stage=='baseline':
        (out/'producer.py').write_bytes(Path(__file__).read_bytes())
        for n in files:
            dst=out/'source'/n;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((DEMO/n).read_bytes())
    print(sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
