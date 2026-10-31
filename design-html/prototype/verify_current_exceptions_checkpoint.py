"""Bind isolated exception executions to current product and immutable fixtures."""
import json
from replay_current_initial_controls import ROOT, deps, sha, dump
from replay_current_exceptions import JOBS, scripts

def main():
    folder=ROOT/'evidence/current/exceptions-20261031'
    data=json.loads((folder/'results.json').read_text(encoding='utf-8'))
    assert data['complete'] and data['all_passed'] and len(data['results'])==14
    assert data['dependencies']==deps() and data['fixture_sha256']==scripts()
    for sub,mapping in [('source',data['dependencies']),('fixtures',data['fixture_sha256'])]:
        for n,h in mapping.items():assert sha(folder/sub/n)==h,n
    for n,h in data['preserved_reports'].items():assert sha(ROOT/n)==h,n
    operations={};total=0;events=0;reports={}
    for (script,report,count),row in zip(JOBS,data['results']):
        case_dir=folder/script.removesuffix('.py')
        assert sha(case_dir/'execution.json')==row['execution_sha256']
        raw=json.loads((case_dir/'execution.json').read_text(encoding='utf-8'))
        assert {k:v for k,v in row.items() if k not in ['expected_cases','execution_sha256']}==raw
        assert row['exit_code']==0 and row['cases']==row['passed']==row['contexts']==count
        payload=json.loads((case_dir/report).read_text(encoding='utf-8'))
        reports[str((case_dir/report).relative_to(ROOT)).replace(chr(92),'/')]=sha(case_dir/report)
        results=payload['results'] if isinstance(payload,dict) else payload
        assert len(results)==count and all(r['passed'] and not r.get('errors') for r in results)
        total+=count
        for event in row['events']:
            assert event['case_passed'] and event['case']==results[event['context_index']]['case']
            assert event['url'].startswith('http://127.0.0.1:8765/')
            operations.setdefault(event['operation'],[]).append({'script':script,'case':event['case'],'url':event['url']})
            events+=1
    assert total==110
    for report in ['initial-controls-20261031-accessible','continuous-journeys-20261031']:
        previous=json.loads((ROOT/'evidence/current'/report/'results.json').read_text(encoding='utf-8'))
        assert previous['dependencies']==deps()
    result={'passed':True,'producer_sha256':sha(ROOT/'verify_current_exceptions_checkpoint.py'),'report_sha256':sha(folder/'results.json'),'reports_sha256':reports,'product_dependencies':len(deps()),'suites':14,'cases':110,'failure_events':events,'distinct_consumed_operations':len(operations),'operations':operations,'human_accepted_pages':0,'scope':'Named exception cases and actual consumed failures. No claim of all branches, layouts, native devices, or complete41 acceptance.'}
    dump(folder/'checkpoint.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['operations','reports_sha256']},ensure_ascii=False))

if __name__=='__main__':main()
