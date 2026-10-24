"""Current auth evidence and refreshed114-page observation/catalog, without final acceptance."""
import hashlib,json,re
from pathlib import Path
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,BASE,source
from verify_auth_submit_context import CASES

def main():
 h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8'));out=ROOT/'evidence/current';dest=out/'auth-submit-context';files=source();styles={p.relative_to(DEMO).as_posix():h(p) for p in (DEMO/'assets').glob('*.css')}
 redroot=ROOT/'evidence/baseline/auth-submit-context';red=read(redroot/'results.json');v=read(dest/'results.json')
 assert len(red['results'])==40 and sum(r['passed'] for r in red['results'])==4 and all(not r['errors'] for r in red['results'])
 assert red['script_sha256']==h(redroot/'verify_auth_submit_context.py') and red['styles']==styles and h(redroot/'prototype-auth-flow.js')==red['files']['assets/prototype-auth-flow.js']
 assert {k for k in files if files[k]!=red['files'][k]}=={'assets/prototype-auth-flow.js'}
 assert v['files']==files and v['styles']==styles and v['script_sha256']==h(ROOT/'verify_auth_submit_context.py') and len(v['results'])==40 and {(r['kind'],r['mode']) for r in v['results']}==set(CASES) and all(r['passed'] and not r['errors'] for r in v['results'])
 assert sum(r.get('rollback_preserved_all_state',False) for r in v['results'])==14 and sum(r.get('stale_submit_rejected_with_input',False) for r in v['results'])==21 and sum(r.get('actual_content_keys_initialized',False) for r in v['results'])==2
 regression=read(dest/'regressions.json');assert regression['files']==files and regression['styles']==styles and regression['script_sha256']==h(ROOT/'verify_auth_submit_regressions.py') and len(regression['results'])==8 and all(r['exit_code']==0 for r in regression['results'])
 expected={'verify_onboarding_controls.py':82,'verify_onboarding_flow.py':8,'verify_session_invite_recovery.py':15,'verify_new_user_journey.py':2};reports=[dest/'results.json',dest/'regressions.json',redroot/'results.json'];scripts=['verify_auth_submit_context.py','verify_auth_submit_regressions.py','verify_auth_submit_checkpoint.py','diagnose_auth_rollback.py','audit_submission_awaits.cjs','execution_source.py','audit_hidden_overlays.py','verify_pet_controls.py','audit_runtime.py']
 for r in regression['results']:
  scripts.append(r['script']);assert r['script_sha256']==h(ROOT/r['script'])
  if 'report' in r:reports.append(ROOT/r['report']);assert r['report_sha256']==h(ROOT/r['report'])
  if r['script'] in expected:assert r['cases']==r['passed']==expected[r['script']] and r['errors']==0
 runtime=read(out/'current-runtime-summary.json');observations=read(out/'current-runtime-inventory.json');assert runtime['files']==files and runtime['observations']==len(observations)==228 and runtime['controls_observed']==1696 and not runtime['errors'] and not runtime['unbound_or_delegated_candidates']
 assert {(r['id'],r['scenario']) for r in observations}=={(p.stem,s) for p in (DEMO/'custom').glob('*.html') for s in ['empty','populated']}
 catalog=read(out/'page-contracts.json');assert catalog['files']==files and len(catalog['pages'])==114 and len(catalog['assets'])==267
 controls=[r for p in catalog['pages'] for r in p['control_evidence']];assert len(controls)==752 and sum(r['status']=='当前源码通过' for r in controls)==82 and sum(r['status']=='历史通过／待当前复验' for r in controls)==670
 journeys=read(out/'new-user-journey-results.json');assert sum(len(r['steps']) for r in journeys['results'])==13
 first=ROOT/'evidence/history/auth-submit-first-current';v=read(first/'results.json');assert v['files']==files and v['script_sha256']==red['script_sha256'] and len(v['results'])==40 and sum(r['passed'] for r in v['results'])==32 and read(first/'execution.json')['exit_code']==1
 diagnostic=ROOT/'evidence/history/auth-registration-rollback-diagnostic';v=read(diagnostic/'results.json');assert v['files']==files and v['script_sha256']==h(ROOT/'diagnose_auth_rollback.py') and len(v['results'])==2 and all(r['values_equal'] and all(not c for c in r['changed_keys'].values()) for r in v['results'])
 probe=ROOT/'evidence/history/auth-submit-unmodified-probe';assert read(probe/'results.json')['files']==red['files'] and read(probe/'note.json')['exit_code']==1
 locator_history=ROOT/'evidence/history/auth-regression-alert-locators';old=read(locator_history/'regressions.json');assert old['files']==files and old['styles']==styles and len(old['results'])==2 and old['script_sha256']==h(locator_history/'verify_auth_submit_regressions.py') and old['results']==regression['results'][:2] and read(locator_history/'execution.json')['exit_code']==1
 assert read(locator_history/'onboarding-flow-source.json')['files']==files
 oldflow=read(locator_history/'onboarding-flow-results.json');assert len(oldflow)==8 and sum(r['passed'] for r in oldflow)==6
 reports.extend([locator_history/'regressions.json',locator_history/'onboarding-flow-results.json',locator_history/'execution.json'])
 inventorypath=out/'submission-await-audit/inventory.json';inventory=read(inventorypath);assert inventory['files']=={k:v for k,v in files.items() if k.endswith('.js')} and inventory['script_sha256']==h(ROOT/'audit_submission_awaits.cjs') and len(inventory['results'])==78
 required=lambda p:[line.split('|')[1:3] for line in p.read_text(encoding='utf-8').splitlines() if re.match(r'^\| \d+ ',line)]
 history=ROOT/'evidence/history/pre-auth-submit-1ac29c3';assert len(required(history/'ACCEPTANCE_REQUIREMENTS.md'))==41 and required(ROOT/'ACCEPTANCE_REQUIREMENTS.md')==required(history/'ACCEPTANCE_REQUIREMENTS.md')
 for path,digest in {**files,**styles}.items():
  with urlopen(BASE+path.replace('custom/','pages/',1),timeout=10) as response:assert response.headers.get('Cache-Control')=='no-store' and hashlib.sha256(response.read()).hexdigest()==digest
 pages=list((DEMO/'custom').glob('*.html'));assert len(pages)==114
 for p in pages:assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
 reports.extend([out/'current-runtime-inventory.json',out/'page-contract-audit-checkpoint.json',out/'current-navigation-candidates.json',out/'onboarding-flow-source.json',first/'results.json',first/'execution.json',diagnostic/'results.json',probe/'results.json',probe/'note.json',inventorypath])
 documents=['SESSION_INVITE_IMPLEMENTATION.md','AUTH_SUBMIT_CONTEXT.md','ACCEPTANCE_REQUIREMENTS.md','README.md','ISSUES.md','SUBMISSION_AWAIT_AUDIT.md','CURRENT_PAGES.md','CURRENT_CONTROL_AUDIT.md','PAGE_CATALOG.md','CURRENT_NAVIGATION.md','PAGE_RELATIONSHIPS.mmd','STATE_MATRIX.md'];canonical=lambda p:hashlib.sha256(p.read_text(encoding='utf-8').replace('\r\n','\n').encode()).hexdigest()
 scope='40 auth submit/rollback cases plus107 existing contracts, flows and new-user journeys.228 runtime observations and114-page/267-asset catalog refreshed;82 initial controls current,670 historical. This does not prove all product branches, layouts or final114-page acceptance.'
 cp=dict(files=files,styles=styles,reports_sha256={p.relative_to(ROOT).as_posix():h(p) for p in reports},scripts_sha256={n:h(ROOT/n) for n in set(scripts)},document_text_sha256={n:canonical(ROOT/n) for n in documents},queue_sha256=h(ROOT/'queue.json'),executions=dict(baseline=dict(session='79376',exit_code=1,cases=40,passed=4),unmodified_probe=dict(session='88994',exit_code=1,intentionally_stopped=True),first_current=dict(session='40787',exit_code=1,passed=32,cases=40),native=dict(session='76094',exit_code=0,cases=40),regressions_initial=dict(session='92990',exit_code=1,completed_jobs=2),regressions_resume=dict(session='75553',exit_code=0,cases=107),source_audit=dict(chunk='9f965f',exit_code=0),rollback_diagnostic=dict(chunk='4df012',exit_code=0)),native_cases=40,regression_cases=107,total_checks=147,runtime_observations=228,runtime_controls=1696,catalog_pages=114,catalog_assets=267,accepted_pages=0,scope=scope)
 (dest/'checkpoint.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 statepath=out/'current-evidence-state.json';state=read(statepath)
 if state['files']!=files:
  assert state['files']==red['files']
  for name,count in list(state.items()):
   if name.startswith('current_') and isinstance(count,int) and not isinstance(count,bool) and count>0:state['historical_'+name.removeprefix('current_')]=count;state[name]=0
 state.update(files=files,style_dependencies=styles,current_auth_submit_context_cases=40,current_onboarding_control_cases=82,current_onboarding_flow_cases=8,current_session_invite_cases=15,current_initial_controls=82,historical_initial_controls=670,current_continuous_journey_cases=2,current_continuous_journey_steps=13,current_auth_submit_checkpoint='evidence/current/auth-submit-context/checkpoint.json',previous_behavior_source_manifest='evidence/history/pre-auth-submit-1ac29c3/current-evidence-state.json',runtime_requires_refresh=False,catalog_requires_refresh=False,flow_replay_requires_refresh=True,auth_submit_context_issue='fixed_for_24_context_cases_and_registration_rollback_and_initialization',accepted_pages=0,reason=scope)
 statepath.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(native=40,regressions=107,total=147,observations=228,current_initial=82,historical_initial=670,catalog_pages=114,assets=267,mirrors=114,accepted_pages=0)))

if __name__=='__main__':main()
