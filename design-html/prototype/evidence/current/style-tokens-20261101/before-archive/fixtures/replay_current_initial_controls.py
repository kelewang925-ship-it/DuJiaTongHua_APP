"""Fresh114 initial-control replay using existing explicit module contracts."""
import argparse,ast,hashlib,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
from audit_hidden_overlays import declarations,seed_onboarding,MODULES
from audit_runtime import INIT,OBSERVE
from verify_pet_controls import ROOT,DEMO,source
from verify_book_v2_reconciliation import dependencies as book_dependencies
from verify_book_v2_initial_controls import contract as book_contract,custom_control

OUT=ROOT/'evidence/current/initial-controls-20261031'
GROUPS=[('onboarding',[f'm01-p{i:02}' for i in range(1,9)]+[f'm02-p{i:02}' for i in range(1,10)]),('record',[f'm03-p{i:02}' for i in range(1,13)]),('moment',[f'm04-p{i:02}' for i in [1,2,3,4,16,17]]),('time',[f'm04-p{i:02}' for i in range(5,16)]),('workshop',[f'm05-p{i:02}' for i in range(1,11)]),('settings',[f'm06-p{i:02}' for i in range(1,13)]),('pet',[f'm07-p{i:02}' for i in range(1,26)]),('book',[f'm08-p{i:02}' for i in range(1,22)])]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def deps():return dict(sorted({**source(),**book_dependencies()}.items()))
def dump(p,value):p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def fixture_files():
    pending=[Path(__file__).resolve()]+[ROOT/n for n in MODULES.values()]+[ROOT/'verify_book_v2_initial_controls.py'];found=set()
    while pending:
        p=pending.pop()
        if p in found:continue
        found.add(p)
        for n in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            names=[n.module] if isinstance(n,ast.ImportFrom) and n.module else [v.name for v in n.names] if isinstance(n,ast.Import) else []
            for name in names:
                other=ROOT/(name.split('.')[0]+'.py')
                if other.is_file() and other not in found:pending.append(other)
    return {p.name:sha(p) for p in sorted(found)}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--resume',action='store_true');args=parser.parse_args();OUT.mkdir(parents=True,exist_ok=True)
    files=deps();scripts=fixture_files();manifest=json.loads((DEMO/'manifest.json').read_text(encoding='utf-8'));ids=[p for _,pages in GROUPS for p in pages]
    assert len(ids)==len(set(ids))==114 and set(ids)=={v['id'] for v in manifest}
    path=OUT/'results.json';prior=json.loads(path.read_text(encoding='utf-8')) if args.resume and path.exists() else None
    if path.exists() and not args.resume:raise RuntimeError('Evidence exists; use --resume to retain only exact-source completed executions')
    if prior:assert prior['dependencies']==files and prior['fixture_sha256']==scripts
    fixtures={name:declarations(script) for name,script in MODULES.items()};inventory=[];results=[];inventory_errors=[]
    prior_inventory={v['page']:v for v in prior['inventory']} if prior else {};prior_results={(v['page'],v['selector']):v for v in prior['results'] if v['passed']} if prior else {}
    report={'dependencies':files,'fixture_sha256':scripts,'scope':'Every visible enabled initial control in114 declared module fixtures, executed against explicit contracts. Does not prove every conditional/hidden state, layout or complete user journey.','viewport':[390,844],'locale':'zh-CN','timezone':'Asia/Shanghai','inventory':inventory,'inventory_errors':inventory_errors,'results':results,'complete':False,'human_accepted_pages':0}
    def save():dump(path,report)
    def prepare(p,group,page):
        if group=='onboarding':seed_onboarding(p,page)
        else:fixtures[group]['seed'](p,page)
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');report['browser']=browser.version
        def context():
            c=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai',accept_downloads=True);c.add_init_script(INIT);c.grant_permissions(['clipboard-read','clipboard-write'],origin='http://127.0.0.1:8765');return c
        for group,pages in GROUPS:
            print('GROUP',group,flush=True)
            for page in pages:
                assert deps()==files and fixture_files()==scripts
                c=context();p=c.new_page();p.set_default_timeout(6500);p.set_default_navigation_timeout(15000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
                try:
                    prepare(p,group,page);observed=p.evaluate(OBSERVE);assert not errors,errors
                    controls=[v for v in observed['controls'] if v['visible'] and not v['disabled'] and not v.get('blocked_by_modal',False)]
                    entry={'group':group,'page':page,'effective':p.url,'observed':observed,'controls':controls};assert controls,(page,'no enabled controls');inventory.append(entry)
                except Exception:
                    inventory_errors.append({'group':group,'page':page,'failure':traceback.format_exc(),'errors':errors,'effective':p.url});p.screenshot(path=str(OUT/f'inventory-{page}.png'),full_page=True);c.close();save();continue
                c.close();print('INVENTORY',page,len(controls),flush=True)
                for v in controls:
                    c=context();p=c.new_page();p.set_default_timeout(6500);p.set_default_navigation_timeout(15000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));row={'group':group,'page':page,'selector':v['selector'],'label':v['label'],'contract':None,'passed':False,'execution':'new'}
                    try:
                        if group=='onboarding':kind=fixtures[group]['RULES'][page].get(v['label']) or ('input:native' if v['native_input'] else None)
                        elif group=='book':kind=book_contract(page,v,fixtures[group])
                        else:kind=fixtures[group]['contract'](page,v)
                        assert kind,(page,v['label'],'no explicit contract');row['contract']=kind
                        saved=prior_results.get((page,v['selector']))
                        if saved and saved['contract']==kind and prior_inventory[page]['controls']==controls:
                            row=dict(saved,execution='retained-exact-source-prior-execution');results.append(row);c.close();save();continue
                        if group=='onboarding':row['details']=fixtures[group]['run'](p,c,{'id':page,'selector':v['selector'],'label':v['label'],'contract':kind})
                        elif group=='book' and (kind in ['close-supplements','reader-prev','reader-next'] or kind.startswith('read-route:')):custom_control(p,page,v,kind,fixtures[group])
                        else:fixtures[group]['control'](p,page,v,kind)
                        assert not errors,errors;row['passed']=True
                    except Exception:
                        row['failure']=traceback.format_exc();p.screenshot(path=str(OUT/f'failure-{len(results):04}-{page}.png'),full_page=True)
                    row.update(errors=errors,effective=p.url);results.append(row);c.close();save();print(('PASS' if row['passed'] else 'FAIL'),page,v['label'].replace('\n',' / '),flush=True)
                assert deps()==files and fixture_files()==scripts
                report['finished_pages']=len(inventory)+len(inventory_errors);save()
        browser.close()
    assert deps()==files and fixture_files()==scripts
    report['complete']=not inventory_errors and len(inventory)==114
    report['all_passed']=report['complete'] and all(r['passed'] and not r['errors'] for r in results)
    report['new_executions']=sum(r['execution']=='new' for r in results);report['retained_executions']=len(results)-report['new_executions'];save()
    for n in files:
        target=OUT/'source'/n;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((DEMO/n).read_bytes())
    for n in scripts:
        target=OUT/'fixtures'/n;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((ROOT/n).read_bytes())
    print('FINISH',len(inventory),'pages;',sum(r['passed'] for r in results),'/',len(results),'controls;',len(inventory_errors),'inventory errors',flush=True)
    return 0 if report['all_passed'] else 1

if __name__=='__main__':raise SystemExit(main())
