"""Bound Chrome lifetime and memory by auditing one module at a time."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from verify_pet_controls import ROOT, source


def main():
    files=source(); executions=[]; destination=ROOT/'evidence/current/initial-quality/serial-executions.json'
    for number in range(1,9):
        module=f'm{number:02}'
        result=subprocess.run([sys.executable,str(ROOT/'audit_initial_quality.py'),'--modules',module,'--widths','320,375,390,414,430'],cwd=ROOT.parents[1])
        executions.append(dict(module=module,exit_code=result.returncode))
        assert source()==files
        destination.write_text(json.dumps(dict(files=files,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),audit_script_sha256=hashlib.sha256((ROOT/'audit_initial_quality.py').read_bytes()).hexdigest(),executions=executions),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(f'MODULE_DONE {module} exit={result.returncode}',flush=True)
        if result.returncode:raise SystemExit(result.returncode)


if __name__=='__main__':main()
