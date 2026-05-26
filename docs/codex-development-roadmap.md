# 《独家童话》Codex 分阶段开发路线图

> 更新时间：2026-05-26  
> 用途：本文件专门用于后续通过 Codex 程序继续开发整个项目。  
> 使用方式：每次只复制一个阶段或一个任务块给 Codex，不要一次性让 Codex 完成所有阶段。

---

## 0. Codex 使用总规则

使用 Codex 开发本项目时，必须遵守以下规则：

1. 每次只做一个阶段中的一个任务，不要一次性做多个大功能。
2. 每次任务开始前，让 Codex 先读取：
   - `docs/project-development-master-plan.md`
   - `docs/project-file-structure.md`
   - `docs/design-system-v1.md`
   - `docs/backend-and-api-plan.md`
   - 当前任务相关文件
3. 每次任务要明确告诉 Codex：
   - 本次目标
   - 允许修改的文件
   - 禁止修改的文件
   - 验收标准
   - 需要更新的文档
4. 每次提交前必须检查 import 路径。
5. 不允许把真实密钥写入仓库。
6. 不允许绕过 `src/api/` 直接在页面里写后端请求。
7. 不允许破坏现有童话绘本视觉体系。
8. 每完成一个阶段，都要更新 `docs/project-development-master-plan.md`。

推荐每次 Codex 提交信息格式：

```text
phase-x: 简短说明
```

示例：

```text
phase-1: add dev runbook and env example
phase-2: complete diary mock flow
phase-5: add supabase auth api
```

---

# Phase 1：项目稳定化与运行检查

## 目标

让项目可以稳定启动，主要页面可以访问，并建立开发运行文档。

## 任务 1.1：检查启动配置和依赖

### Codex 指令

```text
请读取 docs/project-development-master-plan.md、docs/project-file-structure.md 和 package.json。
本次只处理 Phase 1 的启动配置检查。
请检查 package.json 中的 scripts、dependencies 是否适合 Expo Router 项目；检查 app/_layout.js 和 app/(tabs)/_layout.js 是否存在明显路由问题；检查常见 import 路径是否可能缺失。
不要大规模重构页面，不要接入后端，不要改变 UI 风格。
如果发现缺失依赖或明显错误，请修复。
完成后给出验证命令和结果说明。
```

### 允许修改

- `package.json`
- `app/_layout.js`
- `app/(tabs)/_layout.js`
- 明显错误的 import 文件

### 禁止修改

- 不要重构所有页面。
- 不要删除现有组件。
- 不要接入 Supabase。

### 验收标准

- `npm install` 无明显依赖冲突。
- `npm run start` 可以启动。
- Expo Router 不出现基础路由错误。

---

## 任务 1.2：新增环境变量示例

### Codex 指令

```text
请为项目新增 .env.example，用于后续 mock/real API 模式和 Supabase 接入。
只创建示例变量，不要写真实密钥。
同时检查 .gitignore，确保 .env 不会被提交。
完成后更新 docs/project-development-master-plan.md 的 Phase 1 记录。
```

### 建议内容

```bash
EXPO_PUBLIC_API_MODE=mock
EXPO_PUBLIC_SUPABASE_URL=
EXPO_PUBLIC_SUPABASE_ANON_KEY=
EXPO_PUBLIC_APP_NAME=独家童话
```

### 允许修改

- `.env.example`
- `.gitignore`
- `docs/project-development-master-plan.md`

### 验收标准

- `.env.example` 存在。
- `.gitignore` 忽略 `.env`。
- 没有真实密钥。

---

## 任务 1.3：新增开发运行手册

### Codex 指令

```text
请新增 docs/dev-runbook.md，作为项目开发运行手册。
文档需要包含：环境要求、安装依赖、启动命令、Expo 调试方式、常见报错处理、路由新增规则、组件新增规则、提交前检查清单。
不要修改业务代码。
完成后更新 docs/project-file-structure.md，把 dev-runbook.md 加入 docs 文档列表。
```

### 允许修改

- `docs/dev-runbook.md`
- `docs/project-file-structure.md`

### 验收标准

- 新人可以根据文档启动项目。
- 文档明确说明如何处理 Expo Router 路由和常见报错。

---

## 任务 1.4：主流程手动检查记录

### Codex 指令

```text
请新增 docs/manual-checklist.md，用于记录每次开发后的手动验收清单。
清单需要覆盖：启动、四个 Tab、日记新增、照片模拟上传、纪念日新增、AI 创建任务、我的统计、设置页、返回导航。
不要修改业务代码。
```

### 允许修改

- `docs/manual-checklist.md`
- `docs/project-file-structure.md`

