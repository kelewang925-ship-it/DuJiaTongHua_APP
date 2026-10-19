"""Canonical 114-page fixtures: initial mobile geometry and actual keyboard/AX audit."""
import argparse
import ast
import hashlib
import json
import traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from audit_current_runtime import data
from verify_pet_controls import ROOT,DEMO,BASE,source

def load_seed(name):
    # Older verification scripts run tests at import time. Read only the existing
    # fixture function and its two literal/config declarations, never their harness.
    tree=ast.parse((ROOT/('verify_'+name+'_controls.py')).read_text(encoding='utf-8'))
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='seed'
           or isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id in ['PAGES','QUERY']for t in n.targets)]
    namespace=dict(data=data,BASE=BASE,expect=expect)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),name+' fixture','exec'),namespace)
    return namespace['seed']

record_seed,moment_seed,time_seed,workshop_seed,settings_seed,pet_seed,book_seed=[load_seed(name)for name in ['record','moment','time','workshop','settings','pet','book']]

OBSERVE="""() => {
 const visible=e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>0&&r.height>0&&s.visibility!=='hidden'&&s.display!=='none'};
 const elements=[...document.querySelectorAll('button,a[href],input,textarea,select,[role=button],[role=switch],[role=tab]')].filter(visible);
 const metrics=elements.map((e,i)=>{
  e.dataset.auditId=String(i);let target=e;const style=getComputedStyle(e);
  if(e.matches('input')&&e.labels?.length&&(style.pointerEvents==='none'||Number(style.opacity)===0))target=e.labels[0];
  target.scrollIntoView({block:'center',inline:'nearest',behavior:'instant'});
  const r=target.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);
  let fixed=false;for(let node=target;node;node=node.parentElement)if(getComputedStyle(node).position==='fixed')fixed=true;
  let tabbable=!e.disabled&&e.tabIndex>=0;
  if(e.matches('input[type=radio]')&&e.name){const group=elements.filter(x=>x.matches('input[type=radio]')&&x.name===e.name);tabbable=tabbable&&(group.find(x=>x.checked)||group[0])===e}
  return {id:String(i),tag:e.tagName,type:e.type,name:e.getAttribute('aria-label')||e.innerText?.trim()||e.name||e.id,
   selector:e.id?'#'+e.id:'[data-audit-id="'+i+'"]',disabled:!!e.disabled,tabbable,
   rect:{x:r.x,y:r.y,width:r.width,height:r.height},hit:!!hit&&(hit===target||target.contains(hit)),
   fixed,safeTop:!fixed||r.y>=43,safeBottom:!fixed||r.bottom<=innerHeight-33,
   labelled:!e.matches('input:not([type=hidden]):not([type=submit]):not([type=button]),textarea,select')||!!(e.labels?.length||e.getAttribute('aria-label')||e.getAttribute('aria-labelledby'))};
 });
 return {documentWidth:document.documentElement.scrollWidth,viewportWidth:innerWidth,controls:metrics,
  imagesWithoutAlt:[...document.images].filter(e=>visible(e)&&!e.hasAttribute('alt')).map(e=>e.src)};
}"""

def canonical(p,page):
    module=page[:3];number=int(page[-2:])
    if module in ['m01','m02']:
        p.goto(BASE+'prototype/review.html')
        p.evaluate("d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem('dujia-prototype-peer-response','manual');for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}",data(False))
        if page=='m01-p05':p.evaluate("sessionStorage.setItem('dujia-prototype-challenge',JSON.stringify({purpose:'recovery',verified:true,phone:'13812345678',expiresAt:Date.now()+600000,code:'284631'}))")
        p.goto(BASE+'pages/'+page+'.html')
    elif module=='m03':record_seed(p,page)
    elif module=='m04':(moment_seed if number in [1,2,3,4,16,17]else time_seed)(p,page)
    else:{'m05':workshop_seed,'m06':settings_seed,'m07':pet_seed,'m08':book_seed}[module](p,page)
    p.evaluate('document.fonts.ready')
    p.wait_for_timeout(500)
    assert p.url.split('?')[0].endswith(page+'.html'),(page,p.url)


