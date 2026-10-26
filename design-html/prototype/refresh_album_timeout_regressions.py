"""Replay affected album paths in dedicated artifacts, preserving earlier reports/screenshots."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from verify_pet_controls import ROOT, source

OUT = ROOT / 'evidence/current'
DEST = OUT / 'album-timeout/regressions'
HISTORY = ROOT / 'evidence/history/pre-album-1d96f61/originals'
JOBS = [
    ('decode', 'verify_work_album_decode.py', 'work-album-decode/results.json', 10, None, []),
    ('controls', 'verify_workshop_controls.py', 'workshop-controls-results.json', 92, None, []),
    ('flow', 'verify_workshop_flow.py', 'workshop-flow-results.json', 3, None,
     ['workshop-free', 'workshop-shared', 'workshop-film']),
    ('state', 'verify_workshop_states.py', 'workshop-state-results.json', 8, None, ['workshop-state-']),
    ('journey', 'verify_product_journey.py', 'product-journey-results.json', 1, 'product-journey', []),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def watched(report, directory, prefixes):
    paths = {OUT / report} if (OUT / report).exists() else set()
    if directory:
        paths.update((OUT / directory).glob('*.png'))
    paths.update(p for p in OUT.glob('*.png') if any(p.name.startswith(prefix) for prefix in prefixes))
    for path in paths:
        path.resolve().relative_to(OUT.resolve())
    return paths


def main():
    files = source()
    styles = {p.relative_to(ROOT.parent).as_posix(): digest(p)
              for p in (ROOT.parent / 'assets').glob('*.css')}
    rows = []
    DEST.mkdir(parents=True, exist_ok=True)
    for name, script, report, expected, directory, prefixes in JOBS:
        saved = {p: p.read_bytes() for p in watched(report, directory, prefixes)}
        history = HISTORY / name
        history.mkdir(parents=True, exist_ok=True)
        for path, raw in saved.items():
            target = history / path.name
            if target.exists():
                assert target.read_bytes() == raw
            else:
                target.write_bytes(raw)
        target = DEST / name
        target.mkdir(parents=True, exist_ok=True)
        print('START ' + script, flush=True)
        try:
            execution = subprocess.run([sys.executable, str(ROOT / script)], capture_output=True,
                                       text=True, encoding='utf-8')
            (target / 'execution.log').write_text(execution.stdout + execution.stderr, encoding='utf-8')
            artifact_files = {}
            for path in watched(report, directory, prefixes):
                if path.name == 'failure.png' and execution.returncode == 0:
                    continue
                artifact = target / path.name
                artifact.write_bytes(path.read_bytes())
                artifact_files[artifact.relative_to(ROOT).as_posix()] = digest(artifact)
            artifact_report = target / Path(report).name
            payload = json.loads(artifact_report.read_text(encoding='utf-8'))
            cases = payload['results'] if isinstance(payload, dict) else payload
            if isinstance(payload, dict):
                assert payload['files'] == files
            row = dict(script=script, script_sha256=digest(ROOT / script), exit_code=execution.returncode,
                       report=artifact_report.relative_to(ROOT).as_posix(), report_sha256=digest(artifact_report),
                       cases=len(cases), passed=sum(bool(case['passed']) for case in cases),
                       errors=sum(len(case.get('errors', [])) for case in cases),
                       artifacts_sha256=artifact_files,
                       original_files_sha256={p.relative_to(ROOT).as_posix(): hashlib.sha256(raw).hexdigest()
                                               for p, raw in saved.items()})
        finally:
            for path in watched(report, directory, prefixes):
                if path not in saved:
                    path.resolve().relative_to(OUT.resolve())
                    path.unlink()
            for path, raw in saved.items():
                path.write_bytes(raw)
        assert all(p.read_bytes() == raw for p, raw in saved.items())
        assert source() == files
        assert {p.relative_to(ROOT.parent).as_posix(): digest(p)
                for p in (ROOT.parent / 'assets').glob('*.css')} == styles
        rows.append(row)
        metadata = dict(files=files, styles=styles, script_sha256=digest(Path(__file__)), results=rows,
                        expected_cases=114, accepted_pages=0,
                        scope='Affected native decode10,workshop103 andone22-stage product chain. Dedicated new artifacts; prior original reports/screenshots restored byte-for-byte. Other source-wide proofs retain original manifests.')
        (OUT / 'album-timeout/regressions.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps({key: row[key] for key in ['script', 'exit_code', 'cases', 'passed', 'errors']}), flush=True)
        if execution.returncode or row['cases'] != expected or row['passed'] != expected or row['errors']:
            print(execution.stdout[-3500:] + execution.stderr[-1000:], flush=True)
            raise SystemExit(1)
    assert sum(row['cases'] for row in rows) == 114
    print(json.dumps(dict(cases=114, passed=114, journey_steps=22)), flush=True)


if __name__ == '__main__':
    main()
