"""Execute inherited consumer groups and preserve their prior source evidence."""
import sys,json,subprocess,hashlib,shutil
from verify_pet_controls import ROOT,source
OUT=ROOT/'evidence/current';files=source();group=sys.argv[1]
history=ROOT/'evidence/history/pre-editor-current-e608d0b';history.mkdir(parents=True,exist_ok=True)
prior=OUT/('shared-display-'+group+'-source.json')
old=json.loads(prior.read_text(encoding='utf-8'))
for name in [*old['reports'],prior.name]:
 if not(history/name).exists():shutil.copy2(OUT/name,history/name)
if group=='shared':
 for name in ['shared-display-results.json','shared-display-checkpoint.json','current-runtime-inventory.json','current-runtime-summary.json']:
  if not(history/name).exists():shutil.copy2(OUT/name,history/name)
run=subprocess.run([sys.executable,str(ROOT/'verify_shared_display_regressions.py'),group,*sys.argv[2:]]);assert run.returncode==0
v=json.loads(prior.read_text(encoding='utf-8'));assert v['files']==files;reports=v['reports']
if group=='shared':
 run=subprocess.run([sys.executable,str(ROOT/'verify_shared_display_scope.py')]);p=OUT/'shared-display-results.json';value=json.loads(p.read_text(encoding='utf-8'));rows=value['results'];assert value['files']==files
 reports[p.name]=dict(exit_code=run.returncode,cases=len(rows),passed=sum(r['passed']for r in rows),errors=sum(len(r['errors'])for r in rows),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
assert source()==files;(OUT/('editor-current-'+group+'-source.json')).write_text(json.dumps(dict(files=files,reports=reports),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(r['exit_code']==0 and r['cases']==r['passed']and not r['errors']for r in reports.values())else 1)
