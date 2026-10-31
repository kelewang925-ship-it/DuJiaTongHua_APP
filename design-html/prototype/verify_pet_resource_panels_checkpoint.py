"""Bind resource/inventory evidence and exact five-file presentation integration."""
import json
from pathlib import Path
from verify_pet_resource_panels import ROOT,DEMO,dependencies,sha

def main():
    base=ROOT/'evidence/baseline/pet-resource-panels';prior=ROOT/'evidence/baseline/pet-resource-panels-before-readonly-flow';current=ROOT/'evidence/current/pet-resource-panels';read=lambda p:json.loads(p.read_text(encoding='utf-8'))
    red=read(base/'results.json');first=read(prior/'results.json');green=read(current/'results.json');patch=read(base/'patch.json')
    assert len(red['results'])==30 and not any(r['passed'] for r in red['results'])
    reasons={reason:sum(reason in r['failure'] for r in red['results']) for reason in ['Requirement escapes card or overlaps explanation','Explanation overlaps action or escapes card','Owned target must not request more resources']};assert reasons=={'Requirement escapes card or overlaps explanation':15,'Explanation overlaps action or escapes card':9,'Owned target must not request more resources':6}
    assert red['producer_sha256']==sha(base/'producer.py')==first['producer_sha256']==sha(prior/'producer.py')
    assert len(first['results'])==38 and sum(r['passed'] for r in first['results'])==36
    assert all(r['kind']=='layout' and r['value'][1]==320 and r['value'][2]=='large' for r in first['results'] if not r['passed'])
    addition="    assert inventory.get_by_role('button').count()==0,'Read-only inventory categories must not add inert controls'\n"
    assert (ROOT/'verify_pet_resource_panels.py').read_text(encoding='utf-8').replace(addition,'')==(prior/'producer.py').read_text(encoding='utf-8')
    assert green['producer_sha256']==sha(ROOT/'verify_pet_resource_panels.py')
    assert red['fixture_sha256']==first['fixture_sha256']==green['fixture_sha256']==sha(ROOT/'verify_pet_controls.py')
    assert green['dependencies']==dependencies()
    assert len(green['results'])==38 and all(r['passed'] for r in green['results'])
    for directory,report in [(base,red),(prior,first)]:
        for n,h in report['dependencies'].items():assert sha(directory/'source'/n)==h
    assert set(patch)=={'custom/m07-p13.html','pages/m07-p13.html','custom/m07-p16.html','pages/m07-p16.html','assets/prototype-pet-life.js'}
    for n in red['dependencies']:
        raw=(DEMO/n).read_bytes()
        for a,b in reversed(patch.get(n,[])):assert raw.count(b.encode())==1;raw=raw.replace(b.encode(),a.encode())
        assert raw==(base/'source'/n).read_bytes(),n
    assert set(green['dependencies'])-set(red['dependencies'])=={'assets/prototype-pet-resource-presentation.js','assets/prototype-pet-resource-presentation.css'}
    for n in [13,16]:assert (DEMO/f'custom/m07-p{n}.html').read_bytes()==(DEMO/f'pages/m07-p{n}.html').read_bytes()
    counts={k:sum(r['kind']==k for r in green['results']) for k in ['layout','control','return']};assert counts=={'layout':30,'control':4,'return':4}
    value={'passed':True,'cases':38,'case_counts':counts,'dependency_files':dependencies(),'exact_four_html_and_one_branch_reversal':True,'existing_model_inventory_prices_navigation_and_art_unchanged':True,'human_accepted_pages':0,'scope':'p13 crown/p16 lamp requirements and real owned list, three widths/five states, original controls and enough/owned return routes. Other selected-item illustration previews, long-name headers and full114 acceptance remain open.','producer_sha256':sha(Path(__file__))}
    (current/'checkpoint.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS38:30 resource/inventory layouts,4 original controls,4 selection returns;five exact integration reversals')

if __name__=='__main__':main()
