# 流程测试报告（阶段证据，未最终验收）

副本历史阶段说明：最近一次完整114页观察及账号执行来自5ea93bf的源码；新增原始副本入口、隐藏弹层与下载按RECOVERY_ARCHIVES_IMPLEMENTATION.md专项验证。本表未升级为新增源码的全页验收。

当前源码指纹：`e35ee44d89a9140816cb1ee9e6ed49988b7133e59869cec4bf1a3a15b7d0e69b`。114页最终验收仍为0页；本报告分开记录全页观察与本批实际操作，不将事件绑定、候选出口或历史阶段结果计为已完成完整产品流程。

## 当前证据

| 检查 | 数量 | 结果与边界 |
| --- | ---: | --- |
| 全页空／有数据观察 | 228 | 114个请求页各两次；脚本/观察错误0，无绑定/委托候选0。不执行所有事件 |
| 初始账号／关系控件 | 82 | 82通过；17页当前空态所有可用初始控件，一个声明前置条件/代表性操作 |
| 隐藏弹层与重发 | 14 | 14通过；协议确认、验证方式、剪贴板、实际下载、分享等待、日期回填/取消/未保存保护及重发恢复 |
| 导航回调引用候选 | 618 | 包含fallback和条件分支，候选数量不代表已走通路径数量 |
| 条件重定向 | 50 | 保留请求与实际落点；未进入的原状态仍需特定条件触发 |

本批实际操作数量以当前两类结果表为准，重复运行不重复累计。最初分享下载探测使用了全页同名按钮选择器，发生观察器strict-mode错误，修正为当前dialog范围后通过；原错误保留在baseline/onboarding-overlay-observer-error.json，不算产品缺陷。

## 各模块覆盖边界

| 模块 | 页面数 | 当前空／有数据观察节点记录 | 本批初始控件实际执行 | 全部页面验收 |
| --- | ---: | ---: | ---: | --- |
| m01 | 8 | 102 | 50 | 未完成 |
| m02 | 9 | 64 | 32 | 未完成 |
| m03 | 12 | 190 | 0 | 未完成 |
| m04 | 17 | 199 | 0 | 未完成 |
| m05 | 10 | 189 | 0 | 未完成 |
| m06 | 12 | 166 | 0 | 未完成 |
| m07 | 25 | 450 | 0 | 未完成 |
| m08 | 21 | 333 | 0 | 未完成 |

其余模块已有模块实施记录与历史流程证据，本批列为0仅表示本批尚未逐控件执行，不表示没有实现。源文件哈希不同的历史报告不直接升级为当前全产品验收。

## 未完成的最终门槛

- 114页每个控件全部适用状态、动态列表条目、Modal/Sheet及真实导航完整契约与执行。
- 首次内容主线之外的退出再登录、其他集合与宠物/工坊/回忆册跨模块连续闭环。
- 破损数据、图片/加载/保存/生成失败的可恢复性，保留有效数据和未提交输入。
- 全部任务来源、提交后历史、快速返回、缓存恢复与弹层优先级；浏览器证据不等于Android原生验证。
- 当前版本全部状态的五宽度、长输入、热区、滚动、键盘、安全区、视觉与访问性验证。

复查脚本：audit_current_runtime.py、build_current_catalog.py、verify_onboarding_controls.py、verify_onboarding_overlays.py、build_execution_catalog.py。脚本依赖当前本地8765预览、独立Chrome与已配置Python/Playwright环境。最后两类结果必须与当前运行源码哈希匹配，不跳过失败行；详细原始结果保留于evidence/current。

## 无预置业务数据的连续用户流程

| 流程 | 实际步骤 | 结果 |
| --- | --- | --- |
| new-user-continuous-registration-binding-diary-crud | fresh-welcome → registered → bound → first-empty-home → first-save-failed-input-kept → first-saved-list → first-detail → edited-and-reloaded → updated-home → deleted-list → empty-home-after-delete | 通过 |
| diary-created-list-home-return | return-contract-saved → return-contract-home | 通过 |

其中一条使用全新浏览器、用户注册/验证码/绑定后从成功页进入空首页，实际创建、查看、编辑、刷新、返回、取消删除、确认删除和空首页恢复；另一条单独复查创建后列表返回首页。未预置业务集合，未使用直接跳转串接步骤。具体源码及页面/记录数量见new-user-journey-results.json。这两条不是全模块连续终验；详见NEW_USER_JOURNEY_IMPLEMENTATION.md。

## 日记与照片记录损坏恢复

21项专项检查通过：12项数据与恢复保护、4个跨模块读取入口、5种宽度/安全区。检查实际原始下载、保留副本、容量失败、并发更新和未保存输入；不以成功Toast代替数据断言。日记4项、照片3项、设置5项、回忆册4项正常回归另见record-recovery-checkpoint.json。

副本历史导出UI已由后续专项补齐；其他存储集合和所有114页恢复状态仍待补齐。详见RECORD_RECOVERY_IMPLEMENTATION.md；这不是全部数据恢复完成或全产品验收。

## 原始副本历史入口专项

15项副本专项、21项恢复回归、5项设置回归共41项检查通过。实际原始下载不写主集合；普通导出和共同备份不包含原始副本，清缓存保留、注销清除。源码哈希与151文件HTTP一致性见recovery-archive-checkpoint.json，细节见RECOVERY_ARCHIVES_IMPLEMENTATION.md。最近一次完整观察的源码早于此改动，最终验收0页。
