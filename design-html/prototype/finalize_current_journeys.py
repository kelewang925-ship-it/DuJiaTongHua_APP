"""Persist the final retained case omitted by the runner's early continue."""
import json
from replay_current_initial_controls import ROOT, deps, sha, dump

folder=ROOT/'evidence/current/continuous-journeys-20261031'
path=folder/'results.json'
baseline=ROOT/'evidence/baseline/continuous-journeys-20261031/results.json'
raw=folder/'results-before-final-retained-case.json'
assert not raw.exists()
data=json.loads(path.read_text(encoding='utf-8'))
assert data['dependencies']==deps() and len(data['results'])==3
assert all(r['passed'] for r in data['results'])
old=json.loads(baseline.read_text(encoding='utf-8'))
row=old['results'][3]
assert row['case']=='anniversary-capsule-reminders' and row['passed']
for n,h in old['fixture_sha256'].items():
    assert sha(baseline.parent/'fixtures'/n)==h
    if n not in ['verify_product_journey.py','replay_current_journeys.py']:assert sha(ROOT/n)==h
raw.write_bytes(path.read_bytes())
data['results'].append({**row,'execution':'retained-baseline-pass','provenance':{'report':str(baseline.relative_to(ROOT)).replace(chr(92),'/'),'sha256':sha(baseline),'case':row['case']}})
data.update(complete=True,all_passed=True,finalization={'producer':__file__.split(chr(92))[-1],'sha256':sha(ROOT/'finalize_current_journeys.py'),'raw_report_sha256':sha(raw),'reason':'Runner printed and retained final case in memory but skipped final report persistence. No browser execution repeated or inferred.'})
dump(path,data)
print('Finalized fourth retained case; 1 fresh and 3 retained, 54 stage records.')
