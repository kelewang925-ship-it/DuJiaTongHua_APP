"""Source-bound continuous time-flow and shared-guard checkpoint; final goal still open."""
import json,hashlib,subprocess,sys
from datetime import datetime,timezone
from verify_pet_controls import ROOT,source
OUT=ROOT/'evidence/current';files=source()
assert subprocess.run([sys.executable,str(ROOT/'verify_product_journey_checkpoint.py')]).returncode==0
base=json.loads((OUT/'product-journey-checkpoint.json').read_text(encoding='utf-8'));assert base['files']==files
meta=json.loads((OUT/'time-journey-regression-source.json').read_text(encoding='utf-8'));assert meta['files']==files;tests={};total=base['named_checks']
counts={'anniversary-flow-results.json':3,'anniversary-state-results.json':7,'capsule-flow-results.json':3,'capsule-state-results.json':5,'time-collection-results.json':7,'settings-sheet-guard-results.json':11,'time-controls-results.json':54,'time-layout-results.json':20,'time-entry-layout-results.json':15,'time-task-return-results.json':6}
for name,count in counts.items():
 p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));rows=v['results']if isinstance(v,dict)else v;m=meta['reports'][name];assert len(rows)==count and all(r['passed']and not r['errors']for r in rows)and m['exit_code']==0 and m['sha256']==hashlib.sha256(p.read_bytes()).hexdigest(),name
 if isinstance(v,dict):assert v['files']==files,name
 tests[name]=m;total+=count
p=OUT/'time-product-journey-results.json';v=json.loads(p.read_text(encoding='utf-8'));assert v['files']==files and len(v['results'])==1;row=v['results'][0];assert row['passed']and not row['errors'];assert {'today-related-diary','sealed-private','opened-photo','deleted-capsule-kept-moment','empty-reminders-kept-originals'}<={s['step']for s in row['steps']};tests[p.name]=dict(cases=1,sha256=hashlib.sha256(p.read_bytes()).hexdigest());total+=1;assert total==165
assert files==source();checkpoint=dict(scope='Two real registered-user journeys, specified time controls/states and shared-guard regressions; complete product acceptance pending',verified_at=datetime.now(timezone.utc).isoformat(),files=files,fingerprint=base['fingerprint'],tests=tests,preceding_product_checks=base['named_checks'],preceding_checkpoint_sha256=hashlib.sha256((OUT/'product-journey-checkpoint.json').read_bytes()).hexdigest(),named_checks=total,observations=base['observations'],observed_controls=base['observed_controls'],conditional_redirects=base['conditional_redirects'],observation_only=True,http_pages=base['http_pages'],http_shared_assets=base['http_shared_assets'],accepted_pages=0)
(OUT/'time-journey-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:checkpoint[k]for k in ['named_checks','observations','observed_controls','conditional_redirects','http_pages','http_shared_assets','accepted_pages']}),flush=True)
