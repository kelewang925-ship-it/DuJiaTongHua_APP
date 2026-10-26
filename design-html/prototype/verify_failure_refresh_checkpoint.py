"""Bind isolated exception executions without treating names as all-branch coverage."""
import argparse
import hashlib
import json

from build_failure_operation_matrix import main as build_matrix
from refresh_failure_traces import JOBS
from verify_pet_controls import ROOT, source


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--session', type=int, required=True)
    parser.add_argument('--exit-code', type=int, required=True)
    args = parser.parse_args()
    assert args.exit_code == 0
    out = ROOT / 'evidence/current'
    files = source()
    meta_path = out / 'failure-trace-refresh-source.json'
    meta = json.loads(meta_path.read_text(encoding='utf-8'))
    assert meta['files'] == files
    styles = {p.relative_to(ROOT.parent).as_posix(): digest(p)
              for p in sorted((ROOT.parent / 'assets').glob('*.css'))}
    assert meta['styles'] == styles
    assert meta['expected_suites'] == len(meta['results']) == len(JOBS) == 14
    assert meta['expected_cases'] == 110
    for name, sha in meta['scripts_sha256'].items():
        assert digest(ROOT / name) == sha, name
    for name, sha in meta['preserved_reports'].items():
        assert digest(out / name) == sha, name
    for name, sha in meta['initial_preservation'].items():
        assert digest(ROOT / name) == sha, name
    for (script, original, count), record in zip(JOBS, meta['results']):
        assert record['script'] == script and record['exit_code'] == 0
        assert record['cases'] == record['passed'] == count
        assert digest(out / record['trace']) == record['trace_sha256']
        assert digest(out / record['report']) == record['report_sha256']
        trace = json.loads((out / record['trace']).read_text(encoding='utf-8'))
        assert trace['files'] == files and trace['exit_code'] == 0
        assert trace['report'].startswith('failure-traced-')
        assert trace['isolated_execution']['original_report_restored'] is True
        assert trace['isolated_execution']['child_exit_code'] == 0
    candidates_path = out / 'failure-operation-candidates.json'
    candidates = json.loads(candidates_path.read_text(encoding='utf-8'))
    assert candidates['script_sha256'] == digest(ROOT / 'audit_failure_candidates.cjs')
    assert candidates['literal_operation_count'] == 61
    assert len(candidates['candidates']) == 65 and len(candidates['dynamic_sites']) == 4
    # Existing matrix builder validates every trace, matching case/event and report.
    build_matrix()
    matrix_path = out / 'failure-operation-matrix.json'
    matrix = json.loads(matrix_path.read_text(encoding='utf-8'))
    assert matrix['files'] == files and matrix['cases'] == 110
    assert matrix['literal_observed'] == 61 and matrix['literal_untraced'] == 0
    assert set(matrix['traces']) == {r['trace'] for r in meta['results']}
    checkpoint = dict(
        files=files, styles=styles,
        execution=dict(session_id=args.session, exit_code=args.exit_code),
        metadata_sha256=digest(meta_path), matrix_sha256=digest(matrix_path),
        candidates_sha256=digest(candidates_path),
        scripts_sha256={**meta['scripts_sha256'], **{name: digest(ROOT / name) for name in
                         ['audit_failure_candidates.cjs', 'build_failure_operation_matrix.py',
                          'verify_failure_refresh_checkpoint.py']}},
        suites=14, cases=110, literal_operations=61, literal_sites=65, dynamic_sites=4,
        observed_operations=matrix['observed_operations'], accepted_pages=0,
        scope='Actual failure hook consumption in passing declared scenarios, with unchanged original reports and initial evidence. Distinct operation names are not every call site, input, permission, source, concurrency, timeout, native image or layout branch.')
    checkpoint_path = out / 'fresh-failure-refresh-checkpoint.json'
    checkpoint_path.write_text(json.dumps(checkpoint, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    state_path = out / 'current-evidence-state.json'
    state = json.loads(state_path.read_text(encoding='utf-8'))
    assert state['files'] == files and state['current_initial_controls'] == 752
    state.update(current_failure_literal_candidates=61, current_failure_trace_cases=110,
                 current_failure_refresh_checkpoint=checkpoint_path.relative_to(ROOT).as_posix(),
                 failure_candidate_all_conditions_complete=False, accepted_pages=0)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(suites=14, cases=110, literal_observed=61,
                         observed_operations=matrix['observed_operations'],
                         initial_evidence_preserved=True, accepted_pages=0)))


if __name__ == '__main__':
    main()
