"""Check declared operations, provenance and served bytes; no full acceptance claim."""
import json,hashlib
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,source
OUT=ROOT/'evidence/current';files=source();tests={};meta=json.loads((OUT/'backup-regression-source.json').read_text(encoding='utf-8'));assert meta['files']==files
counts={'backup-preservation-results.json':15,'backup-state-results.json':20,'backup-scope-results.json':2,'settings-controls-results.json':81,'settings-state-results.json':9,'settings-flow-results.json':5,'book-global-results.json':6,'pet-state-results.json':7,'recovery-archive-results.json':15,'account-recovery-results.json':20,'record-recovery-results.json':21}
for name,count in counts.items():
 p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));rows=v['results']if isinstance(v,dict)else v;assert len(rows)==count and all(r['passed']and not r['errors']for r in rows),name
 if isinstance(v,dict):assert v['files']==files,name
 digest=hashlib.sha256(p.read_bytes()).hexdigest()
 if name in meta['reports']:
  item=meta['reports'][name];assert item['exit_code']==0 and item['cases']==item['passed']==count and not item['errors']and item['sha256']==digest,name
 tests[name]=dict(cases=count,sha256=digest)
assert set(meta['reports'])==set(counts)-{'backup-preservation-results.json','backup-state-results.json','backup-scope-results.json'}
v=json.loads((OUT/'settings-controls-results.json').read_text(encoding='utf-8'));assert len(v['inventory'])==12 and {(r['page'],r['selector'])for r in v['results']}=={(item['page'],control['selector'])for item in v['inventory']for control in item['controls']}
runtime=json.loads((OUT/'current-runtime-summary.json').read_text(encoding='utf-8'));assert runtime['files']==files and runtime['observations']==228 and not runtime['errors']and not runtime['unbound_or_delegated_candidates']
served=[DEMO/'pages'/p.name for p in(DEMO/'custom').glob('*.html')]+list((DEMO/'assets').glob('prototype-*.*'))
for p in(DEMO/'custom').glob('*.html'):assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
def check(p):
 with urlopen('http://127.0.0.1:8765/'+p.relative_to(DEMO).as_posix(),timeout=15)as response:assert response.status==200 and response.read()==p.read_bytes()
with ThreadPoolExecutor(max_workers=6)as pool:list(pool.map(check,served))
queue=json.loads((ROOT/'queue.json').read_text(encoding='utf-8'));assert len(queue)==114 and not any(v.get('flow_verified')for v in queue);assert files==source()
result=dict(scope='Preservation of previous backup under declared source damage and backup failures; full product acceptance pending',files=files,tests=tests,named_checks=sum(counts.values()),observations=228,observed_controls=runtime['controls_observed'],conditional_redirects=len(runtime['redirects']),http_pages=114,http_shared_assets=len(served)-114,accepted_pages=0)
assert result['named_checks']==201
(OUT/'backup-preservation-checkpoint.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:result[k]for k in ['named_checks','observations','observed_controls','http_pages','http_shared_assets','accepted_pages']}))
