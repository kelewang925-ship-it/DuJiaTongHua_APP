"""Validate terminal replay provenance and regenerated initial-control catalog."""
import hashlib
import json
from verify_pet_controls import ROOT, source

out = ROOT / 'evidence/current'
files = source()
meta = json.loads((out / 'initial-controls-refresh-source.json').read_text(encoding='utf-8'))
expected = {'time': 54, 'workshop': 92, 'settings': 81, 'pet': 151, 'book': 154}
assert meta['files'] == files
assert set(meta['reports']) == {f'{name}-controls-results.json' for name in expected}
for name, count in expected.items():
    filename = f'{name}-controls-results.json'
    execution = meta['reports'][filename]
    raw = (out / filename).read_bytes()
    report = json.loads(raw)
    assert execution['exit_code'] == 0 and execution['source_current']
    assert execution['expected_cases'] == execution['cases'] == execution['passed'] == count
    assert not execution['errors']
    assert execution['sha256'] == hashlib.sha256(raw).hexdigest()
    assert report['files'] == files and len(report['results']) == count
    assert all(row['passed'] and not row['errors'] for row in report['results'])
catalog = json.loads((out / 'page-contracts.json').read_text(encoding='utf-8'))
assert catalog['files'] == files
rows = [row for page in catalog['pages'] for row in page['control_evidence']]
assert len(rows) == 752 and all(row['status'] == '当前源码通过' for row in rows)
assert source() == files
checkpoint = dict(files=files, newly_replayed=sum(expected.values()), current_initial_controls=len(rows), historical_initial_controls=0, pages=114, accepted_pages=0, reports=meta['reports'])
(out / 'initial-controls-refresh-checkpoint.json').write_text(json.dumps(checkpoint, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({key: value for key, value in checkpoint.items() if key not in ('files', 'reports')}))
