# 童话工坊控件执行

当前共享源码已加入工坊作品恢复；本文件保留此前阶段范围与结果，不能替代最新全产品终验。当前247项及同源证据见[WORKSHOP_RECOVERY_IMPLEMENTATION](WORKSHOP_RECOVERY_IMPLEMENTATION.md)，此前被覆盖报告／图片保留evidence/history/pre-workshop-recovery-2651f8a，各文件保留原来源。

## 当前结果

m05-p01至p10十页声明fixture的92个初始可用控件全部按明确行为实际执行；12项隐藏检查、10项五宽度弹层检查、11项已有正常/异常流程回归，共125项通过。六个稳定作品ID覆盖漫画自由/照片/影片草稿、生成中、失败、影片完成；生成中初始控件fixture采用远期dueAt保证逐项检查不会自动离页，真实3秒生成及离开后完成由既有连续流程另行验证。所有测试在隔离浏览器context内运行。

## 实际修复

1. W.sources(moment)曾把私密/未发布时刻显示在共同素材Sheet中。添加与共同创作一致的visibility/private与status/draft过滤；已发布且没有可见性字段的历史正常时刻继续可用。baseline/workshop-hidden-results.json记录修复前私密时刻出现；修复后检查私密和草稿均不出现，共同时刻仍可选并能创建稳定作品。更广集合类型、语义与引用完整性仍开放。
2. 主角设定页已有work参数时实际回原创作，但返回按钮仍叫“返回童话工坊”。现在根据work是否存在显示“返回当前创作”或原工坊文字，导航逻辑与稳定ID保持一致。

## 隐藏分支与异常

12项检查包括：时刻素材权限1项，日记/照片/时刻/自由回忆四类实际选择并创建作品4项，漫画/照片/影片/主角四个编辑页浏览器返回继续/放弃4项，相册重复保存不重复1项，删除取消与实际删除仅移除目标1项，主角返回文字与原作品ID1项。既有11项重跑覆盖生成失败重试、保存失败/空间不足、主角保存、真实生成/离页完成/播放、素材图片/保存相册失败重试、deadline后取消确认、历史加载/删除失败、收藏及复制权限失败的手动复制入口。

320/360/390/414/430px，34px安全区下分别检查素材Sheet与300字未保存确认：弹层在屏内，按钮至少44px高，取消/继续不写入数据且保留正文。人工查看320px两张截图。实际软键盘、所有页面/状态视觉及全产品动效并未由这些检查覆盖。

## 观察器诊断

baseline/workshop-controls-observer-pet-route.json记录初轮92项中宠物目的地错误期望；bound关系且pet为空时正确入口为m07-p04（领养），已按当前业务规则修正契约。baseline/workshop-hidden-results.json另包含默认日记选项accessible name带CSS选中✓造成exact匹配失败的观察器问题，使用明确.option文本定位实际按钮；同文件两项产品缺口照常保留。baseline/workshop-layout-selector-diagnostic.json记录背景按钮和Sheet checkbox同名的strict匹配失败，修正为dialog内选择。旧工坊状态脚本恢复Storage方法时改为不返回函数，避免Illegal invocation观察器错误。

## 控件契约

