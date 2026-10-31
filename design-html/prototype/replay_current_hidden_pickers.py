"""Fresh picker consumer suite and explicit birthday-clear persistence/retry."""
import ast
import json
import sys
import traceback
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from audit_hidden_overlays import declarations
from audit_runtime import INIT
from replay_current_initial_controls import ROOT, deps, sha, dump
from replay_current_hidden_business import OUT as ARCHIVE, fixture_files as shared_fixtures

OUT = ROOT / 'evidence/current/hidden-pickers-20261101'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    assert not (OUT / 'execution.json').exists()
    files = deps()
    scripts = dict(shared_fixtures())
    for name in [Path(__file__).name, 'verify_shared_picker_fields.py']:
        scripts[name] = sha(ROOT / name)
    for name, digest in scripts.items():
        path = OUT / 'fixtures' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((ROOT / name).read_bytes())
        assert sha(path) == digest
    archived = json.loads((ARCHIVE / 'results.json').read_text(encoding='utf-8'))
    assert files == archived['dependencies']
    for name, digest in files.items():
        assert sha(ARCHIVE / 'source' / name) == digest
    script = ROOT / 'verify_shared_picker_fields.py'
    output = (OUT / 'picker-results.json').relative_to(ROOT).as_posix()
    changed = []
    class Redirect(ast.NodeTransformer):
        def visit_Constant(self, node):
            if node.value == 'evidence/current/shared-picker-fields-results.json':
                changed.append(node.lineno)
                return ast.copy_location(ast.Constant(output), node)
            return node
    tree = Redirect().visit(ast.parse(script.read_text(encoding='utf-8'), filename=str(script)))
    assert len(changed) == 1
    ast.fix_missing_locations(tree)
    sys.argv = [str(script)]
    code = 0
    try:
        exec(compile(tree, str(script), 'exec'), {'__file__': str(script), '__name__': '__main__'})
    except SystemExit as error:
        code = error.code or 0
    rows = json.loads((OUT / 'picker-results.json').read_text(encoding='utf-8'))['results']
    row = dict(case='birthday-clear-save-failure-retry-reload', page='m06-p02', passed=False)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        context = browser.new_context(viewport=dict(width=390, height=844), reduced_motion='reduce')
        context.add_init_script(INIT)
        page = context.new_page()
        page.set_default_timeout(6000)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        try:
            declarations('verify_settings_controls.py')['seed'](page, 'm06-p02')
            page.evaluate("localStorage.setItem('dujia-profile',JSON.stringify({...PrototypePreferences.profile(),birthday:'1998-06-21'}))")
            page.reload()
            expect(page.locator('#birthday')).to_have_value('1998-06-21')
            before = page.evaluate('({...localStorage})')
            page.locator('#birthday').click()
            dialog = page.locator('dialog[open]')
            expect(dialog.locator('h2')).to_have_text('你的生日')
            dialog.get_by_role('button', name='不填写生日', exact=True).click()
            expect(dialog).to_have_count(0)
            expect(page.locator('#birthday')).to_have_value('')
            assert page.evaluate('({...localStorage})') == before
            page.evaluate("sessionStorage.setItem('dujia-prototype-fail-next','settings-profile')")
            page.locator('#save').click()
            expect(page.locator('.prototype-toast')).to_contain_text('个人资料未保存')
            expect(page.locator('#save')).to_be_enabled()
            expect(page.locator('#birthday')).to_have_value('')
            assert page.evaluate('({...localStorage})') == before
            page.locator('#save').click()
            page.wait_for_url('**/m06-p01.html*')
            after = page.evaluate('({...localStorage})')
            saved = json.loads(after['dujia-profile'])
            original = json.loads(before['dujia-profile'])
            assert saved['birthday'] == ''
            assert all(saved[k] == original[k] for k in ['nickname', 'saying', 'color', 'avatar'])
            assert {k: v for k, v in before.items() if k != 'dujia-profile'} == {k: v for k, v in after.items() if k != 'dujia-profile'}
            page.goto('http://127.0.0.1:8765/pages/m06-p02.html')
            expect(page.locator('#birthday')).to_have_value('')
            assert not errors
            row.update(passed=True, clear_is_candidate=True, failed_save_preserved=True, retry_persisted=True, reopened_empty=True, unrelated_data_preserved=True)
        except Exception:
            row['failure'] = traceback.format_exc()
            page.screenshot(path=str(OUT / 'birthday-clear-failure.png'), full_page=True)
        row['errors'] = errors
        context.close()
        browser.close()
    dump(OUT / 'birthday-clear.json', row)
    assert deps() == files
    assert all(sha(ROOT / name) == digest for name, digest in scripts.items())
    report = dict(dependencies=files, fixture_sha256=scripts, source_archive=ARCHIVE.relative_to(ROOT).as_posix() + '/source',
        picker_report_sha256=sha(OUT / 'picker-results.json'), birthday_report_sha256=sha(OUT / 'birthday-clear.json'),
        output_literal_line=changed[0], suite_exit_code=code, picker_cases=len(rows), picker_passed=sum(r['passed'] for r in rows),
        extra_case_passed=row['passed'], all_passed=code == 0 and len(rows) == 50 and all(r['passed'] for r in rows) and row['passed'],
        scope='Nine actual picker/filter/tag entries and local two-factor function at five widths, plus one birthday-clear parent-save retry. No original report overwrite or product change.', human_accepted_pages=0)
    dump(OUT / 'execution.json', report)
    print(json.dumps(dict(picker_cases=len(rows), passed=sum(r['passed'] for r in rows), birthday_clear=row['passed'])))
    return 0 if report['all_passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
