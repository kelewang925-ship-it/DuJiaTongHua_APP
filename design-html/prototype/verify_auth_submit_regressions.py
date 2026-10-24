"""Refresh full runtime then run current auth contracts and source-bound catalog sequentially."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
from verify_pet_controls import ROOT,DEMO,source
from execution_source import current_source_fingerprint

def main():
 files=source();h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();styles={p.relative_to(DEMO).as_posix():h(p) for p in (DEMO/'assets').glob('*.css')};dest=ROOT/'evidence/current/auth-submit-context';rows=[]
 jobs=[('audit_current_runtime.py','current-runtime-summary.json',228),('verify_onboarding_controls.py','onboarding-control-results.json',82),('verify_onboarding_flow.py','onboarding-flow-results.json',8),('verify_session_invite_recovery.py','session-invite-results.json',15),('verify_new_user_journey.py','new-user-journey-results.json',2),('build_current_catalog.py',None,None),('build_page_contracts.py','page-contracts.json',114),('verify_page_contracts.py',None,None)]
 ap=argparse.ArgumentParser();ap.add_argument('--resume',action='store_true');args=ap.parse_args()
 if args.resume:
  old=json.loads((dest/'regressions.json').read_text(encoding='utf-8'));assert old['files']==files and old['styles']==styles and len(old['results'])==2 and old['script_sha256']==h(ROOT/'evidence/history/auth-regression-alert-locators/verify_auth_submit_regressions.py')
  for r in old['results']:assert r['exit_code']==0 and r['script_sha256']==h(ROOT/r['script']) and r['report_sha256']==h(ROOT/r['report'])
  rows=old['results'];jobs=jobs[2:];print('Reusing two verified current jobs; resume remaining six',flush=True)
 for script,name,count in jobs:
  print('RUN '+script,flush=True);sha=h(ROOT/script);run=subprocess.run([sys.executable,str(ROOT/script)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8');assert source()==files and h(ROOT/script)==sha and styles=={p.relative_to(DEMO).as_posix():h(p) for p in (DEMO/'assets').glob('*.css')}
  row=dict(script=script,script_sha256=sha,exit_code=run.returncode)
  if name:
   path=ROOT/'evidence/current'/name;v=json.loads(path.read_text(encoding='utf-8'));row.update(report=path.relative_to(ROOT).as_posix(),report_sha256=h(path))
   if script=='audit_current_runtime.py':
    assert v['files']==files and v['observations']==count and not v['errors'] and not v['unbound_or_delegated_candidates'];row.update(observations=v['observations'],controls_observed=v['controls_observed'],errors=0)
   elif script=='build_page_contracts.py':assert v['files']==files and len(v['pages'])==114 and len(v['assets'])==267;row.update(pages=114,assets=267)
   else:
    results=v['results'] if isinstance(v,dict) else v;assert len(results)==count and all(r['passed'] and not r['errors'] for r in results),[(r.get('case',r.get('label')),r.get('failure')) for r in results if not r['passed']]
    if isinstance(v,dict):assert v['files']==files
    if script=='verify_onboarding_controls.py':assert all(r['source_fingerprint']==current_source_fingerprint() for r in results)
    if script=='verify_new_user_journey.py':assert sum(len(r['steps']) for r in results)==13
    row.update(cases=count,passed=count,errors=0)
  rows.append(row);(dest/'regressions.json').write_text(json.dumps(dict(files=files,styles=styles,script_sha256=h(Path(__file__)),results=rows,accepted_pages=0),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(row),flush=True)
  if run.returncode:print(run.stdout[-6000:],flush=True);raise SystemExit(run.returncode)
 print('Current107 auth regressions,228 runtime observations and114-page catalog completed',flush=True)

if __name__=='__main__':main()
