"""Achievement overview must expose truthful progress and the next available step."""
import argparse,hashlib,json,re,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
MODES=['pending','partial','complete','claimed','last-reward']
IDS=['meet','play10','feed20','room','care7','affinity','days30']

def dependencies():
    files={'custom/m07-p21.html','pages/m07-p21.html','assets/m07-p21-art.webp','assets/font.ttf','assets/prototype-components.css','assets/book-v2/paper.webp'}
    for page in ['m07-p21','m07-p20','m07-p06','m07-p05']:
        files.add('pages/'+page+'.html');files.update('assets/'+v for v in re.findall(r'(?:src|href)="\.\./assets/([^"]+)"',(DEMO/f'pages/{page}.html').read_text(encoding='utf-8')))
    return {n:sha(DEMO/n) for n in sorted(files)}

def prepare(p,f,mode):
    f['seed'](p,'m07-p21');p.evaluate('''mode=>{const pet=PrototypePet.read();pet.logs=[];pet.claims=[];pet.affinity=20;pet.adoptedDate='2026-10-06';pet.stars=30;
    const add=(type,n)=>{for(let i=0;i<n;i++)pet.logs.push({id:type+'-'+i,type,text:'历史照顾',actor:'小满',date:'2026-10-05',at:1791158400000,story:false})};
    if(mode==='partial'){add('play',4);add('feed',3);pet.claims=['achievement:meet']}
    if(['complete','claimed','last-reward'].includes(mode)){add('play',10);add('feed',20);add('room',1);pet.affinity=200;pet.adoptedDate='2026-09-01';for(let i=0;i<7;i++)pet.logs.push({id:'care-'+i,type:'water',text:'添水',actor:'小满',date:'2026-09-0'+(i+1),at:1791158400000,story:false});}
    if(mode==='claimed')pet.claims=['meet','play10','feed20','room','care7','affinity','days30'].map(v=>'achievement:'+v);
    if(mode==='last-reward')pet.claims=['meet','play10','feed20','room','care7','affinity'].map(v=>'achievement:'+v);
    localStorage.setItem('dujia-prototype-pet',JSON.stringify(pet))}''',mode);p.reload();expect(p.locator('.screen')).to_have_attribute('aria-busy','false');p.evaluate('document.fonts.ready')

def check(p):
    items=p.evaluate('PrototypePetLife.achievements(PrototypePet.read())');pending=next((v for v in items if v['done'] and not v['claimed']),None);next_item=next((v for v in items if not v['done']),None)
    summary=p.locator('.next');expect(summary).to_be_visible()
    if pending:expect(summary).to_have_text('可领取：'+pending['name']+'\n奖励星星 ×'+str(pending['reward'])+' · 点上方成就查看')
    elif next_item:expect(summary).to_have_text('下一枚：'+next_item['name']+'\n进度 '+str(min(next_item['progress'],next_item['target']))+' / '+str(next_item['target'])+' · 奖励星星 ×'+str(next_item['reward']))
    else:expect(summary).to_have_text('成就奖励已全部领取\n'+str(len(items))+' 枚纪念章已收藏')
    expect(p.locator('.badge-number')).to_have_text(str(sum(v['done'] for v in items))+' / '+str(len(items)))
    assert summary.evaluate('e=>{const r=e.getBoundingClientRect(),s=document.querySelector(".screen").getBoundingClientRect(),cta=document.querySelector(".cta").getBoundingClientRect();return !e.hidden&&e.scrollWidth<=e.clientWidth+1&&e.scrollHeight<=e.clientHeight+1&&r.left>=s.left+s.width*.32&&r.top>=s.top+s.height*.79&&r.bottom<cta.top}'),'Summary clips text, covers pet or enters task CTA'
    for i,item in enumerate(items):
        b=p.locator('.cards button').nth(i);state='奖励已领取' if item['claimed'] else '可领取奖励' if item['done'] else '进行中'
        expect(b.locator('.pet-achievement-title')).to_have_text(item['name']);expect(b.locator('progress')).to_have_attribute('max',str(item['target']));expect(b.locator('progress')).to_have_attribute('value',str(max(0,min(item['progress'],item['target']))));expect(b.locator('.pet-achievement-state')).to_have_text(state)
        assert b.locator('svg[aria-hidden=true]').count()==1,'Each real achievement needs its own editable medal'
        assert b.evaluate('e=>e.scrollWidth<=e.clientWidth+1&&e.scrollHeight<=e.clientHeight+1'),'Achievement card clips content'
    last=p.locator('.cards button').last;last.scroll_into_view_if_needed();expect(last).to_be_visible();last.focus();expect(last).to_be_focused();assert p.locator('.cards').evaluate('e=>e.scrollWidth<=e.clientWidth+1')

