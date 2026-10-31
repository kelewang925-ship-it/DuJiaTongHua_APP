"""Correct native-modal availability using an actual fresh DOM observation."""
import copy,json,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from replay_current_initial_controls import ROOT,DEMO,OUT,deps,sha,dump
from audit_hidden_overlays import declarations
from audit_runtime import INIT,OBSERVE
from verify_book_v2_initial_controls import contract,custom_control

def main():
    raw_path=OUT/'results.json';raw=json.loads(raw_path.read_text(encoding='utf-8'))
    assert raw['complete'] and len(raw['inventory'])==114 and not raw['inventory_errors'];assert raw['dependencies']==deps()
    assert all(sha(ROOT/n)==h for n,h in raw['fixture_sha256'].items())
    assert all(r['passed'] and not r['errors'] for r in raw['results'] if r['page']!='m08-p20')
    target=ROOT/'evidence/current/initial-controls-20261031-accessible';target.mkdir(parents=True,exist_ok=True);assert not(target/'results.json').exists()
    fixture=declarations('verify_book_controls.py');errors=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe');version=browser.version
        c=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');c.add_init_script(INIT);p=c.new_page();p.set_default_timeout(6500);p.on('pageerror',lambda e:errors.append(str(e)))
        fixture['seed'](p,'m08-p20');expect(p.locator('dialog[open]')).to_have_count(1);observed=p.evaluate(OBSERVE);assert not errors
        for control in observed['controls']:
            control['blocked_by_modal']=p.evaluate('s=>{const e=document.querySelector(s),d=document.querySelector("dialog[open]");return !!e&&(!!e.closest("[inert]")||!!d&&!d.contains(e))}',control['selector'])
        controls=[v for v in observed['controls'] if v['visible'] and not v['disabled'] and not v['blocked_by_modal']]
        blocked=[v for v in observed['controls'] if v['visible'] and not v['disabled'] and v['blocked_by_modal']]
        original=next(v for v in raw['inventory'] if v['page']=='m08-p20')
        original_keys={(v['selector'],v['label']) for v in original['controls']}
        assert original_keys<={(v['selector'],v['label']) for v in controls+blocked}
        assert original_keys<={(v['selector'],v['label']) for v in blocked}
        assert controls and blocked
        p.screenshot(path=str(target/'m08-p20-native-modal.png'),full_page=True);entry={'group':'book','page':'m08-p20','effective':p.url,'observed':observed,'controls':controls};c.close();new_rows=[]
        for v in controls:
            c=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce',locale='zh-CN',timezone_id='Asia/Shanghai');p=c.new_page();p.set_default_timeout(6500);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));kind=contract('m08-p20',v,fixture);row={'group':'book','page':'m08-p20','selector':v['selector'],'label':v['label'],'contract':kind,'passed':False,'execution':'new-modal-availability-correction'}
            try:custom_control(p,'m08-p20',v,kind,fixture);assert not errors;row['passed']=True
            except Exception:row['failure']=traceback.format_exc()
            row.update(errors=errors,effective=p.url);new_rows.append(row);c.close()
        browser.close()
    assert deps()==raw['dependencies'] and all(sha(ROOT/n)==h for n,h in raw['fixture_sha256'].items())
    inventory=[entry if v['page']=='m08-p20' else copy.deepcopy(v) for v in raw['inventory']];rows=[];relative=raw_path.relative_to(ROOT).as_posix()
    for index,row in enumerate(raw['results']):
        if row['page']=='m08-p20':continue
        rows.append(dict(row,execution='retained-exact-source-actual-execution',retained_from={'report':relative,'result_index':index}))
    rows+=new_rows
    assert {(v['page'],v['selector']) for v in rows}=={(v['page'],c['selector']) for v in inventory for c in v['controls']}
    report={**raw,'inventory':inventory,'results':rows,'browser':version,'fixture_sha256':{**raw['fixture_sha256'],Path(__file__).name:sha(Path(__file__))},'source_report':relative,'source_report_sha256':sha(raw_path),'observation_correction':{'page':'m08-p20','reason':'Wait for the native initial dialog to open, then exclude its unavailable visible background. The original collector observed the background before the automatic dialog settled. No product source was changed.','newly_available_controls':[{'selector':v['selector'],'label':v['label']} for v in controls if (v['selector'],v['label']) not in original_keys],'blocked_controls':[{'selector':v['selector'],'label':v['label']} for v in blocked],'raw_page_results':[v for v in raw['results'] if v['page']=='m08-p20']},'new_executions':len(new_rows),'retained_executions':len(rows)-len(new_rows),'complete':True,'all_passed':all(v['passed'] and not v['errors'] for v in rows)}
    dump(target/'results.json',report)
    for name in raw['dependencies']:
        dest=target/'source'/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((DEMO/name).read_bytes())
    for name in report['fixture_sha256']:
        dest=target/'fixtures'/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((ROOT/name).read_bytes())
    print('Native-modal availability correction:',len(blocked),'background controls;',len(new_rows),'new actual executions;',report['retained_executions'],'retained actual executions;',sum(r['passed'] for r in rows),'/',len(rows))
    return 0 if report['all_passed'] else 1

if __name__=='__main__':raise SystemExit(main())
