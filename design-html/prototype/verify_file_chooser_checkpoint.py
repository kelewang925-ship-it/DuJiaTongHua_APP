"""Chooser opening boundary, active-operation block and existing change-event regression."""
import hashlib,json
from pathlib import Path
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,BASE,source

def main():
 h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8'));out=ROOT/'evidence/current';dest=out/'file-chooser-pending';files=source();styles={p.relative_to(DEMO).as_posix():h(p) for p in (DEMO/'assets').glob('*.css')}
 red=read(ROOT/'evidence/baseline/file-chooser-pending/results.json');red_shared=read(ROOT/'evidence/baseline/file-chooser-started/results.json')
 assert red['files']==red_shared['files'] and red['styles']==red_shared['styles']==styles
 assert len(red['results'])==4 and all(not r['passed'] and r['unchanged_before_chooser_result'] is False and not r['errors'] for r in red['results'])
 assert len(red_shared['results'])==4 and all(not r['passed'] and r['chooser_count_while_started']==1 and not r['errors'] for r in red_shared['results'])
 assert red['script_sha256']==h(ROOT/'verify_file_chooser_pending.py') and red_shared['script_sha256']==h(ROOT/'verify_file_chooser_started.py')
 assert h(ROOT/'evidence/baseline/file-chooser-pending/prototype-ui.js')==red['files']['assets/prototype-ui.js'];assert {k for k in files if files[k]!=red['files'][k]}=={'assets/prototype-ui.js'}
 definitions=[(dest/'results.json',24,'verify_file_chooser_pending.py'),(out/'file-chooser-started/results.json',4,'verify_file_chooser_started.py'),(out/'pending-image-read/results.json',16,'verify_pending_image_reads.py')]
 for path,count,script in definitions:
  v=read(path);assert v['files']==files and v['styles']==styles and v['script_sha256']==h(ROOT/script) and len(v['results'])==count and all(r['passed'] and not r['errors'] for r in v['results'])
 from verify_file_chooser_pending import TRIGGERS
 v=read(dest/'results.json');assert len(TRIGGERS)==8 and {(r['case'],r['mode']) for r in v['results']}=={(n,m) for n in TRIGGERS for m in ['cancel','success','decode-failure']};assert all(r['unchanged_before_chooser_result'] and r['explicit_retry_and_reload_consistent'] for r in v['results'])
 assert all(r['chooser_count_while_started']==0 and r['restored_after_operation'] for r in read(out/'file-chooser-started/results.json')['results'])
 for path,digest in {**files,**styles}.items():
  with urlopen(BASE+path.replace('custom/','pages/',1),timeout=10) as response:assert response.headers.get('Cache-Control')=='no-store' and hashlib.sha256(response.read()).hexdigest()==digest
 pages=list((DEMO/'custom').glob('*.html'));assert len(pages)==114
 for p in pages:assert p.read_bytes()==(DEMO/'pages'/p.name).read_bytes()
 paths=[v[0] for v in definitions]+[ROOT/'evidence/baseline/file-chooser-pending/results.json',ROOT/'evidence/baseline/file-chooser-started/results.json'];scripts=[v[2] for v in definitions]+['verify_file_chooser_checkpoint.py','verify_image_pending_exit.py','verify_image_read_order.py','verify_submission_changes.py','verify_pending_page_guard.py','verify_overlay_form_saves.py','audit_hidden_overlays.py','audit_current_runtime.py','book_test_helpers.py']+['verify_'+n+'_controls.py' for n in ['onboarding','record','moment','time','workshop','settings','pet','book']]
 cp=dict(files=files,styles=styles,reports_sha256={p.relative_to(ROOT).as_posix():h(p) for p in paths},scripts_sha256={n:h(ROOT/n) for n in scripts},executions=dict(chooser_red=dict(chunk='f484bf',exit_code=1),started_red=dict(chunk='8a8932',exit_code=1),chooser_and_started=dict(session='28714',exit_code=0),change_event=dict(session='6749',exit_code=0)),chooser_cases=24,started_contract_cases=4,change_event_cases=16,total_checks=44,accepted_pages=0,scope='Actual Chromium chooser requests from8 save entries before any selection, cancel/valid/invalid results and explicit save;4 synthetic started-operation file activation contracts;16 native change-event regressions. Headless browser event boundary, not a real Windows/mobile dialog. Typed edits after operation start, world-avatar permission changes and full final matrices remain unaccepted.')
 (dest/'checkpoint.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 statepath=out/'current-evidence-state.json';state=read(statepath);history=ROOT/'evidence/history/pre-file-chooser-9bc47dc';history.mkdir(parents=True,exist_ok=True)
 if state['files']!=files:
  (history/'current-evidence-state.json').write_bytes(statepath.read_bytes())
  for name,count in list(state.items()):
   if name.startswith('current_') and isinstance(count,int) and not isinstance(count,bool) and count>0:state['historical_'+name.removeprefix('current_')]=count;state[name]=0
 state.update(files=files,style_dependencies=styles,current_file_chooser_cases=24,current_file_chooser_started_contract_cases=4,current_pending_image_cases=16,current_image_read_checkpoint='evidence/current/file-chooser-pending/checkpoint.json',previous_behavior_source_manifest='evidence/history/pre-file-chooser-9bc47dc/current-evidence-state.json',runtime_requires_refresh=True,catalog_requires_refresh=True,flow_replay_requires_refresh=True,file_chooser_submission_issue='fixed_for_eight_save_entries_and_shared_started_contract',accepted_pages=0,reason=cp['scope'])
 statepath.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(chooser=24,started_contract=4,change_event=16,total=44,mirrors=114,accepted_pages=0)))

if __name__=='__main__':main()
