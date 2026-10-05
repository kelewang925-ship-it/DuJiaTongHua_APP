from pathlib import Path
from urllib.request import urlopen
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'prototype/evidence/current';tests={}
for name,count in {'pet-flow-results.json':3,'pet-state-results.json':7,'pet-layout-results.json':55,'settings-flow-results.json':5,'settings-state-results.json':9}.items():
 file=OUT/name;rows=json.loads(file.read_text(encoding='utf-8'));assert len(rows)==count and all(r['passed'] for r in rows),name;tests[name]={'cases':count,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()}
rows=json.loads((OUT/'pet-layout-results.json').read_text(encoding='utf-8'));assert {(r['page'],r['width']) for r in rows}=={(f'm07-p{n:02}',w) for n in range(1,12) for w in [320,360,390,414,431]}
files=set(ROOT.glob('assets/prototype-*'));files.add(ROOT/'prototype/review.html')
for n in range(1,12):
 source=ROOT/'custom'/f'm07-p{n:02}.html';page=ROOT/'pages'/source.name;assert source.read_bytes()==page.read_bytes(),source.name;files.update([source,page]);files.update(ROOT/'assets'/a for a in re.findall(r'\.\./assets/([\w.-]+)',source.read_text(encoding='utf-8')))
manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'));assert len(manifest)==114
for item in manifest:
 file=ROOT/'pages'/f'{item["id"]}.html'
 with urlopen('http://127.0.0.1:8765/pages/'+file.name,timeout=10) as response:assert response.status==200 and response.read()==file.read_bytes(),file.name
for file in sorted(files):
 with urlopen('http://127.0.0.1:8765/'+file.relative_to(ROOT).as_posix(),timeout=10) as response:assert response.read()==file.read_bytes(),file
queue=json.loads((ROOT/'prototype/queue.json').read_text(encoding='utf-8'));assert len(queue)==114 and not any(v['flow_verified'] for v in queue)
report={'scope':'Pet care first eleven pages: named checks and settings regression only; fourteen pet pages, twenty-one book pages and full acceptance pending','tests':tests,'http_pages_matching_checkout':114,'partial_implemented':sum(v['status'].startswith('partial-implemented') for v in queue),'final_accepted':0,'files':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}}
(OUT/'pet-checkpoint.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Pet care checkpoint: 65 named checks and 14 settings regression checks pass; 114 HTTP pages match; 79 partial / 0 final accepted')
