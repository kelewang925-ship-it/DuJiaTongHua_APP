# 首页、日记与照片控件执行记录

源码指纹：`7c617d4b27dd30960fd8177b5a9a96ff1e03081c23ccd7105190b304816395f9`。12页各一个声明fixture的全部92个初始可用控件；不代表全部数据前置条件或114页最终验收。原始节点、label、selector、契约及结果见evidence/current/record-controls-results.json。

| 页面/场景 | 控件 | 实际契约 | 结果 |
| --- | --- | --- | --- |
| m03-p01/empty | 搜索共同记录 | route:m03-p03 | 通过 |
| m03-p01/empty | 写日记 | route:m03-p05 | 通过 |
| m03-p01/empty | 添加照片 | route:m03-p11 | 通过 |
| m03-p01/empty | 去童话工坊，把回忆变成故事 › | route:m05-p01 | 通过 |
| m03-p01/empty | 首页 | nav:self | 通过 |
| m03-p01/empty | 重要时刻 | nav:m04-p02 | 通过 |
| m03-p01/empty | 工坊 | nav:m05-p01 | 通过 |
| m03-p01/empty | 宠物 | nav:pet | 通过 |
| m03-p01/empty | 我的 | nav:m06-p01 | 通过 |
| m03-p02/populated | 搜索共同记录 | route:m03-p03 | 通过 |
| m03-p02/populated | 写日记 / 记录心情 | route:m03-p05 | 通过 |
| m03-p02/populated | 添加照片 / 珍藏瞬间 | route:m03-p11 | 通过 |
| m03-p02/populated | 去童话工坊，把回忆变成故事 › | route:m05-p01 | 通过 |
| m03-p02/populated | 查看全部 › | route:m03-p06 | 通过 |
| m03-p02/populated | 共同日记 / 小满 · 共同可见 | route:m03-p08 | 通过 |
| m03-p02/populated | 自己的日记 / 小满 · 仅自己可见 | route:m03-p07 | 通过 |
| m03-p02/populated | 共同照片 / 小满 · 共同可见 | route:m03-p12 | 通过 |
| m03-p02/populated | 共同测试册 / 从目录开始阅读 / 继续阅读 › | route:m08-p15 | 通过 |
| m03-p02/populated | 下一件重要时刻 / 未来的纪念日 · 79 天后 / 查看纪念日 › | route:m04-p10 | 通过 |
| m03-p02/populated | 首页 | nav:self | 通过 |
| m03-p02/populated | 重要时刻 | nav:m04-p01 | 通过 |
| m03-p02/populated | 工坊 | nav:m05-p01 | 通过 |
| m03-p02/populated | 宠物 | nav:pet | 通过 |
| m03-p02/populated | 我的 | nav:m06-p01 | 通过 |
| m03-p03/empty | 返回首页 | route:m03-p01 | 通过 |
| m03-p03/empty | 搜索关键词 | query | 通过 |
| m03-p03/empty | 清除搜索 | clear-query | 通过 |
| m03-p03/empty | 晚霞 | search-chip:晚霞 | 通过 |
| m03-p03/empty | 火锅 | search-chip:火锅 | 通过 |
| m03-p03/empty | 旅行 | search-chip:旅行 | 通过 |
| m03-p03/empty | 日记 | search-chip:日记 | 通过 |
| m03-p03/empty | 照片 | search-chip:照片 | 通过 |
| m03-p03/empty | 旅行 | search-chip:旅行 | 通过 |
| m03-p03/empty | 纪念日 | search-chip:纪念日 | 通过 |
| m03-p04/populated | 返回搜索 | route:m03-p03 | 通过 |
| m03-p04/populated | 搜索关键词 | query | 通过 |
| m03-p04/populated | 清除 | clear-query | 通过 |
| m03-p04/populated | 共同日记 /  / 真正可编辑的共同正文 /  / 共同可见 | route:m03-p08 | 通过 |
| m03-p04/populated | 共同照片 /  / 共同照片说明 /  / 共同可见 | route:m03-p12 | 通过 |
| m03-p05/empty | 返回日记列表 | route:m03-p06 | 通过 |
| m03-p05/empty | 存草稿 | diary-draft | 通过 |
| m03-p05/empty | 日记标题 | input | 通过 |
| m03-p05/empty | 今天的心情 | mood | 通过 |
| m03-p05/empty | 日记正文 | input | 通过 |
| m03-p05/empty | 添加照片 | file | 通过 |
| m03-p05/empty | visibility | input | 通过 |
| m03-p05/empty | visibility | input | 通过 |
| m03-p05/empty | 保存日记 | diary-save | 通过 |
| m03-p06/populated | 返回首页 | route:m03-p02 | 通过 |
| m03-p06/populated | 筛选日记 | sheet:筛选日记 | 通过 |
| m03-p06/populated | 全部 | tab:all | 通过 |
| m03-p06/populated | 草稿 0 | tab:draft | 通过 |
| m03-p06/populated | 写日记 | route:m03-p05 | 通过 |
| m03-p06/populated | 共同日记 /  / 真正可编辑的共同正文 /  / 小满 · 2026/10/4 · 共同可见 | route:m03-p08 | 通过 |
| m03-p06/populated | 自己的日记 /  / 独立私密正文 /  / 小满 · 2026/10/4 · 仅自己可见 | route:m03-p07 | 通过 |
| m03-p06/populated | 刷新日记 | refresh:diary | 通过 |
| m03-p07/populated | 返回日记列表 | route:m03-p06 | 通过 |
| m03-p07/populated | 编辑日记 | route:m03-p05 | 通过 |
| m03-p07/populated | 更多操作 | sheet:日记操作 | 通过 |
| m03-p08/populated | 返回日记列表 | route:m03-p06 | 通过 |
| m03-p08/populated | 编辑日记 | route:m03-p05 | 通过 |
| m03-p08/populated | 给 TA 留一句话 | input | 通过 |
| m03-p08/populated | 添加表情 | emoji | 通过 |
| m03-p08/populated | 发送留言 | reply | 通过 |
| m03-p08/populated | 更多操作 | sheet:日记操作 | 通过 |
| m03-p09/empty | 返回首页 | route:m03-p01 | 通过 |
| m03-p09/empty | 添加第一张照片 | route:m03-p11 | 通过 |
| m03-p09/empty | 从系统相册选择 | route:m03-p11 | 通过 |
| m03-p10/populated | 返回首页 | route:m03-p02 | 通过 |
| m03-p10/populated | 筛选照片 | sheet:筛选照片 | 通过 |
| m03-p10/populated | 全部 | tab:all | 通过 |
| m03-p10/populated | 共同可见 | tab:shared | 通过 |
| m03-p10/populated | 旅行 | tab:travel | 通过 |
| m03-p10/populated | 共同照片 | route:m03-p12 | 通过 |
| m03-p10/populated | ＋ 添加照片 | route:m03-p11 | 通过 |
| m03-p10/populated | 刷新相册 | refresh:photo | 通过 |
| m03-p11/empty | 返回相册 | route:m03-p09 | 通过 |
| m03-p11/empty | 完成 | photo-save | 通过 |
| m03-p11/empty | 选择照片 | file | 通过 |
| m03-p11/empty | 照片心情 | input | 通过 |
| m03-p11/empty | 照片日期 | sheet:选择照片日期 | 通过 |
| m03-p11/empty | 照片标签 | input | 通过 |
| m03-p11/empty | 添加标签 | sheet:照片标签 | 通过 |
| m03-p11/empty | visibility | input | 通过 |
| m03-p11/empty | visibility | input | 通过 |
| m03-p11/empty | 保存照片 | photo-save | 通过 |
| m03-p12/populated | 返回照片相册 | route:m03-p10 | 通过 |
| m03-p12/populated | 编辑照片 | route:m03-p11 | 通过 |
| m03-p12/populated | 给 TA 留一句话 | input | 通过 |
| m03-p12/populated | 添加表情 | emoji | 通过 |
| m03-p12/populated | 发送留言 | reply | 通过 |
| m03-p12/populated | 更多操作 | sheet:照片操作 | 通过 |

