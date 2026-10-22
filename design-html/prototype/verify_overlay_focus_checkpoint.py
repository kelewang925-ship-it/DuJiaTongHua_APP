"""Bind full initial replay, runtime/catalog refresh and form-entry evidence."""
import argparse
import hashlib
import json
import subprocess
from urllib.request import urlopen
from verify_pet_controls import ROOT, DEMO, BASE, source


def main():
    parser=argparse.ArgumentParser()
    for name in ['serial','repairs','focus','baseline','runtime','catalog','danger']:
        parser.add_argument('--'+name+'-session',type=str,required=True)
        parser.add_argument('--'+name+'-exit',type=int,required=True)
    args=parser.parse_args()
    assert args.baseline_exit==1
    assert all(getattr(args,name+'_exit')==0 for name in ['serial','repairs','focus','runtime','catalog','danger'])
    h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    read=lambda p:json.loads(p.read_text(encoding='utf-8'))
    out=ROOT/'evidence/current';quality=out/'initial-quality';focus=out/'overlay-entry-focus'
    files=source();styles={p.relative_to(DEMO).as_posix():h(p) for p in (DEMO/'assets').glob('*.css')}
    execution=read(quality/'serial-executions.json')
    assert execution['files']==files and execution['script_sha256']==h(ROOT/'run_initial_quality_serial.py') and execution['audit_script_sha256']==h(ROOT/'audit_initial_quality.py')
    assert execution['executions']==[dict(module=f'm{n:02}',exit_code=0) for n in range(1,9)]
    reports={};rows=[];fixture_hashes={}
    for n in range(1,9):
        path=quality/f'm{n:02}-320_375_390_414_430.json';v=read(path)
        assert v['files']==files and v['styles']==styles and v['script_sha256']==h(ROOT/'audit_initial_quality.py')
        for name,digest in v['fixture_script_sha256'].items():
            assert h(ROOT/('verify_'+name+'_controls.py'))==digest;fixture_hashes[name]=digest
        assert all(r['passed'] and not any(r['failures'].values()) for r in v['results'])
        rows.extend(v['results']);reports[path.relative_to(ROOT).as_posix()]=h(path)
    ids={v['id'] for v in read(DEMO/'manifest.json')}
    assert len(rows)==570 and {(r['page'],r['width']) for r in rows}=={(p,w) for p in ids for w in [320,375,390,414,430]}
    keyboards=[r for r in rows if r['width']==390]
    assert len(keyboards)==114 and all(not r['keyboard']['unreached'] and not r['keyboard']['noVisibleFocus'] for r in keyboards)
    repair_path=quality/'repair-behavior-results.json';v=read(repair_path)
    assert v['files']==files and v['styles']==styles and v['script_sha256']==h(ROOT/'verify_initial_quality_repairs.py')
    assert len(v['results'])==5 and all(r['passed'] for r in v['results']);reports[repair_path.relative_to(ROOT).as_posix()]=h(repair_path)
    focus_path=focus/'results.json';current=read(focus_path)
    assert current['files']==files and current['styles']==styles and current['script_sha256']==h(ROOT/'verify_overlay_entry_focus.py')
    assert current['locator_candidates_sha256']==h(out/'hidden-overlay-observations.json')
    assert len(current['results'])==84 and all(r['passed'] for r in current['results'])
    assert len({(r.get('index'),r.get('width'),r.get('case')) for r in current['results']})==84
    baseline_path=ROOT/'evidence/baseline/overlay-entry-focus/results.json';baseline=read(baseline_path)
    assert baseline['script_sha256']==h(ROOT/'verify_overlay_entry_focus.py') and len(baseline['results'])==5
    assert all(not r['passed'] and r['index']==72 and r['entry']['focused'] and r['entry']['headingTop']>=r['entry']['dialogTop'] and 'Locator expected to be focused' in r['failure'] for r in baseline['results'])
    assert {name for name in files if baseline['files'][name]!=files[name]}=={'assets/prototype-ui.js'} and baseline['styles']==styles
    title_baseline=ROOT/'evidence/baseline/overlay-entry-focus/entry-title-before-focus.json';title=read(title_baseline)
    assert title['script_sha256']==h(ROOT/'evidence/baseline/overlay-entry-focus/entry-title-before-focus-verifier.py')
    assert len(title['results'])==5 and all(not r['passed'] and r['entry']['headingBottom']<r['entry']['dialogTop'] for r in title['results'])
    assert title['files']==read(ROOT/'evidence/history/pre-overlay-focus-99f0af5/current-evidence-state.json')['files']
    canonical_ui=subprocess.run(['git','show','99f0af5:design-html/assets/prototype-ui.js'],cwd=DEMO.parent,capture_output=True,check=True).stdout
    assert (ROOT/'evidence/history/pre-overlay-focus-99f0af5/prototype-ui-before-title-focus.git.js').read_bytes()==canonical_ui
    assert h(ROOT/'evidence/history/heading-focus-before-reverse-tab/prototype-ui.js')==baseline['files']['assets/prototype-ui.js']
    helper_names=['audit_hidden_overlays.py','verify_overlay_form_saves.py','audit_current_runtime.py','book_test_helpers.py']+['verify_'+name+'_controls.py' for name in ['onboarding','record','moment','time','workshop','settings','pet','book']]
    helper_hashes={}
    for name in helper_names:
        blob=subprocess.run(['git','show','99f0af5:design-html/prototype/'+name],cwd=DEMO.parent,capture_output=True,check=True).stdout
        actual=(ROOT/name).read_bytes().replace(b'\r\n',b'\n');assert actual==blob.replace(b'\r\n',b'\n');helper_hashes[name]=hashlib.sha256(actual).hexdigest()
    for name,count in [('danger-confirmation-results.json',18),('danger-primary-contract-results.json',5)]:
        v=read(out/name);assert v['files']==files and len(v['results'])==count and all(r['passed'] and not r['errors'] for r in v['results']);reports['evidence/current/'+name]=h(out/name)
    runtime=read(out/'current-runtime-summary.json');catalog=read(out/'page-contracts.json')
    assert runtime['files']==files and runtime['requested_pages']==114 and runtime['observations']==228 and runtime['controls_observed']==1696 and not runtime['errors'] and not runtime['unbound_or_delegated_candidates']
    assert catalog['files']==files and len(catalog['pages'])==114 and len(catalog['assets'])==267
    for asset in catalog['assets']:assert h(DEMO/asset['path'])==asset['sha256']
    for page in ids:assert (DEMO/'custom'/(page+'.html')).read_bytes()==(DEMO/'pages'/(page+'.html')).read_bytes()
    for name,digest in {**files,**styles}.items():
        with urlopen(BASE+name.replace('custom/','pages/',1),timeout=10) as response:assert response.headers.get("Cache-Control")=="no-store" and hashlib.sha256(response.read()).hexdigest()==digest
    for path in [focus_path,out/'current-runtime-summary.json',out/'current-runtime-inventory.json',out/'page-contracts.json',out/'page-contract-audit-checkpoint.json',quality/'serial-executions.json']:
        reports[path.relative_to(ROOT).as_posix()]=h(path)
    checkpoint=dict(files=files,styles=styles,reports_sha256=reports,layout_cases=570,replayed_layout_cases=570,retained_layout_cases=0,keyboard_pages=114,keyboard_visits=sum(len(r['keyboard']['visited']) for r in keyboards),repair_cases=5,focus_cases=84,focus_retained_cases=0,focus_replayed_cases=84,baseline_sha256=h(baseline_path),title_baseline_sha256=h(title_baseline),fixture_script_sha256=fixture_hashes,helpers_unchanged_from_99f0af5=helper_hashes,scripts_sha256={name:h(ROOT/name) for name in ['verify_overlay_entry_focus.py','verify_overlay_focus_checkpoint.py','run_initial_quality_serial.py','audit_initial_quality.py','verify_initial_quality_repairs.py','audit_current_runtime.py','build_current_catalog.py','build_page_contracts.py','verify_page_contracts.py','serve_preview.py','verify_danger_confirmations.py','verify_danger_primary_contract.py']},executions={name:dict(reference=('session:' if getattr(args,name+'_session').isdecimal() else 'chunk:')+getattr(args,name+'_session'),exit_code=getattr(args,name+'_exit')) for name in ['serial','repairs','focus','baseline','runtime','catalog','danger']},screenshots_sha256={p.name:h(p) for p in focus.glob('*.png')},danger_cases=23,runtime_observations=228,controls_observed=1696,catalog_pages=114,assets=267,accepted_pages=0,scope='570 newly executed canonical initial observations and114 keyboard traversals.84 newly executed form/default-focus outcomes, including reverse Tab from the heading and first field. Five-width420px viewport pressure and native scroll are simulations, not real mobile IME or full screen-reader/final-flow acceptance.')
    encoded=json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n';(focus/'checkpoint.json').write_text(encoded,encoding='utf-8');(quality/'checkpoint.json').write_text(encoded,encoding='utf-8')
    state_path=out/'current-evidence-state.json';state=read(state_path)
    for name,count in list(state.items()):
        if name.startswith('current_') and isinstance(count,int) and not isinstance(count,bool) and count>0:state['historical_'+name.removeprefix('current_')]=count;state[name]=0
    state.update(files=files,style_dependencies=styles,current_initial_quality_pages=114,current_initial_quality_layout_cases=570,current_initial_quality_keyboard_pages=114,current_initial_quality_repair_cases=5,current_overlay_entry_focus_cases=84,current_danger_confirmation_cases=18,current_primary_contract_cases=5,initial_quality_current_checkpoint='evidence/current/overlay-entry-focus/checkpoint.json',previous_behavior_source_manifest='evidence/history/pre-overlay-focus-99f0af5/current-evidence-state.json',runtime_requires_refresh=False,catalog_requires_refresh=False,flow_replay_requires_refresh=True,overlay_entry_focus_issue='fixed',accepted_pages=0,reason=checkpoint['scope'])
    state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(layout=570,keyboard_pages=114,focus_cases=84,repairs=5,runtime=228,catalog_pages=114,accepted_pages=0)))


if __name__=='__main__':main()
