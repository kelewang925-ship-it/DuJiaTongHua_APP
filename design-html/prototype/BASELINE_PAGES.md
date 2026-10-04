# 交互原型初始扫描：114 页

本文件由 scan_project.py 从改动前的 custom 页面生成。行为分类是静态发现，不代表交互验收通过；JS 事件绑定与运行时数据需逐页复核。

## 页面、入口和出口

| ID | 页面 | 类型 | 入口 | 出口 | 控件数 |
| --- | --- | --- | --- | --- | ---: |
| m01-p01 | 独家童话 | 详情/状态/列表（逐页确认） | m01-p03, m06-p07, m06-p08 | m01-p02, m01-p03 | 2 |
| m01-p02 | 欢迎回来 | 表单/任务 | m01-p01, m01-p03, m01-p04, m01-p06, m01-p08 | 无静态跳转 | 9 |
| m01-p03 | 写下你的名字 | 表单/任务 | m01-p01 | m01-p01, m01-p02 | 12 |
| m01-p04 | 找回你的钥匙 | 表单/任务 | m01-p05, m01-p06 | m01-p02, m01-p05 | 6 |
| m01-p05 | 换一把新钥匙 | 表单/任务 | m01-p04 | m01-p04 | 6 |
| m01-p06 | 独家童话你的故事，独一无二 | 表单/任务 | 目录直达 | m01-p02, m01-p04 | 5 |
| m01-p07 | 信已经送出啦 | 表单/任务 | 目录直达 | 无静态跳转 | 10 |
| m01-p08 | 新钥匙准备好了 | 详情/状态/列表（逐页确认） | 目录直达 | m01-p02 | 1 |
| m02-p01 | 一起写我们的故事 | 详情/状态/列表（逐页确认） | m02-p03, m02-p04, m02-p08 | m02-p02, m02-p03 | 2 |
| m02-p02 | 把这张邀请函交给 TA | 详情/状态/列表（逐页确认） | m02-p01 | 无静态跳转 | 3 |
| m02-p03 | 收到一封特别邀请 | 表单/任务 | m02-p01, m02-p04, m02-p07, m02-p08 | m02-p01, m02-p04 | 7 |
| m02-p04 | 确认和 阿舟 一起写故事吗？ | 详情/状态/列表（逐页确认） | m02-p03 | m02-p01, m02-p03, m02-p05 | 3 |
| m02-p05 | 从今天起，故事有了我们 | 详情/状态/列表（逐页确认） | m02-p04, m02-p06 | m02-p06, m03-p02 | 2 |
| m02-p06 | 我们的小资料 | 表单/任务 | m02-p05, m02-p09 | m02-p05 | 5 |
| m02-p07 | 邀请已经出发 | 详情/状态/列表（逐页确认） | 目录直达 | m02-p03 | 2 |
| m02-p08 | 这张邀请函失效了 | 详情/状态/列表（逐页确认） | 目录直达 | m02-p01, m02-p03 | 2 |
| m02-p09 | 你已经有一起写故事的人啦 | 详情/状态/列表（逐页确认） | 目录直达 | m02-p06, m03-p02 | 2 |
| m03-p01 | 今天也在写童话 | 详情/状态/列表（逐页确认） | m07-p01 | m03-p03, m03-p05, m03-p11, m05-p01 | 4 |
| m03-p02 | 今天也在写童话 | 一级入口 | m02-p05, m02-p09, m03-p03, m03-p05, m03-p06, m03-p09, m03-p10 | m03-p03, m03-p05, m03-p06, m03-p11, m03-p12, m04-p01, m05-p01, m08-p01 | 10 |
| m03-p03 | 搜索共同记录 | 表单/任务 | m03-p01, m03-p02, m03-p04 | m03-p02, m03-p04 | 10 |
| m03-p04 | 搜索共同记录 | 表单/任务 | m03-p03, m03-p04 | m03-p03, m03-p04, m03-p06, m03-p12, m04-p01 | 7 |
| m03-p05 | 写日记 | 表单/任务 | m03-p01, m03-p02, m03-p06, m03-p07, m03-p08, m04-p10, m04-p11 | m03-p02 | 11 |
| m03-p06 | 日记 | 详情/状态/列表（逐页确认） | m03-p02, m03-p04, m03-p07, m03-p08, m04-p17 | m03-p02, m03-p05 | 8 |
| m03-p07 | 雨后的那封信 | 详情/状态/列表（逐页确认） | 目录直达 | m03-p05, m03-p06 | 3 |
| m03-p08 | 今天因为一件小事笑了好久 | 表单/任务 | m04-p03, m04-p10, m04-p16 | m03-p05, m03-p06 | 5 |
| m03-p09 | 照片相册 | 详情/状态/列表（逐页确认） | 目录直达 | m03-p02, m03-p11 | 3 |
| m03-p10 | 照片相册 | 详情/状态/列表（逐页确认） | m03-p11, m03-p12, m04-p03 | m03-p02, m03-p11, m03-p12 | 12 |
| m03-p11 | 添加照片 | 表单/任务 | m03-p01, m03-p02, m03-p09, m03-p10, m03-p12 | m03-p10 | 11 |
| m03-p12 | 晚霞散步 | 表单/任务 | m03-p02, m03-p04, m03-p10 | m03-p10, m03-p11 | 5 |
| m04-p01 | 重要时刻 | 一级入口 | m03-p02, m03-p04, m04-p03, m04-p04, m04-p05, m04-p06, m04-p07, m04-p08, m04-p12, m04-p16, m04-p17 | m04-p03, m04-p07, m04-p10, m04-p12, m04-p16 | 8 |
| m04-p02 | 重要时刻 | 详情/状态/列表（逐页确认） | 目录直达 | m04-p04 | 2 |
| m04-p03 | 重要时刻 | 详情/状态/列表（逐页确认） | m04-p01, m04-p05, m04-p10, m04-p11, m04-p16 | m03-p08, m03-p10, m04-p01, m04-p16 | 4 |
| m04-p04 | 新建重要时刻 | 表单/任务 | m04-p02 | m04-p01 | 12 |
| m04-p05 | 共同提醒 | 详情/状态/列表（逐页确认） | 目录直达 | m04-p01, m04-p03, m04-p10, m04-p15 | 5 |
| m04-p06 | 共同提醒 | 详情/状态/列表（逐页确认） | 目录直达 | m04-p01 | 2 |
| m04-p07 | 纪念日 | 详情/状态/列表（逐页确认） | m04-p01, m04-p09, m04-p10 | m04-p01, m04-p09, m04-p10 | 8 |
| m04-p08 | 纪念日 | 详情/状态/列表（逐页确认） | 目录直达 | m04-p01, m04-p09 | 2 |
| m04-p09 | 添加纪念日 | 表单/任务 | m04-p07, m04-p08 | m04-p07 | 7 |
| m04-p10 | 相识纪念日 | 详情/状态/列表（逐页确认） | m04-p01, m04-p05, m04-p07 | m03-p05, m03-p08, m04-p03, m04-p07 | 4 |
| m04-p11 | 相识纪念日 | 详情/状态/列表（逐页确认） | 目录直达 | m03-p05, m04-p03 | 2 |
| m04-p12 | 时光胶囊 | 详情/状态/列表（逐页确认） | m04-p01, m04-p13, m04-p14, m04-p15 | m04-p01, m04-p13, m04-p14, m04-p15 | 8 |
| m04-p13 | 新建时光胶囊 | 表单/任务 | m04-p12 | m04-p12 | 9 |
| m04-p14 | 时光胶囊 | 详情/状态/列表（逐页确认） | m04-p12 | m04-p12 | 2 |
| m04-p15 | 时光胶囊 | 表单/任务 | m04-p05, m04-p12 | m04-p12 | 2 |
| m04-p16 | 悄悄留言 | 详情/状态/列表（逐页确认） | m04-p01, m04-p03 | m03-p08, m04-p01, m04-p03 | 4 |
| m04-p17 | 悄悄留言 | 详情/状态/列表（逐页确认） | 目录直达 | m03-p06, m04-p01 | 2 |
| m05-p01 | 童话工坊 | 一级入口 | m03-p01, m03-p02, m05-p02, m05-p05, m05-p06, m05-p07, m05-p09, m05-p10 | m05-p02, m05-p05, m05-p08, m05-p09 | 6 |
| m05-p02 | 挑一段我们的回忆 | 详情/状态/列表（逐页确认） | m05-p01, m05-p03, m05-p04 | m05-p01, m05-p03, m05-p04 | 6 |
| m05-p03 | 回忆转漫画 | 表单/任务 | m05-p02, m05-p07, m05-p08, m05-p09, m06-p04 | m05-p02, m05-p06, m05-p10 | 10 |
| m05-p04 | 照片转漫画 | 表单/任务 | m05-p02 | m05-p02, m05-p06, m05-p10 | 12 |
| m05-p05 | 回忆影片 | 表单/任务 | m05-p01, m05-p09, m06-p04 | m05-p01, m05-p06 | 10 |
| m05-p06 | 回忆正在变成童话 | 详情/状态/列表（逐页确认） | m05-p03, m05-p04, m05-p05, m05-p07, m05-p09 | m05-p01 | 1 |
| m05-p07 | 这次魔法没有成功 | 详情/状态/列表（逐页确认） | 目录直达 | m05-p01, m05-p03, m05-p06 | 3 |
| m05-p08 | 海边的那天 | 详情/状态/列表（逐页确认） | m05-p01, m05-p09 | m05-p03, m05-p09 | 12 |
| m05-p09 | 我的创作 | 详情/状态/列表（逐页确认） | m05-p01, m05-p08 | m05-p01, m05-p03, m05-p05, m05-p06, m05-p08 | 10 |
| m05-p10 | 我们的主角设定 | 表单/任务 | m05-p03, m05-p04 | m05-p01 | 6 |
| m06-p01 | 我的与设置 | 一级入口 | m06-p02, m06-p03, m06-p04, m06-p05, m06-p06, m06-p07, m06-p12 | m06-p02, m06-p03, m06-p04, m06-p05, m06-p06, m06-p07, m06-p12 | 7 |
| m06-p02 | 编辑个人资料 | 表单/任务 | m06-p01, m06-p03 | m06-p01 | 8 |
| m06-p03 | 我们的小世界 | 详情/状态/列表（逐页确认） | m06-p01 | m06-p01, m06-p02, m06-p09 | 6 |
| m06-p04 | 草稿箱 | 详情/状态/列表（逐页确认） | m06-p01 | m05-p03, m05-p05, m06-p01 | 4 |
| m06-p05 | 标签管理 | 详情/状态/列表（逐页确认） | m06-p01 | m06-p01 | 10 |
| m06-p06 | 童话会员 | 详情/状态/列表（逐页确认） | m06-p01 | m06-p01 | 3 |
| m06-p07 | 设置 | 详情/状态/列表（逐页确认） | m06-p01, m06-p08, m06-p09, m06-p10, m06-p11 | m01-p01, m06-p01, m06-p08, m06-p09, m06-p10, m06-p11 | 8 |
| m06-p08 | 账号与安全 | 详情/状态/列表（逐页确认） | m06-p07 | m01-p01, m06-p07 | 7 |
| m06-p09 | 隐私与共同可见 | 详情/状态/列表（逐页确认） | m06-p03, m06-p07 | m06-p07 | 6 |
| m06-p10 | 通知设置 | 详情/状态/列表（逐页确认） | m06-p07 | m06-p07 | 6 |
| m06-p11 | 数据与存储 | 详情/状态/列表（逐页确认） | m06-p07 | m06-p07 | 6 |
| m06-p12 | 帮助与关于 | 详情/状态/列表（逐页确认） | m06-p01 | m06-p01 | 7 |
| m07-p01 | 等待 TA 的确认 | 一级入口 | m07-p02 | m03-p01 | 2 |
| m07-p02 | 一起领养小伙伴 | 表单/任务 | m07-p04 | m07-p01 | 6 |
| m07-p03 | 糯米的小屋 | 一级入口 | m07-p05, m07-p07, m07-p09, m07-p12, m07-p13, m07-p14, m07-p16, m07-p17, m07-p20, m07-p25 | m07-p06, m07-p08, m07-p10, m07-p12, m07-p15, m07-p18, m07-p21 | 8 |
| m07-p04 | 我们的宠物 | 详情/状态/列表（逐页确认） | 目录直达 | m07-p02 | 4 |
| m07-p05 | 糯米玩得好开心！ | 详情/状态/列表（逐页确认） | m07-p06 | m07-p03, m07-p06 | 2 |
| m07-p06 | 和糯米玩一会儿 | 详情/状态/列表（逐页确认） | m07-p03, m07-p05, m07-p11 | m07-p05, m07-p07 | 5 |
| m07-p07 | 和糯米互动 | 详情/状态/列表（逐页确认） | m07-p06 | m07-p03, m07-p08, m07-p18 | 3 |
| m07-p08 | 给糯米喂点好吃的 | 详情/状态/列表（逐页确认） | m07-p03, m07-p07 | m07-p09, m07-p10 | 5 |
| m07-p09 | 给糯米喂食 | 详情/状态/列表（逐页确认） | m07-p08 | m07-p03, m07-p10 | 2 |
| m07-p10 | 一起完成啦！ | 详情/状态/列表（逐页确认） | m07-p03, m07-p08, m07-p09 | m07-p12 | 1 |
| m07-p11 | 一起照顾糯米 | 详情/状态/列表（逐页确认） | m07-p13, m07-p16, m07-p21 | m07-p06, m07-p15 | 5 |
| m07-p12 | 给糯米换新装 | 详情/状态/列表（逐页确认） | m07-p03, m07-p10, m07-p23 | m07-p03 | 9 |
| m07-p13 | 给糯米换装 | 详情/状态/列表（逐页确认） | 目录直达 | m07-p03, m07-p11 | 2 |
| m07-p14 | 小屋布置完成 | 详情/状态/列表（逐页确认） | m07-p15 | m07-p03, m07-p15 | 2 |
| m07-p15 | 一起布置糯米的小屋 | 详情/状态/列表（逐页确认） | m07-p03, m07-p11, m07-p14, m07-p22 | m07-p14 | 9 |
| m07-p16 | 布置糯米的小屋 | 详情/状态/列表（逐页确认） | 目录直达 | m07-p03, m07-p11 | 2 |
| m07-p17 | 糯米的成长故事 | 详情/状态/列表（逐页确认） | 目录直达 | m07-p03 | 2 |
| m07-p18 | 糯米的成长故事 | 详情/状态/列表（逐页确认） | m07-p03, m07-p07 | m07-p19 | 1 |
| m07-p19 | 第 27 天 · 今天也被好好照顾 | 详情/状态/列表（逐页确认） | m07-p18 | m07-p20 | 1 |
| m07-p20 | 我们的宠物成就 | 详情/状态/列表（逐页确认） | m07-p19 | m07-p03 | 2 |
| m07-p21 | 我们和糯米的成就 | 详情/状态/列表（逐页确认） | m07-p03, m07-p22 | m07-p11 | 7 |
| m07-p22 | 糯米的收藏图鉴 | 详情/状态/列表（逐页确认） | m07-p23 | m07-p15, m07-p21 | 9 |
| m07-p23 | 小花围巾 | 详情/状态/列表（逐页确认） | 目录直达 | m07-p12, m07-p22 | 3 |
| m07-p24 | 在告别前，再确认一次 | 详情/状态/列表（逐页确认） | m07-p25 | m07-p25 | 3 |
| m07-p25 | 糯米的小屋设置 | 详情/状态/列表（逐页确认） | m07-p24 | m07-p03, m07-p24 | 10 |
| m08-p01 | 共同回忆册 | 一级入口 | m03-p02, m08-p02, m08-p03, m08-p04, m08-p15 | m08-p03, m08-p04 | 5 |
| m08-p02 | 共同回忆册 | 详情/状态/列表（逐页确认） | m08-p21 | m08-p01, m08-p03 | 2 |
| m08-p03 | 本月回忆推荐 | 详情/状态/列表（逐页确认） | m08-p01, m08-p02 | m08-p01, m08-p04, m08-p05 | 3 |
| m08-p04 | 新建回忆册 | 表单/任务 | m08-p01, m08-p03, m08-p05 | m08-p01, m08-p05 | 7 |
| m08-p05 | 为这本书挑一件外衣 | 详情/状态/列表（逐页确认） | m08-p03, m08-p04, m08-p06 | m08-p04, m08-p06 | 6 |
| m08-p06 | 选择共同素材 | 详情/状态/列表（逐页确认） | m08-p05, m08-p07, m08-p09, m08-p11 | m08-p05, m08-p07 | 13 |
| m08-p07 | 素材预览 | 详情/状态/列表（逐页确认） | m08-p06, m08-p08 | m08-p06, m08-p08 | 3 |
| m08-p08 | 为回忆选一页版式 | 详情/状态/列表（逐页确认） | m08-p07, m08-p09, m08-p10, m08-p11, m08-p12 | m08-p07, m08-p09 | 8 |
| m08-p09 | 编排日记摘录页 | 表单/任务 | m08-p08, m08-p13 | m08-p06, m08-p08, m08-p10 | 9 |
| m08-p10 | 编排照片故事页 | 表单/任务 | m08-p09 | m08-p08, m08-p13 | 13 |
| m08-p11 | 编排重要时刻页 | 表单/任务 | 目录直达 | m08-p06, m08-p08, m08-p13 | 7 |
| m08-p12 | 作品与宠物成长 | 表单/任务 | 目录直达 | m08-p08, m08-p13 | 8 |
| m08-p13 | 整理章节与页序 | 详情/状态/列表（逐页确认） | m08-p10, m08-p11, m08-p12, m08-p14, m08-p17, m08-p21 | m08-p09, m08-p14 | 9 |
| m08-p14 | 这本回忆书完成啦 | 详情/状态/列表（逐页确认） | m08-p13 | m08-p13, m08-p15 | 2 |
| m08-p15 | 我们的夏天 | 详情/状态/列表（逐页确认） | m08-p14, m08-p16, m08-p17, m08-p18, m08-p20 | m08-p01, m08-p16 | 14 |
| m08-p16 | 独家童话 | 详情/状态/列表（逐页确认） | m08-p15, m08-p17, m08-p18 | m08-p15, m08-p17, m08-p18 | 4 |
| m08-p17 | 阅读工具 | 详情/状态/列表（逐页确认） | m08-p16, m08-p20, m08-p21 | m08-p13, m08-p15, m08-p16, m08-p18, m08-p19, m08-p21 | 6 |
| m08-p18 | 为这一页加一张补页 | 详情/状态/列表（逐页确认） | m08-p16, m08-p17, m08-p19 | m08-p15, m08-p16, m08-p19 | 6 |
| m08-p19 | 写一张补页 | 表单/任务 | m08-p17, m08-p18 | m08-p18, m08-p20 | 8 |
| m08-p20 | 独家童话 | 详情/状态/列表（逐页确认） | m08-p19 | m08-p15, m08-p17 | 3 |
| m08-p21 | 管理这本回忆册 | 详情/状态/列表（逐页确认） | m08-p17 | m08-p02, m08-p13, m08-p17 | 7 |

