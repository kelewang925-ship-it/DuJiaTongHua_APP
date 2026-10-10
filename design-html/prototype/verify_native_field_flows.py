"""Reexecute actual save/stash/reply and input-limit contracts affected by native field adoption."""
import hashlib,json,traceback
from playwright.sync_api import sync_playwright
from audit_runtime import INIT
from audit_hidden_overlays import MODULES,declarations
from verify_pet_controls import ROOT,source

POSITIVE={'diary-draft','diary-save','photo-save','reply','create','page-save','stash','supplement','save','save-anniversary','save-draft','save-sealed','generate','save-characters','profile-save','adopt'}
PAGES={'m03-p05','m03-p08','m03-p11','m03-p12','m04-p04','m04-p09','m04-p13','m05-p03','m05-p04','m05-p05','m05-p10','m06-p02','m07-p02','m08-p04','m08-p09','m08-p10','m08-p11','m08-p12','m08-p19'}
def main():
    files=source();cases=[];locators={};namespaces={}
    for group,module in MODULES.items():
        if group=='onboarding':continue
        namespaces[group]=declarations(module);path=ROOT/f'evidence/current/{group}-controls-results.json';raw=path.read_bytes();report=json.loads(raw);locators[group]=hashlib.sha256(raw).hexdigest()
        assert all(report['files'].get(k)==v for k,v in files.items()if k.startswith('custom/'))
        inventory={(r.get('page',r.get('id')),c['selector']):c for r in report['inventory']for c in r['controls']}
        for row in report['results']:
            page=row.get('page');kind=row.get('contract')
            if page not in PAGES or kind not in POSITIVE|{'input','mood'}:continue
            if (page,row['selector'])not in inventory:continue
            control=inventory[page,row['selector']]
            if kind=='input'and control.get('type')in ['file','color','radio','checkbox']:continue
            assert namespaces[group]['contract'](page,control)==kind
            cases.append((group,page,control,kind))
    rows=[]
    with sync_playwright()as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for group,page,control,kind in cases:
            context=browser.new_context(viewport=dict(width=390,height=844),reduced_motion='reduce');context.add_init_script(INIT);p=context.new_page();p.set_default_timeout(7000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row=dict(group=group,page=page,selector=control['selector'],contract=kind)
            try:namespaces[group]['control'](p,page,control,kind);assert not errors,errors;row['passed']=True
            except Exception:row.update(passed=False,failure=traceback.format_exc()[-2200:])
            row.update(errors=errors,effective=p.url);rows.append(row);context.close();assert source()==files
            print(('PASS 'if row['passed']else'FAIL ')+str(len(rows))+'/'+str(len(cases))+' '+page+' '+kind,flush=True)
        browser.close()
    (ROOT/'evidence/current/native-field-flows-results.json').write_text(json.dumps(dict(files=files,locator_candidates_only=True,locator_candidates_sha256=locators,results=rows,accepted_pages=0,scope='Fresh actual input limits and save/reply/stash flows in 19 affected field pages, using unchanged old control locators and current explicit fixture contracts; no promotion of historical whole initial suites.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(cases=len(rows),passed=sum(r['passed']for r in rows))));raise SystemExit(0 if rows and all(r['passed']for r in rows)else 1)

if __name__=='__main__':main()
