# 《独家童话》项目文件结构说明

本文档用于记录当前《独家童话》APP 项目的主要文件结构，以及每个文件/目录承担的职责。项目基于 React Native、Expo、Expo Router、JavaScript 开发，视觉方向遵循童话绘本、奶油纸感、桃粉、干玫瑰、可可棕、手绘贴纸式组件和轻量 AI 魔法感。

> 维护规则：新增页面、组件、状态模块、API 模块、Supabase 文件或设计稿时，需要同步更新本文档。

---

## 1. 根目录文件

| 文件 | 作用 |
| --- | --- |
| `package.json` | 项目依赖与启动脚本配置。当前入口为 `expo-router/entry`，使用 Expo Router 管理页面路由。 |
| `app.json` | Expo 项目配置文件，通常用于配置应用名称、图标、启动页、平台参数等。 |
| `.gitignore` | Git 忽略规则，避免提交 node_modules、构建产物、临时文件等。 |

---

## 2. `app/` 路由目录

`app/` 是 Expo Router 的页面路由目录。文件路径会直接映射为 App 内页面路由。

### 2.1 根布局与基础页面

| 文件 | 路由 | 作用 |
| --- | --- | --- |
| `app/_layout.js` | 全局布局 | Expo Router 根布局，统一隐藏 Stack Header，并配置状态栏。 |
| `app/login.js` | `/login` | 登录/授权页，用于账号进入与后续情侣绑定判断。 |
| `app/settings.js` | `/settings` | 设置页，包含通知、隐私、主题、缓存等设置入口；当前已作为 `FairyPage` + `FairyHeader` 的二级页面示例。 |
| `app/drafts.js` | `/drafts` | 草稿箱页面，用于承载未完成的日记、照片说明、AI创作草稿等。 |
| `app/help-feedback.js` | `/help-feedback` | 帮助与反馈页，用于展示常见问题、反馈入口和产品支持信息。 |

---

### 2.2 Tab 主导航

| 文件 | 路由 | 作用 |
| --- | --- | --- |
| `app/(tabs)/_layout.js` | Tab Layout | 四个主 Tab 的布局配置：首页、情侣空间、童话工坊、我的；当前已接入 `FairyTabBar` 自定义贴纸式底部导航。 |
| `app/(tabs)/index.js` | `/` 或 `/(tabs)` | 首页/记录中心。展示恋爱天数、记录统计、日记/照片/AI/纪念日快捷入口、最近记录列表和回忆碎片墙；新增日记或照片后会随 `useFairyStore.records` 自动更新。 |
| `app/(tabs)/couple.js` | `/(tabs)/couple` | 情侣空间。展示情侣资料、恋爱天数、共同记录/AI作品统计、日记/照片/AI/纪念日互动入口、纪念日预览和双人故事线；使用 `CoupleTimeline` 展示聚合后的 mock 动态流。 |
| `app/(tabs)/workshop.js` | `/(tabs)/workshop` | 童话工坊。展示漫画、视频、文字转漫画三个入口、最近作品提示和创作历史；点击历史作品会选中 `activeAiJob` 并进入进度/结果页，读取 `useFairyStore.creations`。 |
| `app/(tabs)/mine.js` | `/(tabs)/mine` | 我的页面。展示用户资料、情侣统计、日记/照片/AI作品/纪念日四项统计，以及设置、草稿箱、PDF导出、数据备份入口；四项统计分别来自 `useFairyStore.getStats()`。 |

---

### 2.3 账号与情侣关联页面

| 文件 | 路由 | 作用 |
| --- | --- | --- |
| `app/account/invite.js` | `/account/invite` | 情侣邀请页，用于生成或展示邀请入口、邀请码/二维码等绑定方式。 |
| `app/account/bind-confirm.js` | `/account/bind-confirm` | 情侣绑定确认页，用于确认对方身份并完成绑定流程。 |

---

### 2.4 日记与记录页面

