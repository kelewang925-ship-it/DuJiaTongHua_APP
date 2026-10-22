"""Bind this bounded cancellation fix to actual red/green results and current source bytes."""
import hashlib,json,argparse
from pathlib import Path
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,BASE,source

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--baseline-session',required=True);parser.add_argument('--cancel-session',required=True);parser.add_argument('--regression-session',required=True);args=parser.parse_args()
 h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8'));out=ROOT/'evidence/current';target=out/'pending-form-cancel';files=source();styles={p.relative_to(DEMO).as_posix():h(p) for p in (DEMO/'assets').glob('*.css')}
 redpath=ROOT/'evidence/baseline/pending-form-cancel/results.json';red=read(redpath);cancel=read(target/'results.json');contract=read(target/'contract-results.json');saves=read(out/'overlay-form-save-results.json')
 assert h(redpath.parent/'prototype-ui.js')==red['files']['assets/prototype-ui.js']
 assert len(red['results'])==4 and all(not r['passed'] and r['storage_unchanged_before_decision'] is False and r['storage_unchanged_after_discard'] is False for r in red['results'])
 assert len(cancel['results'])==96 and all(r['passed'] and not r['errors'] and r['storage_unchanged_before_decision'] for r in cancel['results'])
 assert len(contract['results'])==8 and all(r['passed'] and not r['errors'] for r in contract['results'])
 assert len(saves['results'])==47 and all(r['passed'] and not r['errors'] for r in saves['results'])
 assert red['script_sha256']==cancel['script_sha256']==h(ROOT/'verify_pending_form_cancel.py')
 for report,script in [(cancel,'verify_pending_form_cancel.py'),(contract,'verify_pending_form_contract.py'),(saves,'verify_overlay_form_saves.py')]:assert report['files']==files and report['script_sha256']==h(ROOT/script)
 assert cancel['styles']==contract['styles']==styles
 assert {k for k in files if files[k]!=red['files'][k]}=={'assets/prototype-ui.js'}
 from verify_overlay_form_saves import SPECS
 assert {(r['index'],r['method']) for r in cancel['results']}=={(i,m) for i in SPECS for m in ['button','escape','back','backdrop','drag','keep']}
 for r in cancel['results']:
  if r['method']=='keep':assert r['retry_persisted']
  else:assert r['storage_unchanged_after_discard'] and r['reload_consistent']
 for path,digest in {**files,**styles}.items():
  with urlopen(BASE+path.replace('custom/','pages/',1),timeout=10) as response:assert response.headers.get('Cache-Control')=='no-store' and hashlib.sha256(response.read()).hexdigest()==digest
 pages=list((DEMO/'custom').glob('*.html'));assert len(pages)==114
 for p in pages:assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
 reports={p.relative_to(ROOT).as_posix():h(p) for p in [redpath,target/'results.json',target/'contract-results.json',out/'overlay-form-save-results.json']}
 scripts={name:h(ROOT/name) for name in ['verify_pending_form_cancel.py','verify_pending_form_contract.py','verify_pending_form_checkpoint.py','verify_overlay_form_saves.py','verify_overlay_exit_paths.py','audit_hidden_overlays.py','audit_current_runtime.py','book_test_helpers.py']+['verify_'+v+'_controls.py' for v in ['onboarding','record','moment','time','workshop','settings','pet','book']]}
 checkpoint=dict(files=files,styles=styles,reports_sha256=reports,scripts_sha256=scripts,executions=dict(baseline=dict(session=args.baseline_session,exit_code=1),cancel=dict(session=args.cancel_session,exit_code=0),sequential_contract_then_saves=dict(session=args.regression_session,exit_code=0)),actual_form_cancel_cases=96,shared_contract_cases=8,form_save_cases=47,accepted_pages=0,scope='16 observed actual forms across six pending-close paths; 8 synthetic helper boundary contracts; 47 actual normal/invalid/quota-retry checks. Top-level guards, all other pending operations, concurrency and final journeys remain unaccepted.')
 (target/'checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 statepath=out/'current-evidence-state.json';state=read(statepath)
 history=ROOT/'evidence/history/pre-pending-cancel-b6a3257';history.mkdir(parents=True,exist_ok=True)
 if state['files']!=files:
  (history/'current-evidence-state.json').write_bytes(statepath.read_bytes())
  for name,count in list(state.items()):
   if name.startswith('current_') and isinstance(count,int) and not isinstance(count,bool) and count>0:state['historical_'+name.removeprefix('current_')]=count;state[name]=0
 state.update(files=files,style_dependencies=styles,current_pending_form_cancel_cases=96,current_pending_form_contract_cases=8,current_overlay_form_save_cases=47,current_pending_form_checkpoint='evidence/current/pending-form-cancel/checkpoint.json',previous_behavior_source_manifest='evidence/history/pre-pending-cancel-b6a3257/current-evidence-state.json',runtime_requires_refresh=True,catalog_requires_refresh=True,flow_replay_requires_refresh=True,pending_form_cancel_issue='fixed_for_16_observed_forms',accepted_pages=0,reason=checkpoint['scope'])
 state.pop('initial_quality_current_checkpoint',None)
 statepath.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(actual_cancel=96,shared_contract=8,form_save=47,mirrors=114,accepted_pages=0)))

if __name__=='__main__':main()