## 每页控件及已有状态

### m01-p01 · 独家童话

原稿：01-引导页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.primary | 登录并开始 | explicit-inline | location.href='m01-p02.html' |
| 2 | button.ui-hit-text | 创建账号 | explicit-inline | location.href='m01-p03.html' |

已有弹层/状态：未发现具名状态节点

### m01-p02 · 欢迎回来

原稿：02-登录页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回 | explicit-inline | history.back() |
| 2 | input | 手机号 | native-input | 原生输入/选择 |
| 3 | #password | password | native-input | 原生输入/选择 |
| 4 | #eye | 显示密码 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button.forgot | 忘记密码？ | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button.submit | 登录并回到故事里 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | button.ui-hit-text | 创建账号 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 8 | a.ui-hit-text | 《用户协议》 | explicit-inline | # |
| 9 | a.ui-hit-text | 《隐私政策》 | explicit-inline | # |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m01-p03 · 写下你的名字

原稿：03-创建账号页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回欢迎页 | explicit-inline | location.href='m01-p01.html' |
| 2 | input | 昵称 | native-input | 原生输入/选择 |
| 3 | input | 手机号 | native-input | 原生输入/选择 |
| 4 | input | 验证码 | native-input | 原生输入/选择 |
| 5 | #send-code | 获取验证码 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | #password | 登录密码 | native-input | 原生输入/选择 |
| 7 | #eye | 显示密码 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 8 | input | (图标/无名称) | native-input | 原生输入/选择 |
| 9 | a.ui-hit-text | 《用户协议》 | explicit-inline | # |
| 10 | a.ui-hit-text | 《隐私政策》 | explicit-inline | # |
| 11 | button.submit | 创建账号 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 12 | a.ui-hit-text | 去登录 | explicit-inline | m01-p02.html |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m01-p04 · 找回你的钥匙