| 文件 | 路由 | 作用 |
| --- | --- | --- |
| `app/diary/editor.js` | `/diary/editor` | 日记编辑器。支持标题、正文、心情、故事标签输入；已接入 `FairyInput`，保存后调用 `addDiaryRecord`，给出保存成功反馈并跳转日记详情，同步首页记录和情侣空间动态。 |
| `app/diary/detail.js` | `/diary/detail` | 日记详情页。读取最新一篇日记，展示标题、日期、心情、标签、正文，提供文本转漫画入口，并在无日记时显示统一空状态。 |

---

### 2.5 照片与相册页面

| 文件 | 路由 | 作用 |
| --- | --- | --- |
| `app/photo/upload.js` | `/photo/upload` | 照片上传页。当前为模拟照片上传，已接入 `FairyInput`，支持标题、备注、标签、照片数量选择；保存后调用 `addPhotoRecord`，给出完成反馈并跳转相册。 |
| `app/photo/album.js` | `/photo/album` | 照片相册浏览页。读取 `records` 中的照片记录，展示照片统计、上传入口、网格/时间线两种视图、标签和统一空状态。 |
| `app/album/index.js` | `/album` | 相册首页/相册浏览入口，用于承载更完整的相册浏览体验。 |

---

### 2.6 AI 童话工坊页面

| 文件 | 路由 | 作用 |
| --- | --- | --- |
| `app/ai/comic-config.js` | `/ai/comic-config` | AI 漫画生成配置页。支持选择素材、漫画风格、作品名称；点击生成后调用 `addCreation` 创建 mock 任务并跳转进度页。 |
| `app/ai/video-config.js` | `/ai/video-config` | AI 短视频配置页。支持输入作品名称、选择音乐和时长；点击生成后调用 `addCreation` 创建 mock 任务并跳转进度页。 |
| `app/ai/progress.js` | `/ai/progress` | AI 生成进度页。优先读取 `activeAiJob` 展示生成中的漫画/视频状态、步骤和结果预览，可模拟完成并回到童话工坊。 |
| `app/ai/generation-progress.js` | `/ai/generation-progress` | 生成进度相关页面，可能用于兼容或承载另一版 AI 生成流程。 |
| `app/ai/text-to-comic.js` | `/ai/text-to-comic` | 文本转漫画页。已接入 `FairyInput` 和 `useFairyStore`，可从最近日记或自由文本创建 mock 漫画任务。 |
| `app/ai/video-preview.js` | `/ai/video-preview` | 视频预览/编辑页，用于展示生成后的视频预览、字幕、封面或编辑入口。 |

---

### 2.7 纪念日页面

| 文件 | 路由 | 作用 |
| --- | --- | --- |
| `app/anniversary/index.js` | `/anniversary` | 纪念日管理页。读取 `anniversaries`，支持新增纪念日，表单已接入 `FairyInput`，保存后同步情侣空间动态。 |
| `app/anniversary/countdown.js` | `/anniversary/countdown` | 纪念日倒计时页，用于展示某个重要日子的倒计时/已过去天数。 |

---

### 2.8 数据与导出页面

| 文件 | 路由 | 作用 |
| --- | --- | --- |
| `app/data/backup.js` | `/data/backup` | 数据备份/恢复页。展示日记、照片、AI作品统计，并提供备份/恢复操作入口。 |
| `app/data/pdf-export.js` | `/data/pdf-export` | PDF 导出配置页。展示导出范围、绘本样式、预览导出入口。 |

---

## 3. `src/components/` 组件目录

组件目录用于沉淀童话绘本风格的复用 UI，不直接绑定具体业务路由。

