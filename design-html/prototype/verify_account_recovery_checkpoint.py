"""Verify typed identity recovery and named regressions against current served source."""
from pathlib import Path
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'prototype/evidence/current'
account=json.loads((OUT/'account-recovery-results.json').read_text(encoding='utf-8'));files=account['files']
report=json.loads((OUT/'current-runtime-summary.json').read_text(encoding='utf-8'))
assert files==report['files'] and report['observations']==228 and not report['errors'] and not report['unbound_or_delegated_candidates']
for path,digest in files.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
fingerprint=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest()
expected={'account-recovery-results.json':20,'onboarding-flow-results.json':8,'new-user-journey-results.json':2,'settings-flow-results.json':5,'record-recovery-results.json':21,'recovery-archive-results.json':15,'pet-flow-results.json':3,'book-flow-results.json':4,'workshop-flow-results.json':3,'onboarding-control-results.json':82,'onboarding-overlay-results.json':14};tests={}
for name,count in expected.items():
    path=OUT/name;result=json.loads(path.read_text(encoding='utf-8'));rows=result['results'] if isinstance(result,dict) else result
    assert len(rows)==count and all(row['passed'] and not row.get('errors') for row in rows),name
    if isinstance(result,dict):assert result['files']==files,name
    if name in ['onboarding-control-results.json','onboarding-overlay-results.json']:assert all(row['source_fingerprint']==fingerprint for row in rows),name
    tests[name]={'checks':count,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
assert json.loads((OUT/'record-recovery-source.json').read_text(encoding='utf-8'))['files']==files
paths=[f'pages/{p.name}' for p in sorted((ROOT/'custom').glob('*.html'))]+[path for path in files if path.startswith('assets/')]
def served(path):
    with urlopen('http://127.0.0.1:8765/'+path,timeout=15) as response:assert response.status==200 and response.read()==(ROOT/path).read_bytes(),path
    if path.startswith('pages/'):assert (ROOT/path).read_bytes()==(ROOT/'custom'/Path(path).name).read_bytes(),path
with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(served,paths))
queue_path=ROOT/'prototype/queue.json';queue=json.loads(queue_path.read_text(encoding='utf-8'));assert len(queue)==114 and not any(row['flow_verified'] for row in queue)
for row in queue:
    row['current_runtime_observation_source']=fingerprint
    if row['id'] in ['m02-p05','m03-p06','m06-p01','m06-p02','m06-p03','m06-p11']:row['account_recovery_evidence']='evidence/current/account-recovery-results.json'
queue_path.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
checkpoint={'scope':'Personal/relationship data recovery and named normal regressions; session/invite and other collections, all controls and final acceptance still pending.','source_fingerprint':fingerprint,'files':files,'tests':tests,'named_checks':sum(value['checks'] for value in tests.values()),'observations':228,'observed_control_records':report['controls_observed'],'http_pages':114,'http_shared_assets':37,'accepted_pages':0}
(OUT/'account-recovery-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
for name,scope,count in [('control-execution-checkpoint.json','Account/relationship representative controls and overlays only',96),('new-user-journey-checkpoint.json','Two continuous journeys only',2)]:
    (OUT/name).write_text(json.dumps({'scope':scope,'source_fingerprint':fingerprint,'actual_checks':count,'final_accepted':0,'files':files,'http_pages_matching_checkout':114,'http_shared_assets_matching_checkout':37},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({key:checkpoint[key] for key in ['named_checks','observations','observed_control_records','http_pages','http_shared_assets','accepted_pages']},ensure_ascii=False),flush=True)
