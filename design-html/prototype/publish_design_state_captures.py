"""Verify114 real captures and link them from the existing page catalog and queue."""
import hashlib
import json
from pathlib import Path
import re
import struct

from verify_pet_controls import ROOT, DEMO, source


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    folder = ROOT / 'evidence/current/design-state-capture'
    report_path = folder / 'results.json'; report = read(report_path)
    assert report['files'] == source()
    assert report['assets'] == {p.relative_to(DEMO).as_posix(): sha(p) for p in (DEMO / 'assets').rglob('*') if p.is_file()}
    for name, digest in report['scripts_sha256'].items(): assert sha(ROOT / name) == digest, name
    producers = {sha(ROOT / 'capture_design_states.py'): 'capture_design_states.py',
                 sha(folder / 'executed-before-group-fix.py'): (folder / 'executed-before-group-fix.py').relative_to(ROOT).as_posix()}
    assert set(report['capture_script_by_page'].values()) == set(producers)
    assert report['script_sha256'] == sha(ROOT / 'capture_design_states.py')
    assert len(report['results']) == 114 and all(row['passed'] and not row['errors'] for row in report['results'])
    by_id = {row['page']: row for row in report['results']}; assert len(by_id) == 114
    for parent in report['parent_reports']:
        assert sha(ROOT / parent['path']) == parent['sha256']
        prior = read(ROOT / parent['path'])
        assert prior['script_sha256'] == parent['producer_script_sha256']
        for row in prior['results']:
            if row['passed']: assert by_id[row['page']] == row, row['page']
    queue_path = ROOT / 'queue.json'; queue = read(queue_path)
    assert {row['id'] for row in queue} == set(by_id)
    dimensions = {}
    for row in queue:
        capture = by_id[row['id']]; screenshot = ROOT / capture['screenshot']
        assert sha(screenshot) == capture['screenshot_sha256']
        raw = screenshot.read_bytes(); assert raw[:8] == b'\x89PNG\r\n\x1a\n'
        width, height = struct.unpack('>II', raw[16:24]); dimensions[row['id']] = [width,height]
        assert width == 390 and abs(height-capture['metrics']['scrollHeight']) <= 2
        assert capture['reference_image'] == row['design_path'] and (ROOT.parent.parent / row['design_path']).is_file()
        assert all(image['complete'] and image['width'] > 0 for image in capture['metrics']['images'] if image['src'])
        row['automated_evidence']['design_state_capture'] = dict(report=report_path.relative_to(ROOT).as_posix(), page=row['id'],
                                                               screenshot=capture['screenshot'], sha256=capture['screenshot_sha256'])
        row['last_verification'] = dict(verified_at=capture['captured_at'], verifier='Codex（截图与运行自检）',
                                       verification_kind='design-state-capture', viewport_css_px=[390,844],
                                       browser_and_dpr=report['environment'], screenshot_path=capture['screenshot'],
                                       screenshot_pixels=[width,height], console_or_check_log=report_path.relative_to(ROOT).as_posix(),
                                       interaction_cases=[], visual_differences=[],
                                       result='指定mock设计状态截图与运行检查通过；未逐页人工对照，不认定无差异；交互证据另列',
                                       human_reviewer=None,human_reviewed_at=None)
    queue_path.write_text(json.dumps(queue, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    catalog = ROOT / 'PAGE_CATALOG.md'; lines = []; linked = []
    for line in catalog.read_text(encoding='utf-8').splitlines():
        if line.startswith('| 页面 |') and '自动截图' not in line:
            line += ' 原稿导出／自动截图（待人工） |'
        elif line.startswith('| --- |') and '自动截图' not in '\n'.join(lines[-2:]):
            pass
        elif line.startswith('| --- |') and '自动截图' in '\n'.join(lines[-2:]) and line.count('|') == 7:
            line += ' --- |'
        match = re.match(r'^\| (m\d\d-p\d\d) \|', line)
        if match:
            identity = match[1]; linked.append(identity)
            addition = f' [原稿导出](../assets/{identity}-source.webp) · [自动截图]({by_id[identity]["screenshot"]}) |'
            if '[自动截图]' not in line: line += addition
        lines.append(line)
    assert set(linked) == set(by_id) and len(linked) == 114
    catalog.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    checkpoint = dict(files=report['files'], captured_pages=114, accepted_pages=0, human_reviewer=None,
                      report_sha256=sha(report_path), producer_scripts=producers, dimensions=dimensions,
                      publication_script_sha256=sha(Path(__file__)),
                      actual_executions=[dict(session=78780,exit_code=1,retained_captures=33,reason='fixture-group collector error before m04-p05 capture'),
                                         dict(session=11094,exit_code=0,new_captures=81)],
                      scope='114 saved design-state screenshots linked to the sole queue/catalog;33 prior valid captures retained with exact producer provenance. Not human visual acceptance or an interaction replay.')
    (folder / 'checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(captured_pages=114,catalog_links=114,accepted_pages=0)))


if __name__ == '__main__':
    main()
