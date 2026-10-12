"""Source-bound form, confirmed, identity and arrangement deletion outcomes."""
import argparse,json,hashlib
from urllib.request import urlopen
from verify_pet_controls import ROOT,BASE,source

def main():
    p=argparse.ArgumentParser();p.add_argument('--forms-session',type=int,required=True);p.add_argument('--forms-exit',type=int,required=True);p.add_argument('--delete-session',type=int,required=True);p.add_argument('--delete-exit',type=int,required=True);p.add_argument('--sequential-session',type=int,required=True);p.add_argument('--sequential-exit',type=int,required=True);a=p.parse_args();assert a.forms_exit==a.delete_exit==a.sequential_exit==0
    files=source();out=ROOT/'evidence/current';h=lambda path:hashlib.sha256(path.read_bytes()).hexdigest();observed=h(out/'hidden-overlay-observations.json');reports={};counts={'overlay-form-save-results.json':47,'confirmed-deletion-results.json':45,'identity-deletion-results.json':13,'book-candidate-deletion-results.json':25}
    for name,count in counts.items():
        value=json.loads((out/name).read_text(encoding='utf-8'));assert value['files']==files and value['observations_sha256']==observed and len(value['results'])==count and all(r['passed']and not r['errors']for r in value['results']);reports[name]=h(out/name)
    for name in ['overlay-form-save-summary.json','confirmed-deletion-summary.json','identity-deletion-summary.json','book-candidate-deletion-summary.json']:
        value=json.loads((out/name).read_text(encoding='utf-8'));assert value['files']==files;reports[name]=h(out/name)
    checkpoint=dict(files=files,executions=dict(forms=dict(session_id=a.forms_session,exit_code=a.forms_exit,cases=47),confirmed=dict(session_id=a.delete_session,exit_code=a.delete_exit,cases=45),identity_and_candidates=dict(session_id=a.sequential_session,exit_code=a.sequential_exit,cases=38,identity_first=True,identity_exit_gated_before_candidates=True)),report_sha256=reports,observations_sha256=observed,script_sha256={name:h(ROOT/name)for name in ['verify_overlay_form_saves.py','verify_confirmed_deletions.py','verify_identity_deletions.py','verify_book_candidate_deletions.py','build_overlay_form_save_summary.py','build_confirmed_deletion_summary.py','build_identity_deletion_summary.py','build_book_candidate_deletion_summary.py','verify_fresh_save_delete_outcomes.py']},form_cases=47,confirmed_cases=45,identity_cases=13,candidate_cases=25,total=130,accepted_pages=0,scope='Declared16 forms,15 confirmed record/tag entrances,2 identity boundaries and5 candidate arrangement deletes in representative390px/reduced-motion fixtures. Stored outcomes/failure retry proven; other fields/conditions/concurrent sources/submitting/layout and whole product journeys remain incomplete.')
    (out/'fresh-save-delete-outcomes-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    state_path=out/'current-evidence-state.json';state=json.loads(state_path.read_text(encoding='utf-8'));assert state['files']==files and state['current_initial_controls']==752 and state['current_overlay_exit_total']==498;state.update(current_overlay_form_save_checks=47,current_confirmed_deletion_checks=45,current_identity_cases=13,historical_identity_cases=0,current_book_candidate_deletion_checks=25,accepted_pages=0);state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name,digest in files.items():
        with urlopen(BASE+name.replace('custom/','pages/',1),timeout=10)as r:assert hashlib.sha256(r.read()).hexdigest()==digest,name
    print(json.dumps(dict(forms=47,confirmed_deletions=45,identity=13,arrangement_candidates=25,total=130,current_initial=752,accepted_pages=0)))

if __name__=='__main__':main()