### 验收标准

- 有明确可勾选清单。
- 后续每次开发可以按清单验证。

---

# Phase 2：前端 MVP 页面补齐

## 目标

在 mock 数据下形成完整可演示产品。

---

## 任务 2.1：首页记录中心完善

### Codex 指令

```text
请读取 docs/design-system-v1.md、docs/project-file-structure.md、src/store/useFairyStore.js、app/(tabs)/index.js。
本次只完善首页记录中心，不处理后端。
目标：让首页清楚展示恋爱天数、快捷入口、最近记录、回忆碎片墙，并能跳转到日记、照片、AI、纪念日相关页面。
页面必须保持童话绘本、奶油纸感、桃粉/干玫瑰/可可棕风格。
优先使用已有 FairyCard、FairyButton、FairyTag、MemoryWall 等组件。
完成后更新 docs/project-file-structure.md 中首页说明。
```

### 允许修改

- `app/(tabs)/index.js`
- `src/components/MemoryWall.js`
- `src/components/MemoryCard.js`
- `src/store/useFairyStore.js`，仅限补充必要 mock 字段
- `docs/project-file-structure.md`

### 验收标准

- 首页能展示记录。
- 首页快捷入口能跳转。
- 新增日记/照片后首页能更新。
- UI 风格统一。

---

## 任务 2.2：日记编辑与详情闭环

### Codex 指令

```text
请完善日记编辑和日记详情 mock 闭环。
读取 app/diary/editor.js、app/diary/detail.js、src/store/useFairyStore.js 和相关组件。
目标：用户能输入标题、正文、心情、标签；保存后写入 useFairyStore；跳转到详情页；详情页展示最近保存的日记，并提供“转成漫画”入口。
不要接后端，不要引入数据库。
需要加入基础输入校验和保存成功反馈。
完成后更新 docs/project-file-structure.md。
```

### 允许修改

- `app/diary/editor.js`
- `app/diary/detail.js`
- `src/store/useFairyStore.js`
- `src/components/FairyInput.js`
- `src/components/FairyButton.js`
- `docs/project-file-structure.md`

### 验收标准

- 空标题时有默认标题或提示。
- 保存后首页、情侣空间、我的统计同步更新。
- 详情页能看到保存内容。
- 文本转漫画入口可跳转。

---

## 任务 2.3：照片上传与相册闭环

### Codex 指令

```text
请完善照片上传和相册 mock 闭环。
读取 app/photo/upload.js、app/photo/album.js、src/store/useFairyStore.js。
当前阶段只做模拟上传，不接真实相册和 Storage。
目标：用户可填写照片标题、备注、标签、照片数量；保存后生成照片记录；相册页能以网格和时间线两种方式展示照片记录；空状态使用 FairyEmptyState。
完成后更新 docs/project-file-structure.md。
```

### 允许修改

- `app/photo/upload.js`
- `app/photo/album.js`
- `src/store/useFairyStore.js`
- `src/components/FairyEmptyState.js`
- `docs/project-file-structure.md`

### 验收标准

- 可新增模拟照片记录。
- 相册能展示照片记录。
- 网格/时间线切换可用。
- 首页和情侣空间同步更新。

---

## 任务 2.4：情侣空间完善

### Codex 指令

```text
请完善情侣空间页面。
读取 app/(tabs)/couple.js、src/components/CoupleTimeline.js、src/store/useFairyStore.js。
目标：展示情侣资料、恋爱天数、互动入口、纪念日入口、双人时间线。
时间线需要聚合日记、照片、纪念日、AI 作品的 mock 动态。
不要接真实后端。
完成后更新 docs/project-file-structure.md。
```

### 允许修改

- `app/(tabs)/couple.js`
- `src/components/CoupleTimeline.js`
- `src/store/useFairyStore.js`
- `docs/project-file-structure.md`

### 验收标准

- 情侣空间能展示动态流。
- 新增日记/照片/纪念日/AI 后时间线更新。
- 页面视觉符合设计系统。

---

## 任务 2.5：童话工坊与 AI mock 闭环

### Codex 指令

```text
请完善童话工坊和 AI mock 生成闭环。
读取 app/(tabs)/workshop.js、app/ai/comic-config.js、app/ai/video-config.js、app/ai/text-to-comic.js、app/ai/progress.js、src/store/useFairyStore.js。
目标：用户能从童话工坊进入漫画/视频/文本转漫画配置页，创建 mock AI 任务，进入进度页，进度页展示生成中状态和作品信息。
不要接真实 AI 服务。
完成后更新 docs/project-file-structure.md。
```

### 允许修改