契约说明：route/navigation实际进入目标或条件redirect；当前主Tab滚回顶部；input/query/mood校验输入长度、选择和focus；file触发系统文件选择并实际预览；diary-draft/save及photo-save持久化后回列表；reply实际追加回应、清空并可离开；emoji追加表情且聚焦；sheet验证标题、关闭及焦点回到入口；tab筛选/草稿有可用空态；refresh显示区域busy并恢复列表；search-chip实际搜索并保存历史；clear-query清空且回到可继续输入的搜索入口。

## 修复与隐藏分支

日记和照片未发送回应离开时使用现有guard确认继续/放弃；成功发送后清空并commit，失败保留输入和存储，照片成功增加共享Toast。回应隐私关闭时禁用表情。日记列表/详情对缺少createdAt但有date的有效记录用date回退，解析失败显示日期未记录。照片心情caption参与搜索与结果摘要；结果清除搜索后入口聚焦。日记编辑器返回aria-label改为实际日记列表。共享浏览器返回在确认前恢复guard节点，防止选择继续后快速再次返回的空窗；6项重复返回专项每项连续继续3次，最后确认放弃。

隐藏检查：两类删除取消/失败/重试及保存其他记录；两类回应失败保留/重试并干净返回；两类筛选应用/清除；照片日期与标签回填/取消和dirty；搜索失败重试；日记照片添加后移除。四种未发送回应返回检查、两种关闭回应权限、有效日期回退、实际输入caption搜索另列。320/360/390/414/430px每类回应确认各一次，共10项，检查44px热区、安全区、继续后300字仍保留。

## 证据与边界

baseline/record-controls-results.json保留原源码8项失败（四种丢失输入、两个权限表情仍可用、日期显示Invalid Date、caption遗漏搜索）。baseline/record-search-focus-results.json记录随后逐控件执行的焦点缺口；probe手动观察焦点在body，修复后全组重跑。随后record-overlay-and-back-race-results.json包含两个同名selector观察器错误和两个实际快速返回竞态，分别修正选择器与共享guard；原始诊断保留。record-reentry-dialog-expectation与record-reentry-close-expectation记录修复后仅留在当前页/再次显示确认的合法时序被观察器误判；最终快速返回专项验证输入和页面不丢、允许新确认、稳定后仍能确认离开。共享返回变更后重新执行时刻6页53项控件/隐藏操作和8条账号/关系流程；原完整时刻67项及旧账号82+14汇总仍保持阶段来源。此前全114页扫描属于aed142d。

本批195项通过并检查114页/37共享资产HTTP与工作区一致。其余79页初始控件契约、已覆盖页全部动态分支/记录结构与引用、所有设计组件/布局条件、跨模块连续流程仍开放；114页最终验收0。Android式返回为浏览器历史模拟，不是原生Android设备验收。
