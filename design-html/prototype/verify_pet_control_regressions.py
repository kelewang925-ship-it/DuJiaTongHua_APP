"""Preserve pet reports, rerun normal/exception scenarios with source binding."""
import sys,json,hashlib,subprocess,shutil
from verify_pet_controls import ROOT,source
OUT=ROOT/'evidence/current';HISTORY=ROOT/'evidence/history/pre-pet-controls-7311c3b';HISTORY.mkdir(parents=True,exist_ok=True);files=source();reports={}
for prefix in ['pet-','adoption-']:
    for p in OUT.glob(prefix+'*'):
        if p.name.startswith(('pet-control','pet-hidden','pet-guard')):continue
        dest=HISTORY/p.name
        if not dest.exists():shutil.copy2(p,dest)
for script,name in [('verify_pet_flow.py','pet-flow-results.json'),('verify_pet_states.py','pet-state-results.json'),('verify_pet_life_flow.py','pet-life-flow-results.json'),('verify_pet_life_states.py','pet-life-state-results.json')]:
    run=subprocess.run([sys.executable,str(ROOT/script)]);p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));assert files==source();reports[name]=dict(exit_code=run.returncode,cases=len(v),passed=sum(r['passed']for r in v),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
assert files==source();(OUT/'pet-control-regression-source.json').write_text(json.dumps(dict(files=files,reports=reports),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(v['exit_code']==0 and v['passed']==v['cases']for v in reports.values())else 1)
