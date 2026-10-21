"""Bind pet/book repairs to browser evidence and unchanged initial observations."""
import argparse
import hashlib
import json
from urllib.request import urlopen
from verify_pet_controls import ROOT, DEMO, BASE, source


def main():
    parser = argparse.ArgumentParser()
    for name in ['behavior', 'layout', 'baseline']:
        parser.add_argument('--' + name + '-session', type=int, required=True)
        parser.add_argument('--' + name + '-exit', type=int, required=True)
    args = parser.parse_args()
    assert args.behavior_exit == args.layout_exit == 0 and args.baseline_exit == 1
    h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    cache = {}
    def read(p):
        if p not in cache: cache[p] = json.loads(p.read_text(encoding='utf-8'))
        return cache[p]
    out = ROOT/'evidence/current'
    basis_path = ROOT/'evidence/history/pre-pet-book-selection-bd5dde2/initial-quality-checkpoint.json'
    basis = read(basis_path)
    files = source()
    styles = {p.relative_to(DEMO).as_posix(): h(p) for p in (DEMO/'assets').glob('*.css')}
    changed = {'m07-p02','m07-p06','m07-p08','m08-p04','m08-p08'}
    assert {name for name in files if files[name] != basis['files'][name]} == {'custom/'+p+'.html' for p in changed}
    assert styles == basis['styles']
    ancestor = basis
    lineage = {basis_path.relative_to(ROOT).as_posix():h(basis_path)}
    while 'unchanged_non_style_assets' not in ancestor:
        for name, digest in ancestor.get('fixture_dependencies_unchanged_from_1db300c',{}).items():
            assert hashlib.sha256((ROOT/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest() == digest
        path = ROOT/ancestor['basis_checkpoint']
        assert h(path) == ancestor['basis_sha256']
        lineage[path.relative_to(ROOT).as_posix()] = h(path)
        ancestor = read(path)
    for name, digest in ancestor['unchanged_non_style_assets'].items(): assert h(DEMO/name) == digest
    rows, provenance, reports = [], [], {}
    for item in basis['row_provenance']:
        if item['page'] in changed: continue
        path = ROOT/item['report']; v = read(path)
        assert h(path) == basis['reports_sha256'][item['report']]
        assert v['styles'] == styles and v['script_sha256'] == h(ROOT/'audit_initial_quality.py')
        for fixture,digest in v['fixture_script_sha256'].items(): assert h(ROOT/('verify_'+fixture+'_controls.py')) == digest
        row = v['results'][item['index']]
        assert row['page'] == item['page'] and row['width'] == item['width'] and row['passed'] and not any(row['failures'].values())
        assert v['files']['custom/'+row['page']+'.html'] == files['custom/'+row['page']+'.html']
        rows.append(row); provenance.append(item); reports[item['report']] = h(path)
    assert len(rows) == 545
    layout_path = out/'initial-quality/pages-m07-p02-m07-p06-m07-p08-m08-p04-m08-p08-320_375_390_414_430.json'
    v = read(layout_path)
    assert v['files'] == files and v['styles'] == styles and v['script_sha256'] == h(ROOT/'audit_initial_quality.py')
    assert len(v['results']) == 25
    for index,row in enumerate(v['results']):
        assert row['page'] in changed and row['passed'] and not any(row['failures'].values())
        rows.append(row); provenance.append(dict(page=row['page'],width=row['width'],report=layout_path.relative_to(ROOT).as_posix(),index=index,basis='direct replay after native pet/book choices and cost wrapping'))
    reports[layout_path.relative_to(ROOT).as_posix()] = h(layout_path)
    ids = {v['id'] for v in read(DEMO/'manifest.json')}
    assert {(r['page'],r['width']) for r in rows} == {(p,w) for p in ids for w in [320,375,390,414,430]}
    keyboards = [r for r in rows if r['width'] == 390]
    assert len(keyboards) == 114 and all(not r['keyboard']['unreached'] and not r['keyboard']['noVisibleFocus'] for r in keyboards)
    behavior_path = out/'pet-book-selection-paint/results.json'; v = read(behavior_path)
    script = ROOT/'verify_pet_book_selection_paint.py'
    assert v['files'] == files and v['styles'] == styles and v['script_sha256'] == h(script)
    assert len(v['results']) == 25 and all(r['passed'] for r in v['results'])
    reports[behavior_path.relative_to(ROOT).as_posix()] = h(behavior_path)
    baseline_path = ROOT/'evidence/baseline/pet-book-selection-paint/results.json'; baseline = read(baseline_path)
    assert baseline['files'] == basis['files'] and baseline['styles'] == styles and baseline['script_sha256'] == h(script)
    assert len(baseline['results']) == 25 and all(not r['passed'] for r in baseline['results'])
    assert all(('Action cost text crosses' if r['page']=='m07-p06' else 'Native card must cover') in r['failure'] for r in baseline['results'])
    for p in ids: assert (DEMO/'custom'/(p+'.html')).read_bytes() == (DEMO/'pages'/(p+'.html')).read_bytes()
    for name,digest in {**files,**styles}.items():
        with urlopen(BASE+name.replace('custom/','pages/',1),timeout=10) as response: assert hashlib.sha256(response.read()).hexdigest() == digest
    checkpoint = dict(files=files,styles=styles,basis_checkpoint=basis_path.relative_to(ROOT).as_posix(),basis_sha256=h(basis_path),dependency_lineage_sha256=lineage,reports_sha256=reports,row_provenance=provenance,retained_layout_cases=545,replayed_layout_cases=25,layout_cases=570,keyboard_pages=114,keyboard_visits=sum(len(r['keyboard']['visited']) for r in keyboards),behavior_cases=25,baseline_sha256=h(baseline_path),scripts_sha256={n:h(ROOT/n) for n in ['verify_pet_book_selection_paint.py','verify_pet_book_selection_checkpoint.py','audit_initial_quality.py']},executions={name:dict(session_id=getattr(args,name+'_session'),exit_code=getattr(args,name+'_exit')) for name in ['behavior','layout','baseline']},screenshots_sha256={p.name:h(p) for p in (out/'pet-book-selection-paint').glob('*.png')},accepted_pages=0,scope='Five changed pages:25 direct initial/layout observations and25 behavior cases.545 prior initial observations retained by exact own-page/shared asset/fixture identity. Not full hidden-state, soft-keyboard, screen-reader or final-flow acceptance.')
    encoded = json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n'
    (out/'pet-book-selection-paint/checkpoint.json').write_text(encoded,encoding='utf-8')
    (out/'initial-quality/checkpoint.json').write_text(encoded,encoding='utf-8')
    state_path = out/'current-evidence-state.json'; state = read(state_path)
    state.update(files=files,style_dependencies=styles,current_initial_quality_layout_cases=570,current_initial_quality_keyboard_pages=114,current_pet_book_selection_cases=25,initial_quality_current_checkpoint='evidence/current/pet-book-selection-paint/checkpoint.json',pet_adoption_raster_issue='fixed',pet_food_raster_issue='fixed',book_start_raster_issue='fixed',book_template_raster_issue='fixed',pet_action_cost_overflow_issue='fixed',runtime_requires_refresh=True,catalog_requires_refresh=True,flow_replay_requires_refresh=True,accepted_pages=0,reason=checkpoint['scope'])
    state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(retained=545,replayed=25,layout=570,behavior=25,keyboard_pages=114,accepted_pages=0)))


if __name__ == '__main__': main()
