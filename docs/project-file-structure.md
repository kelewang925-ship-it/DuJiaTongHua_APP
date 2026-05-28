# 《独家童话》项目文件结构说明

> 文档说明：本文档用于记录《独家童话》当前项目目录、页面路由、组件、状态、API、Supabase、设计稿、图片资产和文档文件的职责，是新开发者、Codex 和后续接手人员理解项目结构的主要入口。

> 维护规则：新增页面、组件、状态模块、API 模块、Supabase 文件、设计稿、图片资产或文档时，需要同步更新本文档。

---

## 0. 统一说明

| 术语 | 说明 |
| --- | --- |
| `mock MVP` | 表示当前页面已经具备本地可演示交互闭环，但不接真实后端、不接真实 AI、不接真实文件服务。 |
| `真实能力` | 表示需要接入 Supabase、Storage、真实 AI、PDF 导出、系统相册、登录态等生产能力。 |
| `兼容路由` | 表示为旧入口、历史设计稿或跳转兼容保留的转发页面，不作为新的主开发入口。 |
| `图片资产` | 表示项目中可被页面或组件引用的独立 PNG/WebP/SVG 资源，不包含整块设计效果图。 |

---

## 1. 根目录文件

| 文件 | 作用 |
| --- | --- |
| `package.json` | 项目依赖与启动脚本配置。当前入口为 `expo-router/entry`，使用 Expo Router 管理页面路由。 |
| `app.json` | Expo 项目配置文件，用于配置应用名称、图标、启动页、平台参数等。 |
| `.gitignore` | Git 忽略规则，避免提交 `node_modules`、构建产物、`.env`、`.expo` 等。 |
| `.env.example` | 环境变量示例文件，用于区分 mock / real API 模式和 Supabase 配置占位。 |

---

## 2. `app/` 路由目录

`app/` 是 Expo Router 的页面路由目录。文件路径会直接映射为 App 内页面路由。

### 2.1 全局、引导与基础页面

| 文件 | 路由 | 作用 |
| --- | --- | --- |
| `app/_layout.js` | 全局布局 | Expo Router 根布局，统一隐藏 Stack Header，并配置全局状态/认证入口。 |
| `app/onboarding.js` | `/onboarding` | 首次使用引导页（mock MVP），展示产品定位与进入登录/绑定流程入口。 |
| `app/login.js` | `/login` | 登录/授权页（mock MVP + Supabase Auth 骨架），支持邮箱/密码或 mock 登录流程。 |
| `app/settings.js` | `/settings` | 设置页，展示通知、隐私、主题、缓存等设置入口。 |
| `app/drafts.js` | `/drafts` | 草稿箱页面（mock MVP），展示日记草稿与 AI 草稿状态。 |
| `app/search.js` | `/search` | 记录搜索页（mock MVP），搜索 `records`、`creations`、`anniversaries`、`timeline`。 |
| `app/help-feedback.js` | `/help-feedback` | 帮助与反馈页（mock MVP），展示常见问题并支持反馈内容提交。 |
| `app/empty-state.js` | `/empty-state` | 空状态展示页，用于统一空状态视觉参考。 |
| `app/share-preview.js` | `/share-preview` | 分享预览页（mock MVP），支持分享样式切换、隐私选项和 mock 生成反馈。 |
| `app/membership.js` | `/membership` | 会员权益说明页（mock MVP），展示权益、方案选择和 mock 开通反馈。 |

### 2.2 Tab 主导航

| 文件 | 路由 | 作用 |
| --- | --- | --- |
| `app/(tabs)/_layout.js` | Tab Layout | 四个主 Tab 的布局配置：首页、情侣空间、童话工坊、我的；已接入 `FairyTabBar`。 |
| `app/(tabs)/index.js` | `/` 或 `/(tabs)` | 首页/记录中心。展示恋爱天数、快捷入口、记录统计、最近记录和 `MemoryWall` 回忆碎片墙；顶部 Hero 已通过 `FairyImage homeCover` 接入真实图片。 |
| `app/(tabs)/couple.js` | `/(tabs)/couple` | 情侣空间。展示情侣资料、互动入口、纪念日预览和 `CoupleTimeline` 手绘时间轴；顶部 Hero 已通过 `FairyImage coupleCover` 接入真实图片。 |
| `app/(tabs)/workshop.js` | `/(tabs)/workshop` | 童话工坊。展示漫画、视频、文本转漫画入口和创作历史；顶部 Hero 已通过 `FairyImage workshopCover` 接入真实图片。 |
| `app/(tabs)/mine.js` | `/(tabs)/mine` | 我的页面。展示用户资料、数据统计、纪念日、数据导出、设置、退出登录等入口。 |

