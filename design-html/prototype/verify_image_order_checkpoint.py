"""Latest image request wins, removal and valid-image retention: actual native I/O outcomes."""
import hashlib,json
from pathlib import Path
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,BASE,source

def main():
 h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8'));out=ROOT/'evidence/current';folder=out/'image-read-order';baseline=ROOT/'evidence/baseline/image-read-order';files=source();styles={p.relative_to(DEMO).as_posix():h(p) for p in (DEMO/'assets').glob('*.css')}
 reds=[(baseline/'first-results.json',16,'verifier-first.py'),(baseline/'loading-results.json',7,'verifier-loading.py'),(baseline/'results.json',1,'verifier-retain.py')]
 for path,count,script in reds:
  r=read(path);assert len(r['results'])==count and all(not v['passed'] for v in r['results']) and r['script_sha256']==h(baseline/script) and r['styles']==styles
 assert read(reds[0][0])['files']==read(reds[1][0])['files']
 changed={k for k in files if read(reds[0][0])['files'][k]!=files[k]};expected={'assets/prototype-'+n+'.js' for n in ['records','diary','photo','moment','capsule','settings','book-editors']};assert changed==expected
 retain=read(baseline/'results.json');assert {k for k in files if retain['files'][k]!=files[k]}=={'assets/prototype-book-editors.js'};assert h(baseline/'book-editors-before-retain.js')==retain['files']['assets/prototype-book-editors.js']
 prior=ROOT/'evidence/history/image-order-before-retain-fix';v=read(prior/'results.json');assert len(v['results'])==23 and all(r['passed'] for r in v['results']) and v['files']==retain['files'] and v['script_sha256']==h(prior/'verifier.py')
 definitions=[(folder/'results.json',30,'verify_image_read_order.py'),(out/'pending-image-read/results.json',16,'verify_pending_image_reads.py')]
 for path,count,script in definitions:
  r=read(path);assert r['files']==files and r['styles']==styles and len(r['results'])==count and all(v['passed'] and not v['errors'] and v.get('persisted_and_reload_consistent',v.get('explicit_retry_and_reload_consistent')) for v in r['results']) and r['script_sha256']==h(ROOT/script)
 names=['diary-publish','photo-top','moment','capsule-draft','profile','book-supplement','world-avatar'];r=read(folder/'results.json');assert {(v['case'],v['mode']) for v in r['results']}=={(n,m) for n in names for m in ['old-success','old-error','older-first','latest-error']}|{(n,'remove') for n in ['diary-publish','capsule-draft']}
 for v in r['results']:
  if v['mode'] in ['old-success','old-error']:assert v['latest_still_shown']
  elif v['mode']=='older-first':assert v['latest_read_kept_pending']
  elif v['mode']=='latest-error':assert v['previous_valid_image_retained']
 for path,digest in {**files,**styles}.items():
  with urlopen(BASE+path.replace('custom/','pages/',1),timeout=10) as response:assert response.headers.get('Cache-Control')=='no-store' and hashlib.sha256(response.read()).hexdigest()==digest
 pages=list((DEMO/'custom').glob('*.html'));assert len(pages)==114
 for p in pages:assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
 reports={p.relative_to(ROOT).as_posix():h(p) for p in [v[0] for v in definitions]+[v[0] for v in reds]+[prior/'results.json']};scripts=[v[2] for v in definitions]+['verify_image_order_checkpoint.py','verify_pending_image_checkpoint.py','verify_pending_page_guard.py','verify_submission_changes.py','verify_overlay_form_saves.py','audit_hidden_overlays.py','audit_current_runtime.py','book_test_helpers.py']+['verify_'+v+'_controls.py' for v in ['onboarding','record','moment','time','workshop','settings','pet','book']]
 cp=dict(files=files,styles=styles,reports_sha256=reports,scripts_sha256={n:h(ROOT/n) for n in scripts},executions=dict(first_red=dict(session='75023',exit_code=1),pending_red=dict(chunk='f61e71',exit_code=1),first_helper=dict(session='74613',exit_code=0),retain_red=dict(chunk='b39838',exit_code=1),final_order_and_pending=dict(session='24848',exit_code=0)),image_order_cases=30,pending_image_cases=16,total_checks=46,accepted_pages=0,scope='Seven actual image inputs with latest/older success/error and pending flags; two explicit removals;16 actual pending-save native decode success/failure outcomes. Native FileReader and Image events observed, real persistence and reload. Other guards/permissions and image-only navigation remain incomplete.')
 (folder/'checkpoint.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 statepath=out/'current-evidence-state.json';state=read(statepath);history=ROOT/'evidence/history/pre-image-order-249b5b7';history.mkdir(parents=True,exist_ok=True)
 if state['files']!=files:
  (history/'current-evidence-state.json').write_bytes(statepath.read_bytes())
  for name,count in list(state.items()):
   if name.startswith('current_') and isinstance(count,int) and not isinstance(count,bool) and count>0:state['historical_'+name.removeprefix('current_')]=count;state[name]=0
 state.pop('current_submission_checkpoint',None)
 state.update(files=files,style_dependencies=styles,current_pending_image_cases=16,current_image_order_cases=30,current_image_read_checkpoint='evidence/current/image-read-order/checkpoint.json',previous_behavior_source_manifest='evidence/history/pre-image-order-249b5b7/current-evidence-state.json',runtime_requires_refresh=True,catalog_requires_refresh=True,flow_replay_requires_refresh=True,image_request_order_issue='fixed_for_seven_image_inputs',accepted_pages=0,reason=cp['scope'])
 statepath.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(order=30,pending=16,total=46,mirrors=114,accepted_pages=0)))

if __name__=='__main__':main()
