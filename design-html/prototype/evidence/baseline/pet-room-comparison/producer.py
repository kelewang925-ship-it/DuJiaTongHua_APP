"""The saved room comparison must show historical snapshots, never the latest room."""
import argparse,json,re,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from verify_pet_draft_previews import ROOT,DEMO,sha,prepare as draft_prepare,select,BASE
BEFORE={'地毯':'花朵地毯','小床':'木质小床','墙饰':'花朵墙饰','摆件':'花朵花瓶'}
AFTER={'地毯':'格纹地毯','小床':'奶油小床','墙饰':'回忆相框','摆件':'纪念日星灯'}

def dependencies():
    files={'assets/font.ttf','assets/prototype-components.css','assets/book-v2/paper.webp'}
    for n in [14,15]:
        name=f'm07-p{n}';files.update([f'pages/{name}.html',f'custom/{name}.html',f'assets/{name}-art.webp']);files.update('assets/'+v for v in re.findall(r'(?:src|href)="\.\./assets/([^"]+)"',(DEMO/f'pages/{name}.html').read_text(encoding='utf-8')))
    return {n:sha(DEMO/n) for n in sorted(files)}

def prepare(p,f,mode):
    f['seed'](p,'m07-p14');entry={'id':'comparison-history','type':'room','text':'整理了小屋' if mode=='same' else '更换了小屋布置','actor':'保存当时的共同伙伴','date':'2026-10-06','story':True}
    if mode in ['changed','same']:entry.update(before=BEFORE,after=BEFORE if mode=='same' else AFTER)
    if mode=='partial':entry.update(before={'地毯':'已下架未知地毯'},after={'地毯':'格纹地毯','小床':'不存在的小床'})
    p.evaluate('e=>{const pet=PrototypePet.read();pet.room={地毯:"月亮地毯",小床:"木质小床",墙饰:"花朵墙饰",摆件:"花朵花瓶"};pet.logs=[e];pet.lastRoom=e.id;localStorage.setItem(PrototypePet.key,JSON.stringify(pet));}',entry);p.goto(BASE+'m07-p14.html?id=comparison-history');expect(p.locator('.screen')).to_have_attribute('aria-busy','false');p.evaluate('document.fonts.ready');return entry

def check(p,entry):
    panel=p.locator('.pet-room-comparison');assert panel.count()==1,'No comparison of saved historical room snapshots'
    for key,label in [('before','布置前'),('after','布置后')]:
        figure=panel.locator('[data-snapshot="'+key+'"]');expect(figure.get_by_role('heading',name=label,exact=True)).to_be_visible();value=entry.get(key,{})
        wanted=p.evaluate('v=>PrototypePetLife.catalog.filter(i=>i.type==="room"&&v[i.group]===i.name).map(i=>i.id)',value)
        if wanted:
            svg=figure.get_by_role('img');expect(svg).to_be_visible();assert svg.locator('[data-preview-item]').evaluate_all('es=>es.map(e=>e.dataset.previewItem)')==wanted
        else:assert figure.get_by_role('img').count()==0
        for group in BEFORE:
            name=value.get(group);known=p.evaluate('v=>PrototypePetLife.catalog.some(i=>i.type==="room"&&i.group===v[0]&&i.name===v[1])',[group,name])
            expect(figure.locator('.pet-room-snapshot-labels')).to_contain_text(group+'：'+(name if known else '未记录'))
        assert figure.evaluate('e=>e.scrollWidth<=e.clientWidth+1&&e.scrollHeight<=e.clientHeight+1')
    assert panel.get_by_role('button').count()==0
    assert panel.evaluate('e=>{const r=e.getBoundingClientRect(),s=document.querySelector(".screen").getBoundingClientRect(),b=document.querySelector(".primary").getBoundingClientRect();return r.left>=s.left&&r.right<=s.right&&r.bottom<=b.top}')
    expect(p.locator('.receipt')).to_contain_text(entry['actor'])

def saved(p,f):
    draft_prepare(p,f,15);before=p.evaluate('PrototypePetLife.room(PrototypePet.read())');select(p,'cream-bed');p.locator('.save').click();p.wait_for_url('**/m07-p14.html*');expect(p.locator('.screen')).to_have_attribute('aria-busy','false');entry=p.evaluate('PrototypePet.read().logs.find(v=>v.id===new URLSearchParams(location.search).get("id"))');assert entry['before']==before and entry['after']['小床']=='奶油小床';check(p,entry);p.reload();expect(p.locator('.screen')).to_have_attribute('aria-busy','false');check(p,entry)

def peer(p,f):
    entry=prepare(p,f,'changed');check(p,entry);other=p.context.new_page();other.goto('http://127.0.0.1:8765/prototype/review.html');other.evaluate('()=>{const pet=JSON.parse(localStorage.getItem("dujia-prototype-pet"));pet.room={地毯:"野餐垫",小床:"木质小床",墙饰:"花朵墙饰",摆件:"花朵花瓶"};localStorage.setItem("dujia-prototype-pet",JSON.stringify(pet));}');expect(p.locator('.screen')).to_have_attribute('aria-busy','false');expect(p.locator('.pet-room-comparison')).to_be_visible();check(p,entry);other.close()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stage',choices=['baseline','current'],required=True);args=ap.parse_args();out=ROOT/f'evidence/{args.stage}/pet-room-comparison';out.mkdir(parents=True,exist_ok=True);assert not (out/'results.json').exists();deps=dependencies();f=declarations('verify_pet_controls.py');cases=[('layout',(390,mode)) for mode in ['changed','same','missing','partial']]
    if args.stage=='current':
        cases=[('layout',(w,mode)) for w in [320,375,390,414,430] for mode in ['changed','same','missing','partial']];catalog=json.loads((ROOT/'evidence/current/page-contracts.json').read_text(encoding='utf-8'));cases += [('control',v) for row in catalog['pages'] if row['id']=='m07-p14' for v in row['control_evidence']]+[('save',None),('peer',None)]
    rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for kind,value in cases:
            c=b.new_context(viewport={'width':value[0] if kind=='layout' else 390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row={'kind':kind,'value':value,'passed':False}
            try:
                if kind=='control':f['control'](p,'m07-p14',value,value['contract'])
                elif kind=='save':saved(p,f)
                elif kind=='peer':peer(p,f)
                else:
                    entry=prepare(p,f,value[1]);before=f['store'](p)
                    if value[0]==390:p.screenshot(path=str(out/(value[1]+'.png')),full_page=True)
                    check(p,entry);assert f['store'](p)==before
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
