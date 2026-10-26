"""Refresh changed submission/return/image boundaries; preserve existing evidence files."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from verify_pet_controls import ROOT, DEMO, source

JOBS = [
    ('forms', 'verify_pending_form_cancel.py', 'pending-form-cancel/results.json', 96),
    ('form-helper', 'verify_pending_form_contract.py', 'pending-form-cancel/contract-results.json', 8),
    ('pages', 'verify_pending_page_guard.py', 'pending-page-guard/results.json', 52),
    ('page-helper', 'verify_pending_guard_contract.py', 'pending-page-guard/contract-results.json', 12),
    ('changes', 'verify_submission_changes.py', 'submission-changes/results.json', 19),
    ('capsule-date', 'verify_capsule_date_pending.py', 'capsule-date-pending-results.json', 3),
    ('image-exit', 'verify_image_pending_exit.py', 'image-pending-exit/results.json', 36),
    ('chooser', 'verify_file_chooser_pending.py', 'file-chooser-pending/results.json', 24),
    ('chooser-helper', 'verify_file_chooser_started.py', 'file-chooser-started/results.json', 4),
    ('decode-pending', 'verify_pending_image_reads.py', 'pending-image-read/results.json', 16),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--resume', action='store_true'); args = parser.parse_args()
    current = source(); styles = {p.relative_to(DEMO).as_posix(): sha(p) for p in (DEMO / 'assets').glob('*.css')}
    out = ROOT / 'evidence/current'; dest = out / 'submit-boundary-refresh'; dest.mkdir(parents=True, exist_ok=True)
    metadata = dest / 'executions.json'; rows = []
    if metadata.exists():
        assert args.resume, 'Explicit --resume required; retain completed exact-source jobs.'
        previous = json.loads(metadata.read_text(encoding='utf-8'))
        assert previous['files'] == current and previous['styles'] == styles and previous['script_sha256'] == sha(Path(__file__))
        for row in previous['results']:
            if row['exit_code'] == 0 and row['passed'] == row['expected']:
                assert sha(ROOT / row['script']) == row['script_sha256']
                assert sha(ROOT / row['report']) == row['report_sha256']
                assert all(sha(ROOT / name) == digest for name, digest in row['restored_originals_sha256'].items())
                rows.append(row)
    completed = {row['name'] for row in rows}
    for name, script, relative, expected in JOBS:
        if name in completed: continue
        original = out / relative; target = dest / name; target.mkdir(parents=True, exist_ok=True)
        # Watch only the report and screenshots owned by this suite, never other reports.
        parent = original.parent
        prefix = 'capsule-date-' if name == 'capsule-date' else None
        screenshots = lambda: set(parent.glob(prefix+'*.png' if prefix else '*.png'))
        paths = {original} | screenshots(); saved = {p: p.read_bytes() for p in paths if p.exists()}
        prior_report = target / 'prior-report.json'
        if not prior_report.exists() and original.exists(): prior_report.write_bytes(saved[original])
        print('START ' + script, flush=True)
        try:
            execution = subprocess.run([sys.executable, str(ROOT / script)], capture_output=True, text=True, encoding='utf-8')
            (target / 'execution.log').write_text(execution.stdout+execution.stderr, encoding='utf-8')
            report = target / 'results.json'; report.write_bytes(original.read_bytes())
            captured = {}
            for path in screenshots():
                if path not in saved or path.read_bytes() != saved[path]:
                    artifact = target / path.name; artifact.write_bytes(path.read_bytes()); captured[artifact.relative_to(ROOT).as_posix()] = sha(artifact)
            payload = json.loads(report.read_text(encoding='utf-8'))
            assert payload['files'] == current
            if 'styles' in payload: assert payload['styles'] == styles
            cases = payload['results']
            row = dict(name=name, script=script, script_sha256=sha(ROOT / script), exit_code=execution.returncode,
                       expected=expected, cases=len(cases), passed=sum(r['passed'] for r in cases),
                       errors=sum(len(r.get('errors', [])) for r in cases),
                       report=report.relative_to(ROOT).as_posix(), report_sha256=sha(report),
                       generated_screenshots_sha256=captured,
                       restored_originals_sha256={p.relative_to(ROOT).as_posix(): hashlib.sha256(raw).hexdigest() for p,raw in saved.items()})
        finally:
            for path in screenshots() | {original}:
                path.resolve().relative_to(out.resolve())
                if path not in saved: path.unlink(missing_ok=True)
            for path,raw in saved.items(): path.write_bytes(raw)
        assert all(p.read_bytes() == raw for p,raw in saved.items())
        assert source() == current
        assert {p.relative_to(DEMO).as_posix(): sha(p) for p in (DEMO / 'assets').glob('*.css')} == styles
        rows.append(row)
        manifest = dict(files=current, styles=styles, results=rows, expected_cases=sum(job[3] for job in JOBS),
                        script_sha256=sha(Path(__file__)), accepted_pages=0,
                        scope='Ten named pending submit/return/chooser/image suites. Existing reports/screenshots restored byte-for-byte;270 declared cases, including synthetic helper boundaries. Not a new full114-page acceptance.')
        metadata.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print(json.dumps({key:row[key] for key in ['name','exit_code','cases','passed','errors']}), flush=True)
        if execution.returncode or row['cases'] != expected or row['passed'] != expected or row['errors']:
            print(execution.stdout[-2000:]+execution.stderr[-1000:], flush=True)
            raise SystemExit(1)
    assert sum(row['cases'] for row in rows) == 270
    print('270/270 named submission boundary checks passed', flush=True)


if __name__ == '__main__':
    main()
