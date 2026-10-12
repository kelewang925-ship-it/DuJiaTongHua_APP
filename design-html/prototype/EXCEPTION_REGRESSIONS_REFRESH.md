# 工坊、回忆册与时间异常回归

本批保持114份HTML和37份prototype资源的151份源码指纹不变。实际父进程49665及73382退出0，16份子报告全部退出0、全部案例通过。完整原型目标继续，最终验收0页。

## 已执行范围

| 批次 | 检查数 | 边界 |
| --- | ---: | --- |
| 工坊／回忆册 | 32 | 素材失败重试、生成取消与配额失败、任务返回、册全局规则、创建日期与首页计数 |
| 时间模块 | 131 | 纪念日／胶囊创建编辑删除、封存门槛、收集回滚、提醒、设置弹层、任务返回与布局 |
| 其中重复初始控件 | 54 | 属于已有752初始控件；不增加覆盖数量 |
| 其中布局 | 35 | 7页×5宽度，不能外推至114页及全部动态状态 |

## 实际报告清单

| 报告 | 通过数 |
| --- | ---: | --- |
| workshop-flow-results.json | 3/3 |
| workshop-state-results.json | 8/8 |
| book-global-results.json | 6/6 |
| workshop-task-return-results.json | 4/4 |
| book-created-date-results.json | 5/5 |
| home-counter-results.json | 6/6 |
| anniversary-flow-results.json | 3/3 |
| anniversary-state-results.json | 7/7 |
| capsule-flow-results.json | 3/3 |
| capsule-state-results.json | 5/5 |
| time-collection-results.json | 7/7 |
| settings-sheet-guard-results.json | 11/11 |
| time-controls-results.json | 54/54 |
| time-layout-results.json | 20/20 |
| time-entry-layout-results.json | 15/15 |
| time-task-return-results.json | 6/6 |

## 初始报告引用修正

发现旧检查点／页面目录引用的time-controls报告哈希d1d6…与已提交报告ebd917…不一致，原文和已提交字节均已保存在history/pre-exception-regressions-12efee3。无法用旧引用确认那份报告。本次实际54项执行全部通过，报告6c2844…现用于目录与初始检查点。remaining-initial-refresh-source显式记录73382刷新执行，原83928保留其他五模块批次来源；没有重新宣称执行整个615项批次。

## 尚未完成

failure-operation-candidates.json是源码清单：65处字面量调用、61个不同操作名及4处动态入口。源码中存在失败钩子不能证明对应错误、取消、重试、结果或权限状态已经执行。本批只能证明上表命名脚本实际案例。

下一阶段对61个操作及动态调用逐项对应实际案例，执行缺口；补齐图片失败、权限与来源变化、提交中退出、键盘／可访问性／安全区和114页布局。保持未执行项明确标记，避免重复运行已经充分验证的同一层。

## 校验方式

verify_fresh_exception_regressions.py核对报告字节、各子脚本、源码指纹、执行退出记录及实际HTTP提供的151份产品字节。build_page_contracts、verify_consolidated_initial_replay与verify_page_contracts核对目录引用与752初始控件。所有flow_verified仍false。