| 文件 | 作用 |
| --- | --- |
| `src/components/FairyPage.js` | 页面外壳组件。统一月白纸感背景、页面横向内边距、顶部间距、底部安全留白和滚动容器，后续新页面优先使用它替代散落的 `ScrollView`。 |
| `src/components/FairyHeader.js` | 页面标题组件。统一 eyebrow、标题、副标题、返回按钮和右侧操作区，适合二级页面、设置页和通用功能页。 |
| `src/components/FairyCard.js` | 基础卡片组件。统一圆角、描边、纸感背景、柔和阴影。 |
| `src/components/FairyButton.js` | 基础按钮组件。支持 primary/secondary 样式与按压反馈。 |
| `src/components/FairyTag.js` | 标签组件。用于日记标签、AI标签、会员标签、状态标签等。 |
| `src/components/FairyInput.js` | 统一输入框组件。支持 label、icon、helper、error、单行/多行输入，用于替代页面内散落的原生 TextInput。 |
| `src/components/FairyEmptyState.js` | 统一空状态组件。支持插画、标题、说明、按钮和 compact 模式，用于相册、搜索、草稿箱、创作历史等空状态。 |
| `src/components/FairyDialog.js` | 统一弹窗组件。支持图标、标题、说明、确认/取消按钮，用于删除确认、AI生成确认、退出编辑确认等浮层场景。 |
| `src/components/FairyToast.js` | 统一轻反馈组件。支持 success/error/info 三种语气，用于保存成功、上传完成、生成开始、失败提醒等短提示。 |
| `src/components/FairyTabBar.js` | 自定义贴纸式底部 TabBar。用于替代 Expo 默认 TabBar，实现桃粉激活胶囊、贴纸底座和图标浮起。 |
| `src/components/FairyImage.js` | 图片统一入口组件。通过 `name` 映射使用插画资源，真实图片缺失时 fallback 到 `FairyIllustration`。 |
| `src/components/MemoryWall.js` | 首页回忆碎片墙组件。用于将日记、照片、漫画、视频等记录以拼贴、胶带、拍立得、贴纸卡片形式展示。 |
| `src/components/CoupleTimeline.js` | 情侣空间手绘时间轴组件。用于将情侣动态展示为章节式故事线，包含贴纸节点、曲线连接线、胶带卡片和互动入口。 |
| `src/components/FairyBackButton.js` | 返回按钮组件。用于二级页面顶部返回操作。 |
| `src/components/FairyIllustration.js` | SVG 插画组件。提供 cover、album、workshop/movie、anniversary 等绘本插画场景。 |
| `src/components/FeaturePage.js` | 通用功能页模板。适合快速搭建帮助、说明、特殊功能、设置子页等内容型页面；当前已使用 `FairyPage` 和 `FairyHeader`。 |
| `src/components/MemoryCard.js` | 回忆记录卡片。用于普通记录流，展示日记/照片/漫画等混合记录。 |
| `src/components/WorkshopCard.js` | 工坊入口卡片。用于 AI 漫画、AI 视频等创作入口。 |

---

## 4. `src/theme/` 设计 Token 目录

主题目录统一管理设计系统中的颜色、间距、字体和阴影，避免页面内硬编码过多视觉参数。

| 文件 | 作用 |
| --- | --- |
| `src/theme/colors.js` | 颜色 token。包含主色桃粉、辅助粉、干玫瑰、可可棕、月白背景、琥珀金等。 |
| `src/theme/spacing.js` | 间距 token。包含 xs/sm/md/lg/xl/xxl/page 等基础间距。 |
| `src/theme/typography.js` | 字体排版 token。包含 title、sectionTitle、subtitle、body、caption 等字号与行高。 |
| `src/theme/shadows.js` | 阴影 token。包含 card、floating 等柔和阴影样式。 |

---

## 5. `src/store/` 状态管理目录

| 文件 | 作用 |
| --- | --- |
| `src/store/useFairyStore.js` | Zustand 全局状态。管理情侣资料、记录流、情侣动态、AI作品、当前 AI 任务、纪念日、日记草稿；提供 `addDiaryRecord`、`addPhotoRecord`、`addAnniversary`、`addCreation`、`selectAiJob`、`completeActiveAiJob`、`getStats` 等方法。 |

当前主要状态流转：

```text
写日记 → addDiaryRecord → records + timeline
传照片 → addPhotoRecord → records + timeline
添加纪念日 → addAnniversary → anniversaries + timeline
生成AI作品 → addCreation → creations + timeline
```

---

## 6. `src/data/` 本地数据目录

| 文件 | 作用 |
| --- | --- |
| `src/data/mockData.js` | 当前 App 原型使用的本地 mock 数据。包含情侣资料、初始记录、初始动态、初始创作历史、初始纪念日。 |

---

## 7. `src/api/` API 模块目录

