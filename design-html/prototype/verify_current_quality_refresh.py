"""Verify exact current-source geometry, actual Tab and native-modal boundaries."""
import json
from replay_current_initial_controls import ROOT, DEMO, deps, sha, dump

def main():
    folder=ROOT/'evidence/current/quality-file-target-20261031'
    report=folder/'results.json';data=json.loads(report.read_text(encoding='utf-8'))
    assert data['complete'] and data['all_passed'] and data['dependencies']==deps()
    ids={v['id'] for v in json.loads((DEMO/'manifest.json').read_text(encoding='utf-8'))}
    rows=data['results'];assert len(rows)==570
    baseline_folder=ROOT/'evidence/current/quality-20261031'
    baseline_path=baseline_folder/'results.json';baseline=json.loads(baseline_path.read_text(encoding='utf-8'))
    assert baseline['complete'] and not baseline['all_passed']
    assert [(r['page'],r['width']) for r in baseline['results'] if not r['passed']]==[('m08-p19',w) for w in [320,375,390,414,430]]
    css='assets/prototype-book-v2.css'
    assert [n for n,h in deps().items() if baseline['dependencies'][n]!=h]==[css]
    before=(baseline_folder/'source'/css).read_bytes();after=(DEMO/css).read_bytes()
    patch=data['reconciliation']['patch']
    assert after==before+patch.encode('utf-8')
    assert patch.replace('\r\n','\n')=='.book-v2[data-book-page="19"] .v2-upload input[type="file"]{min-height:var(--prototype-touch,44px)}\n.book-v2[data-book-page="19"] .v2-upload input[type="file"]::file-selector-button{min-height:var(--prototype-touch,44px);font:inherit}\n'
    assert sha(baseline_path)==data['reconciliation']['baseline_report_sha256']
    for sub,mapping in [('source',baseline['dependencies']),('fixtures',baseline['fixture_sha256'])]:
        for n,h in mapping.items():assert sha(baseline_folder/sub/n)==h,n
    five_path=folder/'five-layout-results.json';assert sha(five_path)==data['reconciliation']['five_layout_report_sha256']
    five=json.loads(five_path.read_text(encoding='utf-8'))
    assert len(five['results'])==5 and all(r['passed'] for r in five['results'])
    baseline_rows={(r['page'],r['width']):r for r in baseline['results']}
    for row in rows:
        if row['execution']=='retained-unaffected':
            assert row['page']!='m08-p19' and row['provenance']['sha256']==sha(baseline_path)
            assert {k:v for k,v in row.items() if k not in ['execution','provenance']}==baseline_rows[row['page'],row['width']]
        else:
            assert row['execution']=='fresh' and row['page']=='m08-p19'
            assert {k:v for k,v in row.items() if k!='execution'}==next(r for r in five['results'] if r['width']==row['width'])
    assert sum(r['execution']=='fresh' for r in rows)==5
    assert len(data['photo_flows'])==5 and all(r['passed'] and r['file_height']>=44 and r['native_button_min_height']>=44 for r in data['photo_flows'])
    assert sha(ROOT/'replay_quality_file_target.py')==data['reconciliation']['sha256']==sha(folder/'fixtures/replay_quality_file_target.py')
    assert {(r['page'],r['width']) for r in rows}=={(page,width) for page in ids for width in [320,375,390,414,430]}
    for sub,mapping in [('source',data['dependencies']),('fixtures',data['fixture_sha256'])]:
        for n,h in mapping.items():
            assert sha(folder/sub/n)==h,n
            if sub=='fixtures':assert sha(ROOT/n)==h,n
    for n,h in data['preserved_reports'].items():assert sha(ROOT/n)==h,n
    keyboard=[];modal=[]
    for row in rows:
        assert row['passed'] and not any(row['failures'].values())
        assert row['effective'].split('?')[0].endswith('/'+row['page']+'.html')
        if row['native_modal']:modal.append({'page':row['page'],'width':row['width']})
        if row['width']==390:
            assert not row['keyboard']['unreached'] and not row['keyboard']['noVisibleFocus']
            assert row['keyboard']['expected']
            keyboard.extend(row['keyboard']['visited'])
            image_folder=folder if row['execution']=='fresh' else baseline_folder
            assert (image_folder/(row['page']+'.png')).is_file()
        else:assert row['keyboard'] is None
    assert modal==[{'page':'m08-p20','width':w} for w in [320,375,390,414,430]]
    result={'passed':True,'producer_sha256':sha(ROOT/'verify_current_quality_refresh.py'),'report_sha256':sha(report),'product_dependencies':len(deps()),'pages':114,'geometry_cases':570,'fresh_geometry_cases':5,'retained_unaffected_cases':565,'photo_flows':5,'keyboard_pages':114,'actual_tab_observations':len(keyboard),'native_modal_cases':modal,'screenshots':{str(p.relative_to(ROOT)).replace(chr(92),'/'):sha(p) for source in [baseline_folder,folder] for p in source.glob('m??-p??.png')},'human_accepted_pages':0,'scope':'Canonical initial fixtures only, five widths,844px height, simulated44/34 safe insets, reduced motion. Geometry and keyboard do not imply visual fidelity or native IME/AT validation.'}
    dump(folder/'checkpoint.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['screenshots','native_modal_cases']},ensure_ascii=False))

if __name__=='__main__':main()
