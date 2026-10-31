"""Audit deliverable inventory and provenance; never upgrade historical test results."""
import json,re,hashlib
from pathlib import Path
from verify_pet_controls import source

ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def artifact_sha(p):return hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()

def main():
    catalog_path=ROOT/'evidence/current/page-contracts.json';catalog=json.loads(catalog_path.read_text(encoding='utf-8'));current=source()
    queue=json.loads((ROOT/'queue.json').read_text(encoding='utf-8'));manifest=json.loads((ROOT.parent/'manifest.json').read_text(encoding='utf-8'))
    ids={v['id'] for v in manifest};assert len(ids)==114 and len(queue)==114 and {v['id'] for v in queue}==ids
    assert len(catalog['pages'])==114 and {v['id'] for v in catalog['pages']}==ids
    assert all((ROOT.parent/'pages'/f'{id}.html').is_file() and (ROOT.parent/'custom'/f'{id}.html').is_file() for id in ids)
    requirements=(ROOT/'ACCEPTANCE_REQUIREMENTS.md').read_text(encoding='utf-8');assert [int(n) for n in re.findall(r'^\| (\d+) ',requirements,re.M)]==list(range(1,42))
    groups=[('页面清单',['PAGE_CATALOG.md','evidence/current/page-contracts.json']),('页面关系',['CURRENT_NAVIGATION.md','PAGE_RELATIONSHIPS.mmd']),('组件规范',['COMPONENTS.md','ORIGINAL_COMPONENT_DECISIONS.md','TOKEN_COVERAGE.md']),('交互规则',['INTERACTION_RULES.md','CONTROL_BEHAVIORS.md']),('状态规则',['STATE_RULES.md','STATE_MATRIX.md']),('动效规则',['MOTION_RULES.md']),('问题与验收',['ISSUES.md','ACCEPTANCE_REQUIREMENTS.md'])]
    artifacts=[]
    for title,names in groups:
        assert all((ROOT/n).is_file() for n in names)
        artifacts.append({'deliverable':title,'files':{n:artifact_sha(ROOT/n) for n in names},'hash_mode':'UTF-8 text bytes with CRLF normalized to LF','content_acceptance':'Existence and provenance checked; full current behavior coverage is not proved by file presence.'})
    old=catalog['files'];changed={n:{'catalog':h,'current':current.get(n)} for n,h in old.items() if current.get(n)!=h};added={n:h for n,h in current.items() if n not in old}
    result={'pages':114,'original_requirement_rows':41,'deliverables':artifacts,'catalog_sha256':sha(catalog_path),'catalog_dependencies':old,'current_dependencies':current,'changed_dependencies':changed,'added_dependencies':added,'catalog_current_execution_proven':old==current,'historically_current_labelled_controls':sum(c['status']=='当前源码通过' for p in catalog['pages'] for c in p['control_evidence']),'human_accepted_pages':sum(bool(v.get('visual_self_review',{}).get('accepted')) for v in queue),'scope':'Inventory and source freshness only. Historical control results and all acceptance flags are preserved. Current114 flows, states, exceptions, visual work and original41 acceptance remain open.','producer_sha256':sha(Path(__file__))}
    dest=ROOT/'evidence/current/deliverable-freshness';dest.mkdir(parents=True,exist_ok=True)
    (dest/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (dest/'producer.py').write_bytes(Path(__file__).read_bytes())
    print('Inventory114 / requirements41 / deliverables7; changed',len(changed),'added',len(added),'historical current-labelled controls',result['historically_current_labelled_controls'],'full current execution proven',result['catalog_current_execution_proven'])

if __name__=='__main__':main()
