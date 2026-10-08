import json,sys,subprocess,hashlib,shutil
from verify_pet_controls import ROOT,source
OUT=ROOT/'evidence/current';files=source();reports={};group=sys.argv[1]
groups={
 'business':[('verify_time_controls.py --controls','time-controls-results.json'),('verify_time_controls.py','time-collection-results.json'),('verify_time_layout.py','time-layout-results.json'),('verify_capsule_flow.py','capsule-flow-results.json'),('verify_capsule_states.py','capsule-state-results.json'),('verify_anniversary_flow.py','anniversary-flow-results.json'),('verify_anniversary_states.py','anniversary-state-results.json'),('verify_moment_flow.py','moment-flow-results.json'),('verify_moment_states.py','moment-state-results.json'),('verify_anniversary_date_recovery.py','anniversary-date-recovery-results.json')],
 'shared':[('verify_pet_book_recovery.py','pet-book-recovery-results.json'),('verify_pet_book_recovery_states.py','pet-book-recovery-state-results.json'),('verify_time_collection_recovery.py','time-collection-recovery-results.json'),('verify_time_collection_states.py','time-collection-state-results.json'),('verify_backup_preservation.py','backup-preservation-results.json'),('verify_backup_states.py','backup-state-results.json'),('verify_backup_scope.py','backup-scope-results.json'),('verify_recovery_archives.py','recovery-archive-results.json'),('verify_book_global.py','book-global-results.json'),('verify_product_journey.py','product-journey-results.json'),('verify_time_product_journey.py','time-product-journey-results.json')]
}
history=ROOT/'evidence/history/pre-capsule-semantics-13d559c';history.mkdir(parents=True,exist_ok=True)
for _,name in groups[group]:
 p=OUT/name
 if p.exists()and not(history/name).exists():shutil.copy2(p,history/name)
if group=='shared':
 for name in ['pet-book-recovery-checkpoint.json','current-runtime-summary.json','current-runtime-inventory.json']:
  if not(history/name).exists():shutil.copy2(OUT/name,history/name)
for script,name in groups[group]:
 args=script.split();args[0]=str(ROOT/args[0]);p=OUT/name;previous=json.loads(p.read_text(encoding='utf-8'))if p.exists()else None
 retained='--resume'in sys.argv and isinstance(previous,dict)and previous.get('files')==files and previous.get('results')and all(r['passed']and not r['errors']for r in previous['results'])
 run=None if retained else subprocess.run([sys.executable,*args]);v=json.loads(p.read_text(encoding='utf-8'));rows=v['results']if isinstance(v,dict)else v
 if isinstance(v,dict):assert v['files']==files,name
 assert source()==files;reports[name]=dict(exit_code=None if retained else run.returncode,revalidated_bound_report=bool(retained),cases=len(rows),passed=sum(r['passed']for r in rows),errors=sum(len(r['errors'])for r in rows),sha256=hashlib.sha256(p.read_bytes()).hexdigest());print('REPORT '+name+' '+str(reports[name]['passed'])+'/'+str(len(rows)),flush=True)
(OUT/('capsule-semantic-'+group+'-source.json')).write_text(json.dumps(dict(files=files,reports=reports),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all((v['exit_code']==0 or v['revalidated_bound_report'])and v['cases']==v['passed']and not v['errors']for v in reports.values())else 1)
