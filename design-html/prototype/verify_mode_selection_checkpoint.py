"""Compose unchanged-page evidence with a directly replayed changed page."""
import argparse
import hashlib
import json
import subprocess
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,BASE,source


def main():
    parser=argparse.ArgumentParser()
    for name in ['behavior','layout','repairs']:
        parser.add_argument('--'+name+'-session',type=int,required=True)
        parser.add_argument('--'+name+'-exit',type=int,required=True)
    args=parser.parse_args();assert args.behavior_exit==args.layout_exit==args.repairs_exit==0
    h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();out=ROOT/'evidence/current';quality=out/'initial-quality';history=ROOT/'evidence/history/pre-native-mode-selection-1db300c'
    files=source();styles={p.relative_to(DEMO).as_posix():h(p)for p in (DEMO/'assets').glob('*.css')}
    basis_path=history/'initial-quality-checkpoint.json';basis=json.loads(basis_path.read_text(encoding='utf-8'))
    assert {name for name in files if files[name]!=basis['files'][name]}=={'custom/m05-p03.html'}
    assert styles==basis['styles'],'A shared style change requires replaying its consumers'
    fixture_dependencies={}
    for name in ['audit_current_runtime.py','book_test_helpers.py']:
        blob=subprocess.run(['git','show','1db300c:design-html/prototype/'+name],cwd=DEMO.parent,capture_output=True,check=True).stdout
        actual=(ROOT/name).read_bytes().replace(b'\r\n',b'\n');assert actual==blob.replace(b'\r\n',b'\n')
        fixture_dependencies[name]=hashlib.sha256(actual).hexdigest()
    for name,sha in basis['unchanged_non_style_assets'].items():assert h(DEMO/name)==sha
    widths=[320,375,390,414,430];rows=[];provenance=[];reports={}
    # Initial render/Tab evidence depends on its own HTML and all shared assets,
    # not on another page's HTML. All shared source/assets are byte-identical.
    for name,sha in basis['reports_sha256'].items():
        if name=='repair-behavior-results.json':
            assert h(history/'initial-quality-repair-behavior-results.json')==sha
            continue
        path=quality/name;assert h(path)==sha;v=json.loads(path.read_text(encoding='utf-8'))
        assert v['styles']==styles and v['script_sha256']==h(ROOT/'audit_initial_quality.py')
        for fixture,digest in v['fixture_script_sha256'].items():assert h(ROOT/('verify_'+fixture+'_controls.py'))==digest
        for index,row in enumerate(v['results']):
            if row['page']=='m05-p03':continue
            assert v['files']['custom/'+row['page']+'.html']==files['custom/'+row['page']+'.html']
            assert row['passed']and not any(row['failures'].values());rows.append(row)
            provenance.append(dict(page=row['page'],width=row['width'],report=path.relative_to(ROOT).as_posix(),index=index,basis='unchanged own HTML and shared dependencies'))
        reports[path.relative_to(ROOT).as_posix()]=sha
    assert len(rows)==565
    replay=quality/'pages-m05-p03-320_375_390_414_430.json';v=json.loads(replay.read_text(encoding='utf-8'))
    assert v['files']==files and v['styles']==styles and v['script_sha256']==h(ROOT/'audit_initial_quality.py')
    assert len(v['results'])==5
    for index,row in enumerate(v['results']):
        assert row['page']=='m05-p03'and row['passed']and not any(row['failures'].values());rows.append(row)
        provenance.append(dict(page=row['page'],width=row['width'],report=replay.relative_to(ROOT).as_posix(),index=index,basis='direct replay after native repaint'))
    reports[replay.relative_to(ROOT).as_posix()]=h(replay)
    ids={p['id']for p in json.loads((DEMO/'manifest.json').read_text(encoding='utf-8'))}
    assert len(rows)==570 and {(r['page'],r['width'])for r in rows}=={(page,width)for page in ids for width in widths}
    keyboards=[r for r in rows if r['width']==390];assert len(keyboards)==114 and all(not r['keyboard']['unreached']and not r['keyboard']['noVisibleFocus']for r in keyboards)
    for name,script in [('mode-selection/results.json','verify_mode_selection.py'),('initial-quality/repair-behavior-results.json','verify_initial_quality_repairs.py')]:
        path=out/name;v=json.loads(path.read_text(encoding='utf-8'))
        assert v['files']==files and v['styles']==styles and v['script_sha256']==h(ROOT/script)and len(v['results'])==5 and all(r['passed']for r in v['results']);reports[path.relative_to(ROOT).as_posix()]=h(path)
    baseline=ROOT/'evidence/baseline/mode-selection/results.json';b=json.loads(baseline.read_text(encoding='utf-8'));assert len(b['results'])==5 and not any(r['passed']for r in b['results'])and b['script_sha256']==h(history/'baseline-verify_mode_selection.py')
    style_baseline=ROOT/'evidence/baseline/mode-selection/style-baseline-results.json';b=json.loads(style_baseline.read_text(encoding='utf-8'));assert len(b['results'])==5 and not any(r['passed']for r in b['results'])and b['script_sha256']==h(ROOT/'evidence/history/pre-native-style-selection/style-baseline-verifier.py')
    for page in ids:assert (DEMO/'custom'/f'{page}.html').read_bytes()==(DEMO/'pages'/f'{page}.html').read_bytes()
    for name,sha in {**files,**styles}.items():
        with urlopen(BASE+name.replace('custom/','pages/',1),timeout=10)as response:assert hashlib.sha256(response.read()).hexdigest()==sha
    checkpoint=dict(files=files,styles=styles,fixture_dependencies_unchanged_from_1db300c=fixture_dependencies,basis_checkpoint=str(basis_path.relative_to(ROOT)).replace('\\','/'),basis_sha256=h(basis_path),retained_layout_cases=565,replayed_layout_cases=5,layout_cases=570,keyboard_pages=114,keyboard_visits=sum(len(r['keyboard']['visited'])for r in keyboards),mode_behavior_cases=5,repair_behavior_cases=5,baseline_sha256={str(p.relative_to(ROOT)).replace('\\','/'):h(p)for p in [baseline,style_baseline]},reports_sha256=reports,row_provenance=provenance,executions={name:dict(session_id=getattr(args,name+'_session'),exit_code=0)for name in ['behavior','layout','repairs']},accepted_pages=0,scope='Only m05-p03 HTML changed.565 initial rows retain exact own-page/shared-asset inputs;5 changed-page rows replayed. State/save/failure/retry/generation behavior newly executed at5 widths. Other hidden/long/keyboard/exception acceptance remains separate.')
    checkpoint['script_sha256']={name:h(ROOT/name)for name in ['verify_mode_selection.py','verify_mode_selection_checkpoint.py','audit_initial_quality.py','verify_initial_quality_repairs.py']}
    checkpoint['screenshots_sha256']={f'{kind}-selected-{width}.png':h(out/'mode-selection'/f'{kind}-selected-{width}.png')for kind in ['movie','warm']for width in widths}
    checkpoint['visual_review_examples']=['movie-selected-320.png','warm-selected-390.png']
    encoded=json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n'
    (out/'mode-selection/checkpoint.json').write_text(encoded,encoding='utf-8')
    (quality/'checkpoint.json').write_text(encoded,encoding='utf-8')
    state_path=out/'current-evidence-state.json';state=json.loads(state_path.read_text(encoding='utf-8'));state.update(files=files,style_dependencies=styles,current_initial_quality_layout_cases=570,current_initial_quality_keyboard_pages=114,current_initial_quality_repair_cases=5,current_native_mode_selection_cases=5,initial_quality_current_checkpoint='evidence/current/mode-selection/checkpoint.json',mode_raster_issue='fixed',style_raster_issue='fixed',runtime_requires_refresh=True,catalog_requires_refresh=True,flow_replay_requires_refresh=True,accepted_pages=0,reason='Native mode/style choices repaired and directly exercised;114 initial-page geometry coverage composed by exact dependency identity plus changed-page replay. Broader final runtime/flow refresh follows remaining UI audits.');state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(retained=565,replayed=5,layout_cases=570,keyboard_pages=114,native_behavior=5,repair_behavior=5,accepted_pages=0)))


if __name__=='__main__':main()
