"""Publish a bounded lifecycle index after checking fresh browser results."""
import json
from collections import Counter
from pathlib import Path
from replay_current_overlay_lifecycle import ROOT, sha, dump
from verify_current_overlay_lifecycle import OUT, main as verify


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def main():
    verify(published=False)
    report = json.loads((OUT / 'results.json').read_text(encoding='utf-8'))
    rows = report['results']
    controls = []
    for observation in report['inventory']:
        i = observation['candidate_index']
        result_indices = [n for n, r in enumerate(rows) if r['candidate_index'] == i]
        for j, control in enumerate(observation['overlays'][0]['controls']):
            controls.append(dict(candidate_index=i, control_index=j, page=observation['page'],
                                 trigger=observation['label'], title=observation['overlays'][0]['title'],
                                 control=control, lifecycle_result_indices=result_indices,
                                 scope='Observed control and overlay lifecycle only. Selecting/submitting this business action is not proved by closure results.'))
    dump(OUT / 'controls.json', dict(report_sha256=sha(OUT / 'results.json'), controls=controls))
    counts = dict(entries=len(report['inventory']), cases=len(rows), passed=sum(r['passed'] for r in rows),
                  dirty=sum(r['dirty'] for r in rows), sheets=sum(r['sheet'] for r in report['inventory']),
                  editable_forms=sum(r['editable_submit'] for r in report['inventory']),
                  observed_control_appearances=len(controls), methods=dict(Counter(r['method'] for r in rows)),
                  groups=dict(Counter(c['group'] for c in report['candidates'])))
    doc = ['# 当前手动弹层入口与关闭保护', '',
           f"104个手动入口、{counts['cases']}项关闭案例通过：570项首轮成功保留，1项按实际按钮新执行；其中{counts['dirty']}项修改后关闭，覆盖{counts['editable_forms']}个可编辑提交表单。产品HTML/CSS/JS和资源未改。", '',
           '从114页初态合同选择104个明确Modal／Sheet入口，在当前201产品依赖上真实点击。初态合同只提供候选，不将其成功结果当成关闭结果；输入合同原字节、执行时源码及递归夹具均归档。', '',
           '每个入口检查Escape、安全取消／关闭按钮、遮罩、浏览器Back；Sheet另用真实鼠标指针拖动顶部把手110px。可编辑提交表单在每种关闭方式下先修改字段，再选择“继续编辑”并核对原输入，之后再次关闭并明确“放弃修改”。关闭后均核对原URL、完整localStorage和触发器焦点。', '',
           '执行环境：Chrome、390×844、zh-CN、Asia/Shanghai、减少动效；独立上下文和本地模拟数据。这里的Back是HTML历史栈验证，鼠标指针拖动不是实际手机触摸或Android系统返回验收。', '',
           '## 结果与复验', '',
           '[最终结果](evidence/current/overlay-lifecycle-20261031-final/results.json)／[隐藏控件出现索引](evidence/current/overlay-lifecycle-20261031-final/controls.json)／[汇总与指纹](evidence/current/overlay-lifecycle-20261031-final/summary.json)。', '',
           '[首轮571项](evidence/current/overlay-lifecycle-20261031/results.json)有1项测试助手错误：照片预览的安全按钮叫“返回阅读”，旧名单没有此名称，尚未执行点击就抛错。实际截图确认后，只补跑该按钮并验证页面、存储及焦点；原失败、截图及所有夹具保持原字节，不为测试修改产品。', '',
           '执行`python design-html/prototype/verify_current_overlay_lifecycle.py`检查当前源码、归档字节、104个实际入口、完整且不重复的关闭矩阵及逐项断言。采集器拒绝覆盖已有结果；如需新执行，应显式使用新的证据目录。', '',
           '## 逐入口对应', '',
           '| 序号 | 页面 | 触发控件 | 弹层标题 | 类型 | 可编辑提交表单 | 新执行案例 |',
           '| --- | --- | --- | --- | --- | --- | --- |']
    for observation in report['inventory']:
        i = observation['candidate_index']
        count = sum(r['candidate_index'] == i for r in rows)
        doc.append('| ' + ' | '.join(cell(v) for v in [i, observation['page'], observation['label'], observation['overlays'][0]['title'], 'Sheet' if observation['sheet'] else 'Modal', '是' if observation['editable_submit'] else '否', count]) + ' |')
    doc += ['', '## 范围与剩余', '',
            '本批观察隐藏控件并证明弹层关闭／未保存保护，不把关闭算成控件业务提交成功。嵌套选择、保存／删除的具体数据结果、提交竞争和其他种子条件需结合各专项证据继续核对。m08-p20自动打开的补页Sheet未计入104个手动入口，其初态关闭另见CURRENT_INITIAL_REPLAY；不因本批通过而声称所有条件已穷尽。', '',
            '旧250控件及回忆册V2的106次控件出现和业务结果仍保留原采集指纹，本批不重绑旧结果。原41项和七项交付继续，原稿视觉差异及人工验收0保持明确。', '']
    path = ROOT / 'CURRENT_OVERLAY_LIFECYCLE.md'
    path.write_text('\n'.join(doc), encoding='utf-8')
    dump(OUT / 'summary.json', dict(counts=counts, report_sha256=sha(OUT / 'results.json'),
                                  controls_sha256=sha(OUT / 'controls.json'), document_sha256=sha(path),
                                  producer_sha256=sha(Path(__file__)), verifier_sha256=sha(ROOT / 'verify_current_overlay_lifecycle.py'),
                                  human_accepted_pages=0))
    print(json.dumps(counts))


if __name__ == '__main__':
    main()
