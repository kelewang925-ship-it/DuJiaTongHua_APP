"""Source/served-byte-bound shared-danger phase checkpoint; full acceptance remains open."""
import json,hashlib,subprocess,sys
from datetime import datetime,timezone
from verify_pet_controls import ROOT,source
OUT=ROOT/'evidence/current';files=source()
assert subprocess.run([sys.executable,str(ROOT/'verify_time_journey_checkpoint.py')]).returncode==0
base=json.loads((OUT/'time-journey-checkpoint.json').read_text(encoding='utf-8'));assert base['files']==files and base['named_checks']==165
meta=json.loads((OUT/'danger-regression-source.json').read_text(encoding='utf-8'));assert meta['files']==files;tests={};total=base['named_checks']
counts={'danger-confirmation-results.json':18,'settings-flow-results.json':5,'settings-state-results.json':9,'pet-life-state-results.json':12,'book-structure-results.json':5,'record-recovery-results.json':21,'account-recovery-results.json':20,'danger-overlay-results.json':62,'danger-primary-contract-results.json':5,'danger-workshop-delayed-load-results.json':1}
for name,count in counts.items():
 p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));rows=v['results']if isinstance(v,dict)else v;assert len(rows)==count and all(r['passed']and not r['errors']for r in rows),name
 if isinstance(v,dict)and 'files'in v:assert v['files']==files,name
 digest=hashlib.sha256(p.read_bytes()).hexdigest()
 if name in meta['reports']:
  m=meta['reports'][name];assert m['exit_code']==0 and m['cases']==m['passed']==count and m['sha256']==digest and not m['errors'],name
 tests[name]=dict(cases=count,sha256=digest);total+=count
inventory=json.loads((OUT/'danger-modal-callsite-inventory.json').read_text(encoding='utf-8'));assert inventory['files']==files and len(inventory['results'])==51 and sum(r['danger']for r in inventory['results'])==15
assert total==323 and files==source()
checkpoint=dict(scope='Shared destructive-component adoption, actual cancellation/dismissal/layout and touched business regressions; full product acceptance pending',verified_at=datetime.now(timezone.utc).isoformat(),files=files,fingerprint=base['fingerprint'],tests=tests,preceding_checks=165,preceding_checkpoint_sha256=hashlib.sha256((OUT/'time-journey-checkpoint.json').read_bytes()).hexdigest(),named_checks=total,observations=base['observations'],observed_controls=base['observed_controls'],conditional_redirects=base['conditional_redirects'],http_pages=base['http_pages'],http_shared_assets=base['http_shared_assets'],accepted_pages=0)
(OUT/'danger-components-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:checkpoint[k]for k in ['named_checks','observations','observed_controls','conditional_redirects','http_pages','http_shared_assets','accepted_pages']}),flush=True)
