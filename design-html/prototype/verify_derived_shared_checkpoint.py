"""Declared shared ancestry scope; complete 114-page acceptance remains pending."""
import json,hashlib
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,source
OUT=ROOT/'evidence/current';files=source();tests={}
counts={'derived-shared-results.json':17,'workshop-flow-results.json':3,'workshop-state-results.json':8,'pet-life-flow-results.json':4,'pet-life-state-results.json':12,'book-flow-results.json':4,'book-state-results.json':6,'book-global-results.json':6,'backup-preservation-results.json':15,'backup-state-results.json':20,'backup-scope-results.json':2,'capsule-semantic-results.json':17,'product-journey-results.json':1,'time-product-journey-results.json':1}
counts['derived-shared-results.json']=19
metas=[json.loads((OUT/('derived-shared-'+group+'-source.json')).read_text(encoding='utf-8'))for group in ['content','shared']];assert all(v['files']==files for v in metas)
provenance={k:v for m in metas for k,v in m['reports'].items()};assert set(provenance)==set(counts)-{'derived-shared-results.json'}
for name,count in counts.items():
 p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));rows=v['results']if isinstance(v,dict)else v;assert len(rows)==count and all(r['passed']and not r['errors']for r in rows),name
 if isinstance(v,dict):assert v['files']==files,name
 digest=hashlib.sha256(p.read_bytes()).hexdigest()
 if name in provenance:
  m=provenance[name];assert m['cases']==m['passed']==count and not m['errors']and m['exit_code']==0 and m['sha256']==digest,name
 tests[name]=dict(cases=count,sha256=digest)
runtime=json.loads((OUT/'current-runtime-summary.json').read_text(encoding='utf-8'));assert runtime['files']==files and runtime['observations']==228 and runtime['requested_pages']==114 and not runtime['errors']and not runtime['unbound_or_delegated_candidates']
served=[DEMO/'pages'/p.name for p in(DEMO/'custom').glob('*.html')]+list((DEMO/'assets').glob('prototype-*.*'))
for p in(DEMO/'custom').glob('*.html'):assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
def check(p):
 with urlopen('http://127.0.0.1:8765/'+p.relative_to(DEMO).as_posix(),timeout=15)as response:assert response.status==200 and response.read()==p.read_bytes(),p.name
with ThreadPoolExecutor(max_workers=6)as pool:list(pool.map(check,served))
q=json.loads((ROOT/'queue.json').read_text(encoding='utf-8'));assert len(q)==114 and not any(r.get('flow_verified')for r in q);assert source()==files
result=dict(scope='Current capsule ancestry in shared catalogs/backup/book/pet plus generation and album publication; full product acceptance pending',files=files,verified_at=datetime.now(timezone.utc).isoformat(),tests=tests,named_checks=sum(counts.values()),observations=228,observed_controls=runtime['controls_observed'],conditional_redirects=len(runtime['redirects']),http_pages=114,http_shared_assets=len(served)-114,accepted_pages=0)
assert result['named_checks']==118
(OUT/'derived-shared-checkpoint.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:result[k]for k in ['named_checks','observations','observed_controls','conditional_redirects','http_pages','http_shared_assets','accepted_pages']}))
