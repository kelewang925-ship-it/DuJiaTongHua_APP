"""Check p19 stored story authors and replies against the original artwork regions."""
import argparse,hashlib,json,re,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
SCENARIOS=[{'author':'小满','comments':[]},{'author':'一二三四五六七八九十甲乙丙丁戊己庚辛壬癸','comments':[]},{'author':'W'*20,'comments':[{'author':'阿舟','text':'回'*300}]},{'author':'小满','comments':[{'author':'长'*20,'text':str(i)+'共同回应'+('W'*80)} for i in range(3)]}]

def dependencies():
    files={'custom/m07-p19.html','pages/m07-p19.html','assets/m07-p19-art.webp','assets/font.ttf'}
    files.update('assets/'+s for s in re.findall(r'(?:src|href)="\.\./assets/([^"]+)"',(DEMO/'pages/m07-p19.html').read_text(encoding='utf-8')))
    return {n:sha(DEMO/n) for n in sorted(files)}

def prepare(p,f,scenario):
    f['seed'](p,'m07-p19');p.evaluate('s=>{const pet=PrototypePet.read(),entry=pet.logs.find(v=>v.id==="pet-story");entry.actor=s.author;entry.comments=s.comments;localStorage.setItem("dujia-prototype-pet",JSON.stringify(pet))}',scenario);p.reload();expect(p.locator('.screen')).to_have_attribute('aria-busy','false');expect(p.locator('.pet-load')).to_have_count(0);p.evaluate('document.fonts.ready')

def layout(p,s):
    data=p.evaluate('''()=>{const selectors=['.screen','.name.her','.name.his','.role.her','.role.his','.reply','.private'];return Object.fromEntries(selectors.map(s=>{const e=document.querySelector(s),r=e.getBoundingClientRect();return [s,{x:r.x,y:r.y,w:r.width,h:r.height,fit:e.scrollWidth<=e.clientWidth+1&&e.scrollHeight<=e.clientHeight+1}]}))}''')
    frame=data['.screen'];x,y,w,h=[frame[v] for v in ['x','y','w','h']];r=data['.reply'];a=data['.name.her'];b=data['.name.his'];role=data['.role.her']
    assert r['y']>=y+h*.835 and r['y']+r['h']<=y+h*.887,'Reply region escapes original paper bubble'
    assert r['x']>=x+w*.44 and r['x']+r['w']<=x+w*.82,'Reply region enters original heart or bubble edge'
    assert a['x']+a['w']+2<=b['x'],'Stored author enters response column'
    assert a['y']+a['h']+1<=role['y'],'Stored author overlaps role caption'
    assert a['fit'] and b['fit'],'Full stored author/caption must fit without truncation'
    expect(p.locator('.name.her')).to_have_text(s['author'])
    expected='\n'.join(v['author']+'：'+v['text'] for v in s['comments']) or '还没有回应，一起留下温柔的一句话吧'
    expect(p.locator('.reply')).to_have_text(expected)
    if not s['comments']:assert r['fit'],'Empty reply hint must fit inside bubble'
    else:
        assert p.locator('.reply').evaluate('e=>e.scrollWidth<=e.clientWidth+1'),'Long reply overflows horizontally'
        p.locator('.reply').focus();p.locator('.reply').evaluate('e=>e.scrollTop=e.scrollHeight');assert p.locator('.reply').evaluate('e=>e.scrollTop>0'),'Long replies must remain reachable by scrolling'
    return data

def flow(p,f,name):
    prepare(p,f,SCENARIOS[1]);before=f['store'](p);p.get_by_role('button',name='回应这一页',exact=True).click();field=p.get_by_role('textbox',name='回应内容',exact=True);field.fill('回'*300)
    if name=='save-failure-retry':
        p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","pet-reply")');p.get_by_role('button',name='保存回应',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('操作未完成');assert f['store'](p)==before;expect(field).to_have_value('回'*300);p.get_by_role('button',name='保存回应',exact=True).click();expect(p.locator('dialog')).to_have_count(0);expect(p.locator('.reply')).to_contain_text('回'*300);comments=p.evaluate('PrototypePet.read().logs.find(v=>v.id==="pet-story").comments');assert len(comments)==1 and comments[0]['text']=='回'*300;layout(p,{'author':SCENARIOS[1]['author'],'comments':comments})
    else:
        p.keyboard.press('Escape');expect(p.locator('dialog[open]')).to_have_count(2);p.get_by_role('button',name='继续编辑',exact=True).click();expect(field).to_have_value('回'*300);p.keyboard.press('Escape');p.get_by_role('button',name='放弃修改',exact=True).click();expect(p.locator('dialog')).to_have_count(0);assert f['store'](p)==before;expect(p.get_by_role('button',name='回应这一页',exact=True)).to_be_focused()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stage',choices=['baseline','current'],required=True);args=ap.parse_args();out=ROOT/f'evidence/{args.stage}/pet-story-captions';out.mkdir(parents=True,exist_ok=True);assert not (out/'results.json').exists();files=dependencies();fixture=declarations('verify_pet_controls.py');rows=[]
    cases=[('layout',(w,i)) for w in [320,360,390,414,430] for i in range(4)]
    if args.stage=='current':
        catalog=json.loads((ROOT/'evidence/current/page-contracts.json').read_text(encoding='utf-8'));cases += [('control',v) for r in catalog['pages'] if r['id']=='m07-p19' for v in r['control_evidence']];cases += [('flow',n) for n in ['save-failure-retry','dirty-exit']]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for kind,value in cases:
            c=b.new_context(viewport={'width':value[0] if kind=='layout' else 390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));r={'kind':kind,'value':value,'passed':False}
            try:
                if kind=='control':fixture['control'](p,'m07-p19',value,value['contract'])
                elif kind=='flow':flow(p,fixture,value)
                else:
                    width,index=value;s=SCENARIOS[index];prepare(p,fixture,s);before=fixture['store'](p)
                    if width in [320,390]:p.screenshot(path=str(out/f'{width}-{index}.png'),full_page=True)
                    r['geometry']=layout(p,s);assert fixture['store'](p)==before
                assert not errors;r['passed']=True
            except Exception:r['failure']=traceback.format_exc()
            r['page_errors']=errors;rows.append(r);c.close();assert dependencies()==files;print(('PASS ' if r['passed'] else 'FAIL ')+kind+' '+str(value),flush=True)
        b.close()
    (out/'results.json').write_text(json.dumps({'dependencies':files,'producer_sha256':sha(Path(__file__)),'fixture_sha256':sha(ROOT/'verify_pet_controls.py'),'browser':version,'scenarios':SCENARIOS,'results':rows,'scope':'p19 author/role and reply bubble layout, initial controls and two response flows only; other pet inline and full114 acceptance remain open.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.stage=='baseline':
        (out/'producer.py').write_bytes(Path(__file__).read_bytes())
        for n in files:
            dst=out/'source'/n;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((DEMO/n).read_bytes())
    print(sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
