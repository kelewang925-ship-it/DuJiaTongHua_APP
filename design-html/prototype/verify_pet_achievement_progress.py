"""Native achievement bars/status must agree with the existing pet achievement model."""
import argparse,hashlib,json,re,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations

ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
MODES={'zero':(0,0,0,[]),'partial':(4,9,0,[]),'complete':(10,20,1,[]),'over-target':(13,25,3,['achievement:meet','achievement:play10'])}
IDS=['meet','play10','feed20','room'];NAMES=['第一次见面','玩到天黑','默契喂食','小屋变新了'];TARGETS=[1,10,20,1]

def dependencies():
    text=(DEMO/'custom/m07-p20.html').read_text(encoding='utf-8');files={'custom/m07-p20.html','pages/m07-p20.html','assets/m07-p20-art.webp','assets/font.ttf','assets/prototype-components.css','assets/book-v2/paper.webp'}
    files.update('assets/'+p for p in re.findall(r'(?:src|href)="\.\./assets/([^"]+)"',text))
    return {p:sha(DEMO/p) for p in sorted(files)}

def prepare(p,fixture,mode='partial',counts=None):
    fixture['seed'](p,'m07-p20');play,feed,room,claims=MODES[mode]
    if counts:play,feed,room=counts
    p.evaluate('d=>{const pet=PrototypePet.read();pet.logs=[];for(const [type,count]of Object.entries(d.counts))for(let i=0;i<count;i++)pet.logs.push({id:type+"-"+i,type,text:"历史照顾",actor:"小满",date:"2026-10-05",at:1791158400000});pet.claims=d.claims;pet.stars=30;localStorage.setItem("dujia-prototype-pet",JSON.stringify(pet));}',{'counts':{'play':play,'feed':feed,'room':room},'claims':claims})
    p.goto('http://127.0.0.1:8765/pages/m07-p20.html?achievement=play10');expect(p.locator('.screen')).to_have_attribute('aria-busy','false');p.evaluate('document.fonts.ready');return [1,play,feed,room],claims

