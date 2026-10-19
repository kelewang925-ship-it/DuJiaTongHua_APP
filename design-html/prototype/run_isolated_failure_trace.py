"""Keep earlier source-bound reports intact while recording a fresh trace."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parent


def main():
    p=argparse.ArgumentParser();p.add_argument('script');p.add_argument('report');a=p.parse_args()
    assert Path(a.script).name==a.script and Path(a.report).name==a.report
    out=ROOT/'evidence/current';prefix=a.report.removesuffix('-results.json')
    prefixes=(prefix,'diary-long-detail-')if prefix=='diary-state'else(prefix,)
    saved={path:path.read_bytes()for path in out.iterdir()if path.name.startswith(prefixes)
           if path.is_file()and not path.name.endswith('-failure-trace.json')}
    history=ROOT/'evidence/history/pre-isolated-failure-traces-53fb10f'/prefix
    history.mkdir(parents=True,exist_ok=True)
    for path,raw in saved.items():
        if not(history/path.name).exists():(history/path.name).write_bytes(raw)
    code=1
    try:
        result=subprocess.run([sys.executable,str(ROOT/'trace_failure_suite.py'),a.script,a.report])
        code=result.returncode
        trace_path=out/(prefix+'-failure-trace.json')
        assert trace_path.exists(),'No trace generated; original reports will be restored.'
        trace=json.loads(trace_path.read_text(encoding='utf-8'))
        report=out/('failure-traced-'+a.report)
        shutil.copy2(out/a.report,report)
        assert hashlib.sha256(report.read_bytes()).hexdigest()==trace['report_sha256']
        trace['report']=report.name
        trace['isolated_execution']=dict(wrapper='run_isolated_failure_trace.py',child_exit_code=code,
                                         original_report_restored=True)
        trace_path.write_text(json.dumps(trace,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        screenshots=out/'failure-traces/screenshots'/prefix;screenshots.mkdir(parents=True,exist_ok=True)
        for path in [p for p in out.iterdir()if p.name.startswith(prefixes)and p.suffix=='.png']:
            shutil.copy2(path,screenshots/path.name)
            if path not in saved:path.unlink()
    finally:
        for path,raw in saved.items():path.write_bytes(raw)
    raise SystemExit(code)


if __name__=='__main__':main()
