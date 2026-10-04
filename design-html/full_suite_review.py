"""Fresh cross-module checks for the editable HTML demo; does not change state."""
import json
import re
import argparse
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
ids={x['id'] for x in manifest}
parser=argparse.ArgumentParser()
parser.add_argument('--pages',nargs='+',help='Recheck changed pages and merge unchanged evidence')
args=parser.parse_args()
if args.pages and set(args.pages)-ids:parser.error('Unknown page ID')
static=[]
for item in manifest:
    id=item['id'];source=ROOT/'custom'/f'{id}.html';preview=ROOT/'pages'/f'{id}.html'
    text=source.read_text(encoding='utf-8')
    missing=[]
    for asset in re.findall(r'''(?:src=|href=)["']([^"']+)["']|url\(['"]?([^)'";]+)''',text):
        value=next(x for x in asset if x)
        if value.startswith(('data:','http:','https:','#','${')):continue
        value=value.split('?',1)[0].split('#',1)[0]
        if not (source.parent/value).resolve().exists():missing.append(value)
    routes=set(re.findall(r'm\d{2}-p\d{2}\.html',text))
    static.append({'id':id,'preview_matches_source':source.read_bytes()==preview.read_bytes(),
                   'foundation': 'ui-foundation.css' in text,'viewport_fit':'viewport-fit=cover' in text,
                   'missing_assets':sorted(set(missing)), 'missing_routes':sorted(x for x in routes if x[:-5] not in ids)})

records=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    for item in [x for x in manifest if not args.pages or x['id'] in args.pages]:
        record={'id':item['id'],'checked_at':datetime.now(timezone.utc).isoformat(),
                'html_sha256':hashlib.sha256((ROOT/'pages'/f"{item['id']}.html").read_bytes()).hexdigest(),'widths':{}}
        for width in [320,375,390,414,430]:
            page=browser.new_page(viewport={'width':width,'height':932})
            errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto((ROOT/'pages'/f"{item['id']}.html").as_uri());page.evaluate('document.fonts.ready')
            metrics=page.evaluate('''() => {
              const screen=document.querySelector('.screen').getBoundingClientRect();
              const visible=e=>e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden';
              const name=e=>(e.getAttribute('aria-label')||e.innerText||e.placeholder||e.id||e.name||e.tagName).slice(0,60);
              const controls=[...document.querySelectorAll('button,a,input,textarea,select')].filter(visible);
              const target=e=>{let r=e.getBoundingClientRect();const label=e.closest('label');
                if(label&&e.tagName==='INPUT'&&label.getBoundingClientRect().height>=40)r=label.getBoundingClientRect();
                if(e.classList.contains('ui-hit-text'))return {left:r.left-6,right:r.right+6,top:r.top+r.height/2-22,bottom:r.top+r.height/2+22,width:r.width+12,height:44};return r;};
              const inScroll=e=>{for(let a=e.parentElement;a&&a.className!=='screen';a=a.parentElement)if(['auto','scroll'].includes(getComputedStyle(a).overflowY))return true;return false;};
              const clipped=controls.filter(e=>{if(inScroll(e))return false;const r=target(e);return r.left<screen.left-2||r.right>screen.right+2||r.top<screen.top-2||r.bottom>screen.bottom+2;}).map(e=>({name:name(e),className:e.className}));
              const small=controls.filter(e=>{const r=target(e);return r.width<39.5||r.height<39.5;}).map(name);
              const overflow=[...document.querySelectorAll('button,p,h1,h2,label')].filter(e=>visible(e)&&!e.classList.contains('ui-hit-text')&&e.clientWidth>0&&e.scrollWidth>e.clientWidth+2).filter(e=>{
                if(!e.classList.contains('ui-art-selection'))return true;
                const box=e.getBoundingClientRect(),walker=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);let node;
                while(node=walker.nextNode()){if(!node.textContent.trim())continue;const range=document.createRange();range.selectNodeContents(node);if([...range.getClientRects()].some(r=>r.right>box.right+2||r.left<box.left-2))return true;}return false;
              }).map(name);
              const overlaps=[];
              const buttons=controls.filter(e=>['BUTTON','A'].includes(e.tagName)&&!inScroll(e));
              for(let i=0;i<buttons.length;i++)for(let j=i+1;j<buttons.length;j++){
                const a=buttons[i],b=buttons[j];if(a.contains(b)||b.contains(a))continue;
                const x=target(a),y=target(b),w=Math.min(x.right,y.right)-Math.max(x.left,y.left),h=Math.min(x.bottom,y.bottom)-Math.max(x.top,y.top);
                if(w>4&&h>4)overlaps.push([name(a),name(b),Math.round(w),Math.round(h)]);
              }
              const unnamed=controls.filter(e=>e.tagName==='BUTTON'&&!e.getAttribute('aria-label')&&!e.innerText.trim()&&!e.getAttribute('title')).map(e=>e.className);
              return {documentWidth:document.documentElement.scrollWidth,fontLoaded:document.fonts.check('12px Fairy'),smallTargets:small,textOverflow:overflow,clippedTargets:clipped,overlappingButtons:overlaps,unnamedButtons:unnamed,brokenImages:[...document.images].filter(e=>visible(e)&&(!e.complete||!e.naturalWidth)).map(e=>e.src)};
            }''')
            metrics['pageErrors']=errors
            if width==320:
                page.evaluate("document.documentElement.style.setProperty('--ui-safe-top','44px');document.documentElement.style.setProperty('--ui-safe-bottom','34px')")
                metrics['safeArea']=page.evaluate("()=>{const s=document.querySelector('.screen').getBoundingClientRect();return s.top>=44&&document.documentElement.scrollHeight>=s.height+77&&document.documentElement.scrollWidth===320}")
            record['widths'][str(width)]=metrics;page.close()
        records.append(record);print(item['id'],flush=True)
    browser.close()
if args.pages:
    previous=json.loads((ROOT/'ui-audit/full-suite-results.json').read_text(encoding='utf-8'))['records']
    merged={x['id']:x for x in previous};merged.update({x['id']:x for x in records})
    records=[merged[x['id']] for x in manifest]
result={'checked_at':datetime.now(timezone.utc).isoformat(),'pages':len(records),'width_checks':len(records)*5,'static':static,'records':records}
(ROOT/'ui-audit/full-suite-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('Fresh full-suite evidence saved',flush=True)
