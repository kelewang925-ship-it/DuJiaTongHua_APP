"""Complete the unexecuted editor suite and current save/delete consumers.

The first execution is immutable. Correct the newly generated inventory's
dependency scope, then run only the missing editor cases and additional suites.
"""
import argparse
import ast
import json
import subprocess
import sys
import traceback
from pathlib import Path
from replay_current_hidden_business import OUT as RAW, ROOT, DEMO, JOBS, child as original_child
import replay_current_hidden_business as initial
from replay_current_initial_controls import deps, sha, dump
from verify_book_v2_reconciliation import dependencies as book_dependencies
from verify_pet_controls import source

OUT = RAW.with_name(RAW.name + '-final')
ADDITIONAL = [
    ('verify_overlay_form_saves.py', 'overlay-form-save-results.json', 47),
    ('verify_confirmed_deletions.py', 'confirmed-deletion-results.json', 45),
    ('verify_identity_deletions.py', 'identity-deletion-results.json', 13),
]


def fixture_files():
    pending = [Path(__file__).resolve()] + [ROOT / n for n, _, _ in ADDITIONAL]
    found = set()
    while pending:
        path = pending.pop()
        if path in found:
            continue
        found.add(path)
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            names = ([node.module.split('.')[0] + '.py'] if isinstance(node, ast.ImportFrom) and node.module else
                     [a.name.split('.')[0] + '.py' for a in node.names] if isinstance(node, ast.Import) else
                     [node.value] if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value.endswith('.py') else [])
            for name in names:
                other = ROOT / name
                if other.is_file() and other not in found:
                    pending.append(other)
    return {p.name: sha(p) for p in sorted(found)}


def child(script, report_name):
    if script == 'verify_book_v2_hidden_editors.py':
        initial.OUT = OUT
        return original_child(script, 'book-v2-hidden-editors')
    target = OUT / script.removesuffix('.py')
    target.mkdir()
    (target / 'hidden-overlay-observations.json').write_bytes((OUT / 'inputs/current-observations.json').read_bytes())
    path = ROOT / script
    tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    changed = 0
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'OUT' for t in node.targets):
            node.value = ast.Call(func=ast.Name(id='Path', ctx=ast.Load()), args=[ast.Constant(str(target))], keywords=[])
            changed += 1
    assert changed == 1
    ast.fix_missing_locations(tree)
    sys.argv = [str(path)]
    code = 0
    try:
        exec(compile(tree, str(path), 'exec'), {'__file__': str(path), '__name__': '__main__', 'Path': Path})
    except SystemExit as error:
        code = error.code or 0
    except Exception:
        code = 1
        (target / 'runner-error.txt').write_text(traceback.format_exc(), encoding='utf-8')
    report = json.loads((target / report_name).read_text(encoding='utf-8')) if (target / report_name).exists() else {}
    rows = report.get('results', [])
    dump(target / 'execution.json', dict(script=script, report=report_name, exit_code=code,
         redirect='Only top-level OUT assignment redirected in compiled AST. Current actual observation input copied to isolated OUT; original assertions unchanged.',
         cases=len(rows), passed=sum(r['passed'] for r in rows), report_sha256=sha(target / report_name) if report else None))
    return code


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--child')
    parser.add_argument('--report')
    args = parser.parse_args()
    if args.child:
        return child(args.child, args.report)
    baseline = json.loads((RAW / 'results.json').read_text(encoding='utf-8'))
    assert baseline['complete'] and baseline['dependencies'] == deps()
    assert baseline['fixture_sha256'] == initial.fixture_files()
    failed = [r for r in baseline['results'] if r['exit_code'] != 0]
    assert len(failed) == 1 and failed[0]['script'] == 'verify_book_v2_hidden_editors.py' and failed[0]['cases'] == 0
    OUT.mkdir(parents=True, exist_ok=True)
    assert not (OUT / 'results.json').exists()
    (OUT / 'inputs').mkdir()
    book = json.loads((RAW / 'inputs/current-book-inventory.json').read_text(encoding='utf-8'))
    book['dependency_files'] = book_dependencies()
    assert all(baseline['dependencies'].get(k) == v for k, v in book['dependency_files'].items())
    book['scope_correction'] = '63 actual book dependencies, a verified subset of the 201 archived product dependencies; observation rows unchanged.'
    dump(OUT / 'inputs/current-book-inventory.json', book)
    observations = json.loads((RAW / 'inputs/current-observations.json').read_text(encoding='utf-8'))
    prior_observations = json.loads((RAW / 'inputs/historical-observations.json').read_text(encoding='utf-8'))
    for index in [118, 122, 129]:
        previous = prior_observations['results'][index]
        matches = [r for r in book['results'] if r['page'] == previous['page'] and r['expected_title'] == previous['overlays'][0]['title']]
        assert len(matches) == 1, index
        observation = matches[0]
        observations['results'][index] = dict(page=observation['page'], group='book', selector=observation['selector'],
            label=observation['trigger'], overlays=observation['overlays'], lifecycle_candidate_index=observation['lifecycle_candidate_index'], historical_observation_index=index)
    observations['files'] = source()
    observations['current_files_scope'] = 'Actual source() dependency subset. Each populated observation comes from current lifecycle or current catalog probes; placeholders remain unavailable.'
    assert all(baseline['dependencies'].get(k) == v for k, v in observations['files'].items())
    dump(OUT / 'inputs/current-observations.json', observations)
    scripts = fixture_files()
    for name in scripts:
        path = OUT / 'fixtures' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((ROOT / name).read_bytes())
    preserved = dict(baseline['preserved_reports'])
    preserved.update({str((ROOT / 'evidence/current' / report).relative_to(ROOT)): sha(ROOT / 'evidence/current' / report) for _, report, _ in ADDITIONAL})
    preserved[str((RAW / 'results.json').relative_to(ROOT))] = sha(RAW / 'results.json')
    report = dict(dependencies=baseline['dependencies'], fixture_sha256=scripts, preserved_reports=preserved,
        baseline_sha256=sha(RAW / 'results.json'), retained_cases=108, fresh_cases=0, complete=False,
        results=[dict(r, retained_from=(RAW / r['script'].removesuffix('.py') / 'results.json').relative_to(ROOT).as_posix()) for r in baseline['results'] if r['exit_code'] == 0], human_accepted_pages=0,
        scope='Eight same-source suites retained; editor suite and save/delete suites actually executed. Current observed controls and declared consumer variants only; not arbitrary conditions or visual acceptance.')
    jobs = [('verify_book_v2_hidden_editors.py', 'results.json', 18)] + ADDITIONAL
    for script, report_name, expected in jobs:
        print('START', script, flush=True)
        process = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--child', script, '--report', report_name])
        target = OUT / script.removesuffix('.py')
        execution = json.loads((target / 'execution.json').read_text(encoding='utf-8'))
        assert process.returncode == execution['exit_code']
        report['results'].append(dict(execution, report=report_name, expected_cases=expected, execution_sha256=sha(target / 'execution.json')))
        report['fresh_cases'] += execution['cases']
        assert deps() == report['dependencies'] and fixture_files() == scripts
        assert all(sha(ROOT / n) == h for n, h in preserved.items())
        dump(OUT / 'results.json', report)
        print('DONE', script, execution['passed'], '/', execution['cases'], flush=True)
    report['complete'] = True
    report['all_passed'] = len(report['results']) == 12 and all(r['exit_code'] == 0 and r['passed'] == r['cases'] == r['expected_cases'] for r in report['results'])
    dump(OUT / 'results.json', report)
    return 0 if report['all_passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
