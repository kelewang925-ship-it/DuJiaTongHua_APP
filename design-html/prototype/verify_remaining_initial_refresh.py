"""Verify actual six-module exits, retained evidence and full current catalog."""
import argparse,hashlib,json
from verify_pet_controls import ROOT,source
from refresh_remaining_initial_controls import GROUPS

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--parent-session',type=int,required=True);parser.add_argument('--parent-exit',type=int,required=True);args=parser.parse_args()
    assert args.parent_exit==0
    out=ROOT/'evidence/current';files=source();h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    meta=json.loads((out/'remaining-initial-refresh-source.json').read_text(encoding='utf-8'));assert meta['files']==files
    assert set(meta['reports'])=={group+'-controls-results.json'for group,_,_,_,_ in GROUPS}
    for group,script,_,count,initial in GROUPS:
        name=group+'-controls-results.json';execution=meta['reports'][name];report=json.loads((out/name).read_text(encoding='utf-8'))
        assert execution['exit_code']==0 and execution['source_current']
        assert execution['expected_checks']==execution['cases']==execution['passed']==count
        assert execution['expected_initial']==execution['initial_cases']==initial and not execution['errors']
        assert execution['sha256']==h(out/name)and meta['scripts'][script]==h(ROOT/script)
        assert report['files']==files and all(r['passed']and not r['errors']for r in report['results'])
    assert sum(v['cases']for v in meta['reports'].values())==615
    assert sum(v['initial_cases']for v in meta['reports'].values())==589
    retained=json.loads((out/'identity-deletion-checkpoint.json').read_text(encoding='utf-8'));assert retained['files']==files
    for name in ['identity-deletion-results.json','identity-deletion-summary.json','settings-controls-results.json','onboarding-control-results.json','current-runtime-summary.json','current-runtime-inventory.json']:
        assert h(out/name)==retained['reports'][name],name
    old_catalog=ROOT/'evidence/history/pre-remaining-refresh-97edd42/page-contracts.json'
    assert h(old_catalog)==retained['reports']['page-contracts.json']
    for name,digest in retained['scripts'].items():assert h(ROOT/name)==digest
    catalog=json.loads((out/'page-contracts.json').read_text(encoding='utf-8'));assert catalog['files']==files
    rows=[r for page in catalog['pages']for r in page['control_evidence']]
    assert len(rows)==752 and all(r['status']=='当前源码通过'for r in rows)
    identity=json.loads((out/'identity-deletion-results.json').read_text(encoding='utf-8'));assert len(identity['results'])==13 and all(r['passed']and not r['errors']for r in identity['results'])
    scripts={**meta['scripts'],**{name:h(ROOT/name)for name in ['refresh_remaining_initial_controls.py','verify_remaining_initial_refresh.py']}}
    checkpoint=dict(files=files,reports=meta['reports'],scripts=scripts,newly_executed_checks=615,newly_executed_initial=589,
        retained_initial=163,current_initial_controls=752,historical_initial_controls=0,retained_identity=13,
        parent_execution=dict(session_id=args.parent_session,exit_code=args.parent_exit),accepted_pages=0,
        catalog_sha256=h(out/'page-contracts.json'),retained_phase_checkpoint_sha256=h(out/'identity-deletion-checkpoint.json'))
    (out/'remaining-initial-refresh-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    state=dict(files=files,current_initial_controls=752,historical_initial_controls=0,reports=catalog['reports'],current_identity_cases=13,
        historical_phase_checkpoints=['overlay-exit-checkpoint.json','overlay-form-save-checkpoint.json','confirmed-deletion-checkpoint.json','book-candidate-deletion-checkpoint.json'],
        reason='Six initial modules replayed after account deletion repair; older hidden phase evidence still requires current replay',accepted_pages=0)
    (out/'current-evidence-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert source()==files
    print(json.dumps(dict(new_checks=615,new_initial=589,current_initial=752,historical_initial=0,retained_identity=13,accepted_pages=0)))

if __name__=='__main__':main()
