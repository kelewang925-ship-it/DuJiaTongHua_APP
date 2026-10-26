"""Verify the270 refreshed contracts and preservation of every prior watched artifact."""
import argparse
import hashlib
import json
from pathlib import Path

from refresh_submit_boundaries import JOBS
from verify_pet_controls import ROOT, DEMO, source


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--session', type=int, required=True)
    parser.add_argument('--exit-code', type=int, required=True); args = parser.parse_args()
    assert args.exit_code == 0
    folder = ROOT / 'evidence/current/submit-boundary-refresh'
    metadata_path = folder / 'executions.json'; metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
    assert metadata['files'] == source()
    assert metadata['styles'] == {p.relative_to(DEMO).as_posix(): sha(p) for p in (DEMO / 'assets').glob('*.css')}
    assert metadata['script_sha256'] == sha(ROOT / 'refresh_submit_boundaries.py')
    assert metadata['report_wrapper_sha256'] == sha(ROOT / 'run_suite_report_isolated.py')
    assert [row['name'] for row in metadata['results']] == [job[0] for job in JOBS]
    reports = {}
    for row, job in zip(metadata['results'], JOBS):
        assert row['exit_code'] == 0 and row['cases'] == row['passed'] == row['expected'] == job[3] and row['errors'] == 0
        assert sha(ROOT / row['script']) == row['script_sha256']
        report = ROOT / row['report']; assert sha(report) == row['report_sha256']
        payload = json.loads(report.read_text(encoding='utf-8'))
        assert payload['files'] == metadata['files'] and len(payload['results']) == job[3]
        assert all(case['passed'] and not case.get('errors') for case in payload['results'])
        for name,digest in row['restored_originals_sha256'].items(): assert sha(ROOT / name) == digest, name
        for name,digest in row['generated_screenshots_sha256'].items(): assert sha(ROOT / name) == digest, name
        reports[row['report']] = row['report_sha256']
    assert sum(row['cases'] for row in metadata['results']) == 270
    checkpoint = dict(files=metadata['files'], styles=metadata['styles'], cases=270,
                      actual_app_cases=246, synthetic_shared_helper_cases=24, accepted_pages=0,
                      actual_execution=dict(session=args.session,exit_code=0),
                      interrupted_execution=dict(session=49922,exit_code=1,reason='OS report write error; no completed suite claimed'),
                      reports_sha256=reports, metadata_sha256=sha(metadata_path),
                      verification_script_sha256=sha(Path(__file__)),
                      scope='Named pending submit, return, editing, chooser and image boundaries. Original reports/screenshots retained byte-for-byte; does not establish all other state or human visual acceptance.')
    (folder / 'checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(cases=270,actual_app_cases=246,synthetic_helper_cases=24,accepted_pages=0)))


if __name__ == '__main__':
    main()
