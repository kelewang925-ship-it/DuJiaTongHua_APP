"""Bind this recovery phase's named results to current source and served files."""
from pathlib import Path
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
import hashlib,json

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'prototype/evidence/current'
source=json.loads((OUT/'record-recovery-source.json').read_text(encoding='utf-8'))
report=json.loads((OUT/'current-runtime-summary.json').read_text(encoding='utf-8'))
assert source['files']==report['files'] and source['checks']==21 and source['passed']==21
for name,digest in source['files'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
assert report['observations']==228 and not report['errors'] and not report['unbound_or_delegated_candidates']
fingerprint=hashlib.sha256(json.dumps(report['files'],sort_keys=True).encode()).hexdigest()
expected={'record-recovery-results.json':21,'diary-flow-results.json':4,'photo-flow-results.json':3,'settings-flow-results.json':5,'book-flow-results.json':4,'onboarding-control-results.json':82,'onboarding-overlay-results.json':14,'new-user-journey-results.json':2}
tests={}
for name,count in expected.items():
    path=OUT/name;result=json.loads(path.read_text(encoding='utf-8'));rows=result['results'] if isinstance(result,dict) else result
    assert len(rows)==count and all(row['passed'] and not row.get('errors') for row in rows),name
    if name.startswith('onboarding-'):assert all(row['source_fingerprint']==fingerprint for row in rows),name
    if name=='new-user-journey-results.json':assert result['files']==report['files']
    tests[name]={'checks':count,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
paths=[f'pages/{p.name}' for p in sorted((ROOT/'custom').glob('*.html'))]+[p for p in report['files'] if p.startswith('assets/')]
assert len(paths)==151
def served(path):
    with urlopen('http://127.0.0.1:8765/'+path,timeout=15) as response:assert response.status==200 and response.read()==(ROOT/path).read_bytes(),path
    if path.startswith('pages/'):assert (ROOT/path).read_bytes()==(ROOT/'custom'/Path(path).name).read_bytes(),path
with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(served,paths))
queue_path=ROOT/'prototype/queue.json';queue=json.loads(queue_path.read_text(encoding='utf-8'))
assert len(queue)==114 and not any(row['flow_verified'] for row in queue)
for row in queue:
    row['current_runtime_observation_source']=fingerprint
    if row['id'] in ['m03-p02','m03-p05','m03-p06','m03-p10','m04-p05','m06-p04']:
        row['record_recovery_evidence']='evidence/current/record-recovery-results.json'
queue_path.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
checkpoint={'scope':'Records recovery phase only; other collections, all controls and final acceptance remain open.','source_fingerprint':fingerprint,'files':report['files'],'tests':tests,'named_checks':sum(item['checks'] for item in tests.values()),'http_pages':114,'http_shared_assets':37,'observations':228,'observed_control_records':report['controls_observed'],'accepted_pages':0,'recovery_copy_history_ui':'pending'}
(OUT/'record-recovery-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
control={'scope':'Current representative account/relationship initial and overlay checks; remaining controls and final acceptance pending.','source_fingerprint':fingerprint,'actual_checks':96,'observations':228,'observed_control_records':report['controls_observed'],'http_pages_matching_checkout':114,'http_shared_assets_matching_checkout':37,'partial_implemented':114,'final_accepted':0,'results':{name:tests[name]['sha256'] for name in ['onboarding-control-results.json','onboarding-overlay-results.json']},'files':report['files']}
(OUT/'control-execution-checkpoint.json').write_text(json.dumps(control,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
journey={'scope':'Two continuous journeys rerun after record recovery; earlier binding layout checks remain historical.','source_fingerprint':fingerprint,'actual_checks':2,'final_accepted':0,'http_pages_matching_checkout':114,'http_shared_assets_matching_checkout':37,'results':{'new-user-journey-results.json':tests['new-user-journey-results.json']['sha256']},'files':report['files']}
(OUT/'new-user-journey-checkpoint.json').write_text(json.dumps(journey,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({key:checkpoint[key] for key in ['named_checks','http_pages','http_shared_assets','observations','observed_control_records','accepted_pages']},ensure_ascii=False),flush=True)
