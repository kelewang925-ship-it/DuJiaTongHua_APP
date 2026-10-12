"""Validate finite native field scope and keep old flow evidence historical."""
import hashlib,json
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,BASE,source

def main():
    files=source();out=ROOT/'evidence/current';checkpoint=json.loads((out/'native-shared-fields-checkpoint.json').read_text(encoding='utf-8'));assert checkpoint['files']==files
    for name,digest in checkpoint['artifacts_sha256'].items():assert hashlib.sha256((DEMO/name).read_bytes()).hexdigest()==digest,name
    native=json.loads((out/'native-shared-fields-results.json').read_text(encoding='utf-8'));assert native['files']==files and len(native['pages'])==29 and len(native['results'])==146
    assert all(r['passed']and not r.get('errors')for r in native['results'])
    assert {(r['page'],r['width'])for r in native['results']if 'page'in r}=={(p,w)for p in native['pages']for w in [320,360,390,414,430]}
    for width in [320,360,390,414,430]:assert sum(len(r['fields'])for r in native['results']if r.get('width')==width)==69
    assert sum(r.get('case')=='adapter-preserves-native-contract'for r in native['results'])==1
    anchor=json.loads((out/'native-field-error-anchor.json').read_text(encoding='utf-8'));assert anchor['files']==files and anchor['passed']and anchor['observed']['conflicts']==0
    before=json.loads((out.parent/'baseline/native-shared-fields-before.json').read_text(encoding='utf-8'));assert len(before['results'])==29 and not any(r['passed']for r in before['results'])
    flows=json.loads((out/'native-field-flows-results.json').read_text(encoding='utf-8'));assert len(flows['results'])==59 and all(r['passed']for r in flows['results'])and flows['files']!=files
    state=json.loads((out/'current-evidence-state.json').read_text(encoding='utf-8'));assert state['files']==files and state['current_native_field_checks']==146 and state['current_native_error_anchor_checks']==1 and state['current_native_field_flow_checks']==0 and state['historical_native_field_flow_checks']==59
    assert state['runtime_requires_refresh']and state['catalog_requires_refresh']and state['accepted_pages']==0 and state['current_initial_controls']==0 and state['historical_initial_controls']==752
    assert state['current_overlay_field_checks']==0 and state['current_identity_cases']==0
    assert checkpoint['executions']['final_native']['exit_code']==0 and checkpoint['executions']['diary_anchor']['exit_code']==0
    for path in (DEMO/'custom').glob('*.html'):assert path.read_bytes()==(DEMO/'pages'/path.name).read_bytes()
    for path,digest in files.items():
        url=BASE+(path.replace('custom/','pages/',1)if path.startswith('custom/')else path)
        with urlopen(url,timeout=10)as response:assert hashlib.sha256(response.read()).hexdigest()==digest,path
    print(json.dumps(dict(pages=29,fields=69,width_cases=145,adapter_contracts=1,current_error_anchor=1,http_source_files=len(files),historical_field_flow_cases=59,accepted_pages=0)))

if __name__=='__main__':main()
