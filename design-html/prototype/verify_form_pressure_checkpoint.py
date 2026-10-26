"""Verify explicit form-pressure and duplicate-failure evidence before publishing it."""
import hashlib
import json
from pathlib import Path

from audit_hidden_overlays import MODULES
from verify_pet_controls import ROOT, DEMO, source


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    folder = ROOT / 'evidence/current/page-form-pressure'
    original = read(folder / 'results.json')
    supplemental = read(folder / 'accepted-code-results.json')
    failures_path = ROOT / 'evidence/current/duplicate-failure-sites/results.json'
    failures = read(failures_path)
    current = source()
    assert original['files'] == supplemental['files'] == failures['files'] == current
    assert original['script_sha256'] == digest(folder / 'executed-initial.py')
    assert supplemental['script_sha256'] == digest(ROOT / 'verify_page_form_pressure.py')
    assert failures['script_sha256'] == digest(ROOT / 'verify_duplicate_failure_sites.py')
    assert failures['tracer_sha256'] == digest(ROOT / 'trace_failure_suite.py')
    assert [len(r['results']) for r in [original, supplemental, failures]] == [96, 2, 5]
    assert all(r['passed'] and not r['errors'] for report in [original, supplemental, failures] for r in report['results'])
    for name, value in original['locator_candidates_sha256'].items():
        assert digest(ROOT / name) == value, name
    for width in [320, 390]:
        rows = [r for r in original['results'] if r['width'] == width]
        assert len([r for r in rows if r['mode'] == 'long-input']) == 29
        assert len([r for r in rows if r['mode'] == 'normal-action']) == 19
        fixed = next(r for r in supplemental['results'] if r['width'] == width)
        assert fixed['page'] == 'm02-p03' and len(fixed['fields']) == 4
        assert all(f['actual_length'] == f['max'] == 2 for f in fixed['fields'])
        # Original invitation observations verified rejection of the invalid
        # prefix; this supplemental case verifies accepted characters as well.
        for row in rows:
            if row['mode'] == 'long-input' and row['page'] != 'm02-p03':
                assert all(f['actual_length'] > 0 for f in row['fields'] if 'actual_length' in f)
    expected = {'credentials-retry-page': ('prototype-auth-flow.js', 197),
                'otp-resend': ('prototype-auth-flow.js', 148),
                'recovery-verify': ('prototype-auth-flow.js', 119),
                'recovery-send-code': ('prototype-auth-flow.js', 71),
                'work-save-generate': ('prototype-workshop.js', 33)}
    for row in failures['results']:
        file, line = expected[row['case']]
        assert f'/{file}:{line}:' in row['consumed_event']['stack']
        assert row['failure_preserved_data'] and row['explicit_retry_succeeded']
    fixtures = set(MODULES.values()) | {'audit_hidden_overlays.py', 'audit_runtime.py',
                  'audit_current_runtime.py', 'book_test_helpers.py',
                  'verify_native_shared_fields.py', 'verify_native_field_flows.py', 'trace_failure_suite.py'}
    checkpoint = dict(files=current,
                      styles={p.relative_to(DEMO).as_posix(): digest(p) for p in (DEMO / 'assets').glob('*.css')},
                      fixture_scripts_sha256={name: digest(ROOT / name) for name in sorted(fixtures)},
                      reports_sha256={p.relative_to(ROOT).as_posix(): digest(p) for p in [folder / 'results.json', folder / 'accepted-code-results.json', failures_path]},
                      scripts_sha256={name: digest(ROOT / name) for name in ['verify_page_form_pressure.py', 'verify_duplicate_failure_sites.py', 'verify_form_pressure_checkpoint.py']},
                      actual_executions=[dict(session=32913, exit_code=0, cases=96),
                                         dict(output='d6531f', exit_code=0, cases=2),
                                         dict(session=43624, exit_code=0, cases=5)],
                      accepted_pages=0, long_input_contexts=58, short_normal_actions=38,
                      accepted_invite_supplement=2, duplicate_failure_entrances=5,
                      scope='Specific original form and mock failure entrance contracts only. No product change, full114-page acceptance, human visual approval or mobile IME claim.')
    (folder / 'checkpoint.json').write_text(json.dumps(checkpoint, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(initial=96, accepted_invite_supplement=2, duplicate_failure_entrances=5, accepted_pages=0)))


if __name__ == '__main__':
    main()
