from pathlib import Path
from urllib.request import urlopen
import json,hashlib,re

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'prototype/evidence/current';tests={}
for name,count in {'book-extended-results.json':7,'book-layout-results.json':105,'book-image-variant-results.json':10,'book-flow-results.json':4,'book-state-results.json':6}.items():
 file=OUT/name;rows=json.loads(file.read_text(encoding='utf-8'));assert len(rows)==count and all(v['passed'] for v in rows),name;tests[name]={'count':count,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()}
rows=json.loads((OUT/'book-layout-results.json').read_text(encoding='utf-8'));assert {(v['page'],v['width']) for v in rows}=={(f'm08-p{n:02}',w) for n in range(1,22) for w in [320,375,390,414,430]}
baseline=json.loads((ROOT/'prototype/evidence/baseline/book-extended-results.json').read_text(encoding='utf-8'));assert len(baseline)==3 and not any(v['passed'] for v in baseline)
files={p for p in ROOT.glob('assets/prototype-book*') if p.is_file()}
for n in range(1,22):
 source=ROOT/'custom'/f'm08-p{n:02}.html';page=ROOT/'pages'/source.name;assert source.read_bytes()==page.read_bytes(),source.name
 assert source.read_text(encoding='utf-8').count('prototype-book-editors.js')==1;files.update([source,page]);files.update(ROOT/'assets'/a for a in re.findall(r'\.\./assets/([\w.-]+)',source.read_text(encoding='utf-8')))
manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'));assert len(manifest)==114
for item in manifest:
 file=ROOT/'pages'/f'{item["id"]}.html'
 with urlopen('http://127.0.0.1:8765/pages/'+file.name,timeout=10) as response:assert response.status==200 and response.read()==file.read_bytes(),file
for file in sorted(files):
 with urlopen('http://127.0.0.1:8765/'+file.relative_to(ROOT).as_posix(),timeout=10) as response:assert response.read()==file.read_bytes(),file
queue=json.loads((ROOT/'prototype/queue.json').read_text(encoding='utf-8'));assert len(queue)==114 and not any(v['flow_verified'] for v in queue);assert all(v['status'].startswith('partial-implemented') for v in queue)
report={'scope':'All book controllers connected; named checks only; book multi-source/editor/structure/global integration and full product acceptance pending','tests':tests,'http_pages_matching_checkout':114,'partial_implemented':114,'final_accepted':0,'files':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}}
(OUT/'book-extended-checkpoint.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Book module: 132 named checks; 114 HTTP pages match; 114 partial / zero final accepted')
