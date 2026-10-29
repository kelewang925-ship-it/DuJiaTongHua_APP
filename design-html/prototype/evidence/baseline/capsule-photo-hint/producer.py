"""The capsule photo hint must remain readable through actual native image I/O states."""
import argparse,hashlib,json,re,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_hidden_overlays import declarations
from verify_image_read_order import GATE,A,choose,finish,uri

ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def dependencies():
    text=(DEMO/'custom/m04-p13.html').read_text(encoding='utf-8')
    names={'custom/m04-p13.html','pages/m04-p13.html','assets/m04-p13-art.webp','assets/font.ttf','assets/prototype-components.css'}
    names.update('assets/'+s for s in re.findall(r'(?:src|href)="\.\./assets/([^"]+)"',text))
    return {n:sha(DEMO/n) for n in sorted(names)}

def image(p):
    choose(p,'#photo',A,'memory.svg');expect(p.locator('#chosen')).to_have_text('1 张照片已选择');expect(p.locator('.prototype-capsule-preview')).to_be_visible()
    p.wait_for_function('document.querySelector(".prototype-capsule-preview").naturalWidth>0')

def geometry(p):
    return p.locator('#chosen').evaluate('''e=>{
      const r=e.getBoundingClientRect(),range=document.createRange();range.selectNodeContents(e);const ink=range.getBoundingClientRect();
      const style=getComputedStyle(e),z=el=>Number.parseInt(getComputedStyle(el).zIndex)||0;
      const overlap=(a,b)=>Math.min(a.right,b.right)-Math.max(a.left,b.left)>.5&&Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>.5;
      const slot=document.querySelector('.prototype-capsule-photo-slot');
      const covered=overlap(r,slot.getBoundingClientRect())&&(z(e)<z(slot)||(z(e)===z(slot)&&!!(e.compareDocumentPosition(slot)&Node.DOCUMENT_POSITION_FOLLOWING)));
      const controls=[document.querySelector('.add-photo'),document.querySelector('.prototype-capsule-remove'),document.querySelector('.opening')].filter(el=>el.getClientRects().length);
      return {rect:r.toJSON(),text:ink.toJSON(),font:style.fontSize,z:style.zIndex,covered,clipped:e.scrollWidth>e.clientWidth+1||ink.right>r.right+1,controlOverlap:controls.filter(el=>overlap(r,el.getBoundingClientRect())).map(el=>el.className),inside:r.left>=0&&r.right<=innerWidth&&r.bottom<=document.querySelector('.screen').getBoundingClientRect().bottom};
    }''')