该目录用于沉淀未来真实后端 API 的访问逻辑。目前接口以 mock 模式为主，后续 Phase 5/6 会逐步替换为 Supabase real 模式。

| 文件 | 作用 |
| --- | --- |
| `src/api/client.js` | API 客户端基础封装。当前支持 `EXPO_PUBLIC_API_MODE=mock/real`、`isMockMode`、统一响应结构、错误归一化、mock 延迟、Supabase 配置读取和 Phase 5 的 client 占位。 |
| `src/api/mockData.js` | API 层 mock 数据。用于接口尚未完成时模拟用户、情侣、照片、AI任务等数据。 |
| `src/api/diaryApi.js` | 日记相关 API 封装。提供 `getDiaryList`、`getDiaryDetail`、`createDiary`、`updateDiary`、`deleteDiary`。 |
| `src/api/photoApi.js` | 照片与相册 API 封装。提供 `getPhotoTimeline`、`getAlbumList`、`uploadPhoto`、`getAlbumDetail`、`deletePhoto`。 |
| `src/api/anniversaryApi.js` | 纪念日 API 封装。提供 `getAnniversaries`、`getAnniversaryList`、`getNextAnniversary`、`createAnniversary`、`updateAnniversary`、`deleteAnniversary`。 |
| `src/api/aiApi.js` | AI 创作相关 API 封装。提供 `createComicJob`、`createVideoJob`、`getAiJobDetail`、`getAiCreationHistory`、`retryAiJob`。 |
| `src/api/coupleApi.js` | 情侣关系 API 封装。提供 `getCoupleInfo`、`getCurrentCouple`、`createInviteCode`、`bindCouple`、`bindCoupleByCode`、`updateCoupleInfo`、`getCoupleTimeline`。 |
| `src/api/storageApi.js` | 存储 API 抽象。提供 `uploadImage`、`getSignedUrl`、`deleteFile`，后续用于 Supabase Storage。 |

---

## 8. `src/screens/` 页面实现目录

该目录用于存放较复杂页面的拆分实现。当前项目主要使用 `app/` 路由文件直接写页面，后续当页面变大时，可逐步迁移到 `src/screens/`。

| 文件 | 作用 |
| --- | --- |
| `src/screens/HomeScreen.js` | 首页屏幕实现草稿/历史版本，后续可作为 `app/(tabs)/index.js` 的拆分目标。 |
| `src/screens/MineScreen.js` | 我的页面屏幕实现草稿/历史版本，后续可作为 `app/(tabs)/mine.js` 的拆分目标。 |

---

## 9. `supabase/` 后端 SQL 目录

该目录用于保存 Supabase 数据库、权限和 Edge Function 相关文件。当前处于 Phase 5 后端接入阶段。

| 文件 | 作用 |
| --- | --- |
| `supabase/schema.sql` | Phase 5.1 数据库结构文件。包含 `profiles`、`couples`、`diaries`、`photos`、`anniversaries`、`ai_jobs`、`comments`、`notifications` 八张核心表，以及更新时间触发器、约束和常用索引。 |

后续计划文件：

| 文件 | 作用 |
| --- | --- |
| `supabase/rls-policies.sql` | Phase 5.2 权限策略文件。用于开启 RLS 并限制用户只能访问自己的 profile 和 active couple 内的数据。 |
| `supabase/functions/create-ai-comic-job/index.ts` | Phase 7 AI 漫画任务 Edge Function。 |
| `supabase/functions/create-ai-video-job/index.ts` | Phase 7 AI 视频任务 Edge Function。 |
| `supabase/functions/export-memory-pdf/index.ts` | Phase 8 PDF 导出 Edge Function。 |

---

## 10. `assets/design/` 设计稿目录

该目录保存《独家童话》APP 的视觉设计稿，主要为 SVG 设计图和总设计索引。

### 10.1 设计索引

| 文件 | 作用 |
| --- | --- |
| `assets/design/项目全界面设计索引.md` | 全界面设计稿索引，记录所有模块对应的 SVG 设计图与使用规则。 |
| `assets/design/界面设计图.png` | 项目总视觉参考图，后续页面设计与开发需保持同一风格。 |

### 10.2 八个主模块设计图

