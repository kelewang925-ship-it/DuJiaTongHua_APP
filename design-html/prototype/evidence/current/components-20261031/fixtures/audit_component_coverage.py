"""Actual shared component classes and computed tokens, plus static candidates."""
import hashlib,json,re,sys,traceback,uuid
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse,parse_qs
from playwright.sync_api import sync_playwright
from audit_current_runtime import data,query
from audit_runtime import INIT
from verify_pet_controls import ROOT,DEMO,BASE,source

SELECTORS={'Button':'.prototype-component-button','Input':'.prototype-component-field input,input[data-prototype-field=canvas]','Textarea':'.prototype-component-field textarea,textarea[data-prototype-field=canvas]',
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
    rows=[];retained=[];replayed=[];baseline_sha=None;repair='--replay-random-drafts'in sys.argv
    if repair:
        baseline_raw=(ROOT/'evidence/baseline/component-coverage-before-route-fix.json').read_bytes();baseline=json.loads(baseline_raw)
        assert baseline['files']==files and baseline['catalog_sha256']==hashlib.sha256(catalog_raw).hexdigest()
        assert baseline['static_pages']==static and baseline['shared_stylesheets']==definitions
        assert len(baseline['observations'])==228
        assert {(r['page'],r['scenario'])for r in baseline['observations']if not r['passed']}=={(p,'empty')for p in['m05-p03','m05-p04','m05-p05']}
        rows=baseline['observations'];retained=[i for i,r in enumerate(rows)if r['passed']];assert len(retained)==225
        baseline_sha=hashlib.sha256(baseline_raw).hexdigest()
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for populated in [False,True]:
            context=browser.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');context.add_init_script(INIT)
            for entry in pages:
                if repair and (populated or entry['id']not in['m05-p03','m05-p04','m05-p05']):continue
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
                    if not populated and entry['id']in['m05-p03','m05-p04','m05-p05']:
                        actual=urlparse(page.url);prior=urlparse(expected);assert actual.scheme==prior.scheme and actual.netloc==prior.netloc and actual.path==prior.path
                        params=parse_qs(actual.query);assert set(params)=={'id'}and len(params['id'])==1
                        identifier=params['id'][0];assert identifier.startswith('work-')and uuid.UUID(identifier[5:]).version==4
                        work=page.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-works"))');assert len(work)==1 and work[0]['id']==identifier and work[0]['status']=='draft'
                        assert work[0]['type']==('film'if entry['id']=='m05-p05'else'comic')and work[0]['sourceKind']==('photo'if entry['id']=='m05-p04'else'free')
                        row['generated_draft_contract']=dict(id=identifier,status=work[0]['status'],type=work[0]['type'],sourceKind=work[0]['sourceKind'])
                    else:assert page.url==expected,(page.url,expected)
                    assert not errors,errors;row.update(passed=True,effective=page.url,observed=observed)
                except Exception:row.update(passed=False,effective=page.url,failure=traceback.format_exc()[-2200:])
                row['errors']=errors
                if repair:
                    index=next(i for i,r in enumerate(rows)if r['page']==row['page']and r['scenario']==row['scenario']);rows[index]=row;replayed.append(index)
                else:rows.append(row)
                page.close();assert source()==files
                value=dict(files=files,catalog_sha256=hashlib.sha256(catalog_raw).hexdigest(),selectors=SELECTORS,tokens=tokens,
                    shared_stylesheets=definitions,static_pages=static,observations=rows,accepted_pages=0,
                    scope='Initial empty/populated rendering only; static calls are candidates; local color literals may be intentional artwork; no per-page exception accepted automatically',
                    retained_baseline_sha256=baseline_sha,retained_indices=retained,replayed_indices=replayed)
                temp=OUT/'component-coverage-observations.json.tmp';temp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temp.replace(OUT/'component-coverage-observations.json')
                if repair:print('REPLAY '+row['page']+' '+str(len(replayed))+'/3 '+('PASS'if row['passed']else'FAIL'),flush=True)
                elif len(rows)%19==0:print('Observed '+str(len(rows))+'/228 components; failures='+str(sum(not r['passed']for r in rows)),flush=True)
            context.close()
        browser.close()
    print(json.dumps(dict(pages=114,observations=len(rows),passed=sum(r['passed']for r in rows),component_types=len(SELECTORS),tokens=len(tokens))))
    raise SystemExit(0 if all(r['passed']for r in rows)else 1)

if __name__=='__main__':main()
