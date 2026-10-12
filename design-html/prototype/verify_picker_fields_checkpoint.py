"""Bind dynamic-picker evidence to current source and actual served bytes."""
import json,hashlib
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,BASE,source

def main():
    files=source();out=ROOT/'evidence/current';checkpoint=json.loads((out/'shared-picker-fields-checkpoint.json').read_text(encoding='utf-8'));assert checkpoint['files']==files
    for path,digest in checkpoint['artifacts_sha256'].items():assert hashlib.sha256((DEMO/path).read_bytes()).hexdigest()==digest,path
    before=json.loads((out.parent/'baseline/shared-picker-fields-before.json').read_text(encoding='utf-8'));assert len(before['results'])==10 and not any(r['passed']for r in before['results'])
    picker=json.loads((out/'shared-picker-fields-results.json').read_text(encoding='utf-8'));assert picker['files']==files and len(picker['results'])==50 and all(r['passed']and not r['errors']for r in picker['results'])
    for width in [320,360,390,414,430]:assert sum(r['width']==width for r in picker['results'])==10
    native=json.loads((out/'native-shared-fields-results.json').read_text(encoding='utf-8'));assert native['files']==files and len(native['results'])==146 and all(r['passed']and not r.get('errors')for r in native['results'])
    assert len(native['pages'])==29
    for width in [320,360,390,414,430]:assert sum(len(r.get('fields',[]))for r in native['results']if r.get('width')==width)==69
    state=json.loads((out/'current-evidence-state.json').read_text(encoding='utf-8'));assert state['files']==files and state['current_picker_field_checks']==50 and state['current_native_field_checks']==146 and state['accepted_pages']==0
    assert state['current_initial_controls']==0 and state['historical_initial_controls']==752 and state['current_identity_cases']==0 and state['current_overlay_field_checks']==0 and state['runtime_requires_refresh']and state['catalog_requires_refresh']
    assert checkpoint['executions']['pickers']['exit_code']==0 and checkpoint['executions']['native_final']['exit_code']==0
    for name,digest in files.items():
        with urlopen(BASE+name.replace('custom/','pages/',1),timeout=10)as response:assert hashlib.sha256(response.read()).hexdigest()==digest,name
    for path in (DEMO/'custom').glob('*.html'):assert path.read_bytes()==(DEMO/'pages'/path.name).read_bytes()
    print(json.dumps(dict(picker_checks=50,native_checks=146,http_source_files=151,accepted_pages=0)))

if __name__=='__main__':main()
