"""Prove exact local CSS scope and preserve baseline/failed/final source evidence."""
import json
from pathlib import Path
from verify_pet_story_captions import ROOT,DEMO,dependencies,sha

def main():
    base=ROOT/'evidence/baseline/pet-story-captions';first=ROOT/'evidence/baseline/pet-story-captions-before-specificity';metadata=ROOT/'evidence/baseline/pet-story-captions-before-comment-metadata';current=ROOT/'evidence/current/pet-story-captions'
    load=lambda p:json.loads(p.read_text(encoding='utf-8'))
    red,failed,invalid,green=[load(p/'results.json') for p in [base,first,metadata,current]]
    assert len(red['results'])==20 and not any(r['passed'] for r in red['results'])
    assert sum('Reply region escapes original paper bubble' in r['failure'] for r in red['results'])==10
    assert all(('Reply region escapes original paper bubble' in r['failure'])==(r['value'][1]<2) for r in red['results'])
    assert len(failed['results'])==25 and sum(r['passed'] for r in failed['results'])==4
    assert len(invalid['results'])==25 and sum(r['passed'] for r in invalid['results'])==15
    assert all(r['kind']=='layout' and r['value'][1]>=2 for r in invalid['results'] if not r['passed'])
    for directory,report in [(base,red),(first,failed),(metadata,invalid)]:
        assert report['producer_sha256']==sha(directory/'producer.py')
        for n,h in report['dependencies'].items():assert sha(directory/'source'/n)==h
    assert green['producer_sha256']==sha(ROOT/'verify_pet_story_captions.py')
    # These two harness corrections affect only the unexecuted baseline flow and subpixel rounding.
    original=(base/'producer.py').read_text(encoding='utf-8')
    intermediate=original.replace("expect(p.locator('dialog[open]')).to_have_count(2)","expect(p.locator('.prototype-sheet-discard')).to_be_visible()")
    assert intermediate==(first/'producer.py').read_text(encoding='utf-8')
    expected=intermediate.replace("r['x']>=x+w*.44 and r['x']+r['w']<=x+w*.82,","r['x']>=x+w*.44-.5 and r['x']+r['w']<=x+w*.82+.5,")
    assert expected==(metadata/'producer.py').read_text(encoding='utf-8')
    declaration="for scenario in SCENARIOS:\n    for i,comment in enumerate(scenario['comments']):comment.update(id='comment-'+str(i),at=1791158400000+i)\n"
    assert (ROOT/'verify_pet_story_captions.py').read_text(encoding='utf-8').replace(declaration,'')==expected
    assert green['dependencies']==dependencies()
    assert red['fixture_sha256']==failed['fixture_sha256']==invalid['fixture_sha256']==green['fixture_sha256']==sha(ROOT/'verify_pet_controls.py')
    assert len(green['results'])==25 and all(r['passed'] for r in green['results'])
    changed=['custom/m07-p19.html','pages/m07-p19.html']
    css=('/* Keep stored author names below their portrait and responses inside the paper bubble. */\n'
         '.screen[data-pet-page="19"] .name.her{left:8%;width:34%;font-size:3.4cqw;line-height:1.1;text-align:center;overflow-wrap:anywhere}\n'
         '.screen[data-pet-page="19"] .name.his{left:60%;width:28%;font-size:3.8cqw;line-height:1.1;text-align:center}\n'
         '.screen[data-pet-page="19"] .role.her{left:8%;width:34%;top:83.2%;font-size:3cqw;line-height:1.25;text-align:center}\n'
         '.screen[data-pet-page="19"] .role.his{left:60%;width:28%;top:82%;font-size:3cqw;line-height:1.25;text-align:center}\n'
         'main.screen[data-pet-page="19"] .reply{left:48%;right:18%;top:84%;width:auto;height:4%;padding:0;font-size:3.2cqw;line-height:1.3;overflow:auto;overflow-wrap:anywhere}\n').replace('\n','\r\n').encode()
    for n,h in red['dependencies'].items():
        raw=(DEMO/n).read_bytes()
        if n in changed:assert raw.count(css)==1;raw=raw.replace(css,b'')
        assert raw==(base/'source'/n).read_bytes(),n
    assert (DEMO/changed[0]).read_bytes()==(DEMO/changed[1]).read_bytes()
    counts={k:sum(r['kind']==k for r in green['results']) for k in ['layout','control','flow']};assert counts=={'layout':20,'control':3,'flow':2}
    value={'passed':True,'cases':25,'case_counts':counts,'dependency_files':dependencies(),'exact_two_html_css_reversal':True,'shared_direct_dependencies_and_art_unchanged':True,'human_accepted_pages':0,'scope':'p19 stored author/role and response bubble layout only. Other inline/skin findings and full114 acceptance remain open.','producer_sha256':sha(Path(__file__))}
    (current/'checkpoint.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS25:20 layouts,3 original controls,2 response flows;2 exact CSS reversals;shared source/art unchanged')

if __name__=='__main__':main()
