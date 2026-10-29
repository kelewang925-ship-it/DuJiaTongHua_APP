"""Prove the two-page layout-only patch and current full-name/control evidence."""
import json
from pathlib import Path
from verify_pet_header_layout import ROOT,DEMO,dependencies,sha

def load(p):return json.loads(p.read_text(encoding='utf-8'))

def main():
    base=ROOT/'evidence/baseline/pet-header-layout';explore=ROOT/'evidence/baseline/pet-header-layout-before-avatar-contract';current=ROOT/'evidence/current/pet-header-layout';patch=load(base/'patch.json');red=load(base/'results.json');green=load(current/'results.json');old=load(explore/'results.json')
    assert len(patch)==4
    for name,replacements in patch.items():
        raw=(DEMO/name).read_bytes()
        for a,b in reversed(replacements):assert raw.count(b.encode())==1;raw=raw.replace(b.encode(),a.encode(),1)
        assert raw==(base/'source'/name).read_bytes(),name
    for page in ['m07-p11','m07-p25']:assert (DEMO/f'custom/{page}.html').read_bytes()==(DEMO/f'pages/{page}.html').read_bytes()
    assert len(old['results'])==40 and not any(r['passed'] for r in old['results']);assert old['producer_sha256']==sha(explore/'producer.py')
    assert old['dependency_files']==red['dependency_files']
    assert len(red['results'])==40 and sum(r['passed'] for r in red['results'])==5;assert red['producer_sha256']==sha(base/'producer.py')
    assert all(r['value'][0]=='m07-p25' and r['value'][2]==0 for r in red['results'] if r['passed'])
    assert len(green['results'])==62 and all(r['passed'] for r in green['results']);assert green['dependency_files']==dependencies();assert green['producer_sha256']==sha(ROOT/'verify_pet_header_layout.py')
    assert green['fixture_sha256']==red['fixture_sha256']==old['fixture_sha256']==sha(ROOT/'verify_pet_controls.py')
    assert set(green['dependency_files'])==set(red['dependency_files']);assert all(dependencies()[p]==h for p,h in red['dependency_files'].items() if p not in patch)
    counts={kind:sum(r['kind']==kind for r in green['results']) for kind in ['layout','control','flow']};assert counts=={'layout':40,'control':20,'flow':2}
    controls={page:sum(r['kind']=='control' and r['value'][0]==page for r in green['results']) for page in ['m07-p11','m07-p25']};assert controls=={'m07-p11':9,'m07-p25':11}
    value={'passed':True,'dependency_files':dependencies(),'browser_cases':62,'case_counts':counts,'initial_controls_per_page':controls,'exact_four_html_reversal':True,'all_javascript_css_assets_and_artwork_unchanged':True,'human_accepted_pages':0,'scope':'p11/p25 header and full-name layout only, pet12/owner20 at five widths, original controls and two long-name flows. Other P2-VIS-PET-INLINE pages and full114 acceptance remain open.','producer_sha256':sha(Path(__file__))}
    (current/'checkpoint.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS62 header cases;40 full-name layouts,20 original controls,2 long-name flows;4 exact HTML reversals and unchanged shared scripts/artwork')

if __name__=='__main__':main()
