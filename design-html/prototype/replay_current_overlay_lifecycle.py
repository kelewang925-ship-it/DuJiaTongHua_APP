"""Exercise current declared manual overlay entries and actual clean/dirty exits.

The input catalog supplies candidates, never passing results. Every result below
is executed afresh. Native dialogs opened automatically and nested business
choices are outside this lifecycle batch.
"""
import ast
import json
import traceback
from pathlib import Path
from urllib.request import urlopen

from playwright.sync_api import sync_playwright, expect
from audit_hidden_overlays import declarations, seed_onboarding, MODULES, SNAPSHOT
from audit_runtime import INIT
from verify_overlay_exit_paths import close, change_field
from replay_current_initial_controls import ROOT, DEMO, deps, sha, dump
from verify_pet_controls import BASE

OUT = ROOT / 'evidence/current/overlay-lifecycle-20261031'
CATALOG = ROOT / 'evidence/current/initial-controls-20261031-accessible/contracts.json'


def fixture_files():
    pending = [Path(__file__).resolve()] + [ROOT / n for n in MODULES.values()]
    found = set()
    while pending:
        path = pending.pop()
        if path in found:
            continue
        found.add(path)
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            names = ([node.module] if isinstance(node, ast.ImportFrom) and node.module
                     else [a.name for a in node.names] if isinstance(node, ast.Import) else [])
            for name in names:
                other = ROOT / (name.split('.')[0] + '.py')
                if other.is_file() and other not in found:
                    pending.append(other)
    return {p.name: sha(p) for p in sorted(found)}


