"""Observe hidden controls after representative initial triggers; check clean Escape closure."""
import ast
import hashlib
import json
import re
import traceback
from urllib.request import urlopen
from playwright.sync_api import sync_playwright, expect
from audit_runtime import INIT, OBSERVE
from audit_current_runtime import data
from verify_pet_controls import ROOT, DEMO, BASE, source

OUT = ROOT / 'evidence/current'
MODULES = {'onboarding':'verify_onboarding_controls.py', 'record':'verify_record_controls.py',
    'moment':'verify_moment_controls.py', 'time':'verify_time_controls.py',
    'workshop':'verify_workshop_controls.py', 'settings':'verify_settings_controls.py',
    'pet':'verify_pet_controls.py', 'book':'verify_book_controls.py'}

def declarations(name):
    """Load fixture declarations, stopping before an unguarded browser runner."""
    path = ROOT / name
    parsed = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    body = []
    for node in parsed.body:
        if isinstance(node, ast.With): break
        if isinstance(node, ast.If) and '__name__' in ast.unparse(node.test): continue
        body.append(node)
    namespace = {'__file__':str(path), '__name__':'overlay_fixture'}
    exec(compile(ast.Module(body=body, type_ignores=[]), str(path), 'exec'), namespace)
    return namespace

def seed_onboarding(page, identifier):
    page.goto(BASE+'prototype/review.html')
    page.evaluate('d=>{localStorage.clear();sessionStorage.clear();for(const[k,v]of Object.entries(d))localStorage.setItem(k,JSON.stringify(v));sessionStorage.setItem("dujia-prototype-peer-response","manual")}', data(False))
    if identifier == 'm01-p05':
        page.evaluate("sessionStorage.setItem('dujia-prototype-challenge',JSON.stringify({purpose:'recovery',verified:true,phone:'13812345678',expiresAt:Date.now()+600000,code:'284631'}))")
    page.goto(BASE+'pages/'+identifier+'.html')
    page.evaluate('document.fonts.ready')

SNAPSHOT = """() => {
 const dialogs=[...document.querySelectorAll('dialog[open]')];
 const observed=(OBSERVE)();
 return dialogs.map(dialog=>({title:dialog.querySelector('h2')?.textContent||dialog.getAttribute('aria-label')||'',
   html:dialog.outerHTML, focus:document.activeElement?.outerHTML,
   bounds:(()=>{const r=dialog.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height}})(),
   controls:observed.controls.filter(control=>{const element=document.querySelector(control.selector);return element&&dialog.contains(element)})}));
}""".replace('OBSERVE', OBSERVE)

def main():
    files = source()
    for path, digest in files.items():
        served = path.replace('custom/', 'pages/', 1) if path.startswith('custom/') else path
        with urlopen(BASE+served, timeout=10) as response:
            assert hashlib.sha256(response.read()).hexdigest()==digest, 'Preview differs from source: '+path
    catalog_path = OUT / 'page-contracts.json'
    catalog = json.loads(catalog_path.read_text(encoding='utf-8'))
    assert catalog['files'] == files
    fixtures = {key:declarations(name) for key,name in MODULES.items()}
    candidates = []
    # This is a broad candidate filter, not a claim of every indirect or nested trigger.
    kinds = re.compile('modal|sheet|more|choose|picker|select|tag|manage|archive|edit|menu|reply|filter|source|template|reward|catalog|unlock|character|guide|member|feedback|device|scope|help|policy|terms|two|storage|delete|logout|unbind|care',re.I)
    for page in catalog['pages']:
        for control in page['control_evidence']:
            if kinds.search(control['contract']):
                group = control['report'].split('/')[-1].split('-controls')[0].split('-control')[0]
                assert group in MODULES, group
                candidates.append({**control, 'page':page['id'], 'group':group})
    rows = []
    def save():
        assert source() == files
        value = dict(files=files,catalog_sha256=hashlib.sha256(catalog_path.read_bytes()).hexdigest(),
            fixture_scripts={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in MODULES.values()},
            candidates=len(candidates),completed=len(rows),results=rows,
            scope='Representative candidate triggers only; nested actions, dirty closure and other conditions remain pending',accepted_pages=0)
        temporary=OUT/'hidden-overlay-observations.json.tmp'
        temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        temporary.replace(OUT/'hidden-overlay-observations.json')
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for index, candidate in enumerate(candidates):
            context=browser.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce',accept_downloads=True)
            context.add_init_script(INIT)
            page=context.new_page();page.set_default_timeout(4500);page.set_default_navigation_timeout(15000)
            errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
            row=dict(candidate,overlays=[])
            try:
                if candidate['group']=='onboarding':seed_onboarding(page,candidate['page'])
                else:fixtures[candidate['group']]['seed'](page,candidate['page'])
                trigger=page.locator(candidate['selector']);expect(trigger).to_be_visible();expect(trigger).to_be_enabled()
                tag=trigger.evaluate('e=>e.tagName')
                row['requested']=page.url
                if tag in ['INPUT','TEXTAREA','SELECT']:
                    row['outcome']='native-field; not an overlay opening probe'
                else:
                    trigger.click();page.wait_for_timeout(750)
                    row['effective']=page.url
                    overlays=page.evaluate(SNAPSHOT);row['overlays']=overlays
                    if overlays:
                        before=page.evaluate('JSON.stringify({...localStorage})')
                        page.keyboard.press('Escape');expect(page.locator('dialog[open]')).to_have_count(0)
                        assert before==page.evaluate('JSON.stringify({...localStorage})'),'Escape changed local storage'
                        row['escape_preserved_storage']=True
                        if page.url==row['effective'] and trigger.count() and trigger.is_visible() and trigger.is_enabled():
                            row['focus_returned']=trigger.evaluate('e=>document.activeElement===e')
                            assert row['focus_returned'],'Escape did not restore trigger focus'
                        row['outcome']='overlay observed; clean Escape checked'
                    else:row['outcome']='no overlay in this initial fixture; other trigger conditions pending'
                assert not errors,errors
                row['passed']=True
            except Exception:
                row.update(passed=False,failure=traceback.format_exc()[-2200:])
            row['errors']=errors;rows.append(row);context.close();save()
            print(('PASS 'if row['passed']else'FAIL ')+str(index+1)+'/'+str(len(candidates))+' '+candidate['page']+' '+candidate['label'].replace('\n',' '),flush=True)
        browser.close()
    save()
    print(json.dumps(dict(candidates=len(candidates),passed=sum(r['passed']for r in rows),overlay_triggers=sum(bool(r['overlays'])for r in rows),hidden_controls=sum(len(o['controls'])for r in rows for o in r['overlays']))))
    raise SystemExit(0 if all(r['passed']for r in rows)else 1)

if __name__=='__main__':main()
