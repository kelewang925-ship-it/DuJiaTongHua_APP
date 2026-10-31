"""Bind result illustrations to transaction evidence, preserving the invalid star-test assumption."""
import json,re
from pathlib import Path
from verify_pet_result_illustrations import ROOT,DEMO,sha,dependencies,ACTIONS

def main():
    read=lambda p:json.loads(p.read_text(encoding='utf-8'))
    base=ROOT/'evidence/baseline/pet-result-illustrations';prior=ROOT/'evidence/baseline/pet-result-illustrations-before-visual-review';current=ROOT/'evidence/current/pet-result-illustrations'
    red=read(base/'results.json');first=read(prior/'results.json');green=read(current/'results.json');patch=read(base/'patch.json')
    assert len(red['results'])==4 and not any(r['passed'] for r in red['results'])
    assert all('No illustration corresponding to this actual result log' in r['failure'] for r in red['results'])
    assert len(first['results'])==65 and sum(r['passed'] for r in first['results'])==58
    failed=[r for r in first['results'] if not r['passed']]
    assert sum(r['kind']=='layout' and r['value'][2]=='星星 ×5' for r in failed)==5
    assert sum(r['kind']=='claim' and r['value'] in ['note','weekly-stars'] for r in failed)==2
    assert all('assert image.evaluate' in r['failure'] for r in failed)
    assert red['producer_sha256']==sha(base/'producer.py')==first['producer_sha256']==sha(prior/'producer.py')
    assert green['producer_sha256']==sha(ROOT/'verify_pet_result_illustrations.py')
    addition="    if n==5:\n        progress=p.get_by_role('progressbar',name='本周照顾奖励进度',exact=True);expect(progress).to_have_attribute('max','3');assert progress.evaluate('e=>e.value')==p.evaluate('Math.min(3,PrototypePet.weekCount(PrototypePet.read()))')\n"
    assert (ROOT/'verify_pet_result_illustrations.py').read_text(encoding='utf-8').replace(addition,'').replace('.length>0','.length>1')==(prior/'producer.py').read_text(encoding='utf-8')
    for report in [red,first,green]:assert report['fixture_sha256']==sha(ROOT/'verify_pet_controls.py')
    assert green['dependencies']==dependencies()
    assert len(green['results'])==65 and all(r['passed'] and not r['page_errors'] for r in green['results'])
    for directory,report in [(base,red),(prior,first)]:
        for n,h in report['dependencies'].items():assert sha(directory/'source'/n)==h
    assert set(patch)=={'assets/prototype-pet.js','assets/prototype-pet-draft-preview.js',*[f'{directory}/m07-p{n:02}.html' for directory in ['custom','pages'] for n in [5,10]]}
    for n in red['dependencies']:
        raw=(DEMO/n).read_bytes()
        for a,b in reversed(patch.get(n,[])):
            assert raw.count(b.encode())==1;raw=raw.replace(b.encode(),a.encode())
        assert raw==(base/'source'/n).read_bytes(),n
    additions={'assets/prototype-pet-result-illustration.js','assets/prototype-pet-result-illustration.css'}
    assert set(green['dependencies'])-set(red['dependencies'])==additions
    for n,h in first['dependencies'].items():
        if n not in additions:assert h==green['dependencies'][n],n
    n='assets/prototype-pet-result-illustration.js';raw=(DEMO/n).read_bytes();blocks=re.findall(rb"    if\(action\)\{\n      screen.querySelector\('\.piece'\).*?    }\n",raw,re.S);assert len(blocks)==1
    assert raw.replace(blocks[0],b'')==(prior/'source'/n).read_bytes()
    n='assets/prototype-pet-result-illustration.css';raw=(DEMO/n).read_bytes();assert raw.split(b'\nmain.screen .pet-result-week')[0].replace(b'.art-hero{height:12%}',b'.art-hero{height:18%}').replace(b'.art-hero{height:16%}',b'.art-hero{height:22%}')==(prior/'source'/n).read_bytes()
    for n in [5,10]:assert (DEMO/f'custom/m07-p{n:02}.html').read_bytes()==(DEMO/f'pages/m07-p{n:02}.html').read_bytes()
    counts={kind:sum(r['kind']==kind for r in green['results']) for kind in ['layout','control','play','claim']};assert counts=={'layout':50,'control':5,'play':4,'claim':6}
    for row in green['results']:
        if row['kind']!='layout':continue
        n,w,value=row['value'];wanted=[value] if n==5 else [name for name in ['主粮','礼物','爱心小饼干','金币','星星','小花围巾'] if name in value] or ['记录'];assert row['symbols']==wanted
    value={'passed':True,'cases':65,'case_counts':counts,'dependencies':dependencies(),'exact_six_file_integration_reversal':True,'original_model_reward_transactions_and_art_unchanged':True,'single_path_star_is_valid_svg_not_a_product_failure':True,'weekly_progress_native_from_real_count':True,'screenshots':{p.name:sha(p) for p in sorted(current.glob('*.png'))},'human_accepted_pages':0,'scope':'p05 four saved interactions and p10 five reward types plus unknown legacy fallback; five widths, original exits, four interaction and six claim failure/retry flows. Native semantic SVGs, not watercolor pixel-match acceptance. Other inline typography and full114 final audit remain open.','producer_sha256':sha(Path(__file__))}
    (current/'checkpoint.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS65:50 layouts,5 exits,4 play and6 claim failure/retry flows; six exact reversals')

if __name__=='__main__':main()