def prepare(page, candidate, fixtures):
    if candidate['group'] == 'onboarding':
        seed_onboarding(page, candidate['page'])
    else:
        fixtures[candidate['group']]['seed'](page, candidate['page'])
    page.evaluate('document.fonts.ready')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    assert not (OUT / 'results.json').exists(), 'Refuse to overwrite an execution'
    files, scripts = deps(), fixture_files()
    for name, digest in files.items():
        served = name.replace('custom/', 'pages/', 1) if name.startswith('custom/') else name
        with urlopen(BASE + served, timeout=10) as response:
            assert __import__('hashlib').sha256(response.read()).hexdigest() == digest, name
    for sub, mapping, origin in [('source', files, DEMO), ('fixtures', scripts, ROOT)]:
        for name in mapping:
            target = OUT / sub / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((origin / name).read_bytes())
    (OUT / 'input-contracts.json').write_bytes(CATALOG.read_bytes())
    catalog = json.loads(CATALOG.read_text(encoding='utf-8'))
    candidates = [dict(c, group=p['fixture_group']) for p in catalog['pages']
                  for c in p['initial_controls'] if c['contract'].startswith(('sheet:', 'modal:'))]
    assert len(candidates) == 104
    assert len({(c['page'], c['selector']) for c in candidates}) == 104
    fixtures = {group: declarations(name) for group, name in MODULES.items()}
    report = dict(dependencies=files, fixture_sha256=scripts, catalog_sha256=sha(CATALOG),
                  candidates=candidates, inventory=[], results=[], complete=False,
                  scope='104 manual entries from the declared initial catalog. Fresh Escape, safe button, backdrop, browser Back and sheet-handle drag; dirty submit forms also exercise continue-editing then discard. No nested business outcome, automatic overlay or native-device claim.',
                  human_accepted_pages=0)

    def save():
        assert deps() == files and fixture_files() == scripts
        assert sha(CATALOG) == report['catalog_sha256']
        dump(OUT / 'results.json', report)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        report['browser'] = browser.version
        for index, candidate in enumerate(candidates):
            # Discovery and the Escape result share one real interaction. All
            # other closure methods start from separate seeded contexts.
            jobs = [('escape', False)]
            while jobs:
                method, dirty = jobs.pop(0)
                context = browser.new_context(viewport=dict(width=390, height=844), reduced_motion='reduce', locale='zh-CN', timezone_id='Asia/Shanghai', accept_downloads=True)
                context.add_init_script(INIT)
                page = context.new_page()
                page.set_default_timeout(5000)
                page.set_default_navigation_timeout(15000)
                errors = []
                page.on('pageerror', lambda error: errors.append(str(error)))
                row = dict(candidate_index=index, page=candidate['page'], method=method, dirty=dirty, passed=False)
                try:
                    prepare(page, candidate, fixtures)
                    trigger = page.locator(candidate['selector'])
                    expect(trigger).to_be_visible()
                    expect(trigger).to_be_enabled()
                    trigger.click()
                    dialog = page.locator('dialog[open]')
                    expect(dialog).to_have_count(1)
                    expect(dialog.locator('h2')).to_have_text(candidate['contract'].split(':', 1)[1])
                    before_url = page.url
                    before_store = page.evaluate('JSON.stringify({...localStorage})')
                    if method == 'escape' and not dirty:
                        overlays = page.evaluate(SNAPSHOT)
                        assert len(overlays) == 1
                        sheet = dialog.locator('.prototype-sheet-handle').count() == 1
                        editable_submit = dialog.locator('form input:not([type=hidden]):not([type=file]):not([readonly]):not([disabled]),form textarea:not([readonly]):not([disabled]),form select:not([disabled])').count() > 0 and dialog.locator('form [type=submit]').count() > 0
                        methods = ['escape', 'button', 'backdrop', 'back'] + (['drag'] if sheet else [])
                        jobs.extend((m, False) for m in methods if m != 'escape')
                        if editable_submit:
                            jobs.extend((m, True) for m in methods)
                        report['inventory'].append(dict(candidate_index=index, page=candidate['page'], selector=candidate['selector'], label=candidate['label'], sheet=sheet, editable_submit=editable_submit, methods=methods, overlays=overlays))
                    if dirty:
                        form = dialog.locator('form')
                        expect(form).to_have_count(1)
                        snapshot = change_field(form)
                        (page.keyboard.press('Escape') if method == 'escape' else close(page, method))
                        warning = dialog.locator('.prototype-sheet-discard')
                        expect(warning).to_be_visible()
                        warning.get_by_role('button', name='继续编辑', exact=True).click()
                        expect(warning).to_have_count(0)
                        expect(form).to_be_visible()
                        assert snapshot == form.evaluate('f=>JSON.stringify([...f.querySelectorAll("input,textarea,select")].map(e=>[e.value,e.checked]))')
                        assert page.url == before_url and page.evaluate('JSON.stringify({...localStorage})') == before_store
                        (page.keyboard.press('Escape') if method == 'escape' else close(page, method))
                        expect(warning).to_be_visible()
                        warning.get_by_role('button', name='放弃修改', exact=True).click()
                        row['continue_preserved_fields'] = True
                    else:
                        (page.keyboard.press('Escape') if method == 'escape' else close(page, method))
                    expect(page.locator('dialog[open]')).to_have_count(0)
                    assert page.url == before_url, 'Closure navigated away from underlying page'
                    assert before_store == page.evaluate('JSON.stringify({...localStorage})'), 'Closure changed stored content'
                    expect(trigger).to_be_focused()
                    assert not errors, errors
                    row.update(passed=True, storage_preserved=True, underlying_page_preserved=True, focus_returned=True)
                except Exception:
                    row['failure'] = traceback.format_exc()
                    page.screenshot(path=str(OUT / f'failure-{index}-{method}-{dirty}.png'), full_page=True)
                row['errors'] = errors
                report['results'].append(row)
                context.close()
                save()
            cases = [r for r in report['results'] if r['candidate_index'] == index]
            print(f"ENTRY {index+1}/104 {candidate['page']} {sum(r['passed'] for r in cases)}/{len(cases)}", flush=True)
        browser.close()
    report['complete'] = True
    report['all_passed'] = len(report['inventory']) == 104 and all(r['passed'] for r in report['results'])
    save()
    print(json.dumps(dict(entries=len(report['inventory']), cases=len(report['results']), passed=sum(r['passed'] for r in report['results']), dirty=sum(r['dirty'] for r in report['results']))))
    return 0 if report['all_passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
