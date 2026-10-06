"""Book exact control coverage, provenance, and served bytes."""
import json,hashlib
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
from verify_book_controls import ROOT,DEMO,source
OUT=ROOT/'evidence/current';files=source();report=json.loads((OUT/'book-controls-results.json').read_text(encoding='utf-8'));assert report['files']==files
assert len(report['inventory'])==21 and len(report['results'])==154
assert {(r['page'],r['selector'])for r in report['results']}=={(e['page'],v['selector'])for e in report['inventory']for v in e['controls']}
tests={};total=0
for name,count in [('book-controls-results.json',154),('book-control-return-results.json',2),('book-control-layout-results.json',15)]:
    p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));assert v['files']==files and len(v['results'])==count and all(r['passed']and not r['errors']for r in v['results']),name;total+=count;tests[name]=dict(cases=count,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
v=json.loads((OUT/'book-control-layout-results.json').read_text(encoding='utf-8'));assert {(r['kind'],r['width'])for r in v['results']}=={(k,w)for k in ['supplement','editor','rename']for w in [320,360,390,414,430]}
meta=json.loads((OUT/'book-control-regression-source.json').read_text(encoding='utf-8'));assert meta['files']==files
for name,count in [('book-flow-results.json', 4), ('book-state-results.json', 6), ('book-extended-results.json', 7), ('book-structure-results.json', 5), ('book-cover-results.json', 4), ('book-global-results.json', 6), ('book-editor-draft-results.json', 7)]:
    p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));r=meta['reports'][name];assert len(v)==count and all(row['passed']and not row['errors']for row in v)and r['exit_code']==0 and r['sha256']==hashlib.sha256(p.read_bytes()).hexdigest(),name;tests[name]=r;total+=count
assert total==210
for p in (DEMO/'custom').glob('*.html'):assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
served=[DEMO/'pages'/p.name for p in (DEMO/'custom').glob('*.html')]+list((DEMO/'assets').glob('prototype-*.*'))
def verify(p):
    with urlopen('http://127.0.0.1:8765/'+p.relative_to(DEMO).as_posix(),timeout=15)as r:assert r.status==200 and r.read()==p.read_bytes(),p.name
with ThreadPoolExecutor(max_workers=6)as pool:list(pool.map(verify,served))
queue=json.loads((ROOT/'queue.json').read_text(encoding='utf-8'));entries=queue if isinstance(queue,list)else queue['pages'];assert len(entries)==114 and not any(v.get('flow_verified')for v in entries)
fingerprint=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest();checkpoint=dict(scope='Twenty-one book fixtures and supplement return; full-product acceptance pending',files=files,fingerprint=fingerprint,tests=tests,named_checks=total,initial_controls=154,http_pages=114,http_shared_assets=len(served)-114,accepted_pages=0)
(OUT/'book-controls-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

print(json.dumps({k:checkpoint[k] for k in ['named_checks','initial_controls','http_pages','http_shared_assets','accepted_pages']}),flush=True)
