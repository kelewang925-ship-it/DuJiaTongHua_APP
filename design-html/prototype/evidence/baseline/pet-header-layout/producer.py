"""Full-length pet/owner captions must avoid artwork, controls and following sections."""
import argparse,hashlib,json,re,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations

ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
NAMES=[{'pet':'奶糖','actor':'鹿鹿','peer':'星野'}, {'pet':'一二三四五六七八九十甲乙','actor':'一二三四五六七八九十甲乙丙丁戊己庚辛壬癸','peer':'甲乙丙丁戊己庚辛壬癸一二三四五六七八九十'}, {'pet':'MochiWWWWWWW','actor':'W'*20,'peer':'abcdefghijklmnopqrst'}, {'pet':'奶糖小满阿舟星星伙伴团团','actor':'阿舟小满糯米星野伙伴奶糖鹿鹿童话日记','peer':'糯米阿舟小满奶糖伙伴星野鹿鹿日记童话'}]
assert all(len(n['pet'])<=12 and len(n['actor'])<=20 and len(n['peer'])<=20 for n in NAMES)

def dependencies():
    files={'assets/font.ttf','assets/prototype-components.css','assets/book-v2/paper.webp'}
    for page in ['m07-p11','m07-p25']:
        files.update([f'custom/{page}.html',f'pages/{page}.html',f'assets/{page}-art.webp']);text=(DEMO/f'custom/{page}.html').read_text(encoding='utf-8');files.update('assets/'+v for v in re.findall(r'(?:src|href)="\.\./assets/([^"]+)"',text))
    return {n:sha(DEMO/n) for n in sorted(files)}

def prepare(p,fixture,page,names):
    fixture['seed'](p,page);p.evaluate('n=>{const pet=PrototypePet.read();pet.name=n.pet;localStorage.setItem("dujia-prototype-pet",JSON.stringify(pet));const profile=JSON.parse(localStorage.getItem("dujia-profile"));profile.nickname=n.actor;localStorage.setItem("dujia-profile",JSON.stringify(profile));const pair=JSON.parse(localStorage.getItem("dujia-prototype-relationship"));pair.partner=n.peer;localStorage.setItem("dujia-prototype-relationship",JSON.stringify(pair));}',names);p.reload();expect(p.locator('.screen')).to_have_attribute('aria-busy','false');expect(p.locator('.pet-load')).to_have_count(0);p.evaluate('document.fonts.ready')

def box(p,selector):return p.locator(selector).bounding_box()
def right(r):return r['x']+r['width']
def bottom(r):return r['y']+r['height']
def fits(p,selector):return p.locator(selector).evaluate('e=>e.scrollWidth<=e.clientWidth+1&&e.scrollHeight<=e.clientHeight+1')
def overlap(a,b):return min(right(a),right(b))-max(a['x'],b['x'])>.5 and min(bottom(a),bottom(b))-max(a['y'],b['y'])>.5

def layout(p,page,names):
    frame=box(p,'.screen');title=box(p,'.title');couple=box(p,'.couple');w,h=frame['width'],frame['height'];x,y=frame['x'],frame['y']
    assert fits(p,'.title'),'Full pet title is clipped/overflows';assert p.locator('.title').inner_text()==('一起照顾'+names['pet'] if page=='m07-p11' else names['pet']+'的小屋设置')
    assert right(title)<=x+w*(.64 if page=='m07-p11' else .84),'Title enters the pet portrait or more-action region'
    assert bottom(title)<=y+h*(.115 if page=='m07-p11' else .095),'Title enters the avatar/profile card'
    assert ''.join(p.locator('.couple').text_content().split())==''.join((names['actor']+'×'+names['peer']).split());assert fits(p,'.couple');assert right(couple)<=x+w*.95
    if p.locator('.owner-name').count():
        expect(p.locator('.couple .owner-name')).to_have_text([names['actor'],names['peer']]);assert p.locator('.owner-name').evaluate_all('ns=>ns.every(e=>e.scrollWidth<=e.clientWidth+1&&e.scrollHeight<=e.clientHeight+1&&getComputedStyle(e).textOverflow!=="ellipsis")'),'Owner names must remain complete, with wrapping rather than truncation'
    if page=='m07-p11':
        back=box(p,'.pet-back');assert title['x']>=right(back)+2
        for left,right_edge in [(.09,.225),(.49,.615)]:assert not overlap(couple,{'x':x+w*left,'y':y+h*.122,'width':w*(right_edge-left),'height':h*.070}),'Owner names enter the avatar portraits'
        assert not overlap(couple,{'x':x+w*.65,'y':y+h*.05,'width':w*.34,'height':h*.172}),'Owner names enter the pet portrait';assert bottom(couple)+4<=box(p,'.tabs')['y'];assert bottom(box(p,'.tabs'))+4<=box(p,'.pet-task-list')['y'];assert bottom(box(p,'.pet-task-list'))+4<=box(p,'.next')['y']
        last=p.locator('.pet-task-list button').last;last.scroll_into_view_if_needed();expect(last).to_be_visible();assert p.locator('.pet-task-list').evaluate('e=>e.scrollWidth<=e.clientWidth+1')
    else:
        back=box(p,'.back');more=box(p,'.pet-life-extra');dog=box(p,'.dog');day=box(p,'.day');info=box(p,'.pet-owner-info') if p.locator('.pet-owner-info').count() else {'x':min(couple['x'],day['x']),'y':couple['y'],'width':max(right(couple),right(day))-min(couple['x'],day['x']),'height':bottom(day)-couple['y']}
        assert couple['y']>=y+h*.208,'Owner names enter the avatar portraits'
        assert title['x']>=right(back)+2 and right(title)+2<=more['x'];assert dog['x']>=x+w*.09 and right(dog)<=x+w*.46;assert bottom(dog)<=y+h*.315 and fits(p,'.dog');assert p.locator('.dog').inner_text()==names['pet']
        assert info['x']>=x+w*.48 and right(info)<=x+w*.95;assert bottom(info)<=y+h*.336,'Full names/day must stay inside the original profile card';assert bottom(couple)+4<=box(p,'.day')['y'];assert fits(p,'.day')
    return {'title':title,'couple':couple,'frame':frame}

