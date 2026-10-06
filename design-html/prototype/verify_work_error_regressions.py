"""Work state component fix: current-source execution and exact report provenance."""
import json,subprocess,sys,hashlib
from verify_pet_controls import ROOT,source
OUT=ROOT/'evidence/current';files=source();reports={}
jobs=[('verify_work_cancel_navigation.py','work-cancel-navigation-results.json'),('verify_work_error_states.py','work-error-results.json'),('verify_work_error_refresh.py','work-error-refresh-results.json'),('verify_workshop_recovery.py','workshop-recovery-results.json'),('verify_workshop_recovery_states.py','workshop-recovery-state-results.json'),('verify_workshop_flow.py','workshop-flow-results.json'),('verify_workshop_states.py','workshop-state-results.json'),('verify_product_journey.py','product-journey-results.json')]
for script,name in jobs:
 run=subprocess.run([sys.executable,str(ROOT/script)]);p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));rows=v['results']if isinstance(v,dict)else v
 if isinstance(v,dict):assert v['files']==files
 assert files==source();reports[name]=dict(exit_code=run.returncode,cases=len(rows),passed=sum(r['passed']for r in rows),errors=sum(len(r['errors'])for r in rows),sha256=hashlib.sha256(p.read_bytes()).hexdigest());print('REPORT '+name+' '+str(reports[name]['passed'])+'/'+str(len(rows)),flush=True)
(OUT/'work-error-regression-source.json').write_text(json.dumps(dict(files=files,reports=reports),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(v['exit_code']==0 and v['cases']==v['passed']and not v['errors']for v in reports.values())else 1)
