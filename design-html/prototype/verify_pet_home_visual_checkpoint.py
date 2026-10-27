"""Bind a one-page CSS-only visual repair to old business evidence and new checks."""
import hashlib,json,re,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parent;DEMO=ROOT.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    baseline=ROOT/'evidence/baseline/pet-home-visual';current=ROOT/'evidence/current/pet-home-visual'
    red=read(baseline/'results.json');green=read(current/'results.json');first_green=read(current/'layout-only/results.json')
    assert len(red['results'])==25 and sum(r['passed'] for r in red['results'])==15
    assert all(r['passed'] for r in red['results'] if r['kind']=='control')
    assert len(green['results'])==25 and all(r['passed'] and not r['errors'] for r in green['results'])
    assert len(first_green['results'])==25 and all(r['passed'] for r in first_green['results'])
    assert red['script_sha256']==first_green['script_sha256']==sha(current/'layout-only/verifier.py')
    assert green['script_sha256']==sha(ROOT/'verify_pet_home_visual_text.py')
    assert green['fixture_script_sha256']==red['fixture_script_sha256']==sha(ROOT/'verify_pet_controls.py')
    before=baseline/'m07-p03.html';after=DEMO/'custom/m07-p03.html'
    assert sha(before)==red['files']['custom/m07-p03.html'] and sha(after)==green['files']['custom/m07-p03.html']
    assert after.read_bytes()==(DEMO/'pages/m07-p03.html').read_bytes()
    old=before.read_text(encoding='utf-8');new=after.read_text(encoding='utf-8')
    pattern=r'/\* Keep live summaries beside the portraits and labels below the painted icons\. \*/\n(?:\.screen\[data-pet-page="3"\][^\n]+\n){4}'
    matches=list(re.finditer(pattern,new));assert len(matches)==1
    css=matches[0].group();assert new.replace(css,'',1)==old,'Change exceeds four local CSS rules'
    selectors=['.screen[data-pet-page="3"] .care','.screen[data-pet-page="3"] .care-left','.screen[data-pet-page="3"] .actions button','.screen[data-pet-page="3"] .pet-back']
    for line,selector in zip(css.splitlines()[1:],selectors):assert line.startswith(selector+'{') and line.count('{')==line.count('}')==1
    delta=[k for k in red['files'] if red['files'][k]!=green['files'][k]];assert delta==['custom/m07-p03.html']
    assert not subprocess.check_output(['git','diff','10bacba','--name-only','--','design-html/assets']).strip(),'Artwork/font/shared asset change exceeds this patch'
    for key,digest in green['files'].items():assert sha(DEMO/key)==digest,key
    legacy=read(ROOT/'evidence/current/hidden-choice-outcomes/results.json');assert legacy['files']==red['files']
    layout=[r for r in green['results'] if r['kind']=='layout'];assert len(layout)==10 and all(r['care_largest_blue_component']<20 for r in layout)
    # Retain every actual execution and image, including the intermediate
    # detector which incorrectly counted isolated colored font subpixels.
    artifacts=[baseline/'results.json',before,current/'results.json',current/'layout-only/results.json',current/'layout-only/verifier.py',current/'layout-only/blue-icon-probe.json',current/'pixel-detector-observer/results.json',current/'pixel-detector-observer/verifier.py']
    artifacts+=list(current.glob('*.png'))+list(baseline.glob('*.png'))+list((current/'before-header').glob('*'))
    value=dict(files=green['files'],baseline_files=red['files'],baseline_git_revision='10bacba',changed_files=delta,html_body_and_scripts_unchanged=True,html_equivalence='Newline-normalized text is identical after removing exactly four page-scoped CSS rules',shared_assets_unchanged=True,added_css=css,
      artifacts_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in artifacts},verifier_sha256=sha(ROOT/'verify_pet_home_visual_text.py'),checkpoint_script_sha256=sha(Path(__file__)),
      actual_executions=[dict(session_id=41731,exit_code=1,cases=25,passed=15,stage='baseline geometry'),dict(session_id=43885,exit_code=0,cases=25,passed=25,stage='layout-only; later visual inspection found decorative water icon'),dict(session_id=32904,exit_code=1,cases=25,passed=15,stage='naive pixel detector counted colored glyph subpixels'),dict(session_id=20212,exit_code=0,cases=25,passed=25,stage='paper text area and connected-icon exclusion; header overlap separately diagnosed'),dict(session_id=14041,exit_code=0,cases=25,passed=25,stage='final, including portrait/back exclusion and all15 controls')],
      accepted_pages=0,human_reviewer=None,scope='Only m07-p03 inline CSS and mirrored generated page;15 actual initial controls plus10 layout states. Old business reports keep their original source manifests, retained through exact markup/JS preservation. Not a114-page replay or human visual approval.')
    (current/'checkpoint.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Verified: one-page CSS only;25 final checks; original body/scripts and shared assets unchanged')
if __name__=='__main__':main()
