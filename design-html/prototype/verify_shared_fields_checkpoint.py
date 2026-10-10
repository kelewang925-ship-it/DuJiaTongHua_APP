"""Bind shared overlay fields and current identity regression without promoting old catalogs."""
import hashlib,json
from verify_pet_controls import ROOT,DEMO,source

def main():
    out=ROOT/'evidence/current';c=json.loads((out/'shared-overlay-fields-checkpoint.json').read_bytes());files=source();assert c['files']==files and c['accepted_pages']==0
    for name,digest in c['artifacts'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    fields=json.loads((out/'shared-overlay-fields-results.json').read_bytes());assert fields['files']==files and len(fields['results'])==71 and all(r['passed']and not r.get('errors')for r in fields['results'])
    dynamic=[r for r in fields['results']if 'index'in r];assert len(dynamic)==70 and len({(r['index'],r['width'])for r in dynamic})==70
    assert {r['width']for r in dynamic}=={320,360,390,414,430}
    assert all(r['quota_retry_preserved']for r in dynamic)
    assert all(r['inline_error_verified']for r in dynamic if r['index']!=52)
    baseline=json.loads((ROOT/'evidence/baseline/shared-overlay-fields-before.json').read_bytes());assert len(baseline['results'])==15 and not any(r['passed']for r in baseline['results'])
    for p in (ROOT/'evidence/history/pre-shared-overlay-fields-9227657').glob('prototype-*.*'):assert hashlib.sha256(p.read_bytes()).hexdigest()==baseline['files']['assets/'+p.name],p.name
    identity=json.loads((out/'identity-deletion-results.json').read_bytes());assert identity['files']==files and len(identity['results'])==13 and all(r['passed']and not r['errors']for r in identity['results'])and identity['locator_candidates_only']
    prior_raw=(ROOT/'evidence/baseline/identity-deletion-before-inline-field-error-check.json').read_bytes();prior=json.loads(prior_raw);assert identity['retained_baseline_sha256']==hashlib.sha256(prior_raw).hexdigest()
    assert len(identity['retained_indices'])==10 and len(identity['replayed_indices'])==3
    assert sorted(identity['retained_indices']+identity['replayed_indices'])==list(range(13))
    assert all(identity['results'][i]==prior['results'][i]for i in identity['retained_indices'])
    assert {(identity['results'][i]['observation_index'],identity['results'][i]['mode'])for i in identity['replayed_indices']}=={(59,'blank'),(59,'wrong'),(99,'blank')}
    state=json.loads((out/'current-evidence-state.json').read_bytes());assert state['files']==files and state['current_overlay_field_checks']==71 and state['current_identity_cases']==13 and state['historical_initial_controls']==752 and state['runtime_requires_refresh']and state['catalog_requires_refresh']and state['accepted_pages']==0
    for key in ['fields','identity_inline_replay']:assert c['executions'][key]['exit_code']==0
    for p in (DEMO/'custom').glob('*.html'):assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
    print(json.dumps({'current_overlay_field_checks':71,'current_identity_cases':13,'historical_initial_actions':752,'accepted_pages':0}))

if __name__=='__main__':main()