### 2.3 账号与情侣关联页面

| 文件 | 路由 | 作用 |
| --- | --- | --- |
| `app/account/invite.js` | `/account/invite` | 情侣邀请页（mock MVP），展示邀请码、复制反馈和进入绑定确认。 |
| `app/account/bind-confirm.js` | `/account/bind-confirm` | 情侣绑定确认页（mock MVP），展示对方信息并确认绑定。 |
| `app/account/couple-info.js` | `/account/couple-info` | 情侣信息设置页（mock MVP），支持昵称、起始日、空间名称等设置。 |
| `app/account/couple-settings.js` | `/account/couple-settings` | 情侣资料设置页/兼容设置入口，用于后续完善情侣资料管理。 |

### 2.4 日记、记录与标签

| 文件 | 路由 | 作用 |
| --- | --- | --- |
| `app/diary/editor.js` | `/diary/editor` | 日记编辑器。支持标题、正文、心情、标签输入，保存后写入 `records` 和 `timeline`。 |
| `app/diary/detail.js` | `/diary/detail` | 日记详情页。展示最近日记，支持跳转文本转漫画。 |
| `app/tags/index.js` | `/tags` | 标签管理页（mock MVP）。从记录中统计标签，支持新增标签和按标签筛选记录。 |
| `app/records/tags.js` | `/records/tags` | 标签管理兼容路由，指向新的标签管理能力。 |
| `app/time-capsule/settings.js` | `/time-capsule/settings` | 时光胶囊设置页（mock MVP）。支持创建胶囊、设置解锁日期和封存类型。 |
| `app/records/time-capsule.js` | `/records/time-capsule` | 时光胶囊兼容路由，指向新的时光胶囊设置能力。 |

### 2.5 照片与相册页面

| 文件 | 路由 | 作用 |
| --- | --- | --- |
| `app/photo/upload.js` | `/photo/upload` | 照片上传页（mock MVP），支持标题、备注、标签、照片数量选择并写入记录流。 |
| `app/photo/album.js` | `/photo/album` | 照片相册浏览页，支持网格/时间线视图和空状态。 |
| `app/album/index.js` | `/album` | 相册首页/相册浏览入口，用于后续完整相册体验。 |

### 2.6 AI 童话工坊页面

| 文件 | 路由 | 作用 |
| --- | --- | --- |
| `app/ai/comic-config.js` | `/ai/comic-config` | AI 漫画生成配置页，支持素材、风格、作品名并创建 mock AI 任务。 |
| `app/ai/video-config.js` | `/ai/video-config` | AI 短视频配置页，支持作品名、音乐、时长并创建 mock AI 任务。 |
| `app/ai/text-to-comic.js` | `/ai/text-to-comic` | 文本转漫画页（mock MVP），支持从最近日记或自由文本创建漫画任务。 |
| `app/ai/photo-to-comic.js` | `/ai/photo-to-comic` | 照片转漫画页（mock MVP），支持照片组选择、作品名、画风选择和任务创建。 |
| `app/ai/progress.js` | `/ai/progress` | AI 生成进度页，展示当前 `activeAiJob` 的生成状态、步骤和结果预览。 |
| `app/ai/generation-progress.js` | `/ai/generation-progress` | 生成进度兼容页/备用流程入口。 |
| `app/ai/video-preview.js` | `/ai/video-preview` | 视频预览/编辑页（mock MVP），展示播放器、字幕、封面和编辑项。 |
| `app/ai/comic-result.js` | `/ai/comic-result` | AI 漫画结果详情页（mock MVP），展示分镜预览、结果状态和回到工坊入口。 |
| `app/ai/character-profile.js` | `/ai/character-profile` | AI 人设管理页（mock MVP），支持角色设定、关系氛围和风格配置。 |
| `app/ai/history.js` | `/ai/history` | AI 创作历史页，用于集中展示历史作品和后续结果详情入口。 |

### 2.7 情侣互动页面

