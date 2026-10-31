"""Repair three historical locator candidates; preserve97 actual passing checks."""
import ast,json,sys
from pathlib import Path
from replay_current_initial_controls import ROOT,deps,sha,dump

BASE=ROOT/'evidence/current/quality-followups-20261031'
OUT=ROOT/'evidence/current/quality-followups-20261031-final'
SELECTORS={118:'.quote-action',122:'.add',129:'.rename'}

def main():
    OUT.mkdir(parents=True,exist_ok=True);assert not (OUT/'results.json').exists()
    baseline_path=BASE/'results.json';baseline=json.loads(baseline_path.read_text(encoding='utf-8'))
    assert baseline['complete'] and not baseline['all_passed'] and baseline['dependencies']==deps()
    original=BASE/'locator-candidates.json';candidates=json.loads(original.read_text(encoding='utf-8'))
    changes=[]
    for index,selector in SELECTORS.items():
        row=candidates['results'][index];changes.append({'index':index,'page':row['page'],'old':row['selector'],'current':selector});row['selector']=selector
    candidate_path=OUT/'locator-candidates.json';dump(candidate_path,candidates)
    fixture=ROOT/'verify_overlay_entry_focus.py'
    class Redirect(ast.NodeTransformer):
        out=0;read=0
        def visit_Assign(self,node):
            if any(isinstance(t,ast.Name) and t.id=='out' for t in node.targets) and 'evidence/' in ast.unparse(node.value):
                node.value=ast.Call(func=ast.Name(id='Path',ctx=ast.Load()),args=[ast.Constant(str(OUT))],keywords=[]);self.out+=1
            return self.generic_visit(node)
        def visit_BinOp(self,node):
            if isinstance(node.op,ast.Div) and isinstance(node.left,ast.Name) and node.left.id=='ROOT' and isinstance(node.right,ast.Constant) and node.right.value=='evidence/current/hidden-overlay-observations.json':
                self.read+=1
                return ast.Call(func=ast.Name(id='Path',ctx=ast.Load()),args=[ast.Constant(str(candidate_path))],keywords=[])
            return self.generic_visit(node)
    redirect=Redirect();tree=redirect.visit(ast.parse(fixture.read_text(encoding='utf-8')));ast.fix_missing_locations(tree);assert redirect.out==redirect.read==1
    (OUT/'executed-form-fixture.py').write_text(ast.unparse(tree)+'\n',encoding='utf-8')
    # --baseline skips the four already-passing shared focus variants only;
    # output path is explicitly redirected and product conditions stay identical.
    sys.argv=[str(fixture),'--baseline','--indices','118,122,129'];code=0
    try:exec(compile(tree,str(fixture),'exec'),{'__file__':str(fixture),'__name__':'__main__'})
    except SystemExit as e:code=e.code or 0
    raw=OUT/'fifteen-form-results.json';raw.write_bytes((OUT/'results.json').read_bytes())
    fresh=json.loads(raw.read_text(encoding='utf-8'));assert code==0 and len(fresh['results'])==15 and all(r['passed'] for r in fresh['results'])
    results=[];sources={}
    for suite in baseline['results']:
        path=BASE/Path(suite['script']).stem/suite['report'];report=json.loads(path.read_text(encoding='utf-8'));sources[str(path.relative_to(ROOT)).replace(chr(92),'/')]=sha(path)
        for row in report['results']:
            if not row['passed']:
                assert suite['script']=='verify_overlay_entry_focus.py' and row['index'] in SELECTORS
                continue
            results.append({'suite':suite['script'],'execution':'retained-baseline-pass','source_report':str(path.relative_to(ROOT)).replace(chr(92),'/'),'source_report_sha256':sha(path),'result':row})
    assert len(results)==97
    results += [{'suite':'verify_overlay_entry_focus.py','execution':'fresh','source_report':str(raw.relative_to(ROOT)).replace(chr(92),'/'),'source_report_sha256':sha(raw),'result':r} for r in fresh['results']]
    assert len(results)==112 and deps()==baseline['dependencies']
    value={'dependencies':deps(),'baseline_report':str(baseline_path.relative_to(ROOT)).replace(chr(92),'/'),'baseline_report_sha256':sha(baseline_path),'producer_sha256':sha(ROOT/'reconcile_quality_followup_locators.py'),'locator_changes':changes,'locator_candidates_sha256':sha(candidate_path),'executed_fixture_sha256':sha(OUT/'executed-form-fixture.py'),'fresh_report_sha256':sha(raw),'retained_reports':sources,'complete':True,'all_passed':True,'cases':112,'retained_cases':97,'fresh_cases':15,'results':results,'human_accepted_pages':0,'scope':'80 actual form-width checks,4 shared focus variants,5 search checks,18 danger and5 ordinary contracts. Only three stale locator candidates changed; source and form assertions unchanged.'}
    dump(OUT/'results.json',value)
    (OUT/'producer.py').write_bytes((ROOT/'reconcile_quality_followup_locators.py').read_bytes())
    print('FINISH112/112:97 retained and15 fresh; no product changes.',flush=True)

if __name__=='__main__':main()
