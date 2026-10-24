# 114 页状态补齐矩阵

当前752项初始控件全部复验通过，身份删除13项保留；其他隐藏条件及主要异常流程继续，全部114页最终验收仍未通过。详见REMAINING_INITIAL_REFRESH_IMPLEMENTATION。

本轮注销回滚修复后，13项身份删除和163项初始控件已当前验证；其余589初始控件为历史。运行观察228次已刷新，所有flow_verified保持false。

章节／书页候选删除25项当前证据见[BOOK_CANDIDATE_DELETIONS](BOOK_CANDIDATE_DELETIONS.md)，每页最终验收状态保持未通过。

记录类确认删除45项当前结果见[CONFIRMED_DELETIONS](CONFIRMED_DELETIONS.md)；未改变各页最终验收状态。

16保存表单47项当前结果与存储失败恢复见[OVERLAY_FORM_SAVES](OVERLAY_FORM_SAVES.md)，仅声明输入与首错范围；其他表单、字段条件和状态仍待终验。

补充当前代表性弹层关闭／dirty／二层取消498项证据：[OVERLAY_EXIT_PATHS](OVERLAY_EXIT_PATHS.md)。其他状态、字段和来源仍需逐项终验。

隐藏弹层当前代表性观察见[HIDDEN_OVERLAYS](HIDDEN_OVERLAYS.md)：99次无修改Escape关闭／存储／焦点通过，不能替代各动作与其他关闭状态终验。

列表与集合交互的逐页适用决定见[LIST_INTERACTIONS](LIST_INTERACTIONS.md)。该表不替代下列状态执行与终验。

日记m03-p05、照片m03-p11、时刻m04-p04的提交新增当前正文竞争／删除拒绝与新留言合并；m04-p16已读核对当前共同来源与留言。专项23项及指定回归当前265项，见[编辑当前内容](EDITOR_CURRENT_CONTENT_IMPLEMENTATION.md)。这不将下表尚待逐页确认的类型和状态自动判为终验通过。

m04-p15增加异常开启日期Error与明确修正Sheet；验证空／过去日期、dirty取消、失败／quota／竞争及坏根写入拒绝。m04-p14收录验证错关联、ID碰撞、private和当前sealed拒绝；原正常状态保持。五宽度Sheet另模拟44px顶部／34px底部安全区。 详见[胶囊日期与收录关联](CAPSULE_SEMANTIC_RECOVERY_IMPLEMENTATION.md)。

宠物与回忆册初始结构受损显示共享Error；恢复选择、危险确认、原文下载、容量不足、竞争、dirty输入和副本重下载另列专项证据。五宽度验证声明入口的44px按钮、Enter／Escape焦点和无横向溢出，仍不证明全部页面可访问性终验。 详见[宠物与回忆册结构恢复](PET_BOOK_RECOVERY_IMPLEMENTATION.md)。

数据与存储新增role=status备份说明，受损时提示恢复；手动备份仍有Loading和失败Toast，恢复后可重试。三类时间内容shared快照排除private及draft；accessible导出保留其内容，不清理源数据。 证据及边界见[备份保护与共享范围](BACKUP_PRESERVATION_IMPLEMENTATION.md)。

三类集合坏JSON／错误根／null／重复或缺失ID／字段错误有36项恢复，异常写入等46项、详情Error／Empty30项、纪念日日期修正1项证据。全部日期合法性、封存胶囊日期修正及失效引用仍开放。 证据及边界见[时刻／纪念日／胶囊恢复实施记录](TIME_COLLECTION_RECOVERY_IMPLEMENTATION.md)。

标签坏JSON／错误根／null／重复ID或名称／名称／范围异常增加恢复选择、原文下载、取消、最终危险确认、配额失败重试、竞争中止和外部重查状态；资料→记录→作品→标签为当前实际联合恢复顺序。 证据边界见[TAG_RECOVERY_IMPLEMENTATION](TAG_RECOVERY_IMPLEMENTATION.md)。

下表按明确页面职责、实际字段和控件契约更新适用需求；条件性要求仍需逐页决定。执行列记录初始控件证据，不能替代动态状态和最终验收。

