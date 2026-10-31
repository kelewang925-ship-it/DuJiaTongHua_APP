"""Re-execute book-specific pending boundaries against the current V2 controls."""
import argparse
import ast
import json
import subprocess
import sys
import traceback
from pathlib import Path
from replay_current_initial_controls import ROOT, DEMO, deps, sha, dump

OUT = ROOT / 'evidence/current/book-pending-20261101'
JOBS = [
    ('verify_pending_page_guard.py', ['--cases', 'book-theme'], 4, 'pending-page-guard'),
    ('verify_submission_changes.py', ['--only', 'edit/book-theme'], 1, 'submission-changes'),
    ('verify_pending_form_cancel.py', ['--indices', '118,122,129'], 18, 'pending-form-cancel'),
    ('verify_pending_image_reads.py', ['--cases', 'book-supplement'], 2, 'pending-image-read'),
    ('verify_image_pending_exit.py', ['--cases', 'book-supplement'], 6, 'image-pending-exit'),
    ('verify_file_chooser_pending.py', ['--cases', 'book-supplement'], 3, 'file-chooser-pending'),
]


def fixtures():
    pending = [Path(__file__).resolve()] + [ROOT / j[0] for j in JOBS]
    found = set()
    while pending:
        path = pending.pop()
        if path in found:
            continue
        found.add(path)
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            names = ([node.module.split('.')[0] + '.py'] if isinstance(node, ast.ImportFrom) and node.module else
                     [n.name.split('.')[0] + '.py' for n in node.names] if isinstance(node, ast.Import) else
                     [node.value] if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value.endswith('.py') else [])
            for name in names:
                candidate = ROOT / name
                if candidate.is_file() and candidate not in found:
                    pending.append(candidate)
    return {p.name: sha(p) for p in sorted(found)}


def child(script):
    job = next(j for j in JOBS if j[0] == script)
    folder = OUT / Path(script).stem
    folder.mkdir()
    path = ROOT / script

    class Redirect(ast.NodeTransformer):
        outputs = 0
        inputs = 0
        selectors = 0

        def visit_Assign(self, node):
            if any(isinstance(t, ast.Name) and t.id == 'out' for t in node.targets) and 'evidence/' in ast.unparse(node.value):
                node.value = ast.Call(func=ast.Name(id='Path', ctx=ast.Load()), args=[ast.Constant(str(folder))], keywords=[])
                self.outputs += 1
            return self.generic_visit(node)

        def visit_BinOp(self, node):
            if isinstance(node.op, ast.Div) and isinstance(node.left, ast.Name) and node.left.id == 'ROOT' and isinstance(node.right, ast.Constant) and node.right.value == 'evidence/current/hidden-overlay-observations.json':
                self.inputs += 1
                return ast.Call(func=ast.Name(id='Path', ctx=ast.Load()), args=[ast.Constant(str(OUT / 'current-observations.json'))], keywords=[])
            return self.generic_visit(node)

        def visit_Constant(self, node):
            if script == 'verify_file_chooser_pending.py' and node.value == 'label.photo':
                self.selectors += 1
                return ast.copy_location(ast.Constant('label.v2-upload'), node)
            return node

    redirect = Redirect()
    tree = redirect.visit(ast.parse(path.read_text(encoding='utf-8')))
    ast.fix_missing_locations(tree)
    assert redirect.outputs == 1
    assert redirect.inputs == (1 if script == 'verify_pending_form_cancel.py' else 0)
    assert redirect.selectors == (1 if script == 'verify_file_chooser_pending.py' else 0)
    sys.argv = [str(path)] + job[1]
    code = 0
    try:
        exec(compile(tree, str(path), 'exec'), {'__file__': str(path), '__name__': '__main__', 'Path': Path})
    except SystemExit as error:
        code = error.code or 0
    except Exception:
        code = 1
        (folder / 'runner-error.txt').write_text(traceback.format_exc(), encoding='utf-8')
    report = folder / 'results.json'
    rows = json.loads(report.read_text(encoding='utf-8'))['results'] if report.exists() else []
    dump(folder / 'execution.json', dict(script=script, arguments=job[1], exit_code=code, expected=job[2],
         cases=len(rows), passed=sum(r['passed'] for r in rows), report_sha256=sha(report) if report.exists() else None,
         redirect=dict(output=redirect.outputs, observation_input=redirect.inputs, v2_upload_selector=redirect.selectors)))
    return code


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--child')
    args = parser.parse_args()
    if args.child:
        return child(args.child)
    files, scripts = deps(), fixtures()
    old_observations = ROOT / 'evidence/current/hidden-business-20261101-final/inputs/current-observations.json'
    data = json.loads(old_observations.read_text(encoding='utf-8'))
    for index, expected_page, title in [(118, 'm08-p11', '一句话'), (122, 'm08-p13', '章节'), (129, 'm08-p21', '书名')]:
        observation = data['results'][index]
        assert observation['page'] == expected_page and observation['overlays'][0]['title'] == title
        assert observation['selector'] and observation['lifecycle_candidate_index'] is not None
    assert not OUT.exists() or not any(OUT.iterdir()), 'Do not overwrite existing executions'
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'current-observations.json').write_bytes(old_observations.read_bytes())
    preserved = {str((ROOT / 'evidence/current' / j[3] / 'results.json').relative_to(ROOT)): sha(ROOT / 'evidence/current' / j[3] / 'results.json') for j in JOBS}
    preserved[old_observations.relative_to(ROOT).as_posix()] = sha(old_observations)
    for sub, mapping, source in [('source', files, DEMO), ('fixtures', scripts, ROOT)]:
        for name in mapping:
            path = OUT / sub / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((source / name).read_bytes())
    rows = []
    for script, _, _, _ in JOBS:
        print('START', script, flush=True)
        run = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--child', script], capture_output=True, text=True, encoding='utf-8')
        folder = OUT / Path(script).stem
        (folder / 'execution.log').write_text(run.stdout + run.stderr, encoding='utf-8')
        row = json.loads((folder / 'execution.json').read_text(encoding='utf-8'))
        assert row['exit_code'] == run.returncode
        rows.append(row)
        assert deps() == files and fixtures() == scripts
        assert all(sha(ROOT / n) == h for n, h in preserved.items())
        complete = len(rows) == len(JOBS)
        passed = all(r['exit_code'] == 0 and r['cases'] == r['passed'] == r['expected'] for r in rows)
        dump(OUT / 'results.json', dict(dependencies=files, fixture_sha256=scripts, preserved_reports=preserved,
             observation_sha256=sha(OUT / 'current-observations.json'), results=rows, complete=complete,
             all_passed=complete and passed, expected_cases=34,
             scope='Current V2 book theme4, changed theme input1, three pending forms18, native photo read2, pending-image exit6 and chooser3. Original assertions unchanged; only output/input paths and literal V2 upload affordance updated. Other historic270 cases are not relabelled as current.'))
        print('DONE', script, row['passed'], '/', row['cases'], 'exit', row['exit_code'], flush=True)
        if not passed:
            print(run.stdout[-1200:] + run.stderr[-1200:], flush=True)
            return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
