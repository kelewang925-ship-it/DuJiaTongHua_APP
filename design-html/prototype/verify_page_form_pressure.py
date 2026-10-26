"""Original-page fields under long-input and short-viewport pressure; private mock data only."""
import argparse
import hashlib
import json
import traceback
from pathlib import Path

from playwright.sync_api import sync_playwright
from audit_hidden_overlays import MODULES, declarations, seed_onboarding
from audit_runtime import INIT
from verify_pet_controls import ROOT, DEMO, source
from verify_native_shared_fields import Fields, SELECTOR
from verify_native_field_flows import PAGES, POSITIVE


def group(page):
    if page.startswith(('m01-', 'm02-')):
        return 'onboarding'
    return {'m03': 'record', 'm04': 'time' if int(page[-2:]) >= 7 else 'moment',
            'm05': 'workshop', 'm06': 'settings', 'm07': 'pet', 'm08': 'book'}[page[:3]]


def reachable(target):
    target.scroll_into_view_if_needed()
    metrics = target.evaluate('''e=>{const r=e.getBoundingClientRect(),x=r.x+r.width/2,y=r.y+r.height/2,h=document.elementFromPoint(x,y);return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:innerWidth,height:innerHeight,hit:h===e||e.contains(h),coveredBy:h?.outerHTML.slice(0,260)}}''')
    assert metrics['left'] >= -1 and metrics['right'] <= metrics['width'] + 1, metrics
    assert 0 <= (metrics['top'] + metrics['bottom']) / 2 <= metrics['height'] and metrics['hit'], metrics
    return metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pages')
    parser.add_argument('--long-only', action='store_true')
    parser.add_argument('--output', default='results.json')
    args = parser.parse_args()
    assert Path(args.output).name == args.output and args.output.endswith('.json')
    files = source()
    fixtures = {name: declarations(module) for name, module in MODULES.items() if name != 'onboarding'}
    pages = []
    for path in sorted((DEMO / 'custom').glob('*.html')):
        parser = Fields(); parser.feed(path.read_text(encoding='utf-8'))
        if parser.count:
            pages.append(path.stem)
    assert len(pages) == 29
    saves = {}
    candidates = {}
    for name in fixtures:
        path = ROOT / 'evidence/current' / (name + '-controls-results.json')
        raw = path.read_bytes(); report = json.loads(raw)
        candidates[path.relative_to(ROOT).as_posix()] = hashlib.sha256(raw).hexdigest()
        inventory = {(r.get('page', r.get('id')), c['selector']): c for r in report['inventory'] for c in r['controls']}
        for row in report['results']:
            identity, kind = row.get('page'), row.get('contract')
            if 'selector' not in row:
                continue
            key = (identity, row['selector'])
            if identity in PAGES and kind in POSITIVE and key in inventory and identity not in saves:
                control = inventory[key]
                assert fixtures[name]['contract'](identity, control) == kind
                saves[identity] = (name, control, kind)
    assert set(saves) == PAGES, sorted(PAGES - set(saves))
    out = ROOT / 'evidence/current/page-form-pressure'; out.mkdir(parents=True, exist_ok=True)
    rows = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for width in [320, 390]:
            modes = [('long-input', pages)] + ([] if args.long_only else [('normal-action', sorted(saves))])
            for mode, identities in modes:
                for identity in identities:
                    if args.pages and identity not in args.pages.split(','):
                        continue
                    context = browser.new_context(viewport=dict(width=width, height=420), reduced_motion='reduce')
                    context.add_init_script(INIT)
                    page = context.new_page(); page.set_default_timeout(6500)
                    errors = []; page.on('pageerror', lambda error: errors.append(str(error)))
                    row = dict(page=identity, mode=mode, width=width, height=420)
                    try:
                        if mode == 'normal-action':
                            name, control, kind = saves[identity]
                            fixtures[name]['control'](page, identity, control, kind)
                            row.update(selector=control['selector'], contract=kind)
                        else:
                            name = group(identity)
                            if name == 'onboarding': seed_onboarding(page, identity)
                            else: fixtures[name]['seed'](page, identity)
                            assert identity + '.html' in page.url, page.url
                            page.evaluate('document.fonts.ready')
                            page.add_style_tag(content=':root{--ui-safe-top:44px;--ui-safe-bottom:34px}')
                            tested = []
                            fields = page.locator(SELECTOR)
                            for index in range(fields.count()):
                                field = fields.nth(index)
                                if not field.is_visible() or not field.is_enabled(): continue
                                info = field.evaluate('e=>({id:e.id,type:e.type,tag:e.tagName,readonly:!!e.readOnly,max:e.maxLength,inputmode:e.inputMode})')
                                if not info['readonly'] and info['tag'] != 'SELECT':
                                    value = '9' * 6000 if info['type'] == 'tel' or info['inputmode'] in ['numeric', 'decimal'] else 'Abc长输入' * 1000
                                    field.fill(value)
                                    actual = field.input_value()
                                    if info['max'] is not None and info['max'] >= 0:
                                        assert len(actual) <= info['max'], info
                                    assert actual, 'Long input was entirely filtered: ' + str(info)
                                    info['actual_length'] = len(actual)
                                info['bounds'] = reachable(field)
                                if not info['readonly'] and info['tag'] != 'SELECT':
                                    field.click()
                                tested.append(info)
                            row['fields'] = tested
                            primary = page.locator('.screen button[type=submit],.screen .submit,.screen .save,.screen #save,.screen .next,.screen #generate,.screen #invite,.screen .done')
                            row['primary'] = [dict(text=button.inner_text(), bounds=reachable(button)) for button in primary.all() if button.is_visible() and button.is_enabled()]
                            assert tested
                            assert page.evaluate('document.documentElement.scrollWidth') <= width + 1
                        assert not errors, errors
                        row['passed'] = True
                    except Exception:
                        row.update(passed=False, failure=traceback.format_exc()[-2500:])
                        page.screenshot(path=str(out / (identity + '-' + mode + '-' + str(width) + '.png')), full_page=True)
                    row.update(errors=errors, effective=page.url); rows.append(row); context.close()
                    assert source() == files
                    report = dict(files=files, script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                  locator_candidates_sha256=candidates, results=rows, accepted_pages=0,
                                  scope='29 original-page field contexts with long input, real scrolling and hit testing at320/390x420, simulated44/34 safe inset;19 normal save/reply/generate contracts at same short height. Not actual mobile IME or human visual acceptance.')
                    (out / args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
                    print(('PASS ' if row['passed'] else 'FAIL ') + identity + ' ' + mode + ' ' + str(width), flush=True)
        browser.close()
    print(json.dumps(dict(cases=len(rows), passed=sum(row['passed'] for row in rows))), flush=True)
    raise SystemExit(0 if all(row['passed'] for row in rows) else 1)


if __name__ == '__main__':
    main()
