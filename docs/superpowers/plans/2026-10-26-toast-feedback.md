# Toast可见性与操作避让 Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans inline; steps follow TDD.

**Goal:** 原生dialog打开时Toast可见；关键提交不被覆盖，关闭后剩余反馈继续显示。

**Architecture:** 复用现有Toast、原生dialog和2600ms计时。Toast挂到当前dialog的顶层子树，关闭时移回body；根据当前原生提交／busy／共享Primary及焦点按钮边界选择最近可用垂直位置。沿用现有色彩、字体、时长和返回／字段保护。

**Tech Stack:** 原生JavaScript／CSS、现有Python／Playwright与Chrome。

**Spec:** 原提示词11／31项、ACCEPTANCE_REQUIREMENTS的G4；截图与人工验收独立。

## 证据与决定

- 实际同源另一窗口修改回忆册，书名dialog打开时触发数据更新Toast。320／390×420下Toast在body，被原生dialog盖住；原位还与保存按钮重叠。原截图和几何在evidence/baseline/toast-layout。
- 真实日记编辑器中，320×844、390×420的长success／info也覆盖提交区域。
- 私有DOM探针将Toast移到dialog顶部，截图证明提示可见且不压住保存。选择复用现有节点并在关闭时交接，采用局部位置计算；这是原目标已授权的缺陷修复，输入、存储和业务回调保持。

## 文件职责

- assets/prototype-ui.js：Toast挂载／避让与dialog关闭交接。
- assets/prototype-ui.css：dialog内Toast的首选顶部位置。
- prototype/verify_toast_feedback.py：22项失败后转绿及真实计时检查。
- prototype/TOAST_FEEDBACK.md及ISSUES／41项表：复现、范围和验证记录。

## Task 1 — 保留失败证据

- [x] 12个页面布局合同、4个真实peer更新／关闭合同、2个真实保存交接、3类实际自动消失及1个更新替换，共22项执行。
- [x] 保留原UI源码、CSS、脚本、报告和失败截图；记录实际失败，不将诊断算通过。

## Task 2 — 最小修复

- [x] 添加私有Toast定位函数，复用已有原生提交／busy／共享Primary语义与当前焦点按钮，避让可见操作；有限视口内选择最近可用位置。
- [x] Toast挂到当前dialog或body；dialog内首选顶部；关闭后移回body再定位，计时不中断／不重启。
- [x] 原22项转绿，核对输入／存储保持和无新增脚本错误。

## Task 3 — 收敛验证与交付

- [x] 检查普通／减少动效、两宽度／两高度和保存／取消后反馈；查看修复后的真实截图。
- [x] 确认差异仅为Toast挂载、定位及关闭交接。旧报告和114截图保留原指纹，按影响范围保留；只复验受影响流程，不盲目全量重跑。
- [x] 更新G4和问题记录，提交并仅推送codex/design-html-rebuild。完整114页目标及G3/G5继续。

## 实际验证

10366退出1：22项14通过8失败；11299退出0：原22项全绿。41277退出0：8＋12关闭合同通过。差异AST核对eed576、报告绑定7eed45通过；其他UI语义及非Toast CSS保持。正式源码与证据随本计划同批提交，推送以实际Git回执为准。原完整目标继续，G3／G5未完成。
