# 当前114页导航与来源

## 隐藏动作条件边补证（2026-10-27）

下表为f5bc8d9产品源上的新实际执行。正文后续的大表和原关系图基础边保持原报告来源；其中“current”是原采集阶段标签，不代表全量边在最新源重跑。新证据含各自完整源指纹，不改旧报告。

| 来源 | 目标 | 控件／前提 | 实际结果证据 |
| --- | --- | --- | --- |
| m01-p07 | m01-p04 | 换一种验证方式→重新填写手机号；challenge.purpose=recovery | hidden-choice-outcomes/results.json，行索引0 |
| m01-p07 | m01-p03 | 同一选择；challenge.purpose=register | hidden-choice-outcomes/results.json，行索引1 |
| m02-p02 | m02-p07 | 分享邀请→查看邀请进度；有效演示邀请 | hidden-choice-outcomes/results.json，行索引6；邀请pending且其他数据保留 |
| m07-p04 | m07-p02 | 未领养→宠物日记→去领养 | hidden-auxiliary-outcomes/results.json，行索引7；数据不写入 |
| m04-p04 | m03-p05 | 无可用共同记录→选择共同记录→去写日记 | hidden-auxiliary-outcomes/results.json，行索引8；数据不写入 |
| m06-p07 | m01-p01 | 退出登录→确认退出 | hidden-settings-pet-outcomes/results.json，行索引5；仅退出登录、保留正文 |
| m06-p08 | m01-p01 | 安全设置→退出登录→确认退出 | hidden-settings-pet-outcomes/results.json，行索引6；仅退出登录、保留正文 |
| m07-p24 | m07-p25 | 暂停照顾→确认暂停 | hidden-settings-pet-outcomes/results.json，行索引22；库存／成长保留 |
| m07-p15 | m07-p14 | 解锁并选择格纹／月亮地毯→父页保存布置 | hidden-settings-pet-outcomes/results.json，行索引13、14；解锁不提前更新房间 |

上述相对结果路径均位于`evidence/current/`。关系图同步上述条件边；已有返回／脏输入保护证据保持其明确范围，单向CTA不自动证明所有返回条件。

当前源码绑定于page-contracts.json的151文件字节指纹。实线为当前源码实际控件执行；历史点击使用粗线，仅证明当时路径；虚线为当前代码候选或观察到的条件重定向。每条边保留类型和报告位置，数字go、动态ID、弹层取消／确认及来源历史仍需条件验证。

