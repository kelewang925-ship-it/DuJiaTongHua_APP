"""Work state component, recovered-data refresh and current-source regression gate."""
import json,hashlib
from datetime import datetime,timezone
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
from verify_pet_controls import ROOT,DEMO,source
OUT=ROOT/'evidence/current';files=source();tests={};total=0
counts={'work-cancel-navigation-results.json':3,'work-error-results.json':30,'work-error-refresh-results.json':3,'workshop-recovery-results.json':18,'workshop-recovery-state-results.json':26,'workshop-controls-results.json':92,'workshop-hidden-results.json':12,'workshop-control-layout-results.json':10,'workshop-flow-results.json':3,'workshop-state-results.json':8,'product-journey-results.json':1}
meta=json.loads((OUT/'work-error-regression-source.json').read_text(encoding='utf-8'));assert meta['files']==files
for name,count in counts.items():
 p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));rows=v['results']if isinstance(v,dict)else v;assert len(rows)==count and all(r['passed']and not r['errors']for r in rows),name
 if isinstance(v,dict):assert v['files']==files,name
 digest=hashlib.sha256(p.read_bytes()).hexdigest()
 if name in meta['reports']:
  m=meta['reports'][name];assert m['exit_code']==0 and m['cases']==m['passed']==count and m['sha256']==digest and not m['errors'],name
 tests[name]=dict(cases=count,sha256=digest);total+=count
assert total==206
v=json.loads((OUT/'workshop-controls-results.json').read_text(encoding='utf-8'));assert len(v['inventory'])==10 and {(r['page'],r['selector'])for r in v['results']}=={(row['page'],c['selector'])for row in v['inventory']for c in row['controls']}
runtime=json.loads((OUT/'current-runtime-summary.json').read_text(encoding='utf-8'));assert runtime['files']==files and runtime['observations']==228 and runtime['requested_pages']==114 and not runtime['errors']and not runtime['unbound_or_delegated_candidates']
audit=json.loads((OUT/'remaining-collection-damage-observations.json').read_text(encoding='utf-8'));assert audit['files']==files and len(audit['results'])==36;assert {r['kind']for r in audit['results']}=={'moments','anniversaries','capsules','books','pet','tags'}
for p in(DEMO/'custom').glob('*.html'):assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
served=[DEMO/'pages'/p.name for p in(DEMO/'custom').glob('*.html')]+list((DEMO/'assets').glob('prototype-*.*'))
def verify(p):
 with urlopen('http://127.0.0.1:8765/'+p.relative_to(DEMO).as_posix(),timeout=15)as r:assert r.status==200 and r.read()==p.read_bytes(),p.name
with ThreadPoolExecutor(max_workers=6)as pool:list(pool.map(verify,served))
q=json.loads((ROOT/'queue.json').read_text(encoding='utf-8'));assert len(q)==114 and not any(r.get('flow_verified')for r in q);assert files==source()
checkpoint=dict(scope='Work error/empty component semantics and named refresh/controls/recovery regressions; other collection damage observed only and still open',files=files,verified_at=datetime.now(timezone.utc).isoformat(),fingerprint=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest(),tests=tests,named_checks=total,observations=228,observed_controls=runtime['controls_observed'],conditional_redirects=len(runtime['redirects']),remaining_collection_observations=36,remaining_collection_errors=sum(len(r['errors'])for r in audit['results']),http_pages=114,http_shared_assets=len(served)-114,accepted_pages=0)
(OUT/'work-error-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:checkpoint[k]for k in ['named_checks','observations','observed_controls','remaining_collection_observations','remaining_collection_errors','http_pages','http_shared_assets','accepted_pages']}),flush=True)
