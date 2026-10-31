"""Replay declared exception suites in isolation, retaining completed exact-source jobs."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from verify_pet_controls import ROOT, source

JOBS = [
    ('verify_pet_states.py', 'pet-state-results.json', 7),
    ('verify_book_states.py', 'book-state-results.json', 6),
    ('verify_photo_states.py', 'photo-state-results.json', 4),
    ('verify_settings_states.py', 'settings-state-results.json', 9),
    ('verify_onboarding_faults.py', 'onboarding-fault-results.json', 4),
    ('verify_anniversary_states.py', 'anniversary-state-results.json', 7),
    ('verify_capsule_states.py', 'capsule-state-results.json', 5),
    ('verify_diary_states.py', 'diary-state-results.json', 12),
    ('verify_moment_states.py', 'moment-state-results.json', 6),
    ('verify_workshop_states.py', 'workshop-state-results.json', 8),
    ('verify_pet_life_states.py', 'pet-life-state-results.json', 12),
    ('verify_book_editor_draft.py', 'book-editor-draft-results.json', 7),
    ('verify_remaining_failure_operations.py', 'remaining-failures-results.json', 18),
    ('verify_last_failure_operations.py', 'last-failures-results.json', 5),
]
OUT = ROOT / 'evidence/current'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    files = source()
    styles = {p.relative_to(ROOT.parent).as_posix(): digest(p)
              for p in sorted((ROOT.parent / 'assets').glob('*.css'))}
    scripts = {name: digest(ROOT / name) for name in
               ['refresh_failure_traces.py', 'run_isolated_failure_trace.py',
                'trace_failure_suite.py', *(job[0] for job in JOBS)]}
    # Keep the authoritative original reports intact while traces get dedicated copies.
    preserved = {name: digest(OUT / name) for _, name, _ in JOBS if (OUT / name).exists()}
    checkpoint = OUT / 'current-initial-replay/checkpoint.json'
    initial = json.loads(checkpoint.read_text(encoding='utf-8'))
    assert initial['files'] == files and initial['styles'] == styles
    preservation = {checkpoint.relative_to(ROOT).as_posix(): digest(checkpoint)}
    for name, sha in initial['reports_sha256'].items():
        artifact = ROOT / name if (ROOT / name).exists() else OUT / name
        assert digest(artifact) == sha, name
        preservation[artifact.relative_to(ROOT).as_posix()] = sha
    destination = OUT / 'failure-trace-refresh-source.json'
    rows = []
    if args.resume:
        old = json.loads(destination.read_text(encoding='utf-8'))
        assert old['files'] == files and old['styles'] == styles
        assert old['scripts_sha256'] == scripts and old['preserved_reports'] == preserved
        assert old['initial_preservation'] == preservation
        for job, row in zip(JOBS, old['results']):
            if row['exit_code'] != 0:
                break
            assert row['script'] == job[0] and row['cases'] == row['passed'] == job[2]
            assert digest(OUT / row['trace']) == row['trace_sha256']
            assert digest(OUT / row['report']) == row['report_sha256']
            rows.append(row)

    def save():
        assert source() == files
        assert {p.relative_to(ROOT.parent).as_posix(): digest(p)
                for p in sorted((ROOT.parent / 'assets').glob('*.css'))} == styles
        assert all(digest(OUT / name) == sha for name, sha in preserved.items())
        assert all(digest(ROOT / name) == sha for name, sha in preservation.items())
        value = dict(files=files, styles=styles, scripts_sha256=scripts,
                     preserved_reports=preserved, initial_preservation=preservation,
                     results=rows, expected_suites=len(JOBS), expected_cases=110,
                     accepted_pages=0,
                     scope='Actual consumed failNext hooks in 14 declared suites. All-operation branches, source/permission, native decoder, layout and final acceptance remain separate.')
        temporary = destination.with_suffix('.json.tmp')
        temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        temporary.replace(destination)

    for script, original, count in JOBS[len(rows):]:
        print('START ' + script, flush=True)
        result = subprocess.run([sys.executable, str(ROOT / 'run_isolated_failure_trace.py'), script, original])
        trace_name = original.replace('-results.json', '-failure-trace.json')
        trace = json.loads((OUT / trace_name).read_text(encoding='utf-8'))
        row = dict(script=script, exit_code=result.returncode, cases=trace['cases'],
                   passed=trace['passed'], trace=trace_name, trace_sha256=digest(OUT / trace_name),
                   report=trace['report'], report_sha256=trace['report_sha256'])
        rows.append(row)
        save()
        if result.returncode:
            raise SystemExit(result.returncode)
        assert trace['files'] == files and trace['exit_code'] == 0
        assert trace['script_sha256'] == scripts[script]
        assert trace['cases'] == trace['passed'] == count
        assert digest(OUT / trace['report']) == trace['report_sha256']
        print('DONE ' + script + ' ' + str(count), flush=True)
    assert len(rows) == len(JOBS) and sum(r['cases'] for r in rows) == 110
    save()
    print(json.dumps(dict(suites=len(rows), cases=110, passed=110, accepted_pages=0)), flush=True)


if __name__ == '__main__':
    main()
