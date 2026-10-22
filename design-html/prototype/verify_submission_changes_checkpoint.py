"""Bind pending edit/picker/concurrent task outcomes and the existing guard/form regressions."""
import argparse,hashlib,json
from pathlib import Path
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,BASE,source

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--regression-session',required=True);args=parser.parse_args();h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8'));out=ROOT/'evidence/current';dest=out/'submission-changes';files=source();styles={p.relative_to(DEMO).as_posix():h(p) for p in (DEMO/'assets').glob('*.css')}
 redpath=ROOT/'evidence/baseline/submission-changes/results.json';red=read(redpath);assert len(red['results'])==4 and all(not r['passed'] for r in red['results']);assert all(r.get('unchanged_before_retry',r.get('unchanged_with_picker_open',r.get('unchanged_before_decision'))) is False for r in red['results']);assert red['styles']==styles and red['script_sha256']==h(ROOT/'verify_submission_changes.py');assert h(redpath.parent/'prototype-ui.js')==red['files']['assets/prototype-ui.js'];assert {k for k in files if red['files'][k]!=files[k]}=={'assets/prototype-ui.js'}
 definitions=[(dest/'results.json',19,'verify_submission_changes.py'),(out/'pending-page-guard/results.json',52,'verify_pending_page_guard.py'),(out/'pending-page-guard/contract-results.json',12,'verify_pending_guard_contract.py'),(out/'pending-form-cancel/results.json',96,'verify_pending_form_cancel.py'),(out/'pending-form-cancel/contract-results.json',8,'verify_pending_form_contract.py'),(out/'overlay-form-save-results.json',47,'verify_overlay_form_saves.py')]
 for path,count,script in definitions:
  v=read(path);assert v['files']==files and v['script_sha256']==h(ROOT/script) and len(v['results'])==count and all(r['passed'] and not r['errors'] for r in v['results'])
  if 'styles' in v:assert v['styles']==styles
 from verify_submission_changes import EDIT
 v=read(dest/'results.json');assert len(EDIT)==13
 expected={('edit',name,None) for name in EDIT}|{('picker',name,None) for name in ['apply','cancel']}|{('concurrent',name,mode) for name in ['draft','generate'] for mode in ['finish','cancel']}
 assert {(r['kind'],r['case'],r['mode']) for r in v['results']}==expected
 for r in v['results']:
  if r['kind']=='edit':assert r['unchanged_before_retry'] and r['latest_input_saved_once']
  elif r['kind']=='picker':assert r['unchanged_with_picker_open'] and r['picker_result_and_retry_saved']
  elif r['mode']=='cancel':assert r['unchanged_before_decision']
  else:assert r['first_intent_only']
 for path,digest in {**files,**styles}.items():
  with urlopen(BASE+path.replace('custom/','pages/',1),timeout=10) as response:assert response.headers.get('Cache-Control')=='no-store' and hashlib.sha256(response.read()).hexdigest()==digest
 pages=list((DEMO/'custom').glob('*.html'));assert len(pages)==114
 for p in pages:assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
 reports={p.relative_to(ROOT).as_posix():h(p) for p in [v[0] for v in definitions]+[redpath]}
 names=[v[2] for v in definitions]+['verify_submission_changes_checkpoint.py','audit_hidden_overlays.py','verify_overlay_exit_paths.py','audit_current_runtime.py','book_test_helpers.py']+['verify_'+n+'_controls.py' for n in ['onboarding','record','moment','time','workshop','settings','pet','book']]
 cp=dict(files=files,styles=styles,reports_sha256=reports,scripts_sha256={n:h(ROOT/n) for n in names},executions=dict(red=dict(session='52245',exit_code=1),new_cases=dict(session='79880',exit_code=0),sequential_regressions=dict(session=args.regression_session,exit_code=0)),submission_change_cases=19,actual_case_observations=214,synthetic_contract_cases=20,total_checks=234,accepted_pages=0,scope='19 actual waiting-stage edit/picker/concurrent outcomes plus215 actual/shared guard/form regressions. This is not all114-page acceptance, all guard/rootless operations, or every condition after a business callback has started.')
 (dest/'checkpoint.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 statepath=out/'current-evidence-state.json';state=read(statepath);history=ROOT/'evidence/history/pre-submission-changes-651aba8';history.mkdir(parents=True,exist_ok=True)
 if state['files']!=files:
  (history/'current-evidence-state.json').write_bytes(statepath.read_bytes())
  for name,count in list(state.items()):
   if name.startswith('current_') and isinstance(count,int) and not isinstance(count,bool) and count>0:state['historical_'+name.removeprefix('current_')]=count;state[name]=0
 state.update(files=files,style_dependencies=styles,current_pending_form_cancel_cases=96,current_pending_form_contract_cases=8,current_overlay_form_save_cases=47,current_pending_page_guard_cases=52,current_pending_page_contract_cases=12,current_submission_change_cases=19,current_pending_form_checkpoint='evidence/current/submission-changes/checkpoint.json',current_pending_page_checkpoint='evidence/current/submission-changes/checkpoint.json',current_submission_checkpoint='evidence/current/submission-changes/checkpoint.json',previous_behavior_source_manifest='evidence/history/pre-submission-changes-651aba8/current-evidence-state.json',runtime_requires_refresh=True,catalog_requires_refresh=True,flow_replay_requires_refresh=True,submission_change_issue='fixed_for_19_observed_waiting_stage_cases',accepted_pages=0,reason=cp['scope'])
 statepath.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(new=19,regressions=215,total=234,mirrors=114,accepted_pages=0)))

if __name__=='__main__':main()
