"""Declared regressions bound to source and actual subprocess outcomes."""
import json,sys,subprocess,hashlib,shutil
from verify_pet_controls import ROOT,source
OUT=ROOT/'evidence/current';files=source();reports={}
groups=[('verify_settings_controls.py','settings-controls-results.json'),('verify_settings_states.py','settings-state-results.json'),('verify_settings_flow.py','settings-flow-results.json'),('verify_book_global.py','book-global-results.json'),('verify_pet_states.py','pet-state-results.json'),('verify_recovery_archives.py','recovery-archive-results.json'),('verify_account_recovery.py','account-recovery-results.json'),('verify_record_recovery.py','record-recovery-results.json')]
history=ROOT/'evidence/history/pre-backup-preservation-87ff86d';history.mkdir(parents=True,exist_ok=True)
for _,name in groups:
 p=OUT/name
 if p.exists()and not(history/name).exists():shutil.copy2(p,history/name)
for name in ['time-recovery-checkpoint.json','current-runtime-summary.json','current-runtime-inventory.json','backup-damaged-time-observations.json']:
 if not(history/name).exists():shutil.copy2(OUT/name,history/name)
for script,name in groups:
 run=subprocess.run([sys.executable,str(ROOT/script)]);p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));rows=v['results']if isinstance(v,dict)else v
 if isinstance(v,dict):assert v['files']==files
 assert source()==files;reports[name]=dict(exit_code=run.returncode,cases=len(rows),passed=sum(r['passed']for r in rows),errors=sum(len(r['errors'])for r in rows),sha256=hashlib.sha256(p.read_bytes()).hexdigest());print('REPORT '+name+' '+str(reports[name]['passed'])+'/'+str(len(rows)),flush=True)
(OUT/'backup-regression-source.json').write_text(json.dumps(dict(files=files,reports=reports),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(v['exit_code']==0 and v['cases']==v['passed']and not v['errors']for v in reports.values())else 1)
