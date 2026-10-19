"""Separate actual failure consumption from static test references."""
import ast
import hashlib
import json
from urllib.request import urlopen
from verify_pet_controls import ROOT, BASE, source


def main():
    out=ROOT/'evidence/current';files=source();h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    candidate_path=out/'failure-operation-candidates.json'
    candidate=json.loads(candidate_path.read_text(encoding='utf-8'))
    for name,sha in candidate['files'].items():assert h(ROOT.parent/'assets'/name)==sha
    trace_names=['pet-state','book-state','photo-state','settings-state','onboarding-fault',
                 'anniversary-state','capsule-state','diary-state','moment-state','workshop-state','pet-life-state',
                 'book-editor-draft','remaining-failures','last-failures']
    observed={};traces={};cases=0
    for name in trace_names:
        path=out/(name+'-failure-trace.json');v=json.loads(path.read_text(encoding='utf-8'))
        assert v['files']==files and v['exit_code']==0 and v['cases']==v['passed']
        assert h(ROOT/v['script'])==v['script_sha256']
        assert h(ROOT/v.get('trace_script_path','trace_failure_suite.py'))==v['trace_script_sha256']
        assert h(out/v['report'])==v['report_sha256']
        payload=json.loads((out/v['report']).read_text(encoding='utf-8'))
        rows=payload['results']if isinstance(payload,dict)else payload
        assert len(rows)==v['cases'] and all(r['passed']and not r.get('errors')for r in rows)
        for i,event in enumerate(v['events']):
            row=rows[event['context_index']]
            assert row['case']==event['case'] and row['passed']==event['case_passed']
            observed.setdefault(event['operation'],[]).append(dict(trace=path.name,event_index=i,case=event['case'],url=event['url']))
        traces[path.name]=dict(sha256=h(path),report=v['report'],report_sha256=v['report_sha256'],cases=v['cases'])
        cases+=v['cases']
    references={}
    for path in ROOT.glob('verify_*.py'):
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            if isinstance(node,ast.Constant)and isinstance(node.value,str):
                references.setdefault(node.value,set()).add(path.name)
    operations=sorted({c['operation']for c in candidate['candidates']})
    assert len(operations)==61
    entries=[dict(operation=op,source_sites=[c for c in candidate['candidates']if c['operation']==op],
                  status='observed_failure_in_passing_case'if op in observed else 'not_yet_traced',
                  runtime_evidence=observed.get(op,[]),static_test_references=sorted(references.get(op,[])))for op in operations]
    for op in sorted(set(observed)-set(operations)):
        entries.append(dict(operation=op,source_sites=[],status='observed_failure_in_passing_case',
                            runtime_evidence=observed[op],static_test_references=sorted(references.get(op,[])),
                            note='Dynamic operation observed; not included among the 61 literal source names.'))
    literal_observed=sum(op in observed for op in operations)
    matrix=dict(files=files,candidates_sha256=h(candidate_path),traces=traces,cases=cases,
                literal_operations=61,literal_observed=literal_observed,literal_untraced=61-literal_observed,
                observed_operations=len(observed),entries=entries,accepted_pages=0,
                scope='Failure hooks actually returned true and their containing case passed. Static references are discovery only; full operation branch/permission/timeout/keyboard/layout acceptance remains separate.')
    (out/'failure-operation-matrix.json').write_text(json.dumps(matrix,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# 失败操作执行矩阵','',f'本批{cases}个案例通过，实际触发{len(observed)}个不同失败操作。61个字面量入口中{literal_observed}个已观察、{61-literal_observed}个尚未追踪。','',
           '“已观察”仅证明所列案例中的失败被实际触发，案例完整断言通过；不代表该操作所有权限、取消、并发和布局条件完成。静态测试引用仅用于寻找下一步执行入口。','',
           '| 操作 | 当前追踪 | 实际案例 | 静态候选脚本 |','| --- | --- | --- | --- |']
    for entry in entries:
        lines.append('| '+entry['operation']+' | '+('已观察'if entry['runtime_evidence']else'未追踪')+' | '+
                     '、'.join(sorted({e['case']for e in entry['runtime_evidence']}))+' | '+
                     '、'.join(entry['static_test_references'])+' |')
    (ROOT/'FAILURE_OPERATION_MATRIX.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    for name,sha in files.items():
        with urlopen(BASE+name.replace('custom/','pages/',1),timeout=10)as response:assert hashlib.sha256(response.read()).hexdigest()==sha
    path=out/'current-evidence-state.json';state=json.loads(path.read_text(encoding='utf-8'));assert state['files']==files
    state.update(current_failure_trace_cases=cases,current_failure_consumed_operations=len(observed),
                 current_failure_literal_observed=literal_observed,current_failure_literal_untraced=61-literal_observed,
                 failure_candidates_are_unproven=literal_observed!=61,
                 failure_candidate_all_conditions_complete=False)
    path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=cases,observed_operations=len(observed),literal_observed=literal_observed,literal_untraced=61-literal_observed,accepted_pages=0)))


if __name__=='__main__':main()
