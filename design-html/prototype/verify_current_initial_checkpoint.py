"""Verify frozen-source initial replay and retain only unchanged auth business evidence."""
import argparse,hashlib,json,re
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,BASE,source
from refresh_remaining_initial_controls import GROUPS

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--six-session',required=True);ap.add_argument('--six-exit',type=int,required=True);ap.add_argument('--settings-session',required=True);ap.add_argument('--settings-exit',type=int,required=True);ap.add_argument('--catalog-exit',type=int,required=True);a=ap.parse_args();assert a.six_exit==a.settings_exit==a.catalog_exit==0
 h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8'));files=source();out=ROOT/'evidence/current';dest=out/'current-initial-replay';dest.mkdir(parents=True,exist_ok=True)
 styles={p.relative_to(DEMO).as_posix():h(p) for p in (DEMO/'assets').glob('*.css')};meta=read(out/'remaining-initial-refresh-source.json');assert meta['files']==files and len(meta['reports'])==6
 reports=[out/'remaining-initial-refresh-source.json'];scripts=['verify_current_initial_checkpoint.py','refresh_remaining_initial_controls.py','verify_settings_controls.py','build_page_contracts.py','verify_page_contracts.py'];total=initial=0
 for group,script,_,count,native in GROUPS:
  path=out/(group+'-controls-results.json');v=read(path);r=meta['reports'][path.name];assert v['files']==files and r['exit_code']==0 and r['source_current'] and r['sha256']==h(path) and r['cases']==r['passed']==count and r['initial_cases']==native and r['errors']==0
  assert len(v['results'])==count and all(r['passed'] and not r['errors'] for r in v['results']) and meta['scripts'][script]==h(ROOT/script);reports.append(path);scripts.append(script);total+=count;initial+=native
 assert total==615 and initial==589
 settings=read(out/'settings-controls-results.json');assert settings['files']==files and len(settings['results'])==81 and all(r['passed'] and not r['errors'] for r in settings['results']);reports.append(out/'settings-controls-results.json')
 auth=read(ROOT/'evidence/history/pre-current-initial-d86390a/auth-submit-checkpoint.json');assert auth['files']==files and auth['styles']==styles
 retained={'evidence/current/auth-submit-context/results.json':40,'evidence/current/onboarding-control-results.json':82,'evidence/current/onboarding-flow-results.json':8,'evidence/current/session-invite-results.json':15,'evidence/current/new-user-journey-results.json':2}
 for name,count in retained.items():
  path=ROOT/name;assert h(path)==auth['reports_sha256'][name];v=read(path);rows=v['results'] if isinstance(v,dict) else v;assert len(rows)==count and all(r['passed'] and not r['errors'] for r in rows)
  if isinstance(v,dict):assert v['files']==files
  reports.append(path)
 for n in ['verify_auth_submit_context.py','verify_onboarding_controls.py','verify_onboarding_flow.py','verify_session_invite_recovery.py','verify_new_user_journey.py']:assert h(ROOT/n)==auth['scripts_sha256'][n];scripts.append(n)
 runtime=read(out/'current-runtime-summary.json');assert runtime['files']==files and runtime['observations']==228 and runtime['controls_observed']==1696 and not runtime['errors'] and not runtime['unbound_or_delegated_candidates']
 catalog=read(out/'page-contracts.json');assert catalog['files']==files and len(catalog['pages'])==114 and len(catalog['assets'])==267
 controls=[c for p in catalog['pages'] for c in p['control_evidence']];assert len(controls)==752 and all(c['status']=='当前源码通过' for c in controls)
 for path,digest in {**files,**styles}.items():
  with urlopen(BASE+path.replace('custom/','pages/',1),timeout=10) as response:assert response.headers.get('Cache-Control')=='no-store' and hashlib.sha256(response.read()).hexdigest()==digest
 pages=list((DEMO/'custom').glob('*.html'));assert len(pages)==114
 for p in pages:assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
 before=ROOT/'evidence/history/pre-current-initial-d86390a';requirements=lambda p:[line.split('|')[1:3] for line in p.read_text(encoding='utf-8').splitlines() if re.match(r'^\| \d+ ',line)]
 assert len(requirements(before/'ACCEPTANCE_REQUIREMENTS.md'))==41 and requirements(before/'ACCEPTANCE_REQUIREMENTS.md')==requirements(ROOT/'ACCEPTANCE_REQUIREMENTS.md')
 reports.extend(out/n for n in ['page-contracts.json','page-contract-audit-checkpoint.json','current-runtime-summary.json','current-runtime-inventory.json']);reports.append(before/'auth-submit-checkpoint.json')
 canonical=lambda p:hashlib.sha256(p.read_text(encoding='utf-8').replace('\r\n','\n').encode()).hexdigest();documents=['CURRENT_INITIAL_REPLAY.md','ACCEPTANCE_REQUIREMENTS.md','README.md','ISSUES.md','PAGE_CATALOG.md','CURRENT_NAVIGATION.md','PAGE_RELATIONSHIPS.mmd','STATE_MATRIX.md']
 scope='Frozen product source replay:615 checks across six modules plus81 settings checks;589+81 newly current initial controls and retained82 onboarding controls total752.26 supplemental checks and unchanged147 auth contracts/journeys retained explicitly;843 cases total. Does not establish every hidden state, exception, source or final114-page acceptance.'
 cp=dict(files=files,styles=styles,queue_sha256=h(ROOT/'queue.json'),reports_sha256={p.relative_to(ROOT).as_posix():h(p) for p in reports},scripts_sha256={n:h(ROOT/n) for n in set(scripts)},document_text_sha256={n:canonical(ROOT/n) for n in documents},executions=dict(six_modules=dict(session=a.six_session,exit_code=a.six_exit,cases=615),settings=dict(session=a.settings_session,exit_code=a.settings_exit,cases=81),catalog=dict(exit_code=a.catalog_exit)),new_checks=696,retained_business_checks=147,total_checks=843,current_initial_controls=752,historical_initial_controls=0,supplemental_checks=26,accepted_pages=0,scope=scope)
 (dest/'checkpoint.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 statepath=out/'current-evidence-state.json';state=read(statepath);assert state['files']==files
 state.update(current_initial_controls=752,historical_initial_controls=0,current_initial_supplemental_checks=26,current_settings_control_cases=81,current_record_control_cases=109,current_moment_control_cases=55,current_time_control_cases=54,current_workshop_control_cases=92,current_pet_control_cases=151,current_book_control_cases=154,current_initial_checkpoint='evidence/current/current-initial-replay/checkpoint.json',runtime_requires_refresh=False,catalog_requires_refresh=False,flow_replay_requires_refresh=True,accepted_pages=0,reason=scope)
 statepath.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(new_checks=696,retained_checks=147,total=843,current_initial=752,historical_initial=0,supplemental=26,accepted_pages=0)))

if __name__=='__main__':main()