def flow(p,name,fixture):
    if name=='claim-retry-once':
        prepare(p,fixture,'complete');before=fixture['store'](p);p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","pet-achievement")');p.locator('.claim').click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert fixture['store'](p)==before;expect(p.locator('.claim')).to_be_enabled();p.locator('.claim').click();expect(p.locator('.prototype-toast')).to_contain_text('成就奖励已到账');expect(p.locator('.claim')).to_be_disabled();expect(p.locator('[data-achievement=play10] .pet-achievement-state')).to_have_text('奖励已领取');saved=p.evaluate('PrototypePet.read()');assert saved['stars']==40 and saved['claims'].count('achievement:play10')==1;after=fixture['store'](p);p.evaluate('document.querySelector(".claim").click()');assert fixture['store'](p)==after;p.reload();expect(p.locator('.claim')).to_be_disabled();assert fixture['store'](p)==after
    elif name in ['actual-play','actual-feed']:
        prepare(p,fixture,counts=(9,19,0));page='m07-p06' if name=='actual-play' else 'm07-p08';p.goto('http://127.0.0.1:8765/pages/'+page+'.html');expect(p.locator('.screen')).to_have_attribute('aria-busy','false');p.locator('#play' if name=='actual-play' else '#feed').click()
        if name=='actual-play':p.wait_for_url('**/m07-p05.html?id=*')
        else:expect(p.locator('#stock0')).to_have_text('11')
        achievement='play10' if name=='actual-play' else 'feed20';p.goto('http://127.0.0.1:8765/pages/m07-p20.html?achievement='+achievement);expect(p.locator('[data-achievement='+achievement+'] progress')).to_have_attribute('value','10' if name=='actual-play' else '20');expect(p.locator('[data-achievement='+achievement+'] .pet-achievement-state')).to_have_text('已达成');expect(p.locator('.claim')).to_be_enabled()
    elif name=='cross-tab-refresh':
        prepare(p,fixture);other=p.context.new_page();other.goto('http://127.0.0.1:8765/prototype/review.html');other.evaluate('()=>{const pet=JSON.parse(localStorage.getItem("dujia-prototype-pet"));for(let i=4;i<7;i++)pet.logs.push({id:"play-"+i,type:"play",text:"另一窗口的照顾",actor:"小满",date:"2026-10-05",at:1791158400000});localStorage.setItem("dujia-prototype-pet",JSON.stringify(pet));}');expect(p.locator('[data-achievement=play10] progress')).to_have_attribute('value','7');expect(p.locator('[data-achievement=play10] .pet-achievement-value')).to_have_text('7 / 10');other.close()
    else:raise AssertionError(name)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['baseline','current'],required=True);args=parser.parse_args();out=ROOT/f'evidence/{args.stage}/pet-achievement-progress';out.mkdir(parents=True,exist_ok=True);assert not (out/'results.json').exists(),'Preserve previous evidence first'
    fixture=declarations('verify_pet_controls.py');files=dependencies();cases=[('layout',(w,m)) for w in [320,360,390,414,430] for m in MODES]
    if args.stage=='current':
        catalog=json.loads((ROOT/'evidence/current/page-contracts.json').read_text(encoding='utf-8'));cases += [('control',v) for v in next(r for r in catalog['pages'] if r['id']=='m07-p20')['control_evidence']]
        cases += [('flow',name) for name in ['claim-retry-once','actual-play','actual-feed','cross-tab-refresh']]
    rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for kind,value in cases:
            c=b.new_context(viewport={'width':value[0] if kind=='layout' else 390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));r={'kind':kind,'value':value,'passed':False}
            try:
                if kind=='control':fixture['control'](p,'m07-p20',value,value['contract'])
                elif kind=='flow':flow(p,value,fixture)
                else:
                    width,mode=value;counts,claims=prepare(p,fixture,mode);before=fixture['store'](p)
                    if width==390:p.screenshot(path=str(out/(mode+'.png')),full_page=True)
                    assert p.locator('.row progress').count()==4,'Actual numbers still sit next to baked nonzero progress bars'
                    for i,(id,name,count,target) in enumerate(zip(IDS,NAMES,counts,TARGETS)):
                        row=p.locator('[data-achievement='+id+']');wanted=min(count,target);expect(row.locator('progress')).to_have_attribute('value',str(wanted));expect(row.locator('progress')).to_have_attribute('max',str(target));expect(row.locator('progress')).to_have_attribute('aria-label',name);expect(row.locator('.pet-achievement-value')).to_have_text(f'{wanted} / {target}');expect(row.locator('.pet-achievement-state')).to_have_text('奖励已领取' if 'achievement:'+id in claims else '已达成' if count>=target else '进行中')
                        assert row.evaluate('e=>e.scrollWidth<=e.clientWidth+1&&e.scrollHeight<=e.clientHeight+1'),'Native label/bar escapes the card'
                        assert row.evaluate('e=>{const r=e.getBoundingClientRect(),b=e.querySelector("progress").getBoundingClientRect();return b.left>=r.left&&b.right<=r.right&&b.top>=r.top&&b.bottom<=r.bottom}'),'Progress bar escapes its paper cover'
                    expect(p.locator('.stamp')).to_be_hidden()
                    # The original star occupies x40-51%, y46.5-52% of this source board.
                    assert p.locator('.reward').evaluate('e=>{const range=document.createRange();range.selectNodeContents(e);const r=range.getBoundingClientRect(),s=document.querySelector(".screen").getBoundingClientRect();return r.left>=s.left+s.width*.51+1&&r.right<=s.left+s.width*.80&&e.scrollWidth<=e.clientWidth+1}'),'Reward text overlaps the star illustration or escapes its card'
                    assert fixture['store'](p)==before
                assert not errors;r['passed']=True
            except Exception:r['failure']=traceback.format_exc()
            r['page_errors']=errors;rows.append(r);c.close();assert dependencies()==files;print(('PASS ' if r['passed'] else 'FAIL ')+kind+' '+str(value),flush=True)
        b.close()
    (out/'results.json').write_text(json.dumps({'dependency_files':files,'producer_sha256':sha(Path(__file__)),'fixture_sha256':sha(ROOT/'verify_pet_controls.py'),'browser':version,'results':rows,'scope':'Pet achievement page: four rows/four data states/five widths, reward text/star separation, original initial controls and four actual claim/action/cross-tab outcomes. Not full114 replay or human acceptance.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.stage=='baseline':(out/'producer.py').write_bytes(Path(__file__).read_bytes())
    print('Pet achievement progress:',sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
