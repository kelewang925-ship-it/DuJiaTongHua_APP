"""Current evidence for pending image-only navigation and explicit discard cleanup."""
import hashlib,json
from pathlib import Path
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,BASE,source

def main():
 h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8'));out=ROOT/'evidence/current';dest=out/'image-pending-exit';base=ROOT/'evidence/baseline/image-pending-exit';files=source();styles={p.relative_to(DEMO).as_posix():h(p) for p in (DEMO/'assets').glob('*.css')}
 red=read(base/'results.json');assert len(red['results'])==6 and all(not r['passed'] and not r['errors'] and not r.get('pending_image_only_protected') for r in red['results']);assert red['script_sha256']==h(base/'verifier.py') and red['styles']==styles
 changed={'assets/prototype-'+n+'.js' for n in ['ui','diary','photo','moment','capsule','settings','book-editors']};assert {k for k in files if files[k]!=red['files'][k]}==changed
 for name in changed:assert h(base/'source'/Path(name).name)==red['files'][name]
 definitions=[(dest/'results.json',36,'verify_image_pending_exit.py'),(out/'image-read-order/results.json',30,'verify_image_read_order.py'),(out/'pending-image-read/results.json',16,'verify_pending_image_reads.py'),(out/'pending-page-guard/contract-results.json',12,'verify_pending_guard_contract.py'),(out/'submission-changes/results.json',2,'verify_submission_changes.py')]
 for path,count,script in definitions:
  r=read(path);assert r['files']==files and r['styles']==styles and r['script_sha256']==h(ROOT/script) and len(r['results'])==count and all(v['passed'] and not v['errors'] for v in r['results'])
 names=['diary-publish','photo-top','moment','capsule-draft','profile','book-supplement'];r=read(dest/'results.json');assert {(v['case'],v['method'],v['mode']) for v in r['results']}=={(n,m,k) for n in names for m in ['button','browser'] for k in ['keep-success','keep-failure','discard-held']}
 for v in r['results']:
  assert v['pending_image_only_protected'] and not v['native_dialogs']
  assert v.get('late_result_ignored') if v['mode']=='discard-held' else v.get('continued_and_saved') if v['mode']=='keep-success' else v.get('failure_restores_clean_state')
 defaults=read(definitions[-1][0]);assert {(v['kind'],v['case'],v['mode']) for v in defaults['results']}=={('concurrent',n,'cancel') for n in ['draft','generate']}
 probes=[]
 for folder,count,passed in [('image-pending-exit-network-probe',2,2),('image-pending-exit-ready-probe',36,30)]:
  p=ROOT/('evidence/history/'+folder);v=read(p/'results.json');assert v['files']==files and v['script_sha256']==h(p/'verifier.py') and len(v['results'])==count and sum(r['passed'] for r in v['results'])==passed;probes.append(p/'results.json')
 assert read(probes[0].parent/'execution.json')['interrupted'] is True
 assert all(v['case']=='book-supplement' and '__imageJobs.length' in v['failure'] for v in read(probes[1])['results'] if not v['passed'])
 for path,digest in {**files,**styles}.items():
  with urlopen(BASE+path.replace('custom/','pages/',1),timeout=10) as response:assert response.headers.get('Cache-Control')=='no-store' and hashlib.sha256(response.read()).hexdigest()==digest
 pages=list((DEMO/'custom').glob('*.html'));assert len(pages)==114
 for p in pages:assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
 paths=[v[0] for v in definitions]+[base/'results.json']+probes;scripts=[v[2] for v in definitions]+['verify_image_exit_checkpoint.py','audit_hidden_overlays.py','verify_overlay_form_saves.py','verify_pending_page_guard.py','audit_current_runtime.py','book_test_helpers.py']+['verify_'+v+'_controls.py' for v in ['onboarding','record','moment','time','workshop','settings','pet','book']]
 cp=dict(files=files,styles=styles,reports_sha256={p.relative_to(ROOT).as_posix():h(p) for p in paths},scripts_sha256={n:h(ROOT/n) for n in scripts},executions=dict(red=dict(session='42204',exit_code=1),network_fixture=dict(session='69411',exit_code=1,interrupted=True),ready_fixture=dict(session='36260',exit_code=1),full_exit_and_image_and_shared=dict(session='67869',exit_code=0),default_discard=dict(chunk='56dd63',exit_code=0)),pending_image_exit_cases=36,image_order_cases=30,pending_save_cases=16,shared_contract_cases=12,default_discard_cases=2,total_checks=96,accepted_pages=0,scope='Six manual editors: real top/browser history from same-origin source; pending image only, continued decode success/failure, explicit discard cleanup before deferred native history.go.46 image outcomes plus12 synthetic guard and2 default-discard cases. Originless fallback image combinations, native chooser-before-selection, post-start edits, world-avatar permissions and full final matrices remain unaccepted.')
 (dest/'checkpoint.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 statepath=out/'current-evidence-state.json';state=read(statepath);history=ROOT/'evidence/history/pre-image-pending-exit-98abd0d';history.mkdir(parents=True,exist_ok=True)
 if state['files']!=files:
  (history/'current-evidence-state.json').write_bytes(statepath.read_bytes())
  for name,count in list(state.items()):
   if name.startswith('current_') and isinstance(count,int) and not isinstance(count,bool) and count>0:state['historical_'+name.removeprefix('current_')]=count;state[name]=0
 state.update(files=files,style_dependencies=styles,current_image_pending_exit_cases=36,current_image_order_cases=30,current_pending_image_cases=16,current_pending_page_contract_cases=12,current_default_discard_cases=2,current_image_read_checkpoint='evidence/current/image-pending-exit/checkpoint.json',previous_behavior_source_manifest='evidence/history/pre-image-pending-exit-98abd0d/current-evidence-state.json',runtime_requires_refresh=True,catalog_requires_refresh=True,flow_replay_requires_refresh=True,image_only_pending_exit_issue='fixed_for_six_manual_editors',accepted_pages=0,reason=cp['scope'])
 statepath.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(exit=36,image=46,shared=12,default_discard=2,total=96,mirrors=114,accepted_pages=0)))

if __name__=='__main__':main()
