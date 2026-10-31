"""Verify current-source112 followup outcomes and exact locator-only correction."""
import json
from collections import Counter
from replay_current_initial_controls import ROOT,deps,sha,dump

def main():
    base=ROOT/'evidence/current/quality-followups-20261031';folder=ROOT/'evidence/current/quality-followups-20261031-final'
    path=folder/'results.json';final=json.loads(path.read_text(encoding='utf-8'));baseline_path=ROOT/final['baseline_report'];baseline=json.loads(baseline_path.read_text(encoding='utf-8'))
    assert final['complete'] and final['all_passed'] and final['dependencies']==baseline['dependencies']==deps()
    assert sha(baseline_path)==final['baseline_report_sha256'] and baseline['complete'] and not baseline['all_passed']
    assert len(final['results'])==112
    for sub,mapping in [('source',baseline['dependencies']),('fixtures',baseline['fixture_sha256'])]:
        for n,h in mapping.items():
            assert sha(base/sub/n)==h,n
            if sub=='fixtures':assert sha(ROOT/n)==h,n
    for n,h in baseline['preserved_reports'].items():assert sha(ROOT/n)==h,n
    assert sha(ROOT/'reconcile_quality_followup_locators.py')==final['producer_sha256']==sha(folder/'producer.py')
    assert sha(folder/'executed-form-fixture.py')==final['executed_fixture_sha256']
    assert sha(folder/'fifteen-form-results.json')==final['fresh_report_sha256']
    assert sha(folder/'locator-candidates.json')==final['locator_candidates_sha256']
    old=json.loads((base/'locator-candidates.json').read_text(encoding='utf-8'));new=json.loads((folder/'locator-candidates.json').read_text(encoding='utf-8'))
    assert len(final['locator_changes'])==3
    for change in final['locator_changes']:
        index=change['index'];assert old['results'][index]['selector']==change['old'] and new['results'][index]['selector']==change['current']
        old['results'][index]['selector']=change['current']
    assert old==new
    counts=Counter();keys=set();retained=0;fresh=0
    for row in final['results']:
        report=ROOT/row['source_report'];assert sha(report)==row['source_report_sha256']
        data=json.loads(report.read_text(encoding='utf-8'))
        result=row['result'];assert result in data['results'] and result['passed'] and not result.get('errors')
        key=(row['suite'],result.get('width'),result.get('index'),result.get('case'))
        assert key not in keys;keys.add(key);counts[row['suite']]+=1
        if row['execution']=='fresh':
            assert result['index'] in [118,122,129] and result['persisted'];fresh+=1
        else:
            assert row['execution']=='retained-baseline-pass';retained+=1
    assert retained==97 and fresh==15
    assert dict(counts)=={'verify_overlay_entry_focus.py':84,'verify_initial_quality_repairs.py':5,'verify_danger_confirmations.py':18,'verify_danger_primary_contract.py':5}
    for suite in baseline['results']:
        suite_folder=base/suite['script'].removesuffix('.py')
        assert sha(suite_folder/'execution.json')==suite['execution_sha256']
        assert sha(suite_folder/suite['report'])==suite['report_sha256']
    result={'passed':True,'producer_sha256':sha(ROOT/'verify_quality_followups_checkpoint.py'),'report_sha256':sha(path),'product_dependencies':len(deps()),'cases':112,'retained_cases':97,'fresh_cases':15,'real_form_width_cases':80,'shared_focus_variants':4,'search_cases':5,'danger_cases':18,'ordinary_cases':5,'human_accepted_pages':0,'scope':'Declared form, search, danger and ordinary contracts only; not every hidden or concurrent condition or native IME acceptance.'}
    dump(folder/'checkpoint.json',result);print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
