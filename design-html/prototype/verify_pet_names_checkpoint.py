"""Verify original name-template lineage and source-identical retained naming observations."""
import json,subprocess
from pathlib import Path
from verify_pet_names import ROOT,DEMO,dependencies,sha

def load(p):return json.loads(p.read_text(encoding='utf-8'))

def main():
    baseline=ROOT/'evidence/baseline/pet-names';prior=ROOT/'evidence/baseline/pet-names-before-rename-locator';current=ROOT/'evidence/current/pet-names';patch=load(baseline/'patch.json')
    assert len(patch)==52
    for name,replacements in patch.items():
        raw=(DEMO/name).read_bytes()
        for old,new in reversed(replacements):assert raw.count(new.encode())==1;raw=raw.replace(new.encode(),old.encode(),1)
        assert raw==(baseline/'source'/name).read_bytes(),name
    for i in range(1,26):assert (DEMO/f'custom/m07-p{i:02}.html').read_bytes()==(DEMO/f'pages/m07-p{i:02}.html').read_bytes()
    red,old,green=[load(folder/'results.json') for folder in [baseline,prior,current]]
    assert len(red['results'])==25 and sum(r['passed'] for r in red['results'])==5;assert red['producer_sha256']==sha(baseline/'producer.py')
    assert len(old['results'])==104 and sum(r['passed'] for r in old['results'])==103;assert old['producer_sha256']==sha(prior/'producer.py')
    assert all('strict mode violation' in r['failure'] and '2 elements' in r['failure'] for r in old['results'] if not r['passed'])
    assert old['dependency_files']==green['dependency_files']==dependencies();assert green['producer_sha256']==sha(ROOT/'verify_pet_names.py')
    assert len(green['results'])==104 and all(r['passed'] for r in green['results'])
    assert green['fixture_sha256']==old['fixture_sha256']==red['fixture_sha256']==sha(ROOT/'verify_pet_controls.py')
    assert set(dependencies())-set(red['dependency_files'])=={'assets/prototype-pet-names.js'}
    assert all(dependencies()[name]==h for name,h in red['dependency_files'].items() if name not in patch)
    key=lambda r:json.dumps([r['kind'],r['value']],ensure_ascii=False,sort_keys=True)
    originals={key(r):r for r in old['results']};retained=[r for r in green['results'] if r.get('execution')=='retained-source-identical'];assert len(retained)==103
    for r in retained:
        assert {k:v for k,v in r.items() if k not in ['execution','prior_report']}==originals[key(r)]
        assert r['prior_report']=='evidence/baseline/pet-names-before-rename-locator/results.json'
    fresh=[r for r in green['results'] if r not in retained];assert len(fresh)==1 and fresh[0]['value']=='actual-rename'
    name_cases=[r for r in green['results'] if r['kind']=='names'];assert len(name_cases)==100
    observations=[item for r in name_cases for item in r['attributes']];assert len(observations)==152 and all(r['present'] and r['actual']==r['expected'] for r in observations)
    assert all(r['document_title']==r['expected_title'] for r in name_cases)
    captures=load(current/'retained-captures.json');assert captures['source_report_sha256']==sha(prior/'results.json')
    assert len(captures['captures'])==4
    for name,h in captures['captures'].items():assert sha(current/name)==sha(prior/name)==h
    consumers=sorted(p.stem for p in (DEMO/'custom').glob('*.html') if 'prototype-pet-names.js' in p.read_text(encoding='utf-8'));assert consumers==[f'm07-p{i:02}' for i in range(1,26)]
    for name in ['prototype-pet-names.js','prototype-pet.js','prototype-pet-life.js']:subprocess.run([r'C:\Users\kele\.nvmd\bin\node.exe','--check',str(DEMO/'assets'/name)],check=True)
    result={'passed':True,'dependency_files':dependencies(),'verified_cases':104,'name_cases':100,'source_attribute_observations':152,'title_observations':100,'source_identical_retained_cases':103,'fresh_rename_retry_case':1,'exact_existing_file_reversals':52,'consumers':consumers,'human_accepted_pages':0,'scope':'Static UI name templates, browser title and actual rename/cross-tab propagation. No screen-reader/device certification, all-control replay, long-name layout or full114 acceptance claim.','producer_sha256':sha(Path(__file__))}
    (current/'checkpoint.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS104 naming cases:100 page/name observations,152 source attributes,100 titles, rename and template ownership;52 exact source reversals,25 mirrored consumers,3 JS syntax checks')

if __name__=='__main__':main()
