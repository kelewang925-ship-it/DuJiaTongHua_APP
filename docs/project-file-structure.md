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

### 2.3 业务页面概要

| 分组 | 代表文件 | 状态 |
| --- | --- | --- |
| 账号与情侣关联 | `app/account/invite.js`、`app/account/bind-confirm.js`、`app/account/couple-info.js` | mock MVP |
| 日记、记录与标签 | `app/diary/editor.js`、`app/diary/detail.js`、`app/tags/index.js`、`app/time-capsule/settings.js` | mock MVP |
| 照片与相册 | `app/photo/upload.js`、`app/photo/album.js`、`app/album/index.js` | mock MVP |
| AI 童话工坊 | `app/ai/comic-config.js`、`app/ai/video-config.js`、`app/ai/text-to-comic.js`、`app/ai/photo-to-comic.js`、`app/ai/progress.js`、`app/ai/comic-result.js`、`app/ai/character-profile.js`、`app/ai/history.js` | mock MVP |
| 情侣互动 | `app/couple/activity-detail.js`、`app/comments/index.js`、`app/notifications/index.js` | mock MVP |
| 纪念日 | `app/anniversary/index.js`、`app/anniversary/countdown.js`、`app/anniversary/edit.js`、`app/anniversary/template.js` | mock MVP |
| 数据与导出 | `app/data/backup.js`、`app/data/pdf-export.js`、`app/data/export-preview.js`、`app/data/storage.js` | mock MVP |

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
| `src/components/FairyEmptyState.js` | 统一空状态组件。支持插画、标题、说明、按钮和 compact 模式；后续需扩展真实空状态图片。 |
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
| `src/assets/fairyImages.js` | 图片资产元数据映射。记录 `homeCover`、`coupleCover`、`workshopCover`、`albumCover`、`anniversaryCover` 等 key 的标题、fallback scene、计划路径和说明；后续需要补充已存在但未接入的图片 key。 |

---

## 5. `src/theme/` / `src/store/` / `src/data/` / `src/api/`

| 目录/文件 | 作用 |
| --- | --- |
| `src/theme/colors.js` | 颜色 token，包含桃粉、干玫瑰、可可棕、月白、琥珀金等。 |
| `src/theme/spacing.js` | 间距 token。 |
| `src/theme/typography.js` | 字体排版 token。 |
| `src/theme/shadows.js` | 阴影 token。 |
| `src/store/useFairyStore.js` | Zustand 全局状态。管理情侣资料、记录流、情侣动态、AI作品、当前 AI 任务、纪念日、日记草稿等。 |
| `src/data/mockData.js` | 当前 App 原型使用的本地 mock 数据。 |
| `src/api/*.js` | API 抽象层，支持 mock/real 模式、Auth、日记、照片、纪念日、AI、情侣关系和存储。 |

---

## 6. `supabase/` 后端 SQL 目录

| 文件 | 作用 |
| --- | --- |
| `supabase/schema.sql` | 数据库结构文件，包含 profiles、couples、diaries、photos、anniversaries、ai_jobs、comments、notifications 等核心表。 |
| `supabase/rls-policies.sql` | RLS 权限策略文件，用于限制用户只能访问自己的 profile 和 active couple 内的数据。 |

---

## 7. `assets/design/` 设计稿目录

| 文件 | 作用 |
| --- | --- |
| `assets/design/项目全界面设计索引.md` | 全界面设计稿索引。 |
| `assets/design/png/界面设计图.png` | 第一张整块 PNG 效果图参考。 |
| `assets/design/png/界面设计图2.png` | 第二张整块 PNG 效果图参考。 |
| `assets/design/png/界面设计风格图-2.png` | 颜色、字体、圆角、阴影、组件、图标风格参考。 |
| `assets/design/*.svg` | 各模块和子页面 SVG 设计图。 |

---

## 8. `assets/images/` 图片资产目录

### 8.1 目录说明

| 文件/目录 | 作用 |
| --- | --- |
| `assets/images/README.md` | 图片资产目录说明。 |
| `assets/images/illustrations/` | 页面核心插画和空状态插画目录。 |
| `assets/images/stickers/` | 贴纸图片目录。 |
| `assets/images/backgrounds/` | 背景纹理目录。 |
| `assets/images/covers/` | 分享封面、PDF 封面目录。 |
| `assets/images/generated/` | AI 生成结果或开发期缓存目录。 |

### 8.2 已生成并已接入图片

| 文件 | 作用 | 接入方式 |
| --- | --- | --- |
| `assets/images/illustrations/home-cover-v1.png` | 首页 Hero 真实插画。 | `FairyImage homeCover` → `app/(tabs)/index.js` |
| `assets/images/illustrations/couple-space-cover-v1.png` | 情侣空间 Hero 真实插画。 | `FairyImage coupleCover` → `app/(tabs)/couple.js` |
| `assets/images/illustrations/workshop-cover-v1.png` | 童话工坊 Hero 真实插画。 | `FairyImage workshopCover` → `app/(tabs)/workshop.js` |

