"""Time-task and shared-guard regressions, source-bound with preserved prior reports."""
import json,hashlib,subprocess,sys,shutil
from verify_pet_controls import ROOT,source
OUT=ROOT/'evidence/current';H=ROOT/'evidence/history/pre-time-journey-12cf15c';H.mkdir(parents=True,exist_ok=True);files=source();reports={}
for prefix in ['current-runtime','product-journey','workshop-flow','workshop-state','workshop-task-return','book-created-date','home-counter','time-','anniversary','capsule','settings-sheet-guard']:
 for p in OUT.glob(prefix+'*'):
  target=H/p.name
  if not target.exists():
   if p.is_dir():shutil.copytree(p,target)
   else:shutil.copy2(p,target)
for name in ['CURRENT_PAGES.md','CURRENT_CONTROL_AUDIT.md']:
 if not(H/name).exists():shutil.copy2(ROOT/name,H/name)
jobs=[('verify_anniversary_flow.py',[],'anniversary-flow-results.json'),('verify_anniversary_states.py',[],'anniversary-state-results.json'),('verify_capsule_flow.py',[],'capsule-flow-results.json'),('verify_capsule_states.py',[],'capsule-state-results.json'),('verify_time_controls.py',[],'time-collection-results.json'),('verify_settings_sheet_guard.py',[],'settings-sheet-guard-results.json'),('verify_time_controls.py',['--controls'],'time-controls-results.json'),('verify_time_layout.py',[],'time-layout-results.json'),('verify_time_entry_layout.py',[],'time-entry-layout-results.json'),('verify_time_task_return.py',[],'time-task-return-results.json')]
for script,args,name in jobs:
 run=subprocess.run([sys.executable,str(ROOT/script),*args]);p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));rows=v['results']if isinstance(v,dict)else v;assert files==source();reports[name]=dict(exit_code=run.returncode,cases=len(rows),passed=sum(r['passed']for r in rows),sha256=hashlib.sha256(p.read_bytes()).hexdigest());print('REPORT '+name+' '+str(reports[name]['passed'])+'/'+str(len(rows)),flush=True)
assert files==source();(OUT/'time-journey-regression-source.json').write_text(json.dumps(dict(files=files,reports=reports),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(v['exit_code']==0 and v['cases']==v['passed']for v in reports.values())else 1)
