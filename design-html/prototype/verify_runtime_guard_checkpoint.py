"""Source-bound runtime/catalog and the fixed actual invite return behavior."""
import json,hashlib
from urllib.request import urlopen
from verify_pet_controls import ROOT,DEMO,BASE,source

def main():
    files=source();out=ROOT/'evidence/current';checkpoint=json.loads((out/'consolidated-runtime-guard-checkpoint.json').read_text(encoding='utf-8'));assert checkpoint['files']==files
    for path,digest in checkpoint['artifacts_sha256'].items():assert hashlib.sha256((DEMO/path).read_bytes()).hexdigest()==digest,path
    runtime=json.loads((out/'current-runtime-summary.json').read_text(encoding='utf-8'));assert runtime['files']==files and runtime['requested_pages']==114 and runtime['observations']==228 and runtime['controls_observed']==1696 and len(runtime['redirects'])==51 and not runtime['errors']and not runtime['unbound_or_delegated_candidates']
    guard=json.loads((out/'guard-metadata-results.json').read_text(encoding='utf-8'));assert guard['files']==files and len(guard['results'])==6 and all(r['passed']and not r.get('errors')for r in guard['results'])
    before=json.loads((out.parent/'baseline/guard-metadata-before.json').read_text(encoding='utf-8'));assert len(before['results'])==6 and sum(r['passed']for r in before['results'])==2
    onboarding=json.loads((out/'onboarding-control-results.json').read_text(encoding='utf-8'));fingerprint=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest();assert len(onboarding)==82 and all(r['passed']and not r['errors']and r['source_fingerprint']==fingerprint for r in onboarding)
    settings=json.loads((out/'settings-controls-results.json').read_text(encoding='utf-8'));assert settings['files']==files and len(settings['results'])==81 and all(r['passed']and not r['errors']for r in settings['results'])
    catalog=json.loads((out/'page-contracts.json').read_text(encoding='utf-8'));assert catalog['files']==files and len(catalog['pages'])==114 and len(catalog['assets'])==267
    controls=[c for p in catalog['pages']for c in p['control_evidence']];assert sum(c['status']=='当前源码通过'for c in controls)==163 and sum(c['status']=='历史通过／待当前复验'for c in controls)==589
    state=json.loads((out/'current-evidence-state.json').read_text(encoding='utf-8'));assert state['files']==files and state['current_initial_controls']==163 and state['historical_initial_controls']==589 and state['current_guard_metadata_checks']==6 and not state['runtime_requires_refresh']and not state['catalog_requires_refresh']and state['accepted_pages']==0
    for name in ['runtime_final','guard','settings_final','onboarding_final']:assert checkpoint['executions'][name]['exit_code']==0
    for path,digest in files.items():
        with urlopen(BASE+path.replace('custom/','pages/',1),timeout=10)as response:assert hashlib.sha256(response.read()).hexdigest()==digest,path
    print(json.dumps(dict(pages=114,observations=228,controls=1696,current_initial=163,historical_initial=589,guard_checks=6,assets=267,accepted_pages=0)))

if __name__=='__main__':main()
