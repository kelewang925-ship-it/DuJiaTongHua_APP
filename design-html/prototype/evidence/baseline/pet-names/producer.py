"""Source-template pet/person names in accessibility labels, titles and literal edge-case nicknames."""
import argparse,hashlib,json,re,traceback
from html.parser import HTMLParser
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations

ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
NAMES=[{'pet':'奶糖','actor':'鹿鹿','peer':'星野'}, {'pet':'奶糖小满阿舟星星伙伴团团','actor':'阿舟小满','peer':'糯米阿舟'}, {'pet':'Mochi$&','actor':'鹿$&','peer':'星$&'}, {'pet':'<奶糖>&"','actor':'鹿<&','peer':'星">'}]
TOKENS=re.compile('糯米|小满|阿舟')
replace=lambda text,names:TOKENS.sub(lambda m:names[{'糯米':'pet','小满':'actor','阿舟':'peer'}[m[0]]],text)

class Templates(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True);self.stack=[];self.roots={};self.attrs=[];self.title='';self.feed(text)
    def handle_starttag(self,tag,attrs):
        counts=self.stack[-1]['counts'] if self.stack else self.roots;counts[tag]=counts.get(tag,0)+1
        path=(self.stack[-1]['path']+'>' if self.stack else '')+tag+f':nth-of-type({counts[tag]})'
        for key,value in attrs:
            if key in ['aria-label','alt','title'] and value and TOKENS.search(value):self.attrs.append({'selector':path,'attribute':key,'template':value})
        if tag not in ['meta','link','input','img','br','hr','source','area','base','embed','param','track','wbr']:self.stack.append({'tag':tag,'path':path,'counts':{}})
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i]['tag']==tag:del self.stack[i:];break
    def handle_data(self,data):
        if self.stack and self.stack[-1]['tag']=='title':self.title+=data

def dependencies():
    files={'assets/font.ttf','assets/prototype-components.css'}
    for i in range(1,26):
        id=f'm07-p{i:02}';files.update([f'custom/{id}.html',f'pages/{id}.html',f'assets/{id}-art.webp']);text=(DEMO/f'custom/{id}.html').read_text(encoding='utf-8');files.update('assets/'+x for x in re.findall(r'(?:src|href)="\.\./assets/([^"]+)"',text))
    return {n:sha(DEMO/n) for n in sorted(files)}

def prepare(p,fixture,page,names):
    fixture['seed'](p,page)
    p.evaluate('names=>{const pet=PrototypePet.read();if(pet){pet.name=names.pet;localStorage.setItem("dujia-prototype-pet",JSON.stringify(pet));}const profile=JSON.parse(localStorage.getItem("dujia-profile"));profile.nickname=names.actor;localStorage.setItem("dujia-profile",JSON.stringify(profile));const pair=JSON.parse(localStorage.getItem("dujia-prototype-relationship"));pair.partner=names.peer;localStorage.setItem("dujia-prototype-relationship",JSON.stringify(pair));}',names)
    p.reload();expect(p.locator('.screen')).to_have_attribute('aria-busy','false');expect(p.locator('.pet-load')).to_have_count(0);p.evaluate('document.fonts.ready');return p.evaluate('!!PrototypePet.read()')

