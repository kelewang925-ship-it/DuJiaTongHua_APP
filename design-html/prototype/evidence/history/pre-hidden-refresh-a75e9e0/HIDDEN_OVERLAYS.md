# 运行时隐藏弹层与控件目录

公共源码在本轮注销回滚修复中已变化。本文是此前阶段的历史证据；是否当前复验以IDENTITY_DELETION_IMPLEMENTATION和最新页面合同为准，不能据本文宣称全量当前通过。

后续当前关闭与二层取消证据见[OVERLAY_EXIT_PATHS](OVERLAY_EXIT_PATHS.md)，250条控件各自剩余行为见[HIDDEN_CONTROL_BEHAVIORS](HIDDEN_CONTROL_BEHAVIORS.md)。

使用八模块既有种子，独立浏览器上下文直接触发133个候选。报告保存实际弹层DOM、控件、处理函数、尺寸及焦点。当前只证明观察到的弹层与无修改时Escape关闭、存储保持、可用触发按钮焦点恢复；未观察到弹层不证明其他条件无弹层。

下表覆盖全部114页，不提升页面终验。空白观察的页仍需间接触发、空/失败/缺失条件审计。按钮具体提交、第二层弹窗、修改后关闭、提交途中取消、所有来源与五宽度继续。机器索引的observation_index等字段指向原报告，不靠标题去重忽略不同入口。

