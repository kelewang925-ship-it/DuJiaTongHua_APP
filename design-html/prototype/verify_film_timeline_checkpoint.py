"""Check the precise film-only display patch and unchanged source/storage/generation contracts."""
import json,subprocess
from pathlib import Path
from verify_film_timeline import ROOT,DEMO,dependencies,sha

def load(p):return json.loads(p.read_text(encoding='utf-8'))

def main():
    base=ROOT/'evidence/baseline/film-timeline';current=ROOT/'evidence/current/film-timeline';patch=load(base/'patch.json');red=load(base/'results.json');green=load(current/'results.json')
    for name,replacements in patch.items():
        raw=(DEMO/name).read_bytes()
        for old,new in reversed(replacements):assert raw.count(new.encode())==1;raw=raw.replace(new.encode(),old.encode(),1)
        assert raw==(base/'source'/name).read_bytes(),name
    assert (DEMO/'custom/m05-p05.html').read_bytes()==(DEMO/'pages/m05-p05.html').read_bytes()
    assert len(red['results'])==20 and not any(r['passed'] for r in red['results'])
    assert red['producer_sha256']==sha(base/'producer.py')
    assert len(green['results'])==39 and all(r['passed'] for r in green['results'])
    assert green['dependency_files']==dependencies() and green['producer_sha256']==sha(ROOT/'verify_film_timeline.py')
    assert green['fixture_sha256']==red['fixture_sha256']==sha(ROOT/'verify_workshop_controls.py')
    assert set(dependencies())-set(red['dependency_files'])=={'assets/prototype-film-timeline.js','assets/prototype-film-timeline.css'}
    assert all(dependencies()[n]==h for n,h in red['dependency_files'].items() if n not in patch)
    counts={k:sum(r['kind']==k for r in green['results']) for k in ['layout','control','flow']};assert counts=={'layout':20,'control':11,'flow':8}
    consumers=sorted(p.stem for p in (DEMO/'custom').glob('*.html') if 'prototype-film-timeline.js' in p.read_text(encoding='utf-8'));assert consumers==['m05-p05']
    for name in ['prototype-film-timeline.js','prototype-workshop.js']:subprocess.run([r'C:\Users\kele\.nvmd\bin\node.exe','--check',str(DEMO/'assets'/name)],check=True)
    value={'passed':True,'dependency_files':dependencies(),'browser_cases':39,'case_counts':counts,'exact_three_existing_file_reversal':True,'single_page_consumer':consumers,'unchanged_store_and_artwork':True,'human_accepted_pages':0,'scope':'m05-p05 visible timeline only. Stored source ID order now controls display; picker/save/generate callbacks remain unchanged. Other module record skins, typography and full114 acceptance remain open.','producer_sha256':sha(Path(__file__))}
    (current/'checkpoint.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS39 film timeline cases; exact3 file reversals, single-page helper, original store/artwork and2 JS syntax checks')

if __name__=='__main__':main()
