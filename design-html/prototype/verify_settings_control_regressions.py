"""Preserve historical settings evidence and rerun current affected flows."""
import json,hashlib,subprocess,sys,shutil
from verify_settings_controls import ROOT,source
OUT=ROOT/'evidence/current';HISTORY=ROOT/'evidence/history/pre-settings-controls-e411ac1';HISTORY.mkdir(parents=True,exist_ok=True);files=source();reports={}
for p in OUT.glob('settings-*'):
    if p.name.startswith(('settings-control','settings-sheet')):continue
    dest=HISTORY/p.name
    if not dest.exists():shutil.copy2(p,dest)
for script,name in [('verify_settings_flow.py','settings-flow-results.json'),('verify_settings_states.py','settings-state-results.json')]:
    run=subprocess.run([sys.executable,str(ROOT/script)]);p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));assert files==source();reports[name]=dict(exit_code=run.returncode,cases=len(v),passed=sum(r['passed']for r in v),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
assert files==source();(OUT/'settings-control-regression-source.json').write_text(json.dumps(dict(files=files,reports=reports),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(v['exit_code']==0 and v['passed']==v['cases']for v in reports.values())else 1)
