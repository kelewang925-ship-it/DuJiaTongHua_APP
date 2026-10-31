"""Bind selected-item evidence to current sources and preserve the failed baseline."""
import json,re
from pathlib import Path
from verify_pet_item_previews import ROOT,DEMO,dependencies,sha

def main():
    read=lambda p:json.loads(p.read_text(encoding='utf-8'))
    base=ROOT/'evidence/baseline/pet-item-previews'
    prior=ROOT/'evidence/baseline/pet-item-previews-before-lamp-fill'
    current=ROOT/'evidence/current/pet-item-previews'
    red=read(base/'results.json');old=read(prior/'results.json');green=read(current/'results.json')
    assert len(red['results'])==4 and not any(r['passed'] for r in red['results'])
    assert all('No labeled current-item preview' in r['failure'] for r in red['results'])
    assert len(old['results'])==56 and all(r['passed'] for r in old['results'])
    assert len(green['results'])==56 and all(r['passed'] and not r['page_errors'] for r in green['results'])
    assert red['producer_sha256']==sha(base/'producer.py')==old['producer_sha256']==sha(prior/'producer.py')==green['producer_sha256']==sha(ROOT/'verify_pet_item_previews.py')
    assert red['fixture_sha256']==old['fixture_sha256']==green['fixture_sha256']==sha(ROOT/'verify_pet_controls.py')
    assert green['dependencies']==dependencies()
    for n,h in red['dependencies'].items():assert sha(base/'source'/n)==h
    patch=read(base/'patch.json')
    assert set(patch)=={'custom/m07-p13.html','custom/m07-p16.html','pages/m07-p13.html','pages/m07-p16.html','assets/prototype-pet-resource-presentation.js'}
    for n in red['dependencies']:
        raw=(DEMO/n).read_bytes()
        for a,b in reversed(patch.get(n,[])):
            assert raw.count(b.encode())==1;raw=raw.replace(b.encode(),a.encode())
        assert raw==(base/'source'/n).read_bytes(),n
    additions={'assets/prototype-pet-item-preview.js','assets/prototype-pet-item-preview.css'}
    assert set(green['dependencies'])-set(red['dependencies'])==additions
    renderer='assets/prototype-pet-item-preview.js'
    a=b'<path d="M30 101V34c0-30 56-30 56 0v9M18 101h52v9H18Z"/>'
    b=b'<path fill="none" d="M30 101V34c0-30 56-30 56 0v9"/><path d="M18 101h52v9H18Z"/>'
    raw=(DEMO/renderer).read_bytes();assert raw.count(b)==1
    assert raw.replace(b,a)==(prior/'source'/renderer).read_bytes()
    for n,h in old['dependencies'].items():
        assert h==(sha(prior/'source'/n) if n in additions else green['dependencies'][n])
    for n in [13,16]:assert (DEMO/f'custom/m07-p{n}.html').read_bytes()==(DEMO/f'pages/m07-p{n}.html').read_bytes()
    counts={k:sum(r['kind']==k for r in green['results']) for k in ['layout','control','flow']}
    assert counts=={'layout':50,'control':4,'flow':2}
    gallery=read(current/'vector-gallery.json')
    assert gallery['kind']=='native-vector-asset-review-board-not-app-page'
    assert gallery['renderer_sha256']==sha(DEMO/renderer)
    assert gallery['producer_sha256']==sha(ROOT/'capture_pet_item_preview_gallery.py')==sha(prior/'gallery-producer.py')
    assert gallery['html_sha256']==sha(current/'vector-gallery.html')
    assert gallery['screenshot_sha256']==sha(current/'vector-gallery.png')
    vectors=re.findall(r'<svg\b.*?</svg>',(current/'vector-gallery.html').read_text(encoding='utf-8'))
    assert len(vectors)==len(gallery['items'])==18
    import hashlib
    assert [hashlib.sha256(v.encode()).hexdigest() for v in vectors]==[v['svg_sha256'] for v in gallery['items']]
    value={'passed':True,'cases':56,'case_counts':counts,'dependencies':dependencies(),'exact_five_existing_file_reversals':True,'lamp_fill_visual_correction_preserved':True,'catalog_model_prices_navigation_and_original_art_unchanged':True,'native_vector_items':18,'human_accepted_pages':0,'scope':'p13/p16 selected-item semantic vector illustrations and actual ownership/availability. Not pixel-matched watercolor assets. p12/p15 full previews, other pet states and full114 acceptance remain open.','producer_sha256':sha(Path(__file__))}
    (current/'checkpoint.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS56:50 layouts,4 original controls,2 real unlock failure/retry flows;18 vector assets;exact integration reversal')

if __name__=='__main__':main()
