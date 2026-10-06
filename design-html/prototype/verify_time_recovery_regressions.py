"""Source-bound business and shared recovery runs for the three time collections."""
import json,subprocess,sys,hashlib
from verify_pet_controls import ROOT,source
OUT=ROOT/'evidence/current';files=source();reports={};group='shared'if '--shared'in sys.argv else'business'
groups={
 'business':[('verify_time_collection_recovery.py',[],'time-collection-recovery-results.json'),('verify_time_collection_states.py',[],'time-collection-state-results.json'),('verify_moment_controls.py',[],'moment-controls-results.json'),('verify_moment_controls.py',['--layout'],'moment-reply-layout-results.json'),('verify_moment_flow.py',[],'moment-flow-results.json'),('verify_moment_states.py',[],'moment-state-results.json'),('verify_time_controls.py',['--controls'],'time-controls-results.json'),('verify_time_controls.py',[],'time-collection-results.json'),('verify_time_layout.py',[],'time-layout-results.json'),('verify_anniversary_flow.py',[],'anniversary-flow-results.json'),('verify_anniversary_states.py',[],'anniversary-state-results.json'),('verify_capsule_flow.py',[],'capsule-flow-results.json'),('verify_capsule_states.py',[],'capsule-state-results.json'),('verify_time_product_journey.py',[],'time-product-journey-results.json'),('verify_product_journey.py',[],'product-journey-results.json')],
 'shared':[('verify_tag_recovery.py',[],'tag-recovery-results.json'),('verify_tag_recovery_states.py',[],'tag-recovery-state-results.json'),('verify_account_recovery.py',[],'account-recovery-results.json'),('verify_record_recovery.py',[],'record-recovery-results.json'),('verify_workshop_recovery.py',[],'workshop-recovery-results.json'),('verify_workshop_recovery_states.py',[],'workshop-recovery-state-results.json'),('verify_recovery_archives.py',[],'recovery-archive-results.json'),('verify_settings_sheet_guard.py',[],'settings-sheet-guard-results.json')]
}
for script,args,name in groups[group]:
 run=subprocess.run([sys.executable,str(ROOT/script),*args]);p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));rows=v['results']if isinstance(v,dict)else v
 if isinstance(v,dict):assert v['files']==files
 assert source()==files;reports[name]=dict(exit_code=run.returncode,cases=len(rows),passed=sum(r['passed']for r in rows),errors=sum(len(r['errors'])for r in rows),sha256=hashlib.sha256(p.read_bytes()).hexdigest());print('REPORT '+name+' '+str(reports[name]['passed'])+'/'+str(len(rows)),flush=True)
(OUT/('time-recovery-'+group+'-source.json')).write_text(json.dumps(dict(files=files,reports=reports),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(v['exit_code']==0 and v['cases']==v['passed']and not v['errors']for v in reports.values())else 1)