def flow(p,name,fixture):
    fixture['seed'](p,'m04-p13');before=fixture['store'](p);image(p);selected=p.locator('.prototype-capsule-preview').get_attribute('src')
    if name.startswith('photo-back-'):
        back=lambda:p.go_back() if name.endswith('browser') else p.locator('.back').click()
        back();expect(p.locator('dialog h2')).to_have_text('是否放弃当前修改？');p.get_by_role('button',name='继续编辑',exact=True).click();expect(p.locator('#chosen')).to_have_text('1 张照片已选择');assert p.locator('.prototype-capsule-preview').get_attribute('src')==selected
        back();p.get_by_role('button',name='放弃修改',exact=True).click();p.wait_for_url('**/m04-p12.html');assert fixture['store'](p)==before;return
    if name=='invalid-replacement':
        choose(p,'#photo',b'not a valid image','broken.svg');expect(p.locator('.prototype-toast')).to_contain_text('图片');expect(p.locator('#chosen')).to_have_text('1 张照片已选择');assert p.locator('.prototype-capsule-preview').get_attribute('src')==selected;assert fixture['store'](p)==before;return
    p.locator('#name').fill('照片提示回归');p.locator('#message').fill('保存后仍保留真正选中的照片')
    if name=='draft-remove':
        p.locator('#draft').click();p.wait_for_url('**/m04-p12.html');saved=p.evaluate('PrototypeCapsules.all().find(v=>v.name==="照片提示回归")');assert saved['photo']==selected
        p.goto('http://127.0.0.1:8765/pages/m04-p13.html?id='+saved['id']);expect(p.locator('#chosen')).to_have_text('1 张照片已选择');p.get_by_role('button',name='移除照片',exact=True).click();expect(p.locator('#chosen')).to_have_text('可选 · 留下一张照片');p.locator('#draft').click();p.wait_for_url('**/m04-p12.html');assert p.evaluate('id=>PrototypeCapsules.find(id).photo',saved['id']) is None
    elif name=='seal-retry':
        p.evaluate('sessionStorage.setItem("dujia-prototype-fail-next","capsule-save")');p.get_by_role('button',name='封存这份心意',exact=True).click();expect(p.locator('.prototype-toast')).to_contain_text('重试');assert fixture['store'](p)==before;expect(p.locator('#chosen')).to_have_text('1 张照片已选择')
        p.get_by_role('button',name='封存这份心意',exact=True).click();p.wait_for_url('**/m04-p15.html?id=*');saved=p.evaluate('PrototypeCapsules.all().find(v=>v.name==="照片提示回归")');assert saved['photo']==selected and saved['status']=='sealed';expect(p.locator('img')).to_have_count(0)
    else:raise AssertionError(name)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['baseline','current'],required=True);args=parser.parse_args()
    out=ROOT/f'evidence/{args.stage}/capsule-photo-hint';out.mkdir(parents=True,exist_ok=True);assert not (out/'results.json').exists(),'Preserve old reports first'
    fixture=declarations('verify_time_controls.py');files=dependencies();cases=[('layout',(w,state)) for w in [320,360,390,414,430] for state in ['empty','selected','removed','pending']]
    if args.stage=='current':
        catalog=json.loads((ROOT/'evidence/current/page-contracts.json').read_text(encoding='utf-8'));cases += [('control',c) for c in next(r for r in catalog['pages'] if r['id']=='m04-p13')['control_evidence']]
        cases += [('flow',name) for name in ['photo-back-button','photo-back-browser','invalid-replacement','draft-remove','seal-retry']]
    rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=b.version
        for kind,value in cases:
            c=b.new_context(viewport={'width':value[0] if kind=='layout' else 390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));r={'kind':kind,'value':value,'passed':False}
            try:
                if kind=='control':fixture['control'](p,'m04-p13',value,fixture['contract']('m04-p13',value))
                elif kind=='flow':flow(p,value,fixture)
                else:
                    width,state=value;fixture['seed'](p,'m04-p13');before=fixture['store'](p)
                    if state in ['selected','removed']:image(p)
                    if state=='removed':p.get_by_role('button',name='移除照片',exact=True).click();expect(p.locator('.prototype-capsule-preview')).to_be_hidden()
                    if state=='pending':p.evaluate(GATE);choose(p,'#photo',A,'pending.svg');expect(p.locator('#chosen')).to_have_text('正在读取照片…')
                    p.evaluate('document.fonts.ready');r['geometry']=geometry(p)
                    if width==390:p.screenshot(path=str(out/f'{state}.png'),full_page=True)
                    assert not r['geometry']['covered'],'The later photo cover paints over the hint'
                    assert not r['geometry']['clipped'],'Hint glyphs are truncated'
                    assert not r['geometry']['controlOverlap'],r['geometry']['controlOverlap']
                    assert r['geometry']['inside'];assert fixture['store'](p)==before
                    if state=='pending':finish(p,0,A);expect(p.locator('#chosen')).to_have_text('1 张照片已选择')
                assert not errors;r['passed']=True
            except Exception:r['failure']=traceback.format_exc()
            r['page_errors']=errors;rows.append(r);c.close();assert dependencies()==files;print(('PASS ' if r['passed'] else 'FAIL ')+kind+' '+str(value),flush=True)
        b.close()
    (out/'results.json').write_text(json.dumps({'dependency_files':files,'producer_sha256':sha(Path(__file__)),'fixture_sha256':sha(ROOT/'verify_time_controls.py'),'image_fixture_sha256':sha(ROOT/'verify_image_read_order.py'),'browser':version,'results':rows,'scope':'Single capsule editor photo hint: four actual image I/O states at five widths, original initial controls and five named photo/save/return flows. No full114 replay or human acceptance.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.stage=='baseline':(out/'producer.py').write_bytes(Path(__file__).read_bytes())
    print('Capsule hint:',sum(r['passed'] for r in rows),'/',len(rows));raise SystemExit(0 if all(r['passed'] for r in rows) else 1)

if __name__=='__main__':main()
