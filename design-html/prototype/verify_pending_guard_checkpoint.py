"""Current-source evidence for top-level pending task cancellation and sheet regressions."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,BASE,source

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--page-session',required=True);parser.add_argument('--regression-session',required=True);args=parser.parse_args()
 h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8'));out=ROOT/'evidence/current';dest=out/'pending-page-guard';files=source();styles={p.relative_to(DEMO).as_posix():h(p) for p in (DEMO/'assets').glob('*.css')}
 baseline=ROOT/'evidence/baseline/pending-page-guard';red=read(baseline/'results.json');assert len(red['results'])==3 and all(not r['passed'] and r['storage_unchanged_before_decision'] is False for r in red['results']);assert red['script_sha256']==h(baseline/'verifier.py')
 assert red['files']['assets/prototype-ui.js']==h(baseline/'prototype-ui.js') and red['styles']==styles
 assert {k for k in files if red['files'][k]!=files[k]}=={'assets/prototype-ui.js'}
 definitions=[(dest/'results.json',52,'verify_pending_page_guard.py'),(dest/'contract-results.json',12,'verify_pending_guard_contract.py'),(out/'pending-form-cancel/results.json',96,'verify_pending_form_cancel.py'),(out/'pending-form-cancel/contract-results.json',8,'verify_pending_form_contract.py'),(out/'overlay-form-save-results.json',47,'verify_overlay_form_saves.py')]
 for path,count,script in definitions:
  r=read(path);assert r['files']==files and len(r['results'])==count and all(v['passed'] and not v['errors'] for v in r['results']);assert r['script_sha256']==h(ROOT/script)
  if 'styles' in r:assert r['styles']==styles
 from verify_pending_page_guard import CASES
 r=read(dest/'results.json');assert len(CASES)==13 and len({v['page'] for v in CASES.values()})==11
 assert {(v['case'],v['exit'],v['mode']) for v in r['results']}=={(n,e,m) for n in CASES for e in ['button','back'] for m in ['keep','discard']}
 assert all(v['storage_unchanged_before_decision'] and (v.get('discard_reload_consistent') if v['mode']=='discard' else v.get('retry_saved_once_and_reload_consistent')) for v in r['results'])
 probe=ROOT/'evidence/history/pending-page-guard-first-probe';first=read(probe/'results.json');assert first['files']==files and first['script_sha256']==h(probe/'verifier.py') and len(first['results'])==52 and sum(v['passed'] for v in first['results'])==49 and all(v['case']=='pet-adopt' for v in first['results'] if not v['passed'])
 for path,digest in {**files,**styles}.items():
  with urlopen(BASE+path.replace('custom/','pages/',1),timeout=10) as response:assert response.headers.get('Cache-Control')=='no-store' and hashlib.sha256(response.read()).hexdigest()==digest
 pages=list((DEMO/'custom').glob('*.html'));assert len(pages)==114
 for p in pages:assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
 reports={p.relative_to(ROOT).as_posix():h(p) for p in [v[0] for v in definitions]+[baseline/'results.json',probe/'results.json']}
 helper_names=['verify_pending_guard_checkpoint.py','audit_hidden_overlays.py','verify_overlay_exit_paths.py','audit_current_runtime.py','book_test_helpers.py']+['verify_'+v+'_controls.py' for v in ['onboarding','record','moment','time','workshop','settings','pet','book']]
 scripts={n:h(ROOT/n) for n in [v[2] for v in definitions]+helper_names}
 checkpoint=dict(files=files,styles=styles,reports_sha256=reports,scripts_sha256=scripts,executions=dict(red=dict(chunk='c84c21',exit_code=1),first_probe=dict(session='40947',exit_code=1,reason='49 passed; two wrong pet return selectors and null predicate before async save'),page_and_guard_contract=dict(session=args.page_session,exit_code=0),sheet_regressions=dict(session=args.regression_session,exit_code=0)),page_task_cases=52,page_tasks=13,page_count=11,page_guard_contract_cases=12,sheet_cancel_cases=96,sheet_contract_cases=8,sheet_save_cases=47,accepted_pages=0,scope='52 actual top-level task outcomes on11 pages plus96 actual sheet outcomes and47 actual save/invalid/quota checks;20 synthetic helper contracts. Other guards, nested picker timing, concurrent tasks, runtime/catalog/layout/final journeys still require verification.')
 (dest/'checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 statepath=out/'current-evidence-state.json';state=read(statepath);history=ROOT/'evidence/history/pre-page-guard-16413f4';history.mkdir(parents=True,exist_ok=True)
 if state['files']!=files:
  (history/'current-evidence-state.json').write_bytes(statepath.read_bytes())
  for name,count in list(state.items()):
   if name.startswith('current_') and isinstance(count,int) and not isinstance(count,bool) and count>0:state['historical_'+name.removeprefix('current_')]=count;state[name]=0
 state.update(files=files,style_dependencies=styles,current_pending_form_cancel_cases=96,current_pending_form_contract_cases=8,current_overlay_form_save_cases=47,current_pending_page_guard_cases=52,current_pending_page_contract_cases=12,current_pending_form_checkpoint='evidence/current/pending-page-guard/checkpoint.json',current_pending_page_checkpoint='evidence/current/pending-page-guard/checkpoint.json',previous_behavior_source_manifest='evidence/history/pre-page-guard-16413f4/current-evidence-state.json',runtime_requires_refresh=True,catalog_requires_refresh=True,flow_replay_requires_refresh=True,pending_page_guard_issue='fixed_for_13_observed_tasks',accepted_pages=0,reason=checkpoint['scope'])
 statepath.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(page_cases=52,page_tasks=13,pages=11,page_contract=12,sheet_cancel=96,sheet_contract=8,save=47,mirrors=114,accepted_pages=0)))

if __name__=='__main__':main()