- `app/(tabs)/workshop.js`
- `app/ai/comic-config.js`
- `app/ai/video-config.js`
- `app/ai/text-to-comic.js`
- `app/ai/progress.js`
- `src/store/useFairyStore.js`
- `docs/project-file-structure.md`

### 验收标准

- 可以创建漫画 mock 任务。
- 可以创建视频 mock 任务。
- 进度页能展示最新任务。
- 创作历史能更新。

---

## 任务 2.6：我的页面和统计完善

### Codex 指令

```text
请完善我的页面。
读取 app/(tabs)/mine.js 和 src/store/useFairyStore.js。
目标：展示用户资料、情侣统计、日记数量、照片数量、AI作品数量、纪念日数量，并提供设置、草稿箱、PDF导出、数据备份入口。
统计必须来自 useFairyStore.getStats()。
不要接后端。
完成后更新 docs/project-file-structure.md。
```

### 允许修改

- `app/(tabs)/mine.js`
- `src/store/useFairyStore.js`
- `docs/project-file-structure.md`

### 验收标准

- 统计随 mock 数据变化。
- 入口能跳转。
- 页面风格统一。

---

# Phase 3：组件系统完善

## 任务 3.1：新增 FairyPage 和 FairyHeader

### Codex 指令

```text
请新增 FairyPage 和 FairyHeader 组件。
读取 docs/design-system-v1.md、src/theme/*、现有 FairyCard/FairyButton。
FairyPage 用于统一 SafeArea、ScrollView、背景、页面内边距、底部 Tab 留白。
FairyHeader 用于统一页面标题、副标题、返回按钮、右侧操作。
先改造 2-3 个页面作为示例，不要一次性改全项目。
完成后更新 docs/project-file-structure.md 和 docs/design-system-v1.md。
```

### 允许修改

- `src/components/FairyPage.js`
- `src/components/FairyHeader.js`
- 2-3 个示例页面
- `docs/project-file-structure.md`
- `docs/design-system-v1.md`

### 验收标准

- 组件可复用。
- 示例页面正常显示。
- 没有破坏 Tab 布局。

---

## 任务 3.2：新增 FairyToast 和统一反馈

### Codex 指令

```text
请新增轻量 FairyToast 或统一反馈机制，用于保存成功、生成中、上传完成、失败提示。
当前阶段可先使用 React Native 状态实现，不必引入复杂库。
选择日记保存、照片上传、AI任务创建三个场景接入。
完成后更新 docs/design-system-v1.md。
```

### 允许修改

- `src/components/FairyToast.js`
- `app/diary/editor.js`
- `app/photo/upload.js`
- `app/ai/comic-config.js`
- `docs/design-system-v1.md`

### 验收标准

- 用户操作后有反馈。
- 样式符合童话绘本风格。

---

## 任务 3.3：完善 FairyImage 和图片资产接入

### Codex 指令

```text
请完善 FairyImage 组件和图片资产接入规范。
读取 docs/image-assets-guideline.md。
目标：通过 name 映射使用图片，如 homeCover、coupleCover、workshopCover；如果真实图片不存在，则 fallback 到 FairyIllustration。
不要直接在页面散落 require 图片。
先在首页、情侣空间、童话工坊三个页面接入。
完成后更新 docs/image-assets-guideline.md。
```

### 允许修改

- `src/components/FairyImage.js`
- `src/components/FairyIllustration.js`
- `app/(tabs)/index.js`
- `app/(tabs)/couple.js`
- `app/(tabs)/workshop.js`
- `docs/image-assets-guideline.md`

### 验收标准

- 页面通过 `FairyImage name="xxx"` 使用图片。
- 没有图片时不报错。
- fallback 显示正常。

---

# Phase 4：API 层和 mock/real 模式

## 任务 4.1：完善 API client

### Codex 指令

```text
请完善 src/api/client.js。
目标：支持 EXPO_PUBLIC_API_MODE=mock/real，提供 isMockMode、delay、requestMock、normalizeError 等基础函数。
不要接 Supabase，只预留 createSupabaseClient 占位或注释。
完成后更新 docs/backend-and-api-plan.md。
```

### 允许修改

- `src/api/client.js`
- `.env.example`
- `docs/backend-and-api-plan.md`

### 验收标准

- mock 模式可用。
- 不需要真实 Supabase 也不报错。

---

## 任务 4.2：建立 diaryApi/photoApi/anniversaryApi

### Codex 指令

```text
请建立或完善 diaryApi、photoApi、anniversaryApi。
当前只实现 mock 模式，函数名和返回结构要贴近未来真实接口。
然后逐步让日记、照片、纪念日页面通过 API 层调用，而不是直接写死 mock 数据。
不要接 Supabase。
完成后更新 docs/backend-and-api-plan.md。
```