| 页面 | 控件 | 实际契约 |
| --- | --- | --- |
| m05-p01 | 做成童话漫画 / 把回忆画成专属故事 / 留下一格格心动瞬间 | route:m05-p02 |
| m05-p01 | 制作回忆影片 / 让重要时刻动起来 / 在光影里重温感动 | new-film |
| m05-p01 | 查看全部 › | route:m05-p09 |
| m05-p01 | work-free / 草稿 | work:work-free |
| m05-p01 | work-photos / 草稿 | work:work-photos |
| m05-p01 | 开始一次创作 | route:m05-p02 |
| m05-p01 | 首页 | nav:m03-p02 |
| m05-p01 | 重要时刻 | nav:m04-p01 |
| m05-p01 | 工坊 | nav:self |
| m05-p01 | 宠物 | nav:m07-p04 |
| m05-p01 | 我的 | nav:m06-p01 |
| m05-p02 | 返回童话工坊 | route:m05-p01 |
| m05-p02 | 共同日记 | choice |
| m05-p02 | 相册照片 | choice |
| m05-p02 | 重要时刻 | choice |
| m05-p02 | 自由写一段回忆 | choice |
| m05-p02 | 用这些素材开始 | sheet:选择共同素材 |
| m05-p03 | 返回素材选择 | route:m05-p02 |
| m05-p03 | 回忆内容 | input |
| m05-p03 | 编辑 | focus-story |
| m05-p03 | 暖暖水彩 | setting |
| m05-p03 | 复古漫画 | setting |
| m05-p03 | 轻柔铅笔 | setting |
| m05-p03 | 温柔叙事 / 贴近日常，细腻温暖 | setting |
| m05-p03 | 电影感 / 光影氛围，节奏张力 | setting |
| m05-p03 | 默默 & 小满 / 可爱自然 · 清新温柔 | characters |
| m05-p03 | 生成童话漫画 | generate |
| m05-p03 | 暂存创作草稿 | draft |
| m05-p03 | 创作草稿操作 | sheet:创作操作 |
| m05-p04 | 返回素材选择 | route:m05-p02 |
| m05-p04 | 共同素材照片 | toggle-photo |
| m05-p04 | 补充这段故事 | input |
| m05-p04 | 水彩 | setting |
| m05-p04 | 素描 | setting |
| m05-p04 | 清新插画 | setting |
| m05-p04 | 油画 | setting |
| m05-p04 | 他  / 阳光温柔 | characters |
| m05-p04 | 她  / 温柔爱笑 | characters |
| m05-p04 | 生成童话漫画 | generate |
| m05-p04 | 暂存创作草稿 | draft |
| m05-p04 | 创作草稿操作 | sheet:创作操作 |
| m05-p04 | 选择照片 | sheet:选择共同素材 |
| m05-p05 | 返回工坊 | route:m05-p01 |
| m05-p05 | 选择共同片段 | sheet:片段类型 |
| m05-p05 | 移除片段 共同素材日记 | remove-clip |
| m05-p05 | 影片旁白 | input |
| m05-p05 | 试听演示音轨 | audio |
| m05-p05 | 温柔手帐 | setting |
| m05-p05 | 治愈暖光 | setting |
| m05-p05 | 清新自然 | setting |
| m05-p05 | 生成回忆影片 | generate |
| m05-p05 | 暂存创作草稿 | draft |
| m05-p05 | 创作草稿操作 | sheet:创作操作 |
| m05-p06 | 返回童话工坊 | route:m05-p01 |
| m05-p06 | 取消生成 | modal:取消这次生成？ |
| m05-p07 | 调整内容 | route:m05-p03 |
| m05-p07 | 重新生成 | generate |
| m05-p07 | 先回到童话工坊 ♡ | route:m05-p01 |
| m05-p08 | 返回我的创作 | route:m05-p09 |
| m05-p08 | 第1页 | frame:1 |
| m05-p08 | 第2页 | frame:2 |
| m05-p08 | 第3页 | frame:3 |
| m05-p08 | 第4页 | frame:4 |
| m05-p08 | 第5页 | frame:5 |
| m05-p08 | 第6页 | frame:6 |
| m05-p08 | 第7页 | frame:7 |
| m05-p08 | 第8页 | frame:8 |
| m05-p08 | 保存到共同相册 | album |
| m05-p08 | 给另一半看看 | sheet:给另一半看看 |
| m05-p08 | 重新生成 | route:m05-p05 |
| m05-p08 | 更多作品操作 | sheet:创作操作 |
| m05-p08 | 播放片段演示 | play |
| m05-p09 | 收藏夹 | favorites |
| m05-p09 | 全部 | tab:全部 |
| m05-p09 | 漫画 | tab:漫画 |
| m05-p09 | 影片 | tab:影片 |
| m05-p09 | 草稿 | tab:草稿 |
| m05-p09 | 开始创作 | route:m05-p02 |
| m05-p09 | work-free / 漫画 · 草稿 | work:work-free |
| m05-p09 | work-photos / 漫画 · 草稿 | work:work-photos |
| m05-p09 | work-film / 影片 · 草稿 | work:work-film |
| m05-p09 | work-running / 漫画 · 制作中 | work:work-running |
| m05-p09 | work-failed / 漫画 · 生成失败 | work:work-failed |
| m05-p09 | work-ready / 影片 · 已完成 | work:work-ready |
| m05-p09 | 返回童话工坊 | route:m05-p01 |
| m05-p09 | 刷新我的创作 | refresh |
| m05-p10 | 返回当前创作 | route:m05-p03 |
| m05-p10 | appearance | input |
| m05-p10 | outfit | input |
| m05-p10 | mood | input |
| m05-p10 | object | input |
| m05-p10 | 更新我们的主角 | save-characters |

## 来源与验收边界

源码指纹 `999935f305a6c475d644c8f7778cd2cf528c987629e2d2cf3a31a3d3b55b4a67`；125项报告严格绑定当前源码。114页与37共享资产HTTP字节一致，custom/pages一致。旧工坊报告与修复前本轮回归保存在evidence/history/pre-workshop-controls-56ce968；该文件夹命名为保留时HEAD，不等于旧测试来源。上一阶段纪念日/胶囊99项与更早记录195项保持原源码指纹，本轮没有累计为当前全产品通过。

已建初始控件契约累计56页，余下58页继续逐项执行。所有页面动态条件/其他集合恢复/引用完整性、完整跨模块连续使用、全部组件/视觉/动效与键盘状态仍需推进；114页最终验收0，目标继续。Android式返回是浏览器历史模拟。
