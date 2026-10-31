"""Publish traceable navigation without turning shared cases into click edges."""
import argparse
import hashlib
import json
import re
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DEMO = ROOT.parent
OUT = ROOT / 'evidence/current/navigation-atlas-20261101.json'
GRAPH = ROOT / 'CURRENT_NAVIGATION_ATLAS.mmd'
DOC = ROOT / 'CURRENT_NAVIGATION_ATLAS.md'


@lru_cache(maxsize=None)
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@lru_cache(maxsize=None)
def load(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))


def page(value):
    if not isinstance(value, str):
        return None
    match = re.fullmatch(r'(m\d\d-p\d\d)', value)
    if match:
        return match[1]
    match = re.fullmatch(r'/pages/(m\d\d-p\d\d)\.html', urlparse(value).path)
    return match[1] if match else None


def label(text):
    return str(text).replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', ' ')[:100]


def build():
    initial_name = 'evidence/current/initial-controls-20261031-accessible/results.json'
    contract_name = 'evidence/current/initial-controls-20261031-accessible/contracts.json'
    hidden_name = 'evidence/current/hidden-business-20261101-final/control-business-index.json'
    initial, contracts, hidden = map(load, [initial_name, contract_name, hidden_name])
    pages = {p['id']: {'id': p['id'], 'title': p['title'], 'type': p['type']} for p in contracts['pages']}
    assert len(pages) == 114
    assert initial['all_passed'] and hidden['missing_controls'] == 0
    inputs = {n: digest(ROOT / n) for n in [initial_name, contract_name, hidden_name]}
    token_plan_name = 'evidence/current/style-tokens-20261101/plan.json'
    token_plan = load(token_plan_name)
    token_styles = {row['file']: row for row in token_plan['styles']}
    book_name = 'assets/prototype-book-v2.css'
    old_book = ROOT / 'evidence/current/quality-20261031/source' / book_name
    before_tokens = ROOT / 'evidence/current/style-tokens-20261101/before-archive/source' / book_name
    hot_area = ('.book-v2[data-book-page="19"] .v2-upload input[type="file"]{min-height:var(--prototype-touch,44px)}\r\n'
                '.book-v2[data-book-page="19"] .v2-upload input[type="file"]::file-selector-button{min-height:var(--prototype-touch,44px);font:inherit}\r\n').encode()
    assert old_book.read_bytes() + hot_area == before_tokens.read_bytes()
    # Retain collection-time hashes. Only CSS changed after these collections;
    # the separately verified style-equivalence checkpoint describes that change.
    compatibility = {}
    for name, dependencies in [('initial', initial['dependencies']), ('hidden', hidden['dependencies'])]:
        differences = []
        for relative, old in dependencies.items():
            current = digest(DEMO / relative)
            if current != old:
                assert relative.endswith('.css'), (name, relative)
                assert relative in token_styles
                assert current == token_styles[relative]['after_sha256']
                expected_before = token_plan['dependencies'][relative]
                assert old == expected_before or (relative == book_name and old == digest(old_book) and expected_before == digest(before_tokens))
                differences.append({'file': relative, 'collected_sha256': old, 'current_sha256': current})
        compatibility[name] = differences
    for n in ['evidence/current/style-tokens-20261101/plan.json', 'evidence/current/style-tokens-20261101/after.json',
              'evidence/current/quality-file-target-20261031/results.json']:
        inputs[n] = digest(ROOT / n)
    edges = []
    for i, row in enumerate(initial['results']):
        target = page(row.get('effective'))
        if target and target != row['page']:
            assert row['passed'] and not row.get('errors') and target in pages
            edges.append({'source': row['page'], 'target': target, 'trigger': row['label'],
                          'selector': row['selector'], 'contract': row['contract'], 'url': row['effective'],
                          'evidence': {'report': initial_name, 'row': i, 'sha256': inputs[initial_name]}})
    assert len(edges) == 393
    references = {}
    for item_index, item in enumerate(hidden['items']):
        for ref in item['business_evidence']:
            key = (ref['report'], ref['row'])
            references.setdefault(key, []).append({'item': item_index, 'page': item['page'],
                'observation': item['observation'], 'control': item['control']['label'],
                'mapping_kind': item['mapping_kind']})
            assert digest(ROOT / ref['report']) == ref['sha256']
            inputs[ref['report']] = ref['sha256']
    outcomes, without_terminal = [], []
    for (report, index), refs in sorted(references.items(), key=lambda v: (v[0][0], -1 if v[0][1] is None else v[0][1])):
        data = load(report)
        row = data if index is None else data['results'][index]
        assert row['passed'] and not row.get('errors')
        target = page(row.get('effective')) or page(row.get('destination'))
        record = {'evidence': {'report': report, 'row': index, 'sha256': inputs[report]},
                  'case': {k: row[k] for k in ['case', 'mode', 'operation', 'kind', 'original_suite_case_id', 'result'] if k in row},
                  'linked_controls': refs}
        if target:
            sources = [row['page']] if row.get('page') in pages else sorted({v['page'] for v in refs})
            assert target in pages
            record.update(sources=sources, target=target, url=row.get('effective'),
                          semantics='multi-step-case-terminal; linked controls are correspondence, not individual click edges')
            outcomes.append(record)
        else:
            record['semantics'] = 'no explicit terminal URL recorded; local state/close/field evidence, not a navigation assertion'
            without_terminal.append(record)
    observations = [{k: o[k] for k in ['id', 'page', 'selector', 'trigger', 'title', 'lifecycle_evidence']} for o in hidden['observations']]
    assert len(observations) == 110
    model = {'scope': '393 observed initial click edges;110 observed manual overlay entries;explicit terminal outcomes from linked business cases',
             'pages': list(pages.values()), 'initial_edges': edges, 'overlays': observations,
             'case_terminals': outcomes, 'cases_without_terminal': without_terminal,
             'input_sha256': inputs, 'css_changes_since_collection': compatibility,
             'limitations': ['Not a new browser replay.', 'Case terminals do not imply one-click or all shared variants.',
                            'No explicit terminal is not evidence of a dead end.', 'Unobserved conditional combinations remain outside this atlas.']}
    graph = ['flowchart LR']
    for p in pages.values():
        graph.append(f'  {p["id"].replace("-", "_")}["{label(p["id"] + " " + p["title"])}"]')
    # Keep repeated observed click edges in JSON; coalesce same labels in diagram.
    for source, target, trigger in sorted({(r['source'], r['target'], r['trigger']) for r in edges}):
        graph.append(f'  {source.replace("-", "_")} -->|"{label(trigger)}"| {target.replace("-", "_")}')
    for i, o in enumerate(observations):
        graph.append(f'  O{i}["弹层 {label(o["title"])}"]')
        graph.append(f'  {o["page"].replace("-", "_")} -.->|"{label(o["trigger"])}"| O{i}')
    for i, row in enumerate(outcomes):
        case = ' / '.join(str(v) for v in row['case'].values()) or f'报告行 {row["evidence"]["row"]}'
        graph.append(f'  C{i}{{"多步案例 {label(case)}"}}')
        for source in row['sources']:
            graph.append(f'  {source.replace("-", "_")} -.->|"案例上下文"| C{i}')
        graph.append(f'  C{i} -.->|"实际最终落点"| {row["target"].replace("-", "_")}')
    md = ['# 当前导航与条件案例索引', '',
          f'覆盖114页、393条初态实际跳转、110个手动弹层入口，以及{len(outcomes)}个记录明确最终页面的业务案例。', '',
          '实线是初态单次操作的跨页结果；虚线弹层表示已观察入口；菱形表示多步案例及最终落点。共享案例关联多个控件时，不将最终页认定为每个控件的一次点击结果。', '',
          '[关系图](CURRENT_NAVIGATION_ATLAS.mmd)／[完整机器索引](evidence/current/navigation-atlas-20261101.json)／[逐控件业务规则](CURRENT_HIDDEN_CONTROL_BEHAVIORS.md)。', '',
          '每项保留原报告路径、行号和SHA256。报告没有明确终点的关闭、字段候选、筛选或本地状态另列，不猜测页面目标，也不将其认定为死路。此索引整理既有实际结果，没有重新运行浏览器。', '',
          '采集后HTML／JavaScript／资源的字节必须仍相同；CSS差异逐项保留旧／新指纹，结合[同值Token证明](CURRENT_STYLE_TOKEN_ADOPTION.md)及[照片热区修复](CURRENT_QUALITY_REFRESH.md)查阅。原报告不改绑。', '',
          '## 条件案例最终落点', '', '| 来源上下文 | 案例条件／操作 | 最终页 | 报告行 |', '| --- | --- | --- | --- |']
    for row in outcomes:
        case = ' / '.join(str(v) for v in row['case'].values()).replace('|', '／').replace('\n', ' ')
        ref = row['evidence']
        md.append(f'| {", ".join(row["sources"])} | {case} | {row["target"]} | [{ref["row"]}]({ref["report"]}) |')
    md += ['', f'另有{len(without_terminal)}个关联报告案例未记录明确最终URL，完整数据见机器索引。它们不能用于推断跨页导航。', '',
           '## 复验', '', '`python design-html/prototype/build_current_navigation_atlas.py --check`校验所有产物与来源报告、行号、通过状态和字节指纹；采集后的CSS只允许已登记同值替换与两条照片热区样式。Token行为等价性另运行`python design-html/prototype/verify_current_style_tokens.py`。', '',
           '完整41项目标仍在执行；此图补齐已观察证据的统一入口，不宣称所有条件组合、视觉差异或提交等待边界已经完成。', '']
    return {OUT: json.dumps(model, ensure_ascii=False, indent=2) + '\n', GRAPH: '\n'.join(graph) + '\n', DOC: '\n'.join(md)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for path, text in build().items():
        if args.check:
            assert path.read_bytes() == text.encode('utf-8'), path
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(text.encode('utf-8'))
    print('PASS navigation atlas:114 pages,393 initial click edges,110 overlay entries;case terminals retain exact report references')


if __name__ == '__main__':
    main()