原稿：04-找回密码账号验证页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回 | explicit-inline | location.href='m01-p02.html' |
| 2 | input | 手机号 | native-input | 原生输入/选择 |
| 3 | input | 验证码 | native-input | 原生输入/选择 |
| 4 | #send | 获取验证码 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button.next | 下一步 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | a.ui-hit-text | 返回登录 | explicit-inline | m01-p02.html |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m01-p05 · 换一把新钥匙

原稿：05-找回密码设置新密码页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回找回密码 | explicit-inline | location.href='m01-p04.html' |
| 2 | #password | 输入新密码 | native-input | 原生输入/选择 |
| 3 | button.eye | 显示新密码 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | #confirm | 再次输入新密码 | native-input | 原生输入/选择 |
| 5 | button.eye | 显示确认密码 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button.submit | 确认并重置 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m01-p06 · 独家童话你的故事，独一无二

原稿：06-登录页-校验失败；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回 | explicit-inline | location.href='m01-p02.html' |
| 2 | #password | 密码 | native-input | 原生输入/选择 |
| 3 | button.eye | 显示密码 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button.retry | 再试一次 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | a.ui-hit-text | 找回密码 | explicit-inline | m01-p04.html |

已有弹层/状态：{'tag': 'p', 'id': 'error', 'class': 'error', 'role': None, 'text': '密码错误，还可以尝试 4 次'}

### m01-p07 · 信已经送出啦

原稿：07-验证码已发送-等待验证；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回 | explicit-inline | history.back() |
| 2 | input | 第 1 位验证码 | native-input | 原生输入/选择 |
| 3 | input | 第 2 位验证码 | native-input | 原生输入/选择 |
| 4 | input | 第 3 位验证码 | native-input | 原生输入/选择 |
| 5 | input | 第 4 位验证码 | native-input | 原生输入/选择 |
| 6 | input | 第 5 位验证码 | native-input | 原生输入/选择 |
| 7 | input | 第 6 位验证码 | native-input | 原生输入/选择 |
| 8 | button.verify | 验证并继续 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 9 | #resend | 48 秒后可重新获取 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 10 | #switch | 没收到验证码？换个方式 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m01-p08 · 新钥匙准备好了

原稿：08-密码重置成功；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.login | 返回登录 | explicit-inline | location.href='m01-p02.html' |

已有弹层/状态：未发现具名状态节点

### m02-p01 · 一起写我们的故事

原稿：01-建立情侣关系页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.choice.invite | 邀请 TA 加入生成专属邀请码 | explicit-inline | location.href='m02-p02.html' |
| 2 | button.choice.accept | 输入 TA 的邀请码接受一份特别邀请 | explicit-inline | location.href='m02-p03.html' |

已有弹层/状态：未发现具名状态节点

### m02-p02 · 把这张邀请函交给 TA

原稿：02-分享邀请页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | #copy | ✦ 复制邀请码 ✦ | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 2 | #share | 发送给微信好友 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | #save | 保存邀请卡 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m02-p03 · 收到一封特别邀请

原稿：03-填写邀请码页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回 | explicit-inline | location.href='m02-p01.html' |
| 2 | input | 第 1 位邀请码 | native-input | 原生输入/选择 |
| 3 | input | 第 2 位邀请码 | native-input | 原生输入/选择 |
| 4 | input | 第 3 位邀请码 | native-input | 原生输入/选择 |
| 5 | input | 第 4 位邀请码 | native-input | 原生输入/选择 |
| 6 | button.preview | 查看邀请内容 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | a.ui-hit-text | 请让 TA 分享给你 | explicit-inline | m02-p01.html |

已有弹层/状态：{'tag': 'p', 'id': 'error', 'class': 'error', 'role': None, 'text': '请填写完整的邀请码'}

### m02-p04 · 确认和 阿舟 一起写故事吗？

原稿：04-情侣关系确认页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回 | explicit-inline | location.href='m02-p03.html' |
| 2 | button.confirm | 确认建立关系 | explicit-inline | location.href='m02-p05.html' |
| 3 | button.ui-hit-text | 暂不接受 | explicit-inline | location.href='m02-p01.html' |

已有弹层/状态：未发现具名状态节点

### m02-p05 · 从今天起，故事有了我们

原稿：05-情侣绑定成功页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.primary | 去写第一篇共同日记 ♡ | explicit-inline | location.href='m03-p02.html' |
| 2 | button.secondary | 完善情侣资料 | explicit-inline | location.href='m02-p06.html' |

已有弹层/状态：未发现具名状态节点

### m02-p06 · 我们的小资料

原稿：06-情侣信息设置页；现有本地数据键：dujia-profile-。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回 | explicit-inline | location.href='m02-p05.html' |
| 2 | #nickname | 情侣昵称 | native-input | 原生输入/选择 |
| 3 | #met | 相遇日期 | native-input | 原生输入/选择 |
| 4 | #anniversary | 共同纪念日 | native-input | 原生输入/选择 |
| 5 | button.save | 保存小资料 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m02-p07 · 邀请已经出发

原稿：07-等待TA确认；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | #remind | 提醒 TA 看看 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 2 | #copy | 复制邀请链接 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m02-p08 · 这张邀请函失效了

原稿：08-邀请码失效或不可用；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.again | 请 TA 重新邀请 | explicit-inline | location.href='m02-p01.html' |
| 2 | button.reenter | 重新输入邀请码 | explicit-inline | location.href='m02-p03.html' |

已有弹层/状态：未发现具名状态节点

### m02-p09 · 你已经有一起写故事的人啦

原稿：09-当前账号已有情侣关系；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.primary | 回到我们的首页 | explicit-inline | location.href='m03-p02.html' |
| 2 | a.ui-hit-text | 查看关系设置 | explicit-inline | m02-p06.html |

已有弹层/状态：未发现具名状态节点

### m03-p01 · 今天也在写童话

原稿：01-首页与共同记录-无记录状态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.search | 搜索共同记录 | explicit-inline | location.href='m03-p03.html' |
| 2 | button.choice.diary | 写日记 | explicit-inline | location.href='m03-p05.html' |
| 3 | button.choice.photo | 添加照片 | explicit-inline | location.href='m03-p11.html' |
| 4 | a.ui-hit-text | 去童话工坊，把回忆变成故事 › | explicit-inline | m05-p01.html |

已有弹层/状态：未发现具名状态节点

### m03-p02 · 今天也在写童话

原稿：01-首页与共同记录-正常态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.search | 搜索共同记录 | explicit-inline | location.href='m03-p03.html' |
| 2 | button.action.diary | 写日记记录心情 | explicit-inline | location.href='m03-p05.html' |
| 3 | button.action.photo | 添加照片珍藏瞬间 | explicit-inline | location.href='m03-p11.html' |
| 4 | a.ui-hit-text | 去童话工坊，把回忆变成故事 › | explicit-inline | m05-p01.html |
| 5 | a | 查看全部 › | explicit-inline | m03-p06.html |
| 6 | button.item.photo-record | 晚霞散步今天 20:12 | explicit-inline | location.href='m03-p12.html' |
| 7 | button.item.diary-record | 今天因为一件小事笑了好久小满记录 | explicit-inline | location.href='m03-p06.html' |
| 8 | button.item.reply-record | 阿舟回应了你的日记 ♡刚刚 | explicit-inline | location.href='m03-p06.html' |
| 9 | button.reading | 继续翻阅我们的故事3D 日记本 · 上次读到第 18 页继续阅读 › | explicit-inline | location.href='m08-p01.html' |
| 10 | button.moment | 下一件重要时刻我们的恋爱纪念日 · 18 天后查看重要时刻 › | explicit-inline | location.href='m04-p01.html' |

已有弹层/状态：未发现具名状态节点

### m03-p03 · 搜索共同记录

原稿：02-共同记录搜索页-初始状态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回首页 | explicit-inline | location.href='m03-p02.html' |
| 2 | #query | 搜索关键词 | native-input | 原生输入/选择 |
| 3 | #clear | 清除搜索 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button.ui-hit-text | 晚霞 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button.ui-hit-text | 火锅 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button.ui-hit-text | 旅行 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | button | 日记 › | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 8 | button | 照片 › | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 9 | button | 旅行 › | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 10 | button | 纪念日 › | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m03-p04 · 搜索共同记录

原稿：02-共同记录搜索页-结果状态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回搜索 | explicit-inline | location.href='m03-p03.html' |
| 2 | #query | 搜索关键词 | native-input | 原生输入/选择 |
| 3 | button | 清除 | explicit-inline | location.href='m03-p03.html' |
| 4 | button.diary-result | 今天的晚霞像橘子汽水小满 · 9 月 1 日 · 共同可见 | explicit-inline | location.href='m03-p06.html' |
| 5 | button | 查看海边晚霞照片 | explicit-inline | location.href='m03-p12.html' |
| 6 | button | 查看栏杆边的晚霞照片 | explicit-inline | location.href='m03-p12.html' |
| 7 | button.moment-result | 第一次一起看晚霞 › | explicit-inline | location.href='m04-p01.html' |

已有弹层/状态：未发现具名状态节点

### m03-p05 · 写日记

原稿：03-日记编辑页；现有本地数据键：dujia-diary-draft。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回首页 | explicit-inline | location.href='m03-p02.html' |
| 2 | #top-save | 保存 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | input.title | 日记标题 | native-input | 原生输入/选择 |
| 4 | select.mood | 今天的心情 | native-input | 原生输入/选择 |
| 5 | textarea.body-text | 日记正文 | native-input | 原生输入/选择 |
| 6 | #remove | 移除照片 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | #add-photo | 添加照片 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 8 | #file | (图标/无名称) | native-input | 原生输入/选择 |
| 9 | input | visibility | native-input | 原生输入/选择 |
| 10 | input | visibility | native-input | 原生输入/选择 |
| 11 | button.submit | 保存日记 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m03-p06 · 日记

