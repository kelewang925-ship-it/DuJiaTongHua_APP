"""Exact-value adoption of existing tokens, with before/after browser evidence."""
import argparse
import ast
import hashlib
import json
import re
import traceback
from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import sync_playwright
import audit_initial_quality as Q
from migrate_shared_style_tokens import migrate
from replay_current_initial_controls import ROOT, DEMO, deps, sha, dump
from verify_pet_controls import BASE

OUT = ROOT / 'evidence/current/style-tokens-20261101'
PROPS = ['color', 'backgroundColor', 'fontSize', 'fontFamily', 'fontWeight', 'lineHeight',
         'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft', 'marginTop', 'marginRight', 'marginBottom', 'marginLeft',
         'borderTopColor', 'borderRightColor', 'borderBottomColor', 'borderLeftColor', 'borderTopWidth', 'borderRadius',
         'boxShadow', 'minHeight', 'minWidth', 'gap', 'rowGap', 'columnGap']
SNAPSHOT = """arg => {
 const properties=e=>arg.props.map(k=>e[k]);
 const elements=[...document.body.querySelectorAll('*')].filter(e=>e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden');
 const sheets=[];function visit(s){if(s.href)sheets.push(s.href);for(const r of s.cssRules||[])if(r.styleSheet)visit(r.styleSheet)}
 for(const s of document.styleSheets)visit(s);
 return {sheets:[...new Set(sheets)].sort(),roots:Object.fromEntries(arg.tokens.map(k=>[k,getComputedStyle(document.documentElement).getPropertyValue(k).trim()])),
  elements:elements.map(e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return {tag:e.tagName,classes:typeof e.className==='string'?e.className:e.className.baseVal,
    bounds:[r.x,r.y,r.width,r.height],styles:properties(s),pseudo:['::before','::after'].map(p=>{const x=getComputedStyle(e,p);return ['none','normal'].includes(x.content)?null:[x.content,properties(x)]})}}),
  scroll:[document.documentElement.scrollWidth,document.documentElement.scrollHeight]};
}"""


def fixture_files():
    pending = [Path(__file__).resolve()]
    found = set()
    while pending:
        path = pending.pop()
        if path in found:
            continue
        found.add(path)
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            names = ([node.module.split('.')[0] + '.py'] if isinstance(node, ast.ImportFrom) and node.module else
                     [a.name.split('.')[0] + '.py' for a in node.names] if isinstance(node, ast.Import) else
                     [node.value] if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value.endswith('.py') else [])
            for name in names:
                other = ROOT / name
                if other.is_file() and other not in found:
                    pending.append(other)
    return {p.name: sha(p) for p in sorted(found)}


def build_plan():
    rows = []
    for path in sorted((DEMO / 'assets').glob('prototype-*.css')):
        raw = path.read_bytes()
        updated, changes = migrate(raw.decode('utf-8'))
        if changes:
            rows.append(dict(file=path.relative_to(DEMO).as_posix(), before_sha256=sha(path),
                             after_sha256=hashlib.sha256(updated.encode('utf-8')).hexdigest(), changes=changes))
    assert len(rows) == 10 and sum(len(r['changes']) for r in rows) == 191
    return rows


def jobs():
    catalog = json.loads((ROOT / 'evidence/current/initial-controls-20261031-accessible/contracts.json').read_text(encoding='utf-8'))
    rows = [dict(id=p['id'], page=p['id'], selector=None) for p in catalog['pages']]
    for p in catalog['pages']:
        if p['id'].startswith('m08'):
            for c in p['initial_controls']:
                if c['contract'].startswith(('sheet:', 'modal:')):
                    rows.append(dict(id=p['id'] + ':' + c['selector'], page=p['id'], selector=c['selector']))
    extras = json.loads((ROOT / 'evidence/current/hidden-business-20261101/catalog-overlays.json').read_text(encoding='utf-8'))
    rows.extend(dict(id=v['page'] + ':' + v['selector'], page=v['page'], selector=v['selector']) for v in extras['observations'])
    assert len(rows) == 151 and len({r['id'] for r in rows}) == 151
    return rows


def served(files):
    for name, digest in files.items():
        url = BASE + (name.replace('custom/', 'pages/', 1) if name.startswith('custom/') else name)
        with urlopen(url, timeout=10) as response:
            assert hashlib.sha256(response.read()).hexdigest() == digest, name


