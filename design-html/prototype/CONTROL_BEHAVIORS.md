# 当前控件行为与执行清单

本轮114页初态观察与754项控件结果均对应当前源码；实际导航393条。每次操作使用独立本地模拟数据。逐项结果：[evidence/current/initial-controls-20261031-accessible/results.json](evidence/current/initial-controls-20261031-accessible/results.json)；机器可读合同：[evidence/current/initial-controls-20261031-accessible/contracts.json](evidence/current/initial-controls-20261031-accessible/contracts.json)。

这里只证明声明初态的可用控件，不替代隐藏／条件分支、全部错误／返回／长输入、连续流程、原稿视觉及原41项完整验收。旧全量JSON与原图保留历史版本，不将旧报告重绑为新源码。

| 页面 | 控件 | 明确行为合同 | 实际URL | 结果行 |
| --- | --- | --- | --- | --- |
| m01-p01 | 登录并开始 | route:m01-p02 | http://127.0.0.1:8765/pages/m01-p02.html | 0 |
| m01-p01 | 创建账号 | route:m01-p03 | http://127.0.0.1:8765/pages/m01-p03.html | 1 |
| m01-p02 | 返回 | route:m01-p01 | http://127.0.0.1:8765/pages/m01-p01.html | 2 |
| m01-p02 | 手机号 | input:native | http://127.0.0.1:8765/pages/m01-p02.html | 3 |
| m01-p02 | 密码 | input:native | http://127.0.0.1:8765/pages/m01-p02.html | 4 |
| m01-p02 | 显示密码 | eye:password | http://127.0.0.1:8765/pages/m01-p02.html | 5 |
| m01-p02 | 忘记密码？ | route:m01-p04 | http://127.0.0.1:8765/pages/m01-p04.html | 6 |
| m01-p02 | 登录并回到故事里 | login:m02-p01 | http://127.0.0.1:8765/pages/m02-p01.html | 7 |
| m01-p02 | 创建账号 | route:m01-p03 | http://127.0.0.1:8765/pages/m01-p03.html | 8 |
| m01-p02 | 《用户协议》 | modal:《用户协议》 | http://127.0.0.1:8765/pages/m01-p02.html | 9 |
| m01-p02 | 《隐私政策》 | modal:《隐私政策》 | http://127.0.0.1:8765/pages/m01-p02.html | 10 |
| m01-p03 | 返回欢迎页 | route:m01-p01 | http://127.0.0.1:8765/pages/m01-p01.html | 11 |
| m01-p03 | 昵称 | input:native | http://127.0.0.1:8765/pages/m01-p03.html | 12 |
| m01-p03 | 手机号 | input:native | http://127.0.0.1:8765/pages/m01-p03.html | 13 |
| m01-p03 | 验证码 | input:native | http://127.0.0.1:8765/pages/m01-p03.html | 14 |
| m01-p03 | 获取验证码 | send:register | http://127.0.0.1:8765/pages/m01-p03.html | 15 |
| m01-p03 | 登录密码 | input:native | http://127.0.0.1:8765/pages/m01-p03.html | 16 |
| m01-p03 | 显示密码 | eye:password | http://127.0.0.1:8765/pages/m01-p03.html | 17 |
| m01-p03 | INPUT | input:native | http://127.0.0.1:8765/pages/m01-p03.html | 18 |
| m01-p03 | 《用户协议》 | modal:《用户协议》 | http://127.0.0.1:8765/pages/m01-p03.html | 19 |
| m01-p03 | 《隐私政策》 | modal:《隐私政策》 | http://127.0.0.1:8765/pages/m01-p03.html | 20 |
| m01-p03 | 创建账号 | register:m01-p07 | http://127.0.0.1:8765/pages/m01-p07.html | 21 |
| m01-p03 | 去登录 | route:m01-p02 | http://127.0.0.1:8765/pages/m01-p02.html | 22 |
| m01-p04 | 返回 | route:m01-p02 | http://127.0.0.1:8765/pages/m01-p02.html | 23 |
| m01-p04 | 手机号 | input:native | http://127.0.0.1:8765/pages/m01-p04.html | 24 |
| m01-p04 | 验证码 | input:native | http://127.0.0.1:8765/pages/m01-p04.html | 25 |
| m01-p04 | 获取验证码 | send:recovery | http://127.0.0.1:8765/pages/m01-p04.html | 26 |
| m01-p04 | 下一步 | recovery:m01-p07 | http://127.0.0.1:8765/pages/m01-p07.html | 27 |
| m01-p04 | 返回登录 | route:m01-p02 | http://127.0.0.1:8765/pages/m01-p02.html | 28 |
| m01-p05 | 返回找回密码 | route:m01-p04 | http://127.0.0.1:8765/pages/m01-p04.html | 29 |
| m01-p05 | 输入新密码 | input:native | http://127.0.0.1:8765/pages/m01-p05.html | 30 |
| m01-p05 | 显示新密码 | eye:password | http://127.0.0.1:8765/pages/m01-p05.html | 31 |
| m01-p05 | 再次输入新密码 | input:native | http://127.0.0.1:8765/pages/m01-p05.html | 32 |
| m01-p05 | 显示确认密码 | eye:confirm | http://127.0.0.1:8765/pages/m01-p05.html | 33 |
| m01-p05 | 确认并重置 | reset:m01-p08 | http://127.0.0.1:8765/pages/m01-p08.html | 34 |
| m01-p06 | 返回 | route:m01-p02 | http://127.0.0.1:8765/pages/m01-p02.html | 35 |
| m01-p06 | 密码 | input:native | http://127.0.0.1:8765/pages/m01-p06.html | 36 |
| m01-p06 | 显示密码 | eye:password | http://127.0.0.1:8765/pages/m01-p06.html | 37 |
| m01-p06 | 再试一次 | retry:m02-p01 | http://127.0.0.1:8765/pages/m02-p01.html | 38 |
| m01-p06 | 找回密码 | route:m01-p04 | http://127.0.0.1:8765/pages/m01-p04.html | 39 |
| m01-p07 | 返回 | route:m01-p04 | http://127.0.0.1:8765/pages/m01-p04.html | 40 |
| m01-p07 | 第 1 位验证码 | input:native | http://127.0.0.1:8765/pages/m01-p07.html | 41 |
| m01-p07 | 第 2 位验证码 | input:native | http://127.0.0.1:8765/pages/m01-p07.html | 42 |
| m01-p07 | 第 3 位验证码 | input:native | http://127.0.0.1:8765/pages/m01-p07.html | 43 |
| m01-p07 | 第 4 位验证码 | input:native | http://127.0.0.1:8765/pages/m01-p07.html | 44 |
| m01-p07 | 第 5 位验证码 | input:native | http://127.0.0.1:8765/pages/m01-p07.html | 45 |
| m01-p07 | 第 6 位验证码 | input:native | http://127.0.0.1:8765/pages/m01-p07.html | 46 |
| m01-p07 | 验证并继续 | verify:m01-p05 | http://127.0.0.1:8765/pages/m01-p05.html | 47 |
| m01-p07 | 没收到验证码？换个方式 | sheet:换一种验证方式 | http://127.0.0.1:8765/pages/m01-p07.html | 48 |
| m01-p08 | 返回登录 | route:m01-p02 | http://127.0.0.1:8765/pages/m01-p02.html | 49 |
| m02-p01 | 返回登录 | route:m01-p02 | http://127.0.0.1:8765/pages/m01-p02.html | 50 |
| m02-p01 | 邀请 TA 加入 / 生成专属邀请码 | route:m02-p02 | http://127.0.0.1:8765/pages/m02-p02.html | 51 |
| m02-p01 | 输入 TA 的邀请码 / 接受一份特别邀请 | route:m02-p03 | http://127.0.0.1:8765/pages/m02-p03.html | 52 |
| m02-p02 | 返回建立关系 | route:m02-p01 | http://127.0.0.1:8765/pages/m02-p01.html | 53 |
| m02-p02 | ✦ 复制邀请码 ✦ | clipboard:XH7K-9M2Q | http://127.0.0.1:8765/pages/m02-p02.html | 54 |
| m02-p02 | 发送给微信好友 | sheet:分享邀请 | http://127.0.0.1:8765/pages/m02-p02.html | 55 |
| m02-p02 | 保存邀请卡 | download:独家童话邀请卡.svg | http://127.0.0.1:8765/pages/m02-p02.html | 56 |
| m02-p03 | 返回 | route:m02-p01 | http://127.0.0.1:8765/pages/m02-p01.html | 57 |
| m02-p03 | 第 1 组邀请码，两位 | input:native | http://127.0.0.1:8765/pages/m02-p03.html | 58 |
| m02-p03 | 第 2 组邀请码，两位 | input:native | http://127.0.0.1:8765/pages/m02-p03.html | 59 |
| m02-p03 | 第 3 组邀请码，两位 | input:native | http://127.0.0.1:8765/pages/m02-p03.html | 60 |
| m02-p03 | 第 4 组邀请码，两位 | input:native | http://127.0.0.1:8765/pages/m02-p03.html | 61 |
| m02-p03 | 查看邀请内容 | invite:m02-p04 | http://127.0.0.1:8765/pages/m02-p04.html | 62 |
| m02-p03 | 请让 TA 分享给你 | route:m02-p01 | http://127.0.0.1:8765/pages/m02-p01.html | 63 |
| m02-p04 | 返回 | route:m02-p03 | http://127.0.0.1:8765/pages/m02-p03.html | 64 |
| m02-p04 | 确认建立关系 | bind:m02-p05 | http://127.0.0.1:8765/pages/m02-p05.html | 65 |
| m02-p04 | 暂不接受 | cancel:m02-p01 | http://127.0.0.1:8765/pages/m02-p01.html | 66 |
| m02-p05 | 去写第一篇共同日记 ♡ | route:m03-p05 | http://127.0.0.1:8765/pages/m03-p05.html | 67 |
| m02-p05 | 完善情侣资料 | route:m02-p06 | http://127.0.0.1:8765/pages/m02-p06.html | 68 |
| m02-p05 | 先逛逛我们的首页 | route:m03-p01 | http://127.0.0.1:8765/pages/m03-p01.html | 69 |
| m02-p06 | 返回 | route:m02-p05 | http://127.0.0.1:8765/pages/m02-p05.html | 70 |
| m02-p06 | 情侣昵称 | input:native | http://127.0.0.1:8765/pages/m02-p06.html | 71 |
| m02-p06 | 相遇日期 | picker:选择相遇日期 | http://127.0.0.1:8765/pages/m02-p06.html | 72 |
| m02-p06 | 共同纪念日 | picker:选择共同纪念日 | http://127.0.0.1:8765/pages/m02-p06.html | 73 |
| m02-p06 | 保存小资料 | profile:m02-p01 | http://127.0.0.1:8765/pages/m02-p01.html | 74 |
| m02-p07 | 返回邀请卡 | route:m02-p02 | http://127.0.0.1:8765/pages/m02-p02.html | 75 |
| m02-p07 | 提醒 TA 看看 | remind:已提醒 TA 查看邀请 | http://127.0.0.1:8765/pages/m02-p07.html | 76 |
| m02-p07 | 复制邀请链接 | clipboard-link:m02-p03.html?code=XH7K9M2Q | http://127.0.0.1:8765/pages/m02-p07.html | 77 |
| m02-p08 | 请 TA 重新邀请 | renew:m02-p01 | http://127.0.0.1:8765/pages/m02-p01.html | 78 |
| m02-p08 | 重新输入邀请码 | route:m02-p03 | http://127.0.0.1:8765/pages/m02-p03.html | 79 |
| m02-p09 | 回到我们的首页 | route:m03-p01 | http://127.0.0.1:8765/pages/m03-p01.html | 80 |
| m02-p09 | 查看关系设置 | route:m02-p06 | http://127.0.0.1:8765/pages/m02-p06.html | 81 |
| m03-p01 | 搜索共同记录 | route:m03-p03 | http://127.0.0.1:8765/pages/m03-p03.html | 82 |
| m03-p01 | 写日记 | route:m03-p05 | http://127.0.0.1:8765/pages/m03-p05.html | 83 |
| m03-p01 | 添加照片 | route:m03-p11 | http://127.0.0.1:8765/pages/m03-p11.html | 84 |
| m03-p01 | 去童话工坊，把回忆变成故事 › | route:m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 85 |
| m03-p01 | 首页 | nav:self | http://127.0.0.1:8765/pages/m03-p01.html | 86 |
| m03-p01 | 重要时刻 | nav:m04-p02 | http://127.0.0.1:8765/pages/m04-p02.html | 87 |
| m03-p01 | 工坊 | nav:m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 88 |
| m03-p01 | 宠物 | nav:pet | http://127.0.0.1:8765/pages/m07-p03.html | 89 |
| m03-p01 | 我的 | nav:m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 90 |
| m03-p02 | 搜索共同记录 | route:m03-p03 | http://127.0.0.1:8765/pages/m03-p03.html | 91 |
| m03-p02 | 写日记 / 记录心情 | route:m03-p05 | http://127.0.0.1:8765/pages/m03-p05.html | 92 |
| m03-p02 | 添加照片 / 珍藏瞬间 | route:m03-p11 | http://127.0.0.1:8765/pages/m03-p11.html | 93 |
| m03-p02 | 去童话工坊，把回忆变成故事 › | route:m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 94 |
| m03-p02 | 查看全部 › | route:m03-p06 | http://127.0.0.1:8765/pages/m03-p06.html | 95 |
| m03-p02 | 共同日记 小满 · 共同可见 | route:m03-p08 | http://127.0.0.1:8765/pages/m03-p08.html?id=audit-diary | 96 |
| m03-p02 | 自己的日记 小满 · 仅自己可见 | route:m03-p07 | http://127.0.0.1:8765/pages/m03-p07.html?id=audit-private | 97 |
| m03-p02 | 共同照片 小满 · 共同可见 | route:m03-p12 | http://127.0.0.1:8765/pages/m03-p12.html?id=audit-photo | 98 |
| m03-p02 | 共同测试册 / 从目录开始阅读 / 继续阅读 › | route:m08-p15 | http://127.0.0.1:8765/pages/m08-p15.html?id=book-state | 99 |
| m03-p02 | 下一件重要时刻 / 未来的纪念日 · 54 天后 / 查看纪念日 › | route:m04-p10 | http://127.0.0.1:8765/pages/m04-p10.html?id=audit-anniversary | 100 |
| m03-p02 | 首页 | nav:self | http://127.0.0.1:8765/pages/m03-p02.html | 101 |
| m03-p02 | 重要时刻 | nav:m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 102 |
| m03-p02 | 工坊 | nav:m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 103 |
| m03-p02 | 宠物 | nav:pet | http://127.0.0.1:8765/pages/m07-p03.html | 104 |
| m03-p02 | 我的 | nav:m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 105 |
| m03-p03 | 返回首页 | route:m03-p01 | http://127.0.0.1:8765/pages/m03-p01.html | 106 |
| m03-p03 | 搜索关键词 | query | http://127.0.0.1:8765/pages/m03-p03.html | 107 |
| m03-p03 | 清除搜索 | clear-query | http://127.0.0.1:8765/pages/m03-p03.html | 108 |
| m03-p03 | 晚霞 | search-chip:晚霞 | http://127.0.0.1:8765/pages/m03-p04.html?q=%E6%99%9A%E9%9C%9E | 109 |
| m03-p03 | 火锅 | search-chip:火锅 | http://127.0.0.1:8765/pages/m03-p04.html?q=%E7%81%AB%E9%94%85 | 110 |
| m03-p03 | 旅行 | search-chip:旅行 | http://127.0.0.1:8765/pages/m03-p04.html?q=%E6%97%85%E8%A1%8C | 111 |
| m03-p03 | 日记 | search-chip:日记 | http://127.0.0.1:8765/pages/m03-p04.html?q=%E6%97%A5%E8%AE%B0 | 112 |
| m03-p03 | 照片 | search-chip:照片 | http://127.0.0.1:8765/pages/m03-p04.html?q=%E7%85%A7%E7%89%87 | 113 |
| m03-p03 | 旅行 | search-chip:旅行 | http://127.0.0.1:8765/pages/m03-p04.html?q=%E6%97%85%E8%A1%8C | 114 |
| m03-p03 | 纪念日 | search-chip:纪念日 | http://127.0.0.1:8765/pages/m03-p04.html?q=%E7%BA%AA%E5%BF%B5%E6%97%A5 | 115 |
| m03-p04 | 返回搜索 | route:m03-p03 | http://127.0.0.1:8765/pages/m03-p03.html | 116 |
| m03-p04 | 搜索关键词 | query | http://127.0.0.1:8765/pages/m03-p04.html?q=%E5%85%B1%E5%90%8C | 117 |
| m03-p04 | 清除 | clear-query | http://127.0.0.1:8765/pages/m03-p03.html | 118 |
| m03-p04 | 共同日记 真正可编辑的共同正文 共同可见 | route:m03-p08 | http://127.0.0.1:8765/pages/m03-p08.html?id=audit-diary | 119 |
| m03-p04 | 共同照片 共同照片说明 共同可见 | route:m03-p12 | http://127.0.0.1:8765/pages/m03-p12.html?id=audit-photo | 120 |
| m03-p05 | 返回日记列表 | route:m03-p06 | http://127.0.0.1:8765/pages/m03-p06.html | 121 |
| m03-p05 | 存草稿 | diary-draft | http://127.0.0.1:8765/pages/m03-p06.html | 122 |
| m03-p05 | 日记标题 | input | http://127.0.0.1:8765/pages/m03-p05.html | 123 |
| m03-p05 | 今天的心情 | mood | http://127.0.0.1:8765/pages/m03-p05.html | 124 |
| m03-p05 | 日记正文 | input | http://127.0.0.1:8765/pages/m03-p05.html | 125 |
| m03-p05 | 添加照片 | file | http://127.0.0.1:8765/pages/m03-p05.html | 126 |
| m03-p05 | visibility | input | http://127.0.0.1:8765/pages/m03-p05.html | 127 |
| m03-p05 | visibility | input | http://127.0.0.1:8765/pages/m03-p05.html | 128 |
| m03-p05 | 保存日记 | diary-save | http://127.0.0.1:8765/pages/m03-p06.html | 129 |
| m03-p06 | 返回首页 | route:m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 130 |
| m03-p06 | 筛选日记 | sheet:筛选日记 | http://127.0.0.1:8765/pages/m03-p06.html | 131 |
| m03-p06 | 全部 | tab:all | http://127.0.0.1:8765/pages/m03-p06.html | 132 |
| m03-p06 | 草稿 0 | tab:draft | http://127.0.0.1:8765/pages/m03-p06.html | 133 |
| m03-p06 | 写日记 | route:m03-p05 | http://127.0.0.1:8765/pages/m03-p05.html | 134 |
| m03-p06 | 共同日记 真正可编辑的共同正文 小满 · 2026/10/4 · 共同可见 | route:m03-p08 | http://127.0.0.1:8765/pages/m03-p08.html?id=audit-diary | 135 |
| m03-p06 | 自己的日记 独立私密正文 小满 · 2026/10/4 · 仅自己可见 | route:m03-p07 | http://127.0.0.1:8765/pages/m03-p07.html?id=audit-private | 136 |
| m03-p06 | 刷新日记 | refresh:diary | http://127.0.0.1:8765/pages/m03-p06.html | 137 |
| m03-p07 | 返回日记列表 | route:m03-p06 | http://127.0.0.1:8765/pages/m03-p06.html | 138 |
| m03-p07 | 编辑日记 | route:m03-p05 | http://127.0.0.1:8765/pages/m03-p05.html?id=audit-private | 139 |
| m03-p07 | 更多操作 | sheet:日记操作 | http://127.0.0.1:8765/pages/m03-p07.html?id=audit-private | 140 |
| m03-p08 | 返回日记列表 | route:m03-p06 | http://127.0.0.1:8765/pages/m03-p06.html | 141 |
| m03-p08 | 编辑日记 | route:m03-p05 | http://127.0.0.1:8765/pages/m03-p05.html?id=audit-diary | 142 |
| m03-p08 | 给 TA 留一句话 | input | http://127.0.0.1:8765/pages/m03-p08.html?id=audit-diary | 143 |
| m03-p08 | 添加表情 | emoji | http://127.0.0.1:8765/pages/m03-p08.html?id=audit-diary | 144 |
| m03-p08 | 发送留言 | reply | http://127.0.0.1:8765/pages/m03-p08.html?id=audit-diary | 145 |
| m03-p08 | 更多操作 | sheet:日记操作 | http://127.0.0.1:8765/pages/m03-p08.html?id=audit-diary | 146 |
| m03-p09 | 返回首页 | route:m03-p01 | http://127.0.0.1:8765/pages/m03-p01.html | 147 |
| m03-p09 | 添加第一张照片 | route:m03-p11 | http://127.0.0.1:8765/pages/m03-p11.html | 148 |
| m03-p09 | 从系统相册选择 | route:m03-p11 | http://127.0.0.1:8765/pages/m03-p11.html | 149 |
| m03-p10 | 返回首页 | route:m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 150 |
| m03-p10 | 筛选照片 | sheet:筛选照片 | http://127.0.0.1:8765/pages/m03-p10.html | 151 |
| m03-p10 | 全部 | tab:all | http://127.0.0.1:8765/pages/m03-p10.html | 152 |
| m03-p10 | 共同可见 | tab:shared | http://127.0.0.1:8765/pages/m03-p10.html | 153 |
| m03-p10 | 旅行 | tab:travel | http://127.0.0.1:8765/pages/m03-p10.html | 154 |
| m03-p10 | 共同照片 | route:m03-p12 | http://127.0.0.1:8765/pages/m03-p12.html?id=audit-photo | 155 |
| m03-p10 | ＋ 添加照片 | route:m03-p11 | http://127.0.0.1:8765/pages/m03-p11.html | 156 |
| m03-p10 | 刷新相册 | refresh:photo | http://127.0.0.1:8765/pages/m03-p10.html | 157 |
| m03-p11 | 返回相册 | route:m03-p09 | http://127.0.0.1:8765/pages/m03-p09.html | 158 |
| m03-p11 | 完成 | photo-save | http://127.0.0.1:8765/pages/m03-p10.html | 159 |
| m03-p11 | 选择照片 | file | http://127.0.0.1:8765/pages/m03-p11.html | 160 |
| m03-p11 | 照片心情 | input | http://127.0.0.1:8765/pages/m03-p11.html | 161 |
| m03-p11 | 照片日期 | sheet:选择照片日期 | http://127.0.0.1:8765/pages/m03-p11.html | 162 |
| m03-p11 | 照片标签 | input | http://127.0.0.1:8765/pages/m03-p11.html | 163 |
| m03-p11 | 添加标签 | sheet:照片标签 | http://127.0.0.1:8765/pages/m03-p11.html | 164 |
| m03-p11 | visibility | input | http://127.0.0.1:8765/pages/m03-p11.html | 165 |
| m03-p11 | visibility | input | http://127.0.0.1:8765/pages/m03-p11.html | 166 |
| m03-p11 | 保存照片 | photo-save | http://127.0.0.1:8765/pages/m03-p10.html | 167 |
| m03-p12 | 返回照片相册 | route:m03-p10 | http://127.0.0.1:8765/pages/m03-p10.html | 168 |
| m03-p12 | 编辑照片 | route:m03-p11 | http://127.0.0.1:8765/pages/m03-p11.html?id=audit-photo | 169 |
| m03-p12 | 给 TA 留一句话 | input | http://127.0.0.1:8765/pages/m03-p12.html?id=audit-photo | 170 |
| m03-p12 | 添加表情 | emoji | http://127.0.0.1:8765/pages/m03-p12.html?id=audit-photo | 171 |
| m03-p12 | 发送留言 | reply | http://127.0.0.1:8765/pages/m03-p12.html?id=audit-photo | 172 |
| m03-p12 | 更多操作 | sheet:照片操作 | http://127.0.0.1:8765/pages/m03-p12.html?id=audit-photo | 173 |
| m04-p01 | 查看纪念日 | route:m04-p07 | http://127.0.0.1:8765/pages/m04-p07.html | 174 |
| m04-p01 | 珍藏一个新时刻 | route:m04-p04 | http://127.0.0.1:8765/pages/m04-p04.html | 175 |
| m04-p01 | 查看全部 › | expand | http://127.0.0.1:8765/pages/m04-p01.html | 176 |
| m04-p01 | 共同重要时刻 / 2026-10-04 | route:m04-p03 | http://127.0.0.1:8765/pages/m04-p03.html?id=audit-moment | 177 |
| m04-p01 | 纪念日 | route:m04-p07 | http://127.0.0.1:8765/pages/m04-p07.html | 178 |
| m04-p01 | 时光胶囊 | route:m04-p12 | http://127.0.0.1:8765/pages/m04-p12.html | 179 |
| m04-p01 | 悄悄留言 | route:m04-p16 | http://127.0.0.1:8765/pages/m04-p16.html | 180 |
| m04-p01 | 新建重要时刻 | route:m04-p04 | http://127.0.0.1:8765/pages/m04-p04.html | 181 |
| m04-p01 | 刷新时刻册 | refresh | http://127.0.0.1:8765/pages/m04-p01.html | 182 |
| m04-p01 | 共同提醒 | route:m04-p05 | http://127.0.0.1:8765/pages/m04-p05.html | 183 |
| m04-p01 | 首页 | nav:m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 184 |
| m04-p01 | 重要时刻 | nav:self | http://127.0.0.1:8765/pages/m04-p01.html | 185 |
| m04-p01 | 工坊 | nav:m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 186 |
| m04-p01 | 宠物 | nav:pet | http://127.0.0.1:8765/pages/m07-p03.html | 187 |
| m04-p01 | 我的 | nav:m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 188 |
| m04-p02 | 从共同记录中收录 | collect-empty | http://127.0.0.1:8765/pages/m04-p04.html?choose=1 | 189 |
| m04-p02 | 新建重要时刻 | route:m04-p04 | http://127.0.0.1:8765/pages/m04-p04.html | 190 |
| m04-p02 | 纪念日 | route:m04-p08 | http://127.0.0.1:8765/pages/m04-p08.html | 191 |
| m04-p02 | 时光胶囊 | route:m04-p12 | http://127.0.0.1:8765/pages/m04-p12.html | 192 |
| m04-p02 | 悄悄留言 | route:m04-p17 | http://127.0.0.1:8765/pages/m04-p17.html | 193 |
| m04-p02 | 共同提醒 | route:m04-p05 | http://127.0.0.1:8765/pages/m04-p06.html | 194 |
| m04-p02 | 首页 | nav:m03-p01 | http://127.0.0.1:8765/pages/m03-p01.html | 195 |
| m04-p02 | 重要时刻 | nav:self | http://127.0.0.1:8765/pages/m04-p02.html | 196 |
| m04-p02 | 工坊 | nav:m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 197 |
| m04-p02 | 宠物 | nav:pet | http://127.0.0.1:8765/pages/m07-p03.html | 198 |
| m04-p02 | 我的 | nav:m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 199 |
| m04-p03 | 返回重要时刻 | route:m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 200 |
| m04-p03 | 共同日记 | route:m03-p08 | http://127.0.0.1:8765/pages/m03-p08.html?id=audit-diary | 201 |
| m04-p03 | 悄悄留言 1 条 | sheet:时刻回应 | http://127.0.0.1:8765/pages/m04-p03.html?id=audit-moment | 202 |
| m04-p03 | 编辑时刻 | route:m04-p04 | http://127.0.0.1:8765/pages/m04-p04.html?id=audit-moment | 203 |
| m04-p03 | 更多操作 | sheet:时刻操作 | http://127.0.0.1:8765/pages/m04-p03.html?id=audit-moment | 204 |
| m04-p04 | 返回重要时刻 | route:m04-p02 | http://127.0.0.1:8765/pages/m04-p02.html | 205 |
| m04-p04 | 添加封面 | file | http://127.0.0.1:8765/pages/m04-p04.html | 206 |
| m04-p04 | name | input | http://127.0.0.1:8765/pages/m04-p04.html | 207 |
| m04-p04 | 发生日期 | sheet:发生日期 | http://127.0.0.1:8765/pages/m04-p04.html | 208 |
| m04-p04 | type | input | http://127.0.0.1:8765/pages/m04-p04.html | 209 |
| m04-p04 | type | input | http://127.0.0.1:8765/pages/m04-p04.html | 210 |
| m04-p04 | type | input | http://127.0.0.1:8765/pages/m04-p04.html | 211 |
| m04-p04 | type | input | http://127.0.0.1:8765/pages/m04-p04.html | 212 |
| m04-p04 | 记录这个时刻背后的故事… | input | http://127.0.0.1:8765/pages/m04-p04.html | 213 |
| m04-p04 | 关联共同记录，已选 0 条 | modal:选择共同记录 | http://127.0.0.1:8765/pages/m04-p04.html | 214 |
| m04-p04 | 保存到时刻册 | save | http://127.0.0.1:8765/pages/m04-p01.html | 215 |
| m04-p16 | 返回重要时刻 | route:m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 216 |
| m04-p16 | 查看原记录 | read-reply | http://127.0.0.1:8765/pages/m04-p03.html?id=audit-moment | 217 |
| m04-p17 | 返回重要时刻 | route:m04-p02 | http://127.0.0.1:8765/pages/m04-p02.html | 218 |
| m04-p17 | 去看看共同记录 | route:m03-p06 | http://127.0.0.1:8765/pages/m03-p06.html | 219 |
| m04-p05 | 返回重要时刻 | route:m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 220 |
| m04-p05 | 今天约定就在今天 /  / 一起为 2026-10-05 留一段记录吧 | notice:time-today | http://127.0.0.1:8765/pages/m04-p11.html?id=time-today | 221 |
| m04-p06 | 返回重要时刻 | route:m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 222 |
| m04-p06 | 去看看重要时刻 | route:m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 223 |
| m04-p07 | 返回重要时刻 | route:m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 224 |
| m04-p07 | 添加纪念日 | route:m04-p09 | http://127.0.0.1:8765/pages/m04-p09.html | 225 |
| m04-p07 | 2026-10-05 | route:m04-p11 | http://127.0.0.1:8765/pages/m04-p11.html?id=time-today | 226 |
| m04-p07 | 今天约定 / 每年 2026-10-05 | route:m04-p11 | http://127.0.0.1:8765/pages/m04-p11.html?id=time-today | 227 |
| m04-p07 | 今天约定提醒 | toggle-anniversary:time-today | http://127.0.0.1:8765/pages/m04-p07.html | 228 |
| m04-p07 | 未来约定 / 每年 2026-12-24 | route:m04-p10 | http://127.0.0.1:8765/pages/m04-p10.html?id=time-future | 229 |
| m04-p07 | 未来约定提醒 | toggle-anniversary:time-future | http://127.0.0.1:8765/pages/m04-p07.html | 230 |
| m04-p07 | 添加纪念日 | route:m04-p09 | http://127.0.0.1:8765/pages/m04-p09.html | 231 |
| m04-p07 | 刷新纪念日 | refresh:anniversary | http://127.0.0.1:8765/pages/m04-p07.html | 232 |
| m04-p08 | 返回重要时刻 | route:m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 233 |
| m04-p08 | 添加第一个纪念日 | route:m04-p09 | http://127.0.0.1:8765/pages/m04-p09.html | 234 |
| m04-p09 | 返回纪念日列表 | route:m04-p07 | http://127.0.0.1:8765/pages/m04-p07.html | 235 |
| m04-p09 | name | native | http://127.0.0.1:8765/pages/m04-p09.html | 236 |
| m04-p09 | 纪念日日期 | sheet:纪念日日期 | http://127.0.0.1:8765/pages/m04-p09.html | 237 |
| m04-p09 | 提前 3 天 / 提前 1 天 / 当天 / 不提醒 | native | http://127.0.0.1:8765/pages/m04-p09.html | 238 |
| m04-p09 | 每年重复 | native | http://127.0.0.1:8765/pages/m04-p09.html | 239 |
| m04-p09 | 可选 · 关联一段章节 / 关联时刻 | native | http://127.0.0.1:8765/pages/m04-p09.html | 240 |
| m04-p09 | 保存纪念日 | save-anniversary | http://127.0.0.1:8765/pages/m04-p07.html | 241 |
| m04-p10 | 返回纪念日 | route:m04-p07 | http://127.0.0.1:8765/pages/m04-p07.html | 242 |
| m04-p10 | 关联时刻 | route:m04-p03 | http://127.0.0.1:8765/pages/m04-p03.html?id=time-moment | 243 |
| m04-p10 | 写下新的共同记录 | route:m03-p05 | http://127.0.0.1:8765/pages/m03-p05.html?anniversary=time-future | 244 |
| m04-p10 | 编辑纪念日 | route:m04-p09 | http://127.0.0.1:8765/pages/m04-p09.html?id=time-future | 245 |
| m04-p10 | 更多操作 | sheet:纪念日操作 | http://127.0.0.1:8765/pages/m04-p10.html?id=time-future | 246 |
| m04-p11 | 一起留下今天的记录 | route:m03-p05 | http://127.0.0.1:8765/pages/m03-p05.html?anniversary=time-today | 247 |
| m04-p11 | 查看这个时刻 | route:m04-p03 | http://127.0.0.1:8765/pages/m04-p03.html?id=time-moment | 248 |
| m04-p11 | 返回纪念日列表 | route:m04-p07 | http://127.0.0.1:8765/pages/m04-p07.html | 249 |
| m04-p11 | 编辑纪念日 | route:m04-p09 | http://127.0.0.1:8765/pages/m04-p09.html?id=time-today | 250 |
| m04-p11 | 更多操作 | sheet:纪念日操作 | http://127.0.0.1:8765/pages/m04-p11.html?id=time-today | 251 |
| m04-p12 | 返回重要时刻 | route:m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 252 |
| m04-p12 | 新建时光胶囊 | route:m04-p13 | http://127.0.0.1:8765/pages/m04-p13.html | 253 |
| m04-p12 | 等待开启 | tab:等待开启 | http://127.0.0.1:8765/pages/m04-p12.html | 254 |
| m04-p12 | 已经开启 | tab:已经开启 | http://127.0.0.1:8765/pages/m04-p12.html | 255 |
| m04-p12 | 草稿 | tab:草稿 | http://127.0.0.1:8765/pages/m04-p12.html | 256 |
| m04-p12 | 封存的信 / 2026-10-06 · 还有 1 天 | route:m04-p15 | http://127.0.0.1:8765/pages/m04-p15.html?id=time-sealed | 257 |
| m04-p12 | ＋ 新建时光胶囊 | route:m04-p13 | http://127.0.0.1:8765/pages/m04-p13.html | 258 |
| m04-p12 | 刷新胶囊 | refresh:capsule | http://127.0.0.1:8765/pages/m04-p12.html | 259 |
| m04-p13 | 返回胶囊列表 | route:m04-p12 | http://127.0.0.1:8765/pages/m04-p12.html | 260 |
| m04-p13 | name | native | http://127.0.0.1:8765/pages/m04-p13.html | 261 |
| m04-p13 | message | native | http://127.0.0.1:8765/pages/m04-p13.html | 262 |
| m04-p13 | 添加照片 | file | http://127.0.0.1:8765/pages/m04-p13.html | 263 |
| m04-p13 | opening | sheet:开启日期 | http://127.0.0.1:8765/pages/m04-p13.html | 264 |
| m04-p13 | 开启提醒 | native | http://127.0.0.1:8765/pages/m04-p13.html | 265 |
| m04-p13 | 暂存草稿 | save-draft | http://127.0.0.1:8765/pages/m04-p12.html | 266 |
| m04-p13 | 封存这份心意 | save-sealed | http://127.0.0.1:8765/pages/m04-p15.html?id=capsule-2e53ae69-a7e8-45b4-b6ac-322167494518 | 267 |
| m04-p14 | 返回胶囊列表 | route:m04-p12 | http://127.0.0.1:8765/pages/m04-p12.html | 268 |
| m04-p14 | 把这一刻收录进重要时刻 | collect | http://127.0.0.1:8765/pages/m04-p03.html?id=capsule-moment-time-opened | 269 |
| m04-p14 | 更多胶囊操作 | sheet:胶囊操作 | http://127.0.0.1:8765/pages/m04-p14.html?id=time-opened | 270 |
| m04-p15 | 返回胶囊列表 | route:m04-p12 | http://127.0.0.1:8765/pages/m04-p12.html | 271 |
| m04-p15 | 开启当天提醒我 | native | http://127.0.0.1:8765/pages/m04-p15.html?id=time-sealed | 272 |
| m04-p15 | 更多胶囊操作 | sheet:胶囊操作 | http://127.0.0.1:8765/pages/m04-p15.html?id=time-sealed | 273 |
| m05-p01 | 做成童话漫画 / 把回忆画成专属故事 / 留下一格格心动瞬间 | route:m05-p02 | http://127.0.0.1:8765/pages/m05-p02.html | 274 |
| m05-p01 | 制作回忆影片 / 让重要时刻动起来 / 在光影里重温感动 | new-film | http://127.0.0.1:8765/pages/m05-p05.html?id=work-e603023f-f70d-4c0a-96f0-49bc5f1d6b43 | 275 |
| m05-p01 | 查看全部 › | route:m05-p09 | http://127.0.0.1:8765/pages/m05-p09.html | 276 |
| m05-p01 | work-free / 草稿 | work:work-free | http://127.0.0.1:8765/pages/m05-p03.html?id=work-free | 277 |
| m05-p01 | work-photos / 草稿 | work:work-photos | http://127.0.0.1:8765/pages/m05-p04.html?id=work-photos | 278 |
| m05-p01 | 开始一次创作 | route:m05-p02 | http://127.0.0.1:8765/pages/m05-p02.html | 279 |
| m05-p01 | 首页 | nav:m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 280 |
| m05-p01 | 重要时刻 | nav:m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 281 |
| m05-p01 | 工坊 | nav:self | http://127.0.0.1:8765/pages/m05-p01.html | 282 |
| m05-p01 | 宠物 | nav:m07-p04 | http://127.0.0.1:8765/pages/m07-p04.html | 283 |
| m05-p01 | 我的 | nav:m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 284 |
| m05-p02 | 返回童话工坊 | route:m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 285 |
| m05-p02 | 共同日记 | choice | http://127.0.0.1:8765/pages/m05-p02.html | 286 |
| m05-p02 | 相册照片 | choice | http://127.0.0.1:8765/pages/m05-p02.html | 287 |
| m05-p02 | 重要时刻 | choice | http://127.0.0.1:8765/pages/m05-p02.html | 288 |
| m05-p02 | 自由写一段回忆 | choice | http://127.0.0.1:8765/pages/m05-p02.html | 289 |
| m05-p02 | 用这些素材开始 | sheet:选择共同素材 | http://127.0.0.1:8765/pages/m05-p02.html | 290 |
| m05-p03 | 返回素材选择 | route:m05-p02 | http://127.0.0.1:8765/pages/m05-p02.html | 291 |
| m05-p03 | 回忆内容 | input | http://127.0.0.1:8765/pages/m05-p03.html?id=work-free | 292 |
| m05-p03 | 编辑 | focus-story | http://127.0.0.1:8765/pages/m05-p03.html?id=work-free | 293 |
| m05-p03 | 暖暖水彩 / ✓ | setting | http://127.0.0.1:8765/pages/m05-p03.html?id=work-free | 294 |
| m05-p03 | 复古漫画 | setting | http://127.0.0.1:8765/pages/m05-p03.html?id=work-free | 295 |
| m05-p03 | 轻柔铅笔 | setting | http://127.0.0.1:8765/pages/m05-p03.html?id=work-free | 296 |
| m05-p03 | 温柔叙事 / 贴近日常， / 细腻温暖 / ✓ | setting | http://127.0.0.1:8765/pages/m05-p03.html?id=work-free | 297 |
| m05-p03 | 电影感 / 光影氛围， / 节奏张力 | setting | http://127.0.0.1:8765/pages/m05-p03.html?id=work-free | 298 |
| m05-p03 | 默默 & 小满 / 可爱自然 · 清新温柔 | characters | http://127.0.0.1:8765/pages/m05-p10.html?work=work-free | 299 |
| m05-p03 | 生成童话漫画 | generate | http://127.0.0.1:8765/pages/m05-p06.html?id=work-free | 300 |
| m05-p03 | 暂存创作草稿 | draft | http://127.0.0.1:8765/pages/m05-p09.html | 301 |
| m05-p03 | 创作草稿操作 | sheet:创作操作 | http://127.0.0.1:8765/pages/m05-p03.html?id=work-free | 302 |
| m05-p04 | 返回素材选择 | route:m05-p02 | http://127.0.0.1:8765/pages/m05-p02.html | 303 |
| m05-p04 | 共同素材照片 | toggle-photo | http://127.0.0.1:8765/pages/m05-p04.html?id=work-photos | 304 |
| m05-p04 | 补充这段故事 | input | http://127.0.0.1:8765/pages/m05-p04.html?id=work-photos | 305 |
| m05-p04 | 水彩 / ✓ | setting | http://127.0.0.1:8765/pages/m05-p04.html?id=work-photos | 306 |
| m05-p04 | 素描 | setting | http://127.0.0.1:8765/pages/m05-p04.html?id=work-photos | 307 |
| m05-p04 | 清新插画 | setting | http://127.0.0.1:8765/pages/m05-p04.html?id=work-photos | 308 |
| m05-p04 | 油画 | setting | http://127.0.0.1:8765/pages/m05-p04.html?id=work-photos | 309 |
| m05-p04 | 他  / 阳光温柔 | characters | http://127.0.0.1:8765/pages/m05-p10.html?work=work-photos | 310 |
| m05-p04 | 她  / 温柔爱笑 | characters | http://127.0.0.1:8765/pages/m05-p10.html?work=work-photos | 311 |
| m05-p04 | 生成童话漫画 | generate | http://127.0.0.1:8765/pages/m05-p06.html?id=work-photos | 312 |
| m05-p04 | 暂存创作草稿 | draft | http://127.0.0.1:8765/pages/m05-p09.html | 313 |
| m05-p04 | 创作草稿操作 | sheet:创作操作 | http://127.0.0.1:8765/pages/m05-p04.html?id=work-photos | 314 |
| m05-p04 | 选择照片 | sheet:选择共同素材 | http://127.0.0.1:8765/pages/m05-p04.html?id=work-photos | 315 |
| m05-p05 | 返回工坊 | route:m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 316 |
| m05-p05 | 选择共同片段 | sheet:片段类型 | http://127.0.0.1:8765/pages/m05-p05.html?id=work-film | 317 |
| m05-p05 | 移除片段 共同素材日记 | remove-clip | http://127.0.0.1:8765/pages/m05-p05.html?id=work-film | 318 |
| m05-p05 | 影片旁白 | input | http://127.0.0.1:8765/pages/m05-p05.html?id=work-film | 319 |
| m05-p05 | 试听演示音轨 | audio | http://127.0.0.1:8765/pages/m05-p05.html?id=work-film | 320 |
| m05-p05 | 温柔手帐 / ✓ | setting | http://127.0.0.1:8765/pages/m05-p05.html?id=work-film | 321 |
| m05-p05 | 治愈暖光 | setting | http://127.0.0.1:8765/pages/m05-p05.html?id=work-film | 322 |
| m05-p05 | 清新自然 | setting | http://127.0.0.1:8765/pages/m05-p05.html?id=work-film | 323 |
| m05-p05 | 生成回忆影片 | generate | http://127.0.0.1:8765/pages/m05-p06.html?id=work-film | 324 |
| m05-p05 | 暂存创作草稿 | draft | http://127.0.0.1:8765/pages/m05-p09.html | 325 |
| m05-p05 | 创作草稿操作 | sheet:创作操作 | http://127.0.0.1:8765/pages/m05-p05.html?id=work-film | 326 |
| m05-p06 | 返回童话工坊 | route:m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 327 |
| m05-p06 | 取消生成 | modal:取消这次生成？ | http://127.0.0.1:8765/pages/m05-p06.html?id=work-running | 328 |
| m05-p07 | 调整内容 | route:m05-p03 | http://127.0.0.1:8765/pages/m05-p03.html?id=work-failed | 329 |
| m05-p07 | 重新生成 | generate | http://127.0.0.1:8765/pages/m05-p06.html?id=work-failed | 330 |
| m05-p07 | 先回到童话工坊 ♡ | route:m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 331 |
| m05-p08 | 返回我的创作 | route:m05-p09 | http://127.0.0.1:8765/pages/m05-p09.html | 332 |
| m05-p08 | 第1页 | frame:1 | http://127.0.0.1:8765/pages/m05-p08.html?id=work-ready | 333 |
| m05-p08 | 第2页 | frame:2 | http://127.0.0.1:8765/pages/m05-p08.html?id=work-ready | 334 |
| m05-p08 | 第3页 | frame:3 | http://127.0.0.1:8765/pages/m05-p08.html?id=work-ready | 335 |
| m05-p08 | 第4页 | frame:4 | http://127.0.0.1:8765/pages/m05-p08.html?id=work-ready | 336 |
| m05-p08 | 第5页 | frame:5 | http://127.0.0.1:8765/pages/m05-p08.html?id=work-ready | 337 |
| m05-p08 | 第6页 | frame:6 | http://127.0.0.1:8765/pages/m05-p08.html?id=work-ready | 338 |
| m05-p08 | 第7页 | frame:7 | http://127.0.0.1:8765/pages/m05-p08.html?id=work-ready | 339 |
| m05-p08 | 第8页 | frame:8 | http://127.0.0.1:8765/pages/m05-p08.html?id=work-ready | 340 |
| m05-p08 | 保存到共同相册 | album | http://127.0.0.1:8765/pages/m05-p08.html?id=work-ready | 341 |
| m05-p08 | 给另一半看看 | sheet:给另一半看看 | http://127.0.0.1:8765/pages/m05-p08.html?id=work-ready | 342 |
| m05-p08 | 重新生成 | route:m05-p05 | http://127.0.0.1:8765/pages/m05-p05.html?id=work-ready | 343 |
| m05-p08 | 更多作品操作 | sheet:创作操作 | http://127.0.0.1:8765/pages/m05-p08.html?id=work-ready | 344 |
| m05-p08 | 播放片段演示 | play | http://127.0.0.1:8765/pages/m05-p08.html?id=work-ready | 345 |
| m05-p09 | 收藏夹 | favorites | http://127.0.0.1:8765/pages/m05-p09.html | 346 |
| m05-p09 | 全部 | tab:全部 | http://127.0.0.1:8765/pages/m05-p09.html | 347 |
| m05-p09 | 漫画 | tab:漫画 | http://127.0.0.1:8765/pages/m05-p09.html | 348 |
| m05-p09 | 影片 | tab:影片 | http://127.0.0.1:8765/pages/m05-p09.html | 349 |
| m05-p09 | 草稿 | tab:草稿 | http://127.0.0.1:8765/pages/m05-p09.html | 350 |
| m05-p09 | 开始创作 | route:m05-p02 | http://127.0.0.1:8765/pages/m05-p02.html | 351 |
| m05-p09 | work-free / 漫画 · 草稿 | work:work-free | http://127.0.0.1:8765/pages/m05-p03.html?id=work-free | 352 |
| m05-p09 | work-photos / 漫画 · 草稿 | work:work-photos | http://127.0.0.1:8765/pages/m05-p04.html?id=work-photos | 353 |
| m05-p09 | work-film / 影片 · 草稿 | work:work-film | http://127.0.0.1:8765/pages/m05-p05.html?id=work-film | 354 |
| m05-p09 | work-running / 漫画 · 制作中 | work:work-running | http://127.0.0.1:8765/pages/m05-p06.html?id=work-running | 355 |
| m05-p09 | work-failed / 漫画 · 生成失败 | work:work-failed | http://127.0.0.1:8765/pages/m05-p07.html?id=work-failed | 356 |
| m05-p09 | work-ready / 影片 · 已完成 | work:work-ready | http://127.0.0.1:8765/pages/m05-p08.html?id=work-ready | 357 |
| m05-p09 | 返回童话工坊 | route:m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 358 |
| m05-p09 | 刷新我的创作 | refresh | http://127.0.0.1:8765/pages/m05-p09.html | 359 |
| m05-p10 | 返回当前创作 | route:m05-p03 | http://127.0.0.1:8765/pages/m05-p03.html?id=work-free | 360 |
| m05-p10 | appearance | input | http://127.0.0.1:8765/pages/m05-p10.html?work=work-free | 361 |
| m05-p10 | outfit | input | http://127.0.0.1:8765/pages/m05-p10.html?work=work-free | 362 |
| m05-p10 | mood | input | http://127.0.0.1:8765/pages/m05-p10.html?work=work-free | 363 |
| m05-p10 | object | input | http://127.0.0.1:8765/pages/m05-p10.html?work=work-free | 364 |
| m05-p10 | 更新我们的主角 | save-characters | http://127.0.0.1:8765/pages/m05-p03.html?id=work-free | 365 |
| m06-p01 | 小满 ♡ / 已与阿舟关联 ♡ | route:m06-p02 | http://127.0.0.1:8765/pages/m06-p02.html | 366 |
| m06-p01 | 我们的小世界 / 一起管理共同资料 | route:m06-p03 | http://127.0.0.1:8765/pages/m06-p03.html | 367 |
| m06-p01 | 草稿箱 | route:m06-p04 | http://127.0.0.1:8765/pages/m06-p04.html | 368 |
| m06-p01 | 标签管理 | route:m06-p05 | http://127.0.0.1:8765/pages/m06-p05.html | 369 |
| m06-p01 | 童话会员 | route:m06-p06 | http://127.0.0.1:8765/pages/m06-p06.html | 370 |
| m06-p01 | 设置 | route:m06-p07 | http://127.0.0.1:8765/pages/m06-p07.html | 371 |
| m06-p01 | 帮助与关于 | route:m06-p12 | http://127.0.0.1:8765/pages/m06-p12.html | 372 |
| m06-p01 | 首页 | route:m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 373 |
| m06-p01 | 重要时刻 | route:m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 374 |
| m06-p01 | 工坊 | route:m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 375 |
| m06-p01 | 宠物 | route:m07-p04 | http://127.0.0.1:8765/pages/m07-p04.html | 376 |
| m06-p01 | 我的 | route:self | http://127.0.0.1:8765/pages/m06-p01.html | 377 |
| m06-p02 | 返回我的与设置 | route:m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 378 |
| m06-p02 | 更换头像 | native-file | http://127.0.0.1:8765/pages/m06-p02.html | 379 |
| m06-p02 | 更换头像 | file | http://127.0.0.1:8765/pages/m06-p02.html | 380 |
| m06-p02 | nickname | input | http://127.0.0.1:8765/pages/m06-p02.html | 381 |
| m06-p02 | birthday | sheet:你的生日 | http://127.0.0.1:8765/pages/m06-p02.html | 382 |
| m06-p02 | saying | input | http://127.0.0.1:8765/pages/m06-p02.html | 383 |
| m06-p02 | color | input | http://127.0.0.1:8765/pages/m06-p02.html | 384 |
| m06-p02 | 保存资料 | profile-save | http://127.0.0.1:8765/pages/m06-p01.html | 385 |
| m06-p03 | 返回我的与设置 | route:m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 386 |
| m06-p03 | 共同昵称 / 共同小屋 | sheet:共同昵称 | http://127.0.0.1:8765/pages/m06-p03.html | 387 |
| m06-p03 | 共同头像 | world-file | http://127.0.0.1:8765/pages/m06-p03.html | 388 |
| m06-p03 | 共同空间设置 / 哪些记录邀请对方一起看 | route:m06-p09 | http://127.0.0.1:8765/pages/m06-p09.html | 389 |
| m06-p03 | 关联状态 | modal:关联状态 | http://127.0.0.1:8765/pages/m06-p03.html | 390 |
| m06-p03 | 解除关联 | modal:请求解除关联？ | http://127.0.0.1:8765/pages/m06-p03.html | 391 |
| m06-p04 | 返回我的与设置 | route:m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 392 |
| m06-p04 | 日记草稿 / 日记 · 继续编辑 | draft:m03-p05:audit-diary | http://127.0.0.1:8765/pages/m03-p05.html?id=audit-diary | 393 |
| m06-p04 | 工坊草稿 / 工坊 · 继续编辑 | draft:m05-p03:audit-work | http://127.0.0.1:8765/pages/m05-p03.html?id=audit-work | 394 |
| m06-p04 | 胶囊草稿 / 胶囊 · 继续编辑 | draft:m04-p13:settings-capsule | http://127.0.0.1:8765/pages/m04-p13.html?id=settings-capsule | 395 |
| m06-p04 | 回忆册草稿 / 回忆册 · 继续编辑 | draft:m08-p04:book-state | http://127.0.0.1:8765/pages/m08-p04.html?id=book-state | 396 |
| m06-p04 | 刷新草稿箱 | refresh | http://127.0.0.1:8765/pages/m06-p04.html | 397 |
| m06-p05 | 返回我的与设置 | route:m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 398 |
| m06-p05 | 新建标签 | sheet:新建标签 | http://127.0.0.1:8765/pages/m06-p05.html | 399 |
| m06-p05 | 新建标签 | sheet:新建标签 | http://127.0.0.1:8765/pages/m06-p05.html | 400 |
| m06-p05 | 个人标签 | sheet:个人标签 | http://127.0.0.1:8765/pages/m06-p05.html | 401 |
| m06-p05 | 共同标签 | sheet:共同标签 | http://127.0.0.1:8765/pages/m06-p05.html | 402 |
| m06-p05 | 旅行 | sheet:旅行 | http://127.0.0.1:8765/pages/m06-p05.html | 403 |
| m06-p06 | 返回我的与设置 | route:m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 404 |
| m06-p06 | 开通童话会员 | modal:开通演示会员？ | http://127.0.0.1:8765/pages/m06-p06.html | 405 |
| m06-p06 | 查看会员说明 › | modal:童话会员说明 | http://127.0.0.1:8765/pages/m06-p06.html | 406 |
| m06-p07 | 返回我的与设置 | route:m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 407 |
| m06-p07 | 账号与安全 | route:m06-p08 | http://127.0.0.1:8765/pages/m06-p08.html | 408 |
| m06-p07 | 隐私与共同可见 | route:m06-p09 | http://127.0.0.1:8765/pages/m06-p09.html | 409 |
| m06-p07 | 通知设置 | route:m06-p10 | http://127.0.0.1:8765/pages/m06-p10.html | 410 |
| m06-p07 | 数据与存储 | route:m06-p11 | http://127.0.0.1:8765/pages/m06-p11.html | 411 |
| m06-p07 | 显示与外观 | sheet:显示与外观 | http://127.0.0.1:8765/pages/m06-p07.html | 412 |
| m06-p07 | 语言 | sheet:语言 | http://127.0.0.1:8765/pages/m06-p07.html | 413 |
| m06-p07 | 退出登录 | modal:退出当前登录？ | http://127.0.0.1:8765/pages/m06-p07.html | 414 |
| m06-p08 | 返回设置 | route:m06-p07 | http://127.0.0.1:8765/pages/m06-p07.html | 415 |
| m06-p08 | 修改密码 | route:m01-p04 | http://127.0.0.1:8765/pages/m01-p04.html | 416 |
| m06-p08 | 绑定手机 | sheet:绑定手机（本地演示） | http://127.0.0.1:8765/pages/m06-p08.html | 417 |
| m06-p08 | 登录设备 / 当前设备安全 | modal:登录设备 | http://127.0.0.1:8765/pages/m06-p08.html | 418 |
| m06-p08 | 两步验证 · 未开启 | sheet:开启两步验证演示 | http://127.0.0.1:8765/pages/m06-p08.html | 419 |
| m06-p08 | 退出登录 | modal:退出当前登录？ | http://127.0.0.1:8765/pages/m06-p08.html | 420 |
| m06-p08 | 注销账号 | modal:注销本地演示账号？ | http://127.0.0.1:8765/pages/m06-p08.html | 421 |
| m06-p09 | 返回设置 | route:m06-p07 | http://127.0.0.1:8765/pages/m06-p07.html | 422 |
| m06-p09 | 默认可见范围 / 共同可见 | sheet:新记录默认可见范围 | http://127.0.0.1:8765/pages/m06-p09.html | 423 |
| m06-p09 | 共同可见 | switch | http://127.0.0.1:8765/pages/m06-p09.html | 424 |
| m06-p09 | 共同空间 | switch | http://127.0.0.1:8765/pages/m06-p09.html | 425 |
| m06-p09 | 另一半回应 | switch | http://127.0.0.1:8765/pages/m06-p09.html | 426 |
| m06-p09 | 相关提醒 | switch | http://127.0.0.1:8765/pages/m06-p09.html | 427 |
| m06-p10 | 返回设置 | route:m06-p07 | http://127.0.0.1:8765/pages/m06-p07.html | 428 |
| m06-p10 | 另一半回应 | switch | http://127.0.0.1:8765/pages/m06-p10.html | 429 |
| m06-p10 | 重要时刻 | switch | http://127.0.0.1:8765/pages/m06-p10.html | 430 |
| m06-p10 | 时光胶囊 | switch | http://127.0.0.1:8765/pages/m06-p10.html | 431 |
| m06-p10 | 工坊完成 | switch | http://127.0.0.1:8765/pages/m06-p10.html | 432 |
| m06-p10 | 通知总开关 | switch | http://127.0.0.1:8765/pages/m06-p10.html | 433 |
| m06-p11 | 返回设置 | route:m06-p07 | http://127.0.0.1:8765/pages/m06-p07.html | 434 |
| m06-p11 | 导出我的记录 | export | http://127.0.0.1:8765/pages/m06-p11.html | 435 |
| m06-p11 | 共同记录备份 | backup | http://127.0.0.1:8765/pages/m06-p11.html | 436 |
| m06-p11 | 自动备份 | auto | http://127.0.0.1:8765/pages/m06-p11.html | 437 |
| m06-p11 | 存储空间管理 | modal:本地存储空间 | http://127.0.0.1:8765/pages/m06-p11.html | 438 |
| m06-p11 | 清理缓存 / 0.0 KB | modal:清理浏览记录缓存？ | http://127.0.0.1:8765/pages/m06-p11.html | 439 |
| m06-p12 | 返回我的与设置 | route:m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 440 |
| m06-p12 | 使用帮助 | modal:使用帮助 | http://127.0.0.1:8765/pages/m06-p12.html | 441 |
| m06-p12 | 意见反馈 | sheet:意见反馈 | http://127.0.0.1:8765/pages/m06-p12.html | 442 |
| m06-p12 | 隐私政策 | modal:隐私政策 | http://127.0.0.1:8765/pages/m06-p12.html | 443 |
| m06-p12 | 用户协议 | modal:用户协议 | http://127.0.0.1:8765/pages/m06-p12.html | 444 |
| m06-p12 | 检查更新 | modal:版本信息 | http://127.0.0.1:8765/pages/m06-p12.html | 445 |
| m06-p12 | 关于独家童话 | modal:关于独家童话 | http://127.0.0.1:8765/pages/m06-p12.html | 446 |
| m07-p01 | 提醒 TA 看看 › | remind | http://127.0.0.1:8765/pages/m07-p01.html | 447 |
| m07-p01 | 暂时返回 | route:m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 448 |
| m07-p01 | 返回 | route:m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 449 |
| m07-p01 | 首页 | route:m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 450 |
| m07-p01 | 重要时刻 | route:m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 451 |
| m07-p01 | 工坊 | route:m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 452 |
| m07-p01 | 宠物 | route:self | http://127.0.0.1:8765/pages/m07-p01.html | 453 |
| m07-p01 | 我的 | route:m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 454 |
| m07-p02 | 小狗 | pressed | http://127.0.0.1:8765/pages/m07-p02.html | 455 |
| m07-p02 | 小猫 | pressed | http://127.0.0.1:8765/pages/m07-p02.html | 456 |
| m07-p02 | 小兔 | pressed | http://127.0.0.1:8765/pages/m07-p02.html | 457 |
| m07-p02 | 小狐狸 | pressed | http://127.0.0.1:8765/pages/m07-p02.html | 458 |
| m07-p02 | pet-name | input | http://127.0.0.1:8765/pages/m07-p02.html | 459 |
| m07-p02 | 邀请 TA 一起领养 | adopt | http://127.0.0.1:8765/pages/m07-p01.html | 460 |
| m07-p02 | 返回 | route:m07-p04 | http://127.0.0.1:8765/pages/m07-p04.html | 461 |
| m07-p03 | 互动 | route:m07-p06 | http://127.0.0.1:8765/pages/m07-p06.html | 462 |
| m07-p03 | 喂食 | route:m07-p08 | http://127.0.0.1:8765/pages/m07-p08.html | 463 |
| m07-p03 | 任务 | route:m07-p11 | http://127.0.0.1:8765/pages/m07-p11.html | 464 |
| m07-p03 | 装扮 | route:m07-p12 | http://127.0.0.1:8765/pages/m07-p12.html | 465 |
| m07-p03 | 布置小屋 | route:m07-p15 | http://127.0.0.1:8765/pages/m07-p15.html | 466 |
| m07-p03 | 成长故事 | route:m07-p18 | http://127.0.0.1:8765/pages/m07-p18.html | 467 |
| m07-p03 | 成就图鉴 | route:m07-p21 | http://127.0.0.1:8765/pages/m07-p21.html | 468 |
| m07-p03 | 去任务 › | route:m07-p11 | http://127.0.0.1:8765/pages/m07-p11.html | 469 |
| m07-p03 | 返回 | route:m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 470 |
| m07-p03 | 宠物设置 | route:m07-p25 | http://127.0.0.1:8765/pages/m07-p25.html | 471 |
| m07-p03 | 首页 | route:m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 472 |
| m07-p03 | 重要时刻 | route:m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 473 |
| m07-p03 | 工坊 | route:m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 474 |
| m07-p03 | 宠物 | route:self | http://127.0.0.1:8765/pages/m07-p03.html | 475 |
| m07-p03 | 我的 | route:m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 476 |
| m07-p04 | 照顾指南 | modal:一起照顾小伙伴 | http://127.0.0.1:8765/pages/m07-p04.html | 477 |
| m07-p04 | 宠物日记 | modal:从第一天开始记录 | http://127.0.0.1:8765/pages/m07-p04.html | 478 |
| m07-p04 | 一起领养 | route:m07-p02 | http://127.0.0.1:8765/pages/m07-p02.html | 479 |
| m07-p04 | 先看看照顾指南 | modal:一起照顾小伙伴 | http://127.0.0.1:8765/pages/m07-p04.html | 480 |
| m07-p04 | 返回 | route:m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 481 |
| m07-p04 | 首页 | route:m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 482 |
| m07-p04 | 重要时刻 | route:m04-p01 | http://127.0.0.1:8765/pages/m04-p01.html | 483 |
| m07-p04 | 工坊 | route:m05-p01 | http://127.0.0.1:8765/pages/m05-p01.html | 484 |
| m07-p04 | 宠物 | route:self | http://127.0.0.1:8765/pages/m07-p04.html | 485 |
| m07-p04 | 我的 | route:m06-p01 | http://127.0.0.1:8765/pages/m06-p01.html | 486 |
| m07-p05 | 再玩一次 | route:m07-p06 | http://127.0.0.1:8765/pages/m07-p06.html | 487 |
| m07-p05 | 回到小屋 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 488 |
| m07-p05 | 返回 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 489 |
| m07-p06 | 摸摸头 / 精力 -5 · 亲密 +3 · 心情 +2 | pressed | http://127.0.0.1:8765/pages/m07-p06.html | 490 |
| m07-p06 | 丢球球 / 精力 -12 · 亲密 +3 · 心情 +8 | pressed | http://127.0.0.1:8765/pages/m07-p06.html | 491 |
| m07-p06 | 讲故事 / 精力 -8 · 亲密 +6 · 心情 +4 | pressed | http://127.0.0.1:8765/pages/m07-p06.html | 492 |
| m07-p06 | 送小礼物 / 礼物 1 份 · 消耗1份 | pressed | http://127.0.0.1:8765/pages/m07-p06.html | 493 |
| m07-p06 | 和团团互动 | play | http://127.0.0.1:8765/pages/m07-p05.html?id=e0bcf2cc-04ae-44fe-857d-9a27c11c0890 | 494 |
| m07-p06 | 返回 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 495 |
| m07-p07 | 宠物空间 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 496 |
| m07-p07 | 成长日记 | route:m07-p18 | http://127.0.0.1:8765/pages/m07-p18.html | 497 |
| m07-p07 | 去喂食补充精力 › | route:m07-p08 | http://127.0.0.1:8765/pages/m07-p08.html | 498 |
| m07-p08 | 香香主粮 / ×12 / 饱食+12 精力+15 | pressed | http://127.0.0.1:8765/pages/m07-p08.html | 499 |
| m07-p08 | 爱心小饼干 / ×5 / 饱食+8 精力+8 心情+2 | pressed | http://127.0.0.1:8765/pages/m07-p08.html | 500 |
| m07-p08 | 草莓布丁 / ×1 / 饱食+20 精力+20 心情+5 | pressed | http://127.0.0.1:8765/pages/m07-p08.html | 501 |
| m07-p08 | 喂给团团 | feed | http://127.0.0.1:8765/pages/m07-p08.html | 502 |
| m07-p08 | 去获得更多食物 › | route:m07-p11 | http://127.0.0.1:8765/pages/m07-p11.html | 503 |
| m07-p08 | 返回 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 504 |
| m07-p09 | 返回 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 505 |
| m07-p09 | 去做任务 | route:m07-p11 | http://127.0.0.1:8765/pages/m07-p11.html | 506 |
| m07-p10 | 返回任务 | route:m07-p11 | http://127.0.0.1:8765/pages/m07-p11.html | 507 |
| m07-p10 | 返回 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 508 |
| m07-p11 | 每日任务 | tab | http://127.0.0.1:8765/pages/m07-p11.html | 509 |
| m07-p11 | 本周约定 | tab | http://127.0.0.1:8765/pages/m07-p11.html | 510 |
| m07-p11 | 返回小屋 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 511 |
| m07-p11 | 返回 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 512 |
| m07-p11 | 给宠物添水 | water | http://127.0.0.1:8765/pages/m07-p11.html | 513 |
| m07-p11 | 陪宠物互动 | route:m07-p06 | http://127.0.0.1:8765/pages/m07-p06.html | 514 |
| m07-p11 | 给宠物喂食 | route:m07-p08 | http://127.0.0.1:8765/pages/m07-p08.html | 515 |
| m07-p11 | 整理宠物小屋 | route:m07-p15 | http://127.0.0.1:8765/pages/m07-p15.html | 516 |
| m07-p11 | 记录今天的小心情 | sheet:宠物小心情 | http://127.0.0.1:8765/pages/m07-p11.html | 517 |
| m07-p12 | 返回宠物小屋 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 518 |
| m07-p12 | 衣服 | tab | http://127.0.0.1:8765/pages/m07-p12.html | 519 |
| m07-p12 | 配饰 | tab | http://127.0.0.1:8765/pages/m07-p12.html | 520 |
| m07-p12 | 小物 | tab | http://127.0.0.1:8765/pages/m07-p12.html | 521 |
| m07-p12 | 不佩戴 | none | http://127.0.0.1:8765/pages/m07-p12.html | 522 |
| m07-p12 | 小花围巾 已拥有 | catalog:scarf | http://127.0.0.1:8765/pages/m07-p12.html | 523 |
| m07-p12 | 格纹蝴蝶结 金币20 | catalog:bow | http://127.0.0.1:8765/pages/m07-p12.html | 524 |
| m07-p12 | 星星领结 亲密度160 | catalog:star-bow | http://127.0.0.1:8765/pages/m07-p12.html | 525 |
| m07-p12 | 蜜桃帽子 记录一页成长故事 | catalog:peach-hat | http://127.0.0.1:8765/pages/m07-p12.html | 526 |
| m07-p12 | 星光皇冠 星星30 | catalog:crown | http://127.0.0.1:8765/pages/m07-p12.html | 527 |
| m07-p12 | 保存这身搭配 | outfit-save | http://127.0.0.1:8765/pages/m07-p12.html | 528 |
| m07-p13 | 宠物空间 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 529 |
| m07-p13 | 去做任务 | route:m07-p11 | http://127.0.0.1:8765/pages/m07-p11.html | 530 |
| m07-p14 | 继续布置 | route:m07-p15 | http://127.0.0.1:8765/pages/m07-p15.html | 531 |
| m07-p14 | 回到小屋 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 532 |
| m07-p14 | 返回 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 533 |
| m07-p15 | 地毯 | tab | http://127.0.0.1:8765/pages/m07-p15.html | 534 |
| m07-p15 | 小床 | tab | http://127.0.0.1:8765/pages/m07-p15.html | 535 |
| m07-p15 | 墙饰 | tab | http://127.0.0.1:8765/pages/m07-p15.html | 536 |
| m07-p15 | 摆件 | tab | http://127.0.0.1:8765/pages/m07-p15.html | 537 |
| m07-p15 | 花朵地毯 已拥有 | catalog:flower-rug | http://127.0.0.1:8765/pages/m07-p15.html | 538 |
| m07-p15 | 格纹地毯 金币20 | catalog:plaid-rug | http://127.0.0.1:8765/pages/m07-p15.html | 539 |
| m07-p15 | 月亮地毯 亲密度160 | catalog:moon-rug | http://127.0.0.1:8765/pages/m07-p15.html | 540 |
| m07-p15 | 野餐垫 照顾7个不同日期 | catalog:picnic-rug | http://127.0.0.1:8765/pages/m07-p16.html?item=picnic-rug | 541 |
| m07-p15 | 保存小屋布置 | room-save | http://127.0.0.1:8765/pages/m07-p14.html?id=c65237f1-5ada-4dd5-84cb-7f5eb22feaea | 542 |
| m07-p15 | 返回 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 543 |
| m07-p16 | 返回 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 544 |
| m07-p16 | 去做任务 | route:m07-p11 | http://127.0.0.1:8765/pages/m07-p11.html | 545 |
| m07-p17 | 返回成长时间线 | route:m07-p18 | http://127.0.0.1:8765/pages/m07-p18.html | 546 |
| m07-p17 | 返回成长时间线 | route:m07-p18 | http://127.0.0.1:8765/pages/m07-p18.html | 547 |
| m07-p18 | 写一页成长故事 | sheet:成长故事 | http://127.0.0.1:8765/pages/m07-p18.html | 548 |
| m07-p18 | 返回 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 549 |
| m07-p18 | 2026-10-05 · 小满 / 共同成长故事 | route:m07-p19:id=pet-story | http://127.0.0.1:8765/pages/m07-p19.html?id=pet-story | 550 |
| m07-p18 | 关联共同记录 | sheet:关联共同记录 | http://127.0.0.1:8765/pages/m07-p18.html | 551 |
| m07-p19 | 写下今天的下一页 | sheet:成长故事 | http://127.0.0.1:8765/pages/m07-p19.html?id=pet-story | 552 |
| m07-p19 | 返回 | route:m07-p18 | http://127.0.0.1:8765/pages/m07-p18.html | 553 |
| m07-p19 | 回应这一页 | sheet:回应 | http://127.0.0.1:8765/pages/m07-p19.html?id=pet-story | 554 |
| m07-p20 | 返回 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 555 |
| m07-p20 | 领取奖励 | achievement | http://127.0.0.1:8765/pages/m07-p20.html?achievement=days30 | 556 |
| m07-p21 | 第一次见面 可领取奖励 | route:m07-p20:achievement=meet | http://127.0.0.1:8765/pages/m07-p20.html?achievement=meet | 557 |
| m07-p21 | 玩到天黑 0 / 10 | route:m07-p20:achievement=play10 | http://127.0.0.1:8765/pages/m07-p20.html?achievement=play10 | 558 |
| m07-p21 | 默契喂食 0 / 20 | route:m07-p20:achievement=feed20 | http://127.0.0.1:8765/pages/m07-p20.html?achievement=feed20 | 559 |
| m07-p21 | 小屋变新了 0 / 1 | route:m07-p20:achievement=room | http://127.0.0.1:8765/pages/m07-p20.html?achievement=room | 560 |
| m07-p21 | 照顾7天 1 / 7 | route:m07-p20:achievement=care7 | http://127.0.0.1:8765/pages/m07-p20.html?achievement=care7 | 561 |
| m07-p21 | 亲密搭档 可领取奖励 | route:m07-p20:achievement=affinity | http://127.0.0.1:8765/pages/m07-p20.html?achievement=affinity | 562 |
| m07-p21 | 陪伴30天 可领取奖励 | route:m07-p20:achievement=days30 | http://127.0.0.1:8765/pages/m07-p20.html?achievement=days30 | 563 |
| m07-p21 | 去完成今天的照顾 | route:m07-p11 | http://127.0.0.1:8765/pages/m07-p11.html | 564 |
| m07-p21 | 返回 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 565 |
| m07-p21 | 收藏图鉴 | route:m07-p22 | http://127.0.0.1:8765/pages/m07-p22.html | 566 |
| m07-p22 | 装扮 | tab | http://127.0.0.1:8765/pages/m07-p22.html | 567 |
| m07-p22 | 小屋 | tab | http://127.0.0.1:8765/pages/m07-p22.html | 568 |
| m07-p22 | 纪念物 | tab | http://127.0.0.1:8765/pages/m07-p22.html | 569 |
| m07-p22 | 小花围巾 已拥有 | catalog:scarf | http://127.0.0.1:8765/pages/m07-p23.html?item=scarf | 570 |
| m07-p22 | 格纹蝴蝶结 金币20 | catalog:bow | http://127.0.0.1:8765/pages/m07-p23.html?item=bow | 571 |
| m07-p22 | 星星领结 亲密度160 | catalog:star-bow | http://127.0.0.1:8765/pages/m07-p23.html?item=star-bow | 572 |
| m07-p22 | 蜜桃帽子 记录一页成长故事 | catalog:peach-hat | http://127.0.0.1:8765/pages/m07-p23.html?item=peach-hat | 573 |
| m07-p22 | 星光皇冠 星星30 | catalog:crown | http://127.0.0.1:8765/pages/m07-p23.html?item=crown | 574 |
| m07-p22 | 雨天小斗篷 照顾7个不同日期 | catalog:cape | http://127.0.0.1:8765/pages/m07-p23.html?item=cape | 575 |
| m07-p22 | 暖暖小马甲 金币20 | catalog:vest | http://127.0.0.1:8765/pages/m07-p23.html?item=vest | 576 |
| m07-p22 | 晚安铃铛 喂食20次 | catalog:bell | http://127.0.0.1:8765/pages/m07-p23.html?item=bell | 577 |
| m07-p22 | 返回 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 578 |
| m07-p22 | 认识小伙伴 | sheet:四位小伙伴 | http://127.0.0.1:8765/pages/m07-p22.html | 579 |
| m07-p23 | 返回图鉴 | route:m07-p22 | http://127.0.0.1:8765/pages/m07-p22.html | 580 |
| m07-p23 | 去换上 | equip | http://127.0.0.1:8765/pages/m07-p12.html | 581 |
| m07-p23 | 返回图鉴 | route:m07-p22 | http://127.0.0.1:8765/pages/m07-p22.html | 582 |
| m07-p24 | 先导出成长记录 | export | http://127.0.0.1:8765/pages/m07-p24.html | 583 |
| m07-p24 | 暂时解除共同照顾 | modal:暂停共同照顾？ | http://127.0.0.1:8765/pages/m07-p24.html | 584 |
| m07-p24 | 我再想想，返回 | route:m07-p25 | http://127.0.0.1:8765/pages/m07-p25.html | 585 |
| m07-p24 | 返回 | route:m07-p25 | http://127.0.0.1:8765/pages/m07-p25.html | 586 |
| m07-p25 | 返回宠物空间 | route:m07-p03 | http://127.0.0.1:8765/pages/m07-p03.html | 587 |
| m07-p25 | 共同提醒 / 每天 20:30 · 本地提醒 | sheet:提醒时间 | http://127.0.0.1:8765/pages/m07-p25.html | 588 |
| m07-p25 | 共同提醒 | setting | http://127.0.0.1:8765/pages/m07-p25.html | 589 |
| m07-p25 | 照顾通知 | setting | http://127.0.0.1:8765/pages/m07-p25.html | 590 |
| m07-p25 | 照顾通知 | setting | http://127.0.0.1:8765/pages/m07-p25.html | 591 |
| m07-p25 | 成长故事自动收录 | setting | http://127.0.0.1:8765/pages/m07-p25.html | 592 |
| m07-p25 | 成长故事自动收录 | setting | http://127.0.0.1:8765/pages/m07-p25.html | 593 |
| m07-p25 | 导出团团的成长记录 | export | http://127.0.0.1:8765/pages/m07-p25.html | 594 |
| m07-p25 | 仅我们可见说明 | modal:仅我们可见 | http://127.0.0.1:8765/pages/m07-p25.html | 595 |
| m07-p25 | 暂时解除共同照顾 | route:m07-p24 | http://127.0.0.1:8765/pages/m07-p24.html | 596 |
| m07-p25 | 更多 | sheet:宠物资料与数据 | http://127.0.0.1:8765/pages/m07-p25.html | 597 |
| m08-p01 | 返回首页 | route:m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 598 |
| m08-p01 | ··· | sheet:全部回忆册 | http://127.0.0.1:8765/pages/m08-p01.html | 599 |
| m08-p01 | 全部回忆册 › | sheet:全部回忆册 | http://127.0.0.1:8765/pages/m08-p01.html | 600 |
| m08-p01 | 从封面打开《共同测试册》 | read-route:m08-p16?id=book-state&page=page-state | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-state&offset=0&block=0 | 601 |
| m08-p01 | 封面 | route:m08-p05?id=book-state&origin=manage | http://127.0.0.1:8765/pages/m08-p05.html?id=book-state&origin=manage | 602 |
| m08-p01 | 整理 | route:m08-p13 | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 603 |
| m08-p01 | 开始翻阅 → | read-route:m08-p16?id=book-state&page=page-state | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-state&offset=0&block=0 | 604 |
| m08-p01 | ＋ 新建回忆册 | route:m08-p04 | http://127.0.0.1:8765/pages/m08-p04.html | 605 |
| m08-p01 | 本月推荐 | route:m08-p03 | http://127.0.0.1:8765/pages/m08-p03.html | 606 |
| m08-p01 | 归档与草稿 | sheet:全部回忆册 | http://127.0.0.1:8765/pages/m08-p01.html | 607 |
| m08-p02 | 返回 | route:m03-p02 | http://127.0.0.1:8765/pages/m03-p02.html | 608 |
| m08-p02 | 新建第一本回忆册 | route:m08-p04 | http://127.0.0.1:8765/pages/m08-p04.html | 609 |
| m08-p03 | 返回 | route:m08-p01 | http://127.0.0.1:8765/pages/m08-p01.html | 610 |
| m08-p03 | 共同日记 · 2026-10-04 | route:m03-p08?id=audit-diary | http://127.0.0.1:8765/pages/m03-p08.html?id=audit-diary | 611 |
| m08-p03 | 共同照片 · 2026-10-04 | route:m03-p12?id=audit-photo | http://127.0.0.1:8765/pages/m03-p12.html?id=audit-photo | 612 |
| m08-p03 | 共同重要时刻 · 2026-10-04 | route:m04-p03?id=audit-moment | http://127.0.0.1:8765/pages/m04-p03.html?id=audit-moment | 613 |
| m08-p03 | 实际工坊作品 · 2026-10-05 | route:m05-p08?id=audit-work | http://127.0.0.1:8765/pages/m05-p08.html?id=audit-work | 614 |
| m08-p03 | 实际成长故事 · 2026-10-04 | route:m07-p19?id=audit-story | http://127.0.0.1:8765/pages/m07-p19.html?id=audit-story | 615 |
| m08-p03 | 开始制作 | route:m08-p04 | http://127.0.0.1:8765/pages/m08-p04.html?recommend=1 | 616 |
| m08-p03 | 返回书架 | route:m08-p01 | http://127.0.0.1:8765/pages/m08-p01.html | 617 |
| m08-p04 | 返回 | route:m08-p01 | http://127.0.0.1:8765/pages/m08-p01.html | 618 |
| m08-p04 | 书名 | input | http://127.0.0.1:8765/pages/m08-p04.html | 619 |
| m08-p04 | 开始月份 | input | http://127.0.0.1:8765/pages/m08-p04.html | 620 |
| m08-p04 | 结束月份 | input | http://127.0.0.1:8765/pages/m08-p04.html | 621 |
| m08-p04 | 挑选共同素材 | pressed | http://127.0.0.1:8765/pages/m08-p04.html | 622 |
| m08-p04 | 空白回忆册 | pressed | http://127.0.0.1:8765/pages/m08-p04.html | 623 |
| m08-p04 | 下一步 · 设计封面 | create | http://127.0.0.1:8765/pages/m08-p05.html?id=book-f0fb7187-9f2d-4cf7-8928-6c08e4444646 | 624 |
| m08-p05 | 返回 | route:m08-p04 | http://127.0.0.1:8765/pages/m08-p04.html?id=book-state | 625 |
| m08-p05 | 花园午后 | pressed | http://127.0.0.1:8765/pages/m08-p05.html?id=book-state | 626 |
| m08-p05 | 旅行手札 | pressed | http://127.0.0.1:8765/pages/m08-p05.html?id=book-state | 627 |
| m08-p05 | 暖灯日常 | pressed | http://127.0.0.1:8765/pages/m08-p05.html?id=book-state | 628 |
| m08-p05 | 使用封面照片 | sheet:选择共同素材 | http://127.0.0.1:8765/pages/m08-p05.html?id=book-state | 629 |
| m08-p05 | 保存封面 · 继续 | theme-save | http://127.0.0.1:8765/pages/m08-p06.html?id=book-state | 630 |
| m08-p06 | 返回 | route:m08-p05 | http://127.0.0.1:8765/pages/m08-p05.html?id=book-state | 631 |
| m08-p06 | 全部 | tab | http://127.0.0.1:8765/pages/m08-p06.html?id=book-state | 632 |
| m08-p06 | 日记 | tab | http://127.0.0.1:8765/pages/m08-p06.html?id=book-state | 633 |
| m08-p06 | 照片 | tab | http://127.0.0.1:8765/pages/m08-p06.html?id=book-state | 634 |
| m08-p06 | 时刻 | tab | http://127.0.0.1:8765/pages/m08-p06.html?id=book-state | 635 |
| m08-p06 | 工坊 | tab | http://127.0.0.1:8765/pages/m08-p06.html?id=book-state | 636 |
| m08-p06 | 宠物 | tab | http://127.0.0.1:8765/pages/m08-p06.html?id=book-state | 637 |
| m08-p06 | 共同日记 · 日记 · 2026-10-04 | source-toggle | http://127.0.0.1:8765/pages/m08-p06.html?id=book-state | 638 |
| m08-p06 | 共同照片 · 照片 · 2026-10-04 | source-toggle | http://127.0.0.1:8765/pages/m08-p06.html?id=book-state | 639 |
| m08-p06 | 共同重要时刻 · 时刻 · 2026-10-04 | source-toggle | http://127.0.0.1:8765/pages/m08-p06.html?id=book-state | 640 |
| m08-p06 | 实际工坊作品 · 工坊 · 2026-10-05 | source-toggle | http://127.0.0.1:8765/pages/m08-p06.html?id=book-state | 641 |
| m08-p06 | 实际成长故事 · 宠物 · 2026-10-04 | source-toggle | http://127.0.0.1:8765/pages/m08-p06.html?id=book-state | 642 |
| m08-p06 | 下一步 · 编排回忆 | select-save | http://127.0.0.1:8765/pages/m08-p07.html?id=book-state | 643 |
| m08-p07 | 返回 | route:m08-p06 | http://127.0.0.1:8765/pages/m08-p06.html?id=book-state | 644 |
| m08-p07 | 放进回忆册 | route:m08-p08 | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state&source=audit-diary&kind=diary | 645 |
| m08-p07 | 暂不放入 | skip | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 646 |
| m08-p07 | 重新选择素材 | route:m08-p06 | http://127.0.0.1:8765/pages/m08-p06.html?id=book-state | 647 |
| m08-p08 | 返回 | route:m08-p07 | http://127.0.0.1:8765/pages/m08-p07.html?id=book-state | 648 |
| m08-p08 | ♡ / 日记摘录 | pressed | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state | 649 |
| m08-p08 | ♡ / 照片故事 | pressed | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state | 650 |
| m08-p08 | ♡ / 重要时刻 | pressed | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state | 651 |
| m08-p08 | ♡ / 工坊作品 | pressed | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state | 652 |
| m08-p08 | ♡ / 宠物成长 | pressed | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state | 653 |
| m08-p08 | ♡ / 章节扉页 | pressed | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state | 654 |
| m08-p08 | 使用这个版式 | route:m08-p09 | http://127.0.0.1:8765/pages/m08-p09.html?id=book-state&source=audit-diary&kind=diary&template=%E6%97%A5%E8%AE%B0%E6%91%98%E5%BD%95&page=&draft= | 655 |
| m08-p09 | 返回 | route:m08-p08 | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state | 656 |
| m08-p09 | 书页标题 | input | http://127.0.0.1:8765/pages/m08-p09.html?id=book-state&page=page-state | 657 |
| m08-p09 | 日记摘录 | input | http://127.0.0.1:8765/pages/m08-p09.html?id=book-state&page=page-state | 658 |
| m08-p09 | 书页日期 | input | http://127.0.0.1:8765/pages/m08-p09.html?id=book-state&page=page-state | 659 |
| m08-p09 | 书页寄语 | input | http://127.0.0.1:8765/pages/m08-p09.html?id=book-state&page=page-state | 660 |
| m08-p09 | 更换摘录 | sheet:选择共同素材 | http://127.0.0.1:8765/pages/m08-p09.html?id=book-state&page=page-state | 661 |
| m08-p09 | 选择照片 | sheet:选择共同素材 | http://127.0.0.1:8765/pages/m08-p09.html?id=book-state&page=page-state | 662 |
| m08-p09 | 更换版式 | stash | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state&draft=15c21cef-1e5e-43bb-b6c2-c2421dd4975c&page=page-state&source=audit-diary&kind=diary | 663 |
| m08-p09 | 保存这一页 | page-save | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 664 |
| m08-p10 | 返回 | route:m08-p08 | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state | 665 |
| m08-p10 | 书页标题 | input | http://127.0.0.1:8765/pages/m08-p10.html?id=book-state&page=page-state | 666 |
| m08-p10 | 书页日期 | input | http://127.0.0.1:8765/pages/m08-p10.html?id=book-state&page=page-state | 667 |
| m08-p10 | 照片 1 · 裁剪或替换 | sheet:照片1 | http://127.0.0.1:8765/pages/m08-p10.html?id=book-state&page=page-state | 668 |
| m08-p10 | 照片 2 · 裁剪或替换 | sheet:选择共同素材 | http://127.0.0.1:8765/pages/m08-p10.html?id=book-state&page=page-state | 669 |
| m08-p10 | 照片 3 · 裁剪或替换 | sheet:选择共同素材 | http://127.0.0.1:8765/pages/m08-p10.html?id=book-state&page=page-state | 670 |
| m08-p10 | 这一页的想法 | input | http://127.0.0.1:8765/pages/m08-p10.html?id=book-state&page=page-state | 671 |
| m08-p10 | 添加照片 | sheet:选择共同素材 | http://127.0.0.1:8765/pages/m08-p10.html?id=book-state&page=page-state | 672 |
| m08-p10 | 添加文字 | focus:这一页的想法 | http://127.0.0.1:8765/pages/m08-p10.html?id=book-state&page=page-state | 673 |
| m08-p10 | 添加贴纸 | sheet:选择贴纸 | http://127.0.0.1:8765/pages/m08-p10.html?id=book-state&page=page-state | 674 |
| m08-p10 | 保留草稿换模板 | stash | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state&draft=661d1798-e3ae-441b-9ae5-bdf2d97b0179&page=page-state&source=audit-photo&kind=photo | 675 |
| m08-p10 | 预览这一页 | modal:共同照片 | http://127.0.0.1:8765/pages/m08-p10.html?id=book-state&page=page-state | 676 |
| m08-p10 | 保存这一页 | page-save | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 677 |
| m08-p11 | 返回 | route:m08-p08 | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state | 678 |
| m08-p11 | 选择重要时刻 | sheet:选择共同素材 | http://127.0.0.1:8765/pages/m08-p11.html?id=book-state&page=page-state | 679 |
| m08-p11 | 书页标题 | input | http://127.0.0.1:8765/pages/m08-p11.html?id=book-state&page=page-state | 680 |
| m08-p11 | 书页日期 | input | http://127.0.0.1:8765/pages/m08-p11.html?id=book-state&page=page-state | 681 |
| m08-p11 | 更换照片 | sheet:选择共同素材 | http://127.0.0.1:8765/pages/m08-p11.html?id=book-state&page=page-state | 682 |
| m08-p11 | 添加一句话 | sheet:一句话 | http://127.0.0.1:8765/pages/m08-p11.html?id=book-state&page=page-state | 683 |
| m08-p11 | 保存这一页 | page-save | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 684 |
| m08-p11 | 保留草稿换模板 | stash | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state&draft=8a11f397-a8cb-4e80-aeec-8750e5c7ea1b&page=page-state&source=audit-moment&kind=moment | 685 |
| m08-p12 | 返回 | route:m08-p08 | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state | 686 |
| m08-p12 | 工坊作品 | sheet:选择共同素材 | http://127.0.0.1:8765/pages/m08-p12.html?id=book-state&page=page-state | 687 |
| m08-p12 | 宠物成长 | tab | http://127.0.0.1:8765/pages/m08-p12.html?id=book-state&page=page-state | 688 |
| m08-p12 | 成长说明 | input | http://127.0.0.1:8765/pages/m08-p12.html?id=book-state&page=page-state | 689 |
| m08-p12 | 换内容 | sheet:选择共同素材 | http://127.0.0.1:8765/pages/m08-p12.html?id=book-state&page=page-state | 690 |
| m08-p12 | 换照片 | sheet:选择共同素材 | http://127.0.0.1:8765/pages/m08-p12.html?id=book-state&page=page-state | 691 |
| m08-p12 | 添加说明 | focus:成长说明 | http://127.0.0.1:8765/pages/m08-p12.html?id=book-state&page=page-state | 692 |
| m08-p12 | 保存这一页 | page-save | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 693 |
| m08-p12 | 保留草稿换模板 | stash | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state&draft=59d533e8-4609-4f79-bc16-6b0044eeb5df&page=page-state&source=audit-pet%3Aaudit-story&kind=pet | 694 |
| m08-p13 | 返回 | route:m08-p06 | http://127.0.0.1:8765/pages/m08-p06.html?id=book-state | 695 |
| m08-p13 | 保存排列 | structure-save | http://127.0.0.1:8765/pages/m08-p14.html?id=book-state | 696 |
| m08-p13 | 章节操作「第一章」 | sheet:第一章 · 章节操作 | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 697 |
| m08-p13 | 共同日记 | route:m08-p09?id=book-state&page=page-state | http://127.0.0.1:8765/pages/m08-p09.html?id=book-state&page=page-state | 698 |
| m08-p13 | 页面操作「共同日记」 | sheet:共同日记 · 页面操作 | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 699 |
| m08-p13 | 共同照片 | route:m08-p10?id=book-state&page=page-second | http://127.0.0.1:8765/pages/m08-p10.html?id=book-state&page=page-second | 700 |
| m08-p13 | 页面操作「共同照片」 | sheet:共同照片 · 页面操作 | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 701 |
| m08-p13 | 章节操作「第二章」 | sheet:第二章 · 章节操作 | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 702 |
| m08-p13 | 共同重要时刻 | route:m08-p11?id=book-state&page=page-third | http://127.0.0.1:8765/pages/m08-p11.html?id=book-state&page=page-third | 703 |
| m08-p13 | 页面操作「共同重要时刻」 | sheet:共同重要时刻 · 页面操作 | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 704 |
| m08-p13 | ＋ 添加回忆 | route:m08-p08 | http://127.0.0.1:8765/pages/m08-p08.html?id=book-state | 705 |
| m08-p13 | 新增章节 | sheet:章节 | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 706 |
| m08-p14 | 返回 | route:m08-p01 | http://127.0.0.1:8765/pages/m08-p01.html?id=book-state | 707 |
| m08-p14 | 开始翻阅 | route:m08-p15 | http://127.0.0.1:8765/pages/m08-p15.html?id=book-state | 708 |
| m08-p14 | 继续整理 | route:m08-p13 | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 709 |
| m08-p15 | 返回 | route:m08-p01 | http://127.0.0.1:8765/pages/m08-p01.html | 710 |
| m08-p15 | 管理这本回忆册 | route:m08-p21 | http://127.0.0.1:8765/pages/m08-p21.html?id=book-state | 711 |
| m08-p15 | 共同日记 | read-route:m08-p16?id=book-state&page=page-state | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-state&offset=0&block=0 | 712 |
| m08-p15 | 共同照片 | read-route:m08-p16?id=book-state&page=page-second | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-second&offset=0&block=0 | 713 |
| m08-p15 | 共同重要时刻 | read-route:m08-p16?id=book-state&page=page-third | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-third&offset=0&block=0 | 714 |
| m08-p15 | 从第一页翻阅 | read-route:m08-p16?id=book-state&page=page-state | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-state&offset=0&block=0 | 715 |
| m08-p16 | ‹ 书架 | route:m08-p01 | http://127.0.0.1:8765/pages/m08-p01.html | 716 |
| m08-p16 | 阅读设置与工具 | sheet:阅读设置与工具 | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-second&offset=0&block=0 | 717 |
| m08-p16 | 放大照片 | modal:共同回忆照片 | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-second&offset=0&block=0 | 718 |
| m08-p16 | 查看原始共同记录 | route:m03-p12?id=audit-photo | http://127.0.0.1:8765/pages/m03-p12.html?id=audit-photo | 719 |
| m08-p16 | 上一页 | reader-prev | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-state&offset=0&block=0 | 720 |
| m08-p16 | 当前第 2 / 3 页，打开目录 | sheet:回忆册目录 | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-second&offset=0&block=0 | 721 |
| m08-p16 | 下一页 | reader-next | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-third&offset=0&block=0 | 722 |
| m08-p16 | ☷ 目录 | sheet:回忆册目录 | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-second&offset=0&block=0 | 723 |
| m08-p16 | ♧ 书签 | bookmark | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-second&offset=0&block=0 | 724 |
| m08-p16 | ＋ 留一张补页 | route:m08-p18?id=book-state&page=page-second | http://127.0.0.1:8765/pages/m08-p18.html?id=book-state&page=page-second | 725 |
| m08-p17 | 返回 | read-route:m08-p16 | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-second&offset=0&block=0 | 726 |
| m08-p17 | 全书目录 | route:m08-p15 | http://127.0.0.1:8765/pages/m08-p15.html?id=book-state | 727 |
| m08-p17 | 我的书签 | sheet:我的书签 | http://127.0.0.1:8765/pages/m08-p17.html?id=book-state&page=page-second | 728 |
| m08-p17 | 添加补页 | route:m08-p18 | http://127.0.0.1:8765/pages/m08-p18.html?id=book-state&page=page-second | 729 |
| m08-p17 | 整理书页 | route:m08-p13 | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 730 |
| m08-p17 | 管理这本书 · 书名、归档、导出与删除 | route:m08-p21 | http://127.0.0.1:8765/pages/m08-p21.html?id=book-state | 731 |
| m08-p18 | 返回 | read-route:m08-p16 | http://127.0.0.1:8765/pages/m08-p16.html?id=book-state&page=page-second&offset=0&block=0 | 732 |
| m08-p18 | 查看目录 | route:m08-p15 | http://127.0.0.1:8765/pages/m08-p15.html?id=book-state | 733 |
| m08-p18 | 写几句话 | pressed | http://127.0.0.1:8765/pages/m08-p18.html?id=book-state&page=page-second | 734 |
| m08-p18 | 送一个表情 | pressed | http://127.0.0.1:8765/pages/m08-p18.html?id=book-state&page=page-second | 735 |
| m08-p18 | 附上一张照片 | pressed | http://127.0.0.1:8765/pages/m08-p18.html?id=book-state&page=page-second | 736 |
| m08-p18 | 下一步 · 写补页 | route:m08-p19?id=book-state&page=page-second&kind=写几句话 | http://127.0.0.1:8765/pages/m08-p19.html?id=book-state&page=page-second&kind=%E5%86%99%E5%87%A0%E5%8F%A5%E8%AF%9D | 737 |
| m08-p19 | 返回 | route:m08-p18 | http://127.0.0.1:8765/pages/m08-p18.html?id=book-state&page=page-second | 738 |
| m08-p19 | 补页文字 | input | http://127.0.0.1:8765/pages/m08-p19.html?id=book-state&page=page-second | 739 |
| m08-p19 | 爱心 | pressed | http://127.0.0.1:8765/pages/m08-p19.html?id=book-state&page=page-second | 740 |
| m08-p19 | 星星 | pressed | http://127.0.0.1:8765/pages/m08-p19.html?id=book-state&page=page-second | 741 |
| m08-p19 | 微笑 | pressed | http://127.0.0.1:8765/pages/m08-p19.html?id=book-state&page=page-second | 742 |
| m08-p19 | 花朵 | pressed | http://127.0.0.1:8765/pages/m08-p19.html?id=book-state&page=page-second | 743 |
| m08-p19 | 补页照片 | file | http://127.0.0.1:8765/pages/m08-p19.html?id=book-state&page=page-second | 744 |
| m08-p19 | 放入回忆书 | supplement | http://127.0.0.1:8765/pages/m08-p20.html?id=book-state&page=page-second | 745 |
| m08-p20 | 取消 | close-supplements | http://127.0.0.1:8765/pages/m08-p20.html?id=book-state&page=page-second&offset=0&block=0 | 753 |
| m08-p21 | 返回 | route:m08-p15 | http://127.0.0.1:8765/pages/m08-p15.html?id=book-state | 746 |
| m08-p21 | 修改书名 | sheet:书名 | http://127.0.0.1:8765/pages/m08-p21.html?id=book-state | 747 |
| m08-p21 | 整理页序 | route:m08-p13 | http://127.0.0.1:8765/pages/m08-p13.html?id=book-state | 748 |
| m08-p21 | 修改主题与封面 | route:m08-p05?id=book-state&origin=manage | http://127.0.0.1:8765/pages/m08-p05.html?id=book-state&origin=manage | 749 |
| m08-p21 | 归档回忆册 | archive | http://127.0.0.1:8765/pages/m08-p21.html?id=book-state | 750 |
| m08-p21 | 删除这本回忆册 | modal:确定删除《共同测试册》？ | http://127.0.0.1:8765/pages/m08-p21.html?id=book-state | 751 |
| m08-p21 | 导出这本回忆册 | export | http://127.0.0.1:8765/pages/m08-p21.html?id=book-state | 752 |

原隐藏250控件及回忆册V2106次控件出现的对应表保留执行版本，入口见BOOK_V2_HIDDEN_OUTCOMES。原控件正文及阶段说明在`evidence/history/pre-current-initial-catalog-8cce41c/CONTROL_BEHAVIORS.md`；不将其自动计入本轮新执行。
