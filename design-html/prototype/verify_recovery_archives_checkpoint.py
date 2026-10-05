"""Verify archive history's scoped evidence; do not upgrade the last full-page scan."""
from pathlib import Path
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'prototype/evidence/current'
archive=json.loads((OUT/'recovery-archive-results.json').read_text(encoding='utf-8'));files=archive['files']
for path,digest in files.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
recovery=json.loads((OUT/'record-recovery-source.json').read_text(encoding='utf-8'));assert recovery['files']==files
expected={'recovery-archive-results.json':15,'record-recovery-results.json':21,'settings-flow-results.json':5};tests={}
for name,count in expected.items():
    p=OUT/name;value=json.loads(p.read_text(encoding='utf-8'));rows=value['results'] if isinstance(value,dict) else value
    assert len(rows)==count and all(row['passed'] and not row.get('errors') for row in rows),name
    tests[name]={'checks':count,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
paths=[f'pages/{p.name}' for p in sorted((ROOT/'custom').glob('*.html'))]+[path for path in files if path.startswith('assets/')]
def served(path):
    with urlopen('http://127.0.0.1:8765/'+path,timeout=15) as response:assert response.status==200 and response.read()==(ROOT/path).read_bytes(),path
with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(served,paths))
queue_path=ROOT/'prototype/queue.json';queue=json.loads(queue_path.read_text(encoding='utf-8'));assert len(queue)==114 and not any(row['flow_verified'] for row in queue)
next(row for row in queue if row['id']=='m06-p11')['recovery_archive_evidence']='evidence/current/recovery-archive-results.json'
queue_path.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
previous=json.loads((OUT/'current-runtime-summary.json').read_text(encoding='utf-8'))
checkpoint={'scope':'Archive download history, existing recovery and settings regression only; last full scan remains a previous source snapshot.','files':files,'tests':tests,'named_checks':41,'http_files_matching_checkout':len(paths),'accepted_pages':0,'last_full_observation_matches_current_source':previous['files']==files}
(OUT/'recovery-archive-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({key:checkpoint[key] for key in ['named_checks','http_files_matching_checkout','accepted_pages','last_full_observation_matches_current_source']},ensure_ascii=False),flush=True)
