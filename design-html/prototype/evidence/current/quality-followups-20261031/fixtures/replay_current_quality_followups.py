"""Isolate current short-viewport form and destructive-dialog checks."""
import argparse,ast,json,subprocess,sys,traceback
from pathlib import Path
from replay_current_initial_controls import ROOT,DEMO,deps,fixture_files,sha,dump

OUT=ROOT/'evidence/current/quality-followups-20261031'
JOBS=[('verify_overlay_entry_focus.py','results.json',84),('verify_initial_quality_repairs.py','repair-behavior-results.json',5),('verify_danger_confirmations.py','danger-confirmation-results.json',18),('verify_danger_primary_contract.py','danger-primary-contract-results.json',5)]

def child(script,report):
    folder=OUT/Path(script).stem;folder.mkdir();path=ROOT/script
    class Redirect(ast.NodeTransformer):
        changed=0
        def visit_Assign(self,node):
            if any(isinstance(t,ast.Name) and t.id in ['OUT','out'] for t in node.targets) and 'evidence/' in ast.unparse(node.value):
                node.value=ast.Call(func=ast.Name(id='Path',ctx=ast.Load()),args=[ast.Constant(str(folder))],keywords=[]);self.changed+=1
            return self.generic_visit(node)
        def visit_BinOp(self,node):
            if isinstance(node.op,ast.Div) and isinstance(node.left,ast.Name) and node.left.id=='ROOT' and isinstance(node.right,ast.Constant) and node.right.value=='evidence/current/initial-quality/repair-behavior-results.json':
                self.changed+=1
                return ast.Call(func=ast.Name(id='Path',ctx=ast.Load()),args=[ast.Constant(str(folder/report))],keywords=[])
            return self.generic_visit(node)
    redirect=Redirect();tree=redirect.visit(ast.parse(path.read_text(encoding='utf-8')));ast.fix_missing_locations(tree);assert redirect.changed==1
    sys.argv=[str(path)];code=0
    try:exec(compile(tree,str(path),'exec'),{'__file__':str(path),'__name__':'__main__','Path':Path})
    except SystemExit as e:code=e.code or 0
    except Exception:code=1;(folder/'runner-error.txt').write_text(traceback.format_exc(),encoding='utf-8')
    data=json.loads((folder/report).read_text(encoding='utf-8')) if (folder/report).exists() else {'results':[]}
    rows=data['results'];dump(folder/'execution.json',{'script':script,'report':report,'report_sha256':sha(folder/report) if (folder/report).exists() else None,'exit_code':code,'cases':len(rows),'passed':sum(bool(r['passed']) for r in rows),'redirected_output_paths':redirect.changed})
    return code

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--child');parser.add_argument('--report');args=parser.parse_args()
    if args.child:return child(args.child,args.report)
    OUT.mkdir(parents=True,exist_ok=True);assert not (OUT/'results.json').exists()
    files=deps();scripts=fixture_files();scripts.update({n:sha(ROOT/n) for n in [Path(__file__).name,'audit_initial_quality.py','verify_overlay_form_saves.py',*(v[0] for v in JOBS)]})
    original_files=[p for p in (ROOT/'evidence/current').glob('*.json')]+[p for p in (ROOT/'evidence/current/initial-quality').glob('*') if p.is_file()]+[ROOT/'evidence/current/overlay-entry-focus/results.json']
    preserved={str(p.relative_to(ROOT)):sha(p) for p in original_files if p.is_file()}
    for sub,mapping,origin in [('source',files,DEMO),('fixtures',scripts,ROOT)]:
        for n in mapping:
            p=OUT/sub/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((origin/n).read_bytes())
    candidates=ROOT/'evidence/current/hidden-overlay-observations.json';(OUT/'locator-candidates.json').write_bytes(candidates.read_bytes())
    rows=[]
    for script,report,count in JOBS:
        print('START',script,flush=True)
        result=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--child',script,'--report',report])
        folder=OUT/Path(script).stem;row=json.loads((folder/'execution.json').read_text(encoding='utf-8'))
        assert row['exit_code']==result.returncode;row.update(expected=count,execution_sha256=sha(folder/'execution.json'));rows.append(row)
        assert deps()==files and all(sha(ROOT/n)==h for n,h in scripts.items())
        assert all(sha(ROOT/n)==h for n,h in preserved.items())
        dump(OUT/'results.json',{'dependencies':files,'fixture_sha256':scripts,'preserved_reports':preserved,'locator_candidates_sha256':sha(candidates),'results':rows,'complete':len(rows)==4,'all_passed':len(rows)==4 and all(r['exit_code']==0 and r['cases']==r['passed']==r['expected'] for r in rows),'expected_cases':112,'human_accepted_pages':0,'scope':'80 real form-width save checks plus4 shared focus variants,5 search/selected-focus checks,18 dangerous dialogs and5 ordinary confirmations. Historical selectors are candidates only; actual titles, focus, storage and cancellation re-executed.'})
        print('DONE',script,row['passed'],'/',row['cases'],flush=True)
    return 0 if all(r['exit_code']==0 for r in rows) else 1

if __name__=='__main__':raise SystemExit(main())