原稿：04-日记列表页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回首页 | explicit-inline | location.href='m03-p02.html' |
| 2 | #filter | 筛选日记 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button.active | 全部 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button | 草稿 2 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button.card.one | 今天因为一件小事笑了好久开心小满 · 共同可见阿舟回应了 | explicit-inline | location.href='m03-p05.html' |
| 6 | button.card.two | 雨天的火锅阿舟 · 共同可见 | explicit-inline | location.href='m03-p05.html' |
| 7 | button.card.three | 仅自己可见 | explicit-inline | location.href='m03-p05.html' |
| 8 | button.write | 写日记 | explicit-inline | location.href='m03-p05.html' |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m03-p07 · 雨后的那封信

原稿：05-日记详情页-仅自己可见；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回日记列表 | explicit-inline | location.href='m03-p06.html' |
| 2 | button.edit | 编辑日记 | explicit-inline | location.href='m03-p05.html' |
| 3 | #more | 更多操作 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m03-p08 · 今天因为一件小事笑了好久

原稿：05-日记详情页-共同可见；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回日记列表 | explicit-inline | location.href='m03-p06.html' |
| 2 | button.edit | 编辑日记 | explicit-inline | location.href='m03-p05.html' |
| 3 | #reply | 给 TA 留一句话 | native-input | 原生输入/选择 |
| 4 | #emoji | 添加表情 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button | 发送留言 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m03-p09 · 照片相册

原稿：06-照片相册页-空状态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回首页 | explicit-inline | location.href='m03-p02.html' |
| 2 | button.primary | 添加第一张照片 | explicit-inline | location.href='m03-p11.html' |
| 3 | button.ui-hit-text | 从系统相册选择 | explicit-inline | location.href='m03-p11.html' |

已有弹层/状态：未发现具名状态节点

### m03-p10 · 照片相册

原稿：06-照片相册页-网格状态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回首页 | explicit-inline | location.href='m03-p02.html' |
| 2 | #filter | 筛选照片 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button.active | 全部 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button | 共同可见 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button | 旅行 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button | 晚霞散步 | explicit-inline | location.href='m03-p12.html' |
| 7 | button | 火锅 | explicit-inline | location.href='m03-p12.html' |
| 8 | button | 玫瑰花 | explicit-inline | location.href='m03-p12.html' |
| 9 | button | 雨天窗户 | explicit-inline | location.href='m03-p12.html' |
| 10 | button | 情侣合照 | explicit-inline | location.href='m03-p12.html' |
| 11 | button | 宠物爪子 | explicit-inline | location.href='m03-p12.html' |
| 12 | button.add | ＋ 添加照片 | explicit-inline | location.href='m03-p11.html' |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m03-p11 · 添加照片

原稿：07-照片上传页；现有本地数据键：dujia-photo-draft。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回相册 | explicit-inline | location.href='m03-p10.html' |
| 2 | #done | 完成 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | #photo-hit | 更换照片 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | #file | (图标/无名称) | native-input | 原生输入/选择 |
| 5 | textarea.caption | 照片心情 | native-input | 原生输入/选择 |
| 6 | input | 照片日期 | native-input | 原生输入/选择 |
| 7 | input | 照片标签 | native-input | 原生输入/选择 |
| 8 | #add-tag | 添加标签 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 9 | input | visibility | native-input | 原生输入/选择 |
| 10 | input | visibility | native-input | 原生输入/选择 |
| 11 | button.submit | 保存照片 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m03-p12 · 晚霞散步

原稿：08-照片详情页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回照片相册 | explicit-inline | location.href='m03-p10.html' |
| 2 | button.edit | 编辑照片 | explicit-inline | location.href='m03-p11.html' |
| 3 | #reply | 给 TA 留一句话 | native-input | 原生输入/选择 |
| 4 | #emoji | 添加表情 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button | 发送留言 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m04-p01 · 重要时刻

原稿：01-重要时刻首页-正常态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.calendar | 查看纪念日 | explicit-inline | location.href='m04-p07.html' |
| 2 | button.next | 第一次旅行 | explicit-inline | location.href='m04-p10.html' |
| 3 | #see-all | 查看全部 › | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button | 春日野餐 2024.04.13 | explicit-inline | location.href='m04-p03.html' |
| 5 | button | 第一次一起做饭 2024.05.20 | explicit-inline | location.href='m04-p03.html' |
| 6 | button | 纪念日 | explicit-inline | location.href='m04-p07.html' |
| 7 | button | 时光胶囊 | explicit-inline | location.href='m04-p12.html' |
| 8 | button | 悄悄留言 | explicit-inline | location.href='m04-p16.html' |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m04-p02 · 重要时刻

原稿：01-重要时刻首页-空状态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | #from-records | 从共同记录中收录 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 2 | button | 新建重要时刻 | explicit-inline | location.href='m04-p04.html' |

