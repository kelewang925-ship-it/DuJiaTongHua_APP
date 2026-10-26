"""Replay named shared motion contracts, preserving earlier reports byte-for-byte."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from verify_pet_controls import ROOT, source


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    files = source()
    out = ROOT / 'evidence/current/final-motion'
    out.mkdir(parents=True, exist_ok=True)
    executions = []
    for script, report, expected in [('verify_motion.py', 'motion-results.json', 6),
                                      ('verify_token_motion_states.py', 'shared-token-motion-results.json', 2)]:
        original = ROOT / 'evidence/current' / report
        saved = original.read_bytes() if original.exists() else None
        print('START ' + script, flush=True)
        try:
            run = subprocess.run([sys.executable, str(ROOT / script)], capture_output=True, text=True, encoding='utf-8')
            (out / (script + '.log')).write_text(run.stdout + run.stderr, encoding='utf-8')
            artifact = out / report
            artifact.write_bytes(original.read_bytes())
        finally:
            if saved is None:
                original.unlink(missing_ok=True)
            else:
                original.write_bytes(saved)
        payload = json.loads(artifact.read_text(encoding='utf-8'))
        rows = payload['results'] if isinstance(payload, dict) else payload
        if isinstance(payload, dict):
            assert payload['files'] == files
        execution = dict(script=script, script_sha256=sha(ROOT / script),
                         exit_code=run.returncode, cases=len(rows), passed=sum(r['passed'] for r in rows),
                         report=artifact.relative_to(ROOT).as_posix(), report_sha256=sha(artifact),
                         prior_report_restored_sha256=hashlib.sha256(saved).hexdigest() if saved else None)
        executions.append(execution)
        assert source() == files
        checkpoint = dict(files=files, executions=executions, script_sha256=sha(Path(__file__)),
                          accepted_pages=0,
                          scope='Six shared motion contracts and two archived/current CSS mode comparisons. Not full114-page motion, hardware touch, IME, or human visual acceptance.')
        (out / 'executions.json').write_text(json.dumps(checkpoint, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(execution), flush=True)
        assert run.returncode == 0 and len(rows) == expected and all(r['passed'] and not r.get('errors') for r in rows), run.stdout + run.stderr
    print('8/8 named motion and appearance checks passed', flush=True)


if __name__ == '__main__':
    main()
