"""Verify exact achievement display hook, native progress evidence and original reward logic."""
import json,subprocess
from pathlib import Path
from verify_pet_achievement_progress import ROOT,DEMO,dependencies,sha

def load(p):return json.loads(p.read_text(encoding='utf-8'))

def main():
    baseline=ROOT/'evidence/baseline/pet-achievement-progress';prior=ROOT/'evidence/baseline/pet-achievement-progress-before-reward-label';current=ROOT/'evidence/current/pet-achievement-progress'
    patch=load(baseline/'patch.json');red=load(baseline/'results.json');old=load(prior/'results.json');green=load(current/'results.json')
    for name,replacements in patch.items():
        raw=(DEMO/name).read_bytes()
        for a,b in reversed(replacements):assert raw.count(b.encode())==1;raw=raw.replace(b.encode(),a.encode(),1)
        assert raw==(baseline/'source'/name).read_bytes(),name
    assert (DEMO/'custom/m07-p20.html').read_bytes()==(DEMO/'pages/m07-p20.html').read_bytes()
    assert len(red['results'])==20 and not any(r['passed'] for r in red['results']);assert red['producer_sha256']==sha(baseline/'producer.py')
    assert len(old['results'])==26 and all(r['passed'] for r in old['results']);assert old['producer_sha256']==sha(prior/'producer.py')
    css='assets/prototype-pet-achievement-progress.css';assert old['dependency_files'][css]==sha(prior/'prototype-pet-achievement-progress.css')
    assert all(h==dependencies()[name] for name,h in old['dependency_files'].items() if name!=css)
    diagnostic=load(prior/'reward-overlap.json');assert diagnostic['dependency_files']==old['dependency_files'] and diagnostic['result']['overlap'] is True
    assert len(green['results'])==26 and all(r['passed'] for r in green['results']);assert green['dependency_files']==dependencies();assert green['producer_sha256']==sha(ROOT/'verify_pet_achievement_progress.py')
    assert green['fixture_sha256']==red['fixture_sha256']==old['fixture_sha256']==sha(ROOT/'verify_pet_controls.py')
    assert set(dependencies())-set(red['dependency_files'])=={'assets/prototype-pet-achievement-progress.js',css}
    assert all(dependencies()[name]==h for name,h in red['dependency_files'].items() if name not in patch)
    counts={kind:sum(r['kind']==kind for r in green['results']) for kind in ['layout','control','flow']};assert counts=={'layout':20,'control':2,'flow':4}
    consumers=sorted(p.stem for p in (DEMO/'custom').glob('*.html') if 'prototype-pet-achievement-progress.js' in p.read_text(encoding='utf-8'));assert consumers==['m07-p20']
    for name in ['prototype-pet-achievement-progress.js','prototype-pet-life.js']:subprocess.run([r'C:\Users\kele\.nvmd\bin\node.exe','--check',str(DEMO/'assets'/name)],check=True)
    result={'passed':True,'dependency_files':dependencies(),'browser_cases':26,'case_counts':counts,'exact_three_file_reversal':True,'unchanged_achievement_counts_targets_rewards_claim_logic_and_artwork':True,'consumers':consumers,'human_accepted_pages':0,'scope':'Four achievement rows plus reward label on m07-p20. Existing model drives all state; typography, pet inline/catalog/preview findings and full114 final acceptance remain open.','producer_sha256':sha(Path(__file__))}
    (current/'checkpoint.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS26 achievement cases, exact3 source reversals, native model-driven bars, preserved reward/store/artwork and2 JS syntax checks')

if __name__=='__main__':main()
