"""Bind the page-only grid repair without relabeling earlier full-source reports."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DEMO=ROOT.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    base=ROOT/'evidence/baseline/photo-detail-image-bounds';out=ROOT/'evidence/current/photo-detail-image-bounds'
    red=read(base/'results.json');green=read(out/'results.json');previous_path=ROOT/'evidence/current/relationship-day-counter/checkpoint.json';previous=read(previous_path)
    assert red['files']==previous['files']
    assert len(red['results'])==red['expected_cases']==15 and sum(r['passed'] for r in red['results'])==5
    assert all(r['passed']==(r['value'][1:]==[160,90]) for r in red['results'])
    assert red['script_sha256']==sha(base/'verifier.py')
    assert len(green['results'])==green['expected_cases']==25 and all(r['passed'] and not r['errors'] for r in green['results'])
    assert green['script_sha256']==sha(ROOT/'verify_photo_detail_image_bounds.py')
    assert green['fixture_script_sha256']==sha(ROOT/'verify_record_controls.py')
    delta=[p for p,v in red['files'].items() if green['files'][p]!=v]
    assert delta==['custom/m03-p12.html'],delta
    for p,v in green['files'].items():assert sha(DEMO/p)==v,p
    original=(base/'source-custom.html').read_bytes();current=(DEMO/'custom/m03-p12.html').read_bytes()
    rule=('/* Keep intrinsic image proportions inside the painted photo frame. */\n.screen[aria-label="照片详情"] .photo{grid-template-rows:minmax(0,1fr);grid-template-columns:minmax(0,1fr)}\n').encode()
    assert current.count(rule)==1 and current.replace(rule,b'')==original
    assert current==(DEMO/'pages/m03-p12.html').read_bytes()
    assert sha(base/'source-custom.html')==red['files']['custom/m03-p12.html']
    assert (base/'source-pages.html').read_bytes()==original
    artifacts=[previous_path,base/'results.json',base/'verifier.py',base/'source-custom.html',base/'source-pages.html',out/'results.json',out/'390-portrait.png']
    value=dict(files=green['files'],baseline_files=red['files'],changed_files=delta,html_body_and_scripts_unchanged=True,
      rule=rule.decode(),verifier_sha256=sha(ROOT/'verify_photo_detail_image_bounds.py'),checkpoint_script_sha256=sha(Path(__file__)),
      artifacts_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in artifacts},
      actual_executions=[dict(session_id=37542,exit_code=1,cases=15,passed=5,stage='baseline portrait and square overflow'),dict(session_id=50763,exit_code=0,cases=25,passed=25,stage='grid dimensions,real request retry,original6 controls,dirty2,privacy1')],
      scope='One inline page-scoped grid rule only; original body/scripts,shared CSS/JS and other pages unchanged. Earlier reports preserve source hashes and are not new full replays.',accepted_pages=0)
    (out/'checkpoint.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Verified one page-only grid rule, original body/scripts unchanged,25/25 focused cases.')
if __name__=='__main__':main()
