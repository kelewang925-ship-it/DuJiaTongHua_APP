"""Draft visualization follows real selections, writes only on the existing save actions."""
import argparse,json,re,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from verify_pet_item_previews import sha,ROOT,DEMO,OUTFITS,ROOM,prepare as item_prepare,check as item_check
BASE='http://127.0.0.1:8765/pages/'

def dependencies():
    files={'assets/font.ttf','assets/book-v2/paper.webp','assets/prototype-components.css'}
    for n in [12,15,13,16]:
        name=f'm07-p{n}';files.update([f'pages/{name}.html',f'custom/{name}.html',f'assets/{name}-art.webp'])
        files.update('assets/'+v for v in re.findall(r'(?:src|href)="\.\./assets/([^"]+)"',(DEMO/f'pages/{name}.html').read_text(encoding='utf-8')))
    return {n:sha(DEMO/n) for n in sorted(files)}

def prepare(p,f,n,kind='小狗'):
    f['seed'](p,f'm07-p{n}');p.evaluate('''kind=>{const pet=PrototypePet.read(),L=PrototypePetLife;pet.kind=kind;pet.outfit=null;pet.room={};pet.owned=L.catalog.filter(v=>v.type==='outfit').map(v=>v.name);pet.ownedRoom=L.catalog.filter(v=>v.type==='room').map(v=>v.name);localStorage.setItem(PrototypePet.key,JSON.stringify(pet));}''',kind);p.reload();expect(p.locator('.screen')).to_have_attribute('aria-busy','false');p.evaluate('document.fonts.ready')

def select(p,id):
    item=p.evaluate('id=>PrototypePetLife.find(id)',id)
    p.locator('[data-tab="'+item['group']+'"]' if item['type']=='room' else '.tabs button').filter(has_text=item['group']).click()
    p.locator('button[data-item="'+id+'"]').click()
    return item

def check(p,n,selected=None,room=None):
    if n==12:
        kind=p.evaluate('PrototypePet.read().kind');label=kind+' · 试穿：'+(selected or '不佩戴')+' · 示意图';image=p.get_by_role('img',name=label,exact=True)
    else:
        room=room or p.evaluate('PrototypePetLife.room(PrototypePet.read())');label='小屋布置预览 · '+'、'.join(room.values())+' · 示意图';image=p.get_by_role('img',name=label,exact=True)
    assert image.count()==1,'No visual preview for the actual draft selection'
    expect(image).to_be_visible();assert image.evaluate('e=>e.tagName.toLowerCase()==="svg"')
    ids=image.locator('[data-preview-item]').evaluate_all('es=>es.map(e=>e.dataset.previewItem)')
    wanted=p.evaluate('names=>PrototypePetLife.catalog.filter(v=>names.includes(v.name)).map(v=>v.id)',[selected] if n==12 else list(room.values()))
    assert set(ids)==set(wanted),(ids,wanted)
    panel=p.locator('.pet-draft-preview');assert panel.get_by_role('button').count()==0
    assert panel.evaluate('e=>{const r=e.getBoundingClientRect(),s=document.querySelector(".screen").getBoundingClientRect(),i=e.querySelector("svg").getBoundingClientRect(),tabs=document.querySelector(".tabs").getBoundingClientRect(),list=document.querySelector(".item-list,.cards").getBoundingClientRect();return e.scrollWidth<=e.clientWidth+1&&e.scrollHeight<=e.clientHeight+1&&i.left>=r.left&&i.right<=r.right&&i.bottom<=r.bottom&&r.left>=s.left&&r.right<=s.right&&(r.bottom<=tabs.top+1||r.top>=tabs.bottom-1)&&r.bottom<=list.top}')
    return label

