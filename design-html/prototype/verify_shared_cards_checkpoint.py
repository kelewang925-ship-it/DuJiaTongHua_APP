"""Validate current dynamic Card routes, retained observations and state regression."""
import hashlib,json
from verify_pet_controls import ROOT,DEMO,source

def main():
    out=ROOT/'evidence/current';c=json.loads((out/'shared-list-cards-checkpoint.json').read_bytes());files=source();assert c['files']==files and c['accepted_pages']==0
    for name,digest in c['artifacts'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    report=json.loads((out/'shared-list-cards-results.json').read_bytes());rows=report['results'];assert report['files']==files and len(rows)==66 and all(r['passed']and not r.get('errors')for r in rows)
    dynamic=[r for r in rows if r['case']!='factory-content-and-default-contract'];assert len(dynamic)==65 and len({(r['case'],r['width'])for r in dynamic})==65
    assert {r['width']for r in dynamic}=={320,360,390,414,430}
    assert all(r['geometry']['hit']and r['geometry']['width']>=44 and r['geometry']['height']>=44 for r in dynamic)
    previous=json.loads((ROOT/'evidence/baseline/shared-list-cards-before-reminder-days-fix.json').read_bytes())
    first_raw=(ROOT/'evidence/baseline/shared-list-cards-before-probe-fix.json').read_bytes();first=json.loads(first_raw)
    assert previous['files']==files and first['files']==files
    assert previous['retained_baseline_sha256']==hashlib.sha256(first_raw).hexdigest()
    assert len(previous['retained_indices'])==60 and all(previous['results'][i]==first['results'][i]for i in previous['retained_indices'])
    prior_raw=(ROOT/'evidence/baseline/shared-list-cards-before-reminder-days-fix.json').read_bytes();assert report['retained_baseline_sha256']==hashlib.sha256(prior_raw).hexdigest()
    assert len(report['retained_indices'])==61 and len(report['replayed_indices'])==5
    assert sorted(report['retained_indices']+report['replayed_indices'])==list(range(66))
    assert all(rows[i]==previous['results'][i]for i in report['retained_indices'])
    assert {(rows[i]['case'],rows[i]['width'])for i in report['replayed_indices']}=={('reminder',w)for w in [320,360,390,414,430]}
    state_report=json.loads((out/'shared-list-states-results.json').read_bytes());assert state_report['files']==files and len(state_report['results'])==110 and all(r['passed']and not r['errors']for r in state_report['results'])
    baseline=json.loads((ROOT/'evidence/baseline/shared-list-cards-before.json').read_bytes());assert len(baseline['results'])==14 and not any(r['passed']for r in baseline['results'])
    for p in (ROOT/'evidence/history/pre-shared-list-cards-62f7d29').glob('prototype-*.*'):assert hashlib.sha256(p.read_bytes()).hexdigest()==baseline['files']['assets/'+p.name],p.name
    state=json.loads((out/'current-evidence-state.json').read_bytes());assert state['files']==files and state['current_card_checks']==66 and state['current_state_checks']==110 and state['historical_initial_controls']==752 and state['runtime_requires_refresh']and state['catalog_requires_refresh']and state['accepted_pages']==0
    for key in ['final_reminders','state_regression']:assert c['executions'][key]['exit_code']==0
    for p in (DEMO/'custom').glob('*.html'):assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
    print(json.dumps({'current_card_checks':66,'current_state_checks':110,'historical_initial_actions':752,'accepted_pages':0}))

if __name__=='__main__':main()
