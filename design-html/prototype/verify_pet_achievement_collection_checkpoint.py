"""Check real overview state evidence and the one-branch presentation hook scope."""
import json
from pathlib import Path
from verify_pet_achievement_collection import ROOT,DEMO,dependencies,sha

def main():
    base=ROOT/'evidence/baseline/pet-achievement-collection';prior=ROOT/'evidence/baseline/pet-achievement-collection-before-claim-wait';current=ROOT/'evidence/current/pet-achievement-collection'
    read=lambda p:json.loads(p.read_text(encoding='utf-8'))
    red=read(base/'results.json');first=read(prior/'results.json');green=read(current/'results.json');patch=read(base/'patch.json')
    assert len(red['results'])==25 and not any(r['passed'] for r in red['results'])
    assert all("Locator expected to be visible" in r['failure'] and '.next' in r['failure'] for r in red['results'])
    assert red['producer_sha256']==sha(base/'producer.py')==first['producer_sha256']==sha(prior/'producer.py')
    assert sum(r['passed'] for r in first['results'])==36
    assert all(r['kind']=='flow' and r['value']=='claim-retry' for r in first['results'] if not r['passed'])
    old=(prior/'producer.py').read_text(encoding='utf-8');a="p.locator('.claim').click();expect(p.locator('.claim')).to_be_disabled();assert p.evaluate";b="p.locator('.claim').click();expect(p.locator('.prototype-toast')).to_contain_text('成就奖励已到账');expect(p.locator('.claim')).to_be_disabled();assert p.evaluate"
    assert old.count(a)==1 and old.replace(a,b)==(ROOT/'verify_pet_achievement_collection.py').read_text(encoding='utf-8')
    assert green['producer_sha256']==sha(ROOT/'verify_pet_achievement_collection.py')
    assert first['dependencies']==green['dependencies']
    assert red['fixture_sha256']==green['fixture_sha256']==sha(ROOT/'verify_pet_controls.py')
    assert green['dependencies']==dependencies()
    assert len(green['results'])==37 and all(r['passed'] for r in green['results'])
    counts={k:sum(r['kind']==k for r in green['results']) for k in ['layout','control','flow']};assert counts=={'layout':25,'control':10,'flow':2}
    assert set(patch)=={'custom/m07-p21.html','pages/m07-p21.html','assets/prototype-pet-life.js'}
    for n,h in red['dependencies'].items():
        assert sha(base/'source'/n)==h
        raw=(DEMO/n).read_bytes()
        for a,b in reversed(patch.get(n,[])):assert raw.count(b.encode())==1;raw=raw.replace(b.encode(),a.encode())
        assert raw==(base/'source'/n).read_bytes(),n
    added=set(green['dependencies'])-set(red['dependencies']);assert added=={'assets/prototype-pet-achievement-collection.js','assets/prototype-pet-achievement-collection.css'}
    assert (DEMO/'custom/m07-p21.html').read_bytes()==(DEMO/'pages/m07-p21.html').read_bytes()
    assert sum(len(v) for v in patch.values())==5
    value={'passed':True,'cases':37,'case_counts':counts,'dependency_files':dependencies(),'exact_two_html_and_one_branch_hook_reversal':True,'existing_achievement_model_rewards_claims_and_art_unchanged':True,'human_accepted_pages':0,'scope':'p21 seven editable medal/progress cards plus truthful pending/next/all-claimed summary; original controls, actual claim failure retry and cross-tab interaction. Not full pet typography/skin or full114 acceptance.','producer_sha256':sha(Path(__file__))}
    (current/'checkpoint.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS37:25 layouts,10 original controls,2 real flows;exact presentation-only integration reversal')

if __name__=='__main__':main()
