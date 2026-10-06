"""Work collection recovery, existing business and shared guard regressions, same source."""
import json,subprocess,sys,hashlib
from verify_pet_controls import ROOT,source
OUT=ROOT/'evidence/current';files=source();reports={}
for script,name in [('verify_workshop_flow.py','workshop-flow-results.json'),('verify_workshop_states.py','workshop-state-results.json'),('verify_account_recovery.py','account-recovery-results.json'),('verify_record_recovery.py','record-recovery-results.json'),('verify_settings_sheet_guard.py','settings-sheet-guard-results.json'),('verify_danger_confirmations.py','danger-confirmation-results.json'),('verify_book_global.py','book-global-results.json'),('verify_product_journey.py','product-journey-results.json'),('verify_time_product_journey.py','time-product-journey-results.json')]:
 run=subprocess.run([sys.executable,str(ROOT/script)]);p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));rows=v['results']if isinstance(v,dict)else v
 if isinstance(v,dict)and 'files'in v:assert v['files']==files
 assert files==source();reports[name]=dict(exit_code=run.returncode,cases=len(rows),passed=sum(r['passed']for r in rows),errors=sum(len(r['errors'])for r in rows),sha256=hashlib.sha256(p.read_bytes()).hexdigest());print('REPORT '+name+' '+str(reports[name]['passed'])+'/'+str(len(rows)),flush=True)
(OUT/'workshop-recovery-regression-source.json').write_text(json.dumps(dict(files=files,reports=reports),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(v['exit_code']==0 and v['cases']==v['passed']and not v['errors']for v in reports.values())else 1)
