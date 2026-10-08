"""Current record/moment consumers and shared-flow regressions."""
import sys,json,subprocess,hashlib,shutil
from verify_pet_controls import ROOT,source
OUT=ROOT/'evidence/current';files=source();group=sys.argv[1];reports={}
groups={
 'records':[('verify_record_controls.py','record-controls-results.json'),('verify_record_controls.py --layout','record-reply-layout-results.json'),('verify_record_back_reentry.py','record-back-reentry-results.json')],
 'moments':[('verify_moment_controls.py','moment-controls-results.json'),('verify_moment_controls.py --layout','moment-reply-layout-results.json'),('verify_moment_flow.py','moment-flow-results.json'),('verify_moment_states.py','moment-state-results.json')],
 'shared':[('verify_derived_shared_content.py','derived-shared-results.json'),('verify_backup_scope.py','backup-scope-results.json'),('verify_product_journey.py','product-journey-results.json'),('verify_time_product_journey.py','time-product-journey-results.json')]
}
history=ROOT/'evidence/history/pre-shared-display-55677e2';history.mkdir(parents=True,exist_ok=True)
for _,name in groups[group]:
 p=OUT/name
 if p.exists()and not(history/name).exists():shutil.copy2(p,history/name)
if group=='shared':
 for name in ['derived-shared-checkpoint.json','current-runtime-summary.json','current-runtime-inventory.json']:
  if not(history/name).exists():shutil.copy2(OUT/name,history/name)
meta_path=OUT/('shared-display-'+group+'-source.json');prior=json.loads(meta_path.read_text(encoding='utf-8'))if '--resume'in sys.argv and meta_path.exists()else{}
for script,name in groups[group]:
 p=OUT/name;old=prior.get('reports',{}).get(name,{})
 if prior.get('files')==files and old.get('exit_code')==0 and old.get('cases')==old.get('passed')and not old.get('errors')and old.get('sha256')==hashlib.sha256(p.read_bytes()).hexdigest():
  v=json.loads(p.read_text(encoding='utf-8'));rows=v['results']if isinstance(v,dict)else v;assert len(rows)==old['cases']and all(r['passed']and not r['errors']for r in rows);assert not isinstance(v,dict)or v['files']==files;reports[name]={**old,'retained_execution':True};print('RETAINED '+name,flush=True);continue
 args=script.split();run=subprocess.run([sys.executable,str(ROOT/args[0]),*args[1:]]);v=json.loads(p.read_text(encoding='utf-8'));rows=v['results']if isinstance(v,dict)else v
 if isinstance(v,dict):assert v['files']==files,name
 assert source()==files;reports[name]=dict(exit_code=run.returncode,cases=len(rows),passed=sum(r['passed']for r in rows),errors=sum(len(r['errors'])for r in rows),sha256=hashlib.sha256(p.read_bytes()).hexdigest());print('REPORT '+name+' '+str(reports[name]['passed'])+'/'+str(len(rows)),flush=True)
assert source()==files;meta_path.write_text(json.dumps(dict(files=files,reports=reports),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if all(v['exit_code']==0 and v['cases']==v['passed']and not v['errors']for v in reports.values())else 1)
