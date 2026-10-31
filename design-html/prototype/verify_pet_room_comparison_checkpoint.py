"""Bind historical comparison evidence to exact presentation-only integration changes."""
import json
from pathlib import Path
from verify_pet_room_comparison import ROOT,DEMO,sha,dependencies

def main():
    base=ROOT/'evidence/baseline/pet-room-comparison';current=ROOT/'evidence/current/pet-room-comparison';read=lambda p:json.loads(p.read_text(encoding='utf-8'))
    red=read(base/'results.json');green=read(current/'results.json');patch=read(base/'patch.json')
    assert len(red['results'])==4 and not any(r['passed'] for r in red['results'])
    assert all('No comparison of saved historical room snapshots' in r['failure'] for r in red['results'])
    assert red['producer_sha256']==sha(base/'producer.py')==green['producer_sha256']==sha(ROOT/'verify_pet_room_comparison.py')
    assert red['fixture_sha256']==green['fixture_sha256']==sha(ROOT/'verify_pet_controls.py')
    assert green['dependencies']==dependencies()
    assert len(green['results'])==25 and all(r['passed'] and not r['page_errors'] for r in green['results'])
    assert set(patch)=={'assets/prototype-pet-life.js','assets/prototype-pet-draft-preview.js','custom/m07-p14.html','pages/m07-p14.html'}
    for n,h in red['dependencies'].items():
        assert sha(base/'source'/n)==h
        raw=(DEMO/n).read_bytes()
        for a,b in reversed(patch.get(n,[])):
            assert raw.count(b.encode())==1;raw=raw.replace(b.encode(),a.encode())
        assert raw==(base/'source'/n).read_bytes(),n
    assert set(green['dependencies'])-set(red['dependencies'])=={'assets/prototype-pet-room-comparison.js','assets/prototype-pet-room-comparison.css'}
    assert (DEMO/'custom/m07-p14.html').read_bytes()==(DEMO/'pages/m07-p14.html').read_bytes()
    counts={kind:sum(r['kind']==kind for r in green['results']) for kind in ['layout','control','save','peer']};assert counts=={'layout':20,'control':3,'save':1,'peer':1}
    value={'passed':True,'cases':25,'case_counts':counts,'dependencies':dependencies(),'exact_four_file_integration_reversal':True,'model_snapshots_save_rules_inventory_and_original_art_unchanged':True,'screenshots':{p.name:sha(p) for p in sorted(current.glob('*.png'))},'human_accepted_pages':0,'scope':'p14 actual room log before/after snapshots, missing/unknown slots explicit, five widths, original exits, actual p15 save/reopen and peer current-room update. Semantic SVG preview, not watercolor pixel-match acceptance; full114 final audit remains open.','producer_sha256':sha(Path(__file__))}
    (current/'checkpoint.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS25:20 snapshot layouts,3 original exits,1 save/reopen,1 peer update;4 exact reversals')

if __name__=='__main__':main()
