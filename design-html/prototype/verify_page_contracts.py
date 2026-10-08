"""Check catalog completeness, literal provenance and unchanged product bytes."""
import json,re,hashlib
from verify_pet_controls import ROOT,DEMO,source
OUT=ROOT/'evidence/current';v=json.loads((OUT/'page-contracts.json').read_text(encoding='utf-8'));assert v['files']==source()
manifest=json.loads((DEMO/'manifest.json').read_text(encoding='utf-8'));ids={r['id']for r in manifest};pages=v['pages'];assert len(pages)==114 and {p['id']for p in pages}==ids
runtime=json.loads((OUT/'current-runtime-inventory.json').read_text(encoding='utf-8'));controls=0
for p in pages:
 assert p['type']and '逐页确认'not in p['type'];assert p['title']==next(r['title']for r in manifest if r['id']==p['id'])
 assert (DEMO/p['html']).read_bytes()==(DEMO/'pages'/f"{p['id']}.html").read_bytes()
 assert len(p['runtime'])==2 and p['control_evidence']
 for r in p['runtime']:
  observed=runtime[r['inventory_index']];assert observed['id']==p['id']and observed['scenario']==r['scenario']and observed['effective']==r['effective']and observed['observed']['controls']==r['observed_controls'];controls+=len(r['observed_controls'])
 for c in p['control_evidence']:
  f=ROOT/c['report'];raw=f.read_bytes();name=f.name;assert hashlib.sha256(raw).hexdigest()==v['reports'][name]['sha256'];report=json.loads(raw);rows=report['results']if isinstance(report,dict)else report;actual=rows[c['result_index']];assert actual['selector']==c['selector']and actual.get('contract','')==c['contract']
  if c['status']=='当前源码通过':
   assert actual['passed']and not actual['errors']
   if isinstance(report,dict):assert report['files']==v['files']
   else:assert actual['source_fingerprint']==hashlib.sha256(json.dumps(v['files'],sort_keys=True).encode()).hexdigest()
for a in v['assets']:assert (DEMO/a['path']).stat().st_size==a['bytes']and hashlib.sha256((DEMO/a['path']).read_bytes()).hexdigest()==a['sha256']
assert controls==1696 and len(v['assets'])==267
for e in v['edges']:assert e['source']in ids and e['target']in ids
graph=(ROOT/'PAGE_RELATIONSHIPS.mmd').read_text(encoding='utf-8');assert len(re.findall(r'^  m\d{2}_p\d{2}\[',graph,re.M))==114
matrix=(ROOT/'STATE_MATRIX.md').read_text(encoding='utf-8');assert len(re.findall(r'^\| m\d{2}-p\d{2} \|',matrix,re.M))==114
for p in pages:assert p['type']in next(line for line in matrix.splitlines()if line.startswith('| '+p['id']+' |'))
requirements=(ROOT/'ACCEPTANCE_REQUIREMENTS.md').read_text(encoding='utf-8');sections=re.findall(r'^\| (\d+) ',requirements,re.M);assert list(map(int,sections))==list(range(1,42))
queue=json.loads((ROOT/'queue.json').read_text(encoding='utf-8'));assert len(queue)==114 and not any(p.get('flow_verified')for p in queue)
for q in queue:
 p=next(p for p in pages if p['id']==q['id']);assert q['page_type']==p['type']and q['needed_states']==p['required_states']and(ROOT/q['page_contract']).exists();assert q['current_initial_control_checks']==sum(c['status']=='当前源码通过'for c in p['control_evidence'])
assert source()==v['files']
print(json.dumps(dict(pages=114,assets=267,observations=228,observed_controls=controls,initial_control_evidence=sum(len(p['control_evidence'])for p in pages),requirements=41,accepted_pages=0)))
