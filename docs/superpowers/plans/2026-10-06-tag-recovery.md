# 标签原文保护与恢复实施计划

> 使用 superpowers:executing-plans 在当前独立worktree内执行；各步骤以实际浏览器证据验收。

**Goal:** 标签损坏不覆盖原文，提供明确恢复、原始副本及下载，保护普通编辑和关联记录事务。

**Architecture:** 在现有prototype-preferences.js维护标签分析与恢复，复用PrototypeUI组件及存储guard。设置页仅初始化真正缺失的集合；records副本列表增加标签类型，共享UI仅扩充副本前缀，不新建复杂状态框架。

**Tech Stack:** HTML/CSS/JavaScript、localStorage、现有Python Playwright验证工具。

**Spec:** design-html/prototype/TAG_RECOVERY_PLAN.md、ISSUES.md的I-03及本线程完整114页目标。

- [x] 运行verify_tag_recovery.py --baseline，保留源码和16项实际失败；检查原始内容变化。
- [x] 修改prototype-preferences.js标签读写、恢复与存储保护；prototype-settings.js缺失初始化；prototype-ui.js副本前缀、prototype-ui.css恢复按钮；prototype-records.js副本发现与说明。
- [x] 同一基线修复通过，加入配额、竞争、dirty输入、联合恢复、空/健康、五宽度和原文再次下载验证；修复实际失败后冻结源码。
- [x] 同源重跑声明设置/共享恢复/连续流程与114页观察，校验报告哈希、HTTP114页及37资产；归档被替换的旧证据。
- [x] 更新问题、组件、状态、导航、实施与测试说明；提交阶段成果。114页仍未完整验收，目标继续。

验证收尾：301项有名检查通过；228次观察、1,696个控件节点、51次条件重定向；HTTP114页及37资源一致。其余集合6次脚本错误保持开放，114页终验0页。
