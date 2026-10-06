"""Preserve book reports, rerun normal/exception scenarios with source binding."""
import sys,json,hashlib,subprocess,shutil
from verify_book_controls import ROOT,source
OUT=ROOT/'evidence/current';HISTORY=ROOT/'evidence/history/pre-book-controls-bd1e3b8';HISTORY.mkdir(parents=True,exist_ok=True);files=source();reports={}
for prefix in ['book-']:
    for p in OUT.glob(prefix+'*'):
        if p.suffix!='.json' or p.name.startswith(('book-control','book-hidden','book-guard')):continue
        dest=HISTORY/p.name
        if not dest.exists():shutil.copy2(p,dest)
for script,name in [('verify_book_flow.py', 'book-flow-results.json'), ('verify_book_states.py', 'book-state-results.json'), ('verify_book_extended.py', 'book-extended-results.json'), ('verify_book_structure.py', 'book-structure-results.json'), ('verify_book_cover.py', 'book-cover-results.json'), ('verify_book_global.py', 'book-global-results.json'), ('verify_book_editor_draft.py', 'book-editor-draft-results.json')]:
    run=subprocess.run([sys.executable,str(ROOT/script)]);p=OUT/name;v=json.loads(p.read_text(encoding='utf-8'));assert files==source();reports[name]=dict(exit_code=run.returncode,cases=len(v),passed=sum(r['passed']for r in v),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
assert files==source();(OUT/'book-control-regression-source.json').write_text(json.dumps(dict(files=files,reports=reports),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if all(v['exit_code']==0 and v['passed']==v['cases']for v in reports.values())else 1)
