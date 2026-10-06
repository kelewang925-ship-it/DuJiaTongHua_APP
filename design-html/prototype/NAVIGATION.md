# 导航关系与执行证据（持续实施）

工坊取消生成慢加载重复导航已复现并修复：确认后保持定时器暂停，成功保存只跳编辑一次；失败保持生成页，重试取消或明确继续后推进。外部修复作品后错误CTA重新打开当前URL。 具体证据与边界见[WORK_ERROR_IMPLEMENTATION](WORK_ERROR_IMPLEMENTATION.md)。

作品恢复保持同URL及现有guard；编辑中恢复后选择继续编辑，输入保留并可正常暂存。联合资料／记录／作品损坏优先发现并顺序恢复；副本历史仍由数据与存储进入，不导入当前作品。当前44项专项和声明回归见[WORKSHOP_RECOVERY_IMPLEMENTATION](WORKSHOP_RECOVERY_IMPLEMENTATION.md)，浏览器history模拟不等同于Android原生返回实测。

共享Danger变体保留原取消／关闭协议；14类普通确认分别执行Escape、遮罩、浏览器返回，底层地址与存储保持，直接入口恢复触发焦点。恢复数据最终取消返回恢复选项；Dirty Sheet继续编辑保持输入。最新阶段见[DANGER_COMPONENT_IMPLEMENTATION](DANGER_COMPONENT_IMPLEMENTATION.md)，不替代其他历史路径全量终验。

当前时间流程实际轨迹见time-product-journey-results.json：正常/空时刻册“共同提醒”→m04-p05（无内容条件转m04-p06）；当天纪念日实际共同记录→m03-p08?id；纪念日/胶囊保存成功消费编辑guard历史，顶部按上级返回。按钮、浏览器返回和Enter入口证据见TIME_PRODUCT_JOURNEY_IMPLEMENTATION.md及time-journey-checkpoint.json；其他任务的全部来源条件仍待终验。

当前连续操作实际遍历m01～m08，轨迹见product-journey-results.json；结果页m05-p08→创作列表m05-p09→工坊m05-p01的完成任务返回已经修复并执行4项专项。回忆册管理m08-p21从阅读工具m08-p17进入时返回该原入口。详见[PRODUCT_JOURNEY_IMPLEMENTATION](PRODUCT_JOURNEY_IMPLEMENTATION.md)。以下aed142d表保持历史来源，不能替代当前所有来源/状态/返回的全量终验。

> 本文全页观察与初始控件证据截至 aed142d 阶段。后续登录/邀请恢复改变了共享源码；当前专项及声明回归见 [登录/邀请实施记录](SESSION_INVITE_IMPLEMENTATION.md)，本文旧指纹不代表最新全页验收。

源码指纹：`9ad1a540e95bfe58f15c28708317235dc1bec81d1fb323ddef4cd365b7fceaa0`。完整页面类型见PAGE_CATALOG.md；618条回调引用候选和50次条件重定向见CURRENT_NAVIGATION.md。动态ID、数字拼接和条件结果仍需补全；本文件不宣称完整导航终验。

## 本批实际执行的初始入口

有效提交前置条件见CONTROL_BEHAVIORS.md。返回按钮在直接进入页面的上下文验证fallback，不能由此证明从所有来源进入后的历史返回。

