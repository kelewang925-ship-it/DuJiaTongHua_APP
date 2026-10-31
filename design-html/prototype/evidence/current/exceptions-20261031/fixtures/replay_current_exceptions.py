"""Run legacy exception suites into isolated evidence with actual consumed hooks."""
import argparse, ast, json, subprocess, sys, traceback
from pathlib import Path
from playwright.sync_api import Browser
from refresh_failure_traces import JOBS
from trace_failure_suite import TRACE
from replay_current_initial_controls import ROOT, DEMO, deps, sha, dump

OUT=ROOT/'evidence/current/exceptions-20261031'

def scripts():
    pending=[ROOT/Path(__file__).name]+[ROOT/n for n,_,_ in JOBS];found=set()
    while pending:
        path=pending.pop()
        if path in found:continue
        found.add(path)
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            names=[node.module] if isinstance(node,ast.ImportFrom) and node.module else [v.name for v in node.names] if isinstance(node,ast.Import) else []
            for name in names:
                other=ROOT/(name.split('.')[0]+'.py')
                if other.is_file() and other not in found:pending.append(other)
    return {p.name:sha(p) for p in sorted(found)}

def child(script,report):
    folder=OUT/Path(script).stem;folder.mkdir()
    path=ROOT/script;tree=ast.parse(path.read_text(encoding='utf-8'),filename=str(path));changed=0
    for node in tree.body:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='OUT' for t in node.targets):
            node.value=ast.Call(func=ast.Name(id='Path',ctx=ast.Load()),args=[ast.Constant(str(folder))],keywords=[]);changed+=1
    assert changed==1
    ast.fix_missing_locations(tree)
    events=[];contexts=[];original=Browser.new_context
    def context(browser,*args,**kwargs):
        c=original(browser,*args,**kwargs);index=len(contexts);contexts.append(c)
        c.expose_binding('__recordConsumedFailure',lambda origin,event:events.append({**event,'context_index':index}))
        c.add_init_script(TRACE);return c
    Browser.new_context=context;sys.argv=[str(path)];code=0
    try:exec(compile(tree,str(path),'exec'),{'__file__':str(path),'__name__':'__main__'})
    except SystemExit as e:code=e.code or 0
    except Exception:code=1;(folder/'runner-error.txt').write_text(traceback.format_exc(),encoding='utf-8')
    finally:Browser.new_context=original
    payload=json.loads((folder/report).read_text(encoding='utf-8')) if (folder/report).exists() else []
    rows=payload.get('results',[]) if isinstance(payload,dict) else payload
    for event in events:
        index=event['context_index'];event.update(case=rows[index]['case'] if index<len(rows) else None,case_passed=rows[index]['passed'] if index<len(rows) else False)
    dump(folder/'execution.json',{'script':script,'report':report,'exit_code':code,'cases':len(rows),'passed':sum(bool(r['passed']) for r in rows),'contexts':len(contexts),'events':events,'redirect':'Only top-level OUT assignment changed in compiled AST; archived original fixture bytes preserved.'})
    return code

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--child');parser.add_argument('--report');args=parser.parse_args()
    if args.child:return child(args.child,args.report)
    OUT.mkdir(parents=True,exist_ok=True);assert not (OUT/'results.json').exists()
    files=deps();fixtures=scripts()
    for sub,mapping,origin in [('source',files,DEMO),('fixtures',fixtures,ROOT)]:
        for name in mapping:
            target=OUT/sub/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((origin/name).read_bytes())
    preserved={str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'evidence/current').glob('*.json')}
    rows=[]
    for script,report,count in JOBS:
        print('START',script,flush=True)
        result=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--child',script,'--report',report])
        folder=OUT/Path(script).stem
        data=json.loads((folder/'execution.json').read_text(encoding='utf-8'))
        assert result.returncode==data['exit_code']
        data.update(expected_cases=count,execution_sha256=sha(folder/'execution.json'))
        rows.append(data)
        assert deps()==files and scripts()==fixtures
        assert all(sha(ROOT/n)==h for n,h in preserved.items())
        dump(OUT/'results.json',{'dependencies':files,'fixture_sha256':fixtures,'preserved_reports':preserved,'results':rows,'complete':len(rows)==len(JOBS),'expected_suites':14,'expected_cases':110,'all_passed':len(rows)==14 and all(r['exit_code']==0 and r['cases']==r['passed']==r['expected_cases'] for r in rows),'scope':'Actual legacy exception cases and consumed mock failures against current source. Not every conditional branch or full acceptance.','human_accepted_pages':0})
        print('DONE',script,data['passed'],'/',data['cases'],flush=True)
    return 0 if all(r['exit_code']==0 for r in rows) else 1

if __name__=='__main__':raise SystemExit(main())