def capture(stage):
    path = OUT / (stage + '.json')
    assert not path.exists(), 'Refuse to overwrite an observation phase'
    plan = json.loads((OUT / 'plan.json').read_text(encoding='utf-8'))
    files = deps()
    scripts = fixture_files()
    assert scripts == plan['fixture_sha256']
    previous = json.loads((OUT / 'before.json').read_text(encoding='utf-8')) if stage == 'after' else None
    if previous:
        assert previous['complete'] and previous['all_passed']
        changed = {k for k in files if files[k] != previous['dependencies'].get(k)}
        assert changed == {r['file'] for r in plan['styles']}
        assert all(files[r['file']] == r['after_sha256'] for r in plan['styles'])
    else:
        assert files == plan['dependencies']
    candidates = jobs()
    if previous:
        wanted = {r['id'] for r in previous['results'] if r['affected']}
        candidates = [r for r in candidates if r['id'] in wanted]
    tokens = sorted({v for r in plan['styles'] for c in r['changes'] for v in re.findall(r'--prototype-[\w-]+', c['after'])})
    report = dict(stage=stage, dependencies=files, fixture_sha256=scripts, plan_sha256=sha(OUT / 'plan.json'),
                  viewport=[390, 844], reduced_motion='reduce', properties=PROPS, results=[], complete=False,
                  scope='Visible computed properties, geometry, pseudo-elements and root aliases in canonical initial fixtures and31 book/6 catalog overlays. Only affected loaded stylesheet contexts replayed after exact substitution; not business execution or human visual acceptance.')
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for index, candidate in enumerate(candidates):
            context = browser.new_context(viewport=dict(width=390, height=844), reduced_motion='reduce', locale='zh-CN', timezone_id='Asia/Shanghai')
            page = context.new_page()
            page.set_default_timeout(6000)
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            row = dict(candidate, passed=False)
            try:
                Q.canonical(page, candidate['page'])
                if candidate['selector']:
                    page.locator(candidate['selector']).click()
                    page.locator('dialog[open]').wait_for()
                observed = page.evaluate(SNAPSHOT, dict(props=PROPS, tokens=tokens))
                assert all(observed['roots'].values())
                loaded = {url.rsplit('/', 1)[-1] for url in observed['sheets']}
                row['affected'] = any(r['file'].rsplit('/', 1)[-1] in loaded for r in plan['styles'])
                row['observed'] = observed
                if previous:
                    before = next(r['observed'] for r in previous['results'] if r['id'] == candidate['id'])
                    row['equal'] = observed == before
                    assert row['equal'], 'Computed values/geometry/visible element structure changed'
                assert not errors, errors
                row['passed'] = True
            except Exception:
                row['failure'] = traceback.format_exc()
                page.screenshot(path=str(OUT / (stage + '-' + str(index) + '-failure.png')), full_page=True)
            row['errors'] = errors
            report['results'].append(row)
            context.close()
            assert deps() == files and fixture_files() == scripts
            dump(path, report)
            if (index + 1) % 15 == 0 or not row['passed']:
                print(stage, index + 1, '/', len(candidates), 'PASS' if row['passed'] else 'FAIL', candidate['page'], flush=True)
        browser.close()
    report['complete'] = True
    report['all_passed'] = all(r['passed'] for r in report['results'])
    dump(path, report)
    print(stage, len(report['results']), 'observed;', sum(r['passed'] for r in report['results']), 'passed; affected', sum(r.get('affected', False) for r in report['results']))
    return 0 if report['all_passed'] else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=['before', 'apply', 'after'])
    stage = parser.parse_args().stage
    OUT.mkdir(parents=True, exist_ok=True)
    if stage == 'before':
        assert not (OUT / 'plan.json').exists()
        files, scripts = deps(), fixture_files()
        plan = dict(dependencies=files, fixture_sha256=scripts, styles=build_plan(), new_token_definitions=0)
        for sub, origin, mapping in [('source', DEMO, files), ('fixtures', ROOT, scripts)]:
            for name in mapping:
                target = OUT / 'before-archive' / sub / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((origin / name).read_bytes())
        dump(OUT / 'plan.json', plan)
        served(files)
        return capture('before')
    if stage == 'apply':
        plan = json.loads((OUT / 'plan.json').read_text(encoding='utf-8'))
        before = json.loads((OUT / 'before.json').read_text(encoding='utf-8'))
        assert before['complete'] and before['all_passed'] and deps() == plan['dependencies']
        assert fixture_files() == plan['fixture_sha256']
        assert not (OUT / 'applied.json').exists()
        for row in plan['styles']:
            path = DEMO / row['file']
            assert sha(path) == row['before_sha256']
            updated, changes = migrate(path.read_bytes().decode('utf-8'))
            assert changes == row['changes']
            path.write_bytes(updated.encode('utf-8'))
            assert sha(path) == row['after_sha256'] and not migrate(updated)[1]
            archive = OUT / 'after-styles' / path.name
            archive.parent.mkdir(exist_ok=True)
            archive.write_bytes(path.read_bytes())
        served({r['file']: r['after_sha256'] for r in plan['styles']})
        dump(OUT / 'applied.json', dict(dependencies=deps(), plan_sha256=sha(OUT / 'plan.json'), declarations=191, stylesheets=10))
        print('Applied191 exact-value aliases in10 stylesheets;201 dependencies checked;10 served bytes match')
        return 0
    return capture('after')


if __name__ == '__main__':
    raise SystemExit(main())