| 页面 | 名称 | 类型 | 需要的状态/交互 | 执行状态 |
| --- | --- | --- | --- | --- |
| m01-p01 | 01-引导页 | 引导入口 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion | 初始控件当前2／历史0；观察2次；状态终验未完成 |
| m01-p02 | 02-登录页 | 登录表单 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前9／历史0；观察2次；状态终验未完成 |
| m01-p03 | 03-创建账号页 | 注册表单 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前12／历史0；观察2次；状态终验未完成 |
| m01-p04 | 04-找回密码账号验证页 | 找回密码账号验证表单 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入 | 初始控件当前6／历史0；观察2次；状态终验未完成 |
| m01-p05 | 05-找回密码设置新密码页 | 新密码表单 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入 | 初始控件当前6／历史0；观察2次；状态终验未完成 |
| m01-p06 | 06-登录页-校验失败 | 登录表单／校验失败 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入 | 初始控件当前5／历史0；观察2次；状态终验未完成 |
| m01-p07 | 07-验证码已发送-等待验证 | 验证码表单／等待验证 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前9／历史0；观察2次；状态终验未完成 |
| m01-p08 | 08-密码重置成功 | 密码重置成功状态 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入 | 初始控件当前1／历史0；观察2次；状态终验未完成 |
| m02-p01 | 01-建立情侣关系页 | 关系建立入口 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion | 初始控件当前3／历史0；观察2次；状态终验未完成 |
| m02-p02 | 02-分享邀请页 | 邀请分享工具 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前4／历史0；观察2次；状态终验未完成 |
| m02-p03 | 03-填写邀请码页 | 邀请码表单 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入 | 初始控件当前7／历史0；观察2次；状态终验未完成 |
| m02-p04 | 04-情侣关系确认页 | 关系确认决策 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入 | 初始控件当前3／历史0；观察2次；状态终验未完成 |
| m02-p05 | 05-情侣绑定成功页 | 绑定成功状态 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入 | 初始控件当前3／历史0；观察2次；状态终验未完成 |
| m02-p06 | 06-情侣信息设置页 | 情侣资料表单 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前5／历史0；观察2次；状态终验未完成 |
| m02-p07 | 07-等待TA确认 | 邀请等待状态 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入 | 初始控件当前3／历史0；观察2次；状态终验未完成 |
| m02-p08 | 08-邀请码失效或不可用 | 邀请码失效状态 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入 | 初始控件当前2／历史0；观察2次；状态终验未完成 |
| m02-p09 | 09-当前账号已有情侣关系 | 已有关系冲突状态 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入 | 初始控件当前2／历史0；观察2次；状态终验未完成 |
| m03-p01 | 01-首页与共同记录-无记录状态 | 首页／空记录 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定 | 初始控件当前0／历史9；观察2次；状态终验未完成 |
| m03-p02 | 01-首页与共同记录-正常态 | 首页／有记录 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion | 初始控件当前0／历史15；观察2次；状态终验未完成 |
| m03-p03 | 02-共同记录搜索页-初始状态 | 搜索表单／初始 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入 | 初始控件当前0／历史10；观察2次；状态终验未完成 |
| m03-p04 | 02-共同记录搜索页-结果状态 | 搜索表单与结果列表 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定 | 初始控件当前0／历史5；观察2次；状态终验未完成 |
| m03-p05 | 03-日记编辑页 | 日记编辑表单 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入 | 初始控件当前0／历史9；观察2次；状态终验未完成 |
| m03-p06 | 04-日记列表页 | 日记列表 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史8；观察2次；状态终验未完成 |
| m03-p07 | 05-日记详情页-仅自己可见 | 日记详情／私密 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史3；观察2次；状态终验未完成 |
| m03-p08 | 05-日记详情页-共同可见 | 日记详情与回应表单／共同 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史6；观察2次；状态终验未完成 |
| m03-p09 | 06-照片相册页-空状态 | 相册／空列表 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定 | 初始控件当前0／历史3；观察2次；状态终验未完成 |
| m03-p10 | 06-照片相册页-网格状态 | 相册／照片网格 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史8；观察2次；状态终验未完成 |
| m03-p11 | 07-照片上传页 | 照片编辑表单 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史10；观察2次；状态终验未完成 |
| m03-p12 | 08-照片详情页 | 照片详情与回应表单 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史6；观察2次；状态终验未完成 |
| m04-p01 | 01-重要时刻首页-正常态 | 时刻册列表 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定 | 初始控件当前0／历史15；观察2次；状态终验未完成 |
| m04-p02 | 01-重要时刻首页-空状态 | 时刻册／空列表 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定 | 初始控件当前0／历史11；观察2次；状态终验未完成 |
| m04-p03 | 02-重要时刻详情页 | 时刻详情 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史5；观察2次；状态终验未完成 |
| m04-p04 | 03-重要时刻新建编辑页 | 时刻编辑表单 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史11；观察2次；状态终验未完成 |
| m04-p05 | 04-共同提醒页-未读状态 | 共同提醒列表／未读 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定 | 初始控件当前0／历史2；观察2次；状态终验未完成 |
| m04-p06 | 04-共同提醒页-空状态 | 共同提醒／空列表 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定 | 初始控件当前0／历史2；观察2次；状态终验未完成 |
| m04-p07 | 05-纪念日管理页-正常态 | 纪念日列表 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定 | 初始控件当前0／历史9；观察2次；状态终验未完成 |
| m04-p08 | 05-纪念日管理页-空状态 | 纪念日／空列表 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定 | 初始控件当前0／历史2；观察2次；状态终验未完成 |
| m04-p09 | 06-纪念日添加编辑页 | 纪念日编辑表单 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史7；观察2次；状态终验未完成 |
| m04-p10 | 07-纪念日倒计时页-正常态 | 纪念日详情／倒计时 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史5；观察2次；状态终验未完成 |
| m04-p11 | 07-纪念日倒计时页-纪念日当天 | 纪念日详情／当天 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史5；观察2次；状态终验未完成 |
| m04-p12 | 08-时光胶囊列表页 | 胶囊列表 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定 | 初始控件当前0／历史8；观察2次；状态终验未完成 |
| m04-p13 | 09-时光胶囊编辑新建页 | 胶囊编辑表单 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史8；观察2次；状态终验未完成 |
| m04-p14 | 10-时光胶囊详情页-已开启 | 胶囊详情／已开启 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史3；观察2次；状态终验未完成 |
| m04-p15 | 10-时光胶囊详情页-未到期开启 | 胶囊详情／封存 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史3；观察2次；状态终验未完成 |
| m04-p16 | 11-悄悄留言列表页-正常态 | 共同留言聚合列表 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定 | 初始控件当前0／历史2；观察2次；状态终验未完成 |
| m04-p17 | 11-悄悄留言列表页-空状态 | 共同留言／空列表 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定 | 初始控件当前0／历史2；观察2次；状态终验未完成 |
| m05-p01 | 01-童话工坊首页 | 工坊入口与最近作品 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion | 初始控件当前0／历史11；观察2次；状态终验未完成 |
| m05-p02 | 02-创作素材选择页 | 创作素材选择 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史6；观察2次；状态终验未完成 |
| m05-p03 | 03-回忆转漫画编辑页 | 回忆漫画编辑任务 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史12；观察2次；状态终验未完成 |
| m05-p04 | 04-照片转漫画编辑页 | 照片漫画编辑任务 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史13；观察2次；状态终验未完成 |
| m05-p05 | 05-回忆影片编辑页 | 回忆影片编辑任务 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史11；观察2次；状态终验未完成 |
| m05-p06 | 06-魔法生成中页 | 生成进度任务状态 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史2；观察2次；状态终验未完成 |
| m05-p07 | 07-生成失败页 | 生成失败状态 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入 | 初始控件当前0／历史3；观察2次；状态终验未完成 |
| m05-p08 | 08-作品详情页 | 作品详情 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史14；观察2次；状态终验未完成 |
| m05-p09 | 09-我的创作页 | 作品列表 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定 | 初始控件当前0／历史14；观察2次；状态终验未完成 |
| m05-p10 | 10-我们的主角设定页 | 主角资料编辑任务 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入 | 初始控件当前0／历史6；观察2次；状态终验未完成 |
| m06-p01 | 01-我的与设置首页 | 个人中心入口 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion | 初始控件当前0／历史12；观察2次；状态终验未完成 |
| m06-p02 | 02-编辑个人资料页 | 个人资料设置与编辑弹层 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史8；观察2次；状态终验未完成 |
| m06-p03 | 03-我们的小世界页 | 共同空间设置 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史6；观察2次；状态终验未完成 |
| m06-p04 | 04-草稿箱页 | 多类型草稿列表 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定 | 初始控件当前0／历史6；观察2次；状态终验未完成 |
| m06-p05 | 05-标签管理页 | 标签管理列表 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史6；观察2次；状态终验未完成 |
| m06-p06 | 06-童话会员页 | 会员权益说明与方案选择 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史3；观察2次；状态终验未完成 |
| m06-p07 | 07-设置首页 | 设置入口 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史8；观察2次；状态终验未完成 |
| m06-p08 | 08-账号与安全页 | 账号安全设置 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史7；观察2次；状态终验未完成 |
| m06-p09 | 09-隐私与共同可见页 | 共同可见设置 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史6；观察2次；状态终验未完成 |
| m06-p10 | 10-通知设置页 | 通知设置 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion | 初始控件当前0／历史6；观察2次；状态终验未完成 |
| m06-p11 | 11-数据与存储页 | 数据存储管理 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史6；观察2次；状态终验未完成 |
| m06-p12 | 12-帮助与关于页 | 帮助与关于工具 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史7；观察2次；状态终验未完成 |
| m07-p01 | 60-共同领养页-等待确认 | 领养等待确认状态 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入 | 初始控件当前0／历史8；观察2次；状态终验未完成 |
| m07-p02 | 60-共同领养页-选择宠物 | 宠物品种与名字选择任务 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入 | 初始控件当前0／历史7；观察2次；状态终验未完成 |
| m07-p03 | 60-宠物空间首页-正常态 | 宠物空间入口 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion | 初始控件当前0／历史15；观察2次；状态终验未完成 |
| m07-p04 | 60-宠物空间首页-首次领养 | 宠物空间／未领养 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史10；观察2次；状态终验未完成 |
| m07-p05 | 61-宠物互动页-互动成功 | 宠物互动成功状态 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入 | 初始控件当前0／历史3；观察2次；状态终验未完成 |
| m07-p06 | 61-宠物互动页-正常态 | 宠物互动操作 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion | 初始控件当前0／历史6；观察2次；状态终验未完成 |
| m07-p07 | 61-宠物互动页-精力不足 | 宠物互动／精力不足 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion | 初始控件当前0／历史3；观察2次；状态终验未完成 |
| m07-p08 | 62-喂食页-正常态 | 宠物喂食操作 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion | 初始控件当前0／历史6；观察2次；状态终验未完成 |
| m07-p09 | 62-喂食页-资源不足 | 宠物喂食／资源不足 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion | 初始控件当前0／历史2；观察2次；状态终验未完成 |
| m07-p10 | 63-任务页-奖励领取 | 任务奖励成功状态 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入 | 初始控件当前0／历史2；观察2次；状态终验未完成 |
| m07-p11 | 63-任务页-正常态 | 宠物任务列表 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史9；观察2次；状态终验未完成 |
| m07-p12 | 64-宠物装扮页-正常态 | 装扮选择与保存任务 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入 | 初始控件当前0／历史11；观察2次；状态终验未完成 |
| m07-p13 | 64-宠物装扮页-资源不足 | 装扮／资源不足 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion | 初始控件当前0／历史2；观察2次；状态终验未完成 |
| m07-p14 | 65-房间布置页-保存成功 | 房间布置保存成功状态 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入 | 初始控件当前0／历史3；观察2次；状态终验未完成 |
| m07-p15 | 65-房间布置页-正常态 | 房间布置选择与保存任务 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入 | 初始控件当前0／历史10；观察2次；状态终验未完成 |
| m07-p16 | 65-房间布置页-资源不足 | 房间布置／资源不足 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入 | 初始控件当前0／历史2；观察2次；状态终验未完成 |
| m07-p17 | 66-成长故事页-回忆权限失效 | 成长故事／来源权限失效 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion | 初始控件当前0／历史2；观察2次；状态终验未完成 |
| m07-p18 | 66-成长故事页-正常态 | 成长故事列表 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史4；观察2次；状态终验未完成 |
| m07-p19 | 66-成长故事页-章节详情 | 成长章节详情 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史3；观察2次；状态终验未完成 |
| m07-p20 | 67-成就页-奖励领取 | 成就奖励成功状态 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入 | 初始控件当前0／历史2；观察2次；状态终验未完成 |
| m07-p21 | 67-成就页-正常态 | 成就列表 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定 | 初始控件当前0／历史10；观察2次；状态终验未完成 |
| m07-p22 | 68-宠物图鉴页-正常态 | 宠物收藏图鉴列表 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史13；观察2次；状态终验未完成 |
| m07-p23 | 68-宠物图鉴页-详情态 | 图鉴条目详情 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入 | 初始控件当前0／历史3；观察2次；状态终验未完成 |
| m07-p24 | 69-宠物设置页-导出与删除确认 | 宠物数据导出与解除照顾确认 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史4；观察2次；状态终验未完成 |
| m07-p25 | 69-宠物设置页-正常态 | 宠物设置 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史11；观察2次；状态终验未完成 |
| m08-p01 | 01-书架 | 回忆册书架列表 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史6；观察2次；状态终验未完成 |
| m08-p02 | 02-空书架 | 回忆册／空书架 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定 | 初始控件当前0／历史2；观察2次；状态终验未完成 |
| m08-p03 | 03-本月回忆推荐 | 本月共同素材推荐 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；Empty图形／说明／真实CTA；有异步读取时Loading／Error／重试；刷新／分页／长按／滑动适用决定 | 初始控件当前0／历史8；观察2次；状态终验未完成 |
| m08-p04 | 04-新建回忆册-基础信息 | 回忆册基础信息编辑任务 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入 | 初始控件当前0／历史7；观察2次；状态终验未完成 |
| m08-p05 | 05-主题与封面选择 | 主题封面选择任务 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史6；观察2次；状态终验未完成 |
| m08-p06 | 06-选择共同素材 | 共同素材选择任务 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入 | 初始控件当前0／历史13；观察2次；状态终验未完成 |
| m08-p07 | 07-素材预览与确认 | 素材预览与确认 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入 | 初始控件当前0／历史4；观察2次；状态终验未完成 |
| m08-p08 | 08-选择回忆页模板 | 回忆页模板选择 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入 | 初始控件当前0／历史8；观察2次；状态终验未完成 |
| m08-p09 | 09-日记摘录页编排 | 日记摘录书页编辑任务 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史9；观察2次；状态终验未完成 |
| m08-p10 | 10-照片故事页编排 | 照片故事书页编辑任务 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史13；观察2次；状态终验未完成 |
| m08-p11 | 11-重要时刻页编排 | 重要时刻书页编辑任务 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史8；观察2次；状态终验未完成 |
| m08-p12 | 12-作品与宠物成长页编排 | 作品宠物书页编辑任务 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史9；观察2次；状态终验未完成 |
| m08-p13 | 13-章节与页序整理 | 章节与页序编辑任务 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史12；观察2次；状态终验未完成 |
| m08-p14 | 14-建册完成 | 建册完成状态 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入 | 初始控件当前0／历史3；观察2次；状态终验未完成 |
| m08-p15 | 15-回忆册目录 | 回忆册目录 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion | 初始控件当前0／历史6；观察2次；状态终验未完成 |
| m08-p16 | 16-沉浸翻阅页 | 沉浸阅读 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入 | 初始控件当前0／历史7；观察2次；状态终验未完成 |
| m08-p17 | 17-阅读工具菜单 | 阅读工具菜单页 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史6；观察2次；状态终验未完成 |
| m08-p18 | 18-添加双人补页 | 双人补页模板选择 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入 | 初始控件当前0／历史6；观察2次；状态终验未完成 |
| m08-p19 | 19-双人补页编辑 | 双人补页编辑任务 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；输入或选择的focus／filled／error／disabled；可输入字段的typing／长度限制及及时校验；未保存返回／取消选择保护；有写入时提交loading／success／failure及保留输入 | 初始控件当前0／历史8；观察2次；状态终验未完成 |
| m08-p20 | 20-含补页的阅读状态 | 阅读／含补页 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入 | 初始控件当前0／历史6；观察2次；状态终验未完成 |
| m08-p21 | 21-回忆册管理与删除确认 | 回忆册管理与删除确认 | 来源返回／直接入口fallback；pressed／focus／disabled／reduced-motion；状态／内容ID／来源失效检查；下一步或恢复出口及不重复写入；动态弹层取消／遮罩／Escape／返回／拖动与焦点恢复 | 初始控件当前0／历史7；观察2次；状态终验未完成 |
