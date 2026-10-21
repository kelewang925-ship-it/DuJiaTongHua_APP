"""Retain unchanged initial observations and replace the two repainted pages."""
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
    read = lambda p: json.loads(p.read_text(encoding='utf-8'))
    out = ROOT / 'evidence/current'
    history = ROOT / 'evidence/history/pre-workshop-selection-paint-f08fa83'
    basis_path = history / 'initial-quality-checkpoint.json'
    basis = read(basis_path)
    files = source()
    styles = {p.relative_to(DEMO).as_posix(): h(p) for p in (DEMO / 'assets').glob('*.css')}
    changed = {'m05-p04', 'm05-p05'}
    assert {name for name in files if files[name] != basis['files'][name]} == {'custom/' + page + '.html' for page in changed}
    assert basis['styles'] == styles
    asset_basis = read(ROOT / basis['basis_checkpoint'])
    assert h(ROOT / basis['basis_checkpoint']) == basis['basis_sha256']
    for name, digest in asset_basis['unchanged_non_style_assets'].items():
        assert h(DEMO / name) == digest
    for name, digest in basis['fixture_dependencies_unchanged_from_1db300c'].items():
        assert hashlib.sha256((ROOT / name).read_bytes().replace(b'\r\n', b'\n')).hexdigest() == digest
    reports = {}
    rows, provenance = [], []
    for item in basis['row_provenance']:
        if item['page'] in changed:
            continue
        path = ROOT / item['report']
        assert h(path) == basis['reports_sha256'][item['report']]
        v = read(path)
        assert v['styles'] == styles and v['script_sha256'] == h(ROOT / 'audit_initial_quality.py')
        for fixture, digest in v['fixture_script_sha256'].items():
            assert h(ROOT / ('verify_' + fixture + '_controls.py')) == digest
        row = v['results'][item['index']]
        assert row['page'] == item['page'] and row['width'] == item['width'] and row['passed'] and not any(row['failures'].values())
        own = 'custom/' + row['page'] + '.html'
        assert v['files'][own] == files[own]
        rows.append(row)
        provenance.append(item)
        reports[item['report']] = h(path)
    assert len(rows) == 560
    layout_path = out / 'initial-quality/pages-m05-p04-m05-p05-320_375_390_414_430.json'
    v = read(layout_path)
    assert v['files'] == files and v['styles'] == styles and v['script_sha256'] == h(ROOT / 'audit_initial_quality.py')
    assert len(v['results']) == 10
    for index, row in enumerate(v['results']):
        assert row['page'] in changed and row['passed'] and not any(row['failures'].values())
        rows.append(row)
        provenance.append(dict(page=row['page'], width=row['width'], report=layout_path.relative_to(ROOT).as_posix(), index=index, basis='direct replay after photo/film selection repaint'))
    reports[layout_path.relative_to(ROOT).as_posix()] = h(layout_path)
    ids = {p['id'] for p in read(DEMO / 'manifest.json')}
    assert {(r['page'], r['width']) for r in rows} == {(page, width) for page in ids for width in [320, 375, 390, 414, 430]}
    keyboards = [r for r in rows if r['width'] == 390]
    assert len(keyboards) == 114 and all(not r['keyboard']['unreached'] and not r['keyboard']['noVisibleFocus'] for r in keyboards)
    behavior_path = out / 'workshop-selection-paint/results.json'
    v = read(behavior_path)
    assert v['files'] == files and v['styles'] == styles and v['script_sha256'] == h(ROOT / 'verify_workshop_selection_paint.py')
    assert len(v['results']) == 10 and all(r['passed'] for r in v['results'])
    reports[behavior_path.relative_to(ROOT).as_posix()] = h(behavior_path)
    baseline_path = ROOT / 'evidence/baseline/workshop-selection-paint/results.json'
    baseline = read(baseline_path)
    assert baseline['files'] == basis['files'] and baseline['script_sha256'] == v['script_sha256']
    assert len(baseline['results']) == 10 and all(not r['passed'] and 'Baked first selection' in r['failure'] for r in baseline['results'])
    for page in ids:
        assert (DEMO / 'custom' / (page + '.html')).read_bytes() == (DEMO / 'pages' / (page + '.html')).read_bytes()
    for name, digest in {**files, **styles}.items():
        with urlopen(BASE + name.replace('custom/', 'pages/', 1), timeout=10) as response:
            assert hashlib.sha256(response.read()).hexdigest() == digest
    checkpoint = dict(files=files, styles=styles, basis_checkpoint=basis_path.relative_to(ROOT).as_posix(), basis_sha256=h(basis_path), reports_sha256=reports, row_provenance=provenance, retained_layout_cases=560, replayed_layout_cases=10, layout_cases=570, keyboard_pages=114, keyboard_visits=sum(len(r['keyboard']['visited']) for r in keyboards), behavior_cases=10, baseline_sha256=h(baseline_path), executions={name:dict(session_id=getattr(args,name+'_session'),exit_code=getattr(args,name+'_exit')) for name in ['behavior','layout','baseline']}, scripts_sha256={name:h(ROOT/name) for name in ['verify_workshop_selection_paint.py','verify_workshop_selection_paint_checkpoint.py','audit_initial_quality.py']}, screenshots_sha256={p.name:h(p) for p in (out/'workshop-selection-paint').glob('*.png')}, accepted_pages=0, scope='Two changed pages directly replayed at five widths;560 initial observations retained only with exact own-page and shared dependency identity. Ten new photo/film behavioral cases. Broader dynamic, keyboard and final flow acceptance remains incomplete.')
    encoded = json.dumps(checkpoint, ensure_ascii=False, indent=2) + '\n'
    (out / 'workshop-selection-paint/checkpoint.json').write_text(encoded, encoding='utf-8')
    (out / 'initial-quality/checkpoint.json').write_text(encoded, encoding='utf-8')
    state_path = out / 'current-evidence-state.json'
    state = read(state_path)
    state.update(files=files, style_dependencies=styles, current_initial_quality_layout_cases=570, current_initial_quality_keyboard_pages=114, current_workshop_selection_paint_cases=10, initial_quality_current_checkpoint='evidence/current/workshop-selection-paint/checkpoint.json', photo_style_raster_issue='fixed', film_mood_raster_issue='fixed', runtime_requires_refresh=True, catalog_requires_refresh=True, flow_replay_requires_refresh=True, accepted_pages=0, reason=checkpoint['scope'])
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(retained=560, replayed=10, behavior=10, layout=570, keyboard_pages=114, accepted_pages=0)))


if __name__ == '__main__':
    main()
