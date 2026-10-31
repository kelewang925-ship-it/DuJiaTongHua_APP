"""Actual play/reward logs drive result illustrations without changing transactions."""
import argparse,json,re,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from verify_pet_draft_previews import ROOT,DEMO,sha,BASE
ACTIONS=['摸摸头','丢球球','讲故事','送小礼物']
REWARDS=['主粮 ×1、礼物 ×1','爱心小饼干 ×1','金币 ×20','星星 ×5','小花围巾 ×1','旧版奖励记录']

def dependencies():
    files={'assets/font.ttf','assets/book-v2/paper.webp','assets/prototype-components.css','assets/prototype-pet-draft-preview.js','assets/prototype-pet-item-preview.js'}
    for n in [5,6,10,11]:
        name=f'm07-p{n:02}';files.add(f'pages/{name}.html');files.update('assets/'+v for v in re.findall(r'(?:src|href)="\.\./assets/([^"]+)"',(DEMO/f'pages/{name}.html').read_text(encoding='utf-8')))
        if n in [5,10]:files.update([f'custom/{name}.html',f'assets/{name}-art.webp'])
    return {n:sha(DEMO/n) for n in sorted(files)}

def prepare(p,f,n,value):
    f['seed'](p,f'm07-p{n:02}');entry={'id':'result-history','type':'play' if n==5 else 'reward','text':value,'actor':'小满','date':'2026-10-06','story':n==5}
    if n==5:entry['delta']={'energy':-5,'affinity':3,'mood':2}
    p.evaluate('v=>{const pet=PrototypePet.read();pet.logs=[v];pet.lastInteraction=v.id;pet.lastReward=v.id;localStorage.setItem(PrototypePet.key,JSON.stringify(pet));}',entry);p.goto(BASE+f'm07-p{n:02}.html?id=result-history');expect(p.locator('.screen')).to_have_attribute('aria-busy','false');p.evaluate('document.fonts.ready');return entry

def check(p,n,entry):
    label=('本次互动：' if n==5 else '本次奖励：')+entry['text']+' · 示意图';image=p.get_by_role('img',name=label,exact=True)
    assert image.count()==1,'No illustration corresponding to this actual result log'
    expect(image).to_be_visible();assert image.evaluate('e=>e.tagName.toLowerCase()==="svg"&&e.querySelectorAll("path,circle,ellipse,rect").length>0')
    assert p.locator('.pet-result-illustration').get_by_role('button').count()==0
    assert p.locator('.pet-result-illustration').evaluate('e=>{const r=e.getBoundingClientRect(),s=document.querySelector(".screen").getBoundingClientRect(),label=document.querySelector(".result-label,.label").getBoundingClientRect(),svg=e.querySelector("svg").getBoundingClientRect();return e.scrollWidth<=e.clientWidth+1&&e.scrollHeight<=e.clientHeight+1&&r.left>=s.left&&r.right<=s.right&&r.bottom<=label.top&&svg.bottom<=r.bottom}')
    expect(p.locator('.art-hero')).to_have_attribute('aria-hidden','true')
    if n==5:
        progress=p.get_by_role('progressbar',name='本周照顾奖励进度',exact=True);expect(progress).to_have_attribute('max','3');assert progress.evaluate('e=>e.value')==p.evaluate('Math.min(3,PrototypePet.weekCount(PrototypePet.read()))')
    if n==10:expect(p.locator('.reward')).to_have_text(entry['text'])
    return image.locator('[data-result-symbol]').evaluate_all('es=>es.map(e=>e.dataset.resultSymbol)')

def play(p,f,index):
    f['seed'](p,'m07-p06');p.evaluate('()=>{const v=PrototypePet.read();v.logs=[];v.energy=82;v.gifts=1;localStorage.setItem(PrototypePet.key,JSON.stringify(v));}');p.reload();expect(p.locator('.screen')).to_have_attribute('aria-busy','false');p.locator('.option').nth(index).click();before=f['store'](p);p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","pet-play")');p.locator('#play').click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert f['store'](p)==before;p.locator('#play').click();p.wait_for_url('**/m07-p05.html*');expect(p.locator('.screen')).to_have_attribute('aria-busy','false');entry=p.evaluate('PrototypePet.read().logs[0]');assert entry['text']==ACTIONS[index];check(p,5,entry);assert p.evaluate('PrototypePet.read().logs.filter(v=>v.type==="play").length')==1

