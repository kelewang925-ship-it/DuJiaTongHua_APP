"""Independent value expansion/reconstruction, rendered equivalence and current source."""
import json,re,hashlib
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,BASE,source

def canonical(value):return re.sub(r'\s*,\s*',',',re.sub(r'\s+',' ',value.strip()))
def main():
    out=ROOT/'evidence/current';files=source();checkpoint=json.loads((out/'shared-style-tokens-checkpoint.json').read_text(encoding='utf-8'));assert checkpoint['files']==files
    for name,digest in checkpoint['artifacts_sha256'].items():assert hashlib.sha256((DEMO/name).read_bytes()).hexdigest()==digest,name
    migration=json.loads((out/'shared-style-token-migration.json').read_text(encoding='utf-8'));assert len(migration['files'])==12 and sum(len(v['changes'])for v in migration['files'])==504 and len(migration['new_tokens'])==16
    wanted={name for entry in migration['files']for change in entry['changes']for name in re.findall(r'var\((--prototype-[\w-]+)\)',change['before']+change['after'])};variables={}
    for path in (DEMO/'assets').glob('prototype-*.css'):
        for name,value in re.findall(r'(--[\w-]+)\s*:\s*([^;}]+)',path.read_text(encoding='utf-8')):
            if name not in wanted:continue
            if name in variables:assert canonical(variables[name])==canonical(value),name
            variables[name]=value
    def expand(value):
        for _ in range(10):
            updated=re.sub(r'var\((--[\w-]+)\)',lambda m:variables.get(m[1],m[0]),value)
            if updated==value:return canonical(value)
            value=updated
        raise AssertionError('Unresolved token cycle')
    history=ROOT/'evidence/history/pre-shared-style-tokens-74b3eca'
    baseline=json.loads((ROOT/'evidence/baseline/shared-style-computed-before.json').read_text(encoding='utf-8'))
    suffix='\n:root{'+''.join(k+':'+v+';'for k,v in migration['new_tokens'].items())+'}\n'
    for entry in migration['files']:
        path=DEMO/entry['file'];raw=(history/path.name).read_bytes();assert hashlib.sha256(raw).hexdigest()==entry['before_sha256']==baseline['files'][entry['file']]
        original=raw.decode('utf-8');current=path.read_bytes().decode('utf-8')
        if path.name=='prototype-components.css':assert current.endswith(suffix);current=current[:-len(suffix)]
        position=0;offset=0;recovered=[]
        for change in entry['changes']:
            unchanged=original[position:change['start']];assert current[offset:offset+len(unchanged)]==unchanged;offset+=len(unchanged)
            assert original[change['start']:change['end']]==change['before'];assert current[offset:offset+len(change['after'])]==change['after'];offset+=len(change['after']);position=change['end'];recovered.extend([unchanged,change['before']]);assert expand(change['before'])==expand(change['after']),(entry['file'],change)
        assert current[offset:]==original[position:];recovered.append(current[offset:]);assert ''.join(recovered)==original
    assert {k for k in files if files[k]!=baseline['files'][k]}=={e['file']for e in migration['files']}
    report=json.loads((out/'shared-style-computed-results.json').read_text(encoding='utf-8'));assert report['files']==files and len(report['results'])==60 and all(r['passed']and not r['errors']for r in report['results'])
    for row in report['results']:assert row['observed']==next(r['observed']for r in baseline['results']if r['page']==row['page']and r['width']==row['width'])
    motion=json.loads((out/'shared-token-motion-results.json').read_text(encoding='utf-8'));assert motion['files']==files and len(motion['results'])==2 and all(r['passed']for r in motion['results'])
    full=next(r['observed']for r in motion['results']if r['mode']=='no-preference');reduced=next(r['observed']for r in motion['results']if r['mode']=='reduce')
    assert full['dialog[open]']['animationDuration']=='0.22s'and full['[data-contract=spinner] .prototype-component-spinner']['animationDuration']=='0.9s'
    assert reduced['dialog[open]']['animationDuration']=='0s'and reduced['[data-contract=spinner] .prototype-component-spinner']['animationDuration']=='0s'
    state=json.loads((out/'current-evidence-state.json').read_text(encoding='utf-8'));assert state['files']==files and state['current_style_equivalence_checks']==60 and state['current_token_motion_modes']==2 and state['accepted_pages']==0 and state['runtime_requires_refresh']and state['catalog_requires_refresh']
    assert checkpoint['executions']['after']['exit_code']==0 and checkpoint['executions']['motion']['exit_code']==0
    for name,digest in files.items():
        with urlopen(BASE+name.replace('custom/','pages/',1),timeout=10)as response:assert hashlib.sha256(response.read()).hexdigest()==digest,name
    for path in (DEMO/'custom').glob('*.html'):assert 'prototype-ui.css'in path.read_text(encoding='utf-8')and path.read_bytes()==(DEMO/'pages'/path.name).read_bytes()
    print(json.dumps(dict(stylesheets=12,exact_declarations=504,new_tokens=16,rendered_equivalence=60,motion_modes=2,served_files=151,accepted_pages=0)))

if __name__=='__main__':main()