def keyboard(p,controls):
    expected={c['id']for c in controls if c['tabbable']};seen=set();observations=[]
    p.evaluate('document.activeElement?.blur();window.scrollTo(0,0)')
    for _ in range(len(controls)+5):
        p.keyboard.press('Tab')
        observation=p.evaluate("""()=>{const e=document.activeElement;if(!e||e===document.body)return null;let target=e;
         if(e.matches('input')&&e.labels?.length&&Number(getComputedStyle(e).opacity)===0)target=e.labels[0];
         const s=getComputedStyle(target);return {id:e.dataset.auditId||null,tag:e.tagName,name:e.getAttribute('aria-label')||e.innerText?.trim()||e.name,
          focusVisible:e.matches(':focus-visible'),outline:s.outlineStyle!=='none'&&parseFloat(s.outlineWidth)>0&&s.outlineColor!=='rgba(0, 0, 0, 0)',shadow:s.boxShadow};}""")
        if observation:
            if observation['id']in seen:break
            if observation['id']is not None:seen.add(observation['id'])
            observations.append(observation)
    return dict(expected=sorted(expected),visited=observations,unreached=sorted(expected-seen),
                noVisibleFocus=[v for v in observations if not v['focusVisible']or not v['outline']])


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--modules',default='m01,m02,m03,m04,m05,m06,m07,m08');parser.add_argument('--widths',default='390');args=parser.parse_args()
    modules=args.modules.split(',');widths=list(map(int,args.widths.split(',')));files=source();styles={p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in (DEMO/'assets').glob('*.css')}
    manifest=json.loads((DEMO/'manifest.json').read_text(encoding='utf-8'));pages=[v['id']for v in manifest if v['id'][:3]in modules]
    out=ROOT/'evidence/current/initial-quality';out.mkdir(parents=True,exist_ok=True);rows=[]
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for width in widths:
            for page in pages:
                context=browser.new_context(viewport=dict(width=width,height=844),reduced_motion='reduce');p=context.new_page();p.set_default_timeout(6000);p.set_default_navigation_timeout(10000);errors=[];p.on('pageerror',lambda error:errors.append(str(error)))
                try:
                    canonical(p,page);p.evaluate("document.documentElement.style.setProperty('--ui-safe-top','44px');document.documentElement.style.setProperty('--ui-safe-bottom','34px')")
                    session=context.new_cdp_session(p);tree=session.send('Accessibility.getFullAXTree')['nodes'];missing=[dict(role=n.get('role',{}).get('value'),name=n.get('name',{}).get('value'),backend=n.get('backendDOMNodeId'))for n in tree if not n.get('ignored')and n.get('role',{}).get('value')in ['button','link','textbox','searchbox','combobox','checkbox','radio','switch','tab']and not n.get('name',{}).get('value')]
                    for item in missing:
                        if item['backend']:item['dom']=session.send('DOM.describeNode',dict(backendNodeId=item['backend']))['node']
                    metrics=p.evaluate(OBSERVE);keys=keyboard(p,metrics['controls'])if width==390 else None
                    failures=dict(overflow=metrics['documentWidth']>width,blocked=[c for c in metrics['controls']if not c['disabled']and not c['hit']],small=[c for c in metrics['controls']if not c['disabled']and min(c['rect']['width'],c['rect']['height'])<39.5],unsafe=[c for c in metrics['controls']if not c['safeTop']or not c['safeBottom']],unlabelled=[c for c in metrics['controls']if not c['labelled']],missingNames=missing,imagesWithoutAlt=metrics['imagesWithoutAlt'],keyboardUnreached=keys['unreached']if keys else [],keyboardFocus=keys['noVisibleFocus']if keys else [],errors=errors)
                    row=dict(page=page,width=width,effective=p.url,passed=not any(failures.values()),metrics=metrics,keyboard=keys,failures=failures)
                except Exception:row=dict(page=page,width=width,passed=False,failure=traceback.format_exc()[-2500:],errors=errors)
                rows.append(row);print(('PASS 'if row['passed']else'FINDING ')+page+' '+str(width),flush=True)
                # A DOM/state observation is not a visual acceptance decision.
                context.close()
            assert source()==files
        browser.close()
    result=dict(files=files,styles=styles,modules=modules,widths=widths,results=rows,scope='One canonical initial fixture per114 requested pages; reduced motion,844px height and simulated44/34 safe insets. Geometry at declared widths; actual Tab traversal only390. No hidden-state, contrast, screen-reader or pixel-match acceptance implied.')
    (out/('-'.join(modules)+'-'+args.widths.replace(',','_')+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(cases=len(rows),passed=sum(r['passed']for r in rows),findings=sum(not r['passed']for r in rows))))


if __name__=='__main__':main()
