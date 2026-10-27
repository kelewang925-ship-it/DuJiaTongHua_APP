"""Preserve existing action code while binding the page-only countdown layout patch."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    base=ROOT/'evidence/baseline/countdown-value-layout';out=ROOT/'evidence/current/countdown-value-layout'
    red=read(base/'results.json');green=read(out/'results.json');previous_path=ROOT/'evidence/current/photo-detail-image-bounds/checkpoint.json';previous=read(previous_path)
    assert red['files']==previous['files']
    assert len(red['results'])==40 and sum(r['passed'] for r in red['results'])==5
    assert all(r['passed']==(r['value'][1]==1) for r in red['results'])
    assert red['script_sha256']==sha(base/'verifier.py')
    assert len(green['results'])==green['expected_cases']==47 and all(r['passed'] and not r['errors'] for r in green['results'])
    assert green['script_sha256']==sha(ROOT/'verify_countdown_value_layout.py') and green['fixture_script_sha256']==sha(ROOT/'verify_time_controls.py')
    delta=[p for p,v in red['files'].items() if green['files'][p]!=v];assert delta==['custom/m04-p10.html'],delta
    for p,v in green['files'].items():assert sha(DEMO/p)==v,p
    patch=read(base/'patch.json');assert patch['old']=='<p class="number">3</p><p class="days">天</p>'
    assert patch['new']=='<div class="countdown-value">'+patch['old']+'</div>'
    assert patch['script']=='<script>(()=>{const value=document.querySelector(".countdown-value"),number=value?.querySelector(".number");if(number)value.style.setProperty("--countdown-digits",String(number.textContent.trim().length||1));})();</script>'
    original=(base/'source-custom.html').read_bytes();current=(DEMO/'custom/m04-p10.html').read_bytes();restored=current
    for name in ['css','script']:
        item=patch[name].encode();assert restored.count(item)==1;restored=restored.replace(item,b'')
    assert restored.count(patch['new'].encode())==1;restored=restored.replace(patch['new'].encode(),patch['old'].encode())
    assert restored==original and sha(base/'source-custom.html')==red['files']['custom/m04-p10.html']
    assert current==(DEMO/'pages/m04-p10.html').read_bytes() and (base/'source-pages.html').read_bytes()==original
    artifacts=[previous_path,base/'results.json',base/'verifier.py',base/'patch.json',base/'source-custom.html',base/'source-pages.html',out/'results.json',out/'top-aligned/results.json',out/'top-aligned/patch.json']+list(out.glob('*.png'))
    value=dict(files=green['files'],baseline_files=red['files'],changed_files=delta,original_nodes_and_scripts_preserved=True,display_only_digit_initializer=True,verifier_sha256=sha(ROOT/'verify_countdown_value_layout.py'),checkpoint_script_sha256=sha(Path(__file__)),
      artifacts_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in artifacts},
      actual_executions=[dict(session_id=64394,exit_code=1,cases=40,passed=5,stage='original fixed numeral placement'),dict(session_id=48678,exit_code=0,cases=47,passed=47,stage='contained but visual group too high for multiple digits'),dict(session_id=54504,exit_code=0,cases=47,passed=47,stage='vertically centered final layout and original actions')],
      scope='Only countdown page display wrapper/CSS and local digit-count style initialization. All original nodes and controller dependencies retained; shared assets and original callbacks byte unchanged. Earlier evidence retains original manifests, not new full replays.',accepted_pages=0)
    (out/'checkpoint.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Verified countdown display only,original controller bytes retained,47/47 focused cases.')
if __name__=='__main__':main()
