"""Verify exact substitutions, constant aliases and observed visual equivalence."""
import json
import re
from pathlib import Path
from reconcile_current_style_tokens import ROOT, DEMO, OUT, fixture_files, jobs
from replay_current_initial_controls import deps, sha
from migrate_shared_style_tokens import migrate, COLORS, SPACES, FONTS, RADII, TIMES


def main():
    plan = json.loads((OUT / 'plan.json').read_text(encoding='utf-8'))
    before = json.loads((OUT / 'before.json').read_text(encoding='utf-8'))
    after = json.loads((OUT / 'after.json').read_text(encoding='utf-8'))
    applied = json.loads((OUT / 'applied.json').read_text(encoding='utf-8'))
    files = deps()
    assert before['complete'] and before['all_passed'] and after['complete'] and after['all_passed']
    assert before['dependencies'] == plan['dependencies']
    assert after['dependencies'] == applied['dependencies'] == files
    assert before['plan_sha256'] == after['plan_sha256'] == applied['plan_sha256'] == sha(OUT / 'plan.json')
    assert set(files) == set(before['dependencies'])
    changed = {n for n in files if files[n] != before['dependencies'][n]}
    assert changed == {r['file'] for r in plan['styles']} and len(changed) == 10
    assert sum(len(r['changes']) for r in plan['styles']) == applied['declarations'] == 191
    assert plan['new_token_definitions'] == 0
    assert plan['fixture_sha256'] == before['fixture_sha256'] == after['fixture_sha256'] == fixture_files()
    for name, digest in plan['fixture_sha256'].items():
        assert sha(ROOT / name) == sha(OUT / 'before-archive/fixtures' / name) == digest
    for name, digest in before['dependencies'].items():
        assert sha(OUT / 'before-archive/source' / name) == digest
        if name not in changed:
            assert sha(DEMO / name) == digest
    for row in plan['styles']:
        original = (OUT / 'before-archive/source' / row['file']).read_bytes().decode('utf-8')
        updated, changes = migrate(original)
        assert changes == row['changes']
        assert (DEMO / row['file']).read_bytes() == updated.encode('utf-8')
        assert sha(DEMO / row['file']) == row['after_sha256'] == sha(OUT / 'after-styles' / Path(row['file']).name)
        assert not migrate(updated)[1]
    assert all(not migrate(p.read_bytes().decode('utf-8'))[1] for p in (DEMO / 'assets').glob('prototype-*.css'))
    before_rows = {r['id']: r for r in before['results']}
    after_rows = {r['id']: r for r in after['results']}
    assert len(before_rows) == len(before['results']) == len(jobs()) == 151
    assert set(before_rows) == {r['id'] for r in jobs()}
    assert len(after_rows) == len(after['results']) == 72
    assert set(after_rows) == {r['id'] for r in before['results'] if r['affected']}
    assert sum(r['selector'] is None for r in after['results']) == 35
    assert sum(r['selector'] is not None for r in after['results']) == 37
    assert all(r['passed'] and not r['errors'] for r in before['results'] + after['results'])
    assert all(r['equal'] and r['observed'] == before_rows[k]['observed'] for k, r in after_rows.items())
    # The adopted aliases resolve to their exact existing literals. No nested
    # CSS definition or explicit JS setter can turn an alias into another value.
    expected = {token: value for table in [COLORS, SPACES, FONTS, RADII, TIMES] for value, token in table.items()}
    expected.update({'--prototype-font-family': 'Fairy,serif', '--prototype-control-compact': '40px',
                     '--prototype-touch': '44px', '--prototype-control-height': '48px'})
    used = {v for row in plan['styles'] for c in row['changes'] for v in re.findall(r'--prototype-[\w-]+', c['after'])}
    definitions = {k: [] for k in used}
    for name in files:
        if not name.endswith(('.css', '.html', '.js')):
            continue
        text = (DEMO / name).read_text(encoding='utf-8')
        for token in used:
            assert not re.search(r'setProperty\(\s*([\'\"])' + re.escape(token) + r'\1', text), (name, token)
            for match in re.finditer(re.escape(token) + r'\s*:\s*([^;}]+)', text):
                opening = text.rfind('{', 0, match.start())
                selector = text[:opening].rsplit('}', 1)[-1].rsplit(';', 1)[-1].strip()
                assert selector.endswith(':root'), (name, token, selector)
                assert match[1].strip() == expected[token], (name, token, match[1], expected[token])
                definitions[token].append(name)
    assert all(definitions.values())
    for row in before['results'] + after['results']:
        assert row['observed']['roots'] == {k: expected[k] for k in sorted(used)}
    # Existing business results retain their pre-change source hashes. Compose
    # them with this explicit CSS-only equivalence proof, never rewrite them.
    business = json.loads((ROOT / 'evidence/current/hidden-business-20261101-final/results.json').read_text(encoding='utf-8'))
    assert business['dependencies'] == before['dependencies'] and business['all_passed']
    assert all(not n.endswith(('.js', '.html')) for n in changed)
    print('PASS 10 CSS/191 exact-value aliases;151 before observations,72 affected contexts identical;constant root aliases;all HTML/JS/resources unchanged')


if __name__ == '__main__':
    main()
