"""Exercise14 shared component contracts and observe current114 canonical pages."""
import json,re,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
import audit_initial_quality as Q
from audit_component_coverage import SELECTORS
from replay_current_initial_controls import ROOT,DEMO,deps,fixture_files,sha,dump

OUT=ROOT/'evidence/current/components-20261031'
KINDS=list(SELECTORS)

def dependencies():return {**deps(),'prototype/components.html':sha(ROOT/'components.html')}

def contract(p,kind):
    p.goto('http://127.0.0.1:8765/prototype/components.html');p.evaluate('document.fonts.ready')
    p.evaluate("()=>{document.querySelector('main').replaceChildren(Object.assign(document.createElement('section'),{id:'contract'}));window.hits=0;window.changed=null;}")
    p.evaluate('''kind=>{const U=PrototypeUI,C=U.components,box=document.querySelector('#contract');
      const mark=e=>{e.id='subject';box.append(e);return e;};
      if(kind==='Button'){for(const variant of ['primary','secondary','text','icon','danger']){const e=C.button(variant,()=>window.hits++,{variant,name:variant});e.dataset.test=variant;box.append(e);}const disabled=C.button('disabled',()=>window.hits++,{disabled:true});disabled.id='disabled';box.append(disabled);window.busy=C.button('busy',()=>U.busy(window.busy,'waiting',()=>{window.hits++;return true;}));box.append(window.busy);}
      if(kind==='Input'||kind==='Textarea'){window.field=C.field({label:'contract field',multiline:kind==='Textarea',maxLength:12,placeholder:'required'});mark(field.root);box.append(C.field({label:'disabled field',disabled:true,value:'kept'}).root);}
      if(kind==='Card'){box.append(C.card({title:'static card',message:'information'}));mark(C.card({title:'action card',selected:false,onClick:event=>{window.hits++;event.currentTarget.setAttribute('aria-pressed','true');}}));}
      if(kind==='Header')mark(C.header({title:'共享组件长标题文字可以完整换行显示',transparent:true,onBack:()=>window.hits++,action:C.button('help',()=>window.hits++)}));
      if(kind==='AppModal')mark(C.button('open',()=>{window.result=null;U.modal({title:'contract modal',message:'cancel or confirm',cancel:'cancel',confirm:'confirm'}).then(value=>window.result=value);}));
      if(kind==='BottomSheet')mark(C.button('open',()=>{window.result=null;U.sheet({title:'contract sheet',actions:[{label:'choice',value:'chosen'}]}).then(value=>window.result=value);}));
      if(kind==='Toast')mark(C.button('notify',()=>U.toast('contract notification','success')));
      if(kind==='EmptyState'||kind==='ErrorState')mark(C.state({kind:kind==='EmptyState'?'empty':'error',title:'state title',message:'state context',action:'continue',onAction:()=>window.hits++}));
      if(kind==='Loading'){box.append(C.loading({mode:'skeleton',label:'skeleton'}),C.loading({mode:'spinner',label:'spinner'}),C.loading({mode:'progress',label:'low',value:-4}),C.loading({mode:'progress',label:'high',value:140}));}
      if(kind==='Avatar')mark(C.avatar({name:'星星',src:'data:image/png;base64,invalid'}));
      if(kind==='Tag'){mark(C.tag({label:'toggle',onChange:value=>window.changed=value}));box.append(C.tag({label:'action',selected:null,onActivate:()=>window.hits++}),C.tag({label:'disabled',disabled:true,onChange:()=>window.hits++}));}
      if(kind==='Divider')mark(C.divider());
    }''',kind)
    subject=p.locator('#subject')
    if kind=='Button':
        for variant in ['primary','secondary','text','icon','danger']:
            button=p.get_by_role('button',name=variant,exact=True);button.click();assert button.bounding_box()['height']>=44
        assert p.evaluate('hits')==5
        p.locator('#disabled').evaluate('e=>e.click()');assert p.evaluate('hits')==5
        p.get_by_role('button',name='busy',exact=True).click();expect(p.get_by_role('button',name='waiting',exact=True)).to_be_disabled();p.wait_for_function('hits===6');expect(p.get_by_role('button',name='busy',exact=True)).to_be_enabled()
    elif kind in ['Input','Textarea']:
        field=p.get_by_label('contract field',exact=True);field.fill('abcdefghijklmnop');expect(field).to_have_value('abcdefghijkl')
        p.evaluate("field.setError('please check')");expect(field).to_have_attribute('aria-invalid','true');expect(p.get_by_text('please check',exact=True)).to_be_visible()
        field.fill('fixed');expect(field).to_have_attribute('aria-invalid','false');expect(p.get_by_label('disabled field',exact=True)).to_be_disabled()
        assert field.bounding_box()['height']>=(96 if kind=='Textarea' else 48)
    elif kind=='Card':
        assert p.get_by_text('static card',exact=True).evaluate('e=>e.parentElement.tagName')=='ARTICLE'
        subject.focus();p.keyboard.press('Enter');assert p.evaluate('hits')==1;expect(subject).to_have_attribute('aria-pressed','true')
    elif kind=='Header':
        subject.get_by_role('button',name='返回',exact=True).click();subject.get_by_role('button',name='help',exact=True).click();assert p.evaluate('hits')==2
        assert subject.evaluate('e=>getComputedStyle(e).backgroundColor')=='rgba(0, 0, 0, 0)'
    elif kind=='AppModal':
        subject.click();expect(p.get_by_role('button',name='cancel',exact=True)).to_be_focused();p.keyboard.press('Escape');p.wait_for_function('window.result===false');expect(subject).to_be_focused()
        subject.click();p.get_by_role('button',name='confirm',exact=True).click();p.wait_for_function('window.result===true');expect(p.locator('dialog')).to_have_count(0)
    elif kind=='BottomSheet':
        subject.click();p.get_by_role('button',name='choice',exact=True).click();p.wait_for_function('window.result==="chosen"');expect(subject).to_be_focused()
        subject.click();p.keyboard.press('Escape');expect(p.locator('dialog')).to_have_count(0);p.wait_for_function('window.result===null')
    elif kind=='Toast':
        subject.click();toast=p.locator('.prototype-toast');expect(toast).to_have_attribute('role','status');expect(toast).to_contain_text('contract notification')
        p.evaluate("PrototypeUI.toast('retry context','error')");expect(toast).to_have_attribute('role','alert');expect(toast).to_contain_text('retry context');expect(toast).not_to_have_class(re.compile('.*is-hidden.*'))
    elif kind in ['EmptyState','ErrorState']:
        expect(subject).to_have_attribute('role','region' if kind=='EmptyState' else 'alert');subject.get_by_role('button',name='continue',exact=True).click();assert p.evaluate('hits')==1
    elif kind=='Loading':
        expect(p.get_by_role('status')).to_have_count(4);expect(p.get_by_role('progressbar',name='low',exact=True)).to_have_attribute('value','0');expect(p.get_by_role('progressbar',name='high',exact=True)).to_have_attribute('value','100')
        spinner=p.locator('.prototype-component-spinner');animation=spinner.evaluate('e=>getComputedStyle(e).animationName')
        assert (animation=='none')==p.evaluate('matchMedia("(prefers-reduced-motion:reduce)").matches')
    elif kind=='Avatar':
        expect(subject.locator('img')).to_have_count(0);expect(subject).to_have_attribute('aria-label','星星');expect(subject).to_have_text('星');assert subject.bounding_box()['height']==48
    elif kind=='Tag':
        subject.click();assert p.evaluate('changed') is True;subject.click();assert p.evaluate('changed') is False
        p.get_by_role('button',name='action',exact=True).click();assert p.evaluate('hits')==1
        assert p.get_by_role('button',name='action',exact=True).get_attribute('aria-pressed') is None
        p.get_by_role('button',name='disabled',exact=True).evaluate('e=>e.click()');assert p.evaluate('hits')==1
    elif kind=='Divider':assert subject.evaluate('e=>e.tagName==="HR"&&e.tabIndex<0')
    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth')

