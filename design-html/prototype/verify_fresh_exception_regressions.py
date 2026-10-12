"""Verify executed regression reports without merging repeated initial controls."""
import argparse
import ast
import hashlib
import json
from urllib.request import urlopen
from verify_pet_controls import ROOT, BASE, source


def main():
    parser = argparse.ArgumentParser()
    for batch in ('product', 'time'):
        parser.add_argument('--' + batch + '-session', type=int, required=True)
        parser.add_argument('--' + batch + '-exit', type=int, required=True)
    args = parser.parse_args()
    assert args.product_exit == args.time_exit == 0
    out = ROOT / 'evidence/current'
    files = source()
    digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    batches = {}
    for batch, expected in [('product', 32), ('time', 131)]:
        meta_path = out / (batch + '-journey-regression-source.json')
        meta = json.loads(meta_path.read_text(encoding='utf-8'))
        assert meta['files'] == files
        reports = {}
        for logical, record in meta['reports'].items():
            artifact = meta.get('artifact_files', {}).get(logical, logical)
            path = out / artifact
            assert digest(path) == record['sha256'], artifact
            payload = json.loads(path.read_text(encoding='utf-8'))
            rows = payload['results'] if isinstance(payload, dict) else payload
            assert record['exit_code'] == 0
            assert len(rows) == record['cases'] == record['passed']
            assert all(row['passed'] and not row.get('errors') for row in rows)
            reports[logical] = dict(record, artifact=artifact)
        assert sum(r['cases'] for r in reports.values()) == expected
        runner = ROOT / ('verify_' + batch + '_journey_regressions.py')
        tree = ast.parse(runner.read_text(encoding='utf-8'))
        declarations = [n.value for n in tree.body if isinstance(n, ast.Assign)
                        and any(isinstance(t, ast.Name) and t.id == 'jobs' for t in n.targets)]
        jobs = ast.literal_eval(declarations[0]) if declarations else [
            (script, [], report) for script, report in ast.literal_eval(next(
                n.iter for n in tree.body if isinstance(n, ast.For)
                and isinstance(n.target, ast.Tuple)))]
        assert {job[2] for job in jobs} == set(reports)
        batches[batch] = dict(session_id=getattr(args, batch + '_session'),
                              exit_code=getattr(args, batch + '_exit'), cases=expected,
                              metadata_sha256=digest(meta_path), reports=reports,
                              script_sha256={name: digest(ROOT/name) for name in {runner.name, *(j[0] for j in jobs)}})
    initial = json.loads((out/'consolidated-initial-replay-checkpoint.json').read_text(encoding='utf-8'))
    assert digest(out/'time-controls-results.json') == initial['reports']['time-controls-results.json']['sha256']
    candidates_path = out/'failure-operation-candidates.json'
    candidates = json.loads(candidates_path.read_text(encoding='utf-8'))
    for name, sha in candidates['files'].items():
        assert digest(ROOT.parent/'assets'/name) == sha
    for name, sha in files.items():
        with urlopen(BASE + name.replace('custom/', 'pages/', 1), timeout=10) as response:
            assert hashlib.sha256(response.read()).hexdigest() == sha
    checkpoint = dict(files=files, batches=batches, total=163, repeated_initial_controls=54,
                      additional_beyond_initial=109, layout_checks=35, layout_pages=7,
                      failure_candidates_sha256=digest(candidates_path), accepted_pages=0,
                      scope='Executed named regressions only. Source failure candidates are not runtime coverage. Layout checks cover seven time pages at five widths, not all 114 pages.')
    (out/'fresh-exception-regressions-checkpoint.json').write_text(json.dumps(checkpoint, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    path = out/'current-evidence-state.json'
    state = json.loads(path.read_text(encoding='utf-8'))
    assert state['files'] == files
    state.update(current_product_regression_checks=32, current_time_regression_checks=131,
                 current_regression_layout_checks=35, current_failure_literal_candidates=61,
                 failure_candidates_are_unproven=True, accepted_pages=0)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(product=32, time=131, repeated_initial=54, additional=109, layout=35, accepted_pages=0)))


if __name__ == '__main__':
    main()