def flow(p,name,fixture):
    names=NAMES[1]
    if name=='long-task-tabs':
        prepare(p,fixture,'m07-p11',names);before=fixture['store'](p);p.get_by_role('tab',name='本周约定',exact=True).click();expect(p.locator('.pet-weekly-panel')).to_be_visible();assert bottom(box(p,'.tabs'))+4<=box(p,'.pet-weekly-panel')['y'];p.get_by_role('tab',name='每日任务',exact=True).click();expect(p.locator('.pet-task-list')).to_be_visible();assert fixture['store'](p)==before
    elif name=='long-settings-rename':
        prepare(p,fixture,'m07-p25',names);p.get_by_role('button',name='更多',exact=True).click();p.get_by_role('button',name='修改宠物名字',exact=True).click();p.get_by_role('textbox',name='宠物名字',exact=True).fill(NAMES[3]['pet']);p.get_by_role('button',name='保存宠物名字',exact=True).click();expect(p.locator('dialog')).to_have_count(0);p.evaluate('document.fonts.ready');layout(p,'m07-p25',{**names,'pet':NAMES[3]['pet']});assert p.evaluate('PrototypePet.read().name')==NAMES[3]['pet']
    else:raise AssertionError(name)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['baseline','current'],required=True);args=parser.parse_args();out=ROOT/f'evidence/{args.stage}/pet-header-layout';out.mkdir(parents=True,exist_ok=True);assert not (out/'results.json').exists(),'Preserve previous reports first'
    fixture=declarations('verify_pet_controls.py');files=dependencies();cases=[('layout',(page,width,index)) for page in ['m07-p11','m07-p25'] for width in [320,360,390,414,430] for index in range(len(NAMES))]
    if args.stage=='current':
        catalog=json.loads((ROOT/'evidence/current/page-contracts.json').read_text(encoding='utf-8'));cases += [('control',(r['id'],v)) for r in catalog['pages'] if r['id'] in ['m07-p11','m07-p25'] for v in r['control_evidence']];cases += [('flow',name) for name in ['long-task-tabs','long-settings-rename']]
    rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for kind,value in cases:
            c=b.new_context(viewport={'width':value[1] if kind=='layout' else 390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai',accept_downloads=True);p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));r={'kind':kind,'value':value,'passed':False}
            try:
                if kind=='control':fixture['control'](p,value[0],value[1],value[1]['contract'])
                elif kind=='flow':flow(p,value,fixture)
                else:
                    page,width,index=value;prepare(p,fixture,page,NAMES[index]);before=fixture['store'](p)
                    if width in [320,390] and index in [0,1]:p.screenshot(path=str(out/f'{page}-{width}-{index}.png'),full_page=True)
                    r['geometry']=layout(p,page,NAMES[index]);assert fixture['store'](p)==before
                assert not errors;r['passed']=True
            except Exception:r['failure']=traceback.format_exc()
            r['page_errors']=errors;rows.append(r);c.close();assert dependencies()==files;print(('PASS ' if r['passed'] else 'FAIL ')+kind+' '+str(value),flush=True)
        b.close()
    (out/'results.json').write_text(json.dumps({'dependency_files':files,'producer_sha256':sha(Path(__file__)),'fixture_sha256':sha(ROOT/'verify_pet_controls.py'),'browser':version,'name_scenarios':NAMES,'results':rows,'scope':'p11/p25 full pet12 and owner20 names at five widths; actual title/portrait/control/card bounds, original controls and two long-name interaction flows. No full114, all pet inline or human acceptance claim.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.stage=='baseline':(out/'producer.py').write_bytes(Path(__file__).read_bytes())
    print('Pet header layout:',sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
