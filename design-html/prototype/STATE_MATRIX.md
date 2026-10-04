# 114 页状态补齐矩阵

下表是实施前的适用状态设计。既有状态稿已计入页面清单；“需要”不代表已经实现或通过测试。

| 页面 | 名称 | 类型 | 需要的状态/交互 | 执行状态 |
| --- | --- | --- | --- | --- |
| m01-p01 | 01-引导页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m01-p02 | 02-登录页 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m01-p03 | 03-创建账号页 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m01-p04 | 04-找回密码账号验证页 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m01-p05 | 05-找回密码设置新密码页 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m01-p06 | 06-登录页-校验失败 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m01-p07 | 07-验证码已发送-等待验证 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m01-p08 | 08-密码重置成功 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m02-p01 | 01-建立情侣关系页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m02-p02 | 02-分享邀请页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m02-p03 | 03-填写邀请码页 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m02-p04 | 04-情侣关系确认页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m02-p05 | 05-情侣绑定成功页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m02-p06 | 06-情侣信息设置页 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m02-p07 | 07-等待TA确认 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m02-p08 | 08-邀请码失效或不可用 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m02-p09 | 09-当前账号已有情侣关系 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m03-p01 | 01-首页与共同记录-无记录状态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m03-p02 | 01-首页与共同记录-正常态 | 一级入口 | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m03-p03 | 02-共同记录搜索页-初始状态 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m03-p04 | 02-共同记录搜索页-结果状态 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m03-p05 | 03-日记编辑页 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m03-p06 | 04-日记列表页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m03-p07 | 05-日记详情页-仅自己可见 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；ID上下文；缺失/权限失效恢复；编辑后重读数据 | 待实施/流程验证 |
| m03-p08 | 05-日记详情页-共同可见 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护；ID上下文；缺失/权限失效恢复；编辑后重读数据 | 待实施/流程验证 |
| m03-p09 | 06-照片相册页-空状态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m03-p10 | 06-照片相册页-网格状态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m03-p11 | 07-照片上传页 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m03-p12 | 08-照片详情页 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护；ID上下文；缺失/权限失效恢复；编辑后重读数据 | 待实施/流程验证 |
| m04-p01 | 01-重要时刻首页-正常态 | 一级入口 | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m04-p02 | 01-重要时刻首页-空状态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m04-p03 | 02-重要时刻详情页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；ID上下文；缺失/权限失效恢复；编辑后重读数据 | 待实施/流程验证 |
| m04-p04 | 03-重要时刻新建编辑页 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m04-p05 | 04-共同提醒页-未读状态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m04-p06 | 04-共同提醒页-空状态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m04-p07 | 05-纪念日管理页-正常态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m04-p08 | 05-纪念日管理页-空状态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m04-p09 | 06-纪念日添加编辑页 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m04-p10 | 07-纪念日倒计时页-正常态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；ID上下文；缺失/权限失效恢复；编辑后重读数据 | 待实施/流程验证 |
| m04-p11 | 07-纪念日倒计时页-纪念日当天 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；ID上下文；缺失/权限失效恢复；编辑后重读数据 | 待实施/流程验证 |
| m04-p12 | 08-时光胶囊列表页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m04-p13 | 09-时光胶囊编辑新建页 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m04-p14 | 10-时光胶囊详情页-已开启 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；ID上下文；缺失/权限失效恢复；编辑后重读数据 | 待实施/流程验证 |
| m04-p15 | 10-时光胶囊详情页-未到期开启 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；ID上下文；缺失/权限失效恢复；编辑后重读数据 | 待实施/流程验证 |
| m04-p16 | 11-悄悄留言列表页-正常态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m04-p17 | 11-悄悄留言列表页-空状态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m05-p01 | 01-童话工坊首页 | 一级入口 | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m05-p02 | 02-创作素材选择页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m05-p03 | 03-回忆转漫画编辑页 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m05-p04 | 04-照片转漫画编辑页 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m05-p05 | 05-回忆影片编辑页 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m05-p06 | 06-魔法生成中页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；生成progress；取消保留参数；成功/失败/超时分支 | 待实施/流程验证 |
| m05-p07 | 07-生成失败页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m05-p08 | 08-作品详情页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；ID上下文；缺失/权限失效恢复；编辑后重读数据 | 待实施/流程验证 |
| m05-p09 | 09-我的创作页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m05-p10 | 10-我们的主角设定页 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m06-p01 | 01-我的与设置首页 | 一级入口 | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m06-p02 | 02-编辑个人资料页 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m06-p03 | 03-我们的小世界页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；危险确认/取消安全；成功反馈及数据更新 | 待实施/流程验证 |
| m06-p04 | 04-草稿箱页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m06-p05 | 05-标签管理页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m06-p06 | 06-童话会员页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m06-p07 | 07-设置首页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；危险确认/取消安全；成功反馈及数据更新 | 待实施/流程验证 |
| m06-p08 | 08-账号与安全页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；危险确认/取消安全；成功反馈及数据更新 | 待实施/流程验证 |
| m06-p09 | 09-隐私与共同可见页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m06-p10 | 10-通知设置页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m06-p11 | 11-数据与存储页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m06-p12 | 12-帮助与关于页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m07-p01 | 60-共同领养页-等待确认 | 一级入口 | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m07-p02 | 60-共同领养页-选择宠物 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m07-p03 | 60-宠物空间首页-正常态 | 一级入口 | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m07-p04 | 60-宠物空间首页-首次领养 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m07-p05 | 61-宠物互动页-互动成功 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m07-p06 | 61-宠物互动页-正常态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m07-p07 | 61-宠物互动页-精力不足 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m07-p08 | 62-喂食页-正常态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m07-p09 | 62-喂食页-资源不足 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m07-p10 | 63-任务页-奖励领取 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m07-p11 | 63-任务页-正常态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m07-p12 | 64-宠物装扮页-正常态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m07-p13 | 64-宠物装扮页-资源不足 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m07-p14 | 65-房间布置页-保存成功 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m07-p15 | 65-房间布置页-正常态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m07-p16 | 65-房间布置页-资源不足 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m07-p17 | 66-成长故事页-回忆权限失效 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m07-p18 | 66-成长故事页-正常态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m07-p19 | 66-成长故事页-章节详情 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；ID上下文；缺失/权限失效恢复；编辑后重读数据 | 待实施/流程验证 |
| m07-p20 | 67-成就页-奖励领取 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m07-p21 | 67-成就页-正常态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m07-p22 | 68-宠物图鉴页-正常态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m07-p23 | 68-宠物图鉴页-详情态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；ID上下文；缺失/权限失效恢复；编辑后重读数据 | 待实施/流程验证 |
| m07-p24 | 69-宠物设置页-导出与删除确认 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；危险确认/取消安全；成功反馈及数据更新 | 待实施/流程验证 |
| m07-p25 | 69-宠物设置页-正常态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；危险确认/取消安全；成功反馈及数据更新 | 待实施/流程验证 |
| m08-p01 | 01-书架 | 一级入口 | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m08-p02 | 02-空书架 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m08-p03 | 03-本月回忆推荐 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m08-p04 | 04-新建回忆册-基础信息 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m08-p05 | 05-主题与封面选择 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m08-p06 | 06-选择共同素材 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m08-p07 | 07-素材预览与确认 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m08-p08 | 08-选择回忆页模板 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m08-p09 | 09-日记摘录页编排 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m08-p10 | 10-照片故事页编排 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m08-p11 | 11-重要时刻页编排 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m08-p12 | 12-作品与宠物成长页编排 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m08-p13 | 13-章节与页序整理 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m08-p14 | 14-建册完成 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m08-p15 | 15-回忆册目录 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；loading skeleton；empty + CTA；load error + retry；条件筛选/状态变化 | 待实施/流程验证 |
| m08-p16 | 16-沉浸翻阅页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；ID上下文；缺失/权限失效恢复；编辑后重读数据 | 待实施/流程验证 |
| m08-p17 | 17-阅读工具菜单 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；ID上下文；缺失/权限失效恢复；编辑后重读数据 | 待实施/流程验证 |
| m08-p18 | 18-添加双人补页 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion | 待实施/流程验证 |
| m08-p19 | 19-双人补页编辑 | 表单/任务 | 返回/fallback；pressed/focus/reduced-motion；focus/typing/filled；blur校验/error/disabled；提交loading/success/failure；dirty返回保护 | 待实施/流程验证 |
| m08-p20 | 20-含补页的阅读状态 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；ID上下文；缺失/权限失效恢复；编辑后重读数据 | 待实施/流程验证 |
| m08-p21 | 21-回忆册管理与删除确认 | 详情/状态/列表（逐页确认） | 返回/fallback；pressed/focus/reduced-motion；危险确认/取消安全；成功反馈及数据更新 | 待实施/流程验证 |