### 8.3 已生成但尚未接入图片

| 文件 | 类型 | 建议接入位置 |
| --- | --- | --- |
| `assets/images/illustrations/album-cover-v1.png` | 页面核心插画 | `app/photo/album.js`、照片模块 |
| `assets/images/illustrations/anniversary-cover-v1.png` | 页面核心插画 | `app/anniversary/index.js`、纪念日模块 |
| `assets/images/illustrations/export-cover-v1.png` | 页面核心插画 | `app/data/export-preview.js`、`app/data/pdf-export.js` |
| `assets/images/illustrations/time-capsule-cover-v1.png` | 页面核心插画 | `app/time-capsule/settings.js` |
| `assets/images/illustrations/empty-album-v1.png` | 空状态插画 | 相册/照片空状态 |
| `assets/images/illustrations/empty-diary-v1.png` | 空状态插画 | 日记/草稿空状态 |
| `assets/images/illustrations/empty-search-v1.png` | 空状态插画 | `app/search.js` |
| `assets/images/illustrations/empty-notification-v1.png` | 空状态插画 | `app/notifications/index.js` |
| `assets/images/stickers/heart-sticker-v1.png` | 贴纸 | 首页、时间轴、弹窗、分享图装饰 |
| `assets/images/stickers/star-sticker-v1.png` | 贴纸 | 首页、AI工坊、空状态装饰 |
| `assets/images/stickers/flower-sticker-v1.png` | 贴纸 | 情侣空间、纪念日、封面装饰 |
| `assets/images/stickers/tape-pink-v1.png` | 贴纸 | 卡片胶带、回忆墙、时间轴装饰 |
| `assets/images/stickers/magic-wand-v1.png` | 贴纸 | AI工坊、AI流程页装饰 |
| `assets/images/covers/pdf-memory-book-cover-v1.png` | 封面 | PDF导出预览、回忆册封面 |
| `assets/images/covers/share-preview-cover-v1.png` | 封面 | `app/share-preview.js` |

### 8.4 仍缺失图片

| 文件 | 类型 | 说明 |
| --- | --- | --- |
| `assets/images/illustrations/empty-ai-history-v1.png` | 空状态插画 | AI创作历史为空。 |
| `assets/images/stickers/tape-cream-v1.png` | 贴纸 | 奶油色胶带。 |
| `assets/images/stickers/polaroid-corner-v1.png` | 贴纸 | 拍立得角标。 |
| `assets/images/backgrounds/cream-paper-texture-v1.png` | 背景 | 月白纸感背景。 |
| `assets/images/backgrounds/soft-pink-gradient-v1.png` | 背景 | 柔和桃粉渐变背景。 |
| `assets/images/covers/anniversary-share-cover-v1.png` | 封面 | 纪念日分享封面。 |

---

## 9. `docs/` 文档目录

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
| `docs/next-image-generation-plan.md` | 下一批图片生成计划；已根据 `assets/images/` 实际状态区分“已生成待接入”和“仍缺失”。 |
| `docs/page-route-association-map.md` | 页面关联矩阵和历史兼容重定向说明。 |
| `docs/pending-interfaces-implementation-plan.md` | 待补页面实现计划和连续推进记录。 |
| `docs/project-development-master-plan.md` | 项目完整开发计划与进度记录。 |
| `docs/project-file-structure.md` | 当前文件，即项目文件结构说明。 |
| `docs/project-image-generation-prompts.md` | 已归档的首批项目图片生成提示词。 |
| `docs/supabase-auth-setup.md` | Supabase Auth 接入记录。 |
| `docs/visual-audit-and-next-steps.md` | 视觉还原检查与下一步计划。 |
| `docs/《独家童话》Design System v1.0.md` | 中文完整 Design System。 |
| `docs/《独家童话》UI设计总方向.md` | UI 设计总方向。 |

---

## 10. 当前关键业务闭环

```text
写日记 → addDiaryRecord → records + timeline
传照片 → addPhotoRecord → records + timeline
添加纪念日 → addAnniversary → anniversaries + timeline
生成 AI 作品 → addCreation → creations + timeline
```

---

## 11. 当前图片接入闭环

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

后续新增或接入图片时，需要同步更新：

```text
src/assets/fairyImages.js
src/components/FairyImage.js
docs/image-assets-guideline.md
docs/project-file-structure.md
```

贴纸类图片建议新增统一入口：

```text
src/assets/fairyStickers.js
src/components/FairySticker.js
```
