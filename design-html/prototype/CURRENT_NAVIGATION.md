# 当前页面导航与来源

本轮114页初态观察与754项控件结果均对应当前源码；实际导航393条。每次操作使用独立本地模拟数据。逐项结果：[evidence/current/initial-controls-20261031-accessible/results.json](evidence/current/initial-controls-20261031-accessible/results.json)；机器可读合同：[evidence/current/initial-controls-20261031-accessible/contracts.json](evidence/current/initial-controls-20261031-accessible/contracts.json)。

这里只证明声明初态的可用控件，不替代隐藏／条件分支、全部错误／返回／长输入、连续流程、原稿视觉及原41项完整验收。旧全量JSON与原图保留历史版本，不将旧报告重绑为新源码。

本轮实线关系图：[CURRENT_INITIAL_NAVIGATION.mmd](CURRENT_INITIAL_NAVIGATION.mmd)。原PAGE_RELATIONSHIPS与回忆册隐藏关系图保留各自历史范围；完整条件图仍需按当前证据统一。

| 来源页 | 操作 | 当前行为合同 | 实际目标 | 实际URL | 结果行 |
| --- | --- | --- | --- | --- | --- |
| m01-p01 | 登录并开始 | route:m01-p02 | m01-p02 | http://127.0.0.1:8765/pages/m01-p02.html | 0 |
| m01-p01 | 创建账号 | route:m01-p03 | m01-p03 | http://127.0.0.1:8765/pages/m01-p03.html | 1 |
| m01-p02 | 返回 | route:m01-p01 | m01-p01 | http://127.0.0.1:8765/pages/m01-p01.html | 2 |
| m01-p02 | 忘记密码？ | route:m01-p04 | m01-p04 | http://127.0.0.1:8765/pages/m01-p04.html | 6 |
| m01-p02 | 登录并回到故事里 | login:m02-p01 | m02-p01 | http://127.0.0.1:8765/pages/m02-p01.html | 7 |
| m01-p02 | 创建账号 | route:m01-p03 | m01-p03 | http://127.0.0.1:8765/pages/m01-p03.html | 8 |
| m01-p03 | 返回欢迎页 | route:m01-p01 | m01-p01 | http://127.0.0.1:8765/pages/m01-p01.html | 11 |
| m01-p03 | 创建账号 | register:m01-p07 | m01-p07 | http://127.0.0.1:8765/pages/m01-p07.html | 21 |
| m01-p03 | 去登录 | route:m01-p02 | m01-p02 | http://127.0.0.1:8765/pages/m01-p02.html | 22 |
| m01-p04 | 返回 | route:m01-p02 | m01-p02 | http://127.0.0.1:8765/pages/m01-p02.html | 23 |
| m01-p04 | 下一步 | recovery:m01-p07 | m01-p07 | http://127.0.0.1:8765/pages/m01-p07.html | 27 |
| m01-p04 | 返回登录 | route:m01-p02 | m01-p02 | http://127.0.0.1:8765/pages/m01-p02.html | 28 |
| m01-p05 | 返回找回密码 | route:m01-p04 | m01-p04 | http://127.0.0.1:8765/pages/m01-p04.html | 29 |
| m01-p05 | 确认并重置 | reset:m01-p08 | m01-p08 | http://127.0.0.1:8765/pages/m01-p08.html | 34 |
| m01-p06 | 返回 | route:m01-p02 | m01-p02 | http://127.0.0.1:8765/pages/m01-p02.html | 35 |
| m01-p06 | 再试一次 | retry:m02-p01 | m02-p01 | http://127.0.0.1:8765/pages/m02-p01.html | 38 |
| m01-p06 | 找回密码 | route:m01-p04 | m01-p04 | http://127.0.0.1:8765/pages/m01-p04.html | 39 |
| m01-p07 | 返回 | route:m01-p04 | m01-p04 | http://127.0.0.1:8765/pages/m01-p04.html | 40 |
| m01-p07 | 验证并继续 | verify:m01-p05 | m01-p05 | http://127.0.0.1:8765/pages/m01-p05.html | 47 |
| m01-p08 | 返回登录 | route:m01-p02 | m01-p02 | http://127.0.0.1:8765/pages/m01-p02.html | 49 |
| m02-p01 | 返回登录 | route:m01-p02 | m01-p02 | http://127.0.0.1:8765/pages/m01-p02.html | 50 |
| m02-p01 | 邀请 TA 加入 / 生成专属邀请码 | route:m02-p02 | m02-p02 | http://127.0.0.1:8765/pages/m02-p02.html | 51 |
| m02-p01 | 输入 TA 的邀请码 / 接受一份特别邀请 | route:m02-p03 | m02-p03 | http://127.0.0.1:8765/pages/m02-p03.html | 52 |
| m02-p02 | 返回建立关系 | route:m02-p01 | m02-p01 | http://127.0.0.1:8765/pages/m02-p01.html | 53 |
| m02-p03 | 返回 | route:m02-p01 | m02-p01 | http://127.0.0.1:8765/pages/m02-p01.html | 57 |
| m02-p03 | 查看邀请内容 | invite:m02-p04 | m02-p04 | http://127.0.0.1:8765/pages/m02-p04.html | 62 |
| m02-p03 | 请让 TA 分享给你 | route:m02-p01 | m02-p01 | http://127.0.0.1:8765/pages/m02-p01.html | 63 |
| m02-p04 | 返回 | route:m02-p03 | m02-p03 | http://127.0.0.1:8765/pages/m02-p03.html | 64 |
| m02-p04 | 确认建立关系 | bind:m02-p05 | m02-p05 | http://127.0.0.1:8765/pages/m02-p05.html | 65 |
| m02-p04 | 暂不接受 | cancel:m02-p01 | m02-p01 | http://127.0.0.1:8765/pages/m02-p01.html | 66 |
| m02-p05 | 去写第一篇共同日记 ♡ | route:m03-p05 | m03-p05 | http://127.0.0.1:8765/pages/m03-p05.html | 67 |
| m02-p05 | 完善情侣资料 | route:m02-p06 | m02-p06 | http://127.0.0.1:8765/pages/m02-p06.html | 68 |
| m02-p05 | 先逛逛我们的首页 | route:m03-p01 | m03-p01 | http://127.0.0.1:8765/pages/m03-p01.html | 69 |
| m02-p06 | 返回 | route:m02-p05 | m02-p05 | http://127.0.0.1:8765/pages/m02-p05.html | 70 |
| m02-p06 | 保存小资料 | profile:m02-p01 | m02-p01 | http://127.0.0.1:8765/pages/m02-p01.html | 74 |
| m02-p07 | 返回邀请卡 | route:m02-p02 | m02-p02 | http://127.0.0.1:8765/pages/m02-p02.html | 75 |
| m02-p08 | 请 TA 重新邀请 | renew:m02-p01 | m02-p01 | http://127.0.0.1:8765/pages/m02-p01.html | 78 |
| m02-p08 | 重新输入邀请码 | route:m02-p03 | m02-p03 | http://127.0.0.1:8765/pages/m02-p03.html | 79 |
| m02-p09 | 回到我们的首页 | route:m03-p01 | m03-p01 | http://127.0.0.1:8765/pages/m03-p01.html | 80 |
| m02-p09 | 查看关系设置 | route:m02-p06 | m02-p06 | http://127.0.0.1:8765/pages/m02-p06.html | 81 |
| m03-p01 | 搜索共同记录 | route:m03-p03 | m03-p03 | http://127.0.0.1:8765/pages/m03-p03.html | 82 |
| m03-p01 | 写日记 | route:m03-p05 | m03-p05 | http://127.0.0.1:8765/pages/m03-p05.html | 83 |
| m03-p01 | 添加照片 | route:m03-p11 | m03-p11 | http://127.0.0.1:8765/pages/m03-p11.html | 84 |
| m03-p01 | 去童话工坊，把回忆变成故事 › | route:m05-p01 | m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 85 |
| m03-p01 | 重要时刻 | nav:m04-p02 | m04-p02 | http://127.0.0.1:8765/pages/m04-p02.html | 87 |
| m03-p01 | 工坊 | nav:m05-p01 | m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 88 |
| m03-p01 | 宠物 | nav:pet | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 89 |
| m03-p01 | 我的 | nav:m06-p01 | m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 90 |
| m03-p02 | 搜索共同记录 | route:m03-p03 | m03-p03 | http://127.0.0.1:8765/pages/m03-p03.html | 91 |
| m03-p02 | 写日记 / 记录心情 | route:m03-p05 | m03-p05 | http://127.0.0.1:8765/pages/m03-p05.html | 92 |
| m03-p02 | 添加照片 / 珍藏瞬间 | route:m03-p11 | m03-p11 | http://127.0.0.1:8765/pages/m03-p11.html | 93 |
| m03-p02 | 去童话工坊，把回忆变成故事 › | route:m05-p01 | m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 94 |
| m03-p02 | 查看全部 › | route:m03-p06 | m03-p06 | http://127.0.0.1:8765/pages/m03-p06.html | 95 |
| m03-p02 | 共同日记 小满 · 共同可见 | route:m03-p08 | m03-p08 | http://127.0.0.1:8765/pages/m03-p08.html?id=audit-diary | 96 |
| m03-p02 | 自己的日记 小满 · 仅自己可见 | route:m03-p07 | m03-p07 | http://127.0.0.1:8765/pages/m03-p07.html?id=audit-private | 97 |
| m03-p02 | 共同照片 小满 · 共同可见 | route:m03-p12 | m03-p12 | http://127.0.0.1:8765/pages/m03-p12.html?id=audit-photo | 98 |
| m03-p02 | 共同测试册 / 从目录开始阅读 / 继续阅读 › | route:m08-p15 | m08-p15 | http://127.0.0.1:8765/pages/m08-p15.html?id=book-state | 99 |
| m03-p02 | 下一件重要时刻 / 未来的纪念日 · 54 天后 / 查看纪念日 › | route:m04-p10 | m04-p10 | http://127.0.0.1:8765/pages/m04-p10.html?id=audit-anniversary | 100 |
| m03-p02 | 重要时刻 | nav:m04-p01 | m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 102 |
| m03-p02 | 工坊 | nav:m05-p01 | m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 103 |
| m03-p02 | 宠物 | nav:pet | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 104 |
| m03-p02 | 我的 | nav:m06-p01 | m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 105 |
| m03-p03 | 返回首页 | route:m03-p01 | m03-p01 | http://127.0.0.1:8765/pages/m03-p01.html | 106 |
| m03-p03 | 晚霞 | search-chip:晚霞 | m03-p04 | http://127.0.0.1:8765/pages/m03-p04.html?q=%E6%99%9A%E9%9C%9E | 109 |
| m03-p03 | 火锅 | search-chip:火锅 | m03-p04 | http://127.0.0.1:8765/pages/m03-p04.html?q=%E7%81%AB%E9%94%85 | 110 |
| m03-p03 | 旅行 | search-chip:旅行 | m03-p04 | http://127.0.0.1:8765/pages/m03-p04.html?q=%E6%97%85%E8%A1%8C | 111 |
| m03-p03 | 日记 | search-chip:日记 | m03-p04 | http://127.0.0.1:8765/pages/m03-p04.html?q=%E6%97%A5%E8%AE%B0 | 112 |
| m03-p03 | 照片 | search-chip:照片 | m03-p04 | http://127.0.0.1:8765/pages/m03-p04.html?q=%E7%85%A7%E7%89%87 | 113 |
| m03-p03 | 旅行 | search-chip:旅行 | m03-p04 | http://127.0.0.1:8765/pages/m03-p04.html?q=%E6%97%85%E8%A1%8C | 114 |
| m03-p03 | 纪念日 | search-chip:纪念日 | m03-p04 | http://127.0.0.1:8765/pages/m03-p04.html?q=%E7%BA%AA%E5%BF%B5%E6%97%A5 | 115 |
| m03-p04 | 返回搜索 | route:m03-p03 | m03-p03 | http://127.0.0.1:8765/pages/m03-p03.html | 116 |
| m03-p04 | 清除 | clear-query | m03-p03 | http://127.0.0.1:8765/pages/m03-p03.html | 118 |
| m03-p04 | 共同日记 真正可编辑的共同正文 共同可见 | route:m03-p08 | m03-p08 | http://127.0.0.1:8765/pages/m03-p08.html?id=audit-diary | 119 |
| m03-p04 | 共同照片 共同照片说明 共同可见 | route:m03-p12 | m03-p12 | http://127.0.0.1:8765/pages/m03-p12.html?id=audit-photo | 120 |
| m03-p05 | 返回日记列表 | route:m03-p06 | m03-p06 | http://127.0.0.1:8765/pages/m03-p06.html | 121 |
| m03-p05 | 存草稿 | diary-draft | m03-p06 | http://127.0.0.1:8765/pages/m03-p06.html | 122 |
| m03-p05 | 保存日记 | diary-save | m03-p06 | http://127.0.0.1:8765/pages/m03-p06.html | 129 |
| m03-p06 | 返回首页 | route:m03-p02 | m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 130 |
| m03-p06 | 写日记 | route:m03-p05 | m03-p05 | http://127.0.0.1:8765/pages/m03-p05.html | 134 |
| m03-p06 | 共同日记 真正可编辑的共同正文 小满 · 2026/10/4 · 共同可见 | route:m03-p08 | m03-p08 | http://127.0.0.1:8765/pages/m03-p08.html?id=audit-diary | 135 |
| m03-p06 | 自己的日记 独立私密正文 小满 · 2026/10/4 · 仅自己可见 | route:m03-p07 | m03-p07 | http://127.0.0.1:8765/pages/m03-p07.html?id=audit-private | 136 |
| m03-p07 | 返回日记列表 | route:m03-p06 | m03-p06 | http://127.0.0.1:8765/pages/m03-p06.html | 138 |
| m03-p07 | 编辑日记 | route:m03-p05 | m03-p05 | http://127.0.0.1:8765/pages/m03-p05.html?id=audit-private | 139 |
| m03-p08 | 返回日记列表 | route:m03-p06 | m03-p06 | http://127.0.0.1:8765/pages/m03-p06.html | 141 |
| m03-p08 | 编辑日记 | route:m03-p05 | m03-p05 | http://127.0.0.1:8765/pages/m03-p05.html?id=audit-diary | 142 |
| m03-p09 | 返回首页 | route:m03-p01 | m03-p01 | http://127.0.0.1:8765/pages/m03-p01.html | 147 |
| m03-p09 | 添加第一张照片 | route:m03-p11 | m03-p11 | http://127.0.0.1:8765/pages/m03-p11.html | 148 |
| m03-p09 | 从系统相册选择 | route:m03-p11 | m03-p11 | http://127.0.0.1:8765/pages/m03-p11.html | 149 |
| m03-p10 | 返回首页 | route:m03-p02 | m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 150 |
| m03-p10 | 共同照片 | route:m03-p12 | m03-p12 | http://127.0.0.1:8765/pages/m03-p12.html?id=audit-photo | 155 |
| m03-p10 | ＋ 添加照片 | route:m03-p11 | m03-p11 | http://127.0.0.1:8765/pages/m03-p11.html | 156 |
| m03-p11 | 返回相册 | route:m03-p09 | m03-p09 | http://127.0.0.1:8765/pages/m03-p09.html | 158 |
| m03-p11 | 完成 | photo-save | m03-p10 | http://127.0.0.1:8765/pages/m03-p10.html | 159 |
| m03-p11 | 保存照片 | photo-save | m03-p10 | http://127.0.0.1:8765/pages/m03-p10.html | 167 |
| m03-p12 | 返回照片相册 | route:m03-p10 | m03-p10 | http://127.0.0.1:8765/pages/m03-p10.html | 168 |
| m03-p12 | 编辑照片 | route:m03-p11 | m03-p11 | http://127.0.0.1:8765/pages/m03-p11.html?id=audit-photo | 169 |
| m04-p01 | 查看纪念日 | route:m04-p07 | m04-p07 | http://127.0.0.1:8765/pages/m04-p07.html | 174 |
| m04-p01 | 珍藏一个新时刻 | route:m04-p04 | m04-p04 | http://127.0.0.1:8765/pages/m04-p04.html | 175 |
| m04-p01 | 共同重要时刻 / 2026-10-04 | route:m04-p03 | m04-p03 | http://127.0.0.1:8765/pages/m04-p03.html?id=audit-moment | 177 |
| m04-p01 | 纪念日 | route:m04-p07 | m04-p07 | http://127.0.0.1:8765/pages/m04-p07.html | 178 |
| m04-p01 | 时光胶囊 | route:m04-p12 | m04-p12 | http://127.0.0.1:8765/pages/m04-p12.html | 179 |
| m04-p01 | 悄悄留言 | route:m04-p16 | m04-p16 | http://127.0.0.1:8765/pages/m04-p16.html | 180 |
| m04-p01 | 新建重要时刻 | route:m04-p04 | m04-p04 | http://127.0.0.1:8765/pages/m04-p04.html | 181 |
| m04-p01 | 共同提醒 | route:m04-p05 | m04-p05 | http://127.0.0.1:8765/pages/m04-p05.html | 183 |
| m04-p01 | 首页 | nav:m03-p02 | m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 184 |
| m04-p01 | 工坊 | nav:m05-p01 | m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 186 |
| m04-p01 | 宠物 | nav:pet | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 187 |
| m04-p01 | 我的 | nav:m06-p01 | m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 188 |
| m04-p02 | 从共同记录中收录 | collect-empty | m04-p04 | http://127.0.0.1:8765/pages/m04-p04.html?choose=1 | 189 |
| m04-p02 | 新建重要时刻 | route:m04-p04 | m04-p04 | http://127.0.0.1:8765/pages/m04-p04.html | 190 |
| m04-p02 | 纪念日 | route:m04-p08 | m04-p08 | http://127.0.0.1:8765/pages/m04-p08.html | 191 |
| m04-p02 | 时光胶囊 | route:m04-p12 | m04-p12 | http://127.0.0.1:8765/pages/m04-p12.html | 192 |
| m04-p02 | 悄悄留言 | route:m04-p17 | m04-p17 | http://127.0.0.1:8765/pages/m04-p17.html | 193 |
| m04-p02 | 共同提醒 | route:m04-p05 | m04-p06 | http://127.0.0.1:8765/pages/m04-p06.html | 194 |
| m04-p02 | 首页 | nav:m03-p01 | m03-p01 | http://127.0.0.1:8765/pages/m03-p01.html | 195 |
| m04-p02 | 工坊 | nav:m05-p01 | m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 197 |
| m04-p02 | 宠物 | nav:pet | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 198 |
| m04-p02 | 我的 | nav:m06-p01 | m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 199 |
| m04-p03 | 返回重要时刻 | route:m04-p01 | m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 200 |
| m04-p03 | 共同日记 | route:m03-p08 | m03-p08 | http://127.0.0.1:8765/pages/m03-p08.html?id=audit-diary | 201 |
| m04-p03 | 编辑时刻 | route:m04-p04 | m04-p04 | http://127.0.0.1:8765/pages/m04-p04.html?id=audit-moment | 203 |
| m04-p04 | 返回重要时刻 | route:m04-p02 | m04-p02 | http://127.0.0.1:8765/pages/m04-p02.html | 205 |
| m04-p04 | 保存到时刻册 | save | m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 215 |
| m04-p16 | 返回重要时刻 | route:m04-p01 | m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 216 |
| m04-p16 | 查看原记录 | read-reply | m04-p03 | http://127.0.0.1:8765/pages/m04-p03.html?id=audit-moment | 217 |
| m04-p17 | 返回重要时刻 | route:m04-p02 | m04-p02 | http://127.0.0.1:8765/pages/m04-p02.html | 218 |
| m04-p17 | 去看看共同记录 | route:m03-p06 | m03-p06 | http://127.0.0.1:8765/pages/m03-p06.html | 219 |
| m04-p05 | 返回重要时刻 | route:m04-p01 | m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 220 |
| m04-p05 | 今天约定就在今天 /  / 一起为 2026-10-05 留一段记录吧 | notice:time-today | m04-p11 | http://127.0.0.1:8765/pages/m04-p11.html?id=time-today | 221 |
| m04-p06 | 返回重要时刻 | route:m04-p01 | m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 222 |
| m04-p06 | 去看看重要时刻 | route:m04-p01 | m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 223 |
| m04-p07 | 返回重要时刻 | route:m04-p01 | m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 224 |
| m04-p07 | 添加纪念日 | route:m04-p09 | m04-p09 | http://127.0.0.1:8765/pages/m04-p09.html | 225 |
| m04-p07 | 2026-10-05 | route:m04-p11 | m04-p11 | http://127.0.0.1:8765/pages/m04-p11.html?id=time-today | 226 |
| m04-p07 | 今天约定 / 每年 2026-10-05 | route:m04-p11 | m04-p11 | http://127.0.0.1:8765/pages/m04-p11.html?id=time-today | 227 |
| m04-p07 | 未来约定 / 每年 2026-12-24 | route:m04-p10 | m04-p10 | http://127.0.0.1:8765/pages/m04-p10.html?id=time-future | 229 |
| m04-p07 | 添加纪念日 | route:m04-p09 | m04-p09 | http://127.0.0.1:8765/pages/m04-p09.html | 231 |
| m04-p08 | 返回重要时刻 | route:m04-p01 | m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 233 |
| m04-p08 | 添加第一个纪念日 | route:m04-p09 | m04-p09 | http://127.0.0.1:8765/pages/m04-p09.html | 234 |
| m04-p09 | 返回纪念日列表 | route:m04-p07 | m04-p07 | http://127.0.0.1:8765/pages/m04-p07.html | 235 |
| m04-p09 | 保存纪念日 | save-anniversary | m04-p07 | http://127.0.0.1:8765/pages/m04-p07.html | 241 |
| m04-p10 | 返回纪念日 | route:m04-p07 | m04-p07 | http://127.0.0.1:8765/pages/m04-p07.html | 242 |
| m04-p10 | 关联时刻 | route:m04-p03 | m04-p03 | http://127.0.0.1:8765/pages/m04-p03.html?id=time-moment | 243 |
| m04-p10 | 写下新的共同记录 | route:m03-p05 | m03-p05 | http://127.0.0.1:8765/pages/m03-p05.html?anniversary=time-future | 244 |
| m04-p10 | 编辑纪念日 | route:m04-p09 | m04-p09 | http://127.0.0.1:8765/pages/m04-p09.html?id=time-future | 245 |
| m04-p11 | 一起留下今天的记录 | route:m03-p05 | m03-p05 | http://127.0.0.1:8765/pages/m03-p05.html?anniversary=time-today | 247 |
| m04-p11 | 查看这个时刻 | route:m04-p03 | m04-p03 | http://127.0.0.1:8765/pages/m04-p03.html?id=time-moment | 248 |
| m04-p11 | 返回纪念日列表 | route:m04-p07 | m04-p07 | http://127.0.0.1:8765/pages/m04-p07.html | 249 |
| m04-p11 | 编辑纪念日 | route:m04-p09 | m04-p09 | http://127.0.0.1:8765/pages/m04-p09.html?id=time-today | 250 |
| m04-p12 | 返回重要时刻 | route:m04-p01 | m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 252 |
| m04-p12 | 新建时光胶囊 | route:m04-p13 | m04-p13 | http://127.0.0.1:8765/pages/m04-p13.html | 253 |
| m04-p12 | 封存的信 / 2026-10-06 · 还有 1 天 | route:m04-p15 | m04-p15 | http://127.0.0.1:8765/pages/m04-p15.html?id=time-sealed | 257 |
| m04-p12 | ＋ 新建时光胶囊 | route:m04-p13 | m04-p13 | http://127.0.0.1:8765/pages/m04-p13.html | 258 |
| m04-p13 | 返回胶囊列表 | route:m04-p12 | m04-p12 | http://127.0.0.1:8765/pages/m04-p12.html | 260 |
| m04-p13 | 暂存草稿 | save-draft | m04-p12 | http://127.0.0.1:8765/pages/m04-p12.html | 266 |
| m04-p13 | 封存这份心意 | save-sealed | m04-p15 | http://127.0.0.1:8765/pages/m04-p15.html?id=capsule-2e53ae69-a7e8-45b4-b6ac-322167494518 | 267 |
| m04-p14 | 返回胶囊列表 | route:m04-p12 | m04-p12 | http://127.0.0.1:8765/pages/m04-p12.html | 268 |
| m04-p14 | 把这一刻收录进重要时刻 | collect | m04-p03 | http://127.0.0.1:8765/pages/m04-p03.html?id=capsule-moment-time-opened | 269 |
| m04-p15 | 返回胶囊列表 | route:m04-p12 | m04-p12 | http://127.0.0.1:8765/pages/m04-p12.html | 271 |
| m05-p01 | 做成童话漫画 / 把回忆画成专属故事 / 留下一格格心动瞬间 | route:m05-p02 | m05-p02 | http://127.0.0.1:8765/pages/m05-p02.html | 274 |
| m05-p01 | 制作回忆影片 / 让重要时刻动起来 / 在光影里重温感动 | new-film | m05-p05 | http://127.0.0.1:8765/pages/m05-p05.html?id=work-e603023f-f70d-4c0a-96f0-49bc5f1d6b43 | 275 |
| m05-p01 | 查看全部 › | route:m05-p09 | m05-p09 | http://127.0.0.1:8765/pages/m05-p09.html | 276 |
| m05-p01 | work-free / 草稿 | work:work-free | m05-p03 | http://127.0.0.1:8765/pages/m05-p03.html?id=work-free | 277 |
| m05-p01 | work-photos / 草稿 | work:work-photos | m05-p04 | http://127.0.0.1:8765/pages/m05-p04.html?id=work-photos | 278 |
| m05-p01 | 开始一次创作 | route:m05-p02 | m05-p02 | http://127.0.0.1:8765/pages/m05-p02.html | 279 |
| m05-p01 | 首页 | nav:m03-p02 | m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 280 |
| m05-p01 | 重要时刻 | nav:m04-p01 | m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 281 |
| m05-p01 | 宠物 | nav:m07-p04 | m07-p04 | http://127.0.0.1:8765/pages/m07-p04.html | 283 |
| m05-p01 | 我的 | nav:m06-p01 | m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 284 |
| m05-p02 | 返回童话工坊 | route:m05-p01 | m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 285 |
| m05-p03 | 返回素材选择 | route:m05-p02 | m05-p02 | http://127.0.0.1:8765/pages/m05-p02.html | 291 |
| m05-p03 | 默默 & 小满 / 可爱自然 · 清新温柔 | characters | m05-p10 | http://127.0.0.1:8765/pages/m05-p10.html?work=work-free | 299 |
| m05-p03 | 生成童话漫画 | generate | m05-p06 | http://127.0.0.1:8765/pages/m05-p06.html?id=work-free | 300 |
| m05-p03 | 暂存创作草稿 | draft | m05-p09 | http://127.0.0.1:8765/pages/m05-p09.html | 301 |
| m05-p04 | 返回素材选择 | route:m05-p02 | m05-p02 | http://127.0.0.1:8765/pages/m05-p02.html | 303 |
| m05-p04 | 他  / 阳光温柔 | characters | m05-p10 | http://127.0.0.1:8765/pages/m05-p10.html?work=work-photos | 310 |
| m05-p04 | 她  / 温柔爱笑 | characters | m05-p10 | http://127.0.0.1:8765/pages/m05-p10.html?work=work-photos | 311 |
| m05-p04 | 生成童话漫画 | generate | m05-p06 | http://127.0.0.1:8765/pages/m05-p06.html?id=work-photos | 312 |
| m05-p04 | 暂存创作草稿 | draft | m05-p09 | http://127.0.0.1:8765/pages/m05-p09.html | 313 |
| m05-p05 | 返回工坊 | route:m05-p01 | m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 316 |
| m05-p05 | 生成回忆影片 | generate | m05-p06 | http://127.0.0.1:8765/pages/m05-p06.html?id=work-film | 324 |
| m05-p05 | 暂存创作草稿 | draft | m05-p09 | http://127.0.0.1:8765/pages/m05-p09.html | 325 |
| m05-p06 | 返回童话工坊 | route:m05-p01 | m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 327 |
| m05-p07 | 调整内容 | route:m05-p03 | m05-p03 | http://127.0.0.1:8765/pages/m05-p03.html?id=work-failed | 329 |
| m05-p07 | 重新生成 | generate | m05-p06 | http://127.0.0.1:8765/pages/m05-p06.html?id=work-failed | 330 |
| m05-p07 | 先回到童话工坊 ♡ | route:m05-p01 | m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 331 |
| m05-p08 | 返回我的创作 | route:m05-p09 | m05-p09 | http://127.0.0.1:8765/pages/m05-p09.html | 332 |
| m05-p08 | 重新生成 | route:m05-p05 | m05-p05 | http://127.0.0.1:8765/pages/m05-p05.html?id=work-ready | 343 |
| m05-p09 | 开始创作 | route:m05-p02 | m05-p02 | http://127.0.0.1:8765/pages/m05-p02.html | 351 |
| m05-p09 | work-free / 漫画 · 草稿 | work:work-free | m05-p03 | http://127.0.0.1:8765/pages/m05-p03.html?id=work-free | 352 |
| m05-p09 | work-photos / 漫画 · 草稿 | work:work-photos | m05-p04 | http://127.0.0.1:8765/pages/m05-p04.html?id=work-photos | 353 |
| m05-p09 | work-film / 影片 · 草稿 | work:work-film | m05-p05 | http://127.0.0.1:8765/pages/m05-p05.html?id=work-film | 354 |
| m05-p09 | work-running / 漫画 · 制作中 | work:work-running | m05-p06 | http://127.0.0.1:8765/pages/m05-p06.html?id=work-running | 355 |
| m05-p09 | work-failed / 漫画 · 生成失败 | work:work-failed | m05-p07 | http://127.0.0.1:8765/pages/m05-p07.html?id=work-failed | 356 |
| m05-p09 | work-ready / 影片 · 已完成 | work:work-ready | m05-p08 | http://127.0.0.1:8765/pages/m05-p08.html?id=work-ready | 357 |
| m05-p09 | 返回童话工坊 | route:m05-p01 | m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 358 |
| m05-p10 | 返回当前创作 | route:m05-p03 | m05-p03 | http://127.0.0.1:8765/pages/m05-p03.html?id=work-free | 360 |
| m05-p10 | 更新我们的主角 | save-characters | m05-p03 | http://127.0.0.1:8765/pages/m05-p03.html?id=work-free | 365 |
| m06-p01 | 小满 ♡ / 已与阿舟关联 ♡ | route:m06-p02 | m06-p02 | http://127.0.0.1:8765/pages/m06-p02.html | 366 |
| m06-p01 | 我们的小世界 / 一起管理共同资料 | route:m06-p03 | m06-p03 | http://127.0.0.1:8765/pages/m06-p03.html | 367 |
| m06-p01 | 草稿箱 | route:m06-p04 | m06-p04 | http://127.0.0.1:8765/pages/m06-p04.html | 368 |
| m06-p01 | 标签管理 | route:m06-p05 | m06-p05 | http://127.0.0.1:8765/pages/m06-p05.html | 369 |
| m06-p01 | 童话会员 | route:m06-p06 | m06-p06 | http://127.0.0.1:8765/pages/m06-p06.html | 370 |
| m06-p01 | 设置 | route:m06-p07 | m06-p07 | http://127.0.0.1:8765/pages/m06-p07.html | 371 |
| m06-p01 | 帮助与关于 | route:m06-p12 | m06-p12 | http://127.0.0.1:8765/pages/m06-p12.html | 372 |
| m06-p01 | 首页 | route:m03-p02 | m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 373 |
| m06-p01 | 重要时刻 | route:m04-p01 | m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 374 |
| m06-p01 | 工坊 | route:m05-p01 | m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 375 |
| m06-p01 | 宠物 | route:m07-p04 | m07-p04 | http://127.0.0.1:8765/pages/m07-p04.html | 376 |
| m06-p02 | 返回我的与设置 | route:m06-p01 | m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 378 |
| m06-p02 | 保存资料 | profile-save | m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 385 |
| m06-p03 | 返回我的与设置 | route:m06-p01 | m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 386 |
| m06-p03 | 共同空间设置 / 哪些记录邀请对方一起看 | route:m06-p09 | m06-p09 | http://127.0.0.1:8765/pages/m06-p09.html | 389 |
| m06-p04 | 返回我的与设置 | route:m06-p01 | m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 392 |
| m06-p04 | 日记草稿 / 日记 · 继续编辑 | draft:m03-p05:audit-diary | m03-p05 | http://127.0.0.1:8765/pages/m03-p05.html?id=audit-diary | 393 |
| m06-p04 | 工坊草稿 / 工坊 · 继续编辑 | draft:m05-p03:audit-work | m05-p03 | http://127.0.0.1:8765/pages/m05-p03.html?id=audit-work | 394 |
| m06-p04 | 胶囊草稿 / 胶囊 · 继续编辑 | draft:m04-p13:settings-capsule | m04-p13 | http://127.0.0.1:8765/pages/m04-p13.html?id=settings-capsule | 395 |
| m06-p04 | 回忆册草稿 / 回忆册 · 继续编辑 | draft:m08-p04:book-state | m08-p04 | http://127.0.0.1:8765/pages/m08-p04.html?id=book-state | 396 |
| m06-p05 | 返回我的与设置 | route:m06-p01 | m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 398 |
| m06-p06 | 返回我的与设置 | route:m06-p01 | m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 404 |
| m06-p07 | 返回我的与设置 | route:m06-p01 | m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 407 |
| m06-p07 | 账号与安全 | route:m06-p08 | m06-p08 | http://127.0.0.1:8765/pages/m06-p08.html | 408 |
| m06-p07 | 隐私与共同可见 | route:m06-p09 | m06-p09 | http://127.0.0.1:8765/pages/m06-p09.html | 409 |
| m06-p07 | 通知设置 | route:m06-p10 | m06-p10 | http://127.0.0.1:8765/pages/m06-p10.html | 410 |
| m06-p07 | 数据与存储 | route:m06-p11 | m06-p11 | http://127.0.0.1:8765/pages/m06-p11.html | 411 |
| m06-p08 | 返回设置 | route:m06-p07 | m06-p07 | http://127.0.0.1:8765/pages/m06-p07.html | 415 |
| m06-p08 | 修改密码 | route:m01-p04 | m01-p04 | http://127.0.0.1:8765/pages/m01-p04.html | 416 |
| m06-p09 | 返回设置 | route:m06-p07 | m06-p07 | http://127.0.0.1:8765/pages/m06-p07.html | 422 |
| m06-p10 | 返回设置 | route:m06-p07 | m06-p07 | http://127.0.0.1:8765/pages/m06-p07.html | 428 |
| m06-p11 | 返回设置 | route:m06-p07 | m06-p07 | http://127.0.0.1:8765/pages/m06-p07.html | 434 |
| m06-p12 | 返回我的与设置 | route:m06-p01 | m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 440 |
| m07-p01 | 暂时返回 | route:m03-p02 | m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 448 |
| m07-p01 | 返回 | route:m03-p02 | m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 449 |
| m07-p01 | 首页 | route:m03-p02 | m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 450 |
| m07-p01 | 重要时刻 | route:m04-p01 | m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 451 |
| m07-p01 | 工坊 | route:m05-p01 | m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 452 |
| m07-p01 | 我的 | route:m06-p01 | m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 454 |
| m07-p02 | 邀请 TA 一起领养 | adopt | m07-p01 | http://127.0.0.1:8765/pages/m07-p01.html | 460 |
| m07-p02 | 返回 | route:m07-p04 | m07-p04 | http://127.0.0.1:8765/pages/m07-p04.html | 461 |
| m07-p03 | 互动 | route:m07-p06 | m07-p06 | http://127.0.0.1:8765/pages/m07-p06.html | 462 |
| m07-p03 | 喂食 | route:m07-p08 | m07-p08 | http://127.0.0.1:8765/pages/m07-p08.html | 463 |
| m07-p03 | 任务 | route:m07-p11 | m07-p11 | http://127.0.0.1:8765/pages/m07-p11.html | 464 |
| m07-p03 | 装扮 | route:m07-p12 | m07-p12 | http://127.0.0.1:8765/pages/m07-p12.html | 465 |
| m07-p03 | 布置小屋 | route:m07-p15 | m07-p15 | http://127.0.0.1:8765/pages/m07-p15.html | 466 |
| m07-p03 | 成长故事 | route:m07-p18 | m07-p18 | http://127.0.0.1:8765/pages/m07-p18.html | 467 |
| m07-p03 | 成就图鉴 | route:m07-p21 | m07-p21 | http://127.0.0.1:8765/pages/m07-p21.html | 468 |
| m07-p03 | 去任务 › | route:m07-p11 | m07-p11 | http://127.0.0.1:8765/pages/m07-p11.html | 469 |
| m07-p03 | 返回 | route:m03-p02 | m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 470 |
| m07-p03 | 宠物设置 | route:m07-p25 | m07-p25 | http://127.0.0.1:8765/pages/m07-p25.html | 471 |
| m07-p03 | 首页 | route:m03-p02 | m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 472 |
| m07-p03 | 重要时刻 | route:m04-p01 | m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 473 |
| m07-p03 | 工坊 | route:m05-p01 | m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 474 |
| m07-p03 | 我的 | route:m06-p01 | m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 476 |
| m07-p04 | 一起领养 | route:m07-p02 | m07-p02 | http://127.0.0.1:8765/pages/m07-p02.html | 479 |
| m07-p04 | 返回 | route:m03-p02 | m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 481 |
| m07-p04 | 首页 | route:m03-p02 | m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 482 |
| m07-p04 | 重要时刻 | route:m04-p01 | m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 483 |
| m07-p04 | 工坊 | route:m05-p01 | m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 484 |
| m07-p04 | 我的 | route:m06-p01 | m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 486 |
| m07-p05 | 再玩一次 | route:m07-p06 | m07-p06 | http://127.0.0.1:8765/pages/m07-p06.html | 487 |
| m07-p05 | 回到小屋 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 488 |
| m07-p05 | 返回 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 489 |
| m07-p06 | 和团团互动 | play | m07-p05 | http://127.0.0.1:8765/pages/m07-p05.html?id=e0bcf2cc-04ae-44fe-857d-9a27c11c0890 | 494 |
| m07-p06 | 返回 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 495 |
| m07-p07 | 宠物空间 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 496 |
| m07-p07 | 成长日记 | route:m07-p18 | m07-p18 | http://127.0.0.1:8765/pages/m07-p18.html | 497 |
| m07-p07 | 去喂食补充精力 › | route:m07-p08 | m07-p08 | http://127.0.0.1:8765/pages/m07-p08.html | 498 |
| m07-p08 | 去获得更多食物 › | route:m07-p11 | m07-p11 | http://127.0.0.1:8765/pages/m07-p11.html | 503 |
| m07-p08 | 返回 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 504 |
| m07-p09 | 返回 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 505 |
| m07-p09 | 去做任务 | route:m07-p11 | m07-p11 | http://127.0.0.1:8765/pages/m07-p11.html | 506 |
| m07-p10 | 返回任务 | route:m07-p11 | m07-p11 | http://127.0.0.1:8765/pages/m07-p11.html | 507 |
| m07-p10 | 返回 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 508 |
| m07-p11 | 返回小屋 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 511 |
| m07-p11 | 返回 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 512 |
| m07-p11 | 陪宠物互动 | route:m07-p06 | m07-p06 | http://127.0.0.1:8765/pages/m07-p06.html | 514 |
| m07-p11 | 给宠物喂食 | route:m07-p08 | m07-p08 | http://127.0.0.1:8765/pages/m07-p08.html | 515 |
| m07-p11 | 整理宠物小屋 | route:m07-p15 | m07-p15 | http://127.0.0.1:8765/pages/m07-p15.html | 516 |
| m07-p12 | 返回宠物小屋 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 518 |
| m07-p13 | 宠物空间 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 529 |
| m07-p13 | 去做任务 | route:m07-p11 | m07-p11 | http://127.0.0.1:8765/pages/m07-p11.html | 530 |
| m07-p14 | 继续布置 | route:m07-p15 | m07-p15 | http://127.0.0.1:8765/pages/m07-p15.html | 531 |
| m07-p14 | 回到小屋 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 532 |
| m07-p14 | 返回 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 533 |
| m07-p15 | 野餐垫 照顾7个不同日期 | catalog:picnic-rug | m07-p16 | http://127.0.0.1:8765/pages/m07-p16.html?item=picnic-rug | 541 |
| m07-p15 | 保存小屋布置 | room-save | m07-p14 | http://127.0.0.1:8765/pages/m07-p14.html?id=c65237f1-5ada-4dd5-84cb-7f5eb22feaea | 542 |
| m07-p15 | 返回 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 543 |
| m07-p16 | 返回 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 544 |
| m07-p16 | 去做任务 | route:m07-p11 | m07-p11 | http://127.0.0.1:8765/pages/m07-p11.html | 545 |
| m07-p17 | 返回成长时间线 | route:m07-p18 | m07-p18 | http://127.0.0.1:8765/pages/m07-p18.html | 546 |
| m07-p17 | 返回成长时间线 | route:m07-p18 | m07-p18 | http://127.0.0.1:8765/pages/m07-p18.html | 547 |
| m07-p18 | 返回 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 549 |
| m07-p18 | 2026-10-05 · 小满 / 共同成长故事 | route:m07-p19:id=pet-story | m07-p19 | http://127.0.0.1:8765/pages/m07-p19.html?id=pet-story | 550 |
| m07-p19 | 返回 | route:m07-p18 | m07-p18 | http://127.0.0.1:8765/pages/m07-p18.html | 553 |
| m07-p20 | 返回 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 555 |
| m07-p21 | 第一次见面 可领取奖励 | route:m07-p20:achievement=meet | m07-p20 | http://127.0.0.1:8765/pages/m07-p20.html?achievement=meet | 557 |
| m07-p21 | 玩到天黑 0 / 10 | route:m07-p20:achievement=play10 | m07-p20 | http://127.0.0.1:8765/pages/m07-p20.html?achievement=play10 | 558 |
| m07-p21 | 默契喂食 0 / 20 | route:m07-p20:achievement=feed20 | m07-p20 | http://127.0.0.1:8765/pages/m07-p20.html?achievement=feed20 | 559 |
| m07-p21 | 小屋变新了 0 / 1 | route:m07-p20:achievement=room | m07-p20 | http://127.0.0.1:8765/pages/m07-p20.html?achievement=room | 560 |
| m07-p21 | 照顾7天 1 / 7 | route:m07-p20:achievement=care7 | m07-p20 | http://127.0.0.1:8765/pages/m07-p20.html?achievement=care7 | 561 |
| m07-p21 | 亲密搭档 可领取奖励 | route:m07-p20:achievement=affinity | m07-p20 | http://127.0.0.1:8765/pages/m07-p20.html?achievement=affinity | 562 |
| m07-p21 | 陪伴30天 可领取奖励 | route:m07-p20:achievement=days30 | m07-p20 | http://127.0.0.1:8765/pages/m07-p20.html?achievement=days30 | 563 |
| m07-p21 | 去完成今天的照顾 | route:m07-p11 | m07-p11 | http://127.0.0.1:8765/pages/m07-p11.html | 564 |
| m07-p21 | 返回 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 565 |
| m07-p21 | 收藏图鉴 | route:m07-p22 | m07-p22 | http://127.0.0.1:8765/pages/m07-p22.html | 566 |
| m07-p22 | 小花围巾 已拥有 | catalog:scarf | m07-p23 | http://127.0.0.1:8765/pages/m07-p23.html?item=scarf | 570 |
| m07-p22 | 格纹蝴蝶结 金币20 | catalog:bow | m07-p23 | http://127.0.0.1:8765/pages/m07-p23.html?item=bow | 571 |
| m07-p22 | 星星领结 亲密度160 | catalog:star-bow | m07-p23 | http://127.0.0.1:8765/pages/m07-p23.html?item=star-bow | 572 |
| m07-p22 | 蜜桃帽子 记录一页成长故事 | catalog:peach-hat | m07-p23 | http://127.0.0.1:8765/pages/m07-p23.html?item=peach-hat | 573 |
| m07-p22 | 星光皇冠 星星30 | catalog:crown | m07-p23 | http://127.0.0.1:8765/pages/m07-p23.html?item=crown | 574 |
| m07-p22 | 雨天小斗篷 照顾7个不同日期 | catalog:cape | m07-p23 | http://127.0.0.1:8765/pages/m07-p23.html?item=cape | 575 |
| m07-p22 | 暖暖小马甲 金币20 | catalog:vest | m07-p23 | http://127.0.0.1:8765/pages/m07-p23.html?item=vest | 576 |
| m07-p22 | 晚安铃铛 喂食20次 | catalog:bell | m07-p23 | http://127.0.0.1:8765/pages/m07-p23.html?item=bell | 577 |
| m07-p22 | 返回 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 578 |
| m07-p23 | 返回图鉴 | route:m07-p22 | m07-p22 | http://127.0.0.1:8765/pages/m07-p22.html | 580 |
| m07-p23 | 去换上 | equip | m07-p12 | http://127.0.0.1:8765/pages/m07-p12.html | 581 |
| m07-p23 | 返回图鉴 | route:m07-p22 | m07-p22 | http://127.0.0.1:8765/pages/m07-p22.html | 582 |
| m07-p24 | 我再想想，返回 | route:m07-p25 | m07-p25 | http://127.0.0.1:8765/pages/m07-p25.html | 585 |
| m07-p24 | 返回 | route:m07-p25 | m07-p25 | http://127.0.0.1:8765/pages/m07-p25.html | 586 |
| m07-p25 | 返回宠物空间 | route:m07-p03 | m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 587 |
| m07-p25 | 暂时解除共同照顾 | route:m07-p24 | m07-p24 | http://127.0.0.1:8765/pages/m07-p24.html | 596 |
| m08-p01 | 返回首页 | route:m03-p02 | m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 598 |
| m08-p01 | 从封面打开《共同测试册》 | read-route:m08-p16?id=book-state&page=page-state | m08-p16 | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-state&offset=0&block=0 | 601 |
| m08-p01 | 封面 | route:m08-p05?id=book-state&origin=manage | m08-p05 | http://127.0.0.1:8765/pages/m08-p05.html?id=book-state&origin=manage | 602 |
| m08-p01 | 整理 | route:m08-p13 | m08-p13 | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 603 |
| m08-p01 | 开始翻阅 → | read-route:m08-p16?id=book-state&page=page-state | m08-p16 | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-state&offset=0&block=0 | 604 |
| m08-p01 | ＋ 新建回忆册 | route:m08-p04 | m08-p04 | http://127.0.0.1:8765/pages/m08-p04.html | 605 |
| m08-p01 | 本月推荐 | route:m08-p03 | m08-p03 | http://127.0.0.1:8765/pages/m08-p03.html | 606 |
| m08-p02 | 返回 | route:m03-p02 | m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 608 |
| m08-p02 | 新建第一本回忆册 | route:m08-p04 | m08-p04 | http://127.0.0.1:8765/pages/m08-p04.html | 609 |
| m08-p03 | 返回 | route:m08-p01 | m08-p01 | http://127.0.0.1:8765/pages/m08-p01.html | 610 |
| m08-p03 | 共同日记 · 2026-10-04 | route:m03-p08?id=audit-diary | m03-p08 | http://127.0.0.1:8765/pages/m03-p08.html?id=audit-diary | 611 |
| m08-p03 | 共同照片 · 2026-10-04 | route:m03-p12?id=audit-photo | m03-p12 | http://127.0.0.1:8765/pages/m03-p12.html?id=audit-photo | 612 |
| m08-p03 | 共同重要时刻 · 2026-10-04 | route:m04-p03?id=audit-moment | m04-p03 | http://127.0.0.1:8765/pages/m04-p03.html?id=audit-moment | 613 |
| m08-p03 | 实际工坊作品 · 2026-10-05 | route:m05-p08?id=audit-work | m05-p08 | http://127.0.0.1:8765/pages/m05-p08.html?id=audit-work | 614 |
| m08-p03 | 实际成长故事 · 2026-10-04 | route:m07-p19?id=audit-story | m07-p19 | http://127.0.0.1:8765/pages/m07-p19.html?id=audit-story | 615 |
| m08-p03 | 开始制作 | route:m08-p04 | m08-p04 | http://127.0.0.1:8765/pages/m08-p04.html?recommend=1 | 616 |
| m08-p03 | 返回书架 | route:m08-p01 | m08-p01 | http://127.0.0.1:8765/pages/m08-p01.html | 617 |
| m08-p04 | 返回 | route:m08-p01 | m08-p01 | http://127.0.0.1:8765/pages/m08-p01.html | 618 |
| m08-p04 | 下一步 · 设计封面 | create | m08-p05 | http://127.0.0.1:8765/pages/m08-p05.html?id=book-f0fb7187-9f2d-4cf7-8928-6c08e4444646 | 624 |
| m08-p05 | 返回 | route:m08-p04 | m08-p04 | http://127.0.0.1:8765/pages/m08-p04.html?id=book-state | 625 |
| m08-p05 | 保存封面 · 继续 | theme-save | m08-p06 | http://127.0.0.1:8765/pages/m08-p06.html?id=book-state | 630 |
| m08-p06 | 返回 | route:m08-p05 | m08-p05 | http://127.0.0.1:8765/pages/m08-p05.html?id=book-state | 631 |
| m08-p06 | 下一步 · 编排回忆 | select-save | m08-p07 | http://127.0.0.1:8765/pages/m08-p07.html?id=book-state | 643 |
| m08-p07 | 返回 | route:m08-p06 | m08-p06 | http://127.0.0.1:8765/pages/m08-p06.html?id=book-state | 644 |
| m08-p07 | 放进回忆册 | route:m08-p08 | m08-p08 | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state&source=audit-diary&kind=diary | 645 |
| m08-p07 | 暂不放入 | skip | m08-p13 | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 646 |
| m08-p07 | 重新选择素材 | route:m08-p06 | m08-p06 | http://127.0.0.1:8765/pages/m08-p06.html?id=book-state | 647 |
| m08-p08 | 返回 | route:m08-p07 | m08-p07 | http://127.0.0.1:8765/pages/m08-p07.html?id=book-state | 648 |
| m08-p08 | 使用这个版式 | route:m08-p09 | m08-p09 | http://127.0.0.1:8765/pages/m08-p09.html?id=book-state&source=audit-diary&kind=diary&template=%E6%97%A5%E8%AE%B0%E6%91%98%E5%BD%95&page=&draft= | 655 |
| m08-p09 | 返回 | route:m08-p08 | m08-p08 | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state | 656 |
| m08-p09 | 更换版式 | stash | m08-p08 | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state&draft=15c21cef-1e5e-43bb-b6c2-c2421dd4975c&page=page-state&source=audit-diary&kind=diary | 663 |
| m08-p09 | 保存这一页 | page-save | m08-p13 | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 664 |
| m08-p10 | 返回 | route:m08-p08 | m08-p08 | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state | 665 |
| m08-p10 | 保留草稿换模板 | stash | m08-p08 | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state&draft=661d1798-e3ae-441b-9ae5-bdf2d97b0179&page=page-state&source=audit-photo&kind=photo | 675 |
| m08-p10 | 保存这一页 | page-save | m08-p13 | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 677 |
| m08-p11 | 返回 | route:m08-p08 | m08-p08 | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state | 678 |
| m08-p11 | 保存这一页 | page-save | m08-p13 | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 684 |
| m08-p11 | 保留草稿换模板 | stash | m08-p08 | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state&draft=8a11f397-a8cb-4e80-aeec-8750e5c7ea1b&page=page-state&source=audit-moment&kind=moment | 685 |
| m08-p12 | 返回 | route:m08-p08 | m08-p08 | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state | 686 |
| m08-p12 | 保存这一页 | page-save | m08-p13 | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 693 |
| m08-p12 | 保留草稿换模板 | stash | m08-p08 | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state&draft=59d533e8-4609-4f79-bc16-6b0044eeb5df&page=page-state&source=audit-pet%3Aaudit-story&kind=pet | 694 |
| m08-p13 | 返回 | route:m08-p06 | m08-p06 | http://127.0.0.1:8765/pages/m08-p06.html?id=book-state | 695 |
| m08-p13 | 保存排列 | structure-save | m08-p14 | http://127.0.0.1:8765/pages/m08-p14.html?id=book-state | 696 |
| m08-p13 | 共同日记 | route:m08-p09?id=book-state&page=page-state | m08-p09 | http://127.0.0.1:8765/pages/m08-p09.html?id=book-state&page=page-state | 698 |
| m08-p13 | 共同照片 | route:m08-p10?id=book-state&page=page-second | m08-p10 | http://127.0.0.1:8765/pages/m08-p10.html?id=book-state&page=page-second | 700 |
| m08-p13 | 共同重要时刻 | route:m08-p11?id=book-state&page=page-third | m08-p11 | http://127.0.0.1:8765/pages/m08-p11.html?id=book-state&page=page-third | 703 |
| m08-p13 | ＋ 添加回忆 | route:m08-p08 | m08-p08 | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state | 705 |
| m08-p14 | 返回 | route:m08-p01 | m08-p01 | http://127.0.0.1:8765/pages/m08-p01.html?id=book-state | 707 |
| m08-p14 | 开始翻阅 | route:m08-p15 | m08-p15 | http://127.0.0.1:8765/pages/m08-p15.html?id=book-state | 708 |
| m08-p14 | 继续整理 | route:m08-p13 | m08-p13 | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 709 |
| m08-p15 | 返回 | route:m08-p01 | m08-p01 | http://127.0.0.1:8765/pages/m08-p01.html | 710 |
| m08-p15 | 管理这本回忆册 | route:m08-p21 | m08-p21 | http://127.0.0.1:8765/pages/m08-p21.html?id=book-state | 711 |
| m08-p15 | 共同日记 | read-route:m08-p16?id=book-state&page=page-state | m08-p16 | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-state&offset=0&block=0 | 712 |
| m08-p15 | 共同照片 | read-route:m08-p16?id=book-state&page=page-second | m08-p16 | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-second&offset=0&block=0 | 713 |
| m08-p15 | 共同重要时刻 | read-route:m08-p16?id=book-state&page=page-third | m08-p16 | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-third&offset=0&block=0 | 714 |
| m08-p15 | 从第一页翻阅 | read-route:m08-p16?id=book-state&page=page-state | m08-p16 | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-state&offset=0&block=0 | 715 |
| m08-p16 | ‹ 书架 | route:m08-p01 | m08-p01 | http://127.0.0.1:8765/pages/m08-p01.html | 716 |
| m08-p16 | 查看原始共同记录 | route:m03-p12?id=audit-photo | m03-p12 | http://127.0.0.1:8765/pages/m03-p12.html?id=audit-photo | 719 |
| m08-p16 | ＋ 留一张补页 | route:m08-p18?id=book-state&page=page-second | m08-p18 | http://127.0.0.1:8765/pages/m08-p18.html?id=book-state&page=page-second | 725 |
| m08-p17 | 返回 | read-route:m08-p16 | m08-p16 | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-second&offset=0&block=0 | 726 |
| m08-p17 | 全书目录 | route:m08-p15 | m08-p15 | http://127.0.0.1:8765/pages/m08-p15.html?id=book-state | 727 |
| m08-p17 | 添加补页 | route:m08-p18 | m08-p18 | http://127.0.0.1:8765/pages/m08-p18.html?id=book-state&page=page-second | 729 |
| m08-p17 | 整理书页 | route:m08-p13 | m08-p13 | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 730 |
| m08-p17 | 管理这本书 · 书名、归档、导出与删除 | route:m08-p21 | m08-p21 | http://127.0.0.1:8765/pages/m08-p21.html?id=book-state | 731 |
| m08-p18 | 返回 | read-route:m08-p16 | m08-p16 | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-second&offset=0&block=0 | 732 |
| m08-p18 | 查看目录 | route:m08-p15 | m08-p15 | http://127.0.0.1:8765/pages/m08-p15.html?id=book-state | 733 |
| m08-p18 | 下一步 · 写补页 | route:m08-p19?id=book-state&page=page-second&kind=写几句话 | m08-p19 | http://127.0.0.1:8765/pages/m08-p19.html?id=book-state&page=page-second&kind=%E5%86%99%E5%87%A0%E5%8F%A5%E8%AF%9D | 737 |
| m08-p19 | 返回 | route:m08-p18 | m08-p18 | http://127.0.0.1:8765/pages/m08-p18.html?id=book-state&page=page-second | 738 |
| m08-p19 | 放入回忆书 | supplement | m08-p20 | http://127.0.0.1:8765/pages/m08-p20.html?id=book-state&page=page-second | 745 |
| m08-p21 | 返回 | route:m08-p15 | m08-p15 | http://127.0.0.1:8765/pages/m08-p15.html?id=book-state | 746 |
| m08-p21 | 整理页序 | route:m08-p13 | m08-p13 | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 748 |
| m08-p21 | 修改主题与封面 | route:m08-p05?id=book-state&origin=manage | m08-p05 | http://127.0.0.1:8765/pages/m08-p05.html?id=book-state&origin=manage | 749 |

同文档操作、弹层、输入及无跨页动作均保留在逐控件合同中，不虚构为页面跳转。当前初态没有入边不等于死路；需结合条件／隐藏流程验证。历史导航正文保存在`evidence/history/pre-current-initial-catalog-8cce41c/CURRENT_NAVIGATION.md`。
