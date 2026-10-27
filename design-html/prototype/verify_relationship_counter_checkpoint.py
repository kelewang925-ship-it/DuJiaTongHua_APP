"""Bind the profile-only display repair and retain earlier evidence without relabeling."""
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    base=ROOT/'evidence/baseline/relationship-day-counter';out=ROOT/'evidence/current/relationship-day-counter'
    red=read(base/'results.json');green=read(out/'results.json');controls=read(out/'controls.json');scope=read(out/'source-scope.json');previous_path=ROOT/'evidence/current/pet-home-visual/checkpoint.json';previous=read(previous_path)
    assert red['files']==previous['files'] and red['expected_cases']==len(red['results'])==15 and not any(r['passed'] for r in red['results'])
    assert red['script_sha256']==sha(base/'verifier.py')
    assert green['expected_cases']==len(green['results'])==15 and all(r['passed'] and not r['errors'] for r in green['results'])
    assert green['script_sha256']==sha(ROOT/'verify_relationship_day_counter.py')
    assert controls['files']==green['files'] and len(controls['results'])==5 and all(r['passed'] and not r['errors'] for r in controls['results'])
    assert controls['script_sha256']==sha(ROOT/'verify_relationship_profile_controls.py') and controls['fixture_script_sha256']==sha(ROOT/'verify_onboarding_controls.py')
    assert controls['catalog_sha256']==sha(ROOT/'evidence/current/page-contracts.json')
    assert scope['other_controller_ast_equal'] and scope['masked_nodes']==dict(function=1,listener=1,initial=1)
    assert scope['auditor_sha256']==sha(ROOT/'audit_relationship_counter_scope.cjs')
    for path,digest in scope['files_sha256'].items():assert sha(ROOT/path)==digest,path
    delta=[k for k in red['files'] if red['files'][k]!=green['files'][k]]
    assert set(delta)=={'assets/prototype-relationship.js','custom/m02-p06.html'},delta
    for path,digest in green['files'].items():assert sha(DEMO/path)==digest,path
    assert (DEMO/'custom/m02-p06.html').read_bytes()==(DEMO/'pages/m02-p06.html').read_bytes()
    artifacts=[base/'results.json',base/'verifier.py',base/'prototype-relationship.js',base/'m02-p06.html',out/'results.json',out/'controls.json',out/'source-scope.json',out/'legacy-key-observer/results.json',out/'legacy-key-observer/verifier.py',previous_path]+list(out.glob('*.png'))
    value=dict(files=green['files'],baseline_files=red['files'],changed_files=delta,other_controller_ast_equal=True,
      artifacts_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in artifacts},checkpoint_script_sha256=sha(Path(__file__)),
      actual_executions=[dict(session_id=2834,exit_code=1,cases=15,passed=0,stage='baseline fixed214'),dict(session_id=67832,exit_code=1,cases=15,passed=13,stage='QA did not yet allow three existing legacy profile keys'),dict(session_id=81837,exit_code=0,cases=15,passed=15,stage='calendar,preview,cancel,save failure/retry/reload'),dict(session_id=6423,exit_code=0,cases=5,passed=5,stage='five original actual profile controls')],
      accepted_pages=0,human_reviewer=None,scope='Only profile day display nodes and existing date helper dependency. All original save/validation/navigation callbacks and other page branches retain equal AST. Previous reports preserve original source hashes; no full114-page or98-case replay claimed.')
    (out/'checkpoint.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Verified profile display only:15 new cases+5 existing controls, old action AST unchanged')
if __name__=='__main__':main()
