"""Real existing canvas fields: native nodes, labels, dimensions and shared errors."""
import json,sys,traceback
from html.parser import HTMLParser
from playwright.sync_api import sync_playwright
from audit_hidden_overlays import declarations,MODULES,seed_onboarding
from verify_pet_controls import ROOT,DEMO,BASE,source

SELECTOR='input:not([type=hidden],[type=file],[type=color],[type=range],[type=checkbox],[type=radio]),textarea,select'
class Fields(HTMLParser):
    def __init__(self):super().__init__();self.count=0
    def handle_starttag(self,tag,attrs):
        if tag in ['input','textarea','select']and dict(attrs).get('type','text')not in ['hidden','file','color','range','checkbox','radio']:self.count+=1

def main():
    files=source();baseline='--baseline'in sys.argv;rows=[];pages=[]
    for path in sorted((DEMO/'custom').glob('*.html')):
        parser=Fields();parser.feed(path.read_text(encoding='utf-8'))
        if parser.count:pages.append(path.stem)
    fixtures={name:declarations(module)for name,module in MODULES.items()if name!='onboarding'}
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for width in ([390]if baseline else[320,360,390,414,430]):
            for identifier in pages:
                context=browser.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce');p=context.new_page();p.set_default_timeout(6000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(page=identifier,width=width)
                try:
                    def capture(route):
                        response=route.fetch();body=response.text();route.fulfill(response=response,body='window.__nativeBeforeUI=[...document.querySelectorAll('+json.dumps(SELECTOR)+')].map(e=>({element:e,id:e.id,name:e.name,parent:e.parentElement}));\n'+body)
                    p.route('**/assets/prototype-ui.js',capture)
                    group='onboarding'if identifier.startswith(('m01-','m02-'))else'record'if identifier.startswith('m03-')else('time'if int(identifier[-2:])>=7 else'moment')if identifier.startswith('m04-')else{'m05':'workshop','m06':'settings','m07':'pet','m08':'book'}[identifier[:3]]
                    if group=='onboarding':seed_onboarding(p,identifier)
                    else:fixtures[group]['seed'](p,identifier)
                    assert identifier+'.html'in p.url,p.url
                    p.evaluate('document.fonts.ready')
                    observations=p.evaluate('''selector=>[...document.querySelectorAll(selector)].map(e=>{
                      const before=window.__nativeBeforeUI.find(v=>v.element===e),r=e.getBoundingClientRect();
                      return {id:e.id,name:e.name,tag:e.tagName,type:e.type,value:e.value,maxLength:e.maxLength,readonly:e.readOnly,disabled:e.disabled,
                        shared:e.dataset.prototypeField==='canvas',identity:!!before&&before.parent===e.parentElement&&(!before.id||before.id===e.id)&&before.name===e.name,
                        label:e.getAttribute('aria-label')||e.getAttribute('aria-labelledby')||[...e.labels||[]].map(l=>l.textContent).join(''),
                        error:e.dataset.prototypeError,description:e.getAttribute('aria-describedby'),visible:!!e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden',
                        rect:{left:r.left,right:r.right,width:r.width,height:r.height}}})''',SELECTOR)
                    assert observations, 'No actual fields'
                    row['fields']=observations
                    for field in observations:
                        assert field['identity']and field['shared']and field['label']and field['error'],field
                        assert field['error']in field['description'].split(),field
                        if not field['visible']:continue
                        assert field['rect']['height']>=43.9 and field['rect']['width']>=43.9,field
                        assert field['rect']['left']>=-1 and field['rect']['right']<=width+1,field
                        result=p.evaluate('''id=>{const e=document.getElementById(id),value=e.value,store=JSON.stringify({...localStorage}),error=document.getElementById(e.dataset.prototypeError);PrototypeUI.fieldError(e,'请核对当前输入');const r=error.getBoundingClientRect(),f=e.getBoundingClientRect();const shown=!error.hidden&&error.textContent==='请核对当前输入'&&error.getAttribute('role')==='alert'&&e.getAttribute('aria-invalid')==='true';e.dispatchEvent(new Event('input',{bubbles:true}));return {shown,cleared:error.hidden&&e.getAttribute('aria-invalid')==='false',retained:e.value===value,storeUnchanged:JSON.stringify({...localStorage})===store,bounds:{left:r.left,right:r.right,width:r.width,height:r.height,anchorDelta:r.top-f.bottom}}}''',field['id'])
                        assert result['shown']and result['cleared']and result['storeUnchanged'],result
                        assert result['bounds']['left']>=-1 and result['bounds']['right']<=width+1 and result['bounds']['height']>0,result
                        assert 2<=result['bounds']['anchorDelta']<=6 or 2<=-result['bounds']['anchorDelta']-result['bounds']['height']-field['rect']['height']<=6,result
                    assert not errors,errors;row['passed']=True
                except Exception:row.update(passed=False,failure=traceback.format_exc()[-1800:])
                row['errors']=errors;rows.append(row);context.close();assert source()==files
            print(str(width)+'px '+str(sum(r['passed']for r in rows if r['width']==width))+'/'+str(len(pages)),flush=True)
        context=browser.new_context();p=context.new_page();row={'case':'adapter-preserves-native-contract'}
        try:
            fixtures['record']['seed'](p,'m03-p05')
            result=p.evaluate('''()=>{const canvas=document.querySelector('.screen'),input=document.createElement('input'),help=document.createElement('span');help.id='contract-help';help.textContent='原有帮助';input.id='contract-original';input.name='original';input.value='原稿';input.maxLength=8;input.readOnly=true;input.disabled=true;input.setAttribute('aria-label','原字段');input.setAttribute('aria-describedby',help.id);input.style.cssText='position:absolute;left:40px;top:400px;width:160px;height:48px';let calls=0;input.addEventListener('input',()=>calls++);canvas.append(help,input);const before=input.getBoundingClientRect(),field=PrototypeUI.components.field({element:input,label:'错误标签',value:'错误值',name:'错误名',maxLength:2}),again=PrototypeUI.components.field({element:input}),after=input.getBoundingClientRect();field.setError('请核对');input.dispatchEvent(new Event('input'));const result={sameNode:field.input===input&&field.root===input&&input.parentElement===canvas,id:input.id,name:input.name,value:input.value,max:input.maxLength,readonly:input.readOnly,disabled:input.disabled,label:input.getAttribute('aria-label'),help:input.getAttribute('aria-describedby').split(' ').includes(help.id),sameResult:field===again,errorCount:canvas.querySelectorAll('#'+field.error.id).length,cleared:field.error.hidden&&input.getAttribute('aria-invalid')==='false',listenerCalls:calls,geometry:[before.x,before.y,before.width,before.height].every((v,i)=>v===[after.x,after.y,after.width,after.height][i])};input.remove();help.remove();field.error.remove();return result}''')
            row['observed']=result;assert result==dict(sameNode=True,id='contract-original',name='original',value='原稿',max=8,readonly=True,disabled=True,label='原字段',help=True,sameResult=True,errorCount=1,cleared=True,listenerCalls=1,geometry=True),result;row['passed']=True
        except Exception:row.update(passed=False,failure=traceback.format_exc()[-1600:])
        rows.append(row);context.close();browser.close()
    path=ROOT/('evidence/baseline/native-shared-fields-before.json'if baseline else'evidence/current/native-shared-fields-results.json');path.write_text(json.dumps(dict(files=files,pages=pages,results=rows,accepted_pages=0,scope='Existing native node/label identity and associated error/clear geometry at five widths; each page seeded in one explicit current fixture. Not final flow/keyboard/visual acceptance.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(cases=len(rows),passed=sum(r['passed']for r in rows))));raise SystemExit(0 if all(r['passed']for r in rows)else 1)

if __name__=='__main__':main()
