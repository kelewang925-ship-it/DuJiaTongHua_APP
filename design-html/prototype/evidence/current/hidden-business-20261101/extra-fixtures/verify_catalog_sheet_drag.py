"""Complete drag closure for the six newly observed catalog sheets only."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from audit_hidden_overlays import declarations
from audit_runtime import INIT
from verify_overlay_exit_paths import close
from replay_current_initial_controls import ROOT, deps, sha, dump
from replay_current_hidden_business import OUT


def main():
    data = json.loads((OUT / 'catalog-overlays.json').read_text(encoding='utf-8'))
    assert data['dependencies'] == deps()
    assert not (OUT / 'catalog-drag-results.json').exists()
    path = OUT / 'extra-fixtures' / Path(__file__).name
    path.parent.mkdir(exist_ok=True)
    path.write_bytes(Path(__file__).read_bytes())
    rows = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for observation in data['observations']:
            context = browser.new_context(viewport=dict(width=390, height=844), reduced_motion='reduce')
            context.add_init_script(INIT)
            page = context.new_page()
            page.set_default_timeout(5000)
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            declarations('verify_pet_controls.py')['seed'](page, observation['page'])
            trigger = page.locator(observation['selector'])
            trigger.click()
            expect(page.locator('dialog[open] h2')).to_have_text(observation['overlays'][0]['title'])
            before = page.evaluate('JSON.stringify({...localStorage})')
            before_url = page.url
            close(page, 'drag')
            expect(page.locator('dialog[open]')).to_have_count(0)
            assert page.url == before_url and page.evaluate('JSON.stringify({...localStorage})') == before
            expect(trigger).to_be_focused()
            assert not errors
            rows.append(dict(historical_observation_index=observation['historical_observation_index'], method='drag', passed=True,
                             storage_preserved=True, underlying_page_preserved=True, focus_returned=True, errors=errors))
            context.close()
        browser.close()
    assert deps() == data['dependencies']
    dump(OUT / 'catalog-drag-results.json', dict(dependencies=deps(), producer_sha256=sha(Path(__file__)),
         fixture_sha256=sha(ROOT / 'verify_pet_controls.py'), input_sha256=sha(OUT / 'catalog-overlays.json'), results=rows))
    print('PASS 6/6 newly observed catalog sheet drag closes')


if __name__ == '__main__':
    main()
