"""Actual held HTTP image requests: deadline, late response and explicit retry."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import traceback

from playwright.sync_api import sync_playwright, expect, Error
from audit_hidden_overlays import declarations
from verify_image_read_order import A, uri
from verify_overlay_form_saves import storage
from verify_pet_controls import ROOT, DEMO, source
from verify_work_album_decode import photo_source, records, result, ID

CASES = ['timeout-retry', 'timeout-late-response', 'before-deadline-success']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    out = ROOT / ('evidence/baseline/album-timeout' if args.baseline else 'evidence/current/album-timeout')
    out.mkdir(parents=True, exist_ok=True)
    files = source()
    styles = {p.relative_to(DEMO).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in (DEMO / 'assets').glob('*.css')}
    if args.baseline:
        snapshot = out / 'prototype-workshop-store.js'
        assert not snapshot.exists(), 'Preserve the original baseline; choose another evidence directory for a later probe.'
        snapshot.write_bytes((DEMO / 'assets/prototype-workshop-store.js').read_bytes())
    fixture = declarations('verify_workshop_controls.py')
    png = declarations('verify_record_controls.py')['PNG']
    rows = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for name in CASES:
            context = browser.new_context(viewport=dict(width=390, height=844), reduced_motion='reduce')
            page = context.new_page()
            page.set_default_timeout(6000)
            page.set_default_navigation_timeout(15000)
            errors, pending = [], []
            gate = dict(hold=True)
            row = dict(case=name, phase='fixture')
            page.on('pageerror', lambda error: errors.append(str(error)))

            def intercept(route):
                if gate['hold']:
                    pending.append(route)
                else:
                    route.fulfill(status=200, content_type='image/png', body=png)

            page.route('**/album-timeout-probe.png*', intercept)
            try:
                fixture['seed'](page, 'm05-p08')
                photo_source(page, uri(A))
                page.reload()
                # The visible source is already loaded. The current stored source
                # now requests an explicitly stalled local URL during real export.
                photo_source(page, '../assets/album-timeout-probe.png?case=' + name)
                before = storage(page)
                assert result(page) is None
                button = page.locator('#save')
                with page.expect_request('**/album-timeout-probe.png*') as requested:
                    button.click()
                page.wait_for_timeout(50)
                assert len(pending) == 1
                expect(button).to_have_attribute('aria-busy', 'true')
                row.update(native_request_observed=True, request_url=requested.value.url,
                           phase='held-native-request', source_snapshot_preserved=storage(page) == before)
                started = time.perf_counter()
                if name == 'before-deadline-success':
                    page.wait_for_timeout(5000)
                    expect(button).to_be_disabled()
                    assert storage(page) == before
                    pending[0].fulfill(status=200, content_type='image/png', body=png)
                    expect(button).to_be_enabled()
                    assert result(page) and sum(value['id'] == ID for value in records(page)) == 1
                    saved = storage(page)
                    page.wait_for_timeout(11000)
                    assert storage(page) == saved
                    expect(button).to_be_enabled()
                    expect(page.locator('.prototype-toast[role=alert]')).to_have_count(0)
                    row.update(before_deadline_succeeded=True, stable_after_deadline=True)
                else:
                    page.wait_for_timeout(15250)
                    row.update(phase='deadline-check', waited_seconds=time.perf_counter() - started,
                               storage_preserved_at_deadline=storage(page) == before)
                    assert row['waited_seconds'] >= 15
                    expect(button).to_be_enabled(timeout=1000)
                    expect(page.locator('.prototype-toast[role=alert]')).to_contain_text('图片准备超时，请重试保存')
                    assert storage(page) == before and result(page) is None
                    row['deadline_recovered'] = True
                    if name == 'timeout-late-response':
                        try:
                            pending[0].fulfill(status=200, content_type='image/png', body=png)
                            row['late_response'] = 'delivered to the original route'
                        except Error as error:
                            row['late_response'] = 'original request already cancelled: ' + str(error)[:160]
                        page.wait_for_timeout(250)
                        assert storage(page) == before and result(page) is None
                        expect(button).to_be_enabled()
                        row['late_response_did_not_write'] = True
                    else:
                        gate['hold'] = False
                        button.click()
                        page.wait_for_function('id=>JSON.parse(localStorage.getItem("dujia-prototype-records")).some(v=>v.id===id)', arg=ID)
                        expect(button).to_be_enabled()
                        assert sum(value['id'] == ID for value in records(page)) == 1
                        expect(page.locator('.prototype-toast')).to_contain_text('已保存到共同相册')
                        saved = storage(page)
                        page.reload()
                        assert storage(page) == saved
                        row['explicit_retry_saved_once'] = True
                assert not errors, errors
                row.update(passed=True, waited_seconds=time.perf_counter() - started)
            except Exception:
                row.update(passed=False, failure=traceback.format_exc()[-2600:])
                page.screenshot(path=str(out / (name + '.png')), full_page=True)
            row['errors'] = errors
            rows.append(row)
            context.close()
            assert source() == files
            report = dict(files=files, styles=styles,
                          script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                          results=rows, accepted_pages=0,
                          scope='Three actual local HTTP image request stalls using native Image.decode and real wall-clock waits, no decoder Promise or timer mocking. Local source fixtures explicit; deadline/retry/late-write behavior only.')
            temporary = out / 'results.json.tmp'
            temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            temporary.replace(out / 'results.json')
            print(('PASS ' if row['passed'] else 'FAIL ') + name, flush=True)
        browser.close()
    print(json.dumps(dict(cases=3, passed=sum(row['passed'] for row in rows))), flush=True)
    raise SystemExit(0 if all(row['passed'] for row in rows) else 1)


if __name__ == '__main__':
    main()
