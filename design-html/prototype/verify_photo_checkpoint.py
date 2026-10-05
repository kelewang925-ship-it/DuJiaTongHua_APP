"""Photo batch proof and HTTP snapshot; does not certify all 114 interactions."""
from pathlib import Path
from urllib.request import urlopen
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'prototype/evidence/current'
counts={'photo-flow-results.json':3,'photo-state-results.json':4,'photo-layout-results.json':20,'diary-state-results.json':12,'home-diary-results.json':3};tests={}
for name,count in counts.items():
 file=OUT/name;rows=json.loads(file.read_text(encoding='utf-8'));assert len(rows)==count and all(r['passed'] for r in rows),name;tests[name]={'cases':count,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()}
layout=json.loads((OUT/'photo-layout-results.json').read_text(encoding='utf-8'));assert {(r['page'],r['width']) for r in layout}=={(f'm03-p{n:02}',w) for n in range(9,13) for w in [320,375,390,414,430]}
files=set(ROOT.glob('assets/prototype-*'))
for n in range(1,13):
 source=ROOT/'custom'/f'm03-p{n:02}.html';page=ROOT/'pages'/source.name;assert source.read_bytes()==page.read_bytes(),source.name;files.update([source,page]);files.update(ROOT/'assets'/a for a in re.findall(r'\.\./assets/([\w.-]+)',source.read_text(encoding='utf-8')))
manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'));assert len(manifest)==114
for item in manifest:
 path=f'pages/{item["id"]}.html'
 with urlopen('http://127.0.0.1:8765/'+path,timeout=10) as response:assert response.status==200 and response.read()==(ROOT/path).read_bytes(),path
for file in sorted(files):
 with urlopen('http://127.0.0.1:8765/'+file.relative_to(ROOT).as_posix(),timeout=10) as response:assert response.read()==file.read_bytes(),file
report={'scope':'Photo named scenarios with diary/search regression; final 114-page acceptance pending','tests':tests,'http_pages_matching_checkout':114,'files':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}}
(OUT/'photo-checkpoint.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Photo checkpoint: 27 photo checks + 15 diary/search regression checks; 114 HTTP pages match checkout')
