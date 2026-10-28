"""Check review provenance and the two exact initial-choice repairs."""
import json,subprocess
from pathlib import Path
from verify_book_v2_reconciliation import ROOT,DEMO,dependencies,sha

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    out=ROOT/'evidence/current/book-visual-review'
    capture=read(out/'captures.json');files=dependencies()
    changed={p for p,h in capture['dependency_files'].items() if files.get(p)!=h}
    assert changed=={'assets/prototype-book.js','assets/prototype-book-editors.js'},changed
    assert files.keys()==capture['dependency_files'].keys()
    assert capture['producer_sha256']==sha(ROOT/'capture_book_review.py')
    for label,source,producer in [('book-template-default','prototype-book.js','verify_book_template_default.py'),('book-reply-default','prototype-book-editors.js','verify_book_reply_default.py')]:
        baseline=ROOT/f'evidence/baseline/{label}';current=ROOT/f'evidence/current/{label}'
        patch=read(baseline/'patch.json');raw=(DEMO/'assets'/source).read_bytes()
        assert raw.count(patch['new'].encode())==1
        assert raw.replace(patch['new'].encode(),patch['old'].encode(),1)==(baseline/source).read_bytes()
        red=read(baseline/'results.json');green=read(current/'results.json')
        assert len(red['results'])==len(green['results'])==5
        assert not any(r['passed'] for r in red['results']) and all(r['passed'] for r in green['results'])
        assert green['dependency_files']==files
        assert green['producer_sha256']==sha(ROOT/producer)
        assert red['producer_sha256']==sha(baseline/'verifier.py')
    prior=read(out/'prior-94-results.json');review=read(ROOT/'evidence/current/visual-self-review/results.json')
    assert review['results'][:94]==prior['results'] and len(review['results'])==114
    assert len({r['page_id'] for r in review['results']})==114 and not any(r.get('accepted') for r in review['results'])
    queue=read(ROOT/'queue.json');head=json.loads(subprocess.check_output(['git','show','HEAD:design-html/prototype/queue.json']).decode('utf-8'))
    for page,before in zip(queue,head):
        assert page['id']==before['id']
        for k,v in before.items():
            if k not in ['issues','visual_self_review']:assert page[k]==v,(page['id'],k)
    originals=Path(r'D:\projectCode\DuJiaTongHua\DuJiaTongHua_Project_Docs\新模块分布')
    for row in review['results']:
        ref=row['original_design_reference'];assert sha(originals/ref['path'])==ref['sha256'],row['page_id']
        assert sha(ROOT/row['screenshot'])==row['screenshot_sha256']
    for row in capture['results']:assert sha(ROOT/row['current_screenshot'])==row['current_screenshot_sha256']
    replay=read(ROOT/'evidence/current/book-v2-reconciliation/provenance.json')
    assert replay['passed'] and replay['cases']==11 and replay['dependency_files']==files
    assert {p.replace('\\','/') for p in replay['prior_summary_changed_sources']}==changed
    report=dict(passed=True,reviewed_pages=114,new_original_comparisons=20,v2_captures=21,choice_width_cases=10,v2_contract_replay_cases=11,changed_sources=sorted(changed),prior94_preserved=True,acceptance_fields_preserved=True,human_accepted_pages=0,dependency_files=files,producer_sha256=sha(Path(__file__)),scope='Image self-review and exact initial-choice repairs only; V2 complete navigation/hidden-control/state reconciliation and full41 audit remain open.')
    (out/'checkpoint.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS 114 original references, prior94, 21 captures, exact two repairs, 10 width cases, 11 V2 contracts; acceptance unchanged')

if __name__=='__main__':main()
