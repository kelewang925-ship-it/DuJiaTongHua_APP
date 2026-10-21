"""Photo style and film mood must paint the same selection they persist."""
import argparse
import hashlib
import json
import traceback
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from audit_initial_quality import canonical
from verify_pet_controls import ROOT, DEMO, BASE, source


def selection(p, group, index):
    buttons = p.locator(group + ' button')
    assert p.locator(group).evaluate('e=>getComputedStyle(e).backgroundColor') not in ['transparent', 'rgba(0, 0, 0, 0)'], 'Baked first selection must be covered by opaque paper'
    for i in range(buttons.count()):
        button = buttons.nth(i)
        expect(button).to_have_attribute('aria-pressed', str(i == index).lower())
        marker = button.locator('.selection-check')
        assert marker.count() == 1, 'Each choice needs a native selection marker'
        expect(marker).to_have_attribute('aria-hidden', 'true')
        if i == index:
            expect(marker).to_be_visible()
        else:
            expect(marker).not_to_be_visible()
        assert button.evaluate("e=>getComputedStyle(e,'::after').content") in ['none', 'normal'], 'Do not retain the old pseudo marker alongside the native marker'


def stored(p, work_id):
    return p.evaluate("id=>JSON.parse(localStorage.getItem('dujia-prototype-works')).find(v=>v.id===id)", work_id)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    out = ROOT / ('evidence/baseline/workshop-selection-paint' if args.baseline else 'evidence/current/workshop-selection-paint')
    out.mkdir(parents=True, exist_ok=True)
    files = source()
    styles = {p.relative_to(DEMO).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEMO / 'assets').glob('*.css')}
    rows = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for page, group, field, labels in [
            ('m05-p04', '.styles', 'style', ['水彩', '素描', '清新插画', '油画']),
            ('m05-p05', '.moods', 'mood', ['温柔手帐', '治愈暖光', '清新自然'])
        ]:
            for width in [320, 375, 390, 414, 430]:
                context = browser.new_context(viewport=dict(width=width, height=844), reduced_motion='reduce')
                p = context.new_page()
                p.set_default_timeout(6000)
                errors = []
                p.on('pageerror', lambda e: errors.append(str(e)))
                try:
                    canonical(p, page)
                    work_id = p.evaluate("new URLSearchParams(location.search).get('id')")
                    input_ = p.locator('#story' if field == 'style' else '#narration')
                    story = input_.input_value()
                    buttons = p.locator(group + ' button')
                    buttons.last.click()
                    p.screenshot(path=str(out / f'{page}-last-{width}.png'), full_page=True)
                    selection(p, group, len(labels) - 1)
                    p.get_by_role('button', name='暂存创作草稿', exact=True).click()
                    p.wait_for_url('**/m05-p09.html')
                    assert stored(p, work_id)[field] == labels[-1]
                    p.goto(BASE + 'pages/' + page + '.html?id=' + work_id)
                    selection(p, group, len(labels) - 1)
                    for index in range(len(labels)):
                        button = p.locator(group + ' button').nth(index)
                        button.focus()
                        p.keyboard.press('Space')
                        selection(p, group, index)
                        assert button.evaluate("e=>e.matches(':focus-visible') && parseFloat(getComputedStyle(e).outlineWidth)>=2")
                    p.locator(group + ' button').first.click()
                    selection(p, group, 0)
                    p.evaluate("sessionStorage.setItem('dujia-prototype-fail-next','work-save')")
                    p.get_by_role('button', name='暂存创作草稿', exact=True).click()
                    p.wait_for_function("sessionStorage.getItem('dujia-prototype-fail-next')!=='work-save'")
                    expect(p.locator('.prototype-toast')).to_contain_text('重试')
                    assert stored(p, work_id)[field] == labels[-1]
                    selection(p, group, 0)
                    assert input_.input_value() == story
                    p.get_by_role('button', name='暂存创作草稿', exact=True).click()
                    p.wait_for_url('**/m05-p09.html')
                    assert stored(p, work_id)[field] == labels[0]
                    p.goto(BASE + 'pages/' + page + '.html?id=' + work_id)
                    selection(p, group, 0)
                    p.screenshot(path=str(out / f'{page}-first-{width}.png'), full_page=True)
                    p.locator(group + ' button').nth(1).click()
                    p.evaluate("sessionStorage.setItem('dujia-prototype-fail-next','work-generate')")
                    p.locator('#generate').click()
                    p.wait_for_url('**/m05-p07.html*', timeout=15000)
                    failed = stored(p, work_id)
                    assert failed[field] == labels[1] and failed['story'] == story and failed['status'] == 'failed'
                    p.get_by_role('button', name='重新生成', exact=True).click()
                    p.wait_for_url('**/m05-p08.html*', timeout=15000)
                    final = stored(p, work_id)
                    assert final[field] == labels[1] and final['story'] == story and final['status'] == 'ready'
                    assert not errors, errors
                    row = dict(page=page, width=width, passed=True, field=field, labels=labels, work_id=work_id, final_value=final[field], status=final['status'])
                except Exception:
                    row = dict(page=page, width=width, passed=False, failure=traceback.format_exc()[-2600:], errors=errors)
                rows.append(row)
                print(('PASS ' if row['passed'] else 'FAIL ') + page + ' ' + str(width), flush=True)
                context.close()
        browser.close()
    assert files == source()
    report = dict(files=files, styles=styles, script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), results=rows)
    (out / 'results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    raise SystemExit(0 if all(row['passed'] for row in rows) else 1)


if __name__ == '__main__':
    main()
