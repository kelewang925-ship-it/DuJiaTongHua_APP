"""Capture the114 declared design states using private existing module fixtures."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import traceback

from playwright.sync_api import sync_playwright, expect
from audit_hidden_overlays import MODULES, declarations
from audit_current_runtime import data
from verify_pet_controls import ROOT, DEMO, BASE, source


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def group(identity):
    if identity.startswith(('m01-', 'm02-')): return 'onboarding'
    return {'m03': 'record', 'm04': 'time' if 5 <= int(identity[-2:]) <= 15 else 'moment',
            'm05': 'workshop', 'm06': 'settings', 'm07': 'pet', 'm08': 'book'}[identity[:3]]


def onboarding(page, identity):
    values = data(False)
    if identity in ['m02-p05', 'm02-p06', 'm02-p09']:
        values['dujia-prototype-relationship'] = data(True)['dujia-prototype-relationship']
    page.goto(BASE + 'prototype/review.html')
    page.evaluate('''values=>{
      localStorage.clear();sessionStorage.clear();
      for(const [k,v] of Object.entries(values))localStorage.setItem(k,JSON.stringify(v));
      sessionStorage.setItem('dujia-prototype-peer-response','manual');
      sessionStorage.setItem('dujia-prototype-today','2026-10-06');
    }''', values)
    if identity == 'm01-p05':
        page.evaluate('sessionStorage.setItem("dujia-prototype-challenge",JSON.stringify({purpose:"recovery",verified:true,phone:"13812345678",expiresAt:Date.now()+600000,code:"284631"}))')
    if identity == 'm02-p08':
        page.evaluate('localStorage.setItem("dujia-prototype-invite",JSON.stringify({code:"XH7K9M2Q",expiresAt:1,status:"expired"}))')
    page.goto(BASE + 'pages/' + identity + '.html')


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--resume', action='store_true')
    parser.add_argument('--previous-script', type=Path); args = parser.parse_args()
    queue = json.loads((ROOT / 'queue.json').read_text(encoding='utf-8')); assert len(queue) == 114
    files = source()
    assets = {p.relative_to(DEMO).as_posix(): sha(p) for p in sorted((DEMO / 'assets').rglob('*')) if p.is_file()}
    fixtures = {name: declarations(module) for name, module in MODULES.items() if name != 'onboarding'}
    scripts = {name: sha(ROOT / name) for name in sorted(set(MODULES.values()) | {'audit_hidden_overlays.py', 'audit_current_runtime.py', 'book_test_helpers.py'})}
    own_sha = sha(Path(__file__))
    out = ROOT / 'evidence/current/design-state-capture'; out.mkdir(parents=True, exist_ok=True)
    report_path = out / 'results.json'; rows = []; provenance = {}; parents = []
    if report_path.exists():
        assert args.resume, 'Use --resume to retain verified completed captures.'
        previous = json.loads(report_path.read_text(encoding='utf-8'))
        assert previous['files'] == files and previous['assets'] == assets and previous['scripts_sha256'] == scripts
        prior_sha = previous['script_sha256']
        if prior_sha != own_sha:
            assert args.previous_script and sha(args.previous_script) == prior_sha
        parent = out / ('prior-' + sha(report_path)[:12] + '.json')
        if parent.exists(): assert parent.read_bytes() == report_path.read_bytes()
        else: parent.write_bytes(report_path.read_bytes())
        parents = previous.get('parent_reports', []) + [dict(path=parent.relative_to(ROOT).as_posix(), sha256=sha(parent), producer_script_sha256=prior_sha)]
        provenance = previous.get('capture_script_by_page', {})
        rows = [row for row in previous['results'] if row['passed']]
        for row in rows:
            assert row['fixture_group'] == group(row['page'])
            provenance.setdefault(row['page'], prior_sha)
        assert all(row['passed'] and sha(ROOT / row['screenshot']) == row['screenshot_sha256'] for row in rows)
    completed = {row['page'] for row in rows}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        version = browser.version
        for item in queue:
            identity = item['id']
            if identity in completed: continue
            context = browser.new_context(viewport=dict(width=390, height=844), device_scale_factor=1,
                                          reduced_motion='reduce', locale='zh-CN', timezone_id='Asia/Shanghai')
            page = context.new_page(); page.set_default_timeout(6500); page.set_default_navigation_timeout(15000)
            errors = []; page.on('pageerror', lambda error: errors.append(str(error)))
            row = dict(page=identity, title=item['title'], fixture_group=group(identity),
                       captured_at=datetime.now(timezone.utc).isoformat())
            try:
                if row['fixture_group'] == 'onboarding': onboarding(page, identity)
                else: fixtures[row['fixture_group']]['seed'](page, identity)
                assert '/' + identity + '.html' in page.url, page.url
                declared_identity = page.locator('body').get_attribute('data-prototype-page')
                assert declared_identity in [None, identity], declared_identity
                page.evaluate('document.fonts.ready')
                page.wait_for_timeout(350)
                expect(page.locator('.screen')).to_be_visible()
                metrics = page.evaluate('''()=>({width:innerWidth,height:innerHeight,dpr:devicePixelRatio,scrollWidth:document.documentElement.scrollWidth,scrollHeight:document.documentElement.scrollHeight,fonts:document.fonts.status,screen:document.querySelector('.screen').getAttribute('aria-label'),headings:[...document.querySelectorAll('h1')].map(e=>e.innerText),images:[...document.images].map(e=>({complete:e.complete,width:e.naturalWidth,src:e.getAttribute('src')}))})''')
                assert metrics['width'] == 390 and metrics['height'] == 844 and metrics['dpr'] == 1
                assert metrics['fonts'] == 'loaded' and metrics['scrollWidth'] <= 391
                assert not errors, errors
                screenshot = out / (identity + '.png')
                page.screenshot(path=str(screenshot), full_page=True)
                fixture_storage = page.evaluate('JSON.stringify({local:{...localStorage},session:{...sessionStorage}})')
                row.update(passed=True, effective=page.url, metrics=metrics,
                           screenshot=screenshot.relative_to(ROOT).as_posix(), screenshot_sha256=sha(screenshot),
                           reference_image=item['design_path'], fixture_storage_sha256=hashlib.sha256(fixture_storage.encode()).hexdigest())
            except Exception:
                row.update(passed=False, failure=traceback.format_exc()[-2400:], effective=page.url)
            row['errors'] = errors; rows.append(row); context.close()
            provenance[identity] = own_sha
            assert source() == files
            report = dict(files=files, assets=assets, scripts_sha256=scripts, script_sha256=own_sha,
                          capture_script_by_page=provenance, parent_reports=parents,
                          environment=dict(browser='Chrome headless',version=version,viewport=[390,844],dpr=1,locale='zh-CN',timezone='Asia/Shanghai',reduced_motion='reduce',capture='full-page PNG; image height follows actual document',baseline_status='temporary comparison condition; final project baseline unconfirmed'),
                          results=rows, accepted_pages=0, human_reviewer=None,
                          scope='Current declared design-state captures for manual comparison. Existing explicit mock names, dates and small SVG photo fixtures differ from original designs; captures and runtime checks are not human visual acceptance or proof of every interaction state.')
            report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
            print(('PASS ' if row['passed'] else 'FAIL ') + identity, flush=True)
            if not row['passed']: raise SystemExit(1)
        browser.close()
    assert len(rows) == 114 and source() == files
    assert {p.relative_to(DEMO).as_posix(): sha(p) for p in (DEMO / 'assets').rglob('*') if p.is_file()} == assets
    print(json.dumps(dict(captured=114, accepted_pages=0)), flush=True)


if __name__ == '__main__':
    main()
