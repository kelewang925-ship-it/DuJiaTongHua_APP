"""One-rule capsule editor patch, preserved business sources and exact red/green lineage."""
import json
from pathlib import Path
from verify_capsule_photo_hint import ROOT,DEMO,dependencies,sha

def load(p):return json.loads(p.read_text(encoding='utf-8'))

def main():
    baseline=ROOT/'evidence/baseline/capsule-photo-hint';prior=ROOT/'evidence/baseline/capsule-photo-hint-before-control-metadata';current=ROOT/'evidence/current/capsule-photo-hint'
    patch=load(baseline/'patch.json')['css'].encode()
    for folder in ['custom','pages']:
        raw=(DEMO/f'{folder}/m04-p13.html').read_bytes();assert raw.count(patch)==1
        assert raw.replace(patch,b'',1)==(baseline/f'source-{folder}.html').read_bytes()
    assert (DEMO/'custom/m04-p13.html').read_bytes()==(DEMO/'pages/m04-p13.html').read_bytes()
    red,old,green=[load(p/'results.json') for p in [baseline,prior,current]]
    assert len(red['results'])==20 and not any(r['passed'] for r in red['results'])
    assert red['producer_sha256']==sha(baseline/'producer.py')
    assert len(old['results'])==33 and sum(r['passed'] for r in old['results'])==30
    assert all("KeyError: 'native_input'" in r['failure'] for r in old['results'] if not r['passed'])
    assert old['producer_sha256']==sha(prior/'producer.py')
    assert old['dependency_files']==green['dependency_files']==dependencies()
    assert len(green['results'])==33 and all(r['passed'] for r in green['results'])
    assert green['producer_sha256']==sha(ROOT/'verify_capsule_photo_hint.py')
    for report in [red,old,green]:
        assert report['fixture_sha256']==sha(ROOT/'verify_time_controls.py')
        assert report['image_fixture_sha256']==sha(ROOT/'verify_image_read_order.py')
    assert all(h==dependencies()[name] for name,h in red['dependency_files'].items() if name not in ['custom/m04-p13.html','pages/m04-p13.html'])
    key=lambda r:json.dumps([r['kind'],r['value']],ensure_ascii=False,sort_keys=True)
    retained=[r for r in green['results'] if r.get('execution')=='retained-source-identical'];assert len(retained)==30
    originals={key(r):r for r in old['results']}
    for row in retained:
        clean={k:v for k,v in row.items() if k not in ['execution','prior_report']};assert clean==originals[key(row)]
        assert row['prior_report']=='evidence/baseline/capsule-photo-hint-before-control-metadata/results.json'
    new=[r for r in green['results'] if r not in retained];assert sorted(r['value']['selector'] for r in new)==['#message','#name','#reminder']
    captures=load(current/'retained-captures.json');assert captures['source_report_sha256']==sha(prior/'results.json')
    for name,h in captures['captures'].items():assert sha(current/name)==sha(prior/name)==h
    report={'passed':True,'dependency_files':dependencies(),'browser_cases':33,'layout_states':20,'original_initial_controls':8,'photo_save_return_flows':5,'source_identical_retained_cases':30,'fresh_native_field_retries':3,'exact_html_css_reversal':True,'shared_runtime_and_artwork_unchanged':True,'human_accepted_pages':0,'scope':'Single capsule editor photo hint only. Other P2 visual findings and the full114 goal remain open.','producer_sha256':sha(Path(__file__))}
    (current/'checkpoint.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS33 capsule photo hint cases:30 source-identical retained +3 native-field retries; exact one-rule patch and original shared sources/artwork verified')

if __name__=='__main__':main()