| 页面 | 类型 | 候选观察 | 出现弹层 | 当前条件无弹层 | 弹层控件观察 | 剩余 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| m01-p01 | 引导入口 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m01-p02 | 登录表单 | 2 | 2 | 0 | 2 | 间接／多层／dirty／提交取消／来源／布局 |
| m01-p03 | 注册表单 | 2 | 2 | 0 | 2 | 间接／多层／dirty／提交取消／来源／布局 |
| m01-p04 | 找回密码账号验证表单 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m01-p05 | 新密码表单 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m01-p06 | 登录表单／校验失败 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m01-p07 | 验证码表单／等待验证 | 1 | 1 | 0 | 3 | 间接／多层／dirty／提交取消／来源／布局 |
| m01-p08 | 密码重置成功状态 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m02-p01 | 关系建立入口 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m02-p02 | 邀请分享工具 | 1 | 1 | 0 | 4 | 间接／多层／dirty／提交取消／来源／布局 |
| m02-p03 | 邀请码表单 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m02-p04 | 关系确认决策 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m02-p05 | 绑定成功状态 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m02-p06 | 情侣资料表单 | 2 | 0 | 2 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m02-p07 | 邀请等待状态 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m02-p08 | 邀请码失效状态 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m02-p09 | 已有关系冲突状态 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m03-p01 | 首页／空记录 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m03-p02 | 首页／有记录 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m03-p03 | 搜索表单／初始 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m03-p04 | 搜索表单与结果列表 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m03-p05 | 日记编辑表单 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m03-p06 | 日记列表 | 1 | 1 | 0 | 4 | 间接／多层／dirty／提交取消／来源／布局 |
| m03-p07 | 日记详情／私密 | 1 | 1 | 0 | 2 | 间接／多层／dirty／提交取消／来源／布局 |
| m03-p08 | 日记详情与回应表单／共同 | 2 | 1 | 1 | 2 | 间接／多层／dirty／提交取消／来源／布局 |
| m03-p09 | 相册／空列表 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m03-p10 | 相册／照片网格 | 1 | 1 | 0 | 4 | 间接／多层／dirty／提交取消／来源／布局 |
| m03-p11 | 照片编辑表单 | 2 | 1 | 1 | 3 | 间接／多层／dirty／提交取消／来源／布局 |
| m03-p12 | 照片详情与回应表单 | 2 | 1 | 1 | 2 | 间接／多层／dirty／提交取消／来源／布局 |
| m04-p01 | 时刻册列表 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m04-p02 | 时刻册／空列表 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m04-p03 | 时刻详情 | 2 | 2 | 0 | 5 | 间接／多层／dirty／提交取消／来源／布局 |
| m04-p04 | 时刻编辑表单 | 2 | 1 | 1 | 2 | 间接／多层／dirty／提交取消／来源／布局 |
| m04-p05 | 共同提醒列表／未读 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m04-p06 | 共同提醒／空列表 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m04-p07 | 纪念日列表 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m04-p08 | 纪念日／空列表 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m04-p09 | 纪念日编辑表单 | 1 | 0 | 1 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m04-p10 | 纪念日详情／倒计时 | 1 | 1 | 0 | 2 | 间接／多层／dirty／提交取消／来源／布局 |
| m04-p11 | 纪念日详情／当天 | 1 | 1 | 0 | 2 | 间接／多层／dirty／提交取消／来源／布局 |
| m04-p12 | 胶囊列表 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m04-p13 | 胶囊编辑表单 | 1 | 0 | 1 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m04-p14 | 胶囊详情／已开启 | 1 | 1 | 0 | 2 | 间接／多层／dirty／提交取消／来源／布局 |
| m04-p15 | 胶囊详情／封存 | 1 | 1 | 0 | 2 | 间接／多层／dirty／提交取消／来源／布局 |
| m04-p16 | 共同留言聚合列表 | 1 | 0 | 1 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m04-p17 | 共同留言／空列表 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m05-p01 | 工坊入口与最近作品 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m05-p02 | 创作素材选择 | 1 | 1 | 0 | 3 | 间接／多层／dirty／提交取消／来源／布局 |
| m05-p03 | 回忆漫画编辑任务 | 2 | 1 | 1 | 3 | 间接／多层／dirty／提交取消／来源／布局 |
| m05-p04 | 照片漫画编辑任务 | 4 | 2 | 2 | 6 | 间接／多层／dirty／提交取消／来源／布局 |
| m05-p05 | 回忆影片编辑任务 | 2 | 2 | 0 | 7 | 间接／多层／dirty／提交取消／来源／布局 |
| m05-p06 | 生成进度任务状态 | 1 | 1 | 0 | 2 | 间接／多层／dirty／提交取消／来源／布局 |
| m05-p07 | 生成失败状态 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m05-p08 | 作品详情 | 2 | 2 | 0 | 6 | 间接／多层／dirty／提交取消／来源／布局 |
| m05-p09 | 作品列表 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m05-p10 | 主角资料编辑任务 | 1 | 0 | 1 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m06-p01 | 个人中心入口 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m06-p02 | 个人资料设置与编辑弹层 | 1 | 0 | 1 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m06-p03 | 共同空间设置 | 3 | 3 | 0 | 6 | 间接／多层／dirty／提交取消／来源／布局 |
| m06-p04 | 多类型草稿列表 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m06-p05 | 标签管理列表 | 5 | 5 | 0 | 17 | 间接／多层／dirty／提交取消／来源／布局 |
| m06-p06 | 会员权益说明与方案选择 | 2 | 2 | 0 | 3 | 间接／多层／dirty／提交取消／来源／布局 |
| m06-p07 | 设置入口 | 3 | 3 | 0 | 8 | 间接／多层／dirty／提交取消／来源／布局 |
| m06-p08 | 账号安全设置 | 5 | 5 | 0 | 12 | 间接／多层／dirty／提交取消／来源／布局 |
| m06-p09 | 共同可见设置 | 1 | 1 | 0 | 3 | 间接／多层／dirty／提交取消／来源／布局 |
| m06-p10 | 通知设置 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m06-p11 | 数据存储管理 | 2 | 2 | 0 | 4 | 间接／多层／dirty／提交取消／来源／布局 |
| m06-p12 | 帮助与关于工具 | 6 | 6 | 0 | 8 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p01 | 领养等待确认状态 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p02 | 宠物品种与名字选择任务 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p03 | 宠物空间入口 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p04 | 宠物空间／未领养 | 3 | 3 | 0 | 6 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p05 | 宠物互动成功状态 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p06 | 宠物互动操作 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p07 | 宠物互动／精力不足 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p08 | 宠物喂食操作 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p09 | 宠物喂食／资源不足 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p10 | 任务奖励成功状态 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p11 | 宠物任务列表 | 1 | 1 | 0 | 3 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p12 | 装扮选择与保存任务 | 5 | 4 | 1 | 8 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p13 | 装扮／资源不足 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p14 | 房间布置保存成功状态 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p15 | 房间布置选择与保存任务 | 4 | 2 | 2 | 4 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p16 | 房间布置／资源不足 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p17 | 成长故事／来源权限失效 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p18 | 成长故事列表 | 2 | 2 | 0 | 7 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p19 | 成长章节详情 | 2 | 2 | 0 | 6 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p20 | 成就奖励成功状态 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p21 | 成就列表 | 1 | 0 | 1 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p22 | 宠物收藏图鉴列表 | 9 | 1 | 8 | 5 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p23 | 图鉴条目详情 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p24 | 宠物数据导出与解除照顾确认 | 1 | 1 | 0 | 2 | 间接／多层／dirty／提交取消／来源／布局 |
| m07-p25 | 宠物设置 | 3 | 3 | 0 | 8 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p01 | 回忆册书架列表 | 1 | 1 | 0 | 1 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p02 | 回忆册／空书架 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p03 | 本月共同素材推荐 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p04 | 回忆册基础信息编辑任务 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p05 | 主题封面选择任务 | 1 | 1 | 0 | 2 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p06 | 共同素材选择任务 | 6 | 0 | 6 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p07 | 素材预览与确认 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p08 | 回忆页模板选择 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p09 | 日记摘录书页编辑任务 | 2 | 2 | 0 | 4 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p10 | 照片故事书页编辑任务 | 6 | 6 | 0 | 16 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p11 | 重要时刻书页编辑任务 | 3 | 3 | 0 | 7 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p12 | 作品宠物书页编辑任务 | 3 | 3 | 0 | 6 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p13 | 章节与页序编辑任务 | 6 | 6 | 0 | 28 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p14 | 建册完成状态 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p15 | 回忆册目录 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p16 | 沉浸阅读 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p17 | 阅读工具菜单页 | 1 | 1 | 0 | 1 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p18 | 双人补页模板选择 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p19 | 双人补页编辑任务 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p20 | 阅读／含补页 | 0 | 0 | 0 | 0 | 间接／多层／dirty／提交取消／来源／布局 |
| m08-p21 | 回忆册管理与删除确认 | 4 | 2 | 2 | 5 | 间接／多层／dirty／提交取消／来源／布局 |