已有弹层/状态：{'tag': 'p', 'id': None, 'class': 'empty', 'role': None, 'text': '还没有重要时刻'}；{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m04-p03 · 重要时刻

原稿：02-重要时刻详情页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回重要时刻 | explicit-inline | location.href='m04-p01.html' |
| 2 | button | 野餐日记前往共同记录查看 | explicit-inline | location.href='m03-p08.html' |
| 3 | button | 12 张照片前往共同记录查看 | explicit-inline | location.href='m03-p10.html' |
| 4 | button.message | 悄悄留言 3 条 | explicit-inline | location.href='m04-p16.html' |

已有弹层/状态：未发现具名状态节点

### m04-p04 · 新建重要时刻

原稿：03-重要时刻新建编辑页；现有本地数据键：dujia-moment-draft。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回重要时刻 | explicit-inline | location.href='m04-p01.html' |
| 2 | #cover-button | 添加封面 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | #cover-file | (图标/无名称) | native-input | 原生输入/选择 |
| 4 | input | name | native-input | 原生输入/选择 |
| 5 | input | 发生日期 | native-input | 原生输入/选择 |
| 6 | input | type | native-input | 原生输入/选择 |
| 7 | input | type | native-input | 原生输入/选择 |
| 8 | input | type | native-input | 原生输入/选择 |
| 9 | input | type | native-input | 原生输入/选择 |
| 10 | textarea | 记录这个时刻背后的故事… | native-input | 原生输入/选择 |
| 11 | #related | 从共同记录中选择 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 12 | button.submit | 保存到时刻册 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m04-p05 · 共同提醒

原稿：04-共同提醒页-未读状态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回重要时刻 | explicit-inline | location.href='m04-p01.html' |
| 2 | button.item | 我们的纪念日还有 3 天一起为 9 月 12 日留一段记录吧 | explicit-inline | location.href='m04-p10.html' |
| 3 | button.item | 时光胶囊明天开启写给未来的信，明天见 | explicit-inline | location.href='m04-p15.html' |
| 4 | button.item | 春日野餐 · 重要时刻提醒这一页已经收藏 1 年 | explicit-inline | location.href='m04-p03.html' |
| 5 | #read-item | 每月记录提醒本月的我们，值得一段记录 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m04-p06 · 共同提醒

原稿：04-共同提醒页-空状态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回重要时刻 | explicit-inline | location.href='m04-p01.html' |
| 2 | button.go | 去看看重要时刻 | explicit-inline | location.href='m04-p01.html' |

已有弹层/状态：{'tag': 'p', 'id': None, 'class': 'empty', 'role': None, 'text': '暂时没有新提醒'}

### m04-p07 · 纪念日

原稿：05-纪念日管理页-正常态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回重要时刻 | explicit-inline | location.href='m04-p01.html' |
| 2 | button.plus | 添加纪念日 | explicit-inline | location.href='m04-p09.html' |
| 3 | button.date-pill | 9 月 12 日 | explicit-inline | location.href='m04-p10.html' |
| 4 | button.text | 相识纪念日每年 9 月 12 日 | explicit-inline | location.href='m04-p10.html' |
| 5 | button.switch | 相识纪念日提醒 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button.text | 第一次旅行每年 6 月 18 日 | explicit-inline | location.href='m04-p10.html' |
| 7 | button.switch | 第一次旅行提醒 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 8 | button.add | 添加纪念日 | explicit-inline | location.href='m04-p09.html' |

已有弹层/状态：未发现具名状态节点

### m04-p08 · 纪念日

原稿：05-纪念日管理页-空状态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回重要时刻 | explicit-inline | location.href='m04-p01.html' |
| 2 | button.add | 添加第一个纪念日 | explicit-inline | location.href='m04-p09.html' |

已有弹层/状态：{'tag': 'p', 'id': None, 'class': 'empty', 'role': None, 'text': '还没有纪念日'}

### m04-p09 · 添加纪念日

原稿：06-纪念日添加编辑页；现有本地数据键：dujia-anniversary-draft。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回纪念日列表 | explicit-inline | location.href='m04-p07.html' |
| 2 | input | name | native-input | 原生输入/选择 |
| 3 | input | 纪念日日期 | native-input | 原生输入/选择 |
| 4 | select | 提前 3 天提前 1 天当天不提醒 | native-input | 原生输入/选择 |
| 5 | input | 每年重复 | native-input | 原生输入/选择 |
| 6 | select | 可选 · 关联一段章节春日野餐第一次旅行 | native-input | 原生输入/选择 |
| 7 | button.submit | 保存纪念日 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m04-p10 · 相识纪念日

原稿：07-纪念日倒计时页-正常态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回纪念日 | explicit-inline | location.href='m04-p07.html' |
| 2 | button | 春日野餐 | explicit-inline | location.href='m04-p03.html' |
| 3 | button | 那年九月的日记 | explicit-inline | location.href='m03-p08.html' |
| 4 | button.new-record | 写下新的共同记录 | explicit-inline | location.href='m03-p05.html' |

已有弹层/状态：未发现具名状态节点

### m04-p11 · 相识纪念日

原稿：07-纪念日倒计时页-纪念日当天；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button | 一起留下今天的记录 | explicit-inline | location.href='m03-p05.html' |
| 2 | button | 查看这个时刻 | explicit-inline | location.href='m04-p03.html' |

已有弹层/状态：未发现具名状态节点

### m04-p12 · 时光胶囊

原稿：08-时光胶囊列表页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回重要时刻 | explicit-inline | location.href='m04-p01.html' |
| 2 | button.plus | 新建时光胶囊 | explicit-inline | location.href='m04-p13.html' |
| 3 | button.active | 等待开启 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button | 已经开启 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button.card | 写给一周年的我们2026.09.12 开启还有 10 天 | explicit-inline | location.href='m04-p15.html' |
| 6 | button.card | 下一个春天再见2026.09.12 开启还有 10 天 | explicit-inline | location.href='m04-p15.html' |
| 7 | button.card.third | 去年写给今天的信已开启 | explicit-inline | location.href='m04-p14.html' |
| 8 | button.new | ＋ 新建时光胶囊 | explicit-inline | location.href='m04-p13.html' |

已有弹层/状态：未发现具名状态节点

### m04-p13 · 新建时光胶囊

原稿：09-时光胶囊编辑新建页；现有本地数据键：dujia-capsule-draft。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回胶囊列表 | explicit-inline | location.href='m04-p12.html' |
| 2 | #name | name | native-input | 原生输入/选择 |
| 3 | #message | 愿我们在未来的日子里， 依然心怀热爱，彼此陪伴。 记得今天的约定， 也记得当时心动的瞬间。 | native-input | 原生输入/选择 |
| 4 | button.add-photo | 添加照片 | explicit-inline | document.querySelector('#photo').click() |
| 5 | #photo | (图标/无名称) | native-input | 原生输入/选择 |
| 6 | #opening | opening | native-input | 原生输入/选择 |
| 7 | #reminder | 开启提醒 | native-input | 原生输入/选择 |
| 8 | #draft | 暂存草稿 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 9 | button | 封存这份心意 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m04-p14 · 时光胶囊

原稿：10-时光胶囊详情页-已开启；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回胶囊列表 | explicit-inline | location.href='m04-p12.html' |
| 2 | #collect | 把这一刻收录进重要时刻 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m04-p15 · 时光胶囊

原稿：10-时光胶囊详情页-未到期开启；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回胶囊列表 | explicit-inline | location.href='m04-p12.html' |
| 2 | input | 开启当天提醒我 | native-input | 原生输入/选择 |

已有弹层/状态：未发现具名状态节点

### m04-p16 · 悄悄留言

原稿：11-悄悄留言列表页-正常态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回重要时刻 | explicit-inline | location.href='m04-p01.html' |
| 2 | button.link.ui-hit-text | 查看原记录 › | explicit-inline | location.href='m03-p08.html' |
| 3 | button.link.ui-hit-text | 查看原记录 › | explicit-inline | location.href='m04-p03.html' |
| 4 | button.link.ui-hit-text | 查看原记录 › | explicit-inline | location.href='m03-p08.html' |

已有弹层/状态：未发现具名状态节点

### m04-p17 · 悄悄留言

原稿：11-悄悄留言列表页-空状态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回重要时刻 | explicit-inline | location.href='m04-p01.html' |
| 2 | button.go | 去看看共同记录 | explicit-inline | location.href='m03-p06.html' |

已有弹层/状态：{'tag': 'p', 'id': None, 'class': 'empty', 'role': None, 'text': '还没有悄悄留言'}

### m05-p01 · 童话工坊

原稿：01-童话工坊首页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button | 做成童话漫画把回忆画成专属故事留下一格格心动瞬间 | explicit-inline | location.href='m05-p02.html' |
| 2 | button | 制作回忆影片让重要时刻动起来在光影里重温感动 | explicit-inline | location.href='m05-p05.html' |
| 3 | button.all.ui-hit-text | 查看全部 › | explicit-inline | location.href='m05-p09.html' |
| 4 | button | 已完成海边的那天2024.05.20 | explicit-inline | location.href='m05-p08.html' |
| 5 | button | 草稿雨后的晚餐编辑于 2024.05.18 | explicit-inline | location.href='m05-p08.html' |
| 6 | button.start | 开始一次创作 | explicit-inline | location.href='m05-p02.html' |

已有弹层/状态：未发现具名状态节点

### m05-p02 · 挑一段我们的回忆

原稿：02-创作素材选择页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回童话工坊 | explicit-inline | location.href='m05-p01.html' |
| 2 | button.option | 共同日记2026.08.28 · 阿梨写下 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button.option | 相册照片 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button.option | 重要时刻第一次一起看海 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button.option | 自由写一段回忆 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | #go | 用这些素材开始 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：未发现具名状态节点

### m05-p03 · 回忆转漫画

原稿：03-回忆转漫画编辑页；现有本地数据键：dujia-comic-story。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回素材选择 | explicit-inline | location.href='m05-p02.html' |
| 2 | #story | 回忆内容 | native-input | 原生输入/选择 |
| 3 | button.edit | 编辑 | explicit-inline | document.querySelector('#story').focus() |
| 4 | button | 暖暖水彩 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button | 复古漫画 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button | 轻柔铅笔 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | button | 温柔叙事贴近日常，细腻温暖 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 8 | button | 电影感光影氛围，节奏张力 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 9 | button.character | 默默 & 小满可爱自然 · 清新温柔 | explicit-inline | location.href='m05-p10.html' |
| 10 | #generate | 生成童话漫画 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：未发现具名状态节点

### m05-p04 · 照片转漫画

原稿：04-照片转漫画编辑页；现有本地数据键：dujia-comic-photo-story。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回素材选择 | explicit-inline | location.href='m05-p02.html' |
| 2 | button | 晚霞海边照片 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button | 烟花合照 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button | 牵手散步照片 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | #story | 补充这段故事 | native-input | 原生输入/选择 |
| 6 | button | 水彩 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | button | 素描 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 8 | button | 清新插画 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 9 | button | 油画 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 10 | button | 他 阳光温柔 | explicit-inline | location.href='m05-p10.html' |
| 11 | button | 她 温柔爱笑 | explicit-inline | location.href='m05-p10.html' |
| 12 | #generate | 生成童话漫画 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：未发现具名状态节点

### m05-p05 · 回忆影片

原稿：05-回忆影片编辑页；现有本地数据键：dujia-film-narration。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回工坊 | explicit-inline | location.href='m05-p01.html' |
| 2 | button.clip | 日记那天的日落 2023年05月20日 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button.clip | 照片海边笑起来 2023年08月14日 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button.clip | 重要时刻第一次旅行 2023年10月03日 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | #narration | 影片旁白 | native-input | 原生输入/选择 |
| 6 | #play | 试听晚风和海浪 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | button | 温柔手帐 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 8 | button | 治愈暖光 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 9 | button | 清新自然 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 10 | #generate | 生成回忆影片 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m05-p06 · 回忆正在变成童话

原稿：06-魔法生成中页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.return | 返回童话工坊 | explicit-inline | location.href='m05-p01.html' |

已有弹层/状态：{'tag': 'div', 'id': None, 'class': 'steps', 'role': 'status', 'text': '整理回忆已完成绘出故事进行中装订成册待开始'}

### m05-p07 · 这次魔法没有成功

原稿：07-生成失败页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button | 调整内容 | explicit-inline | location.href='m05-p03.html' |
| 2 | button | 重新生成 | explicit-inline | location.href='m05-p06.html' |
| 3 | button.home | 先回到童话工坊 ♡ | explicit-inline | location.href='m05-p01.html' |

已有弹层/状态：未发现具名状态节点

### m05-p08 · 海边的那天

原稿：08-作品详情页；现有本地数据键：dujia-comic-saved。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回我的创作 | explicit-inline | location.href='m05-p09.html' |
| 2 | button | 第1页 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button | 第2页 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button | 第3页 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button | 第4页 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button | 第5页 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | button | 第6页 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 8 | button | 第7页 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 9 | button | 第8页 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 10 | #save | 保存到共同相册 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 11 | #share | 给另一半看看 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 12 | button.retry.ui-hit-text | 重新生成 | explicit-inline | location.href='m05-p03.html' |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m05-p09 · 我的创作

原稿：09-我的创作页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.folder | 收藏夹 | explicit-inline | selectTab('漫画') |
| 2 | button | 全部 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button | 漫画 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button | 影片 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button | 草稿 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button.work.comic | 海边的那天 已收藏 漫画 | explicit-inline | location.href='m05-p08.html' |
| 7 | button.work.film | 晚风里的告白 影片 | explicit-inline | location.href='m05-p05.html' |
| 8 | button.work.progress | Our Memories正在把回忆装订成册65% 制作中慢慢来，都是我们最珍贵的时光 ♡ | explicit-inline | location.href='m05-p06.html' |
| 9 | button.work.draft | 雨后的晚餐 草稿继续编辑 › | explicit-inline | location.href='m05-p03.html' |
| 10 | button.start | 开始创作 | explicit-inline | location.href='m05-p01.html' |

已有弹层/状态：{'tag': 'p', 'id': 'empty', 'class': 'empty', 'role': None, 'text': '这里暂时没有作品'}

### m05-p10 · 我们的主角设定

原稿：10-我们的主角设定页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回童话工坊 | explicit-inline | location.href='m05-p01.html' |
| 2 | #appearance | (图标/无名称) | native-input | 原生输入/选择 |
| 3 | #outfit | (图标/无名称) | native-input | 原生输入/选择 |
| 4 | #mood | (图标/无名称) | native-input | 原生输入/选择 |
| 5 | #object | (图标/无名称) | native-input | 原生输入/选择 |
| 6 | #save | 更新我们的主角 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m06-p01 · 我的与设置

原稿：01-我的与设置首页；现有本地数据键：dujia-profile。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.profile | 小满 ♡已与阿舟关联 ♡ | explicit-inline | location.href='m06-p02.html' |
| 2 | button.row.world | 我们的小世界一起管理共同资料 | explicit-inline | location.href='m06-p03.html' |
| 3 | button.row.draft | 草稿箱 | explicit-inline | location.href='m06-p04.html' |
| 4 | button.row.tags | 标签管理 | explicit-inline | location.href='m06-p05.html' |
| 5 | button.row.member | 童话会员 | explicit-inline | location.href='m06-p06.html' |
| 6 | button.row.settings | 设置 | explicit-inline | location.href='m06-p07.html' |
| 7 | button.row.help | 帮助与关于 | explicit-inline | location.href='m06-p12.html' |

已有弹层/状态：未发现具名状态节点

### m06-p02 · 编辑个人资料

原稿：02-编辑个人资料页；现有本地数据键：dujia-avatar。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回我的与设置 | explicit-inline | location.href='m06-p01.html' |
| 2 | #avatar | 更换头像 | native-input | 原生输入/选择 |
| 3 | button.change.ui-hit-text | 更换头像 | explicit-inline | document.querySelector('#avatar').click() |
| 4 | #nickname | (图标/无名称) | native-input | 原生输入/选择 |
| 5 | #birthday | (图标/无名称) | native-input | 原生输入/选择 |
| 6 | #saying | (图标/无名称) | native-input | 原生输入/选择 |
| 7 | #color | (图标/无名称) | native-input | 原生输入/选择 |
| 8 | #save | 保存资料 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m06-p03 · 我们的小世界

原稿：03-我们的小世界页；现有本地数据键：dujia-joint-name。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回我的与设置 | explicit-inline | location.href='m06-p01.html' |
| 2 | button.row.nick | 共同昵称 小满与阿舟 | explicit-inline | editNickname() |
| 3 | button.row.portrait | 共同头像 | explicit-inline | location.href='m06-p02.html' |
| 4 | button.row.space | 共同空间设置哪些记录邀请对方一起看 | explicit-inline | location.href='m06-p09.html' |
| 5 | button.row.connection | 关联状态 | explicit-inline | notify('我们的关联状态：已关联') |
| 6 | button.unlink | 解除关联 | explicit-inline | notify('解除关联需要双方确认') |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m06-p04 · 草稿箱

原稿：04-草稿箱页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回我的与设置 | explicit-inline | location.href='m06-p01.html' |
| 2 | button.card.one | 雨天的电影刚刚保存仅自己可见草稿 | explicit-inline | location.href='m05-p05.html' |
| 3 | button.card.two | 给未来的一封信昨天仅自己可见草稿 | explicit-inline | location.href='m05-p03.html' |
| 4 | button.card.three | 旅行计划8 月 28 日共同记录草稿 | explicit-inline | location.href='m05-p03.html' |

已有弹层/状态：未发现具名状态节点

### m06-p05 · 标签管理

原稿：05-标签管理页；现有本地数据键：dujia-extra-tags。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回我的与设置 | explicit-inline | location.href='m06-p01.html' |
| 2 | button.plus | 新建标签 | explicit-inline | addTag() |
| 3 | button.tag.personal.daily | 日常 | explicit-inline | editTag(this) |
| 4 | button.tag.personal.travel | 旅行 | explicit-inline | editTag(this) |
| 5 | button.tag.personal.missing | 想念 | explicit-inline | editTag(this) |
| 6 | button.tag.personal.food | 美食 | explicit-inline | editTag(this) |
| 7 | button.tag.shared.picnic | 春日野餐 | explicit-inline | editTag(this) |
| 8 | button.tag.shared.first-trip | 第一次旅行 | explicit-inline | editTag(this) |
| 9 | button.tag.shared.home | 我们的家 | explicit-inline | editTag(this) |
| 10 | button.add | 新建标签 | explicit-inline | addTag() |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m06-p06 · 童话会员

原稿：06-童话会员页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回我的与设置 | explicit-inline | location.href='m06-p01.html' |
| 2 | button.open | 开通童话会员 | explicit-inline | notify('会员开通演示：当前未接入支付') |
| 3 | button.details.ui-hit-text | 查看会员说明 › | explicit-inline | notify('会员说明：更多时光胶囊、更大照片空间及专属装扮') |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m06-p07 · 设置

原稿：07-设置首页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回我的与设置 | explicit-inline | location.href='m06-p01.html' |
| 2 | button.row.security | 账号与安全 | explicit-inline | location.href='m06-p08.html' |
| 3 | button.row.privacy | 隐私与共同可见 | explicit-inline | location.href='m06-p09.html' |
| 4 | button.row.notifications | 通知设置 | explicit-inline | location.href='m06-p10.html' |
| 5 | button.row.storage | 数据与存储 | explicit-inline | location.href='m06-p11.html' |
| 6 | button.row.display | 显示与外观 | explicit-inline | notify('当前使用原稿的温暖手帐外观') |
| 7 | button.row.language | 语言 | explicit-inline | notify('当前语言：简体中文') |
| 8 | button.logout | 退出登录 | explicit-inline | if(confirm('退出当前登录？'))location.href='m01-p01.html' |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m06-p08 · 账号与安全

原稿：08-账号与安全页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回设置 | explicit-inline | location.href='m06-p07.html' |
| 2 | button.row.password | 修改密码 | explicit-inline | prompt('修改密码：请输入新密码') |
| 3 | button.row.phone | 绑定手机 | explicit-inline | prompt('绑定手机：请输入手机号') |
| 4 | button.row.devices | 登录设备 当前设备安全 | explicit-inline | alert('当前设备安全') |
| 5 | button.row.two-factor | 两步验证 | explicit-inline | alert('两步验证设置将在账号服务接入后开放') |
| 6 | button.logout | 退出登录 | explicit-inline | if(confirm('退出当前登录？'))location.href='m01-p01.html' |
| 7 | button.delete | 注销账号 | explicit-inline | alert('账号注销需要完成身份确认') |

已有弹层/状态：未发现具名状态节点

### m06-p09 · 隐私与共同可见

原稿：09-隐私与共同可见页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回设置 | explicit-inline | location.href='m06-p07.html' |
| 2 | #scope | 默认可见范围 仅自己可见 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button.switch.s1 | 共同可见 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button.switch.s2 | 共同空间 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button.switch.s3 | 另一半回应 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button.switch.s4 | 相关提醒 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：未发现具名状态节点

### m06-p10 · 通知设置

原稿：10-通知设置页；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回设置 | explicit-inline | location.href='m06-p07.html' |
| 2 | button.switch.s1 | 另一半回应 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button.switch.s2 | 重要时刻 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button.switch.s3 | 时光胶囊 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button.switch.s4 | 工坊完成 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button.switch.s5 | 通知总开关 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：未发现具名状态节点

### m06-p11 · 数据与存储

原稿：11-数据与存储页；现有本地数据键：dujia-auto-backup, dujia-last-backup, dujia-notifications, dujia-privacy, dujia-profile。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回设置 | explicit-inline | location.href='m06-p07.html' |
| 2 | #export | 导出我的记录 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | #backup | 共同记录备份 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | #auto | 自动备份 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button.row.manage | 存储空间管理 | explicit-inline | notify('存储空间：1.2 GB / 5 GB') |
| 6 | #cache | 清理缓存 128 MB | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m06-p12 · 帮助与关于

原稿：12-帮助与关于页；现有本地数据键：dujia-feedback-draft。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回我的与设置 | explicit-inline | location.href='m06-p01.html' |
| 2 | button.row.help | 使用帮助 | explicit-inline | notify('使用帮助：从首页记录你们的日常，在工坊创作专属作品') |
| 3 | button.row.feedback | 意见反馈 | explicit-inline | feedback() |
| 4 | button.row.privacy | 隐私政策 | explicit-inline | notify('隐私政策：你的私人记录由你决定是否共同可见') |
| 5 | button.row.terms | 用户协议 | explicit-inline | notify('用户协议：请爱护共同空间中的每一段回忆') |
| 6 | button.row.updates | 检查更新 | explicit-inline | notify('当前已是最新版本') |
| 7 | button.row.about | 关于独家童话 | explicit-inline | notify('独家童话 1.0.0 · 把平凡的日子写成童话') |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m07-p01 · 等待 TA 的确认

原稿：60-共同领养页-等待确认；现有本地数据键：dujia-pet。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | #remind | 提醒 TA 看看 › | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 2 | button.return | 暂时返回 | explicit-inline | location.href='m03-p01.html' |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m07-p02 · 一起领养小伙伴

原稿：60-共同领养页-选择宠物；现有本地数据键：dujia-pet。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.pet | 小狗 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 2 | button.pet | 小猫 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button.pet | 小兔 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button.pet | 小狐狸 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | #pet-name | (图标/无名称) | native-input | 原生输入/选择 |
| 6 | #invite | 邀请 TA 一起领养 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：未发现具名状态节点

### m07-p03 · 糯米的小屋

原稿：60-宠物空间首页-正常态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button | 互动 | explicit-inline | location.href='m07-p06.html' |
| 2 | button | 喂食 | explicit-inline | location.href='m07-p08.html' |
| 3 | button | 任务 | explicit-inline | location.href='m07-p10.html' |
| 4 | button | 装扮 | explicit-inline | location.href='m07-p12.html' |
| 5 | button | 布置小屋 | explicit-inline | location.href='m07-p15.html' |
| 6 | button | 成长故事 | explicit-inline | location.href='m07-p18.html' |
| 7 | button | 成就图鉴 | explicit-inline | location.href='m07-p21.html' |
| 8 | button.go | 去互动 › | explicit-inline | location.href='m07-p06.html' |

已有弹层/状态：未发现具名状态节点

### m07-p04 · 我们的宠物

原稿：60-宠物空间首页-首次领养；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.help | 照顾指南 | explicit-inline | notify('一起喂食、互动和布置小屋，照顾你们的小伙伴') |
| 2 | button.diary | 宠物日记 | explicit-inline | notify('领养后可以记录宠物日记') |
| 3 | button.adopt | 领养糯米 | explicit-inline | location.href='m07-p02.html' |
| 4 | button.guide | 先看看照顾指南 | explicit-inline | notify('每天照顾、陪伴与记录，都会成为你们的共同故事') |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m07-p05 · 糯米玩得好开心！

原稿：61-宠物互动页-互动成功；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.again | 再玩一次 | explicit-inline | location.href='m07-p06.html' |
| 2 | button.home | 回到小屋 | explicit-inline | location.href='m07-p03.html' |

已有弹层/状态：未发现具名状态节点

### m07-p06 · 和糯米玩一会儿

原稿：61-宠物互动页-正常态；现有本地数据键：dujia-pet-energy。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.option | 摸摸头精力 -5 · 亲密 +3 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 2 | button.option | 丢球球精力 -12 · 心情 +8 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button.option | 讲故事精力 -8 · 亲密 +6 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button.option | 送小礼物消耗 1 份礼物 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | #play | 和糯米互动 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：未发现具名状态节点

### m07-p07 · 和糯米互动

原稿：61-宠物互动页-精力不足；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 宠物空间 | explicit-inline | location.href='m07-p03.html' |
| 2 | button.diary.ui-hit-text | 成长日记 | explicit-inline | location.href='m07-p18.html' |
| 3 | button.feed | 去喂食补充精力 › | explicit-inline | location.href='m07-p08.html' |

已有弹层/状态：未发现具名状态节点

### m07-p08 · 给糯米喂点好吃的

原稿：62-喂食页-正常态；现有本地数据键：dujia-food-stock, dujia-pet-satiety。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button | 香香狗粮×12 饱食 +12 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 2 | button | 爱心小饼干×5 饱食 +8 · 心情 +2 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button | 草莓布丁×1 饱食 +20 · 心情 +5 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | #feed | 喂给糯米 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button.more | 去获得更多食物 › | explicit-inline | location.href='m07-p10.html' |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m07-p09 · 给糯米喂食

原稿：62-喂食页-资源不足；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 宠物空间 | explicit-inline | location.href='m07-p03.html' |
| 2 | button.task | 去做任务 | explicit-inline | location.href='m07-p10.html' |

已有弹层/状态：{'tag': 'p', 'id': None, 'class': 'empty', 'role': None, 'text': '食物用完啦'}

### m07-p10 · 一起完成啦！

原稿：63-任务页-奖励领取；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.wear | 去给糯米换上 | explicit-inline | location.href='m07-p12.html' |

已有弹层/状态：未发现具名状态节点

### m07-p11 · 一起照顾糯米

原稿：63-任务页-正常态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button | 每日任务 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 2 | button | 本周约定 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button.task-button.b2 | 完成陪糯米互动 | explicit-inline | location.href='m07-p06.html' |
| 4 | button.task-button.b3 | 完成整理小屋 | explicit-inline | location.href='m07-p15.html' |
| 5 | button.next | 去完成下一件事 | explicit-inline | location.href='m07-p06.html' |

已有弹层/状态：未发现具名状态节点

### m07-p12 · 给糯米换新装

原稿：64-宠物装扮页-正常态；现有本地数据键：dujia-pet-outfit。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回宠物小屋 | explicit-inline | location.href='m07-p03.html' |
| 2 | button | 衣服 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button | 配饰 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button | 小物 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button.item | 小花围巾已拥有 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button.item | 格纹蝴蝶结已拥有 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | button.item.locked | 星星领结亲密度 160 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 8 | button.item.locked | 蜜桃帽子完成故事解锁 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 9 | #save | 保存这身搭配 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'p', 'id': 'toast', 'class': 'toast', 'role': 'status', 'text': ''}

### m07-p13 · 给糯米换装

原稿：64-宠物装扮页-资源不足；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 宠物空间 | explicit-inline | location.href='m07-p03.html' |
| 2 | button.task | 去做任务 | explicit-inline | location.href='m07-p11.html' |

已有弹层/状态：未发现具名状态节点

### m07-p14 · 小屋布置完成

原稿：65-房间布置页-保存成功；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.primary | 继续布置 | explicit-inline | location.href='m07-p15.html' |
| 2 | button.secondary | 回到小屋 | explicit-inline | location.href='m07-p03.html' |

已有弹层/状态：未发现具名状态节点

### m07-p15 · 一起布置糯米的小屋

原稿：65-房间布置页-正常态；现有本地数据键：fairy-room-rug, fairy-room-saved。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button | 地毯 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 2 | button | 小床 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button | 墙饰 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button | 摆件 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button | 花朵地毯已使用 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button | 格纹地毯可使用 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | button | 月亮地毯亲密度 150 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 8 | button | 野餐垫 成就解锁 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 9 | button.save | 保存小屋布置 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'span', 'id': None, 'class': 'saved', 'role': 'status', 'text': '✓ 已保存'}；{'tag': 'div', 'id': None, 'class': 'toast', 'role': 'status', 'text': ''}

