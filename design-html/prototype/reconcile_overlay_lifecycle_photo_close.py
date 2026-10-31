"""Retain the failed baseline and execute its one actual V2 close button."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from replay_current_overlay_lifecycle import OUT as RAW, ROOT, deps, sha, dump, prepare, fixture_files
from audit_hidden_overlays import declarations, MODULES
from audit_runtime import INIT

OUT = RAW.with_name(RAW.name + '-final')


def main():
    baseline = json.loads((RAW / 'results.json').read_text(encoding='utf-8'))
    assert baseline['complete'] and baseline['dependencies'] == deps()
    assert baseline['fixture_sha256'] == fixture_files()
    failures = [r for r in baseline['results'] if not r['passed']]
    assert len(failures) == 1
    old = failures[0]
    assert (old['candidate_index'], old['method'], old['dirty']) == (98, 'button', False)
    assert 'No declared safe close action' in old['failure']
    candidate = baseline['candidates'][98]
    assert candidate['page'] == 'm08-p16' and candidate['contract'] == 'modal:共同回忆照片'
    observation = next(o for o in baseline['inventory'] if o['candidate_index'] == 98)
    assert any(c['label'] == '返回阅读' and c['tag'] == 'BUTTON' for c in observation['overlays'][0]['controls'])
    OUT.mkdir(parents=True, exist_ok=True)
    assert not (OUT / 'results.json').exists()
    fixtures = {group: declarations(name) for group, name in MODULES.items()}
    row = dict(candidate_index=98, page=candidate['page'], method='button', dirty=False, passed=False,
               actual_button='返回阅读', execution='fresh-literal-button-click')
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        context = browser.new_context(viewport=dict(width=390, height=844), reduced_motion='reduce', locale='zh-CN', timezone_id='Asia/Shanghai')
        context.add_init_script(INIT)
        page = context.new_page()
        page.set_default_timeout(5000)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        prepare(page, candidate, fixtures)
        trigger = page.locator(candidate['selector'])
        trigger.click()
        dialog = page.locator('dialog[open]')
        expect(dialog.locator('h2')).to_have_text('共同回忆照片')
        before_url = page.url
        before_store = page.evaluate('JSON.stringify({...localStorage})')
        dialog.get_by_role('button', name='返回阅读', exact=True).click()
        expect(page.locator('dialog[open]')).to_have_count(0)
        assert page.url == before_url and page.evaluate('JSON.stringify({...localStorage})') == before_store
        expect(trigger).to_be_focused()
        assert not errors
        page.screenshot(path=str(OUT / 'photo-close.png'), full_page=True)
        row.update(passed=True, errors=errors, storage_preserved=True, underlying_page_preserved=True, focus_returned=True, browser=browser.version)
        context.close()
        browser.close()
    assert deps() == baseline['dependencies'] and fixture_files() == baseline['fixture_sha256']
    dump(OUT / 'fresh-photo-close.json', row)
    final = dict(baseline)
    final['results'] = [row if r == old else r for r in baseline['results']]
    final.update(all_passed=True, retained_cases=570, fresh_cases=1,
                 baseline_report_sha256=sha(RAW / 'results.json'), fresh_report_sha256=sha(OUT / 'fresh-photo-close.json'),
                 reconciliation_producer_sha256=sha(Path(__file__)),
                 reconciliation='Original 571-case baseline retained unchanged. Only missing test-assistant safe-close name corrected by literal current button; no product or original fixture changes. Source/fixture archives and input catalog remain in sibling overlay-lifecycle-20261031 directory.')
    dump(OUT / 'results.json', final)
    print('PASS 1 fresh literal photo close; 570 exact baseline successes retained; final 571/571')


if __name__ == '__main__':
    main()
