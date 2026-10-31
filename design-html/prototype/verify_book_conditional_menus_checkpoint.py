"""Verify the red/green scope and the exact single-function product change."""
import json
from pathlib import Path
from verify_book_v2_reconciliation import ROOT,DEMO,dependencies,sha

def main():
    base=ROOT/'evidence/baseline/book-conditional-menus';current=ROOT/'evidence/current/book-conditional-menus'
    read=lambda p:json.loads(p.read_text(encoding='utf-8'))
    red=read(base/'results.json');green=read(current/'results.json')
    assert len(red['results'])==12
    assert {r['case'] for r in red['results'] if not r['passed']}=={'rename-published','rename-draft','archive-published','delete-draft','add-draft','publish-draft'}
    assert all(not r['errors'] for r in red['results'])
    assert len(green['results'])==42 and all(r['passed'] and not r['errors'] for r in green['results'])
    expected={(k,n,w) for w in [320,390,430] for k,names in [('library',['rename-published','rename-draft','archive-published','delete-draft','add-draft','publish-draft','unrelated-category','closed-listener']),('bookmark',['choose','cancel','escape','empty'])] for n in names}
    expected|={('regression',n,390) for n in ['library-tabs','library-open-published','library-open-draft','library-open-archive','library-empty-draft-archive','library-cancel']}
    assert {(r['kind'],r['case'],r['width']) for r in green['results']}==expected
    assert red['producer_sha256']==green['producer_sha256']==sha(base/'producer.py')==sha(ROOT/'verify_book_conditional_menus.py')
    assert red['fixture_sha256']==green['fixture_sha256']=={n:sha(ROOT/n) for n in green['fixture_sha256']}
    assert green['dependencies']==dependencies()
    assert set(red['dependencies'])==set(green['dependencies'])
    assert [n for n in red['dependencies'] if red['dependencies'][n]!=green['dependencies'][n]]==['assets/prototype-book-v2.js']
    assert sha(base/'prototype-book-v2.js')==red['dependencies']['assets/prototype-book-v2.js']
    old=(base/'prototype-book-v2.js').read_bytes();new=(DEMO/'assets/prototype-book-v2.js').read_bytes()
    split=lambda raw:(raw[:raw.index(b'  async function library(')],raw[raw.index(b'\n  function shelf('):])
    assert split(old)==split(new)
    for n,h in green['dependencies'].items():assert sha(current/'source'/n)==h,n
    assert sha(current/'producer.py')==green['producer_sha256']
    for n,h in green['fixture_sha256'].items():assert sha(current/'fixtures'/n)==h,n
    # Only append the two narrow follow-up records; never promote acceptance flags.
    previous=read(base/'queue.json')
    queue=read(ROOT/'queue.json');assert len(queue)==len(previous)==114
    for before,after in zip(previous,queue):
        after=dict(after)
        if before['id'] in ['m08-p01','m08-p17']:
            assert len(after['follow_up'])==len(before.get('follow_up',[]))+1
            assert after['follow_up'][-1]['reference']=='BOOK_CONDITIONAL_MENUS.md'
            after['follow_up']=after['follow_up'][:-1]
            if 'follow_up' not in before:after.pop('follow_up')
        assert before==after,before['id']
    result={'passed':True,'fresh_cases':42,'baseline_passed':6,'baseline_failed':6,'dependencies':dependencies(),'single_library_function_change':True,'all_other_source_dependencies_unchanged':True,'queue_acceptance_fields_unchanged':True,'human_accepted_pages':0,'producer_sha256':sha(Path(__file__)),'scope':'Three widths: actual cross-tab library updates and standalone bookmark outcomes; six original library regressions. Historical V2 reports retain their original source versions. Full114 and original41 audit remain open.'}
    (current/'checkpoint.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS42;6 baseline failures reproduced; single library function;114 queue acceptance fields unchanged')

if __name__=='__main__':main()