def main():
    OUT.mkdir(parents=True,exist_ok=True);assert not (OUT/'results.json').exists()
    files=dependencies();scripts=fixture_files();scripts.update({n:sha(ROOT/n) for n in [Path(__file__).name,'audit_initial_quality.py','audit_component_coverage.py']})
    for sub,mapping,origin in [('source',files,DEMO),('fixtures',scripts,ROOT)]:
        for n in mapping:
            target=OUT/sub/n;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((origin/n).read_bytes())
    definitions={p.name:sha(p) for p in (DEMO/'assets').glob('*.css')}
    text='\n'.join(p.read_text(encoding='utf-8') for p in (DEMO/'assets').glob('*.css'))
    tokens=sorted(set(re.findall(r'(--(?:prototype|ui)-[\w-]+)\s*:',text)))
    rows=[];pages=[]
    def save():
        assert dependencies()==files and all(sha(ROOT/n)==h for n,h in scripts.items())
        dump(OUT/'results.json',{'dependencies':files,'fixture_sha256':scripts,'tokens':tokens,'css_sha256':definitions,'component_contracts':rows,'page_observations':pages,'complete':len(rows)==56 and len(pages)==114,'all_passed':len(rows)==56 and len(pages)==114 and all(r['passed'] for r in rows+pages),'human_accepted_pages':0,'scope':'14 component behavioral contracts at320/430 in full/reduced motion;114 canonical initial component counts and root token observations. Counts/root values do not prove every dynamic integration or pixel fidelity.'})
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for width in [320,430]:
            for motion in ['no-preference','reduce']:
                for kind in KINDS:
                    context=browser.new_context(viewport={'width':width,'height':844},reduced_motion=motion);p=context.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
                    try:contract(p,kind);assert not errors;row={'component':kind,'width':width,'motion':motion,'passed':True}
                    except Exception:row={'component':kind,'width':width,'motion':motion,'passed':False,'failure':traceback.format_exc()};p.screenshot(path=str(OUT/(kind+'-'+str(width)+'-'+motion+'-finding.png')),full_page=True)
                    row['errors']=errors;rows.append(row);context.close();save()
                print('COMPONENTS',width,motion,sum(r['passed'] for r in rows if r['width']==width and r['motion']==motion),'/14',flush=True)
        ids=[v['id'] for v in json.loads((DEMO/'manifest.json').read_text(encoding='utf-8'))]
        for index,page in enumerate(ids):
            context=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');p=context.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
            try:
                Q.canonical(p,page)
                observation=p.evaluate('''arg=>{const modal=document.querySelector('dialog[open]'),visible=e=>e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden'&&!e.closest('[inert]')&&(!modal||modal.contains(e));const css=getComputedStyle(document.documentElement);return {components:Object.fromEntries(Object.entries(arg.selectors).map(([name,selector])=>[name,[...document.querySelectorAll(selector)].filter(visible).length])),tokens:Object.fromEntries(arg.tokens.map(name=>[name,css.getPropertyValue(name).trim()])),native_modal:!!modal};}''',{'selectors':SELECTORS,'tokens':tokens})
                assert not errors;pages.append({'page':page,'passed':True,'effective':p.url,'observation':observation,'errors':errors})
            except Exception:pages.append({'page':page,'passed':False,'failure':traceback.format_exc(),'errors':errors})
            context.close();save()
            if (index+1)%19==0:print('PAGES',index+1,'/114',flush=True)
        browser.close()
    return 0 if all(r['passed'] for r in rows+pages) else 1

if __name__=='__main__':raise SystemExit(main())