### m07-p16 · 布置糯米的小屋

原稿：65-房间布置页-资源不足；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 宠物空间 | explicit-inline | location.href='m07-p03.html' |
| 2 | button.cta | 去完成任务 | explicit-inline | location.href='m07-p11.html' |

已有弹层/状态：未发现具名状态节点

### m07-p17 · 糯米的成长故事

原稿：66-成长故事页-回忆权限失效；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 宠物空间 | explicit-inline | location.href='m07-p03.html' |
| 2 | button.return | 返回宠物空间 | explicit-inline | location.href='m07-p03.html' |

已有弹层/状态：未发现具名状态节点

### m07-p18 · 糯米的成长故事

原稿：66-成长故事页-正常态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.view | 查看这一页 › | explicit-inline | location.href='m07-p19.html' |

已有弹层/状态：未发现具名状态节点

### m07-p19 · 第 27 天 · 今天也被好好照顾

原稿：66-成长故事页-章节详情；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.next | 写下今天的下一页 | explicit-inline | location.href='m07-p20.html' |

已有弹层/状态：未发现具名状态节点

### m07-p20 · 我们的宠物成就

原稿：67-成就页-奖励领取；现有本地数据键：fairy-achievement-30。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 宠物空间 | explicit-inline | location.href='m07-p03.html' |
| 2 | button.claim | 领取奖励 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：未发现具名状态节点

