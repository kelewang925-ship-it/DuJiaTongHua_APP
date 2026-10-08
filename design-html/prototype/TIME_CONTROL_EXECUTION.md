# 提醒、纪念日与胶囊控件执行

当前11页54个初始时间控件继续使用既有fixture；异常胶囊日期新增修正入口作为专项动态分支。开启／提醒提交使用当前数据，收录正确关联与private范围另有专项；完整其他状态验收继续。 详见[胶囊日期与收录关联](CAPSULE_SEMANTIC_RECOVERY_IMPLEMENTATION.md)。

## 范围与结果

m04-p05 至 m04-p15 的11页声明fixture，54个初始可用控件全部按明确契约实际执行；由报告计算：54个控件、7项额外操作、20项五宽度弹层检查、18项已有流程/异常回归，共99项通过。

测试日期2026-10-05是显式fixture，真实执行日期为2026-10-06；两者不同。纪念日repeat为boolean、enabled为boolean、reminderDays为number；当天和未来使用独立稳定ID。胶囊包含草稿/封存/开启三种数据，封存内容在未到期时不显示。所有测试只改隔离浏览器context的数据。

## 已修复问题

胶囊收录原先先写重要时刻、再更新胶囊；第二次写入空间不足时留下半完成的时刻。baseline/time-controls-results.json保留修复前失败。现在复用PrototypePreferences.transaction，先更新胶囊关系、再写新增时刻，并在写入失败时回滚。两种集合分别模拟QuotaExceededError，失败保持原内容与当前页，重试进入正确稳定ID；再收录不会重复生成。既有transaction的回滚依赖浏览器仍允许恢复旧值；本轮不声称支持同时拒绝所有写入的故障。baseline/time-observer-restore-results.json是恢复Storage方法时观察器返回函数导致的Illegal invocation诊断，已经改为不返回函数。

## 指定隐藏状态与回归

新增7项：两种集合写入失败/回滚/重试/重复收录，纪念日及胶囊编辑器各自按钮和浏览器返回继续/放弃4项，提醒已读写入失败保持未读/不跳转、重试后单条已读1项。既有18项重新运行，覆盖纪念日新建/关联/修改/删除、保存失败及dirty、今天关联日记、闰年/过期、开关/加载/删除失败、日期取消/长输入/空间不足、提醒已读/空态/失效、刷新后删除；胶囊草稿/封存/开启/收录、图片/长输入/过期/缺失/失败重试。

五宽度320/360/390/414/430px，在34px安全区下检查纪念日/胶囊日期Sheet和两类删除Modal的可达性及44px按钮高度；Escape关闭不写数据。人工查看320px纪念日日期Sheet和胶囊删除确认截图。其余页面状态/动效/实际软键盘并未由这20项覆盖。

## 控件契约

| 页面 | 控件 | 实际契约 |
| --- | --- | --- |
| m04-p05 | 返回重要时刻 | route:m04-p01 |
| m04-p05 | 今天约定就在今天 /  / 一起为 2026-10-05 留一段记录吧 | notice:time-today |
| m04-p06 | 返回重要时刻 | route:m04-p01 |
| m04-p06 | 去看看重要时刻 | route:m04-p01 |
| m04-p07 | 返回重要时刻 | route:m04-p01 |
| m04-p07 | 添加纪念日 | route:m04-p09 |
| m04-p07 | 2026-10-05 | route:m04-p11 |
| m04-p07 | 今天约定 / 每年 2026-10-05 | route:m04-p11 |
| m04-p07 | 今天约定提醒 | toggle-anniversary:time-today |
| m04-p07 | 未来约定 / 每年 2026-12-24 | route:m04-p10 |
| m04-p07 | 未来约定提醒 | toggle-anniversary:time-future |
| m04-p07 | 添加纪念日 | route:m04-p09 |
| m04-p07 | 刷新纪念日 | refresh:anniversary |
| m04-p08 | 返回重要时刻 | route:m04-p01 |
| m04-p08 | 添加第一个纪念日 | route:m04-p09 |
| m04-p09 | 返回纪念日列表 | route:m04-p07 |
| m04-p09 | name | native |
| m04-p09 | 纪念日日期 | sheet:纪念日日期 |
| m04-p09 | 提前 3 天 / 提前 1 天 / 当天 / 不提醒 | native |
| m04-p09 | 每年重复 | native |
| m04-p09 | 可选 · 关联一段章节 / 关联时刻 | native |
| m04-p09 | 保存纪念日 | save-anniversary |
| m04-p10 | 返回纪念日 | route:m04-p07 |
| m04-p10 | 关联时刻 | route:m04-p03 |
| m04-p10 | 写下新的共同记录 | route:m03-p05 |
| m04-p10 | 编辑纪念日 | route:m04-p09 |
| m04-p10 | 更多操作 | sheet:纪念日操作 |
| m04-p11 | 一起留下今天的记录 | route:m03-p05 |
| m04-p11 | 查看这个时刻 | route:m04-p03 |
| m04-p11 | 返回纪念日列表 | route:m04-p07 |
| m04-p11 | 编辑纪念日 | route:m04-p09 |
| m04-p11 | 更多操作 | sheet:纪念日操作 |
| m04-p12 | 返回重要时刻 | route:m04-p01 |
| m04-p12 | 新建时光胶囊 | route:m04-p13 |
| m04-p12 | 等待开启 | tab:等待开启 |
| m04-p12 | 已经开启 | tab:已经开启 |
| m04-p12 | 草稿 | tab:草稿 |
| m04-p12 | 封存的信 / 2026-10-06 · 还有 1 天 | route:m04-p15 |
| m04-p12 | ＋ 新建时光胶囊 | route:m04-p13 |
| m04-p12 | 刷新胶囊 | refresh:capsule |
| m04-p13 | 返回胶囊列表 | route:m04-p12 |
| m04-p13 | name | native |
| m04-p13 | message | native |
| m04-p13 | 添加照片 | file |
| m04-p13 | opening | sheet:开启日期 |
| m04-p13 | 开启提醒 | native |
| m04-p13 | 暂存草稿 | save-draft |
| m04-p13 | 封存这份心意 | save-sealed |
| m04-p14 | 返回胶囊列表 | route:m04-p12 |
| m04-p14 | 把这一刻收录进重要时刻 | collect |
| m04-p14 | 更多胶囊操作 | sheet:胶囊操作 |
| m04-p15 | 返回胶囊列表 | route:m04-p12 |
| m04-p15 | 开启当天提醒我 | native |
| m04-p15 | 更多胶囊操作 | sheet:胶囊操作 |

## 证据边界

全部99项绑定源码指纹 `ebd5deae3fa8341f9fe38164fe2d0245eafdf3f4ae6faa5dd06edd396c6717e4`，114页与37共享资产HTTP字节一致，custom/pages一致。以前record-controls的195项属于4f89521来源，本轮没有重新累计为当前全产品通过。旧纪念日/胶囊报告在evidence/history/pre-time-controls-4f89521保留；历史文件夹命名是保留时HEAD，不等同于旧测试来源。

已建初始控件契约的页面累计46页，余下68页仍需逐项建立与执行。已覆盖页仍有未覆盖动态条件、集合类型/引用恢复、跨模块连续流程、全部设计组件/布局/动效条件；114页最终验收仍为0，目标继续。Android式返回为浏览器历史模拟。
