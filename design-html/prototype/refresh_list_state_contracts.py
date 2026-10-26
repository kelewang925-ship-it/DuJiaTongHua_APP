"""Replay the three explicitly stale list-state suites with isolated report output."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from verify_pet_controls import ROOT, DEMO, source

JOBS = [('states', 'verify_shared_list_states.py', 'shared-list-states-results.json', 110),
        ('loading', 'verify_shared_list_loading.py', 'shared-list-loading-results.json', 30),
        ('widths', 'verify_shared_loading_widths.py', 'shared-loading-widths.json', 50)]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--resume',action='store_true'); args = parser.parse_args()
    files = source(); styles = {p.relative_to(DEMO).as_posix():sha(p) for p in (DEMO/'assets').glob('*.css')}
    out = ROOT/'evidence/current/list-state-refresh'; out.mkdir(parents=True,exist_ok=True)
    metadata = out/'executions.json'; rows=[]
    originals = {name:sha(ROOT/'evidence/current'/name) for _,_,name,_ in JOBS}
    if metadata.exists():
        assert args.resume
        previous=json.loads(metadata.read_text(encoding='utf-8'))
        assert previous['files']==files and previous['styles']==styles and previous['script_sha256']==sha(Path(__file__))
        assert previous['original_reports_sha256']==originals
        for row in previous['results']:
            if row['exit_code']==0 and row['passed']==row['expected']:
                assert sha(ROOT/row['report'])==row['report_sha256'] and sha(ROOT/row['script'])==row['script_sha256']
                rows.append(row)
    completed={row['name'] for row in rows}
    for name,script,original,expected in JOBS:
        if name in completed:continue
        print('START '+script,flush=True)
        target=out/(name+'.json')
        run=subprocess.run([sys.executable,str(ROOT/'run_suite_report_isolated.py'),'--script',str(ROOT/script),
                            '--report',str(ROOT/'evidence/current'/original),'--output',str(target)],
                           capture_output=True,text=True,encoding='utf-8')
        (out/(name+'.log')).write_text(run.stdout+run.stderr,encoding='utf-8')
        payload=json.loads(target.read_text(encoding='utf-8'));assert payload['files']==files
        cases=payload['results'];row=dict(name=name,script=script,script_sha256=sha(ROOT/script),
                                          exit_code=run.returncode,expected=expected,cases=len(cases),
                                          passed=sum(case['passed'] for case in cases),errors=sum(len(case.get('errors',[])) for case in cases),
                                          report=target.relative_to(ROOT).as_posix(),report_sha256=sha(target))
        assert source()==files
        assert originals=={n:sha(ROOT/'evidence/current'/n) for _,_,n,_ in JOBS}
        rows.append(row)
        manifest=dict(files=files,styles=styles,results=rows,original_reports_sha256=originals,
                      script_sha256=sha(Path(__file__)),wrapper_sha256=sha(ROOT/'run_suite_report_isolated.py'),
                      expected_cases=190,accepted_pages=0,
                      scope='22 Empty/Error contexts at5 widths,10 real transient list-load functions in3 scenarios, and10 skeleton surfaces at5 widths. No promotion of old reports or human visual acceptance.')
        temporary=metadata.with_suffix('.json.tmp');temporary.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temporary.replace(metadata)
        print(json.dumps({key:row[key] for key in ['name','exit_code','cases','passed','errors']}),flush=True)
        if run.returncode or len(cases)!=expected or row['passed']!=expected or row['errors']:
            print(run.stdout[-2000:]+run.stderr[-1000:],flush=True);raise SystemExit(1)
    assert sum(row['cases'] for row in rows)==190
    print('190/190 list state contracts passed',flush=True)


if __name__=='__main__':main()