| 来源 | 目标 | 类型 | 控件／条件 | 证据 |
| --- | --- | --- | --- | --- |
| m01-p01 | m01-p02 | executed-current | 登录并开始 | evidence/current/onboarding-control-results.json |
| m01-p01 | m01-p03 | executed-current | 创建账号 | evidence/current/onboarding-control-results.json |
| m01-p02 | m01-p01 | executed-current | 返回 | evidence/current/onboarding-control-results.json |
| m01-p02 | m01-p04 | executed-current | 忘记密码？ | evidence/current/onboarding-control-results.json |
| m01-p02 | m02-p01 | executed-current | 登录并回到故事里 | evidence/current/onboarding-control-results.json |
| m01-p02 | m01-p03 | executed-current | 创建账号 | evidence/current/onboarding-control-results.json |
| m01-p03 | m01-p01 | executed-current | 返回欢迎页 | evidence/current/onboarding-control-results.json |
| m01-p03 | m01-p07 | executed-current | 创建账号 | evidence/current/onboarding-control-results.json |
| m01-p03 | m01-p02 | executed-current | 去登录 | evidence/current/onboarding-control-results.json |
| m01-p04 | m01-p02 | executed-current | 返回 | evidence/current/onboarding-control-results.json |
| m01-p04 | m01-p07 | executed-current | 下一步 | evidence/current/onboarding-control-results.json |
| m01-p04 | m01-p02 | executed-current | 返回登录 | evidence/current/onboarding-control-results.json |
| m01-p05 | m01-p04 | executed-current | 返回找回密码 | evidence/current/onboarding-control-results.json |
| m01-p05 | m01-p08 | executed-current | 确认并重置 | evidence/current/onboarding-control-results.json |
| m01-p06 | m01-p02 | executed-current | 返回 | evidence/current/onboarding-control-results.json |
| m01-p06 | m02-p01 | executed-current | 再试一次 | evidence/current/onboarding-control-results.json |
| m01-p06 | m01-p04 | executed-current | 找回密码 | evidence/current/onboarding-control-results.json |
| m01-p07 | m01-p04 | executed-current | 返回 | evidence/current/onboarding-control-results.json |
| m01-p07 | m01-p05 | executed-current | 验证并继续 | evidence/current/onboarding-control-results.json |
| m01-p08 | m01-p02 | executed-current | 返回登录 | evidence/current/onboarding-control-results.json |
| m02-p01 | m01-p02 | executed-current | 返回登录 | evidence/current/onboarding-control-results.json |
| m02-p01 | m02-p02 | executed-current | 邀请 TA 加入 生成专属邀请码 | evidence/current/onboarding-control-results.json |
| m02-p01 | m02-p03 | executed-current | 输入 TA 的邀请码 接受一份特别邀请 | evidence/current/onboarding-control-results.json |
| m02-p02 | m02-p01 | executed-current | 返回建立关系 | evidence/current/onboarding-control-results.json |
| m02-p03 | m02-p01 | executed-current | 返回 | evidence/current/onboarding-control-results.json |
| m02-p03 | m02-p04 | executed-current | 查看邀请内容 | evidence/current/onboarding-control-results.json |
| m02-p03 | m02-p01 | executed-current | 请让 TA 分享给你 | evidence/current/onboarding-control-results.json |
| m02-p04 | m02-p03 | executed-current | 返回 | evidence/current/onboarding-control-results.json |
| m02-p04 | m02-p05 | executed-current | 确认建立关系 | evidence/current/onboarding-control-results.json |
| m02-p04 | m02-p01 | executed-current | 暂不接受 | evidence/current/onboarding-control-results.json |
| m02-p05 | m03-p05 | executed-current | 去写第一篇共同日记 ♡ | evidence/current/onboarding-control-results.json |
| m02-p05 | m02-p06 | executed-current | 完善情侣资料 | evidence/current/onboarding-control-results.json |
| m02-p05 | m03-p01 | executed-current | 先逛逛我们的首页 | evidence/current/onboarding-control-results.json |
| m02-p06 | m02-p05 | executed-current | 返回 | evidence/current/onboarding-control-results.json |
| m02-p06 | m02-p01 | executed-current | 保存小资料 | evidence/current/onboarding-control-results.json |
| m02-p07 | m02-p02 | executed-current | 返回邀请卡 | evidence/current/onboarding-control-results.json |
| m02-p08 | m02-p01 | executed-current | 请 TA 重新邀请 | evidence/current/onboarding-control-results.json |
| m02-p08 | m02-p03 | executed-current | 重新输入邀请码 | evidence/current/onboarding-control-results.json |
| m02-p09 | m03-p01 | executed-current | 回到我们的首页 | evidence/current/onboarding-control-results.json |
| m02-p09 | m02-p06 | executed-current | 查看关系设置 | evidence/current/onboarding-control-results.json |
| m03-p01 | m03-p03 | executed-current | 搜索共同记录 | evidence/current/record-controls-results.json |
| m03-p01 | m03-p05 | executed-current | 写日记 | evidence/current/record-controls-results.json |
| m03-p01 | m03-p11 | executed-current | 添加照片 | evidence/current/record-controls-results.json |
| m03-p01 | m05-p01 | executed-current | 去童话工坊，把回忆变成故事 › | evidence/current/record-controls-results.json |
| m03-p01 | m04-p02 | executed-current | 重要时刻 | evidence/current/record-controls-results.json |
| m03-p01 | m05-p01 | executed-current | 工坊 | evidence/current/record-controls-results.json |
| m03-p01 | m07-p03 | executed-current | 宠物 | evidence/current/record-controls-results.json |
| m03-p01 | m06-p01 | executed-current | 我的 | evidence/current/record-controls-results.json |
| m03-p02 | m03-p03 | executed-current | 搜索共同记录 | evidence/current/record-controls-results.json |
| m03-p02 | m03-p05 | executed-current | 写日记 记录心情 | evidence/current/record-controls-results.json |
| m03-p02 | m03-p11 | executed-current | 添加照片 珍藏瞬间 | evidence/current/record-controls-results.json |
| m03-p02 | m05-p01 | executed-current | 去童话工坊，把回忆变成故事 › | evidence/current/record-controls-results.json |
| m03-p02 | m03-p06 | executed-current | 查看全部 › | evidence/current/record-controls-results.json |
| m03-p02 | m03-p08 | executed-current | 共同日记 小满 · 共同可见 | evidence/current/record-controls-results.json |
| m03-p02 | m03-p07 | executed-current | 自己的日记 小满 · 仅自己可见 | evidence/current/record-controls-results.json |
| m03-p02 | m03-p12 | executed-current | 共同照片 小满 · 共同可见 | evidence/current/record-controls-results.json |
| m03-p02 | m08-p15 | executed-current | 共同测试册 从目录开始阅读 继续阅读 › | evidence/current/record-controls-results.json |
| m03-p02 | m04-p10 | executed-current | 下一件重要时刻 未来的纪念日 · 61 天后 查看纪念日 › | evidence/current/record-controls-results.json |
| m03-p02 | m04-p01 | executed-current | 重要时刻 | evidence/current/record-controls-results.json |
| m03-p02 | m05-p01 | executed-current | 工坊 | evidence/current/record-controls-results.json |
| m03-p02 | m07-p03 | executed-current | 宠物 | evidence/current/record-controls-results.json |
| m03-p02 | m06-p01 | executed-current | 我的 | evidence/current/record-controls-results.json |
| m03-p03 | m03-p01 | executed-current | 返回首页 | evidence/current/record-controls-results.json |
| m03-p03 | m03-p04 | executed-current | 晚霞 | evidence/current/record-controls-results.json |
| m03-p03 | m03-p04 | executed-current | 火锅 | evidence/current/record-controls-results.json |
| m03-p03 | m03-p04 | executed-current | 旅行 | evidence/current/record-controls-results.json |
| m03-p03 | m03-p04 | executed-current | 日记 | evidence/current/record-controls-results.json |
| m03-p03 | m03-p04 | executed-current | 照片 | evidence/current/record-controls-results.json |
| m03-p03 | m03-p04 | executed-current | 纪念日 | evidence/current/record-controls-results.json |
| m03-p04 | m03-p03 | executed-current | 返回搜索 | evidence/current/record-controls-results.json |
| m03-p04 | m03-p03 | executed-current | 清除 | evidence/current/record-controls-results.json |
| m03-p04 | m03-p08 | executed-current | 共同日记  真正可编辑的共同正文  共同可见 | evidence/current/record-controls-results.json |
| m03-p04 | m03-p12 | executed-current | 共同照片  共同照片说明  共同可见 | evidence/current/record-controls-results.json |
| m03-p05 | m03-p06 | executed-current | 返回日记列表 | evidence/current/record-controls-results.json |
| m03-p05 | m03-p06 | executed-current | 存草稿 | evidence/current/record-controls-results.json |
| m03-p05 | m03-p06 | executed-current | 保存日记 | evidence/current/record-controls-results.json |
| m03-p06 | m03-p02 | executed-current | 返回首页 | evidence/current/record-controls-results.json |
| m03-p06 | m03-p05 | executed-current | 写日记 | evidence/current/record-controls-results.json |
| m03-p06 | m03-p08 | executed-current | 共同日记  真正可编辑的共同正文  小满 · 2026/10/4 · 共同可见 | evidence/current/record-controls-results.json |
| m03-p06 | m03-p07 | executed-current | 自己的日记  独立私密正文  小满 · 2026/10/4 · 仅自己可见 | evidence/current/record-controls-results.json |
| m03-p07 | m03-p06 | executed-current | 返回日记列表 | evidence/current/record-controls-results.json |
| m03-p07 | m03-p05 | executed-current | 编辑日记 | evidence/current/record-controls-results.json |
| m03-p08 | m03-p06 | executed-current | 返回日记列表 | evidence/current/record-controls-results.json |
| m03-p08 | m03-p05 | executed-current | 编辑日记 | evidence/current/record-controls-results.json |
| m03-p09 | m03-p01 | executed-current | 返回首页 | evidence/current/record-controls-results.json |
| m03-p09 | m03-p11 | executed-current | 添加第一张照片 | evidence/current/record-controls-results.json |
| m03-p09 | m03-p11 | executed-current | 从系统相册选择 | evidence/current/record-controls-results.json |
| m03-p10 | m03-p02 | executed-current | 返回首页 | evidence/current/record-controls-results.json |
| m03-p10 | m03-p12 | executed-current | 共同照片 | evidence/current/record-controls-results.json |
| m03-p10 | m03-p11 | executed-current | ＋ 添加照片 | evidence/current/record-controls-results.json |
| m03-p11 | m03-p09 | executed-current | 返回相册 | evidence/current/record-controls-results.json |
| m03-p11 | m03-p10 | executed-current | 完成 | evidence/current/record-controls-results.json |
| m03-p11 | m03-p10 | executed-current | 保存照片 | evidence/current/record-controls-results.json |
| m03-p12 | m03-p10 | executed-current | 返回照片相册 | evidence/current/record-controls-results.json |
| m03-p12 | m03-p11 | executed-current | 编辑照片 | evidence/current/record-controls-results.json |
| m04-p01 | m04-p07 | executed-current | 查看纪念日 | evidence/current/moment-controls-results.json |
| m04-p01 | m04-p04 | executed-current | 珍藏一个新时刻 | evidence/current/moment-controls-results.json |
| m04-p01 | m04-p03 | executed-current | 共同重要时刻 2026-10-04 | evidence/current/moment-controls-results.json |
| m04-p01 | m04-p07 | executed-current | 纪念日 | evidence/current/moment-controls-results.json |
| m04-p01 | m04-p12 | executed-current | 时光胶囊 | evidence/current/moment-controls-results.json |
| m04-p01 | m04-p16 | executed-current | 悄悄留言 | evidence/current/moment-controls-results.json |
| m04-p01 | m04-p04 | executed-current | 新建重要时刻 | evidence/current/moment-controls-results.json |
| m04-p01 | m04-p05 | executed-current | 共同提醒 | evidence/current/moment-controls-results.json |
| m04-p01 | m03-p02 | executed-current | 首页 | evidence/current/moment-controls-results.json |
| m04-p01 | m05-p01 | executed-current | 工坊 | evidence/current/moment-controls-results.json |
| m04-p01 | m07-p03 | executed-current | 宠物 | evidence/current/moment-controls-results.json |
| m04-p01 | m06-p01 | executed-current | 我的 | evidence/current/moment-controls-results.json |
| m04-p02 | m04-p04 | executed-current | 从共同记录中收录 | evidence/current/moment-controls-results.json |
| m04-p02 | m04-p04 | executed-current | 新建重要时刻 | evidence/current/moment-controls-results.json |
| m04-p02 | m04-p08 | executed-current | 纪念日 | evidence/current/moment-controls-results.json |
| m04-p02 | m04-p12 | executed-current | 时光胶囊 | evidence/current/moment-controls-results.json |
| m04-p02 | m04-p17 | executed-current | 悄悄留言 | evidence/current/moment-controls-results.json |
| m04-p02 | m04-p06 | executed-current | 共同提醒 | evidence/current/moment-controls-results.json |
| m04-p02 | m03-p01 | executed-current | 首页 | evidence/current/moment-controls-results.json |
| m04-p02 | m05-p01 | executed-current | 工坊 | evidence/current/moment-controls-results.json |
| m04-p02 | m07-p03 | executed-current | 宠物 | evidence/current/moment-controls-results.json |
| m04-p02 | m06-p01 | executed-current | 我的 | evidence/current/moment-controls-results.json |
| m04-p03 | m04-p01 | executed-current | 返回重要时刻 | evidence/current/moment-controls-results.json |
| m04-p03 | m03-p08 | executed-current | 共同日记 | evidence/current/moment-controls-results.json |
| m04-p03 | m04-p04 | executed-current | 编辑时刻 | evidence/current/moment-controls-results.json |
| m04-p04 | m04-p02 | executed-current | 返回重要时刻 | evidence/current/moment-controls-results.json |
| m04-p04 | m04-p01 | executed-current | 保存到时刻册 | evidence/current/moment-controls-results.json |
| m04-p16 | m04-p01 | executed-current | 返回重要时刻 | evidence/current/moment-controls-results.json |
| m04-p16 | m04-p03 | executed-current | 查看原记录 | evidence/current/moment-controls-results.json |
| m04-p17 | m04-p02 | executed-current | 返回重要时刻 | evidence/current/moment-controls-results.json |
| m04-p17 | m03-p06 | executed-current | 去看看共同记录 | evidence/current/moment-controls-results.json |
| m04-p05 | m04-p01 | executed-current | 返回重要时刻 | evidence/current/time-controls-results.json |
| m04-p05 | m04-p11 | executed-current | 今天约定就在今天  一起为 2026-10-05 留一段记录吧 | evidence/current/time-controls-results.json |
| m04-p06 | m04-p01 | executed-current | 返回重要时刻 | evidence/current/time-controls-results.json |
| m04-p06 | m04-p01 | executed-current | 去看看重要时刻 | evidence/current/time-controls-results.json |
| m04-p07 | m04-p01 | executed-current | 返回重要时刻 | evidence/current/time-controls-results.json |
| m04-p07 | m04-p09 | executed-current | 添加纪念日 | evidence/current/time-controls-results.json |
| m04-p07 | m04-p11 | executed-current | 2026-10-05 | evidence/current/time-controls-results.json |
| m04-p07 | m04-p11 | executed-current | 今天约定 每年 2026-10-05 | evidence/current/time-controls-results.json |
| m04-p07 | m04-p10 | executed-current | 未来约定 每年 2026-12-24 | evidence/current/time-controls-results.json |
| m04-p08 | m04-p01 | executed-current | 返回重要时刻 | evidence/current/time-controls-results.json |
| m04-p08 | m04-p09 | executed-current | 添加第一个纪念日 | evidence/current/time-controls-results.json |
| m04-p09 | m04-p07 | executed-current | 返回纪念日列表 | evidence/current/time-controls-results.json |
| m04-p09 | m04-p07 | executed-current | 保存纪念日 | evidence/current/time-controls-results.json |
| m04-p10 | m04-p07 | executed-current | 返回纪念日 | evidence/current/time-controls-results.json |
| m04-p10 | m04-p03 | executed-current | 关联时刻 | evidence/current/time-controls-results.json |
| m04-p10 | m03-p05 | executed-current | 写下新的共同记录 | evidence/current/time-controls-results.json |
| m04-p10 | m04-p09 | executed-current | 编辑纪念日 | evidence/current/time-controls-results.json |
| m04-p11 | m03-p05 | executed-current | 一起留下今天的记录 | evidence/current/time-controls-results.json |
| m04-p11 | m04-p03 | executed-current | 查看这个时刻 | evidence/current/time-controls-results.json |
| m04-p11 | m04-p07 | executed-current | 返回纪念日列表 | evidence/current/time-controls-results.json |
| m04-p11 | m04-p09 | executed-current | 编辑纪念日 | evidence/current/time-controls-results.json |
| m04-p12 | m04-p01 | executed-current | 返回重要时刻 | evidence/current/time-controls-results.json |
| m04-p12 | m04-p13 | executed-current | 新建时光胶囊 | evidence/current/time-controls-results.json |
| m04-p12 | m04-p15 | executed-current | 封存的信 2026-10-06 · 还有 1 天 | evidence/current/time-controls-results.json |
| m04-p12 | m04-p13 | executed-current | ＋ 新建时光胶囊 | evidence/current/time-controls-results.json |
| m04-p13 | m04-p12 | executed-current | 返回胶囊列表 | evidence/current/time-controls-results.json |
| m04-p13 | m04-p12 | executed-current | 暂存草稿 | evidence/current/time-controls-results.json |
| m04-p13 | m04-p15 | executed-current | 封存这份心意 | evidence/current/time-controls-results.json |
| m04-p14 | m04-p12 | executed-current | 返回胶囊列表 | evidence/current/time-controls-results.json |
| m04-p14 | m04-p03 | executed-current | 把这一刻收录进重要时刻 | evidence/current/time-controls-results.json |
| m04-p15 | m04-p12 | executed-current | 返回胶囊列表 | evidence/current/time-controls-results.json |
| m05-p01 | m05-p02 | executed-current | 做成童话漫画 把回忆画成专属故事 留下一格格心动瞬间 | evidence/current/workshop-controls-results.json |
| m05-p01 | m05-p05 | executed-current | 制作回忆影片 让重要时刻动起来 在光影里重温感动 | evidence/current/workshop-controls-results.json |
| m05-p01 | m05-p09 | executed-current | 查看全部 › | evidence/current/workshop-controls-results.json |
| m05-p01 | m05-p03 | executed-current | work-free 草稿 | evidence/current/workshop-controls-results.json |
| m05-p01 | m05-p04 | executed-current | work-photos 草稿 | evidence/current/workshop-controls-results.json |
| m05-p01 | m05-p02 | executed-current | 开始一次创作 | evidence/current/workshop-controls-results.json |
| m05-p01 | m03-p02 | executed-current | 首页 | evidence/current/workshop-controls-results.json |
| m05-p01 | m04-p01 | executed-current | 重要时刻 | evidence/current/workshop-controls-results.json |
| m05-p01 | m07-p04 | executed-current | 宠物 | evidence/current/workshop-controls-results.json |
| m05-p01 | m06-p01 | executed-current | 我的 | evidence/current/workshop-controls-results.json |
| m05-p02 | m05-p01 | executed-current | 返回童话工坊 | evidence/current/workshop-controls-results.json |
| m05-p03 | m05-p02 | executed-current | 返回素材选择 | evidence/current/workshop-controls-results.json |
| m05-p03 | m05-p10 | executed-current | 默默 & 小满 可爱自然 · 清新温柔 | evidence/current/workshop-controls-results.json |
| m05-p03 | m05-p06 | executed-current | 生成童话漫画 | evidence/current/workshop-controls-results.json |
| m05-p03 | m05-p09 | executed-current | 暂存创作草稿 | evidence/current/workshop-controls-results.json |
| m05-p04 | m05-p02 | executed-current | 返回素材选择 | evidence/current/workshop-controls-results.json |
| m05-p04 | m05-p10 | executed-current | 他  阳光温柔 | evidence/current/workshop-controls-results.json |
| m05-p04 | m05-p10 | executed-current | 她  温柔爱笑 | evidence/current/workshop-controls-results.json |
| m05-p04 | m05-p06 | executed-current | 生成童话漫画 | evidence/current/workshop-controls-results.json |
| m05-p04 | m05-p09 | executed-current | 暂存创作草稿 | evidence/current/workshop-controls-results.json |
| m05-p05 | m05-p01 | executed-current | 返回工坊 | evidence/current/workshop-controls-results.json |
| m05-p05 | m05-p06 | executed-current | 生成回忆影片 | evidence/current/workshop-controls-results.json |
| m05-p05 | m05-p09 | executed-current | 暂存创作草稿 | evidence/current/workshop-controls-results.json |
| m05-p06 | m05-p01 | executed-current | 返回童话工坊 | evidence/current/workshop-controls-results.json |
| m05-p07 | m05-p03 | executed-current | 调整内容 | evidence/current/workshop-controls-results.json |
| m05-p07 | m05-p06 | executed-current | 重新生成 | evidence/current/workshop-controls-results.json |
| m05-p07 | m05-p01 | executed-current | 先回到童话工坊 ♡ | evidence/current/workshop-controls-results.json |
| m05-p08 | m05-p09 | executed-current | 返回我的创作 | evidence/current/workshop-controls-results.json |
| m05-p08 | m05-p05 | executed-current | 重新生成 | evidence/current/workshop-controls-results.json |
| m05-p09 | m05-p02 | executed-current | 开始创作 | evidence/current/workshop-controls-results.json |
| m05-p09 | m05-p03 | executed-current | work-free 漫画 · 草稿 | evidence/current/workshop-controls-results.json |
| m05-p09 | m05-p04 | executed-current | work-photos 漫画 · 草稿 | evidence/current/workshop-controls-results.json |
| m05-p09 | m05-p05 | executed-current | work-film 影片 · 草稿 | evidence/current/workshop-controls-results.json |
| m05-p09 | m05-p06 | executed-current | work-running 漫画 · 制作中 | evidence/current/workshop-controls-results.json |
| m05-p09 | m05-p07 | executed-current | work-failed 漫画 · 生成失败 | evidence/current/workshop-controls-results.json |
| m05-p09 | m05-p08 | executed-current | work-ready 影片 · 已完成 | evidence/current/workshop-controls-results.json |
| m05-p09 | m05-p01 | executed-current | 返回童话工坊 | evidence/current/workshop-controls-results.json |
| m05-p10 | m05-p03 | executed-current | 返回当前创作 | evidence/current/workshop-controls-results.json |
| m05-p10 | m05-p03 | executed-current | 更新我们的主角 | evidence/current/workshop-controls-results.json |
| m06-p01 | m06-p02 | executed-current | 小满 ♡ 已与阿舟关联 ♡ | evidence/current/settings-controls-results.json |
| m06-p01 | m06-p03 | executed-current | 我们的小世界 一起管理共同资料 | evidence/current/settings-controls-results.json |
| m06-p01 | m06-p04 | executed-current | 草稿箱 | evidence/current/settings-controls-results.json |
| m06-p01 | m06-p05 | executed-current | 标签管理 | evidence/current/settings-controls-results.json |
| m06-p01 | m06-p06 | executed-current | 童话会员 | evidence/current/settings-controls-results.json |
| m06-p01 | m06-p07 | executed-current | 设置 | evidence/current/settings-controls-results.json |
| m06-p01 | m06-p12 | executed-current | 帮助与关于 | evidence/current/settings-controls-results.json |
| m06-p01 | m03-p02 | executed-current | 首页 | evidence/current/settings-controls-results.json |
| m06-p01 | m04-p01 | executed-current | 重要时刻 | evidence/current/settings-controls-results.json |
| m06-p01 | m05-p01 | executed-current | 工坊 | evidence/current/settings-controls-results.json |
| m06-p01 | m07-p04 | executed-current | 宠物 | evidence/current/settings-controls-results.json |
| m06-p02 | m06-p01 | executed-current | 返回我的与设置 | evidence/current/settings-controls-results.json |
| m06-p02 | m06-p01 | executed-current | 保存资料 | evidence/current/settings-controls-results.json |
| m06-p03 | m06-p01 | executed-current | 返回我的与设置 | evidence/current/settings-controls-results.json |
| m06-p03 | m06-p09 | executed-current | 共同空间设置 哪些记录邀请对方一起看 | evidence/current/settings-controls-results.json |
| m06-p04 | m06-p01 | executed-current | 返回我的与设置 | evidence/current/settings-controls-results.json |
| m06-p04 | m03-p05 | executed-current | 日记草稿 日记 · 继续编辑 | evidence/current/settings-controls-results.json |
| m06-p04 | m05-p03 | executed-current | 工坊草稿 工坊 · 继续编辑 | evidence/current/settings-controls-results.json |
| m06-p04 | m04-p13 | executed-current | 胶囊草稿 胶囊 · 继续编辑 | evidence/current/settings-controls-results.json |
| m06-p04 | m08-p04 | executed-current | 回忆册草稿 回忆册 · 继续编辑 | evidence/current/settings-controls-results.json |
| m06-p05 | m06-p01 | executed-current | 返回我的与设置 | evidence/current/settings-controls-results.json |
| m06-p06 | m06-p01 | executed-current | 返回我的与设置 | evidence/current/settings-controls-results.json |
| m06-p07 | m06-p01 | executed-current | 返回我的与设置 | evidence/current/settings-controls-results.json |
| m06-p07 | m06-p08 | executed-current | 账号与安全 | evidence/current/settings-controls-results.json |
| m06-p07 | m06-p09 | executed-current | 隐私与共同可见 | evidence/current/settings-controls-results.json |
| m06-p07 | m06-p10 | executed-current | 通知设置 | evidence/current/settings-controls-results.json |
| m06-p07 | m06-p11 | executed-current | 数据与存储 | evidence/current/settings-controls-results.json |
| m06-p08 | m06-p07 | executed-current | 返回设置 | evidence/current/settings-controls-results.json |
| m06-p08 | m01-p04 | executed-current | 修改密码 | evidence/current/settings-controls-results.json |
| m06-p09 | m06-p07 | executed-current | 返回设置 | evidence/current/settings-controls-results.json |
| m06-p10 | m06-p07 | executed-current | 返回设置 | evidence/current/settings-controls-results.json |
| m06-p11 | m06-p07 | executed-current | 返回设置 | evidence/current/settings-controls-results.json |
| m06-p12 | m06-p01 | executed-current | 返回我的与设置 | evidence/current/settings-controls-results.json |
| m07-p01 | m03-p02 | executed-current | 暂时返回 | evidence/current/pet-controls-results.json |
| m07-p01 | m03-p02 | executed-current | 返回 | evidence/current/pet-controls-results.json |
| m07-p01 | m03-p02 | executed-current | 首页 | evidence/current/pet-controls-results.json |
| m07-p01 | m04-p01 | executed-current | 重要时刻 | evidence/current/pet-controls-results.json |
| m07-p01 | m05-p01 | executed-current | 工坊 | evidence/current/pet-controls-results.json |
| m07-p01 | m06-p01 | executed-current | 我的 | evidence/current/pet-controls-results.json |
| m07-p02 | m07-p01 | executed-current | 邀请 TA 一起领养 | evidence/current/pet-controls-results.json |
| m07-p02 | m07-p04 | executed-current | 返回 | evidence/current/pet-controls-results.json |
| m07-p03 | m07-p06 | executed-current | 互动 | evidence/current/pet-controls-results.json |
| m07-p03 | m07-p08 | executed-current | 喂食 | evidence/current/pet-controls-results.json |
| m07-p03 | m07-p11 | executed-current | 任务 | evidence/current/pet-controls-results.json |
| m07-p03 | m07-p12 | executed-current | 装扮 | evidence/current/pet-controls-results.json |
| m07-p03 | m07-p15 | executed-current | 布置小屋 | evidence/current/pet-controls-results.json |
| m07-p03 | m07-p18 | executed-current | 成长故事 | evidence/current/pet-controls-results.json |
| m07-p03 | m07-p21 | executed-current | 成就图鉴 | evidence/current/pet-controls-results.json |
| m07-p03 | m07-p11 | executed-current | 去任务 › | evidence/current/pet-controls-results.json |
| m07-p03 | m03-p02 | executed-current | 返回 | evidence/current/pet-controls-results.json |
| m07-p03 | m07-p25 | executed-current | 宠物设置 | evidence/current/pet-controls-results.json |
| m07-p03 | m03-p02 | executed-current | 首页 | evidence/current/pet-controls-results.json |
| m07-p03 | m04-p01 | executed-current | 重要时刻 | evidence/current/pet-controls-results.json |
| m07-p03 | m05-p01 | executed-current | 工坊 | evidence/current/pet-controls-results.json |
| m07-p03 | m06-p01 | executed-current | 我的 | evidence/current/pet-controls-results.json |
| m07-p04 | m07-p02 | executed-current | 一起领养 | evidence/current/pet-controls-results.json |
| m07-p04 | m03-p02 | executed-current | 返回 | evidence/current/pet-controls-results.json |
| m07-p04 | m03-p02 | executed-current | 首页 | evidence/current/pet-controls-results.json |
| m07-p04 | m04-p01 | executed-current | 重要时刻 | evidence/current/pet-controls-results.json |
| m07-p04 | m05-p01 | executed-current | 工坊 | evidence/current/pet-controls-results.json |
| m07-p04 | m06-p01 | executed-current | 我的 | evidence/current/pet-controls-results.json |
| m07-p05 | m07-p06 | executed-current | 再玩一次 | evidence/current/pet-controls-results.json |
| m07-p05 | m07-p03 | executed-current | 回到小屋 | evidence/current/pet-controls-results.json |
| m07-p05 | m07-p03 | executed-current | 返回 | evidence/current/pet-controls-results.json |
| m07-p06 | m07-p05 | executed-current | 和团团互动 | evidence/current/pet-controls-results.json |
| m07-p06 | m07-p03 | executed-current | 返回 | evidence/current/pet-controls-results.json |
| m07-p07 | m07-p03 | executed-current | 宠物空间 | evidence/current/pet-controls-results.json |
| m07-p07 | m07-p18 | executed-current | 成长日记 | evidence/current/pet-controls-results.json |
| m07-p07 | m07-p08 | executed-current | 去喂食补充精力 › | evidence/current/pet-controls-results.json |
| m07-p08 | m07-p11 | executed-current | 去获得更多食物 › | evidence/current/pet-controls-results.json |
| m07-p08 | m07-p03 | executed-current | 返回 | evidence/current/pet-controls-results.json |
| m07-p09 | m07-p03 | executed-current | 返回 | evidence/current/pet-controls-results.json |
| m07-p09 | m07-p11 | executed-current | 去做任务 | evidence/current/pet-controls-results.json |
| m07-p10 | m07-p11 | executed-current | 返回任务 | evidence/current/pet-controls-results.json |
| m07-p10 | m07-p03 | executed-current | 返回 | evidence/current/pet-controls-results.json |
| m07-p11 | m07-p03 | executed-current | 返回小屋 | evidence/current/pet-controls-results.json |
| m07-p11 | m07-p03 | executed-current | 返回 | evidence/current/pet-controls-results.json |
| m07-p11 | m07-p06 | executed-current | 陪宠物互动 | evidence/current/pet-controls-results.json |
| m07-p11 | m07-p08 | executed-current | 给宠物喂食 | evidence/current/pet-controls-results.json |
| m07-p11 | m07-p15 | executed-current | 整理宠物小屋 | evidence/current/pet-controls-results.json |
| m07-p12 | m07-p03 | executed-current | 返回宠物小屋 | evidence/current/pet-controls-results.json |
| m07-p13 | m07-p03 | executed-current | 宠物空间 | evidence/current/pet-controls-results.json |
| m07-p13 | m07-p11 | executed-current | 去做任务 | evidence/current/pet-controls-results.json |
| m07-p14 | m07-p15 | executed-current | 继续布置 | evidence/current/pet-controls-results.json |
| m07-p14 | m07-p03 | executed-current | 回到小屋 | evidence/current/pet-controls-results.json |
| m07-p14 | m07-p03 | executed-current | 返回 | evidence/current/pet-controls-results.json |
| m07-p15 | m07-p16 | executed-current | 野餐垫 照顾7个不同日期 | evidence/current/pet-controls-results.json |
| m07-p15 | m07-p14 | executed-current | 保存小屋布置 | evidence/current/pet-controls-results.json |
| m07-p15 | m07-p03 | executed-current | 返回 | evidence/current/pet-controls-results.json |
| m07-p16 | m07-p03 | executed-current | 返回 | evidence/current/pet-controls-results.json |
| m07-p16 | m07-p11 | executed-current | 去做任务 | evidence/current/pet-controls-results.json |
| m07-p17 | m07-p18 | executed-current | 返回成长时间线 | evidence/current/pet-controls-results.json |
| m07-p18 | m07-p03 | executed-current | 返回 | evidence/current/pet-controls-results.json |
| m07-p18 | m07-p19 | executed-current | 2026-10-05 · 小满 共同成长故事 | evidence/current/pet-controls-results.json |
| m07-p19 | m07-p18 | executed-current | 返回 | evidence/current/pet-controls-results.json |
| m07-p20 | m07-p03 | executed-current | 返回 | evidence/current/pet-controls-results.json |
| m07-p21 | m07-p20 | executed-current | 第一次见面 可领取奖励 | evidence/current/pet-controls-results.json |
| m07-p21 | m07-p20 | executed-current | 玩到天黑 0 / 10 | evidence/current/pet-controls-results.json |
| m07-p21 | m07-p20 | executed-current | 默契喂食 0 / 20 | evidence/current/pet-controls-results.json |
| m07-p21 | m07-p20 | executed-current | 小屋变新了 0 / 1 | evidence/current/pet-controls-results.json |
| m07-p21 | m07-p20 | executed-current | 照顾7天 1 / 7 | evidence/current/pet-controls-results.json |
| m07-p21 | m07-p20 | executed-current | 亲密搭档 可领取奖励 | evidence/current/pet-controls-results.json |
| m07-p21 | m07-p20 | executed-current | 陪伴30天 可领取奖励 | evidence/current/pet-controls-results.json |
| m07-p21 | m07-p11 | executed-current | 去完成今天的照顾 | evidence/current/pet-controls-results.json |
| m07-p21 | m07-p03 | executed-current | 返回 | evidence/current/pet-controls-results.json |
| m07-p21 | m07-p22 | executed-current | 收藏图鉴 | evidence/current/pet-controls-results.json |
| m07-p22 | m07-p23 | executed-current | 小花围巾 已拥有 | evidence/current/pet-controls-results.json |
| m07-p22 | m07-p23 | executed-current | 格纹蝴蝶结 金币20 | evidence/current/pet-controls-results.json |
| m07-p22 | m07-p23 | executed-current | 星星领结 亲密度160 | evidence/current/pet-controls-results.json |
| m07-p22 | m07-p23 | executed-current | 蜜桃帽子 记录一页成长故事 | evidence/current/pet-controls-results.json |
| m07-p22 | m07-p23 | executed-current | 星光皇冠 星星30 | evidence/current/pet-controls-results.json |
| m07-p22 | m07-p23 | executed-current | 雨天小斗篷 照顾7个不同日期 | evidence/current/pet-controls-results.json |
| m07-p22 | m07-p23 | executed-current | 暖暖小马甲 金币20 | evidence/current/pet-controls-results.json |
| m07-p22 | m07-p23 | executed-current | 晚安铃铛 喂食20次 | evidence/current/pet-controls-results.json |
| m07-p22 | m07-p03 | executed-current | 返回 | evidence/current/pet-controls-results.json |
| m07-p23 | m07-p22 | executed-current | 返回图鉴 | evidence/current/pet-controls-results.json |
| m07-p23 | m07-p12 | executed-current | 去换上 | evidence/current/pet-controls-results.json |
| m07-p24 | m07-p25 | executed-current | 我再想想，返回 | evidence/current/pet-controls-results.json |
| m07-p24 | m07-p25 | executed-current | 返回 | evidence/current/pet-controls-results.json |
| m07-p25 | m07-p03 | executed-current | 返回宠物空间 | evidence/current/pet-controls-results.json |
| m07-p25 | m07-p24 | executed-current | 暂时解除共同照顾 | evidence/current/pet-controls-results.json |
| m08-p01 | m08-p15 | executed-current | ♡ 共同测试册 花园午后 | evidence/current/book-controls-results.json |
| m08-p01 | m08-p15 | executed-current | 继续阅读 › | evidence/current/book-controls-results.json |
| m08-p01 | m08-p04 | executed-current | 新建回忆册 | evidence/current/book-controls-results.json |
| m08-p01 | m08-p03 | executed-current | 本月推荐 | evidence/current/book-controls-results.json |
| m08-p01 | m03-p02 | executed-current | 返回首页 | evidence/current/book-controls-results.json |
| m08-p02 | m03-p02 | executed-current | 返回 | evidence/current/book-controls-results.json |
| m08-p02 | m08-p04 | executed-current | 新建第一本回忆册 | evidence/current/book-controls-results.json |
| m08-p03 | m08-p01 | executed-current | 返回回忆册 | evidence/current/book-controls-results.json |
| m08-p03 | m08-p04 | executed-current | 查看并确认素材 | evidence/current/book-controls-results.json |
| m08-p03 | m08-p01 | executed-current | 返回书架 | evidence/current/book-controls-results.json |
| m08-p03 | m03-p08 | executed-current | 共同日记 · 2026-10-04 | evidence/current/book-controls-results.json |
| m08-p03 | m03-p12 | executed-current | 共同照片 · 2026-10-04 | evidence/current/book-controls-results.json |
| m08-p03 | m04-p03 | executed-current | 共同重要时刻 · 2026-10-04 | evidence/current/book-controls-results.json |
| m08-p03 | m05-p08 | executed-current | 实际工坊作品 · 2026-10-05 | evidence/current/book-controls-results.json |
| m08-p03 | m07-p19 | executed-current | 实际成长故事 · 2026-10-04 | evidence/current/book-controls-results.json |
| m08-p04 | m08-p01 | executed-current | 返回 | evidence/current/book-controls-results.json |
| m08-p04 | m08-p05 | executed-current | 下一步：选择主题 | evidence/current/book-controls-results.json |
| m08-p05 | m08-p04 | executed-current | 返回上一步 | evidence/current/book-controls-results.json |
| m08-p05 | m08-p06 | executed-current | 下一步：选择素材 | evidence/current/book-controls-results.json |
| m08-p06 | m08-p05 | executed-current | 返回上一步 | evidence/current/book-controls-results.json |
| m08-p06 | m08-p07 | executed-current | 开始编排 | evidence/current/book-controls-results.json |
| m08-p07 | m08-p06 | executed-current | 返回素材选择 | evidence/current/book-controls-results.json |
| m08-p07 | m08-p13 | executed-current | 暂不放入 | evidence/current/book-controls-results.json |
| m08-p07 | m08-p08 | executed-current | 放入回忆册 | evidence/current/book-controls-results.json |
| m08-p07 | m08-p06 | executed-current | 重新选择素材 | evidence/current/book-controls-results.json |
| m08-p08 | m08-p07 | executed-current | 返回素材预览 | evidence/current/book-controls-results.json |
| m08-p08 | m08-p09 | executed-current | 使用这个模板 | evidence/current/book-controls-results.json |
| m08-p09 | m08-p08 | executed-current | 返回版式选择 | evidence/current/book-controls-results.json |
| m08-p09 | m08-p08 | executed-current | 换版式 换一种排版 | evidence/current/book-controls-results.json |
| m08-p09 | m08-p13 | executed-current | 完成这一页 | evidence/current/book-controls-results.json |
| m08-p10 | m08-p08 | executed-current | 返回 | evidence/current/book-controls-results.json |
| m08-p10 | m08-p13 | executed-current | 完成这一页 | evidence/current/book-controls-results.json |
| m08-p10 | m08-p08 | executed-current | 保留草稿换模板 | evidence/current/book-controls-results.json |
| m08-p11 | m08-p08 | executed-current | 返回版式选择 | evidence/current/book-controls-results.json |
| m08-p11 | m08-p13 | executed-current | 完成这一页 ♡ | evidence/current/book-controls-results.json |
| m08-p11 | m08-p08 | executed-current | 保留草稿换模板 | evidence/current/book-controls-results.json |
| m08-p12 | m08-p08 | executed-current | 返回版式选择 | evidence/current/book-controls-results.json |
| m08-p12 | m08-p13 | executed-current | 完成这一页 | evidence/current/book-controls-results.json |
| m08-p12 | m08-p08 | executed-current | 保留草稿换模板 | evidence/current/book-controls-results.json |
| m08-p13 | m08-p06 | executed-current | 返回编排 | evidence/current/book-controls-results.json |
| m08-p13 | m08-p14 | executed-current | 保存排列 | evidence/current/book-controls-results.json |
| m08-p13 | m08-p09 | executed-current | 共同日记 | evidence/current/book-controls-results.json |
| m08-p13 | m08-p10 | executed-current | 共同照片 | evidence/current/book-controls-results.json |
| m08-p13 | m08-p11 | executed-current | 共同重要时刻 | evidence/current/book-controls-results.json |
| m08-p13 | m08-p08 | executed-current | 添加书页 | evidence/current/book-controls-results.json |
| m08-p14 | m08-p15 | executed-current | 开始翻阅 | evidence/current/book-controls-results.json |
| m08-p14 | m08-p13 | executed-current | 继续整理 | evidence/current/book-controls-results.json |
| m08-p14 | m08-p01 | executed-current | 返回书架 | evidence/current/book-controls-results.json |
| m08-p15 | m08-p01 | executed-current | 返回书架 | evidence/current/book-controls-results.json |
| m08-p15 | m08-p16 | executed-current | 从第 1 页开始 → | evidence/current/book-controls-results.json |
| m08-p15 | m08-p21 | executed-current | 管理这本回忆册 | evidence/current/book-controls-results.json |
| m08-p15 | m08-p16 | executed-current | 共同日记 | evidence/current/book-controls-results.json |
| m08-p15 | m08-p16 | executed-current | 共同照片 | evidence/current/book-controls-results.json |
| m08-p15 | m08-p16 | executed-current | 共同重要时刻 | evidence/current/book-controls-results.json |
| m08-p16 | m08-p15 | executed-current | 返回 | evidence/current/book-controls-results.json |
| m08-p16 | m08-p15 | executed-current | 目录 | evidence/current/book-controls-results.json |
| m08-p16 | m03-p12 | executed-current | 查看原始共同记录 | evidence/current/book-controls-results.json |
| m08-p16 | m08-p17 | executed-current | 阅读工具 | evidence/current/book-controls-results.json |
| m08-p17 | m08-p16 | executed-current | 返回阅读 | evidence/current/book-controls-results.json |
| m08-p17 | m08-p15 | executed-current | 目录 查看全书目录和章节 | evidence/current/book-controls-results.json |
| m08-p17 | m08-p18 | executed-current | 添加补页 在书中添加新的补充页 | evidence/current/book-controls-results.json |
| m08-p17 | m08-p13 | executed-current | 整理这本书 调整页序、重命名、导出等 | evidence/current/book-controls-results.json |
| m08-p17 | m08-p21 | executed-current | 管理这本书 · 书名、归档、导出与删除 | evidence/current/book-controls-results.json |
| m08-p18 | m08-p16 | executed-current | 返回阅读 | evidence/current/book-controls-results.json |
| m08-p18 | m08-p15 | executed-current | 回到目录 | evidence/current/book-controls-results.json |
| m08-p18 | m08-p19 | executed-current | 选择回应方式 | evidence/current/book-controls-results.json |
| m08-p19 | m08-p18 | executed-current | 返回补页选择 | evidence/current/book-controls-results.json |
| m08-p19 | m08-p20 | executed-current | 放进回忆书 | evidence/current/book-controls-results.json |
| m08-p20 | m08-p17 | executed-current | 返回阅读工具 | evidence/current/book-controls-results.json |
| m08-p20 | m08-p15 | executed-current | 目录 | evidence/current/book-controls-results.json |
| m08-p20 | m03-p12 | executed-current | 查看原始共同记录 | evidence/current/book-controls-results.json |
| m08-p20 | m08-p16 | executed-current | 上一页 | evidence/current/book-controls-results.json |
| m08-p20 | m08-p17 | executed-current | 阅读工具 | evidence/current/book-controls-results.json |
| m08-p21 | m08-p15 | executed-current | 返回阅读 | evidence/current/book-controls-results.json |
| m08-p21 | m08-p13 | executed-current | 整理页序 | evidence/current/book-controls-results.json |
| m08-p21 | m08-p05 | executed-current | 修改主题与封面 | evidence/current/book-controls-results.json |
| m01-p01 | m01-p02 | code-candidate | 登录并开始 | 当前运行回调；未执行 |
| m01-p01 | m01-p03 | code-candidate | 创建账号 | 当前运行回调；未执行 |
| m01-p02 | m01-p01 | code-candidate | 返回 | 当前运行回调；未执行 |
| m01-p02 | m01-p04 | code-candidate | 忘记密码？ | 当前运行回调；未执行 |
| m01-p02 | m01-p03 | code-candidate | 创建账号 | 当前运行回调；未执行 |
| m01-p03 | m01-p01 | code-candidate | 返回欢迎页 | 当前运行回调；未执行 |
| m01-p03 | m01-p02 | code-candidate | 去登录 | 当前运行回调；未执行 |
| m01-p04 | m01-p02 | code-candidate | 返回 | 当前运行回调；未执行 |
| m01-p04 | m01-p02 | code-candidate | 返回登录 | 当前运行回调；未执行 |
| m01-p05 | m01-p04 | code-candidate | 返回找回密码 | 当前运行回调；未执行 |
| m01-p06 | m01-p02 | code-candidate | 返回 | 当前运行回调；未执行 |
| m01-p06 | m01-p04 | code-candidate | 找回密码 | 当前运行回调；未执行 |
| m01-p07 | m01-p04 | code-candidate | 返回 | 当前运行回调；未执行 |
| m01-p07 | m01-p03 | code-candidate | 没收到验证码？换个方式 | 当前运行回调；未执行 |
| m01-p07 | m01-p04 | code-candidate | 没收到验证码？换个方式 | 当前运行回调；未执行 |
| m01-p08 | m01-p02 | code-candidate | 返回登录 | 当前运行回调；未执行 |
| m02-p01 | m01-p02 | code-candidate | 返回登录 | 当前运行回调；未执行 |
| m02-p01 | m02-p02 | code-candidate | 邀请 TA 加入 生成专属邀请码 | 当前运行回调；未执行 |
| m02-p01 | m02-p03 | code-candidate | 邀请 TA 加入 生成专属邀请码 | 当前运行回调；未执行 |
| m02-p01 | m02-p09 | code-candidate | 邀请 TA 加入 生成专属邀请码 | 当前运行回调；未执行 |
| m02-p01 | m02-p02 | code-candidate | 输入 TA 的邀请码 接受一份特别邀请 | 当前运行回调；未执行 |
| m02-p01 | m02-p03 | code-candidate | 输入 TA 的邀请码 接受一份特别邀请 | 当前运行回调；未执行 |
| m02-p01 | m02-p09 | code-candidate | 输入 TA 的邀请码 接受一份特别邀请 | 当前运行回调；未执行 |
| m02-p02 | m02-p01 | code-candidate | 返回建立关系 | 当前运行回调；未执行 |
| m02-p02 | m02-p03 | code-candidate | 发送给微信好友 | 当前运行回调；未执行 |
| m02-p02 | m02-p07 | code-candidate | 发送给微信好友 | 当前运行回调；未执行 |
| m02-p03 | m02-p01 | code-candidate | 返回 | 当前运行回调；未执行 |
| m02-p03 | m02-p01 | code-candidate | 请让 TA 分享给你 | 当前运行回调；未执行 |
| m02-p04 | m02-p03 | code-candidate | 返回 | 当前运行回调；未执行 |
| m02-p04 | m02-p01 | code-candidate | 暂不接受 | 当前运行回调；未执行 |
| m02-p05 | m03-p05 | code-candidate | 去写第一篇共同日记 ♡ | 当前运行回调；未执行 |
| m02-p05 | m02-p06 | code-candidate | 完善情侣资料 | 当前运行回调；未执行 |
| m02-p06 | m02-p05 | code-candidate | 返回 | 当前运行回调；未执行 |
| m02-p07 | m02-p02 | code-candidate | 返回邀请卡 | 当前运行回调；未执行 |
| m02-p07 | m02-p03 | code-candidate | 复制邀请链接 | 当前运行回调；未执行 |
| m02-p08 | m02-p01 | code-candidate | 请 TA 重新邀请 | 当前运行回调；未执行 |
| m02-p08 | m02-p03 | code-candidate | 重新输入邀请码 | 当前运行回调；未执行 |
| m02-p09 | m02-p06 | code-candidate | 查看关系设置 | 当前运行回调；未执行 |
| m03-p01 | m03-p03 | code-candidate | 搜索共同记录 | 当前运行回调；未执行 |
| m03-p01 | m03-p05 | code-candidate | 写日记 | 当前运行回调；未执行 |
| m03-p01 | m03-p11 | code-candidate | 添加照片 | 当前运行回调；未执行 |
| m03-p01 | m05-p01 | code-candidate | 去童话工坊，把回忆变成故事 › | 当前运行回调；未执行 |
| m03-p02 | m03-p01 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m03-p03 | m03-p02 | code-candidate | 返回首页 | 当前运行回调；未执行 |
| m03-p03 | m03-p03 | code-candidate | 清除搜索 | 当前运行回调；未执行 |
| m03-p03 | m03-p04 | code-candidate | 清除搜索 | 当前运行回调；未执行 |
| m03-p04 | m03-p03 | code-candidate | 返回搜索 | 当前运行回调；未执行 |
| m03-p04 | m03-p03 | code-candidate | 清除 | 当前运行回调；未执行 |
| m03-p04 | m03-p03 | code-candidate | 重新搜索 | 当前运行回调；未执行 |
| m03-p05 | m03-p02 | code-candidate | 返回日记列表 | 当前运行回调；未执行 |
| m03-p05 | m03-p06 | code-candidate | 返回日记列表 | 当前运行回调；未执行 |
| m03-p05 | m03-p07 | code-candidate | 返回日记列表 | 当前运行回调；未执行 |
| m03-p05 | m03-p08 | code-candidate | 返回日记列表 | 当前运行回调；未执行 |
| m03-p06 | m03-p02 | code-candidate | 返回首页 | 当前运行回调；未执行 |
| m03-p06 | m03-p06 | code-candidate | 返回首页 | 当前运行回调；未执行 |
| m03-p06 | m03-p07 | code-candidate | 返回首页 | 当前运行回调；未执行 |
| m03-p06 | m03-p08 | code-candidate | 返回首页 | 当前运行回调；未执行 |
| m03-p06 | m03-p05 | code-candidate | 写日记 | 当前运行回调；未执行 |
| m03-p06 | m03-p05 | code-candidate | 写第一篇日记 | 当前运行回调；未执行 |
| m03-p07 | m03-p02 | code-candidate | 返回日记列表 | 当前运行回调；未执行 |
| m03-p07 | m03-p06 | code-candidate | 返回日记列表 | 当前运行回调；未执行 |
| m03-p07 | m03-p07 | code-candidate | 返回日记列表 | 当前运行回调；未执行 |
| m03-p07 | m03-p08 | code-candidate | 返回日记列表 | 当前运行回调；未执行 |
| m03-p08 | m03-p02 | code-candidate | 返回日记列表 | 当前运行回调；未执行 |
| m03-p08 | m03-p06 | code-candidate | 返回日记列表 | 当前运行回调；未执行 |
| m03-p08 | m03-p07 | code-candidate | 返回日记列表 | 当前运行回调；未执行 |
| m03-p08 | m03-p08 | code-candidate | 返回日记列表 | 当前运行回调；未执行 |
| m03-p09 | m03-p02 | code-candidate | 返回首页 | 当前运行回调；未执行 |
| m03-p09 | m03-p09 | code-candidate | 返回首页 | 当前运行回调；未执行 |
| m03-p09 | m03-p10 | code-candidate | 返回首页 | 当前运行回调；未执行 |
| m03-p09 | m03-p11 | code-candidate | 添加第一张照片 | 当前运行回调；未执行 |
| m03-p09 | m03-p11 | code-candidate | 从系统相册选择 | 当前运行回调；未执行 |
| m03-p10 | m03-p09 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m03-p11 | m03-p02 | code-candidate | 返回相册 | 当前运行回调；未执行 |
| m03-p11 | m03-p09 | code-candidate | 返回相册 | 当前运行回调；未执行 |
| m03-p11 | m03-p10 | code-candidate | 返回相册 | 当前运行回调；未执行 |
| m03-p12 | m03-p02 | code-candidate | 返回照片相册 | 当前运行回调；未执行 |
| m03-p12 | m03-p09 | code-candidate | 返回照片相册 | 当前运行回调；未执行 |
| m03-p12 | m03-p10 | code-candidate | 返回照片相册 | 当前运行回调；未执行 |
| m03-p12 | m03-p10 | code-candidate | 返回相册 | 当前运行回调；未执行 |
| m04-p01 | m04-p02 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m04-p02 | m04-p04 | code-candidate | 从共同记录中收录 | 当前运行回调；未执行 |
| m04-p02 | m04-p04 | code-candidate | 新建重要时刻 | 当前运行回调；未执行 |
| m04-p02 | m04-p07 | code-candidate | 纪念日 | 当前运行回调；未执行 |
| m04-p02 | m04-p08 | code-candidate | 纪念日 | 当前运行回调；未执行 |
| m04-p02 | m04-p12 | code-candidate | 时光胶囊 | 当前运行回调；未执行 |
| m04-p02 | m04-p16 | code-candidate | 悄悄留言 | 当前运行回调；未执行 |
| m04-p02 | m04-p17 | code-candidate | 悄悄留言 | 当前运行回调；未执行 |
| m04-p02 | m04-p05 | code-candidate | 共同提醒 | 当前运行回调；未执行 |
| m04-p03 | m04-p04 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p04 | m04-p04 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p04 | m03-p05 | code-candidate | 关联共同记录，已选 0 条 | 当前运行回调；未执行 |
| m04-p05 | m04-p06 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m04-p06 | m04-p01 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p06 | m04-p05 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p06 | m04-p06 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p06 | m04-p07 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p06 | m04-p08 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p06 | m04-p09 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p06 | m04-p10 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p06 | m04-p01 | code-candidate | 去看看重要时刻 | 当前运行回调；未执行 |
| m04-p07 | m04-p08 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m04-p08 | m04-p01 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p08 | m04-p05 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p08 | m04-p06 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p08 | m04-p07 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p08 | m04-p08 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p08 | m04-p09 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p08 | m04-p10 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p08 | m04-p09 | code-candidate | 添加第一个纪念日 | 当前运行回调；未执行 |
| m04-p09 | m04-p01 | code-candidate | 返回纪念日列表 | 当前运行回调；未执行 |
| m04-p09 | m04-p05 | code-candidate | 返回纪念日列表 | 当前运行回调；未执行 |
| m04-p09 | m04-p06 | code-candidate | 返回纪念日列表 | 当前运行回调；未执行 |
| m04-p09 | m04-p07 | code-candidate | 返回纪念日列表 | 当前运行回调；未执行 |
| m04-p09 | m04-p08 | code-candidate | 返回纪念日列表 | 当前运行回调；未执行 |
| m04-p09 | m04-p09 | code-candidate | 返回纪念日列表 | 当前运行回调；未执行 |
| m04-p09 | m04-p10 | code-candidate | 返回纪念日列表 | 当前运行回调；未执行 |
| m04-p10 | m04-p01 | code-candidate | 返回纪念日 | 当前运行回调；未执行 |
| m04-p10 | m04-p05 | code-candidate | 返回纪念日 | 当前运行回调；未执行 |
| m04-p10 | m04-p06 | code-candidate | 返回纪念日 | 当前运行回调；未执行 |
| m04-p10 | m04-p07 | code-candidate | 返回纪念日 | 当前运行回调；未执行 |
| m04-p10 | m04-p08 | code-candidate | 返回纪念日 | 当前运行回调；未执行 |
| m04-p10 | m04-p09 | code-candidate | 返回纪念日 | 当前运行回调；未执行 |
| m04-p10 | m04-p10 | code-candidate | 返回纪念日 | 当前运行回调；未执行 |
| m04-p12 | m04-p01 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p12 | m04-p12 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p12 | m04-p13 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p12 | m04-p13 | code-candidate | 新建时光胶囊 | 当前运行回调；未执行 |
| m04-p12 | m04-p13 | code-candidate | 写给未来的我们 | 当前运行回调；未执行 |
| m04-p12 | m04-p13 | code-candidate | ＋ 新建时光胶囊 | 当前运行回调；未执行 |
| m04-p13 | m04-p01 | code-candidate | 返回胶囊列表 | 当前运行回调；未执行 |
| m04-p13 | m04-p12 | code-candidate | 返回胶囊列表 | 当前运行回调；未执行 |
| m04-p13 | m04-p13 | code-candidate | 返回胶囊列表 | 当前运行回调；未执行 |
| m04-p14 | m04-p01 | code-candidate | 返回胶囊列表 | 当前运行回调；未执行 |
| m04-p14 | m04-p12 | code-candidate | 返回胶囊列表 | 当前运行回调；未执行 |
| m04-p14 | m04-p13 | code-candidate | 返回胶囊列表 | 当前运行回调；未执行 |
| m04-p15 | m04-p01 | code-candidate | 返回胶囊列表 | 当前运行回调；未执行 |
| m04-p15 | m04-p12 | code-candidate | 返回胶囊列表 | 当前运行回调；未执行 |
| m04-p15 | m04-p13 | code-candidate | 返回胶囊列表 | 当前运行回调；未执行 |
| m04-p16 | m04-p17 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m04-p17 | m04-p04 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p17 | m03-p06 | code-candidate | 去看看共同记录 | 当前运行回调；未执行 |
| m05-p01 | m05-p02 | code-candidate | 做成童话漫画 把回忆画成专属故事 留下一格格心动瞬间 | 当前运行回调；未执行 |
| m05-p01 | m05-p05 | code-candidate | 做成童话漫画 把回忆画成专属故事 留下一格格心动瞬间 | 当前运行回调；未执行 |
| m05-p01 | m05-p02 | code-candidate | 制作回忆影片 让重要时刻动起来 在光影里重温感动 | 当前运行回调；未执行 |
| m05-p01 | m05-p05 | code-candidate | 制作回忆影片 让重要时刻动起来 在光影里重温感动 | 当前运行回调；未执行 |
| m05-p01 | m05-p09 | code-candidate | 查看全部 › | 当前运行回调；未执行 |
| m05-p01 | m05-p02 | code-candidate | 开始一次创作 | 当前运行回调；未执行 |
| m05-p02 | m05-p08 | code-candidate | 返回童话工坊 | 当前运行回调；未执行 |
| m05-p03 | m05-p08 | code-candidate | 返回素材选择 | 当前运行回调；未执行 |
| m05-p03 | m05-p10 | code-candidate | 默默 & 小满 可爱自然 · 清新温柔 | 当前运行回调；未执行 |
| m05-p03 | m05-p04 | code-candidate | 生成童话漫画 | 当前运行回调；未执行 |
| m05-p03 | m05-p06 | code-candidate | 生成童话漫画 | 当前运行回调；未执行 |
| m05-p03 | m05-p09 | code-candidate | 暂存创作草稿 | 当前运行回调；未执行 |
| m05-p04 | m05-p08 | code-candidate | 返回素材选择 | 当前运行回调；未执行 |
| m05-p04 | m05-p10 | code-candidate | 他  阳光温柔 | 当前运行回调；未执行 |
| m05-p04 | m05-p10 | code-candidate | 她  温柔爱笑 | 当前运行回调；未执行 |
| m05-p04 | m05-p04 | code-candidate | 生成童话漫画 | 当前运行回调；未执行 |
| m05-p04 | m05-p06 | code-candidate | 生成童话漫画 | 当前运行回调；未执行 |
| m05-p04 | m05-p09 | code-candidate | 暂存创作草稿 | 当前运行回调；未执行 |
| m05-p05 | m05-p08 | code-candidate | 返回工坊 | 当前运行回调；未执行 |
| m05-p05 | m05-p04 | code-candidate | 生成回忆影片 | 当前运行回调；未执行 |
| m05-p05 | m05-p06 | code-candidate | 生成回忆影片 | 当前运行回调；未执行 |
| m05-p05 | m05-p09 | code-candidate | 暂存创作草稿 | 当前运行回调；未执行 |
| m05-p06 | m05-p09 | code-candidate | 返回我的创作 | 当前运行回调；未执行 |
| m05-p07 | m05-p09 | code-candidate | 返回我的创作 | 当前运行回调；未执行 |
| m05-p08 | m05-p09 | code-candidate | 返回我的创作 | 当前运行回调；未执行 |
| m05-p09 | m05-p02 | code-candidate | 开始创作 | 当前运行回调；未执行 |
| m05-p09 | m05-p02 | code-candidate | 开始一次创作 | 当前运行回调；未执行 |
| m05-p09 | m05-p01 | code-candidate | 返回童话工坊 | 当前运行回调；未执行 |
| m05-p10 | m05-p08 | code-candidate | 返回童话工坊 | 当前运行回调；未执行 |
| m06-p02 | m06-p01 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p02 | m06-p07 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p02 | m06-p08 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p02 | m06-p09 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p02 | m06-p10 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p02 | m06-p11 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p02 | m06-p01 | code-candidate | 保存资料 | 当前运行回调；未执行 |
| m06-p03 | m06-p01 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p03 | m06-p07 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p03 | m06-p08 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p03 | m06-p09 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p03 | m06-p10 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p03 | m06-p11 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p03 | m06-p09 | code-candidate | 共同空间设置 哪些记录邀请对方一起看 | 当前运行回调；未执行 |
| m06-p04 | m06-p01 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p04 | m06-p07 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p04 | m06-p08 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p04 | m06-p09 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p04 | m06-p10 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p04 | m06-p11 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p04 | m03-p05 | code-candidate | 写第一篇日记 | 当前运行回调；未执行 |
| m06-p05 | m06-p01 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p05 | m06-p07 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p05 | m06-p08 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p05 | m06-p09 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p05 | m06-p10 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p05 | m06-p11 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p06 | m06-p01 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p06 | m06-p07 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p06 | m06-p08 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p06 | m06-p09 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p06 | m06-p10 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p06 | m06-p11 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p07 | m06-p01 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p07 | m06-p07 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p07 | m06-p08 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p07 | m06-p09 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p07 | m06-p10 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p07 | m06-p11 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p08 | m06-p01 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p08 | m06-p07 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p08 | m06-p08 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p08 | m06-p09 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p08 | m06-p10 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p08 | m06-p11 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p08 | m01-p04 | code-candidate | 修改密码 | 当前运行回调；未执行 |
| m06-p09 | m06-p01 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p09 | m06-p07 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p09 | m06-p08 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p09 | m06-p09 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p09 | m06-p10 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p09 | m06-p11 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p10 | m06-p01 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p10 | m06-p07 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p10 | m06-p08 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p10 | m06-p09 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p10 | m06-p10 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p10 | m06-p11 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p11 | m06-p01 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p11 | m06-p07 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p11 | m06-p08 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p11 | m06-p09 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p11 | m06-p10 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p11 | m06-p11 | code-candidate | 返回设置 | 当前运行回调；未执行 |
| m06-p12 | m06-p01 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p12 | m06-p07 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p12 | m06-p08 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p12 | m06-p09 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p12 | m06-p10 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m06-p12 | m06-p11 | code-candidate | 返回我的与设置 | 当前运行回调；未执行 |
| m07-p01 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p04 | m03-p01 | code-candidate | 返回 | 当前运行回调；未执行 |
| m07-p02 | m02-p01 | code-candidate | 邀请 TA 一起领养 | 当前运行回调；未执行 |
| m07-p03 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p05 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p06 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p07 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p08 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p09 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p10 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p11 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p12 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p13 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p14 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p15 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p16 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p17 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p18 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p19 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p20 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p21 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p22 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p23 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p24 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m07-p25 | m07-p04 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m08-p01 | m08-p02 | observed-redirect | empty | evidence/current/current-runtime-inventory.json |
| m08-p02 | m03-p02 | code-candidate | 返回 | 当前运行回调；未执行 |
| m08-p03 | m03-p05 | code-candidate | 写共同日记 | 当前运行回调；未执行 |
| m08-p07 | m08-p06 | code-candidate | 暂不放入 | 当前运行回调；未执行 |
| m08-p07 | m08-p08 | code-candidate | 放入回忆册 | 当前运行回调；未执行 |
| m08-p10 | m08-p13 | code-candidate | 预览 | 当前运行回调；未执行 |
| m08-p14 | m08-p15 | code-candidate | 开始翻阅 | 当前运行回调；未执行 |
| m08-p14 | m08-p13 | code-candidate | 继续整理 | 当前运行回调；未执行 |
| m08-p15 | m08-p16 | code-candidate | 1. 那天，阳光刚刚好 1 | 当前运行回调；未执行 |
| m08-p15 | m08-p16 | code-candidate | 2. 一起吃的第一支冰淇淋 2 | 当前运行回调；未执行 |
| m08-p15 | m08-p16 | code-candidate | 3. 藏在风里的喜欢 3 | 当前运行回调；未执行 |
| m08-p15 | m08-p16 | code-candidate | 4. 我们的第一张合照 有补页4 | 当前运行回调；未执行 |
| m08-p15 | m08-p16 | code-candidate | 5. 你笑起来真好看 5 | 当前运行回调；未执行 |
| m08-p15 | m08-p16 | code-candidate | 6. 夏天的傍晚，晚风很温柔 6 | 当前运行回调；未执行 |
| m08-p15 | m08-p16 | code-candidate | 7. 海边的日落与你 7 | 当前运行回调；未执行 |
| m08-p15 | m08-p16 | code-candidate | 8. 烟花下许的愿 8 | 当前运行回调；未执行 |
| m08-p15 | m08-p16 | code-candidate | 9. 手牵手，走很长很长的路 9 | 当前运行回调；未执行 |
| m08-p15 | m08-p16 | code-candidate | 10. 属于我们的歌单 10 | 当前运行回调；未执行 |
| m08-p15 | m08-p16 | code-candidate | 11. 一起看过的星星 11 | 当前运行回调；未执行 |
| m08-p15 | m08-p16 | code-candidate | 12. 八月，未完待续 12 | 当前运行回调；未执行 |
| m08-p15 | m08-p16 | code-candidate | 从第 1 页开始 → | 当前运行回调；未执行 |
| m08-p16 | m08-p17 | code-candidate | 目录 | 当前运行回调；未执行 |
| m08-p16 | m08-p18 | code-candidate | 下一页 | 当前运行回调；未执行 |
| m08-p17 | m08-p15 | code-candidate | 目录查看全书目录和章节 | 当前运行回调；未执行 |
| m08-p17 | m08-p19 | code-candidate | 书签查看和管理我的书签 | 当前运行回调；未执行 |
| m08-p17 | m08-p18 | code-candidate | 添加补页在书中添加新的补充页 | 当前运行回调；未执行 |
| m08-p17 | m08-p13 | code-candidate | 整理这本书调整页序、重命名、导出等 | 当前运行回调；未执行 |
| m08-p17 | m08-p21 | code-candidate | 更多设置阅读偏好、背景音乐等设置 | 当前运行回调；未执行 |
| m08-p18 | m08-p15 | code-candidate | 回到目录 | 当前运行回调；未执行 |
| m08-p20 | m08-p15 | code-candidate | 目录 | 当前运行回调；未执行 |
| m08-p21 | m08-p13 | code-candidate | 整理页序 | 当前运行回调；未执行 |
| m03-p01 | m03-p02 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m03-p02 | m03-p03 | code-candidate | 搜索共同记录 | 当前运行回调；未执行 |
| m03-p02 | m03-p05 | code-candidate | 写日记 记录心情 | 当前运行回调；未执行 |
| m03-p02 | m03-p11 | code-candidate | 添加照片 珍藏瞬间 | 当前运行回调；未执行 |
| m03-p02 | m05-p01 | code-candidate | 去童话工坊，把回忆变成故事 › | 当前运行回调；未执行 |
| m03-p02 | m03-p06 | code-candidate | 查看全部 › | 当前运行回调；未执行 |
| m03-p02 | m08-p01 | code-candidate | 共同测试册 从目录开始阅读 继续阅读 › | 当前运行回调；未执行 |
| m03-p02 | m04-p01 | code-candidate | 下一件重要时刻 未来的纪念日 · 79 天后 查看纪念日 › | 当前运行回调；未执行 |
| m03-p07 | m03-p05 | code-candidate | 编辑日记 | 当前运行回调；未执行 |
| m03-p07 | m03-p06 | code-candidate | 更多操作 | 当前运行回调；未执行 |
| m03-p08 | m03-p05 | code-candidate | 编辑日记 | 当前运行回调；未执行 |
| m03-p08 | m03-p06 | code-candidate | 更多操作 | 当前运行回调；未执行 |
| m03-p09 | m03-p10 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m03-p10 | m03-p02 | code-candidate | 返回首页 | 当前运行回调；未执行 |
| m03-p10 | m03-p09 | code-candidate | 返回首页 | 当前运行回调；未执行 |
| m03-p10 | m03-p10 | code-candidate | 返回首页 | 当前运行回调；未执行 |
| m03-p10 | m03-p11 | code-candidate | ＋ 添加照片 | 当前运行回调；未执行 |
| m03-p12 | m03-p11 | code-candidate | 编辑照片 | 当前运行回调；未执行 |
| m04-p01 | m04-p07 | code-candidate | 查看纪念日 | 当前运行回调；未执行 |
| m04-p01 | m04-p08 | code-candidate | 查看纪念日 | 当前运行回调；未执行 |
| m04-p01 | m04-p04 | code-candidate | 珍藏一个新时刻 | 当前运行回调；未执行 |
| m04-p01 | m04-p07 | code-candidate | 纪念日 | 当前运行回调；未执行 |
| m04-p01 | m04-p08 | code-candidate | 纪念日 | 当前运行回调；未执行 |
| m04-p01 | m04-p12 | code-candidate | 时光胶囊 | 当前运行回调；未执行 |
| m04-p01 | m04-p16 | code-candidate | 悄悄留言 | 当前运行回调；未执行 |
| m04-p01 | m04-p17 | code-candidate | 悄悄留言 | 当前运行回调；未执行 |
| m04-p01 | m04-p04 | code-candidate | 新建重要时刻 | 当前运行回调；未执行 |
| m04-p01 | m04-p05 | code-candidate | 共同提醒 | 当前运行回调；未执行 |
| m04-p02 | m04-p01 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m04-p03 | m04-p04 | code-candidate | 编辑时刻 | 当前运行回调；未执行 |
| m04-p05 | m04-p01 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p05 | m04-p05 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p05 | m04-p06 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p05 | m04-p07 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p05 | m04-p08 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p05 | m04-p09 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p05 | m04-p10 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p06 | m04-p05 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m04-p07 | m04-p01 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p07 | m04-p05 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p07 | m04-p06 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p07 | m04-p07 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p07 | m04-p08 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p07 | m04-p09 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p07 | m04-p10 | code-candidate | 返回重要时刻 | 当前运行回调；未执行 |
| m04-p07 | m04-p09 | code-candidate | 添加纪念日 | 当前运行回调；未执行 |
| m04-p08 | m04-p07 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m04-p10 | m04-p03 | code-candidate | 共同重要时刻 | 当前运行回调；未执行 |
| m04-p10 | m04-p09 | code-candidate | 编辑纪念日 | 当前运行回调；未执行 |
| m04-p11 | m04-p10 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m04-p14 | m04-p03 | code-candidate | 把这一刻收录进重要时刻 | 当前运行回调；未执行 |
| m04-p16 | m04-p17 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m05-p04 | m05-p03 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m05-p05 | m05-p03 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m05-p06 | m05-p08 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m05-p08 | m05-p08 | code-candidate | 返回我的创作 | 当前运行回调；未执行 |
| m05-p07 | m05-p08 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m07-p01 | m07-p03 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m07-p03 | m03-p01 | code-candidate | 返回 | 当前运行回调；未执行 |
| m07-p02 | m07-p03 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m07-p04 | m07-p03 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m07-p05 | m07-p06 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m07-p06 | m07-p05 | code-candidate | 和团团互动 | 当前运行回调；未执行 |
| m07-p06 | m07-p07 | code-candidate | 和团团互动 | 当前运行回调；未执行 |
| m07-p07 | m07-p06 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m07-p08 | m07-p09 | code-candidate | 喂给团团 | 当前运行回调；未执行 |
| m07-p09 | m07-p08 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m07-p10 | m07-p11 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m07-p11 | m07-p06 | code-candidate | 完成陪团团互动 | 当前运行回调；未执行 |
| m07-p11 | m07-p15 | code-candidate | 完成整理小屋 | 当前运行回调；未执行 |
| m07-p11 | m07-p10 | code-candidate | 再完成 3 次照顾 | 当前运行回调；未执行 |
| m07-p14 | m07-p15 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m07-p17 | m07-p19 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
| m07-p18 | m03-p05 | code-candidate | 关联共同记录 | 当前运行回调；未执行 |
| m07-p25 | m02-p01 | code-candidate | 暂时解除共同照顾 | 当前运行回调；未执行 |
| m08-p01 | m03-p02 | code-candidate | 返回首页 | 当前运行回调；未执行 |
| m08-p07 | m08-p13 | observed-redirect | populated | evidence/current/current-runtime-inventory.json |