### m07-p21 · 我们和糯米的成就

原稿：67-成就页-正常态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button | 第一次见面 已点亮 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 2 | button | 默契喂食 已点亮 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button | 玩到天黑 已点亮 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button | 小屋变新了 已点亮 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button | 连续照顾 7 天进度 5 / 7 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button | 亲密搭档亲密度 128 / 160 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | button.cta | 去完成今天的照顾 | explicit-inline | location.href='m07-p11.html' |

已有弹层/状态：{'tag': 'div', 'id': None, 'class': 'toast', 'role': 'status', 'text': ''}

### m07-p22 · 糯米的收藏图鉴

原稿：68-宠物图鉴页-正常态；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button | 装扮 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 2 | button | 小屋 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button | 纪念物 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button | 小花围巾已拥有 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button | 格纹蝴蝶结已拥有 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button | 星星领结亲密度 160 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | button | 蜜桃帽子成长故事解锁 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 8 | button | 雨天小斗篷 连续照顾 7 天 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 9 | button | 晚安铃铛 未知 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'div', 'id': None, 'class': 'toast', 'role': 'status', 'text': ''}

### m07-p23 · 小花围巾

原稿：68-宠物图鉴页-详情态；现有本地数据键：fairy-pet-outfit。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回图鉴 | explicit-inline | location.href='m07-p22.html' |
| 2 | #wear | 去换上 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button.return | 返回图鉴 | explicit-inline | location.href='m07-p22.html' |

已有弹层/状态：未发现具名状态节点

### m07-p24 · 在告别前，再确认一次

原稿：69-宠物设置页-导出与删除确认；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | #export | 先导出成长记录 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 2 | #unlink | 暂时解除共同照顾 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button.action.cancel | 我再想想，返回 | explicit-inline | location.href='m07-p25.html' |

已有弹层/状态：{'tag': 'div', 'id': None, 'class': 'toast', 'role': 'status', 'text': ''}

### m07-p25 · 糯米的小屋设置

原稿：69-宠物设置页-正常态；现有本地数据键：fairy-pet-remind-time。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回宠物空间 | explicit-inline | location.href='m07-p03.html' |
| 2 | #time | 共同提醒每天 20:30 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button.switch.s1 | 共同提醒 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | #notice | 照顾通知 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button.switch.s2 | 照顾通知 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | #story | 成长故事自动收录 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | button.switch.s3 | 成长故事自动收录 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 8 | #export | 导出糯米的成长记录 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 9 | #explain | 仅我们可见说明 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 10 | button.row.ui-hit-text.r6 | 暂时解除共同照顾不会删除糯米与共同回忆 | explicit-inline | location.href='m07-p24.html' |

已有弹层/状态：{'tag': 'div', 'id': None, 'class': 'toast', 'role': 'status', 'text': ''}

### m08-p01 · 共同回忆册

原稿：01-书架；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button | 我们的夏天 | explicit-inline | location.href='m08-p04.html' |
| 2 | button | 第一次旅行 | explicit-inline | location.href='m08-p04.html' |
| 3 | button | 小小日常 | explicit-inline | location.href='m08-p04.html' |
| 4 | button.continue-link | 继续阅读 › | explicit-inline | location.href='m08-p04.html' |
| 5 | button.new | 新建回忆册 | explicit-inline | location.href='m08-p03.html' |

已有弹层/状态：未发现具名状态节点

### m08-p02 · 共同回忆册

原稿：02-空书架；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回 | explicit-inline | location.href='m08-p01.html' |
| 2 | button.new | 新建第一本回忆册 | explicit-inline | location.href='m08-p03.html' |

已有弹层/状态：{'tag': 'h2', 'id': None, 'class': 'empty', 'role': None, 'text': '还没有共同回忆册'}

### m08-p03 · 本月回忆推荐

原稿：03-本月回忆推荐；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回回忆册 | explicit-inline | location.href='m08-p01.html' |
| 2 | button.confirm | 查看并确认素材 | explicit-inline | location.href='m08-p05.html' |
| 3 | button.skip | 暂不创建 | explicit-inline | location.href='m08-p04.html' |

已有弹层/状态：未发现具名状态节点

### m08-p04 · 新建回忆册

原稿：04-新建回忆册-基础信息；现有本地数据键：fairy-memory-draft。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回 | explicit-inline | location.href='m08-p01.html' |
| 2 | input.book-name | 书名 | native-input | 原生输入/选择 |
| 3 | input | 开始月份 | native-input | 原生输入/选择 |
| 4 | input | 结束月份 | native-input | 原生输入/选择 |
| 5 | button | 从共同素材开始 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button | 空白回忆册 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | button.next | 下一步：选择主题 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'div', 'id': None, 'class': 'toast', 'role': 'status', 'text': ''}

### m08-p05 · 为这本书挑一件外衣

原稿：05-主题与封面选择；现有本地数据键：fairy-memory-cover-photo, fairy-memory-draft, fairy-memory-theme。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回上一步 | explicit-inline | location.href='m08-p04.html' |
| 2 | button.ui-art-selection | 花园午后 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button.ui-art-selection | 旅行手札 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button.ui-art-selection | 暖灯日常 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button.toggle | 使用封面照片 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button.next | 下一步：选择素材 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：未发现具名状态节点

### m08-p06 · 选择共同素材

原稿：06-选择共同素材；现有本地数据键：fairy-memory-selected。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回上一步 | explicit-inline | location.href='m08-p05.html' |
| 2 | button | 全部 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button | 日记 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button | 照片 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button | 时刻 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button | 工坊 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | button | 宠物 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 8 | button.item | 晚霞散步今天的晚霞把天空染成了橘粉色，我们手牵手走在江边，好像时间都慢了下来。2024.05.18晚霞散步日记2024.05.18 20:47共同可见 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 9 | button.item | 一起看日落照片2024.04.21 18:36共同可见 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 10 | button.item | 厦门之旅第一次旅行重要时刻2023.10.03 – 10.06共同可见 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 11 | button.item | 鼓浪屿的风都温柔手作明信片工坊作品2024.02.14 15:22共同可见 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 12 | button.item | 团子学会握手宠物2024.03.09 11:08共同可见 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 13 | button.next | 开始编排 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'div', 'id': None, 'class': 'toast', 'role': 'status', 'text': ''}