def saved_flow(p,f,n):
    prepare(p,f,n);before=f['store'](p);item=select(p,'bow' if n==12 else 'cream-bed');room=p.evaluate('PrototypePetLife.room(PrototypePet.read())')
    if n==15:room['小床']=item['name']
    check(p,n,item['name'],room);assert f['store'](p)==before
    p.evaluate('n=>sessionStorage.setItem("dujia-prototype-fail-next",n===12?"pet-outfit":"pet-room")',n);p.locator('#save' if n==12 else '.save').click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert f['store'](p)==before;check(p,n,item['name'],room)
    p.locator('#save' if n==12 else '.save').click()
    if n==12:expect(p.locator('.prototype-toast')).to_contain_text('穿戴已保存')
    else:p.wait_for_url('**/m07-p14.html*')
    pet=p.evaluate('PrototypePet.read()');assert (pet['outfit']==item['name'] if n==12 else pet['room']==room)
    logs=sum(v['type']==('outfit' if n==12 else 'room') for v in pet['logs']);assert logs==1
    p.goto(BASE+f'm07-p{n}.html');expect(p.locator('.screen')).to_have_attribute('aria-busy','false');check(p,n,item['name'],room)

def dirty_flow(p,f,n):
    prepare(p,f,n);before=f['store'](p);item=select(p,'bow' if n==12 else 'cream-bed');room=p.evaluate('PrototypePetLife.room(PrototypePet.read())')
    if n==15:room['小床']=item['name']
    p.locator('.back' if n==12 else '.pet-back').click();p.get_by_role('button',name='继续编辑',exact=True).click();check(p,n,item['name'],room);assert f['store'](p)==before
    p.locator('.back' if n==12 else '.pet-back').click();p.get_by_role('button',name='放弃修改',exact=True).click();p.wait_for_url('**/m07-p03.html');assert f['store'](p)==before

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stage',required=True,choices=['baseline','current']);args=ap.parse_args();out=ROOT/f'evidence/{args.stage}/pet-draft-previews';out.mkdir(parents=True,exist_ok=True);assert not (out/'results.json').exists();deps=dependencies();f=declarations('verify_pet_controls.py')
    cases=[('layout',(12,390,'none')),('layout',(12,390,'bow')),('layout',(15,390,'flower-rug')),('layout',(15,390,'cream-bed'))]
    if args.stage=='current':
        cases=[('layout',(12,w,id)) for w in [320,390,430] for id in ['none']+OUTFITS]+[('layout',(15,w,id)) for w in [320,390,430] for id in ROOM]+[('kind',kind) for kind in ['小狗','小猫','小兔','小狐狸']]+[('save',n) for n in [12,15]]+[('dirty',n) for n in [12,15]]+[('resource',id) for id in ['bow','crown','wood-bed','lamp']]
    rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for kind,value in cases:
            c=b.new_context(viewport={'width':value[1] if kind=='layout' else 390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row={'kind':kind,'value':value,'passed':False}
            try:
                if kind=='save':saved_flow(p,f,value)
                elif kind=='dirty':dirty_flow(p,f,value)
                elif kind=='resource':item_prepare(p,f,value,'owned');item_check(p,value)
                else:
                    n,width,id=value if kind=='layout' else (12,390,'crown');prepare(p,f,n,value if kind=='kind' else '小狗');before=f['store'](p);room=p.evaluate('PrototypePetLife.room(PrototypePet.read())');item=select(p,id) if id!='none' else None
                    if n==15:room[item['group']]=item['name']
                    if width==390:p.screenshot(path=str(out/f'{n}-{id}-{value if kind=="kind" else "layout"}.png'),full_page=True)
                    row['label']=check(p,n,item['name'] if item else None,room);assert f['store'](p)==before
                assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc()
            row['page_errors']=errors;rows.append(row);c.close();assert dependencies()==deps;print(('PASS ' if row['passed'] else 'FAIL ')+kind+' '+str(value),flush=True)
        b.close()
    (out/'results.json').write_text(json.dumps({'dependencies':deps,'producer_sha256':sha(Path(__file__)),'fixture_sha256':sha(ROOT/'verify_pet_controls.py'),'browser':version,'results':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.stage=='baseline':
        (out/'producer.py').write_bytes(Path(__file__).read_bytes())
        for n in deps:
            dst=out/'source'/n;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((DEMO/n).read_bytes())
    print(sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
