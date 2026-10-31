"""Run the four existing real-control journeys without overwriting prior evidence."""
import argparse,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
import verify_new_user_journey as NJ
from audit_hidden_overlays import declarations
from replay_current_initial_controls import ROOT,DEMO,deps,fixture_files,sha,dump

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['baseline','current'],required=True);args=parser.parse_args()
    out=ROOT/f'evidence/{args.stage}/continuous-journeys-20261031';out.mkdir(parents=True,exist_ok=True);assert not(out/'results.json').exists()
    files=deps();scripts=fixture_files();scripts.update({n:sha(ROOT/n) for n in ['verify_new_user_journey.py','verify_product_journey.py','verify_time_product_journey.py',Path(__file__).name]})
    product=declarations('verify_product_journey.py');time=declarations('verify_time_product_journey.py')
    cases=[('new-user-registration-binding-diary-crud',NJ.serial,None),('created-list-home-return',NJ.list_home,None),('eight-module-product',product['journey'],product),('anniversary-capsule-reminders',time['journey'],time)]
    baseline_path=ROOT/'evidence/baseline/continuous-journeys-20261031/results.json'
    baseline=json.loads(baseline_path.read_text(encoding='utf-8')) if args.stage=='current' else None
    if baseline:
        assert baseline['complete'] and baseline['dependencies']==files
        for n,h in baseline['fixture_sha256'].items():
            assert sha(baseline_path.parent/'fixtures'/n)==h
            if n not in ['verify_product_journey.py',Path(__file__).name]:assert scripts[n]==h
    rows=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=browser.version
        for name,run,namespace in cases:
            if baseline and name!='eight-module-product':
                row=next(v for v in baseline['results'] if v['case']==name)
                assert row['passed']
                row={**row,'execution':'retained-baseline-pass','provenance':{'report':str(baseline_path.relative_to(ROOT)).replace(chr(92),'/'),'sha256':sha(baseline_path),'case':name}}
                rows.append(row);print('RETAIN',name,len(row['steps']),'stage records',flush=True);continue
            shots=out/name;shots.mkdir();NJ.OUT=shots
            if namespace:namespace['SHOTS']=shots;namespace['NJ'].OUT=shots
            context=browser.new_context(viewport={'width':390,'height':844},reduced_motion='no-preference',timezone_id='Asia/Shanghai',locale='zh-CN',accept_downloads=True)
            p=context.new_page();p.set_default_timeout(6500);p.set_default_navigation_timeout(15000);errors=[];steps=[];navigations=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('framenavigated',lambda f:navigations.append(f.url) if f==p.main_frame else None);row={'case':name,'passed':False,'execution':'fresh'}
            try:run(p,steps);assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc();p.screenshot(path=str(shots/'failure.png'),full_page=True)
            row.update(errors=errors,steps=steps,navigations=navigations,effective=p.url);rows.append(row);context.close();assert deps()==files and all(sha(ROOT/n)==h for n,h in scripts.items())
            dump(out/'results.json',{'dependencies':files,'fixture_sha256':scripts,'browser':version,'viewport':[390,844],'locale':'zh-CN','timezone':'Asia/Shanghai','motion':'no-preference','scope':'Four continuous product-control journeys: baseline has four fresh contexts; current retains three unchanged passing cases with exact baseline provenance and freshly executes the affected eight-module case. Starts at an entry page, then uses product controls; local one-shot failures and explicit peer simulations remain declared in original fixtures. Not every condition or114-page final acceptance.','results':rows,'complete':len(rows)==4,'all_passed':len(rows)==4 and all(v['passed'] for v in rows),'human_accepted_pages':0})
            print(('PASS' if row['passed'] else 'FAIL'),name,len(steps),'stage records',flush=True)
        browser.close()
    for n in files:
        dest=out/'source'/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((DEMO/n).read_bytes())
    for n in scripts:
        dest=out/'fixtures'/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((ROOT/n).read_bytes())
    print('FINISH',sum(r['passed'] for r in rows),'/',len(rows),'journeys;',sum(len(r['steps']) for r in rows),'stage records')
    return 0 if all(v['passed'] for v in rows) else 1

if __name__=='__main__':raise SystemExit(main())
