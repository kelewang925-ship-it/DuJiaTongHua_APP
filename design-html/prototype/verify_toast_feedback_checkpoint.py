"""Bind the red/green feedback proof and focused lifecycle regressions to exact sources."""
import hashlib
import json
from pathlib import Path

from verify_pet_controls import ROOT, DEMO, source


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    out=ROOT/'evidence/current/toast-feedback';baseline=read(ROOT/'evidence/baseline/toast-feedback/results.json');green=read(out/'results.json')
    scope=read(out/'source-scope.json');current=source()
    assert green['files']==current and green['styles']=={p.relative_to(DEMO).as_posix():sha(p) for p in (DEMO/'assets').glob('*.css')}
    assert set(name for name in current if baseline['files'][name]!=current[name])=={'assets/prototype-ui.js','assets/prototype-ui.css'}
    assert {name for name in green['styles'] if green['styles'][name]!=baseline['styles'][name]}=={'assets/prototype-ui.css'}
    assert baseline['script_sha256']==green['script_sha256']==sha(ROOT/'verify_toast_feedback.py')
    assert len(baseline['results'])==22 and sum(row['passed'] for row in baseline['results'])==14
    assert len(green['results'])==22 and all(row['passed'] and not row['errors'] for row in green['results'])
    assert scope['other_ui_ast_equal'] and scope['other_css_text_equal']
    assert scope['ui_before_sha256']==baseline['files']['assets/prototype-ui.js'] and scope['ui_after_sha256']==current['assets/prototype-ui.js']
    assert scope['css_before_sha256']==baseline['styles']['assets/prototype-ui.css'] and scope['css_after_sha256']==green['styles']['assets/prototype-ui.css']
    assert scope['script_sha256']==sha(ROOT/'audit_toast_scope.cjs')
    helper_reports={}
    boundary=read(ROOT/'evidence/current/submit-boundary-refresh/executions.json')
    for name,script,count,job in [('form-helper.json','verify_pending_form_contract.py',8,'form-helper'),('page-helper.json','verify_pending_guard_contract.py',12,'page-helper')]:
        payload=read(out/name)
        assert payload['files']==current and payload['styles']==green['styles']
        assert payload['script_sha256']==sha(ROOT/script)
        assert len(payload['results'])==count and all(row['passed'] and not row.get('errors') for row in payload['results'])
        for path,digest in next(row for row in boundary['results'] if row['name']==job)['restored_originals_sha256'].items():
            assert sha(ROOT/path)==digest,path
        helper_reports[name]=sha(out/name)
    retained={}
    for name in ['submit-boundary-refresh/checkpoint.json','list-state-refresh/checkpoint.json','design-state-capture/checkpoint.json']:
        path=ROOT/'evidence/current'/name;proof=read(path)
        assert proof['files']==baseline['files']
        if 'styles' in proof: assert proof['styles']==baseline['styles']
        retained[name]=dict(checkpoint_sha256=sha(path),source_role='Original pre-Toast source manifest retained. Non-Toast UI AST/CSS unchanged; notice handoff separately tested. Not a re-execution of old suites or screenshots.')
    checkpoint=dict(files=current,styles=green['styles'],feedback_cases=22,lifecycle_helper_cases=20,accepted_pages=0,
                    actual_executions=dict(baseline=dict(session=10366,exit_code=1,passed=14,failed=8),green=dict(session=11299,exit_code=0,passed=22),helpers=dict(session=41277,exit_code=0,passed=20)),
                    baseline_report_sha256=sha(ROOT/'evidence/baseline/toast-feedback/results.json'),green_report_sha256=sha(out/'results.json'),
                    source_scope_sha256=sha(out/'source-scope.json'),helper_reports_sha256=helper_reports,retained_proofs=retained,
                    script_sha256=sha(Path(__file__)),scope='Toast rendering/placement/handoff and20 focused lifecycle contracts; original data/navigation/guard logic and other CSS unchanged by AST/text containment. Human visual and hidden-action audit remain open.')
    (out/'checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(feedback=22,lifecycle_helpers=20,baseline_failed=8,accepted_pages=0)))


if __name__=='__main__':main()
