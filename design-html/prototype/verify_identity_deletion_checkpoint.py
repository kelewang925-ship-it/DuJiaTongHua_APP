"""Verify the current phase without promoting historical full-suite evidence."""
import hashlib,json
from verify_pet_controls import ROOT,source
from verify_identity_deletions import SPECS,MODES

out=ROOT/'evidence/current';checkpoint=json.loads((out/'identity-deletion-checkpoint.json').read_text(encoding='utf-8'))
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert checkpoint['files']==source()
for name,value in checkpoint['reports'].items():assert digest(out/name)==value,name
for name,value in checkpoint['scripts'].items():assert digest(ROOT/name)==value,name
for name,value in checkpoint['baselines'].items():assert digest(ROOT/'evidence/baseline'/name)==value,name
report=json.loads((out/'identity-deletion-results.json').read_text(encoding='utf-8'));assert report['files']==source()
assert len(report['results'])==report['expected_cases']==13
assert {(r['observation_index'],r['mode'])for r in report['results']}=={(i,m)for i in SPECS for m in MODES+(['quota-late-retry']if i==59 else[])}
assert all(r['passed']and not r['errors']for r in report['results'])
runtime=json.loads((out/'current-runtime-summary.json').read_text(encoding='utf-8'));assert runtime['files']==source()and not runtime['errors']
catalog=json.loads((out/'page-contracts.json').read_text(encoding='utf-8'));assert catalog['files']==source()
current=sum(c['status']=='当前源码通过'for p in catalog['pages']for c in p['control_evidence'])
assert current==163
assert sum(len(p['control_evidence'])for p in catalog['pages'])-current==589
assert all(e['exit_code']==0 for e in checkpoint['executions'].values())
assert checkpoint['accepted_pages']==0
print(json.dumps(dict(identity_cases=13,current_initial_controls=163,historical_initial_controls=589,observations=228,accepted_pages=0)))
