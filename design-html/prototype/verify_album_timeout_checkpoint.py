"""Bind actual timeout executions and the affected-path replay without relabeling older proofs."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

from verify_pet_controls import ROOT, DEMO, BASE, source


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--regression-session', type=int, required=True)
    parser.add_argument('--regression-exit', type=int, required=True)
    args = parser.parse_args()
    assert args.regression_exit == 0
    folder = ROOT / 'evidence/current/album-timeout'
    current = source()
    styles = {p.relative_to(DEMO).as_posix(): sha(p) for p in (DEMO / 'assets').glob('*.css')}
    baseline = read(ROOT / 'evidence/baseline/album-timeout/results.json')
    green = read(folder / 'results.json')
    regression = read(folder / 'regressions.json')
    scope = read(folder / 'source-scope.json')
    changed = [name for name in current if current[name] != baseline['files'][name]]
    assert set(current) == set(baseline['files'])
    assert changed == ['assets/prototype-workshop-store.js'], changed
    assert baseline['files'][changed[0]] == scope['before_sha256']
    assert current[changed[0]] == scope['after_sha256']
    assert scope['outside_function_unchanged'] and len(scope['decoder_calls']) == 2
    assert len(scope['album_callers']) == 1
    assert "page==='m05-p08'" in scope['album_callers'][0]['conditions']
    assert scope['script_sha256'] == sha(ROOT / 'audit_album_timeout_scope.cjs')
    assert green['files'] == regression['files'] == current
    assert green['styles'] == regression['styles'] == baseline['styles'] == styles
    assert green['script_sha256'] == sha(ROOT / 'verify_album_request_timeout.py')
    assert regression['script_sha256'] == sha(ROOT / 'refresh_album_timeout_regressions.py')
    assert len(baseline['results']) == 3 and sum(r['passed'] for r in baseline['results']) == 1
    assert len(green['results']) == 3
    assert all(r['passed'] and not r['errors'] and r['native_request_observed'] for r in green['results'])
    cases = {r['case']: r for r in green['results']}
    assert cases['timeout-retry']['explicit_retry_saved_once']
    assert cases['timeout-late-response']['late_response_did_not_write']
    assert cases['before-deadline-success']['stable_after_deadline']
    expected = [('verify_work_album_decode.py', 10), ('verify_workshop_controls.py', 92),
                ('verify_workshop_flow.py', 3), ('verify_workshop_states.py', 8),
                ('verify_product_journey.py', 1)]
    assert [(r['script'], r['cases']) for r in regression['results']] == expected
    reports = {}
    for row in regression['results']:
        assert row['exit_code'] == 0 and row['passed'] == row['cases'] and row['errors'] == 0
        assert row['script_sha256'] == sha(ROOT / row['script'])
        assert row['report_sha256'] == sha(ROOT / row['report'])
        payload = read(ROOT / row['report'])
        entries = payload['results'] if isinstance(payload, dict) else payload
        assert len(entries) == row['cases'] and all(r['passed'] and not r.get('errors') for r in entries)
        for name, digest in row['artifacts_sha256'].items():
            assert sha(ROOT / name) == digest, name
        for name, digest in row['original_files_sha256'].items():
            assert sha(ROOT / name) == digest, 'Earlier evidence overwritten: ' + name
        if row['script'] == 'verify_product_journey.py':
            assert len(entries[0]['steps']) == 22
        reports[row['report']] = row['report_sha256']
    # No-store preview must serve the real changed helper and its actual caller.
    for name in ['assets/prototype-workshop-store.js', 'assets/prototype-workshop.js', 'pages/m05-p08.html']:
        with urlopen(BASE + name, timeout=10) as response:
            raw = response.read()
            assert 'no-store' in response.headers.get('Cache-Control', '')
        assert hashlib.sha256(raw).hexdigest() == sha(DEMO / name), name
    checkpoint = dict(files=current, styles=styles, accepted_pages=0,
                      timeout_cases=3, affected_regression_cases=114, journey_steps=22,
                      actual_executions=dict(baseline_session=73490, baseline_exit=1,
                                             timeout_session=12936, timeout_exit=0,
                                             regression_session=args.regression_session, regression_exit=0),
                      reports_sha256=reports,
                      timeout_report_sha256=sha(folder / 'results.json'),
                      source_scope_sha256=sha(folder / 'source-scope.json'),
                      verification_script_sha256=sha(Path(__file__)),
                      scope='Native timeout and affected album paths only. Earlier full-source reports retain their original source manifests; not a new full114-page replay or human visual acceptance.')
    (folder / 'checkpoint.json').write_text(json.dumps(checkpoint, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(timeout_cases=3, affected_regression_cases=114, journey_steps=22, accepted_pages=0)))


if __name__ == '__main__':
    main()
