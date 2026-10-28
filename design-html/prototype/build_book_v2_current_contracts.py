"""Publish actual V2 initial-control outcomes and navigation without rewriting history."""
import json,re
from pathlib import Path
from verify_book_v2_reconciliation import ROOT,dependencies,sha

def main():
    out=ROOT/'evidence/current/book-v2-controls';report_path=out/'results.json';report=json.loads(report_path.read_text(encoding='utf-8'));inventory=json.loads((out/'inventory.json').read_text(encoding='utf-8'));files=dependencies()
    assert report['dependency_files']==inventory['dependency_files']==files
    rows=report['results'];assert len(rows)==156 and all(r['passed'] for r in rows)
    keys={(r['page'],r['selector']) for r in rows};assert len(keys)==156
    observed={(r['page'],c['selector']) for r in inventory['results'] for c in r['controls'] if c['visible'] and not c['disabled'] and not c['blocked_by_modal']};assert keys==observed
    assert report['producer_sha256']==sha(ROOT/'verify_book_v2_initial_controls.py')
    prior_path=out/'before-v2-contract-corrections/results.json';prior=json.loads(prior_path.read_text(encoding='utf-8'));assert report['prior_report_sha256']==sha(prior_path)
    assert prior['producer_sha256']==sha(prior_path.parent/'verify_book_v2_initial_controls.py')
    previous={(r['page'],r['selector']):r for r in prior['results']}
    for r in rows:
        if r.get('retained_from'):
            old=previous[(r['page'],r['selector'])];assert old['passed'] and old=={k:v for k,v in r.items() if k!='retained_from'}
    pages=[];edges=[]
    for entry in inventory['results']:
        controls=[r for r in rows if r['page']==entry['page']]
        pages.append(dict(id=entry['page'],headings=entry['headings'],initial_url=entry['effective'],initial_overlay_count=entry['dialogs'],controls=controls))
        for row in controls:
            kind=row['contract'];label=row['label'].replace('\n',' ')
            if kind.startswith(('route:','read-route:')):
                dest=kind.split(':',1)[1].split('?')[0];edges.append(dict(origin=row['page'],control=label,destination=dest,query_contract=kind.split(':',1)[1].partition('?')[2],actual_url=row['effective']))
            elif kind in ['reader-prev','reader-next']:edges.append(dict(origin=row['page'],control=label,destination=row['page'],behavior='same-document reader fragment, exact read anchor persisted',actual_url=row['effective']))
    result=dict(scope='Current21 memory-book initial fixtures only. Hidden controls and conditional states remain separate; other93 pages retain their prior evidence.',dependency_files=files,report_sha256=sha(report_path),inventory_sha256=sha(out/'inventory.json'),controls=156,new_executions=report['new_executions'],retained_executions=report['retained_executions'],pages=pages,navigation_edges=edges,human_accepted_pages=0,producer_sha256=sha(Path(__file__)))
    (out/'contracts.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['flowchart TD']
    for entry in pages:lines.append('  '+entry['id'].replace('-','_')+'["'+entry['id']+'"]')
    for edge in edges:
        label=edge['control'].replace('"','').replace('|','/');lines.append('  '+edge['origin'].replace('-','_')+' -->|"'+label+'"| '+edge['destination'].replace('-','_'))
    (ROOT/'BOOK_V2_CURRENT_NAVIGATION.mmd').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('PASS156 current initial-control contracts;21 pages;',len(edges),'observed navigation edges;',report['new_executions'],'new +',report['retained_executions'],'retained executions')

if __name__=='__main__':main()