| 来源页 | 控件 | 触发契约 | 实际落点 | 结果 |
| --- | --- | --- | --- | --- |
| m01-p01 | 登录并开始 | route:m01-p02 | m01-p02 | 通过 |
| m01-p01 | 创建账号 | route:m01-p03 | m01-p03 | 通过 |
| m01-p02 | 返回 | route:m01-p01 | m01-p01 | 通过 |
| m01-p02 | 忘记密码？ | route:m01-p04 | m01-p04 | 通过 |
| m01-p02 | 登录并回到故事里 | login:m02-p01 | m02-p01 | 通过 |
| m01-p02 | 创建账号 | route:m01-p03 | m01-p03 | 通过 |
| m01-p03 | 返回欢迎页 | route:m01-p01 | m01-p01 | 通过 |
| m01-p03 | 创建账号 | register:m01-p07 | m01-p07 | 通过 |
| m01-p03 | 去登录 | route:m01-p02 | m01-p02 | 通过 |
| m01-p04 | 返回 | route:m01-p02 | m01-p02 | 通过 |
| m01-p04 | 下一步 | recovery:m01-p07 | m01-p07 | 通过 |
| m01-p04 | 返回登录 | route:m01-p02 | m01-p02 | 通过 |
| m01-p05 | 返回找回密码 | route:m01-p04 | m01-p04 | 通过 |
| m01-p05 | 确认并重置 | reset:m01-p08 | m01-p08 | 通过 |
| m01-p06 | 返回 | route:m01-p02 | m01-p02 | 通过 |
| m01-p06 | 再试一次 | retry:m02-p01 | m02-p01 | 通过 |
| m01-p06 | 找回密码 | route:m01-p04 | m01-p04 | 通过 |
| m01-p07 | 返回 | route:m01-p04 | m01-p04 | 通过 |
| m01-p07 | 验证并继续 | verify:m01-p05 | m01-p05 | 通过 |
| m01-p08 | 返回登录 | route:m01-p02 | m01-p02 | 通过 |
| m02-p01 | 返回登录 | route:m01-p02 | m01-p02 | 通过 |
| m02-p01 | 邀请 TA 加入 生成专属邀请码 | route:m02-p02 | m02-p02 | 通过 |
| m02-p01 | 输入 TA 的邀请码 接受一份特别邀请 | route:m02-p03 | m02-p03 | 通过 |
| m02-p02 | 返回建立关系 | route:m02-p01 | m02-p01 | 通过 |
| m02-p03 | 返回 | route:m02-p01 | m02-p01 | 通过 |
| m02-p03 | 查看邀请内容 | invite:m02-p04 | m02-p04 | 通过 |
| m02-p03 | 请让 TA 分享给你 | route:m02-p01 | m02-p01 | 通过 |
| m02-p04 | 返回 | route:m02-p03 | m02-p03 | 通过 |
| m02-p04 | 确认建立关系 | bind:m02-p05 | m02-p05 | 通过 |
| m02-p04 | 暂不接受 | cancel:m02-p01 | m02-p01 | 通过 |
| m02-p05 | 去写第一篇共同日记 ♡ | route:m03-p05 | m03-p05 | 通过 |
| m02-p05 | 完善情侣资料 | route:m02-p06 | m02-p06 | 通过 |
| m02-p05 | 先逛逛我们的首页 | route:m03-p01 | m03-p01 | 通过 |
| m02-p06 | 返回 | route:m02-p05 | m02-p05 | 通过 |
| m02-p06 | 保存小资料 | profile:m02-p01 | m02-p01 | 通过 |
| m02-p07 | 返回邀请卡 | route:m02-p02 | m02-p02 | 通过 |
| m02-p08 | 请 TA 重新邀请 | renew:m02-p01 | m02-p01 | 通过 |
| m02-p08 | 重新输入邀请码 | route:m02-p03 | m02-p03 | 通过 |
| m02-p09 | 回到我们的首页 | route:m03-p01 | m03-p01 | 通过 |
| m02-p09 | 查看关系设置 | route:m02-p06 | m02-p06 | 通过 |

## 弹层后的实际导航

| 来源页 | 操作 | 实际落点 | 结果 |
| --- | --- | --- | --- |
| m01-p07 | verify-phone | m01-p04 | 通过 |
| m02-p02 | share-wait | m02-p07 | 通过 |

## 五Tab与返回规则

首页→m03-p02、重要时刻→m04-p01、工坊→m05-p01、宠物→m07-p03、我的→m06-p01；空数据或等待领养由控制器决定实际页。Tab使用replace，详情和完整编辑任务使用页面导航，局部选择使用Sheet，危险决策使用Modal。实际行为及未保存规则见INTERACTION_RULES.md；已有五Tab运行证据见PRIMARY_NAVIGATION_IMPLEMENTATION.md，不自动计入本批控件数量。

## 未闭环

其余模块动态列表条目、全部隐藏弹层、私密与已删除引用、任务提交后历史/BFCache、错误重试后的落点与全部一级入口返回仍需实际执行。旧候选图的无入边不是死路证明。完整产品首次使用串行终验和原生端返回都未完成。

## 时刻册与留言后续执行

最新6页声明fixture的44个初始可用控件、隐藏删除/回应/日期/失败重试及回应dirty保护见[MOMENT_CONTROL_EXECUTION](MOMENT_CONTROL_EXECUTION.md)。对应最新源码和67项专项/回归见evidence/current/moment-controls-checkpoint.json。旧全页观察、旧账号代表控件及上阶段50项汇总保持历史来源；不代表本批最新全114页检查。

## 首页、日记与照片后续执行

最新12页声明fixture的92个初始可用控件、9组隐藏操作、回应离开/权限/日期/搜索专项及10项宽度检查见[RECORD_CONTROL_EXECUTION](RECORD_CONTROL_EXECUTION.md)。最新源码和195项有名检查见evidence/current/record-controls-checkpoint.json。此前全页扫描与其他模块历史控件结果不计作本批最新全产品验收，114页终验仍为0。

## 回忆册逐项操作阶段

21页154个初始控件的操作合同与实际出口见BOOK_CONTROL_EXECUTION.md。补页编辑直接入口的顶部返回指向补页选择，保留当前册/页ID；脏输入需继续或确认放弃。114页已建立分阶段初始契约，全部隐藏分支及当前全产品验证仍待完成。
