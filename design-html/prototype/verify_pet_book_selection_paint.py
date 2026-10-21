"""Pet/book choice painting and pet action-copy containment at five widths."""
import argparse
import hashlib
import json
import traceback
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from audit_initial_quality import canonical
from verify_pet_controls import ROOT, DEMO, BASE, source

CASES = [('m07-p02', '.pets', '.pet'), ('m07-p08', '.foods', '.foods button'), ('m08-p04', '.options', '.options button'), ('m08-p08', '.templates', '.templates button'), ('m07-p06', None, '.option')]


def selected(p, selector, index):
    buttons = p.locator(selector)
    for i in range(buttons.count()):
        button = buttons.nth(i)
        expect(button).to_have_attribute('aria-pressed', str(i == index).lower())
        assert button.evaluate('e=>getComputedStyle(e).backgroundColor') not in ['transparent', 'rgba(0, 0, 0, 0)'], 'Native card must cover the old raster border'
        marker = button.locator('.selection-check')
        assert marker.count() == 1
        expect(marker).to_have_attribute('aria-hidden', 'true')
        if i == index: expect(marker).to_be_visible()
        else: expect(marker).not_to_be_visible()


def contained(p):
    rows = p.locator('.option small').evaluate_all('''es=>es.map(e=>{const r=document.createRange();r.selectNodeContents(e);const b=e.closest('button').getBoundingClientRect();return {text:e.textContent,rects:[...r.getClientRects()].map(x=>({left:x.left,right:x.right,top:x.top,bottom:x.bottom})),button:{left:b.left,right:b.right,top:b.top,bottom:b.bottom}}})''')
    for row in rows:
        b = row['button']
        for r in row['rects']:
            assert r['left'] >= b['left'] - 1 and r['right'] <= b['right'] + 1 and r['top'] >= b['top'] - 1 and r['bottom'] <= b['bottom'] + 1, 'Action cost text crosses its own card: ' + row['text']
    return rows


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--baseline', action='store_true'); args = parser.parse_args()
    out = ROOT / ('evidence/baseline/pet-book-selection-paint' if args.baseline else 'evidence/current/pet-book-selection-paint')
    out.mkdir(parents=True, exist_ok=True)
    files = source(); styles = {p.relative_to(DEMO).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEMO/'assets').glob('*.css')}; rows = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe', headless=True)
        for page, group, selector in CASES:
            for width in [320, 375, 390, 414, 430]:
                c = browser.new_context(viewport=dict(width=width, height=844), reduced_motion='reduce'); p = c.new_page(); p.set_default_timeout(6000); errors = []; p.on('pageerror', lambda e: errors.append(str(e)))
                try:
                    canonical(p, page)
                    buttons = p.locator(selector)
                    buttons.last.click()
                    p.screenshot(path=str(out/f'{page}-{width}.png'), full_page=True)
                    if group:
                        selected(p, selector, buttons.count()-1)
                        for index in range(buttons.count()):
                            button = buttons.nth(index); button.focus(); p.keyboard.press('Space'); selected(p, selector, index)
                            assert button.evaluate("e=>e.matches(':focus-visible') && parseFloat(getComputedStyle(e).outlineWidth)>=2")
                    else:
                        text_rects = contained(p)
                    if page == 'm07-p02':
                        p.locator('#pet-name').fill('小狐狸')
                        p.evaluate("sessionStorage.setItem('dujia-prototype-fail-next','pet-adopt')")
                        p.locator('#invite').click(); p.wait_for_function("sessionStorage.getItem('dujia-prototype-fail-next')!=='pet-adopt'")
                        expect(p.locator('.prototype-toast')).to_contain_text('重试'); selected(p, selector, 3)
                        assert p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-pet'))") is None
                        p.locator('#invite').click(); p.wait_for_url('**/m07-p01.html*')
                        pet = p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-pet'))")
                        assert pet['kind']=='小狐狸' and pet['name']=='小狐狸' and pet['status']=='pending'
                    elif page == 'm07-p08':
                        before = p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-pet'))")
                        p.locator('#feed').click()
                        p.wait_for_function("n=>JSON.parse(localStorage.getItem('dujia-prototype-pet')).food[2]===n-1", arg=before['food'][2])
                        expect(p.locator('.prototype-toast')).to_contain_text('喂食已记录'); selected(p, selector, 2)
                    elif page == 'm08-p04':
                        p.locator('.book-name').fill('空白原生状态测试')
                        p.locator('.next').click(); p.wait_for_url('**/m08-p05.html*')
                        assert p.evaluate("new URLSearchParams(location.search).get('id')")
                        assert p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-books')).some(b=>b.name==='空白原生状态测试' && b.start==='blank')")
                    elif page == 'm08-p08':
                        p.locator(selector).nth(1).click(); selected(p, selector, 1)
                        p.locator('.use').click(); p.wait_for_url('**/m08-p10.html*')
                        expect(p.locator('.screen')).to_be_visible()
                    else:
                        p.locator('#play').click(); p.wait_for_url('**/m07-p05.html*')
                        pet = p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-pet'))")
                        assert any(v['type']=='play' and v['text']=='送小礼物' for v in pet['logs'])
                    assert not errors, errors
                    row = dict(page=page, width=width, passed=True, result_url=p.url)
                    if not group: row['cost_text_bounds'] = text_rects
                except Exception:
                    row = dict(page=page, width=width, passed=False, errors=errors, failure=traceback.format_exc()[-2400:])
                rows.append(row); print(('PASS ' if row['passed'] else 'FAIL ') + page + ' ' + str(width), flush=True); c.close()
        browser.close()
    assert files == source()
    (out/'results.json').write_text(json.dumps(dict(files=files,styles=styles,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)


if __name__ == '__main__': main()