| 文件 | 作用 |
| --- | --- |
| `assets/design/01-账号与关联.svg` | 账号登录、邀请、绑定流程的模块设计总览。 |
| `assets/design/02-首页-记录中心.svg` | 首页和记录中心模块设计总览。 |
| `assets/design/03-情侣空间.svg` | 情侣空间和双人动态模块设计总览。 |
| `assets/design/04-AI童话工坊.svg` | AI 工坊入口和创作历史模块设计总览。 |
| `assets/design/05-AI创作流程.svg` | AI 漫画/视频生成流程设计总览。 |
| `assets/design/06-纪念日管理.svg` | 纪念日管理模块设计总览。 |
| `assets/design/07-数据与导出.svg` | PDF导出、备份恢复、存储管理模块总览。 |
| `assets/design/08-更多功能.svg` | 搜索、草稿、分享、会员、设置等更多功能总览。 |

### 10.3 账号与关联设计图

| 文件 | 作用 |
| --- | --- |
| `assets/design/引导页.svg` | 首次使用引导页设计稿。 |
| `assets/design/登录页.svg` | 登录/授权页设计稿。 |
| `assets/design/情侣邀请页.svg` | 邀请情侣绑定页面设计稿。 |
| `assets/design/情侣绑定确认页.svg` | 绑定确认页设计稿。 |
| `assets/design/情侣信息设置页.svg` | 情侣资料设置页设计稿。 |

### 10.4 首页与记录中心设计图

| 文件 | 作用 |
| --- | --- |
| `assets/design/日记编辑器.svg` | 日记编辑页设计稿。 |
| `assets/design/日记详情页.svg` | 日记详情页设计稿。 |
| `assets/design/照片上传页.svg` | 照片上传页设计稿。 |
| `assets/design/相册浏览页.svg` | 相册浏览页设计稿。 |
| `assets/design/时光胶囊设置页.svg` | 时光胶囊设置页设计稿。 |
| `assets/design/标签管理页.svg` | 标签管理页设计稿。 |

### 10.5 情侣空间与互动设计图

| 文件 | 作用 |
| --- | --- |
| `assets/design/情侣动态详情页.svg` | 情侣动态详情页设计稿。 |
| `assets/design/评论列表页.svg` | 评论列表页设计稿。 |
| `assets/design/互动通知页.svg` | 互动通知页设计稿。 |

### 10.6 AI 童话工坊设计图

| 文件 | 作用 |
| --- | --- |
| `assets/design/AI漫画生成配置页.svg` | AI 漫画配置页设计稿。 |
| `assets/design/文本转漫画页.svg` | 文本转漫画页设计稿。 |
| `assets/design/照片转漫画页.svg` | 照片转漫画页设计稿。 |
| `assets/design/AI短视频配置页.svg` | AI 短视频配置页设计稿。 |
| `assets/design/视频预览编辑页.svg` | 视频预览/编辑页设计稿。 |
| `assets/design/生成进度页.svg` | AI 生成进度页设计稿。 |
| `assets/design/创作历史展示页.svg` | AI 创作历史页设计稿。 |

### 10.7 纪念日管理设计图

| 文件 | 作用 |
| --- | --- |
| `assets/design/纪念日添加编辑页.svg` | 纪念日添加/编辑页设计稿。 |
| `assets/design/纪念日倒计时页.svg` | 纪念日倒计时页设计稿。 |
| `assets/design/纪念日专属记录模板页.svg` | 纪念日专属记录模板页设计稿。 |

### 10.8 数据与导出设计图

| 文件 | 作用 |
| --- | --- |
| `assets/design/PDF导出配置页.svg` | PDF导出配置页设计稿。 |
| `assets/design/导出预览页.svg` | 导出预览页设计稿。 |
| `assets/design/数据备份恢复页.svg` | 数据备份/恢复页设计稿。 |
| `assets/design/存储空间管理页.svg` | 存储空间管理页设计稿。 |

### 10.9 更多功能与特殊交互设计图

