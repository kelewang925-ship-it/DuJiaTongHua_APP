"""Run existing workshop flows and bind results to current product sources."""
from pathlib import Path
import json,hashlib,subprocess,sys
from verify_workshop_controls import ROOT,DEMO,source
OUT=ROOT/'evidence/current';files=source();reports={}
for script,name in [('verify_workshop_flow.py','workshop-flow-results.json'),('verify_workshop_states.py','workshop-state-results.json')]:
    run=subprocess.run([sys.executable,str(ROOT/script)]);p=OUT/name;rows=json.loads(p.read_text(encoding='utf-8'));assert files==source();reports[name]=dict(exit_code=run.returncode,cases=len(rows),passed=sum(v['passed']for v in rows),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
assert files==source();(OUT/'workshop-regression-source.json').write_text(json.dumps(dict(files=files,reports=reports),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(v['exit_code']==0 and v['passed']==v['cases']for v in reports.values())else 1)
