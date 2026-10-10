"""Bind new state actions to production source, while explicitly preserving old evidence scopes."""
import hashlib,json
from verify_pet_controls import ROOT,DEMO,source

def main():
    out=ROOT/'evidence/current';c=json.loads((out/'shared-list-states-checkpoint.json').read_bytes());files=source();assert c['files']==files and c['accepted_pages']==0
    for name,digest in c['artifacts'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    report=json.loads((out/'shared-list-states-results.json').read_bytes());rows=report['results'];assert report['files']==files and len(rows)==110 and all(r['passed']and not r['errors']for r in rows)
    assert {r['width']for r in rows}=={320,360,390,414,430}
    assert len({(r['case'],r['width'])for r in rows})==110
    assert sum(r['kind']=='error'for r in rows)==50 and sum(r['kind']=='empty'for r in rows)==60
    assert all(r['geometry']['height']>=44 and r['geometry']['width']>=44 for r in rows)
    baseline=json.loads((ROOT/'evidence/baseline/shared-list-states-before.json').read_bytes());assert len(baseline['results'])==22 and not any(r['passed']for r in baseline['results'])
    old=baseline['files'];history=ROOT/'evidence/history/pre-shared-list-states-86e7bbe'
    for p in history.glob('prototype-*.*'):assert hashlib.sha256(p.read_bytes()).hexdigest()==old['assets/'+p.name],p.name
    loading=json.loads((out/'shared-list-loading-results.json').read_bytes());assert loading['files']==files and len(loading['results'])==30 and all(r['passed']and not r['errors']for r in loading['results'])
    state=json.loads((out/'current-evidence-state.json').read_bytes());assert state['files']==files and state['current_state_checks']==110 and state['current_loading_behavior_checks']==30 and state['historical_initial_controls']==752 and state['accepted_pages']==0
    for name in ['states','loading_regression']:assert c['executions'][name]['exit_code']==0
    assert state['runtime_requires_refresh']and state['catalog_requires_refresh']
    assert json.loads((out/'current-runtime-summary.json').read_bytes())['files']!=files
    assert json.loads((out/'page-contracts.json').read_bytes())['files']!=files
    for p in (DEMO/'custom').glob('*.html'):assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
    print(json.dumps({'current_state_checks':110,'current_loading_behavior_checks':30,'historical_initial_actions':752,'runtime_refresh_pending':True,'accepted_pages':0}))

if __name__=='__main__':main()
