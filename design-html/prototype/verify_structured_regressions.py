import json,subprocess,sys,hashlib,shutil
from verify_pet_controls import ROOT,source
OUT=ROOT/'evidence/current';files=source();reports={};group=sys.argv[1]
groups={
 'pet':[('verify_pet_controls.py','pet-controls-results.json'),('verify_pet_control_hidden.py','pet-control-hidden-results.json'),('verify_pet_control_layout.py','pet-control-layout-results.json'),('verify_pet_flow.py','pet-flow-results.json'),('verify_pet_states.py','pet-state-results.json'),('verify_pet_life_flow.py','pet-life-flow-results.json'),('verify_pet_life_states.py','pet-life-state-results.json')],
 'books':[('verify_book_controls.py','book-controls-results.json'),('verify_book_control_return.py','book-control-return-results.json'),('verify_book_control_layout.py','book-control-layout-results.json'),('verify_book_flow.py','book-flow-results.json'),('verify_book_states.py','book-state-results.json'),('verify_book_extended.py','book-extended-results.json'),('verify_book_structure.py','book-structure-results.json'),('verify_book_cover.py','book-cover-results.json'),('verify_book_global.py','book-global-results.json'),('verify_book_editor_draft.py','book-editor-draft-results.json')],
 'shared':[('verify_backup_preservation.py','backup-preservation-results.json'),('verify_backup_states.py','backup-state-results.json'),('verify_backup_scope.py','backup-scope-results.json'),('verify_time_collection_recovery.py','time-collection-recovery-results.json'),('verify_time_collection_states.py','time-collection-state-results.json'),('verify_recovery_archives.py','recovery-archive-results.json'),('verify_product_journey.py','product-journey-results.json'),('verify_time_product_journey.py','time-product-journey-results.json')]
}
history=ROOT/'evidence/history/pre-pet-book-recovery-86362d5';history.mkdir(parents=True,exist_ok=True)
for _,name in groups[group]:
 p=OUT/name
 if p.exists()and not(history/name).exists():shutil.copy2(p,history/name)
if group=='shared':
 for name in ['backup-preservation-checkpoint.json','current-runtime-summary.json','current-runtime-inventory.json']:
  if not(history/name).exists():shutil.copy2(OUT/name,history/name)
for script,name in groups[group]:
 run=subprocess.run([sys.executable,str(ROOT/script)]);p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));rows=v['results']if isinstance(v,dict)else v
 if isinstance(v,dict):assert v['files']==files,name
 assert source()==files;reports[name]=dict(exit_code=run.returncode,cases=len(rows),passed=sum(r['passed']for r in rows),errors=sum(len(r['errors'])for r in rows),sha256=hashlib.sha256(p.read_bytes()).hexdigest());print('REPORT '+name+' '+str(reports[name]['passed'])+'/'+str(len(rows)),flush=True)
(OUT/('structured-'+group+'-source.json')).write_text(json.dumps(dict(files=files,reports=reports),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(v['exit_code']==0 and v['cases']==v['passed']and not v['errors']for v in reports.values())else 1)
