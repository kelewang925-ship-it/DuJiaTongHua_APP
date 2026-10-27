"""Bind two page-local storage label rules while retaining all original behavior."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    base=ROOT/'evidence/baseline/storage-quantity-layout';out=ROOT/'evidence/current/storage-quantity-layout'
    red=read(base/'results.json');green=read(out/'results.json');previous_path=ROOT/'evidence/current/countdown-value-layout/checkpoint.json';previous=read(previous_path)
    assert red['files']==previous['files'] and len(red['results'])==red['expected_cases']==15
    assert all(not r['passed'] and not r['errors'] and "assert max(q['bottom'],n['bottom'])" in r['error'] for r in red['results'])
    assert red['script_sha256']==sha(base/'verifier.py')
    assert len(green['results'])==green['expected_cases']==21 and all(r['passed'] and not r['errors'] for r in green['results'])
    assert green['script_sha256']==sha(ROOT/'verify_storage_quantity_layout.py') and green['fixture_script_sha256']==sha(ROOT/'verify_settings_controls.py')
    delta=[p for p,v in red['files'].items() if green['files'][p]!=v];assert delta==['custom/m06-p11.html'],delta
    for p,v in green['files'].items():assert sha(DEMO/p)==v,p
    rule=(base/'rule.css').read_bytes();original=(base/'source-custom.html').read_bytes();current=(DEMO/'custom/m06-p11.html').read_bytes()
    assert current.count(rule)==1 and current.replace(rule,b'')==original
    assert sha(base/'source-custom.html')==red['files']['custom/m06-p11.html']
    assert current==(DEMO/'pages/m06-p11.html').read_bytes() and (base/'source-pages.html').read_bytes()==original
    artifacts=[previous_path,base/'results.json',base/'verifier.py',base/'source-custom.html',base/'source-pages.html',base/'rule.css',out/'results.json']+list(out.glob('*.png'))
    value=dict(files=green['files'],baseline_files=red['files'],changed_files=delta,html_body_and_scripts_unchanged=True,rule=rule.decode(),verifier_sha256=sha(ROOT/'verify_storage_quantity_layout.py'),checkpoint_script_sha256=sha(Path(__file__)),artifacts_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in artifacts},
      actual_executions=[dict(session_id=88393,exit_code=1,cases=15,passed=0,stage='original two-line label enters painted meter'),dict(session_id=75022,exit_code=0,cases=21,passed=21,stage='five widths,real KB/MB,original six controls')],
      scope='Two inline page-scoped CSS rules only. Original body,scripts,shared assets and other pages byte unchanged. Original painted meter remains decoration without a browser quota claim. Previous source manifests retained,not new full replays.',accepted_pages=0)
    (out/'checkpoint.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Verified storage label CSS only,original body/scripts retained,21/21 focused cases.')
if __name__=='__main__':main()
