# 《独家童话》Codex 页面验收测试提示词

> 用途：用于让 Codex 对当前项目页面进行一次系统验收。  
> 测试重点：页面覆盖度、功能可用性、交互闭环、设计方向一致性。  
> 重要限制：当前项目尚未完成“真实图片资源首批替换”，所以本次测试不要求页面中的 AI 配图完全等同 `assets/design/png` 效果图，只检查是否使用了正确的视觉方向、组件体系和图片接入入口。

---

## 1. Codex 可直接复制提示词

```text
请对当前仓库项目 kelewang925-ship-it/DuJiaTongHua_APP 进行一次页面验收测试。

项目名称：《独家童话》
技术栈：React Native + Expo + Expo Router + Zustand + JavaScript
视觉方向：童话绘本、奶油纸感、桃粉、干玫瑰、可可棕、琥珀金、手绘图标、贴纸式组件。

请先读取并理解这些文档：

1. docs/project-file-structure.md
2. docs/pending-interfaces-implementation-plan.md
3. docs/next-chat-handoff-prompt.md
4. docs/visual-audit-and-next-steps.md
5. docs/image-assets-guideline.md
6. docs/image-assets-implementation-plan.md
7. docs/《独家童话》Design System v1.0.md
8. docs/《独家童话》UI设计总方向.md

请参考以下效果图作为设计方向参考：

1. assets/design/png/界面设计图.png
2. assets/design/png/界面设计图2.png
3. assets/design/png/界面设计风格图-2.png

注意：当前项目还没有完成“真实图片资源首批替换”，所以本次不要以“页面插画是否完全等于效果图”为验收标准。只检查：

- 是否使用 FairyImage 作为统一图片入口；
- 是否没有直接把整张效果图塞进页面；
- 页面整体是否遵循童话绘本、奶油纸感、桃粉、干玫瑰、可可棕、琥珀金、贴纸卡片的方向；
- 功能和页面使用程度是否达到 mock MVP 验收标准。

请按以下范围进行验收。

一、启动与基础检查

1. 安装依赖并启动项目：

   npm install
   npx expo start

2. 检查是否有明显编译错误、红屏、缺失模块、路径错误。
3. 检查 Expo Router 路由是否能正常进入主要页面。
4. 如果无法运行，请先定位报错文件和报错原因，不要直接大规模重构。

二、主 Tab 页面验收

请检查：

1. 首页：app/(tabs)/index.js
   - 是否展示恋爱天数；
   - 是否展示快捷入口：写日记、传照片、童话工坊；
   - 是否展示 MemoryWall 回忆碎片墙；
   - 点击日记记录是否进入日记详情；
   - 点击照片记录是否进入相册；
   - 是否使用 FairyImage homeCover；
   - 整体是否接近童话绘本/贴纸拼贴方向。

2. 情侣空间：app/(tabs)/couple.js
   - 是否展示情侣资料；
   - 是否展示互动入口；
   - 是否展示 CoupleTimeline 手绘时间轴；
   - 是否使用 FairyImage coupleCover；
   - 时间轴视觉是否有章节感、贴纸感、手绘故事线方向。

3. 童话工坊：app/(tabs)/workshop.js
   - 是否展示 AI 漫画和回忆视频入口；
   - 是否展示创作历史；
   - 是否使用 FairyImage workshopCover；
   - 是否体现 AI 魔法工坊而不是科技工具风。

4. 我的：app/(tabs)/mine.js
   - 是否展示用户资料；
   - 是否展示日记、照片、作品统计；
   - 是否能进入纪念日、备份、PDF导出、设置等入口。

三、核心记录功能验收

1. 日记编辑页：app/diary/editor.js
   - 标题输入是否可用；
   - 正文输入是否可用；
   - 心情标签选择是否可用；
   - 保存后是否回到首页；
   - 首页 records 是否新增日记；
   - 情侣空间 timeline 是否新增动态。

2. 日记详情页：app/diary/detail.js
   - 是否展示最近日记；
   - 是否展示标题、日期、标签、正文；
   - 是否能跳转文本转漫画。

3. 照片上传页：app/photo/upload.js
   - 照片标题输入是否可用；
   - 备注输入是否可用；
   - 标签选择是否可用；
   - 模拟照片数量选择是否可用；
   - 保存后首页和相册是否更新。

4. 相册页：app/photo/album.js
   - 是否读取照片记录；
   - 网格/时间线切换是否可用；
   - 无照片时是否有 FairyEmptyState。

四、AI 创作功能验收

1. 漫画配置页：app/ai/comic-config.js
   - 是否可输入作品名；
   - 是否可选择素材和风格；
   - 点击生成是否调用 addCreation 并进入进度页。

2. 文本转漫画页：app/ai/text-to-comic.js
   - 是否默认读取最近日记内容；
   - 是否可编辑文本；
   - 是否可选择风格；
   - 点击生成是否进入进度页。

3. 照片转漫画页：app/ai/photo-to-comic.js
   - 是否读取照片记录；
   - 是否可选择照片组；
   - 是否可输入作品名；
   - 是否可选择风格；
   - 无照片时是否引导上传照片；
   - 点击生成是否进入进度页并更新创作历史。

4. 视频配置页：app/ai/video-config.js
   - 是否可选择音乐和时长；
   - 点击生成是否进入进度页并更新创作历史。

5. 生成进度页：app/ai/progress.js
   - 是否展示最新 creation；
   - 是否展示进度、步骤和跳转按钮。

6. 视频预览页：app/ai/video-preview.js
   - 是否展示最新视频或 AI 作品；
   - 是否展示 mock 播放器、时间线、编辑项。

五、情侣互动功能验收

1. 情侣动态详情页：app/couple/activity-detail.js
   - 是否读取 timeline 最近动态；
   - 是否展示标题、时间、描述、标签；
   - 是否展示关联记录和 AI 作品；
   - 评论入口是否能进入评论页；
   - 生成漫画入口是否能进入文本转漫画页。

2. 评论列表页：app/comments/index.js
   - 初始评论是否展示；
   - 评论输入是否可用；
   - 发送后是否追加评论；
   - 空输入是否不发送；
   - 卡片视觉是否统一。

3. 互动通知页：app/notifications/index.js
   - 是否展示通知列表；
   - 是否有点赞、评论、AI、纪念日、系统等类型；
   - 类型筛选是否可用；
   - 已读/未读状态是否可见；
   - 点击通知是否有合理跳转或 mock 行为。

六、纪念日与管理功能验收

1. 纪念日管理页：app/anniversary/index.js
   - 是否展示纪念日列表；
   - 是否可新增纪念日；
   - 新增后是否进入列表；
   - 是否同步情侣空间动态。

2. 标签管理页：app/tags/index.js
   - 是否从 records 中统计 tags；
   - 是否展示使用次数；
   - 是否支持新增 mock 标签；
   - 是否支持点击标签筛选相关记录。

3. 时光胶囊设置页：app/time-capsule/settings.js
   - 是否可创建 mock 胶囊；
   - 是否可填写标题、说明、解锁日期；
   - 是否可选择封存内容类型；
   - 胶囊列表是否展示。

七、数据管理功能验收

1. 数据备份页：app/data/backup.js
   - 是否展示日记、照片、AI作品统计；
   - 备份/恢复按钮是否存在；
   - 是否有合理 mock 状态。

2. PDF导出配置页：app/data/pdf-export.js
   - 是否展示导出范围；
   - 是否展示绘本样式；
   - 是否能进入或关联导出预览。

3. 导出预览页：app/data/export-preview.js
   - 是否展示 PDF 封面；
   - 是否展示章节目录；
   - 是否展示 mock 页数、导出范围、样式；
   - 确认导出按钮是否有 mock 反馈。

4. 存储空间管理页：app/data/storage.js
   - 是否展示总用量；
   - 是否展示照片、AI作品、PDF导出、缓存分类；
   - 是否有进度条或占比展示；
   - 清理缓存 mock 操作是否可用。

八、搜索功能验收

文件：app/search.js

请检查：

- 是否支持关键词搜索；
- 是否支持类型筛选：全部、日记、照片、AI、纪念日、动态；
- 是否搜索 records、creations、anniversaries、timeline；
- 空结果是否有 FairyEmptyState；
- 点击结果是否跳转对应页面。

九、文档验收

请检查这些文档是否存在且内容完整：

1. docs/project-file-structure.md
2. docs/pending-interfaces-implementation-plan.md
3. docs/next-chat-handoff-prompt.md
4. docs/image-assets-guideline.md
5. docs/image-assets-implementation-plan.md
6. docs/visual-audit-and-next-steps.md

如果发现文档缺失或仍是占位，请补全。

十、本次验收不包含

本次不要验收以下内容：

- 真实后端 API；
- 真实 AI 服务；
- 真实 PDF 文件生成；
- 真实系统相册上传；
- 真实用户登录；
- 真实图片资源首批替换；
- 与效果图逐像素一致。

本次只验收：

- 路由是否覆盖；
- 页面是否可打开；
- mock 功能是否可用；
- 状态流转是否合理；
- 组件使用是否符合 Design System；
- 视觉方向是否参考 assets/design/png 中的效果图。

十一、请输出验收结果

完成验收后，请按以下格式输出：

1. 测试环境

- 使用的启动命令；
- 是否安装依赖；
- 是否成功启动；
- 如未启动，具体报错。

2. 通过项

按模块列出通过内容：

- 主 Tab；
- 记录；
- AI创作；
- 情侣互动；
- 纪念日；
- 数据管理；
- 搜索；
- 文档。

3. 问题清单

用表格输出：

| 严重级别 | 文件 | 问题 | 复现方式 | 建议修复 |
| --- | --- | --- | --- | --- |

严重级别分为：

- P0：阻塞运行 / 红屏 / 路由打不开；
- P1：核心流程不可用；
- P2：交互或视觉明显不一致；
- P3：文案、细节、优化项。

4. 是否符合本次验收范围

请明确回答：

- 页面覆盖度是否达标；
- 功能使用程度是否达标；
- 设计方向是否基本达标；
- 是否因为真实图片资源未替换而影响本次验收。

注意：真实图片资源未替换不应判定为本次失败，只记录为后续待办。

5. 建议下一步

请基于测试结果给出下一步建议，优先级可以包括：

- 修复 P0/P1 问题；
- 接入真实图片资源首批替换；
- 接入 Zustand persist；
- 完善登录/绑定流程；
- 完善纪念日编辑、AI结果详情、分享预览、会员页；
- 增加基础自动化测试。
```

---

## 2. 本次验收原则

本次验收只做“功能和使用程度方向”验收。

因为当前项目还未完成：

```text
真实图片资源首批替换
```

所以：

- 不要求页面内插画与效果图完全一致；
- 不要求 AI 配图已经真实切入；
- 不做逐像素对比；
- 不把 `FairyImage` fallback 视为失败。

但仍需要检查：

- 是否保留 `FairyImage` 统一入口；
- 是否没有直接把整张效果图塞进页面；
- 是否遵循效果图的设计方向；
- 是否符合 Design System 文档；
- 页面功能是否可用。

---

## 3. 验收通过标准

本次可判定为通过的条件：

- 项目能启动；
- 主要路由可打开；
- P0/P1 页面不再是纯说明页；
- mock 交互能正常执行；
- 关键数据能在页面之间流转；
- 文档存在且能指导后续任务；
- 视觉方向大体符合童话绘本 / 贴纸 / 奶油纸感；
- 真实图片资源未替换被记录为后续待办，而不是阻塞项。