| 文件 | 路由 | 作用 |
| --- | --- | --- |
| `app/couple/activity-detail.js` | `/couple/activity-detail` | 情侣动态详情页（mock MVP），展示最近时间线节点、关联记录、AI作品和评论入口。 |
| `app/couple/story-detail.js` | `/couple/story-detail` | 情侣故事详情页/兼容详情入口，用于后续承载更完整的故事节点详情。 |
| `app/comments/index.js` | `/comments` | 评论列表页（mock MVP），支持初始评论、输入评论和追加评论。 |
| `app/interaction/comments.js` | `/interaction/comments` | 评论兼容路由，服务旧入口或通知跳转。 |
| `app/notifications/index.js` | `/notifications` | 互动通知页（mock MVP），支持类型筛选、已读状态和跳转对应页面。 |
| `app/interaction/notifications.js` | `/interaction/notifications` | 通知兼容路由，服务旧入口或设计稿旧路径。 |

### 2.8 纪念日页面

| 文件 | 路由 | 作用 |
| --- | --- | --- |
| `app/anniversary/index.js` | `/anniversary` | 纪念日管理页，读取 `anniversaries`，支持新增纪念日和跳转编辑/模板页。 |
| `app/anniversary/countdown.js` | `/anniversary/countdown` | 纪念日倒计时页（mock MVP），展示倒计时信息和模板准备入口。 |
| `app/anniversary/edit.js` | `/anniversary/edit` | 纪念日添加/编辑独立页（mock MVP），支持标题、日期、备注和模板预填。 |
| `app/anniversary/template.js` | `/anniversary/template` | 纪念日专属记录模板页（mock MVP），支持模板选择、预览和跳转编辑。 |

### 2.9 数据与导出页面

| 文件 | 路由 | 作用 |
| --- | --- | --- |
| `app/data/backup.js` | `/data/backup` | 数据备份/恢复页（mock MVP），展示数据统计与备份/恢复入口。 |
| `app/data/pdf-export.js` | `/data/pdf-export` | PDF 导出配置页（mock MVP），展示导出范围、绘本样式和预览入口。 |
| `app/data/export-preview.js` | `/data/export-preview` | 导出预览页（mock MVP），展示封面、目录、页数、样式和确认导出反馈。 |
| `app/data/storage.js` | `/data/storage` | 存储空间管理页（mock MVP），展示分类占比和缓存清理 mock 操作。 |

---

## 3. `src/components/` 组件目录

| 文件 | 作用 |
| --- | --- |
| `src/components/FairyPage.js` | 页面外壳组件。统一背景、内边距、顶部间距、底部安全留白和滚动容器。 |
| `src/components/FairyHeader.js` | 页面标题组件。统一 eyebrow、标题、副标题、返回按钮和右侧操作区。 |
| `src/components/FairyCard.js` | 基础卡片组件。统一圆角、描边、纸感背景、柔和阴影。 |
| `src/components/FairyButton.js` | 基础按钮组件。支持 primary/secondary 样式与按压反馈。 |
| `src/components/FairyTag.js` | 标签组件。用于日记标签、AI 标签、会员标签、状态标签等。 |
| `src/components/FairyInput.js` | 统一输入框组件。支持 label、icon、helper、error、单行/多行输入。 |
| `src/components/FairyEmptyState.js` | 统一空状态组件。支持插画、标题、说明、按钮和 compact 模式。 |
| `src/components/FairyDialog.js` | 统一弹窗组件。支持确认/取消操作。 |
| `src/components/FairyToast.js` | 统一轻反馈组件。支持 success/error/info 三种语气。 |
| `src/components/FairyTabBar.js` | 自定义贴纸式底部 TabBar。 |
| `src/components/FairyImage.js` | 图片统一入口组件，通过 `name` 映射插画资源；当前已接入 `homeCover`、`coupleCover`、`workshopCover` 三张真实 PNG，缺失资源时 fallback 到 `FairyIllustration`。 |
| `src/components/FairyIllustration.js` | SVG 插画组件，提供 cover、album、workshop、anniversary 等绘本场景。 |
| `src/components/MemoryWall.js` | 首页回忆碎片墙组件。 |
| `src/components/CoupleTimeline.js` | 情侣空间手绘时间轴组件。 |
| `src/components/MemoryCard.js` | 普通记录卡片组件。 |
| `src/components/WorkshopCard.js` | AI 工坊入口卡片组件。 |
| `src/components/FairyBackButton.js` | 返回按钮组件。 |
| `src/components/FeaturePage.js` | 通用功能页模板。 |

---

## 4. `src/assets/` 资产映射目录