def claim(p,f,type):
    f['seed'](p,'m07-p11');p.evaluate('''type=>{const pet=PrototypePet.read();pet.claims=[];pet.owned=type==='weekly-stars'?['小花围巾']:[];pet.logs=(type.startsWith('weekly')?['play','feed','water']:[type]).map((v,i)=>({id:'task-'+i,type:v,text:'共同照顾',actor:'小满',date:'2026-10-06',delta:{energy:-5,affinity:3,mood:2},story:true}));localStorage.setItem(PrototypePet.key,JSON.stringify(pet));}''',type);p.reload();expect(p.locator('.screen')).to_have_attribute('aria-busy','false')
    if type.startswith('weekly'):p.locator('.tabs button').nth(1).click();trigger=p.get_by_role('button',name='领取本周奖励',exact=True)
    else:trigger=p.get_by_role('button',name='领取'+{'water':'添水','play':'互动','feed':'喂食','note':'心情'}[type]+'奖励',exact=True)
    before=f['store'](p);p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","pet-claim")');trigger.click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert f['store'](p)==before;trigger.click();p.wait_for_url('**/m07-p10.html*');expect(p.locator('.screen')).to_have_attribute('aria-busy','false');entry=p.evaluate('PrototypePet.read().logs[0]');assert entry['text']=={'water':REWARDS[0],'play':REWARDS[1],'feed':REWARDS[2],'note':REWARDS[3],'weekly':REWARDS[4],'weekly-stars':REWARDS[3]}[type];check(p,10,entry);assert p.evaluate('PrototypePet.read().claims.length')==1;p.locator('.wear').click();p.wait_for_url('**/m07-p11.html');expect(p.locator('.screen')).to_have_attribute('aria-busy','false')
    if type.startswith('weekly'):p.locator('.tabs button').nth(1).click();expect(p.locator('.pet-week-claim')).to_be_disabled()
    else:assert p.evaluate('PrototypePet.taskState(PrototypePet.read(),'+json.dumps(type)+').claimed')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stage',required=True,choices=['baseline','current']);args=ap.parse_args();out=ROOT/f'evidence/{args.stage}/pet-result-illustrations';out.mkdir(parents=True,exist_ok=True);assert not (out/'results.json').exists();deps=dependencies();f=declarations('verify_pet_controls.py');cases=[('layout',(5,390,ACTIONS[0])),('layout',(5,390,ACTIONS[2])),('layout',(10,390,REWARDS[2])),('layout',(10,390,REWARDS[3]))]
    if args.stage=='current':
        cases=[('layout',(n,w,v)) for w in [320,375,390,414,430] for n,values in [(5,ACTIONS),(10,REWARDS)] for v in values];catalog=json.loads((ROOT/'evidence/current/page-contracts.json').read_text(encoding='utf-8'));cases += [('control',(row['id'],v)) for row in catalog['pages'] if row['id'] in ['m07-p05','m07-p10'] for v in row['control_evidence']]+[('play',i) for i in range(4)]+[('claim',type) for type in ['water','play','feed','note','weekly','weekly-stars']]
    rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for kind,value in cases:
            c=b.new_context(viewport={'width':value[1] if kind=='layout' else 390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row={'kind':kind,'value':value,'passed':False}
            try:
                if kind=='control':page,v=value;f['control'](p,page,v,v['contract'])
                elif kind in ['play','claim']:(play if kind=='play' else claim)(p,f,value)
                else:
                    n,w,v=value;entry=prepare(p,f,n,v);before=f['store'](p)
                    if w==390:p.screenshot(path=str(out/(str(n)+'-'+str((ACTIONS if n==5 else REWARDS).index(v))+'.png')),full_page=True)
                    row['symbols']=check(p,n,entry);assert f['store'](p)==before
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
