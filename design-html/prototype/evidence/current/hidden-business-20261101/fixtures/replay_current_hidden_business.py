"""Fresh business outcomes using current observations and isolated legacy suites.

Legacy ordinal IDs remain fixture IDs only. Their selectors/titles come from
actual current observations; historical reports and producer files stay intact.
"""
import argparse
import ast
import json
import subprocess
import sys
import traceback
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from audit_hidden_overlays import declarations, MODULES, SNAPSHOT
from audit_runtime import INIT
from verify_overlay_exit_paths import close
from replay_current_initial_controls import ROOT, DEMO, deps, sha, dump

OUT = ROOT / 'evidence/current/hidden-business-20261101'
JOBS = [
    ('verify_hidden_choice_outcomes.py', 'hidden-choice-outcomes', 17),
    ('verify_hidden_auxiliary_outcomes.py', 'hidden-auxiliary-outcomes', 9),
    ('verify_hidden_workshop_outcomes.py', 'hidden-workshop-outcomes', 14),
    ('verify_hidden_settings_pet_outcomes.py', 'hidden-settings-pet-outcomes', 24),
    ('verify_book_v2_hidden_reading.py', 'book-v2-hidden-reading', 22),
    ('verify_book_v2_hidden_structure.py', 'book-v2-hidden-structure', 13),
    ('verify_book_v2_hidden_editors.py', 'book-v2-hidden-editors', 18),
    ('verify_book_v2_hidden_forms.py', 'book-v2-hidden-forms', 6),
    ('verify_book_v2_hidden_edges.py', 'book-v2-hidden-edges', 3),
]
LIFECYCLE = ROOT / 'evidence/current/overlay-lifecycle-20261031-final/results.json'
OBSERVED = ROOT / 'evidence/current/hidden-overlay-observations.json'
CATALOG = ROOT / 'evidence/current/initial-controls-20261031-accessible/contracts.json'
EXTRA = {74: ('m07-p12', 'bow'), 75: ('m07-p12', 'star-bow'),
         76: ('m07-p12', 'peach-hat'), 77: ('m07-p12', 'crown'),
         79: ('m07-p15', 'plaid-rug'), 80: ('m07-p15', 'moon-rug')}


def fixture_files():
    pending = [Path(__file__).resolve()] + [ROOT / n for n, _, _ in JOBS] + [ROOT / n for n in MODULES.values()]
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


def inputs(files):
    lifecycle = json.loads(LIFECYCLE.read_text(encoding='utf-8'))
    assert lifecycle['dependencies'] == files and lifecycle['all_passed']
    catalog = json.loads(CATALOG.read_text(encoding='utf-8'))
    old = json.loads(OBSERVED.read_text(encoding='utf-8'))
    for name, path in [('lifecycle.json', LIFECYCLE), ('historical-observations.json', OBSERVED), ('initial-contracts.json', CATALOG)]:
        (OUT / 'inputs' / name).write_bytes(path.read_bytes())
    fixtures = {g: declarations(n) for g, n in MODULES.items()}
    extra = {}
    exits = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for index, (page_id, item) in EXTRA.items():
            candidates = [c for p in catalog['pages'] if p['id'] == page_id for c in p['initial_controls'] if c['contract'] == 'catalog:' + item]
            assert len(candidates) == 1
            candidate = candidates[0]
            methods = ['escape', 'button', 'backdrop', 'back']
            for method in methods:
                context = browser.new_context(viewport=dict(width=390, height=844), reduced_motion='reduce', locale='zh-CN', timezone_id='Asia/Shanghai')
                context.add_init_script(INIT)
                page = context.new_page()
                page.set_default_timeout(5000)
                errors = []
                page.on('pageerror', lambda error: errors.append(str(error)))
                fixtures['pet']['seed'](page, page_id)
                trigger = page.locator(candidate['selector'])
                trigger.click()
                dialog = page.locator('dialog[open]')
                expect(dialog).to_have_count(1)
                before_url = page.url
                before = page.evaluate('JSON.stringify({...localStorage})')
                if method == 'escape':
                    overlays = page.evaluate(SNAPSHOT)
                    assert len(overlays) == 1
                    extra[index] = dict(candidate, group='pet', overlays=overlays,
                                        historical_observation_index=index,
                                        origin='fresh actual catalog action; not classified sheet/modal by initial contract')
                (page.keyboard.press('Escape') if method == 'escape' else close(page, method))
                expect(page.locator('dialog[open]')).to_have_count(0)
                assert page.url == before_url and page.evaluate('JSON.stringify({...localStorage})') == before
                expect(trigger).to_be_focused()
                assert not errors
                exits.append(dict(historical_observation_index=index, page=page_id, item=item, method=method, passed=True, storage_preserved=True, underlying_page_preserved=True, focus_returned=True, errors=errors))
                context.close()
            print('CATALOG', index, item, '4/4', flush=True)
        browser.close()
    dump(OUT / 'catalog-overlays.json', dict(dependencies=files, observations=list(extra.values()), results=exits))
    rows = [dict(historical_observation_index=i, unavailable_for_current_replay=True) for i in range(len(old['results']))]
    mappings = []
    for index, observation in enumerate(old['results']):
        if not observation.get('overlays') or observation['page'].startswith('m08'):
            continue
        if index in extra:
            current = extra[index]
            kind = 'fresh-catalog-dialog'
        else:
            matches = [o for o in lifecycle['inventory'] if o['page'] == observation['page'] and o['selector'] == observation['selector']]
            assert len(matches) == 1, (index, observation['page'], observation['label'])
            found = matches[0]
            current = dict(page=found['page'], selector=found['selector'], label=found['label'],
                           group=observation['group'], overlays=found['overlays'], lifecycle_candidate_index=found['candidate_index'])
            kind = 'exact-current-page-and-selector'
        rows[index] = dict(current, historical_observation_index=index)
        mappings.append(dict(historical_observation_index=index, page=current['page'], selector=current['selector'], kind=kind))
    dump(OUT / 'inputs/current-observations.json', dict(dependencies=files, lifecycle_sha256=sha(LIFECYCLE),
          legacy_indices_only=True, mapping=mappings, results=rows,
          scope='Only explicit mapped nonbook observations are available. Placeholders deliberately cannot drive browser actions. No historical observation is rebound to current source.'))
    book = [dict(page=o['page'], selector=o['selector'], trigger=o['label'], expected_title=o['overlays'][0]['title'], overlays=o['overlays'], lifecycle_candidate_index=o['candidate_index']) for o in lifecycle['inventory'] if o['page'].startswith('m08')]
    assert len(book) == 31
    dump(OUT / 'inputs/current-book-inventory.json', dict(dependency_files=files, lifecycle_sha256=sha(LIFECYCLE), results=book))