| 文件 | 作用 |
| --- | --- |
| `src/assets/fairyImages.js` | 图片资产元数据映射。记录 `homeCover`、`coupleCover`、`workshopCover`、`albumCover`、`anniversaryCover` 等 key 的标题、fallback scene、计划路径和说明。 |

---

## 5. `src/theme/` 设计 Token 目录

| 文件 | 作用 |
| --- | --- |
| `src/theme/colors.js` | 颜色 token，包含桃粉、干玫瑰、可可棕、月白、琥珀金等。 |
| `src/theme/spacing.js` | 间距 token，包含 xs/sm/md/lg/xl/xxl/page 等。 |
| `src/theme/typography.js` | 字体排版 token。 |
| `src/theme/shadows.js` | 阴影 token。 |

---

## 6. `src/store/` 状态管理目录

| 文件 | 作用 |
| --- | --- |
| `src/store/useFairyStore.js` | Zustand 全局状态。管理情侣资料、记录流、情侣动态、AI作品、当前 AI 任务、纪念日、日记草稿，并提供 `addDiaryRecord`、`addPhotoRecord`、`addAnniversary`、`addCreation`、`selectAiJob`、`completeActiveAiJob`、`getStats` 等方法。 |

当前主要状态流转：

```text
写日记 → addDiaryRecord → records + timeline
传照片 → addPhotoRecord → records + timeline
添加纪念日 → addAnniversary → anniversaries + timeline
生成 AI 作品 → addCreation → creations + timeline
```

---

## 7. `src/data/` 本地数据目录

| 文件 | 作用 |
| --- | --- |
| `src/data/mockData.js` | 当前 App 原型使用的本地 mock 数据，包含情侣资料、初始记录、动态、创作历史、纪念日等。 |

---

## 8. `src/api/` API 模块目录

| 文件 | 作用 |
| --- | --- |
| `src/api/client.js` | API 客户端基础封装，支持 mock/real 模式、统一响应结构、错误归一化和 Supabase client。 |
| `src/api/authApi.js` | Supabase Auth / mock Auth 封装。 |
| `src/api/mockData.js` | API 层 mock 数据。 |
| `src/api/diaryApi.js` | 日记相关 API 封装。 |
| `src/api/photoApi.js` | 照片与相册 API 封装。 |
| `src/api/anniversaryApi.js` | 纪念日 API 封装。 |
| `src/api/aiApi.js` | AI 创作 API 封装。 |
| `src/api/coupleApi.js` | 情侣关系 API 封装。 |
| `src/api/storageApi.js` | 存储 API 抽象，后续用于 Supabase Storage。 |

---

## 9. `supabase/` 后端 SQL 目录

| 文件 | 作用 |
| --- | --- |
| `supabase/schema.sql` | 数据库结构文件，包含 profiles、couples、diaries、photos、anniversaries、ai_jobs、comments、notifications 等核心表。 |
| `supabase/rls-policies.sql` | RLS 权限策略文件，用于限制用户只能访问自己的 profile 和 active couple 内的数据。 |

---

## 10. `assets/design/` 设计稿目录

| 文件 | 作用 |
| --- | --- |
| `assets/design/项目全界面设计索引.md` | 全界面设计稿索引。 |
| `assets/design/png/界面设计图.png` | 第一张整块 PNG 效果图参考。 |
| `assets/design/png/界面设计图2.png` | 第二张整块 PNG 效果图参考。 |
| `assets/design/png/界面设计风格图-2.png` | 颜色、字体、圆角、阴影、组件、图标风格参考。 |
| `assets/design/*.svg` | 各模块和子页面 SVG 设计图。 |

---

## 11. `assets/images/` 图片资产目录

| 文件/目录 | 作用 |
| --- | --- |
| `assets/images/README.md` | 图片资产目录说明。 |
| `assets/images/illustrations/` | 页面核心插画目录，用于首页、情侣空间、童话工坊、相册、纪念日、空状态等独立插画。 |
| `assets/images/illustrations/home-cover-v1.png` | 首页 Hero 真实插画。已通过 `FairyImage homeCover` 接入 `app/(tabs)/index.js`。 |
| `assets/images/illustrations/couple-space-cover-v1.png` | 情侣空间 Hero 真实插画。已通过 `FairyImage coupleCover` 接入 `app/(tabs)/couple.js`。 |
| `assets/images/illustrations/workshop-cover-v1.png` | 童话工坊 Hero 真实插画。已通过 `FairyImage workshopCover` 接入 `app/(tabs)/workshop.js`。 |
| `assets/images/stickers/` | 贴纸图片目录，后续放入爱心、星星、胶带、花朵、魔法棒等。 |
| `assets/images/backgrounds/` | 背景纹理目录，后续放入月白纸感纹理、柔和渐变等。 |
| `assets/images/covers/` | 分享封面、PDF 封面目录。 |
| `assets/images/generated/` | AI 生成结果或开发期缓存目录。 |

