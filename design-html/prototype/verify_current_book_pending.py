"""Check real V2 pending executions, exact case scope and preserved evidence."""
import json
from replay_current_book_pending import ROOT, DEMO, OUT, JOBS, fixtures, deps, sha


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    summary = read(OUT / 'results.json')
    assert summary['complete'] and summary['all_passed'] and summary['expected_cases'] == 34
    assert summary['dependencies'] == deps() and summary['fixture_sha256'] == fixtures()
    assert all(sha(ROOT / p) == h for p, h in summary['preserved_reports'].items())
    for mapping, prefix, source in [(summary['dependencies'], 'source', DEMO), (summary['fixture_sha256'], 'fixtures', ROOT)]:
        for name, digest in mapping.items():
            assert sha(OUT / prefix / name) == sha(source / name) == digest
    assert summary['observation_sha256'] == sha(OUT / 'current-observations.json')
    assert len(summary['results']) == len(JOBS) == 6
    count = 0
    for execution, (script, args, expected, _) in zip(summary['results'], JOBS):
        folder = OUT / script.removesuffix('.py')
        assert execution == read(folder / 'execution.json')
        assert execution['script'] == script and execution['arguments'] == args
        assert execution['exit_code'] == 0 and execution['cases'] == execution['passed'] == expected
        report = read(folder / 'results.json')
        assert sha(folder / 'results.json') == execution['report_sha256']
        assert report['script_sha256'] == sha(ROOT / script)
        assert all(summary['dependencies'].get(p) == h for p, h in report['files'].items())
        assert all(sha(DEMO / p) == h for p, h in report['styles'].items())
        rows = report['results']
        assert len(rows) == expected and all(r['passed'] and not r['errors'] for r in rows)
        if script == 'verify_pending_page_guard.py':
            assert {(r['case'], r['exit'], r['mode']) for r in rows} == {('book-theme', e, m) for e in ['button', 'back'] for m in ['keep', 'discard']}
            assert all(r['storage_unchanged_before_decision'] for r in rows)
            assert all(r['retry_saved_once_and_reload_consistent'] if r['mode'] == 'keep' else r['discard_reload_consistent'] for r in rows)
        elif script == 'verify_submission_changes.py':
            assert rows[0]['case'] == 'book-theme' and rows[0]['kind'] == 'edit'
            assert rows[0]['unchanged_before_retry']
        elif script == 'verify_pending_form_cancel.py':
            assert {(r['index'], r['method']) for r in rows} == {(i, m) for i in [118, 122, 129] for m in ['button', 'escape', 'back', 'backdrop', 'drag', 'keep']}
            assert all(r['storage_unchanged_before_decision'] for r in rows)
            assert all(r['retry_persisted'] if r['method'] == 'keep' else r['storage_unchanged_after_discard'] and r['reload_consistent'] for r in rows)
        elif script == 'verify_pending_image_reads.py':
            assert {(r['case'], r['mode']) for r in rows} == {('book-supplement', m) for m in ['success', 'decode-failure']}
            assert all(r['unchanged_while_image_reading'] and r['save_during_read_blocked'] and r['explicit_retry_and_reload_consistent'] for r in rows)
        elif script == 'verify_image_pending_exit.py':
            assert {(r['case'], r['method'], r['mode']) for r in rows} == {('book-supplement', e, m) for e in ['button', 'browser'] for m in ['keep-success', 'keep-failure', 'discard-held']}
            assert all(r['pending_image_only_protected'] and not r['native_dialogs'] for r in rows)
        else:
            assert {(r['case'], r['mode']) for r in rows} == {('book-supplement', m) for m in ['cancel', 'success', 'decode-failure']}
            assert all(r['unchanged_before_chooser_result'] and r['explicit_retry_and_reload_consistent'] for r in rows)
        count += len(rows)
    assert count == 34
    print('PASS34 current V2 pending boundaries;6 isolated suites;real storage and image operations;original reports preserved')


if __name__ == '__main__':
    main()
