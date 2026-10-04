"""Observe all initial controls and registered handlers in an isolated browser."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent
INIT="""(() => {
  const registrations=new WeakMap();
  const original=EventTarget.prototype.addEventListener;
  EventTarget.prototype.addEventListener=function(type,listener,options){
    const items=registrations.get(this)||[];
    items.push({type,handler:String(listener)});registrations.set(this,items);
    return original.call(this,type,listener,options);
  };
  window.__prototypeRegistrations=registrations;
})();"""
OBSERVE="""() => {
 const named=e=>e.getAttribute('aria-label')||e.innerText?.trim()||e.placeholder||e.name||e.id||e.tagName;
 const events=e=>window.__prototypeRegistrations.get(e)||[];
 const visible=e=>!!e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden';
 const path=e=>{if(e.id)return '#'+e.id;const parts=[];while(e&&e.nodeType===1&&e!==document.body){const siblings=[...e.parentElement.children].filter(x=>x.tagName===e.tagName);parts.unshift(e.tagName.toLowerCase()+':nth-of-type('+(siblings.indexOf(e)+1)+')');e=e.parentElement;}return 'body>'+parts.join('>');};
 const controls=[...document.querySelectorAll('button,a,input,textarea,select,[role=button],[role=switch],[role=checkbox],[role=tab],[onclick]')].map(e=>{
  const ancestors=[];for(let a=e.parentElement;a;a=a.parentElement){const bound=events(a).filter(x=>['click','submit','change','input','keydown'].includes(x.type));if(bound.length)ancestors.push({selector:path(a),events:bound});}
  const form=e.form;const inherited=form?events(form):[];
  const own=events(e),inline=e.getAttribute('onclick')||e.getAttribute('onchange')||(e.onclick?String(e.onclick):'')||(e.onchange?String(e.onchange):'');
  const native=['INPUT','TEXTAREA','SELECT'].includes(e.tagName);
  const href=e.getAttribute('href');
  const submit=e.tagName==='BUTTON'&&(e.type==='submit')&&form;
  const delegated=ancestors.some(a=>a.events.some(x=>x.type==='click'))||events(document).some(x=>x.type==='click')||typeof document.onclick==='function';
  const handled=native||inline||own.some(x=>['click','keydown','pointerdown'].includes(x.type))||href&&href!=='#'||submit&&inherited.some(x=>x.type==='submit')||delegated;
  return {selector:path(e),tag:e.tagName,label:named(e),visible:visible(e),disabled:!!e.disabled,role:e.getAttribute('role'),type:e.type,href,inline,own_events:own,ancestor_events:ancestors,form_events:inherited,has_candidate_behavior:!!handled,native_input:native,aria_selected:e.getAttribute('aria-selected'),aria_pressed:e.getAttribute('aria-pressed'),rect:(()=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height}})()};
 });
 return {title:document.title,controls,global_events:events(document),body_events:events(document.body),states:[...document.querySelectorAll('[role=dialog],[role=alertdialog],[role=status],[role=alert],.modal,.sheet,.toast,.empty,.loading,.error')].map(e=>({selector:path(e),role:e.getAttribute('role'),visible:visible(e),text:e.textContent.trim()})),css_variables:Object.fromEntries(['--ui-focus','--ui-focus-soft','--ui-safe-top','--ui-safe-bottom'].map(k=>[k,getComputedStyle(document.documentElement).getPropertyValue(k)])),forms:[...document.forms].map(e=>({selector:path(e),events:events(e)})),width:document.documentElement.scrollWidth};
}"""

def main():
 manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
 results=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
  context=browser.new_context(viewport={'width':390,'height':844})
  context.add_init_script(INIT)
  for i,entry in enumerate(manifest):
   page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto('http://127.0.0.1:8765/pages/'+entry['id']+'.html');page.evaluate('document.fonts.ready')
   data=page.evaluate(OBSERVE);data.update(id=entry['id'],page_errors=errors,url=page.url)
   results.append(data);page.close()
   if (i+1)%20==0:print(f"Observed {i+1}/{len(manifest)} pages",flush=True)
  browser.close()
 (OUT/'baseline-runtime.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
 candidates=[{'id':r['id'],'selector':c['selector'],'label':c['label']} for r in results for c in r['controls'] if c['visible'] and not c['disabled'] and not c['has_candidate_behavior']]
 summary={'pages_observed':len(results),'controls_observed':sum(len(r['controls']) for r in results),'visible_unbound_candidates':candidates,'pages_with_errors':[{'id':r['id'],'errors':r['page_errors']} for r in results if r['page_errors']]}
 (OUT/'runtime-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'pages_observed':summary['pages_observed'],'controls_observed':summary['controls_observed'],'visible_unbound_candidates':len(candidates),'pages_with_errors':summary['pages_with_errors']},ensure_ascii=False,indent=2),flush=True)

if __name__=='__main__':main()
