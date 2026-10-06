"""Current source regressions for changed workshop history and book resolver."""
import json,hashlib,shutil,subprocess,sys
from verify_pet_controls import ROOT,source
OUT=ROOT/'evidence/current';HISTORY=ROOT/'evidence/history/pre-product-journey-47b629d';files=source();reports={}
for prefix in ['workshop-flow','workshop-state','workshop-free','workshop-shared','workshop-film','book-global']:
 for p in OUT.glob(prefix+'*'):
  if not (HISTORY/p.name).exists():shutil.copy2(p,HISTORY/p.name)
for script,name in [('verify_workshop_flow.py','workshop-flow-results.json'),('verify_workshop_states.py','workshop-state-results.json'),('verify_book_global.py','book-global-results.json'),('verify_workshop_task_return.py','workshop-task-return-results.json'),('verify_book_created_date.py','book-created-date-results.json'),('verify_home_counter.py','home-counter-results.json')]:
 run=subprocess.run([sys.executable,str(ROOT/script)]);p=OUT/name;data=json.loads(p.read_text(encoding='utf-8'));rows=data['results'] if isinstance(data,dict) else data;assert files==source();reports[name]=dict(exit_code=run.returncode,cases=len(rows),passed=sum(v['passed']for v in rows),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
assert files==source();(OUT/'product-journey-regression-source.json').write_text(json.dumps(dict(files=files,reports=reports),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(v['exit_code']==0 and v['cases']==v['passed']for v in reports.values())else 1)
