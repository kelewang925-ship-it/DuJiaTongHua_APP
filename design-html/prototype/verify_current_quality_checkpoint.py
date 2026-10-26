"""Verify current serial geometry and focus evidence while preserving proven behavior."""
import argparse
import hashlib
import json
from urllib.request import urlopen

from refresh_quality_followups import JOBS
from verify_pet_controls import ROOT, DEMO, BASE, source


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser()
    for name in ['serial', 'followup']:
        parser.add_argument('--' + name + '-session', type=int, required=True)
        parser.add_argument('--' + name + '-exit', type=int, required=True)
    args = parser.parse_args()
    assert args.serial_exit == args.followup_exit == 0
    out = ROOT / 'evidence/current'
    quality = out / 'initial-quality'
    files = source()
    styles = {p.relative_to(DEMO).as_posix(): digest(p)
              for p in sorted((DEMO / 'assets').glob('*.css'))}
    initial = read(out / 'current-initial-replay/checkpoint.json')
    assert initial['files'] == files and initial['styles'] == styles
    for name, sha in initial['reports_sha256'].items():
        artifact = ROOT / name if (ROOT / name).exists() else out / name
        assert digest(artifact) == sha, name
    serial = read(quality / 'serial-executions.json')
    assert serial['files'] == files
    assert serial['script_sha256'] == digest(ROOT / 'run_initial_quality_serial.py')
    assert serial['audit_script_sha256'] == digest(ROOT / 'audit_initial_quality.py')
    assert serial['executions'] == [dict(module=f'm{number:02}', exit_code=0) for number in range(1, 9)]
    rows, reports = [], {}
    for number in range(1, 9):
        path = quality / f'm{number:02}-320_375_390_414_430.json'
        report = read(path)
        assert report['files'] == files and report['styles'] == styles
        assert report['script_sha256'] == digest(ROOT / 'audit_initial_quality.py')
        assert report['widths'] == [320, 375, 390, 414, 430]
        for name, sha in report['fixture_script_sha256'].items():
            assert digest(ROOT / ('verify_' + name + '_controls.py')) == sha, name
        assert all(row['passed'] and not any(row['failures'].values()) for row in report['results'])
        rows.extend(report['results'])
        reports[path.relative_to(ROOT).as_posix()] = digest(path)
    ids = {page['id'] for page in read(DEMO / 'manifest.json')}
    assert len(ids) == 114 and len(rows) == 570
    assert {(row['page'], row['width']) for row in rows} == {
        (page, width) for page in ids for width in [320, 375, 390, 414, 430]}
    keyboards = [row for row in rows if row['width'] == 390]
    assert len(keyboards) == 114
    assert all(row['keyboard'] and not row['keyboard']['unreached'] and
               not row['keyboard']['noVisibleFocus'] for row in keyboards)
    followup_path = out / 'quality-followup-executions.json'
    followup = read(followup_path)
    assert followup['files'] == files and followup['styles'] == styles
    assert len(followup['results']) == len(JOBS) == 4
    for name, sha in followup['scripts_sha256'].items():
        assert digest(ROOT / name) == sha, name
    for (script, filename, expected), record in zip(JOBS, followup['results']):
        assert record['script'] == script and record['report'] == filename
        assert record['exit_code'] == 0 and record['cases'] == record['passed'] == expected
        path = out / filename
        report = read(path)
        assert report['files'] == files and digest(path) == record['report_sha256']
        assert len(report['results']) == expected
        assert all(case['passed'] and not case.get('errors') for case in report['results'])
        if 'styles' in report:
            assert report['styles'] == styles
        reports[path.relative_to(ROOT).as_posix()] = digest(path)
    focus = read(out / 'overlay-entry-focus/results.json')
    assert focus['locator_candidates_sha256'] == digest(out / 'hidden-overlay-observations.json')
    assert len({(row.get('index'), row.get('width'), row.get('case')) for row in focus['results']}) == 84
    screenshots = {f'evidence/current/overlay-entry-focus/entry-72-{width}.png':
                   digest(out / f'overlay-entry-focus/entry-72-{width}.png')
                   for width in [320, 375, 390, 414, 430]}
    reports[followup_path.relative_to(ROOT).as_posix()] = digest(followup_path)
    reports[(quality / 'serial-executions.json').relative_to(ROOT).as_posix()] = digest(quality / 'serial-executions.json')
    for page in ids:
        assert (DEMO / 'custom' / (page + '.html')).read_bytes() == (DEMO / 'pages' / (page + '.html')).read_bytes()
    for name, sha in {**files, **styles}.items():
        with urlopen(BASE + name.replace('custom/', 'pages/', 1), timeout=10) as response:
            assert response.headers.get('Cache-Control') == 'no-store'
            assert hashlib.sha256(response.read()).hexdigest() == sha, name
    state_path = out / 'current-evidence-state.json'
    state = read(state_path)
    # This is a frozen-source replay, so unrelated current proofs must stay intact.
    assert state['files'] == files
    retained_counts = {key: state[key] for key in ['current_initial_controls', 'current_overlay_exit_total',
                      'current_overlay_form_save_checks', 'current_confirmed_deletion_checks',
                      'current_identity_cases', 'current_book_candidate_deletion_checks',
                      'current_continuous_journey_cases', 'current_continuous_journey_steps',
                      'current_failure_trace_cases', 'current_failure_literal_observed']}
    assert retained_counts['current_initial_controls'] == 752
    assert retained_counts['current_overlay_exit_total'] == 498
    assert retained_counts['current_continuous_journey_steps'] == 54
    assert retained_counts['current_failure_trace_cases'] == 110
    checkpoint = dict(files=files, styles=styles, reports_sha256=reports,
                      screenshots_sha256=screenshots, scripts_sha256={
                          **followup['scripts_sha256'], **{name: digest(ROOT / name) for name in
                          ['verify_current_quality_checkpoint.py', 'run_initial_quality_serial.py',
                           'audit_current_runtime.py', 'book_test_helpers.py',
                           *('verify_' + module + '_controls.py' for module in
                             ['record', 'moment', 'time', 'workshop', 'settings', 'pet', 'book'])]}},
                      executions=dict(serial=dict(session_id=args.serial_session, exit_code=0),
                                      followup=dict(session_id=args.followup_session, exit_code=0)),
                      pages=114, layout_cases=570, keyboard_pages=114,
                      keyboard_visits=sum(len(row['keyboard']['visited']) for row in keyboards),
                      focus_cases=84, repair_cases=5, danger_cases=18, primary_cases=5,
                      retained_current_counts=retained_counts, accepted_pages=0,
                      scope='570 canonical initial geometry observations at844px height with44/34simulated safe insets and114 actual390px Tab traversals. Separate112followups:84form/default-focus outcomes with420px viewport pressure,5search/focus and23danger/primary cases. Reduced motion throughout. Not all dynamic states, real IME, screen-reader narration, contrast or final product acceptance.')
    encoded = json.dumps(checkpoint, ensure_ascii=False, indent=2) + '\n'
    (quality / 'checkpoint.json').write_text(encoded, encoding='utf-8')
    (out / 'overlay-entry-focus/checkpoint.json').write_text(encoded, encoding='utf-8')
    state.update(style_dependencies=styles, current_initial_quality_pages=114,
                 current_initial_quality_layout_cases=570, current_initial_quality_keyboard_pages=114,
                 current_initial_quality_repair_cases=5, current_overlay_entry_focus_cases=84,
                 current_danger_confirmation_cases=18, current_primary_contract_cases=5,
                 initial_quality_current_checkpoint='evidence/current/initial-quality/checkpoint.json',
                 accepted_pages=0)
    assert all(state[key] == count for key, count in retained_counts.items())
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(pages=114, layout=570, keyboard_pages=114,
                         keyboard_visits=checkpoint['keyboard_visits'], focus=84,
                         repairs=5, danger=23, accepted_pages=0)))


if __name__ == '__main__':
    main()
