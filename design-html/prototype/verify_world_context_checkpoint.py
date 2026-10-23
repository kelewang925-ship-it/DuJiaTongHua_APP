"""Bind common-profile context fixes and affected compatibility replays to current bytes."""
import hashlib,json
from pathlib import Path
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,BASE,source
from verify_world_write_context import AVATAR,NICK,UNLINK

def main():
 h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8'));out=ROOT/'evidence/current';dest=out/'world-write-context';files=source();styles={p.relative_to(DEMO).as_posix():h(p) for p in (DEMO/'assets').glob('*.css')}
 redpath=ROOT/'evidence/baseline/world-write-context/results.json';red=read(redpath)
 assert len(red['results'])==31 and sum(r['passed'] for r in red['results'])==7 and all(not r['errors'] for r in red['results'])
 assert red['script_sha256']==h(ROOT/'verify_world_write_context.py') and red['styles']==styles
 assert h(redpath.parent/'prototype-settings.js')==red['files']['assets/prototype-settings.js']
 assert {k for k in files if files[k]!=red['files'][k]}=={'assets/prototype-settings.js'}
 definitions=[(dest/'results.json',31,'verify_world_write_context.py'),(out/'world-existing-flow/results.json',4,'verify_world_existing_flow.py'),(out/'image-read-order/results.json',30,'verify_image_read_order.py'),(out/'settings-controls-results.json',81,'verify_settings_controls.py')]
 for path,count,script in definitions:
  v=read(path);assert v['files']==files and len(v['results'])==count and all(r['passed'] and not r['errors'] for r in v['results'])
  if 'script_sha256' in v:assert v['script_sha256']==h(ROOT/script) and v['styles']==styles
 assert {(r['kind'],r['mode']) for r in read(dest/'results.json')['results']}=={('avatar',m) for m in AVATAR}|{('nickname',m) for m in NICK}|{('unlink',m) for m in UNLINK}|{('status','unbound')}
 assert {r['case'] for r in read(out/'world-existing-flow/results.json')['results']}=={'peer-accept','peer-reject-retry','logged-out-demo','nickname-quota-retry'}
 for path,digest in {**files,**styles}.items():
  with urlopen(BASE+path.replace('custom/','pages/',1),timeout=10) as response:assert response.headers.get('Cache-Control')=='no-store' and hashlib.sha256(response.read()).hexdigest()==digest
 pages=list((DEMO/'custom').glob('*.html'));assert len(pages)==114
 for p in pages:assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
 scripts=[v[2] for v in definitions]+['verify_world_context_checkpoint.py','verify_pet_controls.py','verify_pending_image_reads.py','verify_submission_changes.py','verify_pending_page_guard.py','verify_overlay_form_saves.py','audit_hidden_overlays.py','audit_current_runtime.py','audit_runtime.py','book_test_helpers.py']
 probe=ROOT/'evidence/history/world-existing-flow-first-probe';v=read(probe/'results.json');assert v['files']==files and len(v['results'])==4 and sum(r['passed'] for r in v['results'])==1 and v['script_sha256']==h(probe/'verify_world_existing_flow.py');assert read(probe/'execution.json')['exit_code']==1
 reports=[v[0] for v in definitions]+[redpath,probe/'results.json',probe/'execution.json'];scope='31 real common-profile context cases;4 peer/retry/direct-demo chains;81 existing settings controls;30 native image-order checks. Snapshot consistency in local mock storage, not real authorization or cross-tab atomic locking. Full final runtime/catalog/layout/flow replay and remaining state audit still pending.'
 cp=dict(files=files,styles=styles,reports_sha256={p.relative_to(ROOT).as_posix():h(p) for p in reports},scripts_sha256={n:h(ROOT/n) for n in scripts},executions=dict(context=dict(session='61539',exit_code=0),settings_and_images=dict(session='54930',exit_code=0),compatibility=dict(session='86071',exit_code=0),compatibility_first_probe=dict(session='45015',exit_code=1),baseline=dict(rows=31,passed=7,failed=24,terminal_capture_available=False)),context_cases=31,compatibility_cases=4,settings_control_cases=81,image_order_cases=30,total_checks=146,accepted_pages=0,scope=scope)
 (dest/'checkpoint.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 statepath=out/'current-evidence-state.json';state=read(statepath);history=ROOT/'evidence/history/pre-world-context-7b04d9a';history.mkdir(parents=True,exist_ok=True)
 if state['files']!=files:
  assert state['files']==red['files'];(history/'current-evidence-state.json').write_bytes(statepath.read_bytes())
  for name,count in list(state.items()):
   if name.startswith('current_') and isinstance(count,int) and not isinstance(count,bool) and count>0:state['historical_'+name.removeprefix('current_')]=count;state[name]=0
 state.update(files=files,style_dependencies=styles,current_world_context_cases=31,current_world_compatibility_cases=4,current_settings_control_cases=81,current_image_order_cases=30,current_world_context_checkpoint='evidence/current/world-write-context/checkpoint.json',current_image_read_checkpoint='evidence/current/world-write-context/checkpoint.json',previous_behavior_source_manifest='evidence/history/pre-world-context-7b04d9a/current-evidence-state.json',runtime_requires_refresh=True,catalog_requires_refresh=True,flow_replay_requires_refresh=True,world_profile_context_issue='fixed_for_31_observed_context_cases_and_four_compatibility_chains',accepted_pages=0,reason=scope)
 statepath.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(context=31,compatibility=4,settings=81,image_order=30,total=146,mirrors=114,accepted_pages=0)))

if __name__=='__main__':main()
