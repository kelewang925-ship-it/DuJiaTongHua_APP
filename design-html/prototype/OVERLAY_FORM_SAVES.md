# 已观察保存表单的结果与失败恢复

16个入口、47项当前执行：16成功、16定向本地空间失败后重试、15空值拒绝（固定动效Select无空值选项）。检查提交loading/disabled、两次快速DOM激活、输入保持与明确存储结果谓词。空值测试只证明首错，不代替逐字段所有校验。

14个表单直接持久化；寄语／章节先回填候选，父页面保存才写入。QuotaExceededError仅在测试上下文针对目标localStorage键抛一次；生产函数未替换。未声称所有网络／权限／失效失败已覆盖。

| 观察索引／页面 | 表单 | 声明有效输入 | 写入方式／键 | 当前项数 | 剩余 |
| --- | --- | --- | --- | ---: | --- |
| 17 / m04-p03 | 时刻回应 | 回应这个时刻=弹层保存测试 | 直接持久化 / dujia-prototype-moments | 3 | other fields/validation conditions, semantic operation failures, submission cancellation, sources and layouts |
| 42 / m06-p03 | 共同昵称 | 共同昵称=弹层保存测试 | 直接持久化 / dujia-prototype-relationship | 3 | other fields/validation conditions, semantic operation failures, submission cancellation, sources and layouts |
| 45 / m06-p05 | 新建标签 | 标签名称=保存标签45；标签范围=personal | 直接持久化 / dujia-prototype-tags | 3 | other fields/validation conditions, semantic operation failures, submission cancellation, sources and layouts |
| 46 / m06-p05 | 新建标签 | 标签名称=保存标签46；标签范围=personal | 直接持久化 / dujia-prototype-tags | 3 | other fields/validation conditions, semantic operation failures, submission cancellation, sources and layouts |
| 52 / m06-p07 | 显示与外观 | 动效=reduce | 直接持久化 / dujia-prototype-preferences | 2 | other fields/validation conditions, semantic operation failures, submission cancellation, sources and layouts |
| 55 / m06-p08 | 绑定手机（本地演示） | 手机号=13987654321；演示验证码 284631=284631 | 直接持久化 / dujia-prototype-session | 3 | other fields/validation conditions, semantic operation failures, submission cancellation, sources and layouts |
| 57 / m06-p08 | 开启两步验证演示 | 演示验证码 284631=284631 | 直接持久化 / dujia-prototype-preferences | 3 | other fields/validation conditions, semantic operation failures, submission cancellation, sources and layouts |
| 64 / m06-p12 | 意见反馈 | 意见反馈=弹层保存测试 | 直接持久化 / dujia-feedback-draft | 3 | other fields/validation conditions, semantic operation failures, submission cancellation, sources and layouts |
| 72 / m07-p11 | 宠物小心情 | 今天的小心情=弹层保存测试 | 直接持久化 / dujia-prototype-pet | 3 | other fields/validation conditions, semantic operation failures, submission cancellation, sources and layouts |
| 82 / m07-p18 | 成长故事 | 成长故事内容=弹层保存测试 | 直接持久化 / dujia-prototype-pet | 3 | other fields/validation conditions, semantic operation failures, submission cancellation, sources and layouts |
| 84 / m07-p19 | 成长故事 | 成长故事内容=弹层保存测试 | 直接持久化 / dujia-prototype-pet | 3 | other fields/validation conditions, semantic operation failures, submission cancellation, sources and layouts |
| 85 / m07-p19 | 回应 | 回应内容=弹层保存测试 | 直接持久化 / dujia-prototype-pet | 3 | other fields/validation conditions, semantic operation failures, submission cancellation, sources and layouts |
| 97 / m07-p25 | 提醒时间 | 每天提醒时间=21:45 | 直接持久化 / dujia-prototype-pet | 3 | other fields/validation conditions, semantic operation failures, submission cancellation, sources and layouts |
| 118 / m08-p11 | 一句话 | 书页寄语=弹层保存测试 | 候选→父页保存 / dujia-prototype-books | 3 | other fields/validation conditions, semantic operation failures, submission cancellation, sources and layouts |
| 122 / m08-p13 | 章节 | 章节名=弹层保存测试 | 候选→父页保存 / dujia-prototype-books | 3 | other fields/validation conditions, semantic operation failures, submission cancellation, sources and layouts |
| 129 / m08-p21 | 书名 | 回忆册名称=弹层保存测试 | 直接持久化 / dujia-prototype-books | 3 | other fields/validation conditions, semantic operation failures, submission cancellation, sources and layouts |
