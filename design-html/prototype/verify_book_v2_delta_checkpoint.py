"""Verify current V2 deltas, source lineage and precise replay boundaries."""
import json,subprocess
from pathlib import Path
from verify_book_v2_reconciliation import ROOT,DEMO,dependencies,sha
from verify_book_template_preview_checkpoint import main as verify_previews
from build_book_v2_current_contracts import main as verify_controls

def load(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    verify_previews();verify_controls();files=dependencies()
    old=load(ROOT/'evidence/current/book-v2/verification-summary.json')
    changed={p.replace('\\','/') for p,h in old['hashes'].items() if sha(DEMO/p)!=h}
    expected={'assets/prototype-book.js','assets/prototype-book-editors.js','assets/prototype-book-v2.css','custom/m08-p08.html','pages/m08-p08.html'}
    assert changed==expected,changed
    for label,source in [('book-template-default','prototype-book.js'),('book-reply-default','prototype-book-editors.js')]:
        baseline=ROOT/f'evidence/baseline/{label}';patch=load(baseline/'patch.json');raw=(DEMO/'assets'/source).read_bytes()
        assert raw.count(patch['new'].encode())==1 and raw.replace(patch['new'].encode(),patch['old'].encode(),1)==(baseline/source).read_bytes()
        expected_hash=next(h for p,h in old['hashes'].items() if p.replace('\\','/')=='assets/'+source)
        assert sha(baseline/source)==expected_hash
    out=ROOT/'evidence/current/book-v2-controls';controls=load(out/'results.json')
    assert controls['new_executions']==14 and controls['retained_executions']==142
    for n in range(1,22):assert (DEMO/f'custom/m08-p{n:02d}.html').read_bytes()==(DEMO/f'pages/m08-p{n:02d}.html').read_bytes()
    node=r'C:\Users\kele\.nvmd\bin\node.exe'
    syntax=['prototype-book','prototype-book-store','prototype-book-editors','prototype-book-structure','prototype-book-v2','prototype-book-reader']
    for name in syntax:subprocess.run([node,'--check',str(DEMO/'assets'/(name+'.js'))],check=True)
    report=dict(passed=True,dependency_files=files,prior_v2_summary_sha256=sha(ROOT/'evidence/current/book-v2/verification-summary.json'),changed_since_prior_v2_summary=sorted(changed),current_initial_controls=156,new_control_executions=14,retained_control_executions=142,preview_cases=11,mirrored_routes=21,javascript_syntax_files=6,scope='Current V2 initial controls and named visual repairs. Original159 scenarios retain original source version; hidden/conditional/state reconciliation and full41 acceptance remain open.',producer_sha256=sha(Path(__file__)),human_accepted_pages=0)
    (out/'checkpoint.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS current V2 source lineage:5 declared deltas,21 mirrors,6 JS syntax checks,156 controls and11 preview cases')

if __name__=='__main__':main()
