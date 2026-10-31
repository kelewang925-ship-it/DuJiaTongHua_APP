"""Publish readable behavior contracts without overstating observed coverage."""
import json
from pathlib import Path
from replay_current_initial_controls import ROOT, sha, dump
from complete_current_hidden_business import OUT as FINAL
from replay_current_hidden_business import OUT as RAW
from replay_current_hidden_pickers import OUT as PICKERS
from verify_current_hidden_business import main as verify


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def main():
    verify(published=False)
    data = json.loads((FINAL / 'results.json').read_text(encoding='utf-8'))
    index = json.loads((FINAL / 'control-business-index.json').read_text(encoding='utf-8'))
    lines = ['# 当前隐藏操作的实际业务结果', '',
             '当前源码下核对231个业务案例、50个选择器／字段案例，以及1个“不填写生日”保存失败重试案例，共282项通过。另补充6个宠物目录解锁Sheet的30项关闭检查（Escape、安全按钮、遮罩、浏览器Back、拖动各6项）。产品HTML、CSS、JavaScript与资源未改。', '',
             '110个已观察弹层中302次控件出现（301可用、1禁用）已逐项关联实际关闭或业务结果，未对应0。这里不是302次全新业务点击：书库、章节、页序及目录共用路径使用明确的具名数据变体，逐行保留对应类型。', '',
             '## 业务检查', '',
             '| 套件 | 案例 | 结果来源 |', '| --- | --- | --- |']
    for suite in data['results']:
        path = ROOT / suite['retained_from'] if suite.get('retained_from') else FINAL / suite['script'].removesuffix('.py') / suite['report']
        lines.append(f"| {suite['script']} | {suite['cases']}通过 | [实际结果]({path.relative_to(ROOT).as_posix()}) |")
    lines += ['', '前八组108项来自本批首轮成功结果，后四组123项实际新执行，产品依赖完全一致。回忆册章节13项这次全部执行，没有沿用旧报告中的12项历史保留。选择器另执行五宽度50项，生日清空另执行1项。', '',
              '保存检查涵盖明确存储谓词、重复提交、空值、真实容量失败后保留及重试；删除检查涵盖目标集合、其他记录／资料保持、语义失败、容量失败及二层身份确认。解锁检查核对资源扣除、所有权、父页保存后装备／布置。选择器应用只更新候选，取消保留原值；生日清空还检查父页保存失败、重试、重新打开及其他资料保持。', '',
              '## 当前盘点与对应', '',
              '[302行可读行为清单](CURRENT_HIDDEN_CONTROL_BEHAVIORS.md)／[机器可读索引](evidence/current/hidden-business-20261101-final/control-business-index.json)／[业务执行汇总](evidence/current/hidden-business-20261101-final/results.json)／[选择器执行汇总](evidence/current/hidden-pickers-20261101/execution.json)。', '',
              '新增范围来自实际差异：旧隐藏盘点的6个宠物解锁入口已重建；当前初态合同用catalog分类，不能仅靠sheet/modal分类收齐。因此按当前目录ID点击并观察，再验证4种关闭方式，并按实际Sheet类型另补6项拖动。5个日期／生日选择器也逐项进入当前对应表。104个明确Modal/Sheet入口的既有571项关闭证据保持，见CURRENT_OVERLAY_LIFECYCLE。', '',
              '## 保留的采集诊断', '',
              '首轮8组108项通过，编辑选择器18项尚未执行就被依赖校验拦下：新组装输入误把201个全项目依赖放入只接受63个回忆册依赖的字段。原诊断保持在hidden-business-20261101/verify_book_v2_hidden_editors/runner-error.txt。后续用当前201归档中的确切63依赖子集，保留相同31个实际观察，才新执行18项。没有改产品或绕过原断言。', '',
              '历史250控件和V2 106次控件出现表仅提供语义与具名变体对应；所有当前结果引用均指向本批真实执行或当前关闭报告，旧报告和指纹保持原貌。', '',
              '## 复验与边界', '',
              '运行`python design-html/prototype/verify_current_hidden_business.py`核对201产品依赖及归档、全部夹具、108／123来源、282实际结果、30额外关闭、302行唯一性和每条证据的SHA及通过状态。Chrome独立上下文、本地mock、减少动效；主业务390×844，选择器另覆盖320/360/390/414/430。', '',
              '范围是本批实际观察的110个弹层及明确具名业务分支，仍需结合跨窗口／提交竞争／其他条件专项及原41项完成审计。自动弹层、未出现的其他种子组合、真实Android系统返回／IME／触摸及读屏不由此推断通过。原稿视觉差异继续核对；人工验收保持0，完整目标未结束。', '']
    summary_doc = ROOT / 'CURRENT_HIDDEN_BUSINESS.md'
    summary_doc.write_text('\n'.join(lines), encoding='utf-8')
    evidence = {}
    for item in index['items']:
        for ref in item['business_evidence']:
            key = (ref['report'], ref['row'])
            if key not in evidence:
                evidence[key] = len(evidence)
    lines = ['# 当前隐藏控件行为清单', '',
             '从110个实际观察弹层登记302次控件出现。每行说明当前行为并指向通过的实际结果；字段和禁用项一并列出。相同业务谓词可证明多个字段，具名书页变体的复用路径保留标记，不能把表行数当成独立业务点击数。版本、采集诊断与边界见[CURRENT_HIDDEN_BUSINESS](CURRENT_HIDDEN_BUSINESS.md)。', '',
             '| 页面 | 弹层 | 触发控件 | 隐藏控件 | 实际行为 | 对应范围 | 证据编号 |',
             '| --- | --- | --- | --- | --- | --- | --- |']
    for item in index['items']:
        scope = '具名数据变体的共享路径' if item['mapping_kind'].startswith('shared-') else '当前实际结果'
        if item['control']['disabled']:
            scope += '；禁用项'
        refs = ', '.join(str(evidence[(r['report'], r['row'])]) for r in item['business_evidence'])
        lines.append('| ' + ' | '.join(cell(v) for v in [item['page'], item['title'], item['trigger'], item['control']['label'], item['business_contract'], scope, refs]) + ' |')
    lines += ['', '## 证据编号', '', '| 编号 | 原始报告 | 结果行（从0开始） |', '| --- | --- | --- |']
    for (path, row), number in evidence.items():
        lines.append(f'| {number} | [报告]({path}) | {row if row is not None else "独立案例"} |')
    lines.append('')
    control_doc = ROOT / 'CURRENT_HIDDEN_CONTROL_BEHAVIORS.md'
    control_doc.write_text('\n'.join(lines), encoding='utf-8')
    dump(FINAL / 'publishing.json', dict(summary_document_sha256=sha(summary_doc), controls_document_sha256=sha(control_doc),
         index_sha256=sha(FINAL / 'control-business-index.json'), producer_sha256=sha(Path(__file__)), verifier_sha256=sha(ROOT / 'verify_current_hidden_business.py'),
         business_cases=231, picker_cases=50, birthday_cases=1, extra_closes=30, overlays=110, control_appearances=302, human_accepted_pages=0))
    print('Published current business summary and302 readable behavior contracts')


if __name__ == '__main__':
    main()
