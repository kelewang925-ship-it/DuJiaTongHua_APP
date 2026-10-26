"""Verify full canonical initial-page coverage and scope-bound evidence."""
import argparse
import hashlib
import json
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,BASE,source


def main():
    parser=argparse.ArgumentParser()
    for group in ['a','b','c','repairs']:
        parser.add_argument('--'+group+'-session',type=int,required=True)
        parser.add_argument('--'+group+'-exit',type=int,required=True)
    args=parser.parse_args();files=source();out=ROOT/'evidence/current';quality=out/'initial-quality'
    h=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
    styles={p.relative_to(DEMO).as_posix():h(p)for p in (DEMO/'assets').glob('*.css')}
    widths=[320,375,390,414,430];manifest=json.loads((DEMO/'manifest.json').read_text(encoding='utf-8'));ids={p['id']for p in manifest};rows=[];reports={};executions={}
    for group,stem in [('a','m01-m02-m03-m04'),('b','m05-m06'),('c','m07-m08')]:
        assert getattr(args,group+'_exit')==0
        path=quality/(stem+'-320_375_390_414_430.json');value=json.loads(path.read_text(encoding='utf-8'))
        assert value['files']==files and value['styles']==styles and value['widths']==widths
        assert value['script_sha256']==h(ROOT/'audit_initial_quality.py')
        for name,sha in value['fixture_script_sha256'].items():assert h(ROOT/('verify_'+name+'_controls.py'))==sha
        assert all(row['passed']and not any(row['failures'].values())for row in value['results'])
        rows.extend(value['results']);reports[path.name]=h(path);executions[group]=dict(session_id=getattr(args,group+'_session'),exit_code=0,cases=len(value['results']))
    assert len(rows)==570 and {(r['page'],r['width'])for r in rows}=={(page,width)for page in ids for width in widths}
    keyboards=[r for r in rows if r['width']==390];assert len(keyboards)==114
    assert all(r['keyboard']is not None and not r['keyboard']['unreached']and not r['keyboard']['noVisibleFocus']for r in keyboards)
    repairs=quality/'repair-behavior-results.json';v=json.loads(repairs.read_text(encoding='utf-8'));assert args.repairs_exit==0 and v['files']==files and v['styles']==styles and v['script_sha256']==h(ROOT/'verify_initial_quality_repairs.py')and len(v['results'])==5 and all(r['passed']for r in v['results']);reports[repairs.name]=h(repairs);executions['repairs']=dict(session_id=args.repairs_session,exit_code=0,cases=5)
    assets=json.loads((out/'page-contracts.json').read_text(encoding='utf-8'))['assets'];non_styles={}
    for asset in assets:
        if not asset['path'].endswith('.css'):
            assert h(DEMO/asset['path'])==asset['sha256'],asset['path'];non_styles[asset['path']]=asset['sha256']
    assert (DEMO/'custom/m05-p03.html').read_bytes()==(DEMO/'pages/m05-p03.html').read_bytes()
    for name,sha in {**files,**styles}.items():
        with urlopen(BASE+name.replace('custom/','pages/',1),timeout=10)as response:assert hashlib.sha256(response.read()).hexdigest()==sha,name
    checkpoint=dict(files=files,styles=styles,unchanged_non_style_assets=non_styles,executions=executions,reports_sha256=reports,script_sha256={name:h(ROOT/name)for name in ['audit_initial_quality.py','verify_initial_quality_repairs.py','verify_initial_quality_checkpoint.py']},pages=114,layout_cases=570,keyboard_pages=114,keyboard_visits=sum(len(r['keyboard']['visited'])for r in keyboards),repair_behavior_cases=5,accepted_pages=0,
                    scope='Canonical initial states only,320/375/390/414/430 x844,44/34 simulated insets,reduced motion. AX role names/label association/image-alt presence, actual Tab traversal390, focus feedback, geometry and hit points. Contrast, screen-reader narration, all hidden/long/error states and mobile keyboard visual viewport remain separate.')
    (quality/'checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    old=out/'current-evidence-state.json';state=json.loads(old.read_text(encoding='utf-8'))
    if state['files']!=files:
        historical=ROOT/'evidence/history/initial-quality-before-style-fixes';historical.mkdir(parents=True,exist_ok=True)
        if not(historical/old.name).exists():(historical/old.name).write_bytes(old.read_bytes())
        for name,count in list(state.items()):
            if name.startswith('current_')and isinstance(count,int)and not isinstance(count,bool)and count>0:
                state['historical_'+name.removeprefix('current_')]=count;state[name]=0
        state['previous_behavior_source_manifest']='evidence/history/initial-quality-before-style-fixes/current-evidence-state.json'
    state.update(files=files,style_dependencies=styles,current_failure_literal_candidates=61,current_initial_quality_pages=114,current_initial_quality_layout_cases=570,current_initial_quality_keyboard_pages=114,current_initial_quality_repair_cases=5,accepted_pages=0,runtime_requires_refresh=True,catalog_requires_refresh=True,flow_replay_requires_refresh=True,overlay_exit_replay_complete=False,failure_candidates_are_unproven=True,
                 reason='Search-chip geometry and shared keyboard-focus styles changed. Prior full-fingerprint behavior reports retain their actual historical manifests. New575 geometry/repair checks and114 keyboard traversals are current; consolidate remaining visual/hidden-state repairs before final flow refresh.')
    old.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(pages=114,layout_cases=570,keyboard_pages=114,keyboard_visits=checkpoint['keyboard_visits'],repair_cases=5,accepted_pages=0)))


if __name__=='__main__':main()
