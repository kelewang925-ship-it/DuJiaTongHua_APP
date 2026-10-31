"""Verify current factory contracts,114 observations and published token tables."""
import json
from collections import Counter
from replay_current_initial_controls import ROOT,DEMO,deps,sha,dump

def main():
    folder=ROOT/'evidence/current/components-20261031';report=folder/'results.json';data=json.loads(report.read_text(encoding='utf-8'));summary=json.loads((folder/'summary.json').read_text(encoding='utf-8'))
    assert data['complete'] and data['all_passed'] and summary['passed']
    assert data['dependencies']=={**deps(),'prototype/components.html':sha(ROOT/'components.html')}
    assert sha(report)==summary['report_sha256'] and sha(ROOT/'publish_current_components.py')==summary['producer_sha256']
    for sub,mapping in [('source',data['dependencies']),('fixtures',data['fixture_sha256'])]:
        for n,h in mapping.items():
            assert sha(folder/sub/n)==h,n
            if sub=='fixtures':assert sha(ROOT/n)==h,n
    assert len(data['component_contracts'])==56 and all(r['passed'] and not r['errors'] for r in data['component_contracts'])
    counts=Counter(r['component'] for r in data['component_contracts']);assert len(counts)==14 and set(counts.values())=={4}
    assert len({(r['component'],r['width'],r['motion']) for r in data['component_contracts']})==56
    pages=data['page_observations'];ids={v['id'] for v in json.loads((DEMO/'manifest.json').read_text(encoding='utf-8'))}
    assert len(pages)==len(ids)==114 and {r['page'] for r in pages}==ids
    assert all(r['passed'] and not r['errors'] for r in pages)
    assert len(summary['tokens'])==43
    for name,token in summary['tokens'].items():
        assert token['resolved']==114 and len(token['values'])==1 and token['values'][0]
        assert {r['observation']['tokens'][name] for r in pages}==set(token['values'])
    for name,total in summary['component_totals'].items():
        values=[r['observation']['components'][name] for r in pages]
        assert sum(v>0 for v in values)==total['pages_present'] and sum(values)==total['instances']
    history=ROOT/'evidence/history/pre-current-components-af7c4b1';manifest=json.loads((history/'manifest.json').read_text(encoding='utf-8'))
    assert manifest['files']==summary['history']
    for n,h in summary['history'].items():assert sha(history/n)==h,n
    for n,h in summary['artifacts'].items():assert sha(ROOT/n)==h,n
    component_table=(ROOT/'COMPONENT_COVERAGE.md').read_text(encoding='utf-8')
    assert {line.split('|')[1].strip() for line in component_table.splitlines() if line.startswith('| m')}==ids
    token_table=(ROOT/'TOKEN_COVERAGE.md').read_text(encoding='utf-8')
    assert {line.split('|')[1].strip() for line in token_table.splitlines() if line.startswith(('| --prototype-','| --ui-'))}==set(summary['tokens'])
    result={'passed':True,'producer_sha256':sha(ROOT/'verify_current_components_checkpoint.py'),'report_sha256':sha(report),'summary_sha256':sha(folder/'summary.json'),'dependency_files':len(data['dependencies']),'component_types':14,'factory_contracts':56,'canonical_pages':114,'root_tokens':43,'root_tokens_resolved_and_consistent':True,'human_accepted_pages':0,'scope':'Factory behavior and canonical root observations only. Local component/token use, conditional states and full41 acceptance remain separate.'}
    dump(folder/'checkpoint.json',result);print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
