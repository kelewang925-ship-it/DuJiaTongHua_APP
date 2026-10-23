"""Bind album decode fixes, workshop regressions and static await inventory; not final acceptance."""
import hashlib,json
from pathlib import Path
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,BASE,source
from verify_work_album_decode import CASES

def main():
 h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8'));out=ROOT/'evidence/current';dest=out/'work-album-decode';files=source();styles={p.relative_to(DEMO).as_posix():h(p) for p in (DEMO/'assets').glob('*.css')}
 redroot=ROOT/'evidence/baseline/work-album-decode';red=read(redroot/'results.json');v=read(dest/'results.json')
 assert len(red['results'])==10 and sum(r['passed'] for r in red['results'])==8 and {r['case'] for r in red['results'] if not r['passed']}=={'concurrent-export-edit','decode-error-retry'} and all(not r['errors'] for r in red['results'])
 assert red['script_sha256']==h(redroot/'verify_work_album_decode.py') and h(redroot/'prototype-workshop-store.js')==red['files']['assets/prototype-workshop-store.js']
 assert {k for k in files if files[k]!=red['files'][k]}=={'assets/prototype-workshop-store.js'} and red['styles']==styles
 assert v['files']==files and v['styles']==styles and v['script_sha256']==h(ROOT/'verify_work_album_decode.py') and len(v['results'])==10 and {r['case'] for r in v['results']}==set(CASES) and all(r['passed'] and not r['errors'] and r['reload_consistent'] for r in v['results'])
 assert next(r for r in v['results'] if r['case']=='concurrent-export-edit')['external_edit_preserved']
 regression=read(dest/'regressions.json');assert regression['files']==files and regression['styles']==styles and regression['script_sha256']==h(ROOT/'verify_work_album_regressions.py') and len(regression['results'])==3
 expected={'verify_workshop_controls.py':92,'verify_workshop_flow.py':3,'verify_workshop_states.py':8};reports=[dest/'results.json',dest/'regressions.json',redroot/'results.json'];shots=[]
 for r in regression['results']:
  assert r['exit_code']==0 and r['cases']==r['passed']==expected[r['script']] and not r['errors'] and r['script_sha256']==h(ROOT/r['script']) and r['report_sha256']==h(ROOT/r['report'])
  report=ROOT/r['report'];reports.append(report);value=read(report);rows=value['results'] if isinstance(value,dict) else value;assert len(rows)==r['cases'] and all(v['passed'] and not v['errors'] for v in rows)
  if isinstance(value,dict):assert value['files']==files
  if r['script']!='verify_workshop_controls.py':
   prefix='workshop-state-' if r['script']=='verify_workshop_states.py' else 'workshop-';shots.extend(out/(prefix+v['case']+'.png') for v in rows)
 assert len(shots)==11 and all(p.exists() and p.stat().st_size for p in shots)
 inventorypath=out/'submission-await-audit/inventory.json';inventory=read(inventorypath);assert inventory['files']=={k:v for k,v in files.items() if k.endswith('.js')} and inventory['script_sha256']==h(ROOT/'audit_submission_awaits.cjs')
 assert inventory['parser']['sha256']==h(Path('D:/projectCode/DuJiaTongHua/DuJiaTongHua_APP/node_modules/acorn/dist/acorn.js'))
 callbacks=inventory['results'];assert len(callbacks)==78 and all('callback' in r for r in callbacks) and sum(r['async'] for r in callbacks)==25 and sum(bool(r['awaits']) for r in callbacks)==10
 oldinventory=read(ROOT/'evidence/history/pre-album-decode-718a0ec/submission-await-inventory.json');assert oldinventory['files']=={k:v for k,v in red['files'].items() if k.endswith('.js')}
 first=ROOT/'evidence/history/work-album-decode-first-green';g=read(first/'results.json');assert g['files']==files and g['script_sha256']==red['script_sha256'] and len(g['results'])==10 and all(v['passed'] for v in g['results']) and read(first/'execution.json')['exit_code']==0
 reports.extend([inventorypath,first/'results.json',first/'execution.json'])
 for path,digest in {**files,**styles}.items():
  with urlopen(BASE+path.replace('custom/','pages/',1),timeout=10) as response:assert response.headers.get('Cache-Control')=='no-store' and hashlib.sha256(response.read()).hexdigest()==digest
 pages=list((DEMO/'custom').glob('*.html'));assert len(pages)==114
 for p in pages:assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
 scripts=['verify_work_album_decode.py','verify_work_album_regressions.py','verify_work_album_checkpoint.py','audit_submission_awaits.cjs','verify_workshop_controls.py','verify_workshop_flow.py','verify_workshop_states.py','verify_pet_controls.py','verify_overlay_form_saves.py','verify_image_read_order.py','audit_hidden_overlays.py','audit_runtime.py','audit_current_runtime.py']
 documents=['ACCEPTANCE_REQUIREMENTS.md','SUBMISSION_AWAIT_AUDIT.md','WORK_ALBUM_DECODE.md','README.md','ISSUES.md'];canonical=lambda p:hashlib.sha256(p.read_text(encoding='utf-8').replace('\r\n','\n').encode('utf-8')).hexdigest()
 import re
 required=lambda p:[line.split('|')[1:3] for line in p.read_text(encoding='utf-8').splitlines() if re.match(r'^\| \d+ ',line)]
 before=required(ROOT/'evidence/history/pre-album-decode-718a0ec/ACCEPTANCE_REQUIREMENTS.md');assert len(before)==41 and required(ROOT/'ACCEPTANCE_REQUIREMENTS.md')==before
 scope='10 native decode/export checks and103 existing workshop contracts, flows and states.78 direct busy callbacks statically inventoried separately; no whole-program synchronous or cross-tab atomicity claim. Final114-page and named branch replay remains pending.'
 cp=dict(files=files,styles=styles,document_text_sha256={n:canonical(ROOT/n) for n in documents},reports_sha256={p.relative_to(ROOT).as_posix():h(p) for p in reports},scripts_sha256={n:h(ROOT/n) for n in scripts},screenshot_sha256={p.relative_to(ROOT).as_posix():h(p) for p in shots},executions=dict(baseline=dict(session='57771',exit_code=1,passed=8,failed=2),first_green=dict(session='80152',exit_code=0,cases=10),native=dict(session='71526',exit_code=0,cases=10),regressions=dict(session='25577',exit_code=0,cases=103),source_audit=dict(chunk='a5c8e5',exit_code=0)),native_cases=10,regression_cases=103,total_checks=113,static_direct_callbacks=78,accepted_pages=0,scope=scope)
 (dest/'checkpoint.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 statepath=out/'current-evidence-state.json';state=read(statepath);history=ROOT/'evidence/history/pre-album-decode-718a0ec'
 if state['files']!=files:
  assert state['files']==red['files'];(history/'current-evidence-state.json').write_bytes(statepath.read_bytes())
  for name,count in list(state.items()):
   if name.startswith('current_') and isinstance(count,int) and not isinstance(count,bool) and count>0:state['historical_'+name.removeprefix('current_')]=count;state[name]=0
 state.update(files=files,style_dependencies=styles,current_work_album_decode_cases=10,current_workshop_control_cases=92,current_workshop_flow_cases=3,current_workshop_state_cases=8,current_work_album_checkpoint='evidence/current/work-album-decode/checkpoint.json',current_submission_await_inventory='evidence/current/submission-await-audit/inventory.json',previous_behavior_source_manifest='evidence/history/pre-album-decode-718a0ec/current-evidence-state.json',runtime_requires_refresh=True,catalog_requires_refresh=True,flow_replay_requires_refresh=True,work_album_decode_issue='fixed_for_late_duplicate_export_and_native_decode_error',accepted_pages=0,reason=scope)
 statepath.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(native=10,regressions=103,total=113,static_callbacks=78,mirrors=114,accepted_pages=0)))

if __name__=='__main__':main()
