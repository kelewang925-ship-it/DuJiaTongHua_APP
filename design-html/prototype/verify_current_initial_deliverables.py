"""Verify source, case provenance, availability correction and published114 catalog."""
import json,re,hashlib
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen
from replay_current_initial_controls import ROOT,DEMO,OUT,deps,sha,dump

def read(p):return json.loads(p.read_text(encoding='utf-8'))

def main():
    raw_path=OUT/'results.json';raw=read(raw_path);folder=ROOT/'evidence/current/initial-controls-20261031-accessible';path=folder/'results.json';report=read(path);contracts=read(folder/'contracts.json')
    assert raw['complete'] and len(raw['inventory'])==114 and not raw['inventory_errors']
    assert report['complete'] and report['all_passed'] and len(report['inventory'])==114 and not report['inventory_errors']
    assert report['dependencies']==raw['dependencies']==contracts['dependencies']==deps()
    served={}
    for name,h in deps().items():
        url='http://127.0.0.1:8765/'+name.replace('custom/','pages/',1)
        with urlopen(url,timeout=10) as response:
            actual=hashlib.sha256(response.read()).hexdigest();assert actual==h,name
            served[name]={'sha256':actual,'cache_control':response.headers.get('Cache-Control'),'url':url}
    assert report['source_report_sha256']==sha(raw_path) and contracts['report_sha256']==sha(path)
    assert contracts['producer_sha256']==sha(ROOT/'build_current_initial_deliverables.py')
    assert all(v['passed'] and not v['errors'] and v['contract'] for v in report['results'])
    assert len({(v['page'],v['selector']) for v in report['results']})==len(report['results'])
    retained=0;fresh=0
    for v in report['results']:
        if v.get('retained_from'):
            reference=v['retained_from'];assert reference['report']==raw_path.relative_to(ROOT).as_posix()
            before=raw['results'][reference['result_index']];assert before['passed'] and not before['errors'];assert before['page']!='m08-p20'
            stripped=dict(v);stripped.pop('retained_from');stripped['execution']=before['execution'];assert stripped==before;retained+=1
        else:assert v['page']=='m08-p20' and v['execution']=='new-modal-availability-correction';fresh+=1
    assert report['retained_executions']==retained and report['new_executions']==fresh
    corrected=next(v for v in report['inventory'] if v['page']=='m08-p20');original=next(v for v in raw['inventory'] if v['page']=='m08-p20')
    active={(v['selector'],v['label']) for v in corrected['controls']};blocked={(v['selector'],v['label']) for v in report['observation_correction']['blocked_controls']}
    assert not(active&blocked) and {(v['selector'],v['label']) for v in original['controls']}<=blocked
    assert active=={(v['selector'],v['label']) for v in report['observation_correction']['newly_available_controls']}
    assert all(v['blocked_by_modal'] for v in corrected['observed']['controls'] if (v['selector'],v['label']) in blocked)
    assert all(not v['blocked_by_modal'] for v in corrected['controls'])
    assert all(v['page']=='m08-p20' and (v['selector'],v['label']) in blocked and not v['errors'] for v in raw['results'] if not v['passed'])
    for dest,value in [(OUT,raw),(folder,report)]:
        for n,h in value['dependencies'].items():assert sha(dest/'source'/n)==h,n
        for n,h in value['fixture_sha256'].items():assert sha(dest/'fixtures'/n)==h and sha(ROOT/n)==h,n
    ids={v['id'] for v in read(DEMO/'manifest.json')};assert len(ids)==114 and {v['id'] for v in contracts['pages']}==ids
    all_controls=[]
    for v in contracts['pages']:
        assert (DEMO/'pages'/f"{v['id']}.html").read_bytes()==(DEMO/'custom'/f"{v['id']}.html").read_bytes()
        assert v['html_sha256']==sha(DEMO/v['html']);all_controls+=v['initial_controls']
        for control in v['initial_controls']:
            actual=report['results'][control['result_index']];assert actual['page']==v['id'] and actual['selector']==control['selector'] and actual['contract']==control['contract'] and actual['effective']==control['effective']
    assert len(all_controls)==len(report['results'])
    for edge in contracts['edges']:
        v=report['results'][edge['result_index']];assert edge['source']==v['page'] and edge['target'] in ids and edge['source']!=edge['target'] and edge['actual_url']==v['effective']
        assert edge['target']+'.html'==Path(urlparse(v['effective']).path).name
    assert len(re.findall(r'^\| m\d{2}-p\d{2} \|',(ROOT/'PAGE_CATALOG.md').read_text(encoding='utf-8'),re.M))==114
    assert len(re.findall(r'^  m\d{2}_p\d{2}\[',(ROOT/'CURRENT_INITIAL_NAVIGATION.mmd').read_text(encoding='utf-8'),re.M))==114
    assert len(re.findall(r'^\| m\d{2}-p\d{2} \|',(ROOT/'CONTROL_BEHAVIORS.md').read_text(encoding='utf-8'),re.M))==len(report['results'])
    history=ROOT/'evidence/history/pre-current-initial-catalog-8cce41c';old=read(history/'queue.json');queue=read(ROOT/'queue.json');assert len(queue)==len(old)==114
    for before,after in zip(old,queue):
        value=dict(after)
        for key in ['page_contract','current_initial_control_checks','current_initial_control_evidence']:
            if key in before:value[key]=before[key]
            else:value.pop(key,None)
        assert value==before,before['id']
        page=next(v for v in contracts['pages'] if v['id']==after['id']);assert after['current_initial_control_checks']==len(page['initial_controls']) and after['current_initial_control_evidence']['report_sha256']==sha(path)
    requirement_rows=lambda p:[line.split('|')[1:3] for line in p.read_text(encoding='utf-8').splitlines() if re.match(r'^\| \d+ ',line)]
    assert requirement_rows(history/'ACCEPTANCE_REQUIREMENTS.md')==requirement_rows(ROOT/'ACCEPTANCE_REQUIREMENTS.md') and len(requirement_rows(ROOT/'ACCEPTANCE_REQUIREMENTS.md'))==41
    value={'passed':True,'pages':114,'controls':len(report['results']),'retained_actual_executions':retained,'new_modal_executions':fresh,'blocked_background_observations':len(blocked),'raw_failures_preserved':sum(not v['passed'] for v in raw['results']),'observed_navigation_results':len(contracts['edges']),'dependencies':deps(),'report_sha256':sha(path),'contracts_sha256':sha(folder/'contracts.json'),'queue_acceptance_flags_unchanged':True,'original41_requirement_columns_unchanged':True,'human_accepted_pages':0,'producer_sha256':sha(Path(__file__)),'scope':'Declared114 initial fixtures and accessible controls only. Hidden/conditional outcomes, all error and return combinations, continuous journeys, full layout/visual review and original41 final acceptance remain open.'}
    value['served_source']=served
    dump(folder/'checkpoint.json',value);print('PASS114 pages;',len(report['results']),'current-source initial controls;',len(contracts['edges']),'observed navigation results;',len(served),'served bytes matched; original41 and acceptance flags preserved')

if __name__=='__main__':main()