def flow(p,f,name):
    if name=='claim-retry':
        prepare(p,f,'pending');p.get_by_role('button',name='第一次见面',exact=False).click();p.wait_for_url('**/m07-p20.html?achievement=meet');before=f['store'](p);p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","pet-achievement")');p.locator('.claim').click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert f['store'](p)==before;p.locator('.claim').click();expect(p.locator('.prototype-toast')).to_contain_text('成就奖励已到账');expect(p.locator('.claim')).to_be_disabled();assert p.evaluate('PrototypePet.read().stars')==35;p.goto('http://127.0.0.1:8765/pages/m07-p21.html');expect(p.locator('.screen')).to_have_attribute('aria-busy','false');check(p);expect(p.locator('.next')).to_contain_text('下一枚：玩到天黑');assert p.evaluate('PrototypePet.read().claims.filter(v=>v==="achievement:meet").length')==1
    else:
        prepare(p,f,'partial');p.evaluate('()=>{const pet=PrototypePet.read();for(let i=4;i<9;i++)pet.logs.push({id:"play-"+i,type:"play",text:"历史照顾",actor:"小满",date:"2026-10-05",at:1791158400000});localStorage.setItem("dujia-prototype-pet",JSON.stringify(pet))}');p.reload();expect(p.locator('.screen')).to_have_attribute('aria-busy','false');expect(p.locator('.next')).to_contain_text('进度 9 / 10');other=p.context.new_page();other.goto('http://127.0.0.1:8765/pages/m07-p06.html');expect(other.locator('.screen')).to_have_attribute('aria-busy','false');other.locator('#play').click();other.wait_for_url('**/m07-p05.html?id=*');expect(p.locator('.next')).to_contain_text('可领取：玩到天黑');check(p);other.close()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stage',choices=['baseline','current'],required=True);args=ap.parse_args();out=ROOT/f'evidence/{args.stage}/pet-achievement-collection';out.mkdir(parents=True,exist_ok=True);assert not (out/'results.json').exists();files=dependencies();f=declarations('verify_pet_controls.py');rows=[]
    cases=[('layout',(w,m)) for w in [320,360,390,414,430] for m in MODES]
    if args.stage=='current':
        catalog=json.loads((ROOT/'evidence/current/page-contracts.json').read_text(encoding='utf-8'));cases += [('control',v) for r in catalog['pages'] if r['id']=='m07-p21' for v in r['control_evidence']];cases += [('flow',n) for n in ['claim-retry','actual-cross-tab-play']]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for kind,value in cases:
            c=b.new_context(viewport={'width':value[0] if kind=='layout' else 390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));r={'kind':kind,'value':value,'passed':False}
            try:
                if kind=='control':f['control'](p,'m07-p21',value,value['contract'])
                elif kind=='flow':flow(p,f,value)
                else:
                    width,mode=value;prepare(p,f,mode);before=f['store'](p)
                    if width in [320,390]:p.screenshot(path=str(out/f'{width}-{mode}.png'),full_page=True)
                    check(p);assert f['store'](p)==before
                assert not errors;r['passed']=True
            except Exception:r['failure']=traceback.format_exc()
            r['page_errors']=errors;rows.append(r);c.close();assert dependencies()==files;print(('PASS ' if r['passed'] else 'FAIL ')+kind+' '+str(value),flush=True)
        b.close()
    (out/'results.json').write_text(json.dumps({'dependencies':files,'producer_sha256':sha(Path(__file__)),'fixture_sha256':sha(ROOT/'verify_pet_controls.py'),'browser':version,'results':rows,'scope':'p21 seven real achievement cards and truthful pending/next/all-claimed summary; five widths, original controls, claim retry and actual cross-tab interaction. Not full114 or human acceptance.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.stage=='baseline':
        (out/'producer.py').write_bytes(Path(__file__).read_bytes())
        for n in files:
            dst=out/'source'/n;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((DEMO/n).read_bytes())
    print(sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
