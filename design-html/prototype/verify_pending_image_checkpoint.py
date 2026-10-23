"""Current-source proof for pending image reads; retain older full matrices as history."""
import argparse,hashlib,json
from pathlib import Path
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,BASE,source

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--regression-session',required=True);args=parser.parse_args();h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8'));out=ROOT/'evidence/current';dest=out/'pending-image-read';files=source();styles={p.relative_to(DEMO).as_posix():h(p) for p in (DEMO/'assets').glob('*.css')}
 baseline=ROOT/'evidence/baseline/pending-image-read';red=read(baseline/'results.json');assert len(red['results'])==8 and all(not r['passed'] and r['unchanged_while_image_reading'] is False for r in red['results']);assert red['script_sha256']==h(baseline/'verifier.py') and red['styles']==styles;assert red['files']['assets/prototype-ui.js']==h(baseline/'prototype-ui.js');assert {k for k in files if files[k]!=red['files'][k]}=={'assets/prototype-ui.js'}
 definitions=[(dest/'results.json',16,'verify_pending_image_reads.py'),(out/'submission-changes/results.json',19,'verify_submission_changes.py'),(out/'pending-page-guard/contract-results.json',12,'verify_pending_guard_contract.py')]
 for path,count,script in definitions:
  v=read(path);assert v['files']==files and v['styles']==styles and v['script_sha256']==h(ROOT/script) and len(v['results'])==count and all(r['passed'] and not r['errors'] for r in v['results'])
 from verify_pending_image_reads import SPECS
 result=read(dest/'results.json');assert len(SPECS)==8 and {(r['case'],r['mode']) for r in result['results']}=={(n,m) for n in SPECS for m in ['success','decode-failure']};assert all(r['unchanged_while_image_reading'] and r['save_during_read_blocked'] and r['explicit_retry_and_reload_consistent'] for r in result['results'])
 probes=[]
 for name,count,passed in [('pending-image-first-probe',16,10),('pending-image-navigation-probe',2,1)]:
  folder=ROOT/('evidence/history/'+name);v=read(folder/'results.json');assert v['files']==files and v['script_sha256']==h(folder/'verifier.py') and len(v['results'])==count and sum(r['passed'] for r in v['results'])==passed;probes.append(folder/'results.json')
 assert all(r['unchanged_while_image_reading'] and r['save_during_read_blocked'] for r in read(probes[0])['results'])
 assert all(r['diagnostic']['live'] is True for r in read(probes[-1])['results'] if not r['passed'])
 for path,digest in {**files,**styles}.items():
  with urlopen(BASE+path.replace('custom/','pages/',1),timeout=10) as response:assert response.headers.get('Cache-Control')=='no-store' and hashlib.sha256(response.read()).hexdigest()==digest
 pages=list((DEMO/'custom').glob('*.html'));assert len(pages)==114
 for p in pages:assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
 paths=[v[0] for v in definitions]+[baseline/'results.json']+probes;scripts=[v[2] for v in definitions]+['verify_pending_image_checkpoint.py','verify_pending_page_guard.py','verify_overlay_form_saves.py','audit_hidden_overlays.py','audit_current_runtime.py','book_test_helpers.py']+['verify_'+v+'_controls.py' for v in ['onboarding','record','moment','time','workshop','settings','pet','book']]
 cp=dict(files=files,styles=styles,reports_sha256={p.relative_to(ROOT).as_posix():h(p) for p in paths},scripts_sha256={n:h(ROOT/n) for n in scripts},executions=dict(red=dict(session='87496',exit_code=1),first_probe=dict(session='83308',exit_code=1),navigation_diagnostic=dict(session='82837',exit_code=1),image=dict(session='30331',exit_code=0),related_regressions=dict(session=args.regression_session,exit_code=0)),image_cases=16,related_actual_cases=19,shared_scope_contract_cases=12,total_checks=47,accepted_pages=0,scope='16 actual image-read success/failure outcomes,19 actual input/picker/concurrent outcomes and12 synthetic scope contracts. Earlier234-case full matrix retains its old source fingerprint; consolidated final replay remains required. No claim for stale parallel image reads, image-only pending navigation or every editing condition after operation start.')
 (dest/'checkpoint.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 statepath=out/'current-evidence-state.json';state=read(statepath);history=ROOT/'evidence/history/pre-pending-image-bc21206';history.mkdir(parents=True,exist_ok=True)
 if state['files']!=files:
  (history/'current-evidence-state.json').write_bytes(statepath.read_bytes())
  for name,count in list(state.items()):
   if name.startswith('current_') and isinstance(count,int) and not isinstance(count,bool) and count>0:state['historical_'+name.removeprefix('current_')]=count;state[name]=0
 for name in ['current_pending_form_checkpoint','current_pending_page_checkpoint']:state.pop(name,None)
 state.update(files=files,style_dependencies=styles,current_pending_image_cases=16,current_submission_change_cases=19,current_pending_page_contract_cases=12,current_image_read_checkpoint='evidence/current/pending-image-read/checkpoint.json',current_submission_checkpoint='evidence/current/pending-image-read/checkpoint.json',previous_behavior_source_manifest='evidence/history/pre-pending-image-bc21206/current-evidence-state.json',runtime_requires_refresh=True,catalog_requires_refresh=True,flow_replay_requires_refresh=True,pending_image_read_issue='fixed_for_eight_observed_save_entries',accepted_pages=0,reason=cp['scope'])
 statepath.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(image=16,related=19,shared_contract=12,total=47,mirrors=114,accepted_pages=0)))

if __name__=='__main__':main()