### m08-p07 · 素材预览

原稿：07-素材预览与确认；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回素材选择 | explicit-inline | location.href='m08-p06.html' |
| 2 | button.skip | 暂不放入 | explicit-inline | location.href='m08-p06.html' |
| 3 | button.add | 放入回忆册 | explicit-inline | location.href='m08-p08.html' |

已有弹层/状态：未发现具名状态节点

### m08-p08 · 为回忆选一页版式

原稿：08-选择回忆页模板；现有本地数据键：fairy-memory-template。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回素材预览 | explicit-inline | location.href='m08-p07.html' |
| 2 | button | 2024.04.21 周日今天一起去了海边，风很温柔，你在笑，我也觉得整个世界都亮了起来。日记摘录 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button | 那天的晚霞好美呀～照片故事 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button | 我们的重要时刻2023.05.20第一次约会2023.08.10一起旅行2024.02.14确定关系重要时刻 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button | 一起完成的小作品工坊作品 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button | 小家伙的成长日记2个月 6个月 1岁宠物成长 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | button | · 第三章 ·平凡的日子也闪闪发光章节扉页 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 8 | button.use | 使用这个模板 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：未发现具名状态节点

### m08-p09 · 编排日记摘录页

原稿：09-日记摘录页编排；现有本地数据键：fairy-memory-page。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回版式选择 | explicit-inline | location.href='m08-p08.html' |
| 2 | #page-title | (图标/无名称) | native-input | 原生输入/选择 |
| 3 | #excerpt | 天边被晚霞染成了温柔的橘粉色， 我们并肩走着，风也轻轻地。 | native-input | 原生输入/选择 |
| 4 | #date | (图标/无名称) | native-input | 原生输入/选择 |
| 5 | #message | (图标/无名称) | native-input | 原生输入/选择 |
| 6 | #changeExcerpt | 换摘录换一段日记 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | #changePhoto | 换照片换一张照片 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 8 | #changeTemplate | 换版式换一种排版 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 9 | button.done | 完成这一页 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'div', 'id': None, 'class': 'toast', 'role': 'status', 'text': ''}

### m08-p10 · 编排照片故事页

原稿：10-照片故事页编排；现有本地数据键：fairy-memory-photo-page。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back.ui-hit-text | 返回 | explicit-inline | location.href='m08-p08.html' |
| 2 | button.preview.ui-hit-text | 预览 | explicit-inline | location.href='m08-p13.html' |
| 3 | input.page-title | 书页标题 | native-input | 原生输入/选择 |
| 4 | input.date | 书页日期 | native-input | 原生输入/选择 |
| 5 | button.crop.one | 裁剪/替换 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button.crop.two | 裁剪/替换 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | button.crop.three | 裁剪/替换 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 8 | textarea.caption | 这一页的想法 | native-input | 原生输入/选择 |
| 9 | button.done | 完成这一页 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 10 | button | 添加照片 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 11 | button | 添加文字 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 12 | button | 添加贴纸 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 13 | button | 更换模板 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'div', 'id': None, 'class': 'toast', 'role': 'status', 'text': ''}

### m08-p11 · 编排重要时刻页

原稿：11-重要时刻页编排；现有本地数据键：fairy-memory-moment。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回版式选择 | explicit-inline | location.href='m08-p08.html' |
| 2 | input.moment | 时刻主题 | native-input | 原生输入/选择 |
| 3 | input.date | 日期 | native-input | 原生输入/选择 |
| 4 | button.change-photo | 更换照片 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button.select-action | 选择时刻 › | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button.quote-action | 添加一句话 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | button.done | 完成这一页 ♡ | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'div', 'id': None, 'class': 'toast', 'role': 'status', 'text': ''}

### m08-p12 · 作品与宠物成长

原稿：12-作品与宠物成长页编排；现有本地数据键：fairy-memory-pet-page。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回版式选择 | explicit-inline | location.href='m08-p08.html' |
| 2 | button | 工坊作品 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button | 宠物成长 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | input.caption | 成长说明 | native-input | 原生输入/选择 |
| 5 | button | 换内容 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button | 换照片 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | button | 添加说明 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 8 | button.done | 完成这一页 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'div', 'id': None, 'class': 'toast', 'role': 'status', 'text': ''}

### m08-p13 · 整理章节与页序

原稿：13-章节与页序整理；现有本地数据键：fairy-memory-order。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回编排 | explicit-inline | location.href='m08-p09.html' |
| 2 | button | 01初遇的心动 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button | 02一起看日落 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button | 03记录小美好 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button | 01夏夜的摩天轮 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button | 02烟花下的约定 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | button | 03星空下的悄悄话 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 8 | button.add | 新增章节 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 9 | button.save | 保存排列 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'div', 'id': None, 'class': 'toast', 'role': 'status', 'text': ''}

### m08-p14 · 这本回忆书完成啦

原稿：14-建册完成；现有本地数据键：fairy-memory-draft。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.read | 开始翻阅 | explicit-inline | location.href='m08-p15.html' |
| 2 | button.continue | 继续整理 | explicit-inline | location.href='m08-p13.html' |

已有弹层/状态：未发现具名状态节点

### m08-p15 · 我们的夏天

原稿：15-回忆册目录；现有本地数据键：fairy-memory-draft。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回书架 | explicit-inline | location.href='m08-p01.html' |
| 2 | a | 1. 那天，阳光刚刚好 1 | explicit-inline | m08-p16.html |
| 3 | a | 2. 一起吃的第一支冰淇淋 2 | explicit-inline | m08-p16.html |
| 4 | a | 3. 藏在风里的喜欢 3 | explicit-inline | m08-p16.html |
| 5 | a | 4. 我们的第一张合照 有补页4 | explicit-inline | m08-p16.html |
| 6 | a | 5. 你笑起来真好看 5 | explicit-inline | m08-p16.html |
| 7 | a | 6. 夏天的傍晚，晚风很温柔 6 | explicit-inline | m08-p16.html |
| 8 | a | 7. 海边的日落与你 7 | explicit-inline | m08-p16.html |
| 9 | a | 8. 烟花下许的愿 8 | explicit-inline | m08-p16.html |
| 10 | a | 9. 手牵手，走很长很长的路 9 | explicit-inline | m08-p16.html |
| 11 | a | 10. 属于我们的歌单 10 | explicit-inline | m08-p16.html |
| 12 | a | 11. 一起看过的星星 11 | explicit-inline | m08-p16.html |
| 13 | a | 12. 八月，未完待续 12 | explicit-inline | m08-p16.html |
| 14 | button.start | 从第 1 页开始 → | explicit-inline | location.href='m08-p16.html' |

已有弹层/状态：未发现具名状态节点

### m08-p16 · 独家童话

原稿：16-沉浸翻阅页；现有本地数据键：fairy-memory-bookmark-6。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回 | explicit-inline | location.href='m08-p15.html' |
| 2 | button.toc | 目录 | explicit-inline | location.href='m08-p17.html' |
| 3 | button.bookmark | 书签 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button.next-page | 下一页 | explicit-inline | location.href='m08-p18.html' |

已有弹层/状态：未发现具名状态节点

### m08-p17 · 阅读工具

原稿：17-阅读工具菜单；现有本地数据键：无。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回阅读 | explicit-inline | location.href='m08-p16.html' |
| 2 | button | 目录查看全书目录和章节 | explicit-inline | location.href='m08-p15.html' |
| 3 | button | 书签查看和管理我的书签 | explicit-inline | location.href='m08-p19.html' |
| 4 | button | 添加补页在书中添加新的补充页 | explicit-inline | location.href='m08-p18.html' |
| 5 | button | 整理这本书调整页序、重命名、导出等 | explicit-inline | location.href='m08-p13.html' |
| 6 | button | 更多设置阅读偏好、背景音乐等设置 | explicit-inline | location.href='m08-p21.html' |

已有弹层/状态：未发现具名状态节点

### m08-p18 · 为这一页加一张补页

原稿：18-添加双人补页；现有本地数据键：fairy-memory-supplement-kind。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回阅读 | explicit-inline | location.href='m08-p16.html' |
| 2 | button.toc | 回到目录 | explicit-inline | location.href='m08-p15.html' |
| 3 | button | 写几句话记录此刻的想法与心情 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button | 送一个表情用一个表情传达你的心意 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button | 附上一张照片用一张照片定格这份回忆 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button.next | 选择回应方式 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：未发现具名状态节点

### m08-p19 · 写一张补页

原稿：19-双人补页编辑；现有本地数据键：fairy-memory-supplement。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回补页选择 | explicit-inline | location.href='m08-p18.html' |
| 2 | textarea.message | 补页文字 | native-input | 原生输入/选择 |
| 3 | button | 爱心 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 4 | button | 星星 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button | 微笑 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button | 花朵 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | input | (图标/无名称) | native-input | 原生输入/选择 |
| 8 | button.submit | 放进回忆书 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：未发现具名状态节点

### m08-p20 · 独家童话

原稿：20-含补页的阅读状态；现有本地数据键：fairy-memory-bookmark-7, fairy-memory-supplement。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回阅读工具 | explicit-inline | location.href='m08-p17.html' |
| 2 | button.toc | 目录 | explicit-inline | location.href='m08-p15.html' |
| 3 | button.bookmark | 书签 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：未发现具名状态节点

### m08-p21 · 管理这本回忆册

原稿：21-回忆册管理与删除确认；现有本地数据键：fairy-memory-book-archived, fairy-memory-book-name, fairy-memory-supplement。

| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |
| ---: | --- | --- | --- | --- |
| 1 | button.back | 返回阅读 | explicit-inline | location.href='m08-p17.html' |
| 2 | button.rename | 修改书名与封面 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 3 | button | 整理页序 | explicit-inline | location.href='m08-p13.html' |
| 4 | button.archive | 归档回忆册 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 5 | button.show-delete | 删除这本回忆册 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 6 | button.cancel | 取消 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |
| 7 | button.delete | 确认删除 | requires-handler-review | 详见页面脚本，需要人工匹配事件 |

已有弹层/状态：{'tag': 'h2', 'id': None, 'class': 'dialog-title', 'role': None, 'text': '确定删除《我们的夏天》？'}；{'tag': 'p', 'id': None, 'class': 'dialog-copy', 'role': None, 'text': '删除后无法恢复，原始共同记录不会被删除。'}
