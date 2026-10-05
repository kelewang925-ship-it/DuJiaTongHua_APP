"""Verify the named records batch evidence and running checkout, not full acceptance."""
from pathlib import Path
from urllib.request import urlopen
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'prototype/evidence/current'
expected={'diary-flow-results.json':4,'diary-state-results.json':12,'home-diary-results.json':3,'records-layout-results.json':40}
tests={}
for name,count in expected.items():
 p=OUT/name;rows=json.loads(p.read_text(encoding='utf-8'));assert len(rows)==count,(name,len(rows));assert all(r['passed'] for r in rows),name
 tests[name]={'cases':count,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
layout=json.loads((OUT/'records-layout-results.json').read_text(encoding='utf-8'))
assert {(r['page'],r['width']) for r in layout}=={(f'm03-p{n:02}',w) for n in range(1,9) for w in [320,375,390,414,430]}
assert all(r['safe_top']==44 and r['safe_bottom']==34 and r['reduced_motion'] for r in layout)
manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'));assert len(manifest)==114
for item in manifest:
 path=f'pages/{item["id"]}.html'
 with urlopen('http://127.0.0.1:8765/'+path,timeout=10) as response:assert response.status==200 and response.read()==(ROOT/path).read_bytes(),path
files=set(ROOT.glob('assets/prototype-*'))
for n in range(1,9):
 source=ROOT/'custom'/f'm03-p{n:02}.html';rendered=ROOT/'pages'/source.name;assert source.read_bytes()==rendered.read_bytes(),source.name;files.update([source,rendered])
 for asset in re.findall(r'\.\./assets/([\w.-]+)',source.read_text(encoding='utf-8')):files.add(ROOT/'assets'/asset)
for file in sorted(files):
 path=file.relative_to(ROOT).as_posix()
 with urlopen('http://127.0.0.1:8765/'+path,timeout=10) as response:assert response.read()==file.read_bytes(),path
report={'scope':'Partial records batch only: home/search/diary; photo and full 114 acceptance pending','tests':tests,'http_pages_matching_checkout':114,'files':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}}
(OUT/'records-checkpoint.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Verified records batch: 59 named checks, all 114 served pages match checkout, source/render pairs and consumed assets match')
