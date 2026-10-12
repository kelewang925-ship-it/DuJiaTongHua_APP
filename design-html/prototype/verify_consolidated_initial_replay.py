"""Verify the current six-module batch and retained guard-phase initial proofs."""
import argparse,json,hashlib
from verify_pet_controls import ROOT,source
from refresh_remaining_initial_controls import GROUPS

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--parent-session',type=int,required=True);parser.add_argument('--parent-exit',type=int,required=True);args=parser.parse_args();assert args.parent_exit==0
    files=source();out=ROOT/'evidence/current';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();meta=json.loads((out/'remaining-initial-refresh-source.json').read_text(encoding='utf-8'));assert meta['files']==files and set(meta['reports'])=={g+'-controls-results.json'for g,_,_,_,_ in GROUPS}
    for group,script,_,checks,initial in GROUPS:
        name=group+'-controls-results.json';execution=meta['reports'][name];report=json.loads((out/name).read_text(encoding='utf-8'));assert report['files']==files and execution['exit_code']==0 and execution['source_current']and execution['cases']==execution['passed']==checks and execution['initial_cases']==initial and not execution['errors'];assert all(r['passed']and not r['errors']for r in report['results']);assert execution['sha256']==h(out/name)and meta['scripts'][script]==h(ROOT/script)
    retained=json.loads((out/'consolidated-runtime-guard-checkpoint.json').read_text(encoding='utf-8'));assert retained['files']==files
    for name in ['onboarding-control-results.json','settings-controls-results.json','guard-metadata-results.json','current-runtime-inventory.json','current-runtime-summary.json']:
        assert retained['artifacts_sha256']['prototype/evidence/current/'+name]==h(out/name),name
    onboarding=json.loads((out/'onboarding-control-results.json').read_text(encoding='utf-8'));fingerprint=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest();assert len(onboarding)==82 and all(r['passed']and not r['errors']and r['source_fingerprint']==fingerprint for r in onboarding)
    settings=json.loads((out/'settings-controls-results.json').read_text(encoding='utf-8'));assert settings['files']==files and len(settings['results'])==81 and all(r['passed']and not r['errors']for r in settings['results'])
    catalog=json.loads((out/'page-contracts.json').read_text(encoding='utf-8'));assert catalog['files']==files;controls=[c for p in catalog['pages']for c in p['control_evidence']];assert len(controls)==752 and all(c['status']=='当前源码通过'for c in controls)
    checkpoint=dict(files=files,parent_execution=dict(session_id=args.parent_session,exit_code=args.parent_exit),reports=meta['reports'],script_sha256={name:h(ROOT/name)for name in [*[v[1]for v in GROUPS],'refresh_remaining_initial_controls.py','verify_consolidated_initial_replay.py','build_page_contracts.py','verify_page_contracts.py']},new_checks=615,new_initial=589,retained_initial=163,current_initial=752,historical_initial=0,retained_guard_checks=6,retained_phase_sha256=h(out/'consolidated-runtime-guard-checkpoint.json'),catalog_sha256=h(out/'page-contracts.json'),accepted_pages=0,scope='All752 existing initial-control contracts current;26 supplemental record/moment checks and6 guard checks. No promotion of whole hidden/identity/global/layout evidence.')
    (out/'consolidated-initial-replay-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    p=out/'current-evidence-state.json';state=json.loads(p.read_text(encoding='utf-8'));state['files']=files;state.update(current_initial_controls=752,historical_initial_controls=0,current_initial_supplemental_checks=26,current_guard_metadata_checks=6,accepted_pages=0,runtime_requires_refresh=False,catalog_requires_refresh=False,reason='Six existing initial suites executed615 checks with actual child/parent exits0, including589 initial plus26 supplemental; retained163 current onboarding/settings initial controls and6 guard checks. All752 initial contracts source-current; hidden/identity/whole-journey/layout evidence still requires completion.');p.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(new_checks=615,current_initial=752,historical_initial=0,retained_guard=6,accepted_pages=0)))

if __name__=='__main__':main()
