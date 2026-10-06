"""Verify scoped session/invite evidence; older full-page observations stay historical."""
from pathlib import Path
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'prototype/evidence/current'
report=json.loads((OUT/'session-invite-results.json').read_text(encoding='utf-8'));files=report['files']
for path,digest in files.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
expected={'session-invite-results.json':15,'account-recovery-results.json':20,'onboarding-flow-results.json':8,'new-user-journey-results.json':2,'settings-flow-results.json':5};tests={}
for name,count in expected.items():
    p=OUT/name;result=json.loads(p.read_text(encoding='utf-8'));rows=result['results'] if isinstance(result,dict) else result
    assert len(rows)==count and all(row['passed'] and not row.get('errors') for row in rows),name
    if isinstance(result,dict):assert result['files']==files,name
    tests[name]={'checks':count,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
paths=[f'pages/{p.name}' for p in sorted((ROOT/'custom').glob('*.html'))]+[path for path in files if path.startswith('assets/')]
def served(path):
    with urlopen('http://127.0.0.1:8765/'+path,timeout=15) as r:assert r.status==200 and r.read()==(ROOT/path).read_bytes(),path
    if path.startswith('pages/'):assert (ROOT/path).read_bytes()==(ROOT/'custom'/Path(path).name).read_bytes(),path
with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(served,paths))
queue=json.loads((ROOT/'prototype/queue.json').read_text(encoding='utf-8'));assert len(queue)==114 and not any(row['flow_verified'] for row in queue)
fingerprint=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest()
checkpoint={'scope':'Session/invite recovery, OTP integrity/purpose/expiry, five error-state widths and specified normal regressions only. Prior 114-page observations and 82+14 control execution remain historical; no final product acceptance.','source_fingerprint':fingerprint,'files':files,'tests':tests,'named_checks':sum(t['checks'] for t in tests.values()),'http_pages':114,'http_shared_assets':37,'accepted_pages':0}
(OUT/'session-invite-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:checkpoint[k] for k in ['named_checks','http_pages','http_shared_assets','accepted_pages']}),flush=True)
