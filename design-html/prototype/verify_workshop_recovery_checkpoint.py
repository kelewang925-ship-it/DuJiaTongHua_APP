"""Current work recovery, exact control execution, regression, runtime and HTTP gate."""
import json,hashlib
from datetime import datetime,timezone
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
from verify_pet_controls import ROOT,DEMO,source
OUT=ROOT/'evidence/current';files=source();tests={};total=0
counts={'workshop-recovery-results.json':18,'workshop-recovery-state-results.json':26,'workshop-controls-results.json':92,'workshop-hidden-results.json':12,'workshop-control-layout-results.json':10,'workshop-flow-results.json':3,'workshop-state-results.json':8,'account-recovery-results.json':20,'record-recovery-results.json':21,'settings-sheet-guard-results.json':11,'danger-confirmation-results.json':18,'book-global-results.json':6,'product-journey-results.json':1,'time-product-journey-results.json':1}
meta=json.loads((OUT/'workshop-recovery-regression-source.json').read_text(encoding='utf-8'));assert meta['files']==files
for name,count in counts.items():
 p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));rows=v['results']if isinstance(v,dict)else v;assert len(rows)==count and all(r['passed']and not r['errors']for r in rows),name
 if isinstance(v,dict):assert v['files']==files,name
 digest=hashlib.sha256(p.read_bytes()).hexdigest()
 if name in meta['reports']:
  m=meta['reports'][name];assert m['exit_code']==0 and m['cases']==m['passed']==count and m['sha256']==digest and not m['errors'],name
 tests[name]=dict(cases=count,sha256=digest);total+=count
assert total==247
control=json.loads((OUT/'workshop-controls-results.json').read_text(encoding='utf-8'));assert len(control['inventory'])==10;assert {(r['page'],r['selector'])for r in control['results']}=={(entry['page'],v['selector'])for entry in control['inventory']for v in entry['controls']}
runtime=json.loads((OUT/'current-runtime-summary.json').read_text(encoding='utf-8'));inventory=json.loads((OUT/'current-runtime-inventory.json').read_text(encoding='utf-8'));assert runtime['files']==files and runtime['requested_pages']==114 and runtime['observations']==228 and not runtime['errors']and not runtime['unbound_or_delegated_candidates'];assert len(inventory)==228 and len({r['id']for r in inventory})==114
for p in(DEMO/'custom').glob('*.html'):assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
served=[DEMO/'pages'/p.name for p in(DEMO/'custom').glob('*.html')]+list((DEMO/'assets').glob('prototype-*.*'))
def verify(p):
 with urlopen('http://127.0.0.1:8765/'+p.relative_to(DEMO).as_posix(),timeout=15)as r:assert r.status==200 and r.read()==p.read_bytes(),p.name
with ThreadPoolExecutor(max_workers=6)as pool:list(pool.map(verify,served))
q=json.loads((ROOT/'queue.json').read_text(encoding='utf-8'));assert len(q)==114 and not any(r.get('flow_verified')for r in q);assert files==source()
checkpoint=dict(scope='Work collection structural recovery, all ten work states/declared controls and named business/guard regressions; other collections and full acceptance pending',verified_at=datetime.now(timezone.utc).isoformat(),files=files,fingerprint=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest(),tests=tests,named_checks=total,initial_workshop_controls=92,observations=228,observed_controls=runtime['controls_observed'],conditional_redirects=len(runtime['redirects']),runtime_sha256=hashlib.sha256((OUT/'current-runtime-inventory.json').read_bytes()).hexdigest(),http_pages=114,http_shared_assets=len(served)-114,accepted_pages=0)
(OUT/'workshop-recovery-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:checkpoint[k]for k in ['named_checks','observations','observed_controls','conditional_redirects','http_pages','http_shared_assets','accepted_pages']}),flush=True)
