"""Run current focus, long-field and danger checks without historical repair assumptions."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from verify_pet_controls import ROOT, source

JOBS = [
    ('verify_overlay_entry_focus.py', 'overlay-entry-focus/results.json', 84),
    ('verify_initial_quality_repairs.py', 'initial-quality/repair-behavior-results.json', 5),
    ('verify_danger_confirmations.py', 'danger-confirmation-results.json', 18),
    ('verify_danger_primary_contract.py', 'danger-primary-contract-results.json', 5),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def styles():
    return {p.relative_to(ROOT.parent).as_posix(): digest(p)
            for p in sorted((ROOT.parent / 'assets').glob('*.css'))}


def main():
    out = ROOT / 'evidence/current'
    files, css = source(), styles()
    rows = []
    scripts = {name: digest(ROOT / name) for name in
               ['refresh_quality_followups.py', 'audit_initial_quality.py',
                'audit_hidden_overlays.py', 'verify_overlay_form_saves.py',
                *(job[0] for job in JOBS)]}
    for script, report, expected in JOBS:
        assert source() == files and styles() == css
        print('START ' + script, flush=True)
        execution = subprocess.run([sys.executable, str(ROOT / script)])
        assert source() == files and styles() == css
        payload = json.loads((out / report).read_text(encoding='utf-8'))
        cases = payload['results']
        assert payload['files'] == files
        row = dict(script=script, exit_code=execution.returncode, report=report,
                   report_sha256=digest(out / report), expected=expected, cases=len(cases),
                   passed=sum(bool(case['passed']) for case in cases))
        rows.append(row)
        metadata = dict(files=files, styles=css, scripts_sha256=scripts, results=rows,
                        expected_cases=112, accepted_pages=0,
                        scope='84 form/default-focus outcomes at five widths with420px viewport pressure,5 search/focus cases,18danger and5primary contracts. No real mobile IME, screen-reader or final product acceptance.')
        destination = out / 'quality-followup-executions.json'
        temporary = destination.with_suffix('.json.tmp')
        temporary.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        temporary.replace(destination)
        if execution.returncode:
            raise SystemExit(execution.returncode)
        assert len(cases) == row['passed'] == expected
        assert all(not case.get('errors') for case in cases)
        print('DONE ' + script + ' ' + str(expected), flush=True)
    print(json.dumps(dict(cases=112, passed=112, accepted_pages=0)), flush=True)


if __name__ == '__main__':
    main()
