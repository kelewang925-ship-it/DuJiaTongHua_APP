"""Verify exact pet-rest patch boundaries without blessing unrelated book edits."""
import hashlib,json,re
from pathlib import Path
from html.parser import HTMLParser
from verify_pet_rest_name import dependencies,ROOT,DEMO,sha

class Headings(HTMLParser):
    def __init__(self):super().__init__();self.active=False;self.texts=[]
    def handle_starttag(self,tag,attrs):
        if tag=='h2':self.active=True;self.texts.append('')
    def handle_endtag(self,tag):
        if tag=='h2':self.active=False
    def handle_data(self,data):
        if self.active:self.texts[-1]+=data

def main():
    baseline=ROOT/'evidence/baseline/pet-rest-name'
    current=ROOT/'evidence/current/pet-rest-name'
    patch=json.loads((baseline/'patch.json').read_text(encoding='utf-8'))
    source=(DEMO/'assets/prototype-pet.js').read_bytes()
    assert source.count(patch['selector'].encode())==1
    assert source.replace(patch['selector'].encode(),patch['original_selector'].encode(),1)==(baseline/'prototype-pet.js').read_bytes()
    for folder in ['custom','pages']:
        html=(DEMO/f'{folder}/m07-p07.html').read_bytes()
        for key in ['css','long_name_css']:
            chunk=patch[key].encode();assert html.count(chunk)==1
            html=html.replace(chunk,b'',1)
        assert html.count(patch['wrapped_group'].encode())==1
        html=html.replace(patch['wrapped_group'].encode(),patch['original_group'].encode(),1)
        assert html==(baseline/f'source-{folder}.html').read_bytes(),folder
    assert (DEMO/'custom/m07-p07.html').read_bytes()==(DEMO/'pages/m07-p07.html').read_bytes()
    consumers={}
    for path in sorted((DEMO/'custom').glob('*.html')):
        text=path.read_text(encoding='utf-8')
        if 'src="../assets/prototype-pet.js"' in text:
            parser=Headings();parser.feed(text)
            consumers[path.stem]=[t for t in parser.texts if any(n in t for n in ['糯米','小满','阿舟'])]
    assert set(consumers)=={f'm07-p{n:02d}' for n in range(1,12)},consumers
    assert {k:v for k,v in consumers.items() if v}=={'m07-p07':['糯米想先睡一会儿']},consumers
    report=json.loads((current/'results.json').read_text(encoding='utf-8'))
    assert report['dependency_files']==dependencies()
    assert report['script_sha256']==sha(ROOT/'verify_pet_rest_name.py')
    assert report['fixture_script_sha256']==sha(ROOT/'verify_pet_controls.py')
    assert report['expected_cases']==29 and len(report['results'])==29
    assert all(r['passed'] for r in report['results'])
    for sub,expected,passed in [('header-overlap',18,13),('layout-18',18,18),('rest-only',18,18)]:
        archived=current/sub
        r=json.loads((archived/'results.json').read_text(encoding='utf-8'))
        assert len(r['results'])==expected and sum(x['passed'] for x in r['results'])==passed
        assert r['script_sha256']==sha(archived/'verifier.py'),sub
    red=json.loads((baseline/'results.json').read_text(encoding='utf-8'))
    assert len(red['results'])==15 and not any(x['passed'] for x in red['results'])
    assert red['script_sha256']==sha(baseline/'verifier.py')
    result=dict(scope='Pet rest page and its actual dependencies; other modules are not certified.',passed=True,cases=29,dependency_files=dependencies(),shared_consumers=consumers,exact_patch_reversal=True,mirrors_equal=True,human_accepted_pages=0,verifier_sha256=sha(Path(__file__)))
    (current/'checkpoint.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS exact patch reversal, 11 shared consumers, 29 browser cases, archived red/green provenance')

if __name__=='__main__':main()
