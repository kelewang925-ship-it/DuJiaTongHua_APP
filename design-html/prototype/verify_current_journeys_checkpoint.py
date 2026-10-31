"""Verify exact-source journey evidence and explicitly retained baseline passes."""
import json
from replay_current_initial_controls import ROOT, deps, sha, dump

def main():
    base=ROOT/'evidence/baseline/continuous-journeys-20261031'
    current=ROOT/'evidence/current/continuous-journeys-20261031'
    reports=[json.loads((p/'results.json').read_text(encoding='utf-8')) for p in [base,current]]
    old,new=reports
    assert old['complete'] and not old['all_passed']
    assert [r['passed'] for r in old['results']]==[True,True,False,True]
    assert '阅读工具' in old['results'][2]['failure']
    assert new['complete'] and new['all_passed'] and len(new['results'])==4
    raw=current/'results-before-final-retained-case.json'
    assert sha(raw)==new['finalization']['raw_report_sha256']
    assert sha(ROOT/'finalize_current_journeys.py')==new['finalization']['sha256']
    assert json.loads(raw.read_text(encoding='utf-8'))['results']==new['results'][:3]
    assert old['dependencies']==new['dependencies']==deps()
    for folder,report in zip([base,current],reports):
        for n,h in report['dependencies'].items():assert sha(folder/'source'/n)==h,n
        for n,h in report['fixture_sha256'].items():assert sha(folder/'fixtures'/n)==h,n
    for n,h in new['fixture_sha256'].items():assert sha(ROOT/n)==h,n
    for index in [0,1,3]:
        row=new['results'][index]
        assert row['execution']=='retained-baseline-pass'
        assert row['provenance']['sha256']==sha(base/'results.json')
        assert row['provenance']['case']==old['results'][index]['case']
        assert {k:v for k,v in row.items() if k not in ['execution','provenance']}==old['results'][index]
    assert [len(r['steps']) for r in new['results']]==[11,2,22,19]
    journey=new['results'][2]
    assert journey['execution']=='fresh' and not journey['errors']
    stages={s['step']:s for s in journey['steps']}
    published=stages['book-published']['snapshot']
    assert len(published['books'][0]['pages'])==5
    exported=stages['book-real-export']['snapshot']
    assert exported['books'][0]['name']=='八模块共同回忆'
    assert exported['books'][0]['pages'][0]['supplements'][0]['author']=='星星'
    before=stages['logout-kept-content']['snapshot'];after=stages['relogin-content-retained']['snapshot']
    assert not before['session']['loggedIn'] and after['session']['loggedIn']
    assert {k:v for k,v in before.items() if k!='session'}=={k:v for k,v in after.items() if k!='session'}
    deleted=stages['book-deleted-sources-retained']['snapshot']
    assert deleted['books']==[]
    for k in ['records','moments','works','pet','relationship']:assert deleted[k]==after[k],k
    for name in ['book-published','relogin-content-retained','book-deleted-sources-retained']:
        assert (current/journey['case']/(name+'.png')).is_file()
    initial=json.loads((ROOT/'evidence/current/initial-controls-20261031-accessible/results.json').read_text(encoding='utf-8'))
    assert initial['dependencies']==deps()
    result={'passed':True,'dependencies':len(deps()),'journeys':4,'stage_records':54,'fresh_journeys':1,'retained_journeys':3,'baseline_report_sha256':sha(base/'results.json'),'current_report_sha256':sha(current/'results.json'),'human_accepted_pages':0,'scope':'Continuous workflows only; remaining conditions, layouts and original41 requirements remain open.'}
    dump(current/'checkpoint.json',result)
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
