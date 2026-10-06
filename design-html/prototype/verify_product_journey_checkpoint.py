"""Scope-bound eight-module journey, source observation and served-byte checkpoint."""
import json,hashlib,re
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
from verify_pet_controls import ROOT,DEMO,source
OUT=ROOT/'evidence/current';files=source();tests={};total=0
for name,count in [('product-journey-results.json',1),('workshop-task-return-results.json',4),('book-created-date-results.json',5),('home-counter-results.json',6)]:
 p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));assert v['files']==files and len(v['results'])==count and all(r['passed'] and not r['errors'] for r in v['results']),name;tests[name]=dict(cases=count,sha256=hashlib.sha256(p.read_bytes()).hexdigest());total+=count
journey=json.loads((OUT/'product-journey-results.json').read_text(encoding='utf-8'))['results'][0];modules={m.group(1)for u in journey['navigations']if(m:=re.search(r'/pages/(m\d{2})-p',u))};assert modules=={'m'+str(i).zfill(2)for i in range(1,9)}
assert {'book-published','book-real-export','logout-kept-content','relogin-content-retained','book-deleted-sources-retained'}<={s['step']for s in journey['steps']}
meta=json.loads((OUT/'product-journey-regression-source.json').read_text(encoding='utf-8'));assert meta['files']==files
for name,count in [('workshop-flow-results.json',3),('workshop-state-results.json',8),('book-global-results.json',6)]:
 p=OUT/name;rows=json.loads(p.read_text(encoding='utf-8'));v=meta['reports'][name];assert len(rows)==count and all(r['passed']and not r['errors']for r in rows)and v['exit_code']==0 and v['sha256']==hashlib.sha256(p.read_bytes()).hexdigest(),name;tests[name]=v;total+=count
assert total==33
runtime=json.loads((OUT/'current-runtime-summary.json').read_text(encoding='utf-8'));inventory=json.loads((OUT/'current-runtime-inventory.json').read_text(encoding='utf-8'));assert runtime['files']==files and runtime['requested_pages']==114 and runtime['observations']==228 and not runtime['errors']and not runtime['unbound_or_delegated_candidates'];assert len(inventory)==228 and len({r['id']for r in inventory})==114 and all(len([r for r in inventory if r['id']==id and r['scenario']==s])==1 for id in {r['id']for r in inventory}for s in ['empty','populated'])
for p in (DEMO/'custom').glob('*.html'):assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
served=[DEMO/'pages'/p.name for p in (DEMO/'custom').glob('*.html')]+list((DEMO/'assets').glob('prototype-*.*'))
def verify(p):
 with urlopen('http://127.0.0.1:8765/'+p.relative_to(DEMO).as_posix(),timeout=15)as r:assert r.status==200 and r.read()==p.read_bytes(),p.name
with ThreadPoolExecutor(max_workers=6)as pool:list(pool.map(verify,served))
queue=json.loads((ROOT/'queue.json').read_text(encoding='utf-8'));assert len(queue)==114 and not any(r.get('flow_verified')for r in queue)
fingerprint=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest();checkpoint=dict(scope='One continuous eight-module local journey plus targeted regressions; full-product final acceptance pending',files=files,fingerprint=fingerprint,tests=tests,named_checks=total,modules=sorted(modules),observations=228,observed_controls=runtime['controls_observed'],conditional_redirects=len(runtime['redirects']),observation_only=True,runtime_sha256=hashlib.sha256((OUT/'current-runtime-inventory.json').read_bytes()).hexdigest(),summary_sha256=hashlib.sha256((OUT/'current-runtime-summary.json').read_bytes()).hexdigest(),http_pages=114,http_shared_assets=len(served)-114,accepted_pages=0)
(OUT/'product-journey-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:checkpoint[k]for k in ['named_checks','observations','conditional_redirects','http_pages','http_shared_assets','accepted_pages']}),flush=True)
