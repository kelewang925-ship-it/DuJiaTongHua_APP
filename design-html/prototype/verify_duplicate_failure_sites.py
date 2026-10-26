"""Exercise previously untraced entrances that share a mock failure operation name."""
import hashlib
import json
import traceback
from pathlib import Path

from playwright.sync_api import sync_playwright, expect
from audit_hidden_overlays import declarations, seed_onboarding
from trace_failure_suite import TRACE
from verify_pet_controls import ROOT, DEMO, source

INSTRUMENT = 'window.__failureSites=[];window.__recordConsumedFailure=event=>window.__failureSites.push(event);' + TRACE.replace(
    '{operation,url:location.href}', '{operation,url:location.href,stack:new Error().stack}')


def store(page):
    return page.evaluate('JSON.stringify({...localStorage})')


def inject(page, operation, button, message):
    page.evaluate('op=>sessionStorage.setItem("dujia-prototype-fail-next",op)', operation)
    button.click()
    expect(page.locator(message)).to_be_visible()
    expect(button).to_be_enabled()
    assert page.evaluate('sessionStorage.getItem("dujia-prototype-fail-next")') != operation
    events = page.evaluate('window.__failureSites')
    assert len(events) == 1 and events[0]['operation'] == operation
    assert 'prototype-' in events[0]['stack']
    return events[0]


def main():
    files = source(); fixtures = declarations('verify_workshop_controls.py')
    out = ROOT / 'evidence/current/duplicate-failure-sites'; out.mkdir(parents=True, exist_ok=True)
    rows = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for name in ['credentials-retry-page', 'otp-resend', 'recovery-verify', 'recovery-send-code', 'work-save-generate']:
            context = browser.new_context(viewport=dict(width=390, height=420), reduced_motion='reduce')
            context.add_init_script(INSTRUMENT)
            page = context.new_page(); page.set_default_timeout(6500)
            errors = []; page.on('pageerror', lambda e: errors.append(str(e)))
            row = dict(case=name)
            try:
                if name == 'credentials-retry-page':
                    seed_onboarding(page, 'm01-p06'); before = store(page)
                    page.locator('#password').fill('Demo1234'); button = page.locator('.retry')
                    event = inject(page, 'credentials', button, '#error')
                    expect(page.locator('#error')).to_contain_text('3')
                    expect(page.locator('#password')).to_have_value('')
                    assert store(page) == before
                    page.locator('#password').fill('Demo1234'); button.click(); page.wait_for_url('**/m02-p01.html')
                    assert page.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-session")).loggedIn')
                elif name == 'otp-resend':
                    seed_onboarding(page, 'm01-p07')
                    page.evaluate('()=>{const key="dujia-prototype-challenge",v=JSON.parse(sessionStorage.getItem(key));v.resendAt=Date.now()-1000;sessionStorage.setItem(key,JSON.stringify(v))}')
                    button = page.locator('#resend'); expect(button).to_be_enabled()
                    for index, digit in enumerate('123456'): page.locator('.code input').nth(index).fill(digit)
                    before = store(page); challenge = page.evaluate('sessionStorage.getItem("dujia-prototype-challenge")')
                    event = inject(page, 'send-code', button, '.prototype-toast')
                    assert store(page) == before and page.evaluate('sessionStorage.getItem("dujia-prototype-challenge")') == challenge
                    assert page.locator('.code input').evaluate_all('fields=>fields.map(e=>e.value).join("")') == '123456'
                    button.click(); expect(button).to_be_disabled()
                    page.wait_for_function('document.querySelector(".code input").value===""')
                    assert page.evaluate('sessionStorage.getItem("dujia-prototype-challenge")') != challenge
                elif name.startswith('recovery-'):
                    seed_onboarding(page, 'm01-p04'); page.locator('[name=phone]').fill('13812345678')
                    before = store(page); challenge = page.evaluate('sessionStorage.getItem("dujia-prototype-challenge")')
                    operation = 'verify' if name == 'recovery-verify' else 'send-code'
                    button = page.locator('.next' if operation == 'verify' else '#send')
                    event = inject(page, operation, button, '.prototype-toast')
                    assert store(page) == before and page.evaluate('sessionStorage.getItem("dujia-prototype-challenge")') == challenge
                    expect(page.locator('[name=phone]')).to_have_value('13812345678')
                    button.click()
                    if operation == 'verify': page.wait_for_url('**/m01-p07.html')
                    else: expect(page.locator('.prototype-toast')).to_contain_text('284631')
                    assert page.evaluate('JSON.parse(sessionStorage.getItem("dujia-prototype-challenge")).purpose') == 'recovery'
                else:
                    fixtures['seed'](page, 'm05-p03'); page.locator('#story').fill('生成提交失败后保留这段长故事。' * 30)
                    before = store(page); story = page.locator('#story').input_value(); button = page.locator('#generate')
                    event = inject(page, 'work-save', button, '.prototype-toast')
                    assert store(page) == before
                    expect(page.locator('#story')).to_have_value(story)
                    button.click(); page.wait_for_url('**/m05-p06.html?**')
                    assert page.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-works"))[0].status') == 'generating'
                assert not errors, errors
                row.update(passed=True, consumed_event=event, failure_preserved_data=True, explicit_retry_succeeded=True)
            except Exception:
                row.update(passed=False, failure=traceback.format_exc()[-2500:])
                page.screenshot(path=str(out / (name + '.png')), full_page=True)
            row.update(errors=errors, effective=page.url); rows.append(row); context.close()
            assert source() == files
            report = dict(files=files, results=rows, script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                          tracer_sha256=hashlib.sha256((ROOT / 'trace_failure_suite.py').read_bytes()).hexdigest(),
                          scope='Five explicit missing entrances; real failNext consumption with runtime caller stack, data checks and retry. Expired resend cooldown is a declared local fixture; no clock or failure result replacement.', accepted_pages=0)
            (out / 'results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            print(('PASS ' if row['passed'] else 'FAIL ') + name, flush=True)
        browser.close()
    print(json.dumps(dict(cases=5, passed=sum(row['passed'] for row in rows))), flush=True)
    raise SystemExit(0 if all(row['passed'] for row in rows) else 1)


if __name__ == '__main__':
    main()
