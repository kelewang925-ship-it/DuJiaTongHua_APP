# 流程测试报告（阶段证据，未最终验收）

> 本文全页观察与初始控件证据截至 aed142d 阶段。后续登录/邀请恢复改变了共享源码；当前专项及声明回归见 [登录/邀请实施记录](SESSION_INVITE_IMPLEMENTATION.md)，本文旧指纹不代表最新全页验收。

此前完整观察源码指纹：`9ad1a540e95bfe58f15c28708317235dc1bec81d1fb323ddef4cd365b7fceaa0`。114页最终验收仍为0页；本报告分开记录全页观察与本批实际操作，不将事件绑定、候选出口或历史阶段结果计为已完成完整产品流程。

## 最新专项及声明回归

登录/邀请恢复与验证码完整性阶段：50项有名检查全部通过（专项15、个人/关系20、正常注册/关系8、连续新用户2、设置5），114页和37共享资产HTTP与工作区文件一致。结果和最新源码指纹见evidence/current/session-invite-checkpoint.json；不包括最新源码的全114页动态观察/82+14控件重跑。

## 此前完整观察证据

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
| m01 | 8 | 92 | 50 | 未完成 |
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

21项专项检查通过：12项数据与恢复保护、4个跨模块读取入口、5种宽度/安全区。检查实际原始下载、保留副本、容量失败、并发更新和未保存输入；不以成功Toast代替数据断言。日记4项/照片3项属于前阶段，原始记录恢复checkpoint保留在evidence/history/pre-archive-history-5ea93bf；本阶段设置5项/回忆册4项及其他当前回归见account-recovery-checkpoint.json。

副本历史导出UI见RECOVERY_ARCHIVES_IMPLEMENTATION.md；其他存储集合和所有114页恢复状态仍待补齐。详见RECORD_RECOVERY_IMPLEMENTATION.md；这不是全部数据恢复完成或全产品验收。

## 个人/关系资料恢复

20项专项通过：null、坏JSON、错误根结构与字段恢复、原始文件下载、容量失败、并发变更、未保存昵称、事务写入保护、三类数据连续恢复、历史下载及5种宽度。个人/关系问题存在时暂停普通保存，恢复原始副本可继续保存；正常资料不受此限制。

当前账号8项、新用户2项、设置5项、记录21项、副本15项、宠物3项、回忆册4项、工坊3项及82+14账号控件/弹层共177项有名检查见account-recovery-checkpoint.json；日记4项等前阶段报告按自身源码哈希解释，不升级为本阶段结果。会话、邀请码和其他集合恢复仍未完成。详见ACCOUNT_RECOVERY_IMPLEMENTATION.md。

## 时刻册与留言后续执行

最新6页声明fixture的44个初始可用控件、隐藏删除/回应/日期/失败重试及回应dirty保护见[MOMENT_CONTROL_EXECUTION](MOMENT_CONTROL_EXECUTION.md)。对应最新源码和67项专项/回归见evidence/current/moment-controls-checkpoint.json。旧全页观察、旧账号代表控件及上阶段50项汇总保持历史来源；不代表本批最新全114页检查。

## 首页、日记与照片后续执行

最新12页声明fixture的92个初始可用控件、9组隐藏操作、回应离开/权限/日期/搜索专项及10项宽度检查见[RECORD_CONTROL_EXECUTION](RECORD_CONTROL_EXECUTION.md)。最新源码和195项有名检查见evidence/current/record-controls-checkpoint.json。此前全页扫描与其他模块历史控件结果不计作本批最新全产品验收，114页终验仍为0。
