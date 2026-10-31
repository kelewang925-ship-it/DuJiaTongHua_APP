"""Pin draft rendering and action evidence without promoting it to full-product acceptance."""
import json
from pathlib import Path
from verify_pet_draft_previews import ROOT,DEMO,sha,dependencies

def main():
    read=lambda p:json.loads(p.read_text(encoding='utf-8'))
    base=ROOT/'evidence/baseline/pet-draft-previews';prior=ROOT/'evidence/baseline/pet-draft-previews-before-tab-clearance';current=ROOT/'evidence/current/pet-draft-previews'
    red=read(base/'results.json');first=read(prior/'results.json');green=read(current/'results.json');actions=read(current/'actions.json')
    assert len(red['results'])==4 and not any(r['passed'] for r in red['results'])
    assert all('No visual preview for the actual draft selection' in r['failure'] for r in red['results'])
    assert len(first['results'])==69 and sum(r['passed'] for r in first['results'])==60
    assert all(r['kind']=='layout' and r['value'][0]==12 and r['value'][1]==320 for r in first['results'] if not r['passed'])
    assert red['producer_sha256']==sha(base/'producer.py')==first['producer_sha256']==sha(prior/'producer.py')==green['producer_sha256']==sha(ROOT/'verify_pet_draft_previews.py')
    assert actions['producer_sha256']==sha(ROOT/'verify_pet_draft_actions.py')
    assert actions['catalog_sha256']==sha(ROOT/'evidence/current/page-contracts.json')
    for report in [red,first,green,actions]:assert report['fixture_sha256']==sha(ROOT/'verify_pet_controls.py')
    assert green['dependencies']==actions['dependencies']==dependencies()
    assert len(green['results'])==69 and len(actions['results'])==25
    assert all(r['passed'] and not r['page_errors'] for r in green['results']+actions['results'])
    for directory,report in [(base,red),(prior,first)]:
        for n,h in report['dependencies'].items():assert sha(directory/'source'/n)==h
    patch=read(base/'patch.json');expected={'assets/prototype-pet-life.js','assets/prototype-pet-item-preview.js',*[f'{directory}/m07-p{n}.html' for directory in ['custom','pages'] for n in [12,15]]}
    assert set(patch)==expected
    for n in red['dependencies']:
        raw=(DEMO/n).read_bytes()
        for a,b in reversed(patch.get(n,[])):
            if not b:
                assert n=='assets/prototype-pet-life.js' and a=="const preview=button('',()=>{},'pet-life-preview');preview.disabled=true;"
                anchor=b"if(n===12){let group='\xe9\x85\x8d\xe9\xa5\xb0',selected=pet.outfit||null;"
                assert raw.count(anchor)==1;raw=raw.replace(anchor,anchor+a.encode())
            else:
                assert raw.count(b.encode())==1;raw=raw.replace(b.encode(),a.encode())
        assert raw==(base/'source'/n).read_bytes(),n
    additions={'assets/prototype-pet-draft-preview.js','assets/prototype-pet-draft-preview.css'}
    assert set(green['dependencies'])-set(red['dependencies'])==additions
    css='assets/prototype-pet-draft-preview.css'
    tail=b'\nmain.screen[data-pet-page="12"] .art-closet{display:none}\nmain.screen[data-pet-page="12"] .art-bottom{top:87%;height:13%;background-position:left -184.2cqw}\nmain.screen[data-pet-page="15"] .art-middle{background-image:none}\n'
    raw=(DEMO/css).read_bytes();assert raw.endswith(tail)
    assert raw[:-len(tail)].replace(b'top:22%;height:27%',b'top:20%;height:29%')==(prior/'source'/css).read_bytes()
    for n,h in first['dependencies'].items():
        if n!=css:assert h==green['dependencies'][n],n
    for n in [12,15]:assert (DEMO/f'custom/m07-p{n}.html').read_bytes()==(DEMO/f'pages/m07-p{n}.html').read_bytes()
    counts={kind:sum(r['kind']==kind for r in green['results']+actions['results']) for kind in ['layout','kind','save','dirty','resource','control','peer','unlock']}
    assert counts=={'layout':57,'kind':4,'save':2,'dirty':2,'resource':4,'control':21,'peer':2,'unlock':2}
    value={'passed':True,'cases':94,'case_counts':counts,'dependencies':dependencies(),'six_existing_file_reversal':True,'model_prices_inventory_guard_and_art_unchanged':True,'screenshots':{p.name:sha(p) for p in sorted(current.glob('*.png'))},'human_accepted_pages':0,'scope':'p12/p15 native draft schematics: eight outfits plus none, ten room candidates, four pet kinds, save failure/retry/reopen, dirty discard, original controls, peer guards, unlock selection. Semantic editable SVGs, not watercolor pixel-match acceptance. Other states and full114 final acceptance remain open.','producer_sha256':sha(Path(__file__))}
    (current/'checkpoint.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS94:69 visual/draft checks +25 original/peer/unlock actions; six exact integration reversals')

if __name__=='__main__':main()