### 允许修改

- `src/api/diaryApi.js`
- `src/api/photoApi.js`
- `src/api/anniversaryApi.js`
- 相关页面少量调用方式
- `docs/backend-and-api-plan.md`

### 验收标准

- 页面仍能正常工作。
- API 返回结构稳定。
- 后续 real 模式能替换实现。

---

## 任务 4.3：建立 aiApi/coupleApi/storageApi

### Codex 指令

```text
请建立或完善 aiApi、coupleApi、storageApi。
aiApi 提供 createComicJob、createVideoJob、getAiJobDetail、getAiCreationHistory。
coupleApi 提供 getCoupleInfo、createInviteCode、bindCouple、getCoupleTimeline。
storageApi 当前只提供 mock uploadImage、getSignedUrl、deleteFile。
不要接真实后端。
完成后更新 docs/backend-and-api-plan.md。
```

### 允许修改

- `src/api/aiApi.js`
- `src/api/coupleApi.js`
- `src/api/storageApi.js`
- `docs/backend-and-api-plan.md`

### 验收标准

- API 函数可被页面调用。
- mock 返回结构与后端规划一致。

---

# Phase 5：Supabase 后端接入

## 任务 5.1：新增 Supabase SQL 结构

### Codex 指令

```text
请根据 docs/backend-and-api-plan.md 新增 supabase/schema.sql。
包含 profiles、couples、diaries、photos、anniversaries、ai_jobs、comments、notifications 表。
字段请按文档规划，补充 created_at、updated_at、必要索引。
不要在前端写真实 Supabase key。
完成后更新 docs/backend-and-api-plan.md。
```

### 允许修改

- `supabase/schema.sql`
- `docs/backend-and-api-plan.md`

### 验收标准

- SQL 结构完整。
- couple 相关表都有 `couple_id`。
- 常用查询字段有索引。

---

## 任务 5.2：新增 RLS 策略

### Codex 指令

```text
请新增 supabase/rls-policies.sql。
目标：用户只能访问自己的 profile，只能访问自己 active couple 内的数据。
为 profiles、couples、diaries、photos、anniversaries、ai_jobs、comments、notifications 编写基础 RLS 策略。
同时更新 docs/backend-and-api-plan.md 说明 RLS 规则。
```

### 允许修改

- `supabase/rls-policies.sql`
- `docs/backend-and-api-plan.md`

### 验收标准

- 每张核心表都启用 RLS。
- 不允许跨 couple 访问数据。

---

## 任务 5.3：接入 Supabase client 和 Auth

### Codex 指令

```text
请接入 @supabase/supabase-js。
完善 src/api/client.js 和新增 src/api/authApi.js。
登录页先支持最简单的邮箱登录或验证码登录，具体实现以 Expo 端可运行为准。
要求 mock 模式仍然可用；real 模式才使用 Supabase。
不要提交真实 key。
完成后更新 docs/dev-runbook.md 和 docs/backend-and-api-plan.md。
```

### 允许修改

- `package.json`
- `src/api/client.js`
- `src/api/authApi.js`
- `app/login.js`
- `.env.example`
- `docs/dev-runbook.md`
- `docs/backend-and-api-plan.md`

### 验收标准

- mock 模式不受影响。
- real 模式可以创建 Supabase client。
- 登录页有基础登录流程。

---

# Phase 6：核心业务真实化

## 任务 6.1：日记真实 CRUD

### Codex 指令

```text
请将 diaryApi 从 mock 扩展为 mock/real 双模式。
real 模式使用 Supabase diaries 表。
实现 getDiaryList、createDiary、getDiaryDetail、updateDiary、deleteDiary。
页面仍通过 diaryApi 调用，不要直接在页面里写 Supabase 查询。
完成后更新 docs/backend-and-api-plan.md 和 docs/project-file-structure.md。
```

### 验收标准

- mock 模式可用。
- real 模式可对 diaries 表增删改查。
- 页面代码不直接依赖 Supabase。

---

## 任务 6.2：照片真实上传

### Codex 指令

```text
请接入 Expo ImagePicker 和 Supabase Storage，实现照片真实上传的第一版。
photoApi real 模式负责上传图片并写入 photos 表。
页面只调用 photoApi.uploadPhoto。
需要处理权限拒绝、上传中、上传失败、上传成功。
完成后更新 docs/image-assets-guideline.md 和 docs/backend-and-api-plan.md。
```

### 验收标准

