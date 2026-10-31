"""Bind shelf-return proof to preserved failures, contracts and source bytes."""
import json
from pathlib import Path
from verify_book_v2_reconciliation import ROOT,DEMO,dependencies,sha

def main():
    base=ROOT/'evidence/baseline/book-shelf-return';attempt=ROOT/'evidence/baseline/book-shelf-return-before-return-contract';current=ROOT/'evidence/current/book-shelf-return'
    read=lambda p:json.loads(p.read_text(encoding='utf-8'))
    red=read(base/'results.json');prior=read(attempt/'results.json');green=read(current/'results.json')
    assert len(red['results'])==7 and not any(r['passed'] for r in red['results'])
    assert not any(r['errors'] for r in red['results'])
    assert len(prior['results'])==63 and sum(r['passed'] for r in prior['results'])==60
    assert {(r['case'],r['width']) for r in prior['results'] if not r['passed']}=={('archive-published',w) for w in [320,390,430]}
    assert all('to_be_focused' in r['failure'] for r in prior['results'] if not r['passed'])
    assert len(green['results'])==66 and all(r['passed'] and not r['errors'] for r in green['results'])
    assert sum(r['kind']=='return' for r in green['results'])==24
    assert sum(r['kind']=='library' for r in green['results'])==24
    assert sum(r['kind']=='bookmark' for r in green['results'])==12
    assert sum(r['kind']=='regression' for r in green['results'])==6
    expected_returns={'rename','delete-only','archive-only','publish-draft','replace-selected','progress','keep-selected','open-archive-after-last'}
    assert {(r['case'],r['width']) for r in green['results'] if r['kind']=='return'}=={(n,w) for n in expected_returns for w in [320,390,430]}
    assert green['dependencies']==prior['dependencies']==dependencies()
    assert set(red['dependencies'])==set(green['dependencies'])
    assert [n for n in red['dependencies'] if red['dependencies'][n]!=green['dependencies'][n]]==['assets/prototype-book-v2.js']
    for folder,report in [(base,red),(attempt,prior),(current,green)]:
        assert report['producer_sha256']==sha(folder/'producer.py')
        for n,h in report['dependencies'].items():assert sha(folder/'source'/n)==h,n
        for n,h in report['fixture_sha256'].items():assert sha(folder/'fixtures'/n)==h,n
    assert green['producer_sha256']==sha(ROOT/'verify_book_shelf_return.py')
    assert red['producer_sha256']==prior['producer_sha256']!=green['producer_sha256']
    assert red['fixture_sha256']==prior['fixture_sha256']==green['fixture_sha256']=={n:sha(ROOT/n) for n in green['fixture_sha256']}
    raw=(DEMO/'assets/prototype-book-v2.js').read_bytes()
    for a,b in reversed(read(base/'patch.json')):
        assert raw.count(b.encode())==1;raw=raw.replace(b.encode(),a.encode())
    assert raw==(base/'source/assets/prototype-book-v2.js').read_bytes()
    old=read(base/'queue.json');new=read(ROOT/'queue.json');assert len(old)==len(new)==114
    for before,after in zip(old,new):
        if before['id']=='m08-p01':
            after=dict(after);assert after['follow_up'][-1]['reference']=='BOOK_SHELF_RETURN.md';after['follow_up']=after['follow_up'][:-1]
        assert before==after,before['id']
    value={'passed':True,'fresh_cases':66,'baseline_failed':7,'preserved_first_attempt_passed':60,'preserved_first_attempt_total':63,'test_contract_correction':'After the last published book is archived, cancel goes to the empty shelf rather than restoring a removed shelf trigger. Product source unchanged during test correction; direct open-archive navigation added at three widths.','exact_product_patch_reversed':True,'other_source_dependencies_unchanged':True,'queue_acceptance_fields_unchanged':True,'human_accepted_pages':0,'dependencies':dependencies(),'producer_sha256':sha(Path(__file__)),'scope':'Shelf return and the named menu/bookmark regressions only. Full114 and original41 goal remain open.'}
    (current/'checkpoint.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS66;7 baseline failures;60/63 first attempt preserved; exact product reversal;114 queue flags unchanged')

if __name__=='__main__':main()
