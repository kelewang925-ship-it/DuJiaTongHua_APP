"""Independently verify executed suites, retained provenance and control links."""
import json
from collections import Counter
from pathlib import Path
from replay_current_initial_controls import ROOT, DEMO, deps, sha
from replay_current_hidden_business import OUT as RAW, fixture_files as initial_fixtures
from complete_current_hidden_business import OUT as FINAL, fixture_files as final_fixtures
from replay_current_hidden_pickers import OUT as PICKERS


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main(published=True):
    baseline = load(RAW / 'results.json')
    final = load(FINAL / 'results.json')
    pickers = load(PICKERS / 'execution.json')
    index = load(FINAL / 'control-business-index.json')
    files = deps()
    assert baseline['complete'] and not baseline['all_passed']
    assert final['complete'] and final['all_passed'] and pickers['all_passed']
    assert baseline['dependencies'] == final['dependencies'] == pickers['dependencies'] == index['dependencies'] == files
    for name, digest in files.items():
        assert sha(DEMO / name) == sha(RAW / 'source' / name) == digest
    assert final['baseline_sha256'] == sha(RAW / 'results.json')
    assert final['retained_cases'] == 108 and final['fresh_cases'] == 123
    failures = [r for r in baseline['results'] if r['exit_code'] != 0]
    assert len(failures) == 1 and failures[0]['script'] == 'verify_book_v2_hidden_editors.py' and failures[0]['cases'] == 0
    error = (RAW / 'verify_book_v2_hidden_editors/runner-error.txt').read_text(encoding='utf-8')
    assert "inventory['dependency_files']==files" in error
    raw_book = load(RAW / 'inputs/current-book-inventory.json')
    book = load(FINAL / 'inputs/current-book-inventory.json')
    assert len(raw_book['dependency_files']) == 201 and len(book['dependency_files']) == 63
    assert raw_book['results'] == book['results']
    assert all(files.get(k) == v for k, v in book['dependency_files'].items())
    for folder, mapping in [(RAW, baseline['fixture_sha256']), (FINAL, final['fixture_sha256']), (PICKERS, pickers['fixture_sha256'])]:
        for name, digest in mapping.items():
            assert sha(ROOT / name) == sha(folder / 'fixtures' / name) == digest
    assert baseline['fixture_sha256'] == initial_fixtures()
    assert final['fixture_sha256'] == final_fixtures()
    for batch in [baseline, final]:
        for name, digest in batch['preserved_reports'].items():
            assert sha(ROOT / name) == digest
    original_success = {r['script']: r for r in baseline['results'] if r['exit_code'] == 0}
    assert len(final['results']) == 12 and len({r['script'] for r in final['results']}) == 12
    total = 0
    for suite in final['results']:
        if suite.get('retained_from'):
            assert {k: v for k, v in suite.items() if k != 'retained_from'} == original_success[suite['script']]
            path = ROOT / suite['retained_from']
        else:
            path = FINAL / suite['script'].removesuffix('.py') / suite['report']
        execution_path = path.parent / 'execution.json'
        execution = load(execution_path)
        assert suite['execution_sha256'] == sha(execution_path)
        assert execution['report_sha256'] == sha(path)
        assert suite['exit_code'] == execution['exit_code'] == 0
        rows = load(path)['results']
        assert len(rows) == suite['cases'] == suite['passed'] == suite['expected_cases']
        assert all(r['passed'] and not r.get('errors', []) for r in rows)
        total += len(rows)
    assert total == 231
    picker_rows = load(PICKERS / 'picker-results.json')['results']
    birthday = load(PICKERS / 'birthday-clear.json')
    assert pickers['picker_report_sha256'] == sha(PICKERS / 'picker-results.json')
    assert pickers['birthday_report_sha256'] == sha(PICKERS / 'birthday-clear.json')
    assert pickers['suite_exit_code'] == 0 and len(picker_rows) == pickers['picker_cases'] == pickers['picker_passed'] == 50
    assert all(r['passed'] and not r['errors'] for r in picker_rows)
    assert Counter(r['width'] for r in picker_rows) == {320: 10, 360: 10, 390: 10, 414: 10, 430: 10}
    assert birthday['passed'] and not birthday['errors']
    assert all(birthday[k] for k in ['clear_is_candidate', 'failed_save_preserved', 'retry_persisted', 'reopened_empty', 'unrelated_data_preserved'])
    catalog = load(RAW / 'catalog-overlays.json')
    assert catalog['dependencies'] == files and len(catalog['observations']) == 6 and len(catalog['results']) == 24
    assert {(r['historical_observation_index'], r['method']) for r in catalog['results']} == {(i, m) for i in [74, 75, 76, 77, 79, 80] for m in ['escape', 'button', 'backdrop', 'back']}
    assert all(r['passed'] and not r['errors'] for r in catalog['results'])
    drag = load(RAW / 'catalog-drag-results.json')
    assert len(drag['results']) == 6 and {r['historical_observation_index'] for r in drag['results']} == {74, 75, 76, 77, 79, 80}
    assert all(r['passed'] and r['method'] == 'drag' and not r['errors'] for r in drag['results'])
    assert drag['dependencies'] == files and drag['input_sha256'] == sha(RAW / 'catalog-overlays.json')
    assert drag['producer_sha256'] == sha(ROOT / 'verify_catalog_sheet_drag.py') == sha(RAW / 'extra-fixtures/verify_catalog_sheet_drag.py')
    assert drag['fixture_sha256'] == sha(ROOT / 'verify_pet_controls.py')
    assert index['business_summary_sha256'] == sha(FINAL / 'results.json')
    assert index['picker_execution_sha256'] == sha(PICKERS / 'execution.json')
    assert index['catalog_overlays_sha256'] == sha(RAW / 'catalog-overlays.json')
    assert index['catalog_drag_sha256'] == sha(RAW / 'catalog-drag-results.json')
    assert index['producer_sha256'] == sha(ROOT / 'build_current_hidden_business_index.py')
    assert index['observed_overlays'] == len(index['observations']) == 110
    assert index['observed_controls'] == index['mapped_controls'] == len(index['items']) == 302 and index['missing_controls'] == 0
    assert len({(i['observation'], i['control_index']) for i in index['items']}) == 302
    observations = {o['id']: o for o in index['observations']}
    assert sum(len(o['controls']) for o in observations.values()) == 302
    allowed = {(RAW / r['script'].removesuffix('.py') / 'results.json').relative_to(ROOT).as_posix() for r in baseline['results'] if r['exit_code'] == 0}
    allowed.update((FINAL / r['script'].removesuffix('.py') / r['report']).relative_to(ROOT).as_posix() for r in final['results'] if not r.get('retained_from'))
    allowed.update([(PICKERS / 'picker-results.json').relative_to(ROOT).as_posix(), (PICKERS / 'birthday-clear.json').relative_to(ROOT).as_posix(),
                    (RAW / 'catalog-overlays.json').relative_to(ROOT).as_posix(), (RAW / 'catalog-drag-results.json').relative_to(ROOT).as_posix(),
                    'evidence/current/overlay-lifecycle-20261031-final/results.json'])
    for item in index['items']:
        assert item['control'] == observations[item['observation']]['controls'][item['control_index']]
        assert item['mapping_kind'] and item['business_contract'] and item['business_evidence'] and item['lifecycle_evidence']
        for evidence in item['business_evidence'] + item['lifecycle_evidence']:
            assert evidence['report'] in allowed
            path = ROOT / evidence['report']
            assert sha(path) == evidence['sha256']
            payload = load(path)
            row = payload if evidence['row'] is None else payload['results'][evidence['row']]
            assert row['passed'] and not row.get('errors', [])
    if published:
        publishing = load(FINAL / 'publishing.json')
        assert publishing['summary_document_sha256'] == sha(ROOT / 'CURRENT_HIDDEN_BUSINESS.md')
        assert publishing['controls_document_sha256'] == sha(ROOT / 'CURRENT_HIDDEN_CONTROL_BEHAVIORS.md')
        assert publishing['index_sha256'] == sha(FINAL / 'control-business-index.json')
        assert publishing['producer_sha256'] == sha(ROOT / 'publish_current_hidden_business.py')
        assert publishing['verifier_sha256'] == sha(Path(__file__))
        assert publishing['extra_closes'] == 30
    print('PASS 231 business +50 picker +1 birthday cases;30 catalog closes;110 overlays/302 controls linked;201 product dependencies unchanged')


if __name__ == '__main__':
    main()
