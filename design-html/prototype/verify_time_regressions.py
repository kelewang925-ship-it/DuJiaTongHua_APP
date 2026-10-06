"""Retain old reports, run existing scoped scenarios, bind them to tested sources."""
from pathlib import Path
import json,hashlib,subprocess,sys,shutil
ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent;OUT=ROOT/'evidence/current'
def source():return {p.relative_to(DEMO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in list((DEMO/'custom').glob('*.html'))+list((DEMO/'assets').glob('prototype-*.*'))}
files=source();history=ROOT/'evidence/history/pre-time-controls-4f89521';history.mkdir(parents=True,exist_ok=True)
for prefix in ['anniversary','capsule']:
    for p in OUT.glob(prefix+'*'):
        dest=history/p.name
        if not dest.exists():shutil.copy2(p,dest)
reports={}
for script,report in [('verify_anniversary_flow.py','anniversary-flow-results.json'),('verify_anniversary_states.py','anniversary-state-results.json'),('verify_capsule_flow.py','capsule-flow-results.json'),('verify_capsule_states.py','capsule-state-results.json')]:
    result=subprocess.run([sys.executable,str(ROOT/script)],check=False)
    rows=json.loads((OUT/report).read_text(encoding='utf-8'));assert files==source();reports[report]=dict(exit_code=result.returncode,cases=len(rows),passed=sum(bool(r['passed'])for r in rows),sha256=hashlib.sha256((OUT/report).read_bytes()).hexdigest())
assert files==source();(OUT/'time-regression-source.json').write_text(json.dumps(dict(files=files,reports=reports),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(v['exit_code']==0 and v['passed']==v['cases']for v in reports.values())else 1)
