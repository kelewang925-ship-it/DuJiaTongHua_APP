"""Bind actual exit processes and summary without promoting final save/delete actions."""
import argparse,json,hashlib
from urllib.request import urlopen
from verify_pet_controls import ROOT,BASE,source

def main():
    p=argparse.ArgumentParser();p.add_argument('--exit-session',type=int,required=True);p.add_argument('--exit-code',type=int,required=True);p.add_argument('--nested-session',type=int,required=True);p.add_argument('--nested-exit',type=int,required=True);a=p.parse_args();assert a.exit_code==a.nested_exit==0
    files=source();out=ROOT/'evidence/current';h=lambda path:hashlib.sha256(path.read_bytes()).hexdigest();summary=json.loads((out/'overlay-exit-summary.json').read_text(encoding='utf-8'));assert summary['files']==files and summary['closure_cases']==432 and summary['dirty_cases']==64 and summary['nested_cases']==66 and summary['total']==498
    for name,digest in summary['reports'].items():assert h(out/name)==digest,name
    for name,count in [('overlay-exit-path-results.json',432),('nested-confirmation-results.json',66)]:
        report=json.loads((out/name).read_text(encoding='utf-8'));assert report['files']==files and len(report['results'])==count and all(r['passed']and not r['errors']and r['storage_preserved']and r['underlying_page_preserved']for r in report['results'])
    checkpoint=dict(files=files,executions=dict(closure=dict(session_id=a.exit_session,exit_code=a.exit_code,cases=432),nested=dict(session_id=a.nested_session,exit_code=a.nested_exit,cases=66)),report_sha256={**summary['reports'],'overlay-exit-summary.json':h(out/'overlay-exit-summary.json')},script_sha256={name:h(ROOT/name)for name in ['verify_overlay_exit_paths.py','verify_nested_confirmations.py','build_overlay_exit_summary.py','verify_fresh_overlay_exits.py']},total=498,accepted_pages=0,scope='99 observed overlays,390x844/reduced motion;368 clean closes,64 dirty keep/discard paths,66 nested dangerous/identity cancels. Not final action results/all sources/submitting/widths or page acceptance.')
    (out/'fresh-overlay-exit-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    state_path=out/'current-evidence-state.json';state=json.loads(state_path.read_text(encoding='utf-8'));assert state['files']==files and state['current_initial_controls']==752;state.update(current_overlay_exit_checks=432,current_nested_cancel_checks=66,current_overlay_exit_total=498,overlay_exit_replay_session=a.exit_session,nested_cancel_replay_session=a.nested_session,overlay_exit_replay_complete=True,current_overlay_exit_checkpoint='evidence/current/fresh-overlay-exit-checkpoint.json',accepted_pages=0);state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name,digest in files.items():
        with urlopen(BASE+name.replace('custom/','pages/',1),timeout=10)as r:assert hashlib.sha256(r.read()).hexdigest()==digest,name
    print(json.dumps(dict(closure=432,dirty=64,nested=66,total=498,current_initial=752,accepted_pages=0)))

if __name__=='__main__':main()
