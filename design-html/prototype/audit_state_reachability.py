"""Index existing source-page observations separately from action outcome URLs."""
import hashlib
import json
import re
from pathlib import Path

from verify_pet_controls import ROOT, DEMO, source

REPORTS = ['onboarding-control-results.json', 'record-controls-results.json',
           'moment-controls-results.json', 'time-controls-results.json',
           'workshop-controls-results.json', 'settings-controls-results.json',
           'pet-controls-results.json', 'book-controls-results.json']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    out = ROOT / 'evidence/current'
    initial_path = out / 'current-initial-replay/checkpoint.json'
    initial = read(initial_path)
    current = source()
    assert set(initial['files']) == set(current)
    changed = [name for name in current if current[name] != initial['files'][name]]
    assert changed == ['assets/prototype-workshop-store.js'], changed
    album_path = out / 'album-timeout/checkpoint.json'
    album = read(album_path); scope_path = out / 'album-timeout/source-scope.json'; scope = read(scope_path)
    assert album['files'] == current and album['timeout_cases'] == 3 and album['affected_regression_cases'] == 114
    assert album['source_scope_sha256'] == sha(scope_path)
    assert scope['before_sha256'] == initial['files'][changed[0]] and scope['after_sha256'] == current[changed[0]]
    assert scope['outside_function_unchanged'] and scope['private_function'] == 'decodedImage'
    assert scope['script_sha256'] == sha(ROOT / 'audit_album_timeout_scope.cjs')
    assert len(scope['album_callers']) == 1 and "page==='m05-p08'" in scope['album_callers'][0]['conditions']
    styles = {p.relative_to(DEMO).as_posix(): sha(p) for p in (DEMO / 'assets').glob('*.css')}
    assert styles == initial['styles'] == album['styles']
    for name, digest in initial['scripts_sha256'].items():
        assert sha(ROOT / name) == digest, name
    queue = read(ROOT / 'queue.json'); identities = {row['id'] for row in queue}
    origins, outcomes, reports = {}, set(), {}
    for name in REPORTS:
        path = out / name; digest = sha(path)
        assert any((ROOT / key if (ROOT / key).exists() else out / key).resolve() == path.resolve() and value == digest
                   for key, value in initial['reports_sha256'].items()), name
        report = read(path); rows = report['results'] if isinstance(report, dict) else report
        inventory = {r.get('page', r.get('id')): r for r in report.get('inventory', [])} if isinstance(report, dict) else {}
        if isinstance(report, dict):
            assert report['files'] == initial['files'], name
        reports[name] = digest
        for index, row in enumerate(rows):
            identity = row.get('page', row.get('id'))
            if identity not in identities or not row['passed'] or row.get('errors') or not row.get('selector'):
                continue
            effective = str(row.get('effective', row.get('url', '')))
            match = re.search(r'/(m\d\d-p\d\d)\.html', effective)
            if match: outcomes.add(match[1])
            origin_url = inventory.get(identity, {}).get('effective')
            if origin_url:
                assert '/'+identity+'.html' in origin_url, (identity, origin_url)
            origins.setdefault(identity, dict(report=path.relative_to(ROOT).as_posix(), row=index,
                                              selector=row['selector'], label=row.get('label', ''),
                                              contract=row.get('contract'), observed_origin_url=origin_url,
                                              action_outcome_url=effective,
                                              evidence_kind='prior source-page fixture and passed control; not a new browser execution'))
    assert set(origins) == identities and len(origins) == 114, sorted(identities - set(origins))
    for row in queue:
        identity = row['id']
        assert (DEMO / 'custom' / (identity+'.html')).read_bytes() == (DEMO / 'pages' / (identity+'.html')).read_bytes()
        row['automated_evidence']['origin_control'] = origins[identity]
    # Preserve every status and prior report hash; this is evidence indexing only.
    (ROOT / 'queue.json').write_text(json.dumps(queue, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    checkpoint = dict(files=current, styles=styles, reports_sha256=reports,
                      initial_checkpoint_sha256=sha(initial_path), album_checkpoint_sha256=sha(album_path),
                      source_scope_sha256=sha(scope_path), script_sha256=sha(Path(__file__)),
                      source_origins=114, distinct_action_outcomes=len(outcomes),
                      origin_only_in_this_comparison=sorted(identities-outcomes),
                      accepted_pages=0, new_browser_executions=0,
                      scope='Existing origin-page evidence indexed into the sole queue. Frozen initial reports kept verbatim; sole subsequent private decoder change is isolated and covered by album replay. Origin presence and named control behavior do not establish all design states, conditions or human visual acceptance.')
    destination = out / 'state-reachability'; destination.mkdir(parents=True, exist_ok=True)
    (destination / 'checkpoint.json').write_text(json.dumps(checkpoint, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key: checkpoint[key] for key in ['source_origins','distinct_action_outcomes','origin_only_in_this_comparison','new_browser_executions','accepted_pages']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
