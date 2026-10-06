# 时刻册与留言控件执行记录

本文件53项／44初始控件为历史阶段数量。此前新增两处共同提醒入口已补入当前契约，当前6页46个初始控件／9项隐藏实际执行；最新同源范围见[时刻／纪念日／胶囊恢复实施记录](TIME_COLLECTION_RECOVERY_IMPLEMENTATION.md)。

源码指纹：`b2746831b4f83ae34a5a04f75c65640a4b1a53a272cf11198cbdc9ab7125fc80`。6页各一个声明fixture的全部44个初始可用控件；不代表全部数据条件或全产品验收。原始节点与执行结果见evidence/current/moment-controls-results.json。

| 页面/场景 | 控件 | 实际契约 | 结果 |
| --- | --- | --- | --- |
| m04-p01/populated | 查看纪念日 | route:m04-p07 | 通过 |
| m04-p01/populated | 珍藏一个新时刻 | route:m04-p04 | 通过 |
| m04-p01/populated | 查看全部 › | expand | 通过 |
| m04-p01/populated | 共同重要时刻 / 2026-10-04 | route:m04-p03 | 通过 |
| m04-p01/populated | 纪念日 | route:m04-p07 | 通过 |
| m04-p01/populated | 时光胶囊 | route:m04-p12 | 通过 |
| m04-p01/populated | 悄悄留言 | route:m04-p16 | 通过 |
| m04-p01/populated | 新建重要时刻 | route:m04-p04 | 通过 |
| m04-p01/populated | 刷新时刻册 | refresh | 通过 |
| m04-p01/populated | 首页 | nav:m03-p02 | 通过 |
| m04-p01/populated | 重要时刻 | nav:self | 通过 |
| m04-p01/populated | 工坊 | nav:m05-p01 | 通过 |
| m04-p01/populated | 宠物 | nav:pet | 通过 |
| m04-p01/populated | 我的 | nav:m06-p01 | 通过 |
| m04-p02/empty | 从共同记录中收录 | collect-empty | 通过 |
| m04-p02/empty | 新建重要时刻 | route:m04-p04 | 通过 |
| m04-p02/empty | 纪念日 | route:m04-p08 | 通过 |
| m04-p02/empty | 时光胶囊 | route:m04-p12 | 通过 |
| m04-p02/empty | 悄悄留言 | route:m04-p17 | 通过 |
| m04-p02/empty | 首页 | nav:m03-p01 | 通过 |
| m04-p02/empty | 重要时刻 | nav:self | 通过 |
| m04-p02/empty | 工坊 | nav:m05-p01 | 通过 |
| m04-p02/empty | 宠物 | nav:pet | 通过 |
| m04-p02/empty | 我的 | nav:m06-p01 | 通过 |
| m04-p03/populated | 返回重要时刻 | route:m04-p01 | 通过 |
| m04-p03/populated | 共同日记 | route:m03-p08 | 通过 |
| m04-p03/populated | 悄悄留言 1 条 | sheet:时刻回应 | 通过 |
| m04-p03/populated | 编辑时刻 | route:m04-p04 | 通过 |
| m04-p03/populated | 更多操作 | sheet:时刻操作 | 通过 |
| m04-p04/empty | 返回重要时刻 | route:m04-p02 | 通过 |
| m04-p04/empty | 添加封面 | file | 通过 |
| m04-p04/empty | name | input | 通过 |
| m04-p04/empty | 发生日期 | sheet:发生日期 | 通过 |
| m04-p04/empty | type | input | 通过 |
| m04-p04/empty | type | input | 通过 |
| m04-p04/empty | type | input | 通过 |
| m04-p04/empty | type | input | 通过 |
| m04-p04/empty | 记录这个时刻背后的故事… | input | 通过 |
| m04-p04/empty | 关联共同记录，已选 0 条 | modal:选择共同记录 | 通过 |
| m04-p04/empty | 保存到时刻册 | save | 通过 |
| m04-p16/populated | 返回重要时刻 | route:m04-p01 | 通过 |
| m04-p16/populated | 查看原记录 | read-reply | 通过 |
| m04-p17/empty | 返回重要时刻 | route:m04-p02 | 通过 |
| m04-p17/empty | 去看看共同记录 | route:m03-p06 | 通过 |

契约说明：route按业务进入目标页面；nav包含主导航replace、当前Tab滚回顶部和宠物前置状态redirect；input包含文字长度上限和类型标签/键盘选择；file实际触发文件选择并预览；save写入后返回列表；read-reply保存已读后进入原时刻；modal/sheet确认标题、关闭、焦点回到入口；expand展开/收起；refresh加载禁用后恢复列表；collect-empty进入编辑器再打开无共同记录出口。

## 隐藏分支

删除取消/失败/重试且不删关联记录；回应失败保留/重试成功；关闭回应隐私；日期回填及编辑器dirty；列表加载失败/重试。回应输入后取消、Escape、浏览器返回、拖动均确认继续/放弃并还原焦点；五宽度检查安全区、按钮44px与300字限制。

## 复现及诊断

baseline/moment-controls-results.json保留原源码的4种回应关闭失败，输入直接丢失。修复复用protectSheet，不新增状态架构；发送失败不提交，成功后commit再关闭。baseline/moment-radio-observer-error.json的3项失败是测试直接点击pointer-events:none的原生radio，修正为实际label点击并检验键盘Space；baseline/moment-state-fixture-errors.json的两项失败是旧fixture私密回应缺少author触发正确资料恢复、空列表出口错误期待正常列表。诊断不计作产品缺陷。五宽度截图见evidence/current/moment-reply-discard-*.png。

## 边界

全114页动态分支仍待执行；其余91页初始控件契约待完善，历史账号17页和本批6页的代表性控件不等于23页最终验收。时刻集合损坏与引用异常、更多数据条件、照片/日记回应dirty、重要删除DangerButton、跨模块连续流程仍开放。此前完整全页扫描属于aed142d；上阶段50项登录/邀请检查属于94a7065，未重跑为本批结果。