def flow(p,name,fixture):
    prepare(p,fixture,'m07-p25',NAMES[0]);before=fixture['store'](p)
    if name=='actual-rename':
        p.get_by_role('button',name='更多',exact=True).click();p.get_by_role('button',name='修改宠物名字',exact=True).click();p.get_by_label('宠物名字',exact=True).fill('小满$&');p.get_by_role('button',name='保存宠物名字',exact=True).click();expect(p.locator('dialog')).to_have_count(0);expect(p.locator('.art-top')).to_have_attribute('aria-label','小满$&与共同照顾它的鹿鹿和星野');assert p.title()=='小满$&的小屋设置 · 独家童话';assert p.evaluate('PrototypePet.read().name')=='小满$&';p.reload();expect(p.locator('.art-top')).to_have_attribute('aria-label','小满$&与共同照顾它的鹿鹿和星野')
    elif name=='repeat-template':
        for names in [NAMES[1],NAMES[2],NAMES[3],NAMES[1]]:
            p.evaluate('n=>PrototypePetNames.paint(n)',names);wanted=replace('糯米与共同照顾它的小满和阿舟',names);expect(p.locator('.art-top')).to_have_attribute('aria-label',wanted);assert p.title()==replace('糯米的小屋设置 · 独家童话',names)
        assert fixture['store'](p)==before
    elif name=='controller-owned-content':
        p.locator('.art-top').evaluate('e=>e.setAttribute("aria-label","糯米和小满是原始故事中的名字")');p.locator('.title').evaluate('e=>e.textContent="小满亲手写下的内容"');p.evaluate('n=>PrototypePetNames.paint(n)',NAMES[2]);expect(p.locator('.art-top')).to_have_attribute('aria-label','糯米和小满是原始故事中的名字');expect(p.locator('.title')).to_have_text('小满亲手写下的内容');p.evaluate('n=>PrototypePetNames.paint(n)',NAMES[1]);expect(p.locator('.art-top')).to_have_attribute('aria-label','糯米和小满是原始故事中的名字');assert fixture['store'](p)==before
    elif name=='cross-tab-names':
        other=p.context.new_page();other.goto('http://127.0.0.1:8765/prototype/review.html');other.evaluate('names=>{const pet=JSON.parse(localStorage.getItem("dujia-prototype-pet"));pet.name=names.pet;const profile=JSON.parse(localStorage.getItem("dujia-profile"));profile.nickname=names.actor;const pair=JSON.parse(localStorage.getItem("dujia-prototype-relationship"));pair.partner=names.peer;localStorage.setItem("dujia-profile",JSON.stringify(profile));localStorage.setItem("dujia-prototype-relationship",JSON.stringify(pair));localStorage.setItem("dujia-prototype-pet",JSON.stringify(pet));}',NAMES[2]);expect(p.locator('.art-top')).to_have_attribute('aria-label',replace('糯米与共同照顾它的小满和阿舟',NAMES[2]));assert p.title()==replace('糯米的小屋设置 · 独家童话',NAMES[2]);other.close()
    else:raise AssertionError(name)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['baseline','current'],required=True);args=parser.parse_args();out=ROOT/f'evidence/{args.stage}/pet-names';out.mkdir(parents=True,exist_ok=True);assert not (out/'results.json').exists(),'Preserve prior evidence before re-running'
    fixture=declarations('verify_pet_controls.py');files=dependencies();templates={f'm07-p{i:02}':Templates((DEMO/f'custom/m07-p{i:02}.html').read_text(encoding='utf-8')) for i in range(1,26)}
    cases=[('names',(id,index)) for index in range(1 if args.stage=='baseline' else len(NAMES)) for id in templates]
    if args.stage=='current':cases += [('flow',name) for name in ['actual-rename','repeat-template','controller-owned-content','cross-tab-names']]
    rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for kind,value in cases:
            c=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));r={'kind':kind,'value':value,'passed':False}
            try:
                if kind=='flow':flow(p,value,fixture)
                else:
                    id,index=value;names=NAMES[index];has_pet=prepare(p,fixture,id,names);before=fixture['store'](p);observations=[]
                    for item in templates[id].attrs:
                        locator=p.locator(item['selector']);actual=locator.get_attribute(item['attribute']) if locator.count() else None;wanted=replace(item['template'],names) if has_pet else item['template'];observations.append({**item,'expected':wanted,'actual':actual,'present':actual is not None})
                    r['attributes']=observations;r['document_title']=p.title();r['expected_title']=replace(templates[id].title,names) if has_pet else templates[id].title
                    assert all(item['actual']==item['expected'] for item in observations if item['present']),[item for item in observations if item['present'] and item['actual']!=item['expected']]
                    assert r['document_title']==r['expected_title'],'Document title still uses a source placeholder name'
                    if id=='m07-p07':expect(p.locator('h2')).to_contain_text(names['pet']+'想先睡一会儿')
                    if index in [0,1] and id in ['m07-p11','m07-p25']:p.screenshot(path=str(out/f'{id}-names-{index}.png'),full_page=True)
                    assert fixture['store'](p)==before,'Names must not write data'
                assert not errors;r['passed']=True
            except Exception:r['failure']=traceback.format_exc()
            r['page_errors']=errors;rows.append(r);c.close();assert dependencies()==files;print(('PASS ' if r['passed'] else 'FAIL ')+kind+' '+str(value),flush=True)
        b.close()
    (out/'results.json').write_text(json.dumps({'dependency_files':files,'producer_sha256':sha(Path(__file__)),'fixture_sha256':sha(ROOT/'verify_pet_controls.py'),'browser':version,'name_scenarios':NAMES,'results':rows,'scope':'25 pet pages, original accessibility-name/title templates, literal and overlapping names, idempotence, controller-owned content, real rename and native cross-tab update. Not real screen-reader/device certification or full114 acceptance.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.stage=='baseline':(out/'producer.py').write_bytes(Path(__file__).read_bytes())
    print('Pet names:',sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
