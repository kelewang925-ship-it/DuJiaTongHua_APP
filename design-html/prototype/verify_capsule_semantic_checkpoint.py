"""Bounded capsule semantics and declared regressions; whole product acceptance pending."""
import json,hashlib
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,source
OUT=ROOT/'evidence/current';files=source();tests={}
counts={'capsule-semantic-results.json':17,'capsule-current-action-results.json':5,'collection-recovery-entry-results.json':15,'time-controls-results.json':54,'time-collection-results.json':7,'time-layout-results.json':20,'capsule-flow-results.json':3,'capsule-state-results.json':5,'anniversary-flow-results.json':3,'anniversary-state-results.json':7,'moment-flow-results.json':3,'moment-state-results.json':6,'anniversary-date-recovery-results.json':1,'pet-book-recovery-results.json':24,'pet-book-recovery-state-results.json':26,'time-collection-recovery-results.json':36,'time-collection-state-results.json':46,'backup-preservation-results.json':15,'backup-state-results.json':20,'backup-scope-results.json':2,'recovery-archive-results.json':15,'book-global-results.json':6,'product-journey-results.json':1,'time-product-journey-results.json':1}
counts['capsule-date-pending-results.json']=3
metas=[json.loads((OUT/('capsule-semantic-'+group+'-source.json')).read_text(encoding='utf-8'))for group in ['business','shared']];assert all(m['files']==files for m in metas)
provenance={k:v for m in metas for k,v in m['reports'].items()};assert set(provenance)==set(counts)-{'capsule-semantic-results.json','capsule-current-action-results.json','collection-recovery-entry-results.json','capsule-date-pending-results.json'}
for name,count in counts.items():
 p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));rows=v['results']if isinstance(v,dict)else v;assert len(rows)==count and all(r['passed']and not r['errors']for r in rows),name
 if isinstance(v,dict):assert v['files']==files,name
 digest=hashlib.sha256(p.read_bytes()).hexdigest()
 if name in provenance:
  m=provenance[name];assert m['cases']==m['passed']==count and not m['errors']and m['sha256']==digest,name
  if m.get('revalidated_bound_report'):assert m['exit_code']is None and isinstance(v,dict)and v['files']==files,name
  else:assert m['exit_code']==0,name
 tests[name]=dict(cases=count,sha256=digest)
v=json.loads((OUT/'time-controls-results.json').read_text(encoding='utf-8'));assert len(v['inventory'])==11 and {(r['page'],r['selector'])for r in v['results']}=={(v['page'],c['selector'])for v in v['inventory']for c in v['controls']}
v=json.loads((OUT/'capsule-semantic-results.json').read_text(encoding='utf-8'));layouts=[r for r in v['results']if r['case'].startswith('layout-')];assert {r['width']for r in layouts}=={320,360,390,414,430}and all(r['safe_area_simulated']for r in layouts)
runtime=json.loads((OUT/'current-runtime-summary.json').read_text(encoding='utf-8'));assert runtime['files']==files and runtime['observations']==228 and runtime['requested_pages']==114 and not runtime['errors']and not runtime['unbound_or_delegated_candidates']
served=[DEMO/'pages'/p.name for p in(DEMO/'custom').glob('*.html')]+list((DEMO/'assets').glob('prototype-*.*'))
for p in(DEMO/'custom').glob('*.html'):assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
def check(p):
 with urlopen('http://127.0.0.1:8765/'+p.relative_to(DEMO).as_posix(),timeout=15)as response:assert response.status==200 and response.read()==p.read_bytes(),p.name
with ThreadPoolExecutor(max_workers=6)as pool:list(pool.map(check,served))
q=json.loads((ROOT/'queue.json').read_text(encoding='utf-8'));assert len(q)==114 and not any(r.get('flow_verified')for r in q);assert source()==files
result=dict(scope='Sealed capsule date correction, current action gates, collection identity/privacy and recovery entry deduplication plus declared regressions; full acceptance pending',files=files,verified_at=datetime.now(timezone.utc).isoformat(),tests=tests,named_checks=sum(counts.values()),observations=228,observed_controls=runtime['controls_observed'],conditional_redirects=len(runtime['redirects']),http_pages=114,http_shared_assets=len(served)-114,accepted_pages=0)
assert result['named_checks']==341
(OUT/'capsule-semantic-checkpoint.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:result[k]for k in ['named_checks','observations','observed_controls','conditional_redirects','http_pages','http_shared_assets','accepted_pages']}))