## 实际触发与弹层

| 页与报告索引 | 触发 | 观察结果 | 标题／可见控件 |
| --- | --- | --- | --- |
| m01-p02 / 0 | 《用户协议》 | overlay observed; clean Escape checked | 《用户协议》：知道了 |
| m01-p02 / 1 | 《隐私政策》 | overlay observed; clean Escape checked | 《隐私政策》：知道了 |
| m01-p03 / 2 | 《用户协议》 | overlay observed; clean Escape checked | 《用户协议》：知道了 |
| m01-p03 / 3 | 《隐私政策》 | overlay observed; clean Escape checked | 《隐私政策》：知道了 |
| m01-p07 / 4 | 没收到验证码？换个方式 | overlay observed; clean Escape checked | 换一种验证方式：重新填写手机号、查看演示验证码、取消 |
| m02-p02 / 5 | 发送给微信好友 | overlay observed; clean Escape checked | 分享邀请：复制邀请链接、保存邀请卡、查看邀请进度、取消 |
| m02-p06 / 6 | 相遇日期 | native-field; not an overlay opening probe | 当前直接触发未观察到弹层 |
| m02-p06 / 7 | 共同纪念日 | native-field; not an overlay opening probe | 当前直接触发未观察到弹层 |
| m03-p06 / 8 | 筛选日记 | overlay observed; clean Escape checked | 筛选日记：可见范围、应用筛选、清除筛选、取消 |
| m03-p07 / 9 | 更多操作 | overlay observed; clean Escape checked | 日记操作：删除日记、取消 |
| m03-p08 / 10 | 发送留言 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m03-p08 / 11 | 更多操作 | overlay observed; clean Escape checked | 日记操作：删除日记、取消 |
| m03-p10 / 12 | 筛选照片 | overlay observed; clean Escape checked | 筛选照片：照片可见范围、应用筛选、清除筛选、取消 |
| m03-p11 / 13 | 照片日期 | native-field; not an overlay opening probe | 当前直接触发未观察到弹层 |
| m03-p11 / 14 | 添加标签 | overlay observed; clean Escape checked | 照片标签：编辑照片标签、使用这些标签、取消 |
| m03-p12 / 15 | 发送留言 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m03-p12 / 16 | 更多操作 | overlay observed; clean Escape checked | 照片操作：删除照片、取消 |
| m04-p03 / 17 | 悄悄留言 1 条 | overlay observed; clean Escape checked | 时刻回应：回应这个时刻、发送回应、取消 |
| m04-p03 / 18 | 更多操作 | overlay observed; clean Escape checked | 时刻操作：删除重要时刻、取消 |
| m04-p04 / 19 | 发生日期 | native-field; not an overlay opening probe | 当前直接触发未观察到弹层 |
| m04-p04 / 20 | 关联共同记录，已选 0 条 | overlay observed; clean Escape checked | 选择共同记录：继续创建时刻、去写日记 |
| m04-p09 / 21 | 纪念日日期 | native-field; not an overlay opening probe | 当前直接触发未观察到弹层 |
| m04-p10 / 22 | 更多操作 | overlay observed; clean Escape checked | 纪念日操作：删除纪念日、取消 |
| m04-p11 / 23 | 更多操作 | overlay observed; clean Escape checked | 纪念日操作：删除纪念日、取消 |
| m04-p13 / 24 | opening | native-field; not an overlay opening probe | 当前直接触发未观察到弹层 |
| m04-p14 / 25 | 更多胶囊操作 | overlay observed; clean Escape checked | 胶囊操作：删除胶囊、取消 |
| m04-p15 / 26 | 更多胶囊操作 | overlay observed; clean Escape checked | 胶囊操作：删除胶囊、取消 |
| m04-p16 / 27 | 查看原记录 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m05-p02 / 28 | 用这些素材开始 | overlay observed; clean Escape checked | 选择共同素材：source、使用这段回忆、取消 |
| m05-p03 / 29 | 默默 & 小满 可爱自然 · 清新温柔 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m05-p03 / 30 | 创作草稿操作 | overlay observed; clean Escape checked | 创作操作：收藏作品、删除作品、取消 |
| m05-p04 / 31 | 他  阳光温柔 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m05-p04 / 32 | 她  温柔爱笑 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m05-p04 / 33 | 创作草稿操作 | overlay observed; clean Escape checked | 创作操作：收藏作品、删除作品、取消 |
| m05-p04 / 34 | 选择照片 | overlay observed; clean Escape checked | 选择共同素材：source、使用这些素材、取消 |
| m05-p05 / 35 | 选择共同片段 | overlay observed; clean Escape checked | 片段类型：共同日记、相册照片、重要时刻、取消 |
| m05-p05 / 36 | 创作草稿操作 | overlay observed; clean Escape checked | 创作操作：收藏作品、删除作品、取消 |
| m05-p06 / 37 | 取消生成 | overlay observed; clean Escape checked | 取消这次生成？：继续生成、保留草稿并取消 |
| m05-p08 / 38 | 给另一半看看 | overlay observed; clean Escape checked | 给另一半看看：当前原型作品链接、复制作品链接、取消 |
| m05-p08 / 39 | 更多作品操作 | overlay observed; clean Escape checked | 创作操作：收藏作品、删除作品、取消 |
| m05-p10 / 40 | 更新我们的主角 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m06-p02 / 41 | birthday | native-field; not an overlay opening probe | 当前直接触发未观察到弹层 |
| m06-p03 / 42 | 共同昵称 共同小屋 | overlay observed; clean Escape checked | 共同昵称：共同昵称、保存、取消 |
| m06-p03 / 43 | 关联状态 | overlay observed; clean Escape checked | 关联状态：知道了 |
| m06-p03 / 44 | 解除关联 | overlay observed; clean Escape checked | 请求解除关联？：取消、请求解除关联 |
| m06-p05 / 45 | 新建标签 | overlay observed; clean Escape checked | 新建标签：标签名称、标签范围、保存标签、取消 |
| m06-p05 / 46 | 新建标签 | overlay observed; clean Escape checked | 新建标签：标签名称、标签范围、保存标签、取消 |
| m06-p05 / 47 | 个人标签 | overlay observed; clean Escape checked | 个人标签：编辑标签、删除标签、取消 |
| m06-p05 / 48 | 共同标签 | overlay observed; clean Escape checked | 共同标签：编辑标签、删除标签、取消 |
| m06-p05 / 49 | 旅行 | overlay observed; clean Escape checked | 旅行：编辑标签、删除标签、取消 |
| m06-p06 / 50 | 开通童话会员 | overlay observed; clean Escape checked | 开通演示会员？：取消、开通演示会员 |
| m06-p06 / 51 | 查看会员说明 › | overlay observed; clean Escape checked | 童话会员说明：知道了 |
| m06-p07 / 52 | 显示与外观 | overlay observed; clean Escape checked | 显示与外观：动效、保存、取消 |
| m06-p07 / 53 | 语言 | overlay observed; clean Escape checked | 语言：简体中文、English · 尚无译稿、取消 |
| m06-p07 / 54 | 退出登录 | overlay observed; clean Escape checked | 退出当前登录？：继续使用、确认退出 |
| m06-p08 / 55 | 绑定手机 | overlay observed; clean Escape checked | 绑定手机（本地演示）：手机号、演示验证码 284631、保存、取消 |
| m06-p08 / 56 | 登录设备 当前设备安全 | overlay observed; clean Escape checked | 登录设备：知道了 |
| m06-p08 / 57 | 两步验证 · 未开启 | overlay observed; clean Escape checked | 开启两步验证演示：演示验证码 284631、保存、取消 |
| m06-p08 / 58 | 退出登录 | overlay observed; clean Escape checked | 退出当前登录？：继续使用、确认退出 |
| m06-p08 / 59 | 注销账号 | overlay observed; clean Escape checked | 注销本地演示账号？：取消、继续身份确认 |
| m06-p09 / 60 | 默认可见范围 共同可见 | overlay observed; clean Escape checked | 新记录默认可见范围：仅自己可见、共同可见、取消 |
| m06-p11 / 61 | 存储空间管理 | overlay observed; clean Escape checked | 本地存储空间：关闭、查看恢复原始副本 |
| m06-p11 / 62 | 清理缓存 0.0 KB | overlay observed; clean Escape checked | 清理浏览记录缓存？：取消、确认清理 |
| m06-p12 / 63 | 使用帮助 | overlay observed; clean Escape checked | 使用帮助：知道了 |
| m06-p12 / 64 | 意见反馈 | overlay observed; clean Escape checked | 意见反馈：意见反馈、保存反馈、取消 |
| m06-p12 / 65 | 隐私政策 | overlay observed; clean Escape checked | 隐私政策：知道了 |
| m06-p12 / 66 | 用户协议 | overlay observed; clean Escape checked | 用户协议：知道了 |
| m06-p12 / 67 | 检查更新 | overlay observed; clean Escape checked | 版本信息：知道了 |
| m06-p12 / 68 | 关于独家童话 | overlay observed; clean Escape checked | 关于独家童话：知道了 |
| m07-p04 / 69 | 照顾指南 | overlay observed; clean Escape checked | 一起照顾小伙伴：关闭、知道了 |
| m07-p04 / 70 | 宠物日记 | overlay observed; clean Escape checked | 从第一天开始记录：先看看、去领养 |
| m07-p04 / 71 | 先看看照顾指南 | overlay observed; clean Escape checked | 一起照顾小伙伴：关闭、知道了 |
| m07-p11 / 72 | 记录今天的小心情 | overlay observed; clean Escape checked | 宠物小心情：今天的小心情、保存小心情、取消 |
| m07-p12 / 73 | 小花围巾 已拥有 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m07-p12 / 74 | 格纹蝴蝶结 金币20 | overlay observed; clean Escape checked | 解锁格纹蝴蝶结：解锁并选择、取消 |
| m07-p12 / 75 | 星星领结 亲密度160 | overlay observed; clean Escape checked | 解锁星星领结：解锁并选择、取消 |
| m07-p12 / 76 | 蜜桃帽子 记录一页成长故事 | overlay observed; clean Escape checked | 解锁蜜桃帽子：解锁并选择、取消 |
| m07-p12 / 77 | 星光皇冠 星星30 | overlay observed; clean Escape checked | 解锁星光皇冠：解锁并选择、取消 |
| m07-p15 / 78 | 花朵地毯 已拥有 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m07-p15 / 79 | 格纹地毯 金币20 | overlay observed; clean Escape checked | 解锁格纹地毯：解锁并选择、取消 |
| m07-p15 / 80 | 月亮地毯 亲密度160 | overlay observed; clean Escape checked | 解锁月亮地毯：解锁并选择、取消 |
| m07-p15 / 81 | 野餐垫 照顾7个不同日期 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m07-p18 / 82 | 写一页成长故事 | overlay observed; clean Escape checked | 成长故事：成长故事内容、保存成长故事、取消 |
| m07-p18 / 83 | 关联共同记录 | overlay observed; clean Escape checked | 关联共同记录：共同日记、共同照片、共同重要时刻、取消 |
| m07-p19 / 84 | 写下今天的下一页 | overlay observed; clean Escape checked | 成长故事：成长故事内容、保存成长故事、取消 |
| m07-p19 / 85 | 回应这一页 | overlay observed; clean Escape checked | 回应：回应内容、保存回应、取消 |
| m07-p21 / 86 | 照顾7天 1 / 7 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m07-p22 / 87 | 小花围巾 已拥有 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m07-p22 / 88 | 格纹蝴蝶结 金币20 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m07-p22 / 89 | 星星领结 亲密度160 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m07-p22 / 90 | 蜜桃帽子 记录一页成长故事 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m07-p22 / 91 | 星光皇冠 星星30 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m07-p22 / 92 | 雨天小斗篷 照顾7个不同日期 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m07-p22 / 93 | 暖暖小马甲 金币20 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m07-p22 / 94 | 晚安铃铛 喂食20次 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m07-p22 / 95 | 认识小伙伴 | overlay observed; clean Escape checked | 四位小伙伴：小狗 · 正在共同照顾、小猫 · 首次领养可选、小兔 · 首次领养可选、小狐狸 · 首次领养可选、取消 |
| m07-p24 / 96 | 暂时解除共同照顾 | overlay observed; clean Escape checked | 暂停共同照顾？：继续照顾、确认暂停 |
| m07-p25 / 97 | 共同提醒 每天 20:30 · 本地提醒 | overlay observed; clean Escape checked | 提醒时间：每天提醒时间、保存提醒时间、取消 |
| m07-p25 / 98 | 仅我们可见说明 | overlay observed; clean Escape checked | 仅我们可见：关闭、知道了 |
| m07-p25 / 99 | 更多 | overlay observed; clean Escape checked | 宠物资料与数据：修改宠物名字、永久删除宠物数据、取消 |
| m08-p01 / 100 | 归档与草稿 | overlay observed; clean Escape checked | 归档与草稿：取消 |
| m08-p05 / 101 | 使用封面照片 | overlay observed; clean Escape checked | 选择共同素材：共同照片、取消 |
| m08-p06 / 102 | 共同日记 · 日记 · 2026-10-04 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m08-p06 / 103 | 共同照片 · 照片 · 2026-10-04 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m08-p06 / 104 | 共同重要时刻 · 时刻 · 2026-10-04 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m08-p06 / 105 | 实际工坊作品 · 工坊 · 2026-10-05 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m08-p06 / 106 | 实际成长故事 · 宠物 · 2026-10-04 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m08-p06 / 107 | 开始编排 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m08-p09 / 108 | 换摘录 换一段日记 | overlay observed; clean Escape checked | 选择共同素材：共同日记、取消 |
| m08-p09 / 109 | 换照片 换一张照片 | overlay observed; clean Escape checked | 选择共同素材：共同照片、取消 |
| m08-p10 / 110 | 预览 | overlay observed; clean Escape checked | 共同照片：继续编辑 |
| m08-p10 / 111 | 裁剪/替换 | overlay observed; clean Escape checked | 照片1：替换这张照片、裁剪这张照片、移除这张照片、取消 |
| m08-p10 / 112 | 裁剪/替换 | overlay observed; clean Escape checked | 选择共同素材：共同照片、取消 |
| m08-p10 / 113 | 裁剪/替换 | overlay observed; clean Escape checked | 选择共同素材：共同照片、取消 |
| m08-p10 / 114 | 添加照片 | overlay observed; clean Escape checked | 选择共同素材：共同照片、取消 |
| m08-p10 / 115 | 添加贴纸 | overlay observed; clean Escape checked | 选择贴纸：💗、⭐、🌸、😊、取消 |
| m08-p11 / 116 | 更换照片 | overlay observed; clean Escape checked | 选择共同素材：共同照片、取消 |
| m08-p11 / 117 | 选择时刻 › | overlay observed; clean Escape checked | 选择共同素材：共同重要时刻、取消 |
| m08-p11 / 118 | 添加一句话 | overlay observed; clean Escape checked | 一句话：书页寄语、保存一句话、取消 |
| m08-p12 / 119 | 工坊作品 | overlay observed; clean Escape checked | 选择共同素材：实际工坊作品、取消 |
| m08-p12 / 120 | 换内容 | overlay observed; clean Escape checked | 选择共同素材：实际成长故事、取消 |
| m08-p12 / 121 | 换照片 | overlay observed; clean Escape checked | 选择共同素材：共同照片、取消 |
| m08-p13 / 122 | 新增章节 | overlay observed; clean Escape checked | 章节：章节名、保存章节、取消 |
| m08-p13 / 123 | 章节操作「第一章」 | overlay observed; clean Escape checked | 第一章 · 章节操作：修改章节名、上移章节、下移章节、删除章节、取消 |
| m08-p13 / 124 | 页面操作「共同日记」 | overlay observed; clean Escape checked | 共同日记 · 页面操作：上移一页、下移一页、移动到另一章、删除书页、取消 |
| m08-p13 / 125 | 页面操作「共同照片」 | overlay observed; clean Escape checked | 共同照片 · 页面操作：上移一页、下移一页、移动到另一章、删除书页、取消 |
| m08-p13 / 126 | 章节操作「第二章」 | overlay observed; clean Escape checked | 第二章 · 章节操作：修改章节名、上移章节、下移章节、删除章节、取消 |
| m08-p13 / 127 | 页面操作「共同重要时刻」 | overlay observed; clean Escape checked | 共同重要时刻 · 页面操作：上移一页、下移一页、移动到另一章、删除书页、取消 |
| m08-p17 / 128 | 书签 查看和管理我的书签 | overlay observed; clean Escape checked | 我的书签：取消 |
| m08-p21 / 129 | 修改书名 | overlay observed; clean Escape checked | 书名：回忆册名称、保存书名、取消 |
| m08-p21 / 130 | 修改主题与封面 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m08-p21 / 131 | 归档回忆册 | no overlay in this initial fixture; other trigger conditions pending | 当前直接触发未观察到弹层 |
| m08-p21 / 132 | 删除这本回忆册 | overlay observed; clean Escape checked | 确定删除《共同测试册》？：取消、确认删除 |
