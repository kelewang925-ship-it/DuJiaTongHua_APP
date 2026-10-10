"""Verify current Loading evidence and keep older initial actions explicitly historical."""
import hashlib,json
from verify_pet_controls import ROOT,DEMO,source

def main():
    out=ROOT/'evidence/current';checkpoint=json.loads((out/'shared-list-loading-checkpoint.json').read_bytes());files=source()
    assert checkpoint['files']==files and checkpoint['accepted_pages']==0
    for name,digest in checkpoint['artifacts'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    for name,count in [('shared-list-loading-results.json',30),('shared-loading-widths.json',50)]:
        report=json.loads((out/name).read_bytes());assert report['files']==files and len(report['results'])==count
        assert all(row['passed']and not row['errors']for row in report['results'])
    width=json.loads((out/'shared-loading-widths.json').read_bytes())
    assert len({(r['page'],r['width'])for r in width['results']})==50
    assert {r['width']for r in width['results']}=={320,360,390,414,430}
    runtime=json.loads((out/'current-runtime-summary.json').read_bytes());assert runtime['files']==files and runtime['observations']==228 and not runtime['errors']and not runtime['unbound_or_delegated_candidates']
    catalog=json.loads((out/'page-contracts.json').read_bytes());assert catalog['files']==files
    current=sum(c['status']=='当前源码通过'for p in catalog['pages']for c in p['control_evidence'])
    historical=sum(c['status']=='历史通过／待当前复验'for p in catalog['pages']for c in p['control_evidence'])
    assert current==0 and historical==752
    state=json.loads((out/'current-evidence-state.json').read_bytes());assert state['files']==files and state['historical_initial_controls']==historical and state['current_initial_controls']==current
    for key in ['final_behavior','final_widths','final_runtime']:assert checkpoint['executions'][key]['exit_code']==0
    shared=json.loads((ROOT/'evidence/history/pre-shared-list-loading-6284939/component-coverage-observations.json').read_bytes())['shared_stylesheets']
    for name,digest in shared.items():assert hashlib.sha256((DEMO/name).read_bytes()).hexdigest()==digest
    print(json.dumps({'current_loading_checks':80,'runtime_observations':228,'historical_initial_actions':752,'accepted_pages':0}))

if __name__=='__main__':main()
