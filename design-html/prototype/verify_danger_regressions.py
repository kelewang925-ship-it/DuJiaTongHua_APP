"""Scoped business regressions after shared destructive-component adoption."""
import json,subprocess,sys,hashlib
from verify_pet_controls import ROOT,source
OUT=ROOT/'evidence/current';files=source();reports={}
jobs=[('verify_danger_confirmations.py','danger-confirmation-results.json'),('verify_settings_flow.py','settings-flow-results.json'),('verify_settings_states.py','settings-state-results.json'),('verify_pet_life_states.py','pet-life-state-results.json'),('verify_book_structure.py','book-structure-results.json'),('verify_record_recovery.py','record-recovery-results.json'),('verify_account_recovery.py','account-recovery-results.json')]
for script,name in jobs:
 run=subprocess.run([sys.executable,str(ROOT/script)]);p=OUT/name
 if not p.exists():raise AssertionError('Missing report '+name)
 v=json.loads(p.read_text(encoding='utf-8'));rows=v['results']if isinstance(v,dict)else v
 if isinstance(v,dict)and 'files'in v:assert v['files']==files
 assert files==source();reports[name]=dict(exit_code=run.returncode,cases=len(rows),passed=sum(r['passed']for r in rows),errors=sum(len(r['errors'])for r in rows),sha256=hashlib.sha256(p.read_bytes()).hexdigest());print('REPORT '+name+' '+str(reports[name]),flush=True)
(OUT/'danger-regression-source.json').write_text(json.dumps(dict(files=files,reports=reports),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(v['exit_code']==0 and v['cases']==v['passed']and not v['errors']for v in reports.values())else 1)
