"""Bind p22 header evidence to exact HTML bytes and unchanged dependencies."""
import json
from pathlib import Path
from verify_pet_collection_header import ROOT,DEMO,dependencies,sha

def main():
    base=ROOT/'evidence/baseline/pet-collection-header';current=ROOT/'evidence/current/pet-collection-header'
    red=json.loads((base/'results.json').read_text(encoding='utf-8'));green=json.loads((current/'results.json').read_text(encoding='utf-8'))
    assert len(red['results'])==15 and not any(r['passed'] for r in red['results'])
    assert all('.count overlaps .pet-life-extra' in r['failure'] for r in red['results'])
    assert red['producer_sha256']==sha(base/'producer.py')==green['producer_sha256']==sha(ROOT/'verify_pet_collection_header.py')
    assert red['fixture_sha256']==green['fixture_sha256']==sha(ROOT/'verify_pet_controls.py')
    assert len(green['results'])==28 and all(r['passed'] for r in green['results'])
    assert green['dependencies']==dependencies()
    changed=['custom/m07-p22.html','pages/m07-p22.html']
    css=('/* Reserve the top bar for count/actions and keep full names left of the portrait. */\n'
         '.screen[data-pet-page="22"] .count{left:18%;right:auto;top:1.5%;font-size:4cqw;line-height:1.3;white-space:nowrap}\n'
         '.screen[data-pet-page="22"] .title{left:18%;right:42%;max-width:none;font-size:8cqw;line-height:1.1;overflow-wrap:anywhere}\n'
         '.screen[data-pet-page="22"] .pet-collection-name{display:block;font-size:5.5cqw;line-height:1.1}\n').replace('\n','\r\n').encode()
    old='<h1 class="title">糯米的<br>收藏图鉴</h1>'.encode();new='<h1 class="title"><span class="pet-collection-name">糯米的</span>收藏图鉴</h1>'.encode()
    for n,h in red['dependencies'].items():
        assert sha(base/'source'/n)==h
        raw=(DEMO/n).read_bytes()
        if n in changed:
            assert raw.count(css)==1 and raw.count(new)==1
            raw=raw.replace(css,b'').replace(new,old)
        assert raw==(base/'source'/n).read_bytes(),n
    assert (DEMO/changed[0]).read_bytes()==(DEMO/changed[1]).read_bytes()
    counts={k:sum(r['kind']==k for r in green['results']) for k in ['layout','control']};assert counts=={'layout':15,'control':13}
    value={'passed':True,'cases':28,'case_counts':counts,'exact_two_html_reversal':True,'unchanged_direct_shared_dependencies':True,'dependency_files':dependencies(),'human_accepted_pages':0,'scope':'p22 count/action/full-title only. Other inline issues and collection skins remain open.','producer_sha256':sha(Path(__file__))}
    (current/'checkpoint.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS 28 cases; exact two-HTML reversal; direct dependencies unchanged')

if __name__=='__main__':main()