def child(script, folder):
    path = ROOT / script
    target = OUT / script.removesuffix('.py')
    target.mkdir()
    replacements = {'evidence/current/' + folder: target.relative_to(ROOT).as_posix(),
                    'evidence/current/hidden-overlay-observations.json': (OUT / 'inputs/current-observations.json').relative_to(ROOT).as_posix(),
                    'evidence/current/book-v2-hidden/inventory.json': (OUT / 'inputs/current-book-inventory.json').relative_to(ROOT).as_posix()}
    changed = []
    class Redirect(ast.NodeTransformer):
        def visit_Constant(self, node):
            if isinstance(node.value, str) and node.value in replacements:
                changed.append(dict(before=node.value, after=replacements[node.value], line=node.lineno))
                return ast.copy_location(ast.Constant(replacements[node.value]), node)
            return node
    tree = Redirect().visit(ast.parse(path.read_text(encoding='utf-8'), filename=str(path)))
    ast.fix_missing_locations(tree)
    assert any(c['before'] == 'evidence/current/' + folder for c in changed)
    sys.argv = [str(path)]
    code = 0
    try:
        exec(compile(tree, str(path), 'exec'), {'__file__': str(path), '__name__': '__main__'})
    except SystemExit as error:
        code = error.code or 0
    except Exception:
        code = 1
        (target / 'runner-error.txt').write_text(traceback.format_exc(), encoding='utf-8')
    report = json.loads((target / 'results.json').read_text(encoding='utf-8')) if (target / 'results.json').exists() else {}
    rows = report.get('results', [])
    execution = dict(script=script, exit_code=code, path_literal_redirects=changed, cases=len(rows),
                     passed=sum(r['passed'] for r in rows), report_sha256=sha(target / 'results.json') if report else None,
                     scope='Only output directory and two observation input path literals redirected in compiled AST. Original source bytes archived; all actual business assertions unchanged.')
    dump(target / 'execution.json', execution)
    return code


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--child')
    parser.add_argument('--folder')
    args = parser.parse_args()
    if args.child:
        return child(args.child, args.folder)
    OUT.mkdir(parents=True, exist_ok=True)
    assert not (OUT / 'results.json').exists() and not (OUT / 'catalog-overlays.json').exists()
    (OUT / 'inputs').mkdir()
    files, scripts = deps(), fixture_files()
    for sub, origin, mapping in [('source', DEMO, files), ('fixtures', ROOT, scripts)]:
        for name in mapping:
            target = OUT / sub / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((origin / name).read_bytes())
    preserved = {str(p.relative_to(ROOT)): sha(p) for p in [OBSERVED, LIFECYCLE, CATALOG] + [ROOT / 'evidence/current' / folder / 'results.json' for _, folder, _ in JOBS]}
    inputs(files)
    report = dict(dependencies=files, fixture_sha256=scripts, preserved_reports=preserved, results=[], complete=False,
                  scope='126 named business outcomes in nine existing suites, plus six newly observed catalog dialogs. Not every arbitrary conditional combination or visual acceptance.', human_accepted_pages=0)
    for script, folder, count in JOBS:
        print('START', script, flush=True)
        result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--child', script, '--folder', folder])
        target = OUT / script.removesuffix('.py')
        execution = json.loads((target / 'execution.json').read_text(encoding='utf-8'))
        assert result.returncode == execution['exit_code']
        report['results'].append(dict(execution, expected_cases=count, execution_sha256=sha(target / 'execution.json')))
        assert files == deps() and scripts == fixture_files()
        assert all(sha(ROOT / n) == h for n, h in preserved.items())
        dump(OUT / 'results.json', report)
        print('DONE', script, execution['passed'], '/', execution['cases'], flush=True)
    report['complete'] = True
    report['all_passed'] = all(r['exit_code'] == 0 and r['cases'] == r['passed'] == r['expected_cases'] for r in report['results'])
    dump(OUT / 'results.json', report)
    return 0 if report['all_passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
