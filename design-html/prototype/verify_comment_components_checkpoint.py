"""Verify comment/tag component scope, five-case replay and served source."""
import hashlib,json
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,BASE,source

def main():
    files=source();out=ROOT/'evidence/current';checkpoint=json.loads((out/'comment-tag-components-checkpoint.json').read_text(encoding='utf-8'));assert checkpoint['files']==files
    for path,digest in checkpoint['artifacts_sha256'].items():assert hashlib.sha256((DEMO/path).read_bytes()).hexdigest()==digest,path
    report=json.loads((out/'comment-tag-components-results.json').read_text(encoding='utf-8'));assert report['files']==files and len(report['results'])==17 and all(r['passed']and not r.get('errors')for r in report['results'])
    for width in [320,360,390,414,430]:assert {r['page']for r in report['results']if r.get('width')==width}=={'m03-p08','m03-p12','m06-p05'}
    raw=(out.parent/'baseline/comment-tag-components-first-pass.json').read_bytes();prior=json.loads(raw);assert prior['files']==files and report['retained_baseline_sha256']==hashlib.sha256(raw).hexdigest()
    assert len(report['retained_indices'])==12 and len(report['replayed_indices'])==5 and set(report['retained_indices']+report['replayed_indices'])==set(range(17))
    for index in report['retained_indices']:assert report['results'][index]==prior['results'][index]and prior['results'][index]['passed']
    for index in report['replayed_indices']:assert report['results'][index]['page']=='m06-p05'and not prior['results'][index]['passed']
    before=json.loads((out.parent/'baseline/comment-tag-components-before.json').read_text(encoding='utf-8'));assert len(before['results'])==5 and sum(r['passed']for r in before['results'])==1
    decisions=(ROOT/'ORIGINAL_COMPONENT_DECISIONS.md').read_text(encoding='utf-8');assert len([line for line in decisions.splitlines()if line.startswith('| m')])==114
    state=json.loads((out/'current-evidence-state.json').read_text(encoding='utf-8'));assert state['files']==files and state['current_comment_tag_checks']==17 and state['accepted_pages']==0 and state['runtime_requires_refresh']and state['catalog_requires_refresh']
    assert state['current_initial_controls']==0 and state['historical_initial_controls']==752 and state['current_picker_field_checks']==0 and state['current_native_field_checks']==0
    assert checkpoint['executions']['replay']['exit_code']==0
    for path,digest in files.items():
        with urlopen(BASE+path.replace('custom/','pages/',1),timeout=10)as response:assert hashlib.sha256(response.read()).hexdigest()==digest,path
    for path in (DEMO/'custom').glob('*.html'):assert path.read_bytes()==(DEMO/'pages'/path.name).read_bytes()
    print(json.dumps(dict(current_component_checks=17,retained=12,replayed=5,static_preservation_pages=114,http_source_files=151,accepted_pages=0)))

if __name__=='__main__':main()