---

## 12. `docs/` 文档目录

| 文件 | 作用 |
| --- | --- |
| `docs/app-development-guide.md` | App 开发指南。 |
| `docs/backend-and-api-plan.md` | 后端与 API 规划。 |
| `docs/codex-development-roadmap.md` | Codex 分阶段开发路线图。 |
| `docs/design-system-v1.md` | 早期 Design System 文档。 |
| `docs/dev-runbook.md` | 开发运行手册。 |
| `docs/document-consistency-audit.md` | 文档一致性整理记录。 |
| `docs/image-assets-guideline.md` | 图片资产规范与处理记录，记录图片路径、来源、格式、使用页面和 `FairyImage` 接入状态。 |
| `docs/image-assets-implementation-plan.md` | 首批图片资产拆分/重新生成实施计划。 |
| `docs/interface-architecture-design.md` | 界面架构设计。 |
| `docs/interface-list.md` | 当前界面与子界面清单。 |
| `docs/manual-checklist.md` | 手动验收清单。 |
| `docs/next-image-generation-plan.md` | 下一批图片生成计划，覆盖相册、纪念日、导出、时光胶囊、空状态、贴纸、背景和封面。 |
| `docs/page-route-association-map.md` | 页面关联矩阵和历史兼容重定向说明。 |
| `docs/pending-interfaces-implementation-plan.md` | 待补页面实现计划和连续推进记录。 |
| `docs/project-development-master-plan.md` | 项目完整开发计划与进度记录。 |
| `docs/project-file-structure.md` | 当前文件，即项目文件结构说明。 |
| `docs/project-image-generation-prompts.md` | 已归档的首批项目图片生成提示词。 |
| `docs/supabase-auth-setup.md` | Supabase Auth 接入记录。 |
| `docs/visual-audit-and-next-steps.md` | 视觉还原检查与下一步计划。 |
| `docs/《独家童话》Design System v1.0.md` | 中文完整 Design System。 |
| `docs/《独家童话》UI设计总方向.md` | UI 设计总方向。 |

已删除的一次性文档：

```text
docs/codex-page-acceptance-test-prompt.md
docs/next-chat-handoff-prompt.md
```

---

## 13. 当前关键业务闭环

### 13.1 日记闭环

```text
app/diary/editor.js
  → useFairyStore.addDiaryRecord
  → records 新增日记
  → timeline 新增情侣动态
  → 首页 / 情侣空间 / 我的统计同步更新
```

### 13.2 照片闭环

```text
app/photo/upload.js
  → useFairyStore.addPhotoRecord
  → records 新增照片记录
  → timeline 新增情侣动态
  → 首页 / 情侣空间 / 我的统计同步更新
```

### 13.3 纪念日闭环

```text
app/anniversary/index.js
  → useFairyStore.addAnniversary
  → anniversaries 新增纪念日
  → timeline 新增情侣动态
  → 纪念日列表 / 情侣空间同步更新
```

### 13.4 AI 创作闭环

```text
app/ai/comic-config.js / app/ai/video-config.js / app/ai/text-to-comic.js / app/ai/photo-to-comic.js
  → useFairyStore.addCreation
  → creations 新增 AI 作品
  → timeline 新增情侣动态
  → app/ai/progress.js 展示最新作品进度
  → 童话工坊创作历史同步更新
```

---

## 14. 当前图片接入闭环

```text
assets/images/illustrations/home-cover-v1.png
  → src/components/FairyImage.js imageSourceMap.homeCover
  → app/(tabs)/index.js

assets/images/illustrations/couple-space-cover-v1.png
  → src/components/FairyImage.js imageSourceMap.coupleCover
  → app/(tabs)/couple.js

assets/images/illustrations/workshop-cover-v1.png
  → src/components/FairyImage.js imageSourceMap.workshopCover
  → app/(tabs)/workshop.js
```

后续新增图片时，需要同步更新：

```text
src/assets/fairyImages.js
src/components/FairyImage.js
docs/image-assets-guideline.md
docs/project-file-structure.md
```