- 用户能选择本地图片。
- 图片能上传 Storage。
- photos 表有记录。
- 相册能读取真实照片。

---

## 任务 6.3：情侣绑定真实流程

### Codex 指令

```text
请实现情侣绑定真实流程。
包含 createInviteCode、bindCouple、getCoupleInfo。
A 用户生成邀请码，B 用户输入邀请码后绑定，couples.status 变为 active。
绑定后两人共享同一个 couple_id。
不要破坏 mock 模式。
完成后更新 docs/backend-and-api-plan.md 和 docs/project-file-structure.md。
```

### 验收标准

- 两个账号可以绑定。
- 绑定后能读取同一个情侣空间数据。
- 未绑定用户有引导状态。

---

# Phase 7：AI 创作系统

## 任务 7.1：AI job 后端任务骨架

### Codex 指令

```text
请新增 Supabase Edge Function 骨架 create-ai-comic-job 和 create-ai-video-job。
当前先不接真实 AI 供应商，只完成身份验证、couple 权限验证、创建 ai_jobs 记录、返回 jobId。
不要把任何 AI Key 写入前端。
完成后更新 docs/backend-and-api-plan.md。
```

### 验收标准

- Edge Function 有清晰输入输出。
- 能创建 ai_jobs。
- 前端不出现服务端密钥。

---

## 任务 7.2：AI 进度真实化

### Codex 指令

```text
请让 aiApi real 模式可以创建 AI job，并查询 job 详情。
进度页读取 getAiJobDetail，展示 pending/processing/done/failed。
当前可以用模拟进度更新或数据库状态，不必接真实 AI 生成。
完成后更新 docs/project-file-structure.md。
```

### 验收标准

- 前端能创建真实 ai_jobs。
- 进度页能显示真实任务状态。
- mock 模式仍可用。

---

# Phase 8：导出、备份与分享

## 任务 8.1：PDF 导出骨架

### Codex 指令

```text
请实现 PDF 导出功能骨架。
前端 data/pdf-export 页面负责选择范围、内容类型和模板。
后端 Edge Function export-memory-pdf 先提供骨架，可以返回 mock signed URL 或任务 ID。
不要一次性实现复杂 PDF 排版。
完成后更新 docs/backend-and-api-plan.md。
```

### 验收标准

- 前端流程可走通。
- 后端函数有明确输入输出。
- 后续可以替换真实 PDF 生成。

---

## 任务 8.2：分享预览页

### Codex 指令

```text
请新增或完善分享预览页。
支持从日记、纪念日、AI作品生成一张童话绘本风格分享卡片预览。
当前只做前端预览，不接真实分享 SDK。
完成后更新 docs/project-file-structure.md。
```

### 验收标准

- 分享卡片视觉统一。
- 至少支持一种内容类型。
- 后续可以接系统分享能力。

---

# Phase 9：上线准备

## 任务 9.1：隐私与权限说明

### Codex 指令

```text
请新增 docs/privacy-and-permissions.md。
说明项目会使用的权限：相册、通知、网络、存储，并写清使用目的。
检查 app.json 中是否需要配置权限说明。
不要编写正式法律文本，只写开发阶段说明。
```

### 验收标准

- 权限用途清晰。
- 后续上架有准备材料。

---

## 任务 9.2：性能和上线检查清单

### Codex 指令

```text
请新增 docs/release-checklist.md。
包含：启动速度、图片体积、列表性能、错误监控、隐私政策、用户协议、App 图标、启动页、iOS/Android 适配、测试账号、上架截图等检查项。
```

### 验收标准

- 上线前有完整检查清单。

---

## 10. 推荐执行顺序

强烈建议按以下顺序执行：

```text
1. Phase 1.1 启动配置检查
2. Phase 1.2 .env.example
3. Phase 1.3 dev-runbook
4. Phase 1.4 manual-checklist
5. Phase 2.1 首页
6. Phase 2.2 日记
7. Phase 2.3 照片
8. Phase 2.4 情侣空间
9. Phase 2.5 AI mock
10. Phase 2.6 我的页面
11. Phase 3 组件系统
12. Phase 4 API mock/real
13. Phase 5 Supabase
14. Phase 6 真实业务
15. Phase 7 AI
16. Phase 8 导出分享
17. Phase 9 上线准备
```

---

## 11. 每次 Codex 完成后的固定检查

每次 Codex 完成任务后，都要求它输出：

```text
1. 本次修改文件列表
2. 本次完成内容
3. 未完成内容
4. 如何验证
5. 是否更新文档
6. 下一步建议
```

如果 Codex 没有更新文档，需要让它补充文档后再进入下一项任务。