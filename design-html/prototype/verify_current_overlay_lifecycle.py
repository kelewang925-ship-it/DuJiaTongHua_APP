"""Verify exact current candidates, fresh closure matrix and archived bytes."""
import json
from collections import Counter
from replay_current_overlay_lifecycle import ROOT, DEMO, OUT as RAW, CATALOG, deps, sha, fixture_files

OUT = RAW.with_name(RAW.name + '-final')


def main(published=True):
    report = json.loads((OUT / 'results.json').read_text(encoding='utf-8'))
    assert report['complete'] and report['all_passed']
    assert report['dependencies'] == deps()
    assert report['fixture_sha256'] == fixture_files()
    assert report['catalog_sha256'] == sha(CATALOG) == sha(RAW / 'input-contracts.json')
    baseline = json.loads((RAW / 'results.json').read_text(encoding='utf-8'))
    assert report['baseline_report_sha256'] == sha(RAW / 'results.json')
    assert report['fresh_report_sha256'] == sha(OUT / 'fresh-photo-close.json')
    assert report['reconciliation_producer_sha256'] == sha(ROOT / 'reconcile_overlay_lifecycle_photo_close.py')
    fresh = json.loads((OUT / 'fresh-photo-close.json').read_text(encoding='utf-8'))
    assert report['retained_cases'] == 570 and report['fresh_cases'] == 1
    assert len(baseline['results']) == 571 and sum(r['passed'] for r in baseline['results']) == 570
    assert {k: report[k] for k in ['inventory', 'candidates', 'dependencies', 'fixture_sha256']} == {k: baseline[k] for k in ['inventory', 'candidates', 'dependencies', 'fixture_sha256']}
    for old, new in zip(baseline['results'], report['results'], strict=True):
        assert new == (old if old['passed'] else fresh)
    for sub, origin, mapping in [('source', DEMO, report['dependencies']), ('fixtures', ROOT, report['fixture_sha256'])]:
        for name, digest in mapping.items():
            assert sha(origin / name) == sha(RAW / sub / name) == digest, name
    catalog = json.loads(CATALOG.read_text(encoding='utf-8'))
    candidates = [dict(c, group=p['fixture_group']) for p in catalog['pages']
                  for c in p['initial_controls'] if c['contract'].startswith(('sheet:', 'modal:'))]
    assert report['candidates'] == candidates and len(candidates) == 104
    inventory = report['inventory']
    assert len(inventory) == 104
    assert {r['candidate_index'] for r in inventory} == set(range(104))
    expected = set()
    for observation in inventory:
        i = observation['candidate_index']
        candidate = candidates[i]
        assert all(observation[k] == candidate[k] for k in ['page', 'selector', 'label'])
        assert len(observation['overlays']) == 1
        assert observation['overlays'][0]['title'] == candidate['contract'].split(':', 1)[1]
        methods = ['escape', 'button', 'backdrop', 'back'] + (['drag'] if observation['sheet'] else [])
        assert observation['methods'] == methods
        for dirty in ([False, True] if observation['editable_submit'] else [False]):
            expected.update((i, method, dirty) for method in methods)
    actual = [(r['candidate_index'], r['method'], r['dirty']) for r in report['results']]
    assert len(actual) == len(set(actual)) and set(actual) == expected
    for row in report['results']:
        assert row['page'] == candidates[row['candidate_index']]['page']
        assert row['passed'] and not row['errors']
        assert all(row[k] for k in ['storage_preserved', 'underlying_page_preserved', 'focus_returned'])
        if row['dirty']:
            assert row['continue_preserved_fields']
    if published:
        summary = json.loads((OUT / 'summary.json').read_text(encoding='utf-8'))
        controls = json.loads((OUT / 'controls.json').read_text(encoding='utf-8'))
        assert summary['report_sha256'] == controls['report_sha256'] == sha(OUT / 'results.json')
        assert summary['controls_sha256'] == sha(OUT / 'controls.json')
        assert summary['document_sha256'] == sha(ROOT / 'CURRENT_OVERLAY_LIFECYCLE.md')
        assert summary['producer_sha256'] == sha(ROOT / 'publish_current_overlay_lifecycle.py')
        assert summary['verifier_sha256'] == sha(ROOT / 'verify_current_overlay_lifecycle.py')
        observed = [(o['candidate_index'], j, c) for o in inventory for j, c in enumerate(o['overlays'][0]['controls'])]
        indexed = [(c['candidate_index'], c['control_index'], c['control']) for c in controls['controls']]
        assert observed == indexed and len(indexed) == summary['counts']['observed_control_appearances'] == 290
        for c in controls['controls']:
            assert c['lifecycle_result_indices'] == [n for n, r in enumerate(report['results']) if r['candidate_index'] == c['candidate_index']]
        assert summary['counts']['entries'] == 104 and summary['counts']['cases'] == summary['counts']['passed'] == len(actual) == 571
        assert summary['counts']['dirty'] == 80 and summary['counts']['editable_forms'] == 16
    print(json.dumps(dict(entries=104, cases=len(actual), dirty=sum(r['dirty'] for r in report['results']),
                          methods=dict(Counter(r['method'] for r in report['results'])),
                          source_files=len(report['dependencies']), fixtures=len(report['fixture_sha256']))))


if __name__ == '__main__':
    main()