| 文件 | 作用 |
| --- | --- |
| `assets/design/搜索页.svg` | 记录搜索页设计稿。 |
| `assets/design/草稿箱.svg` | 草稿箱页设计稿。 |
| `assets/design/分享预览页.svg` | 分享预览页设计稿。 |
| `assets/design/会员权益说明页.svg` | 会员权益说明页设计稿。 |
| `assets/design/帮助与反馈页.svg` | 帮助与反馈页设计稿。 |
| `assets/design/设置页.svg` | 设置页设计稿。 |
| `assets/design/空状态页.svg` | 空状态页设计稿。 |

---

## 11. `docs/` 文档目录

| 文件 | 作用 |
| --- | --- |
| `docs/app-development-guide.md` | App 开发指南，记录技术栈、目录规则、UI一致性检查和后续工程需求。 |
| `docs/design-system-v1.md` | Design System 文档，记录品牌定位、配色、字体、圆角、阴影、组件规范等。 |
| `docs/interface-architecture-design.md` | 界面架构设计文档，记录主 Tab、功能子页面、页面流程关系等。 |
| `docs/backend-and-api-plan.md` | 后端与 API 规划文档，记录未来接口、数据模型、服务划分等。 |
| `docs/image-assets-guideline.md` | 图片资产规范与处理记录，记录图片目录、命名、尺寸、格式、接入方式和后续替换规则。 |
| `docs/dev-runbook.md` | 开发运行手册，记录环境要求、依赖安装、启动命令、Expo 调试方式、常见报错处理、路由新增规则和提交前检查清单。 |
| `docs/manual-checklist.md` | 手动验收清单，用于记录启动、四个 Tab、日记、照片、纪念日、AI 创建任务、我的统计、设置页和返回导航等检查结果。 |
| `docs/project-development-master-plan.md` | 项目完整开发计划与进度记录，记录当前阶段、后续路线、验收标准和阶段看板。 |
| `docs/codex-development-roadmap.md` | Codex 分阶段开发路线图，包含每个阶段可直接复制给 Codex 的任务指令、文件范围和验收清单。 |
| `docs/《独家童话》UI设计总方向.md` | UI 设计总方向文档，记录童话绘本、奶油纸感、情绪价值等整体视觉策略。 |
| `docs/project-file-structure.md` | 当前文件，即项目文件结构说明。 |

---

## 12. 当前关键业务闭环

### 12.1 日记闭环

```text
app/diary/editor.js
  → useFairyStore.addDiaryRecord
  → records 新增日记
  → timeline 新增情侣动态
  → 首页 / 情侣空间 / 我的统计同步更新
```

### 12.2 照片闭环

```text
app/photo/upload.js
  → useFairyStore.addPhotoRecord
  → records 新增照片记录
  → timeline 新增情侣动态
  → 首页 / 情侣空间 / 我的统计同步更新
```

### 12.3 纪念日闭环

```text
app/anniversary/index.js
  → useFairyStore.addAnniversary
  → anniversaries 新增纪念日
  → timeline 新增情侣动态
  → 纪念日列表 / 情侣空间同步更新
```

### 12.4 AI 创作闭环

```text
app/ai/comic-config.js 或 app/ai/video-config.js
  → useFairyStore.addCreation
  → creations 新增 AI 作品
  → timeline 新增情侣动态
  → app/ai/progress.js 展示最新作品进度
  → 童话工坊创作历史同步更新
```

---

## 13. 后续维护建议

1. 新增路由时，先在 `app/` 中创建页面，再在本文档 `app/` 对应分组补充说明。
2. 新增复用组件时，统一放入 `src/components/`，并说明适用场景。
3. 新增状态方法时，优先放入 `src/store/useFairyStore.js`，并在关键业务闭环中补充流转关系。
4. 新增真实 API 时，优先在 `src/api/` 中建立独立模块，页面层不要直接写请求细节。
5. 新增 Supabase SQL、RLS 或 Edge Function 时，更新本文档的 `supabase/` 部分和 `docs/backend-and-api-plan.md`。
6. 新增设计稿时，更新 `assets/design/项目全界面设计索引.md` 和本文档的 `assets/design/` 部分。
7. 页面视觉必须继续遵循：月白纸感背景、桃粉/干玫瑰强调、可可棕文字、轻描边卡片、AI页面温柔魔法感。
