"""Actual shared component classes and computed tokens, plus static candidates."""
import hashlib,json,re,traceback
from html.parser import HTMLParser
from pathlib import Path
from playwright.sync_api import sync_playwright
from audit_current_runtime import data,query
from audit_runtime import INIT
from verify_pet_controls import ROOT,DEMO,BASE,source

SELECTORS={'Button':'.prototype-component-button','Input':'.prototype-component-field input','Textarea':'.prototype-component-field textarea',
'Card':'.prototype-component-card','Header':'.prototype-component-header','AppModal':'dialog.prototype-modal:not(.prototype-sheet)[open]',
'BottomSheet':'dialog.prototype-sheet[open]','Toast':'.prototype-toast','EmptyState':'.prototype-component-state[data-kind=empty]',
'Loading':'.prototype-component-loading','ErrorState':'.prototype-component-state[data-kind=error]',
'Avatar':'.prototype-component-avatar','Tag':'.prototype-component-tag','Divider':'.prototype-component-divider'}
OUT=ROOT/'evidence/current'

class Markup(HTMLParser):
    def __init__(self):super().__init__();self.counts={};self.css=[];self.in_style=False
    def handle_starttag(self,tag,attrs):
        self.counts[tag]=self.counts.get(tag,0)+1
        if tag=='style':self.in_style=True
        for key,value in attrs:
            if key=='style':self.css.append(value)
    def handle_endtag(self,tag):
        if tag=='style':self.in_style=False
    def handle_data(self,text):
        if self.in_style:self.css.append(text)

def styles(paths):
    found={}
    def read(path):
        path=path.resolve()
        if path in found:return
        text=path.read_text(encoding='utf-8');found[path]=text
        for name in re.findall(r'@import\s+url\([\'\"]?([^\'\"\)]+)',text):
            if not name.startswith(('http:','https:','data:')):read(path.parent/name)
    for name in paths:read(DEMO/name)
    return found

def main():
    files=source();catalog_raw=(OUT/'page-contracts.json').read_bytes();catalog=json.loads(catalog_raw);assert catalog['files']==files
    pages=catalog['pages'];assert len(pages)==114
    shared_css=styles(['assets/prototype-ui.css','assets/ui-foundation.css'])
    tokens=sorted(set(re.findall(r'(--(?:prototype|ui)-[\w-]+)\s*:', '\n'.join(shared_css.values()))))
    definitions={str(path.relative_to(DEMO)):hashlib.sha256(path.read_bytes()).hexdigest()for path in shared_css}
    static=[]
    for entry in pages:
        html=DEMO/entry['html'];parser=Markup();parser.feed(html.read_text(encoding='utf-8'));css=styles(entry['stylesheets'])
        dependencies=[html,*css.keys(),*[DEMO/name for name in entry['controllers']]]
        calls=[]
        for name in entry['controllers']:
            if name.endswith('/prototype-ui.js'):continue
            text=(DEMO/name).read_text(encoding='utf-8')
            for match in re.finditer(r'components\.(button|field|card|header|state|loading|avatar|tag|divider)\b',text):
                calls.append(dict(file=name,line=text[:match.start()].count('\n')+1,api=match.group(1)))
        inline='\n'.join(parser.css)
        static.append(dict(page=entry['id'],type=entry['type'],html_elements=parser.counts,
            inline_colors=sorted(set(re.findall(r'#[0-9a-fA-F]{3,8}\b',inline))),inline_variable_references=sorted(set(re.findall(r'var\((--[\w-]+)',inline))),
            controller_shared_call_candidates=calls,dependencies={str(path.relative_to(DEMO)):hashlib.sha256(path.read_bytes()).hexdigest()for path in dependencies}))
    rows=[]
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for populated in [False,True]:
            context=browser.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');context.add_init_script(INIT)
            for entry in pages:
                page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                row=dict(page=entry['id'],scenario='populated'if populated else'empty')
                try:
                    page.goto(BASE+'prototype/review.html')
                    page.evaluate('d=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-06");for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v))}',data(populated))
                    page.goto(BASE+'pages/'+entry['id']+'.html'+query(entry['id'],populated))
                    for attempt in range(6):
                        try:
                            page.wait_for_load_state('domcontentloaded');page.evaluate('document.fonts.ready');url=page.url;page.wait_for_timeout(650)
                            if url!=page.url:continue
                            observed=page.evaluate('''arg=>{
                              const visible=e=>!!e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden';
                              const counts=Object.fromEntries(Object.entries(arg.selectors).map(([name,selector])=>[name,[...document.querySelectorAll(selector)].filter(visible).length]));
                              const css=getComputedStyle(document.documentElement),tokens=Object.fromEntries(arg.tokens.map(name=>[name,css.getPropertyValue(name).trim()]));
                              const native=Object.fromEntries(['button','input','textarea','select','header','article','hr'].map(tag=>[tag,[...document.querySelectorAll(tag)].filter(visible).length]));
                              return {counts,tokens,native};
                            }''',dict(selectors=SELECTORS,tokens=tokens));break
                        except Exception as error:
                            if attempt==5 or not any(s in str(error)for s in['Execution context was destroyed','Cannot find context']):raise
                    else:raise RuntimeError('Page did not settle')
                    expected=next(v['effective']for v in entry['runtime']if v['scenario']==row['scenario'])
                    assert page.url==expected,(page.url,expected)
                    assert not errors,errors;row.update(passed=True,effective=page.url,observed=observed)
                except Exception:row.update(passed=False,effective=page.url,failure=traceback.format_exc()[-2200:])
                row['errors']=errors;rows.append(row);page.close();assert source()==files
                value=dict(files=files,catalog_sha256=hashlib.sha256(catalog_raw).hexdigest(),selectors=SELECTORS,tokens=tokens,
                    shared_stylesheets=definitions,static_pages=static,observations=rows,accepted_pages=0,
                    scope='Initial empty/populated rendering only; static calls are candidates; local color literals may be intentional artwork; no per-page exception accepted automatically')
                temp=OUT/'component-coverage-observations.json.tmp';temp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temp.replace(OUT/'component-coverage-observations.json')
                if len(rows)%19==0:print('Observed '+str(len(rows))+'/228 components; failures='+str(sum(not r['passed']for r in rows)),flush=True)
            context.close()
        browser.close()
    print(json.dumps(dict(pages=114,observations=len(rows),passed=sum(r['passed']for r in rows),component_types=len(SELECTORS),tokens=len(tokens))))
    raise SystemExit(0 if all(r['passed']for r in rows)else 1)

if __name__=='__main__':main()
