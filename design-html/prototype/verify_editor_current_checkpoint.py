"""Source-bound editor competition, read markers and direct consumers; full acceptance pending."""
import json,hashlib
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,source
OUT=ROOT/'evidence/current';files=source();tests={}
counts={'editor-current-results.json':23,'shared-display-results.json':25,'record-controls-results.json':109,'record-reply-layout-results.json':10,'record-back-reentry-results.json':6,'moment-controls-results.json':55,'moment-reply-layout-results.json':5,'moment-flow-results.json':3,'moment-state-results.json':6,'derived-shared-results.json':19,'backup-scope-results.json':2,'product-journey-results.json':1,'time-product-journey-results.json':1}
metas=[json.loads((OUT/('editor-current-'+group+'-source.json')).read_text(encoding='utf-8'))for group in ['records','moments','shared']];assert all(v['files']==files for v in metas)
provenance={k:v for m in metas for k,v in m['reports'].items()};assert set(provenance)==set(counts)-{'editor-current-results.json'}
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
result=dict(scope='Diary, photo and moment editor competition and current reply read markers; all 114 pages acceptance pending',files=files,verified_at=datetime.now(timezone.utc).isoformat(),tests=tests,named_checks=sum(counts.values()),observations=228,observed_controls=runtime['controls_observed'],conditional_redirects=len(runtime['redirects']),http_pages=114,http_shared_assets=len(served)-114,accepted_pages=0)
assert result['named_checks']==265
(OUT/'editor-current-checkpoint.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:result[k]for k in ['named_checks','observations','observed_controls','conditional_redirects','http_pages','http_shared_assets','accepted_pages']}))
