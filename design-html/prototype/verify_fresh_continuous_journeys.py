"""Bind real current journeys and mandatory stage coverage, not final product acceptance."""
import argparse,ast,hashlib,json
from urllib.request import urlopen
from verify_pet_controls import ROOT,BASE,source

def main():
    p=argparse.ArgumentParser();p.add_argument('--new-session',type=int,required=True);p.add_argument('--new-exit',type=int,required=True);p.add_argument('--product-session',type=int,required=True);p.add_argument('--product-exit',type=int,required=True);p.add_argument('--time-session',type=int,required=True);p.add_argument('--time-exit',type=int,required=True);a=p.parse_args();assert a.new_exit==a.product_exit==a.time_exit==0
    files=source();out=ROOT/'evidence/current';h=lambda path:hashlib.sha256(path.read_bytes()).hexdigest();names={'new-user-journey-results.json':(2,13),'product-journey-results.json':(1,22),'time-product-journey-results.json':(1,19)};reports={};data={}
    for name,(cases,steps)in names.items():
        value=json.loads((out/name).read_text(encoding='utf-8'));assert value['files']==files and len(value['results'])==cases and all(r['passed']and not r['errors']for r in value['results']);assert sum(len(r['steps'])for r in value['results'])==steps;reports[name]=h(out/name);data[name]=value
    for script,report in [('verify_product_journey.py','product-journey-results.json'),('verify_time_product_journey.py','time-product-journey-results.json')]:
        tree=ast.parse((ROOT/script).read_text(encoding='utf-8'));expected=[n.args[2].value for n in ast.walk(tree)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='stage'and len(n.args)>2 and isinstance(n.args[2],ast.Constant)];actual=[s['step']for s in data[report]['results'][0]['steps']];assert set(expected)<=set(actual)and len(actual)==len(set(actual)),(script,actual)
    assert data['new-user-journey-results.json']['results'][0]['steps'][-1]['step']=='empty-home-after-delete'
    assert data['product-journey-results.json']['results'][0]['steps'][-1]['step']=='book-deleted-sources-retained'
    assert data['time-product-journey-results.json']['results'][0]['steps'][-1]['step']=='empty-reminders-kept-originals'
    def new_user_shots(node):return {'new-user-'+n.args[2].value+'.png'for n in ast.walk(node)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='step'and len(n.args)>3 and isinstance(n.args[2],ast.Constant)and isinstance(n.args[3],ast.Constant)and n.args[3].value is True}
    nj_tree=ast.parse((ROOT/'verify_new_user_journey.py').read_text(encoding='utf-8'));serial=next(n for n in nj_tree.body if isinstance(n,ast.FunctionDef)and n.name=='serial');shots=[out/name for name in new_user_shots(nj_tree)]
    for script,directory in [('verify_product_journey.py','product-journey'),('verify_time_product_journey.py','time-product-journey')]:
        tree=ast.parse((ROOT/script).read_text(encoding='utf-8'));stage=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='stage');stage_shots={v.value+'.png'for n in ast.walk(stage)if isinstance(n,ast.Compare)and isinstance(n.left,ast.Name)and n.left.id=='name'for c in n.comparators if isinstance(c,ast.List)for v in c.elts if isinstance(v,ast.Constant)}
        shots.extend(out/directory/name for name in new_user_shots(serial)|stage_shots)
    assert all(p.exists()and p.stat().st_size>0 for p in shots),[str(p)for p in shots if not p.exists()];assert any(p.name=='book-published.png'for p in shots)
    checkpoint=dict(files=files,executions=dict(new_user=dict(session_id=a.new_session,exit_code=a.new_exit,cases=2,steps=13),product=dict(session_id=a.product_session,exit_code=a.product_exit,cases=1,steps=22),time=dict(session_id=a.time_session,exit_code=a.time_exit,cases=1,steps=19)),report_sha256=reports,script_sha256={name:h(ROOT/name)for name in ['verify_new_user_journey.py','verify_product_journey.py','verify_time_product_journey.py','verify_fresh_continuous_journeys.py']},screenshot_sha256={p.relative_to(ROOT).as_posix():h(p)for p in shots},cases=4,step_records=54,accepted_pages=0,scope='Four real product-control chains in fresh browser contexts: new registration/binding/diary CRUD, list-home, eight modules and time/reminder/capsule flows with declared local peer/failure/time simulations. Not all validation/failure/source/keyboard/layout branches or114-page final acceptance.')
    (out/'fresh-continuous-journeys-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    state_path=out/'current-evidence-state.json';state=json.loads(state_path.read_text(encoding='utf-8'));assert state['files']==files and state['current_initial_controls']==752 and state['current_overlay_exit_total']==498;state.update(current_continuous_journey_cases=4,current_continuous_journey_steps=54,accepted_pages=0);state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name,digest in files.items():
        with urlopen(BASE+name.replace('custom/','pages/',1),timeout=10)as r:assert hashlib.sha256(r.read()).hexdigest()==digest,name
    print(json.dumps(dict(journeys=4,stage_records=54,current_initial=752,accepted_pages=0)))

if __name__=='__main__':main()
