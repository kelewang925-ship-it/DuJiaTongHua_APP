# 《独家童话》APP 项目完整开发计划与进度记录

> 更新时间：2026-05-26  
> 仓库：`kelewang925-ship-it/DuJiaTongHua_APP`  
> 执行方式：后续主要通过 Codex 按阶段开发  
> 文档目标：让 Codex、开发者、后续接手人员都能明确知道“现在做到哪里、下一步做什么、具体改哪些文件、怎么验收”。

---

## 0. 如何使用本文档

本文档是项目总计划，不是普通说明文。后续每次开发前都应该先看本文档，再看 `docs/codex-development-roadmap.md`。

推荐使用方式：

1. 先看第 3 节，确认当前项目进度。
2. 再看第 5 节，确定当前处于哪个 Phase。
3. 打开 `docs/codex-development-roadmap.md`，复制对应阶段的 Codex 任务提示词。
4. 让 Codex 只处理当前阶段，不要一次性跨多个阶段大改。
5. 每完成一个阶段，都要更新本文档的任务状态。
6. 新增页面、组件、API、图片、后端表，都必须同步更新对应文档。

后续开发强制规则：

```text
一次只做一个明确阶段。
一次只完成一个可验证闭环。
每次提交都要说明：改了什么、为什么改、怎么验证。
```

---

## 1. 项目定位

《独家童话》是一款面向情侣的情感记录与 AI 创作 APP。它不是普通相册，也不是普通日记，而是把情侣日常、照片、纪念日、互动和 AI 创作沉淀成一本持续生长的“恋爱童话绘本”。

核心价值：

- 让情侣低成本记录日常。
- 让普通照片和文字变成更有情绪价值的作品。
- 让两个人共同拥有一个长期回忆空间。
- 通过 AI 把日记、照片转成漫画、视频、纪念册。

产品关键词：

- 情侣共同记录
- 童话绘本视觉
- 奶油纸感 UI
- 桃粉 / 干玫瑰 / 可可棕 / 琥珀金
- 轻手绘贴纸组件
- AI 漫画 / AI 视频 / PDF 纪念册
- 双人时间线
- 回忆碎片墙
- 情绪价值

---

## 2. 当前技术栈

当前项目是 Expo React Native 前端项目。

已确认技术栈：

- React Native
- Expo
- Expo Router
- JavaScript
- Zustand
- Expo Vector Icons
- Expo Blur
- Expo Linear Gradient
- React Native SVG
- React Native Reanimated
- React Native Gesture Handler

当前启动方式：

```bash
npm install
npm run start
npm run android
npm run ios
npm run web
```

后续建议补充：

- ESLint
- Prettier
- `.env.example`
- Supabase JS SDK
- Expo ImagePicker
- Expo FileSystem
- Expo Sharing
- Sentry 或 Expo Error Reporting

---

## 3. 当前项目进度判断

### 3.1 当前阶段结论

当前项目处于：

```text
MVP 前端原型已搭建 + 设计系统已建立 + mock 数据业务闭环已初步跑通 + 后端/API 仍处于规划阶段
```

项目已经不是空项目，不应该推倒重来。后续应该围绕现有结构持续补齐。

当前最重要的判断：

```text
先把前端 mock MVP 做稳定，再接 Supabase 后端；不要一开始就同时改 UI、状态、后端、AI。
```

### 3.2 已完成内容

#### 工程基础

- 已初始化 Expo React Native 项目。
- 已配置 Expo Router 作为页面路由入口。
- 已建立 `app/` 路由目录。
- 已建立 `src/components/` 复用组件目录。
- 已建立 `src/theme/` 设计 token 目录。
- 已建立 `src/store/` Zustand 状态管理目录。
- 已建立 `src/data/` mock 数据目录。
- 已建立 `src/api/` API 抽象目录。
- 已建立 `docs/` 文档目录。

#### 设计与视觉

- 已形成《独家童话》的第一版 Design System。
- 已明确品牌视觉方向：童话绘本、奶油纸感、手绘贴纸、温柔 AI 魔法感。
- 已建立颜色、字体、圆角、阴影、间距等基础规范。
- 已创建多个 SVG 设计稿和设计索引。
- 已新增图片资产规范文档，明确图片目录、命名、尺寸、格式和接入方式。

#### 页面与路由

已记录或实现的主要路由包括：

- 登录页：`app/login.js`
- 首页：`app/(tabs)/index.js`
- 情侣空间：`app/(tabs)/couple.js`
- 童话工坊：`app/(tabs)/workshop.js`
- 我的：`app/(tabs)/mine.js`
- 日记编辑：`app/diary/editor.js`
- 日记详情：`app/diary/detail.js`
- 照片上传：`app/photo/upload.js`
- 相册浏览：`app/photo/album.js`
- AI 漫画配置：`app/ai/comic-config.js`
- AI 视频配置：`app/ai/video-config.js`
- 文本转漫画：`app/ai/text-to-comic.js`
- AI 生成进度：`app/ai/progress.js`
- 纪念日管理：`app/anniversary/index.js`
- 数据备份：`app/data/backup.js`
- PDF 导出：`app/data/pdf-export.js`
- 设置、草稿箱、帮助反馈等辅助页面。

#### 状态管理

`src/store/useFairyStore.js` 已建立核心状态：

- `couple`：情侣资料
- `records`：记录流
- `timeline`：情侣动态
- `creations`：AI 作品
- `anniversaries`：纪念日
- `draftDiary`：日记草稿

已具备的业务方法：

- `updateDraftDiary`
- `resetDraftDiary`
- `addDiaryRecord`
- `addPhotoRecord`
- `addAnniversary`
- `addCreation`
- `getStats`

当前已经形成以下 mock 业务闭环：

```text
写日记 → records + timeline + 我的统计
上传照片 → records + timeline + 我的统计
添加纪念日 → anniversaries + timeline
创建 AI 作品 → creations + timeline + 生成进度页
```

#### 后端/API 规划

已存在后端与 API 规划文档，推荐使用 Supabase：

- Supabase Auth
- Supabase PostgreSQL
- Supabase Storage
- Supabase Edge Functions
- Supabase Realtime

已规划数据表：

- profiles
- couples
- diaries
- photos
- anniversaries
- ai_jobs
- comments
- notifications

---

## 4. 当前未完成内容

### 4.1 工程层未完成

- 尚未确认真实构建是否全部通过。
- 尚未补充 lint、format、测试脚本。
- 尚未建立 `.env.example`。
- 尚未建立 API mock/real 模式开关。
- 尚未建立统一错误处理。
- 尚未建立统一 loading / empty / error / retry 状态。
- 尚未建立开发运行手册。

### 4.2 前端功能未完成

- 部分页面仍只是视觉或流程占位。
- 相册、搜索、评论、通知、分享、会员等功能仍需实现。
- 输入校验、删除确认、保存反馈、失败提示需要补齐。
- 页面之间的数据传递需要统一规范。
- 部分页面需要从大文件拆分成 `src/screens` 或组件。

### 4.3 后端真实能力未完成

- 登录仍需接入真实 Auth。
- 情侣绑定流程仍需接入真实邀请码 / 二维码 / 关系状态。
- 日记、照片、纪念日、AI 作品仍主要依赖本地 mock 或 Zustand 内存状态。
- 照片上传还未接入真实相册权限、图片选择、压缩、上传和存储。
- AI 漫画 / AI 视频未接入真实 AI 服务。
- PDF 导出未接入真实服务端生成逻辑。

### 4.4 设计资产未完成

- 真实页面插画资产仍需要拆分、生成、压缩和接入。
- `FairyImage` 需要成为统一图片入口。
- 首页、情侣空间、童话工坊等核心插画需要逐步替换 fallback 绘制效果。

---

## 5. 后续开发总路线

项目建议按 9 个阶段推进。每个阶段都必须做到：

- 有明确目标。
- 有明确文件范围。
- 有明确验收标准。
- 有明确 Codex 指令。
- 完成后更新文档。

---

# Phase 1：项目稳定化与运行检查

## 目标

确保当前项目可以被任何开发者拉下来运行，并能完整打开主要页面。

## 处理内容

1. 安装依赖并启动项目。
2. 检查 Expo Router 路由。
3. 修复启动报错、路径错误、组件引用错误。
4. 增加基础工程配置。
5. 建立运行手册。

## 重点文件

- `package.json`
- `app/_layout.js`
- `app/(tabs)/_layout.js`
- `docs/dev-runbook.md`
- `.env.example`
- `.gitignore`

## 具体做法

1. 执行：

```bash
npm install
npm run start
```

2. 逐个点击页面：

- 首页
- 情侣空间
- 童话工坊
- 我的
- 日记编辑
- 照片上传
- AI 配置
- 纪念日
- 设置

3. 如果出现 `Unable to resolve module`：

- 检查 import 路径。
- 检查文件是否存在。
- 优先修复路径，不要重复创建同名组件。

4. 如果出现 Expo Router 路由错误：

- 检查 `app/` 文件路径。
- 检查 `_layout.js`。
- 检查跳转路径是否与文件路径一致。

5. 新增 `.env.example`：

```bash
EXPO_PUBLIC_API_MODE=mock
EXPO_PUBLIC_SUPABASE_URL=
EXPO_PUBLIC_SUPABASE_ANON_KEY=
```

6. 新增 `docs/dev-runbook.md`，记录：

- 启动方式
- 常见报错
- 路由规则
- 新增页面规则
- 提交前检查清单

## 验收标准

- `npm run start` 可以启动。
- 四个 Tab 可以正常切换。
- 主要二级页面可以进入和返回。
- 文档中记录了启动步骤。
- `.env.example` 存在。

---

# Phase 2：前端 MVP 页面补齐

## 目标

在 mock 数据下，把 APP 做成一个完整可演示产品。

## 处理内容

P0 页面必须优先完成：

1. 登录页
2. 首页 / 记录中心
3. 情侣空间
4. 童话工坊
5. 我的页面
6. 日记编辑与详情
7. 照片上传与相册
8. 纪念日管理
9. AI 漫画配置
10. AI 生成进度

P1 页面随后完成：

1. 文本转漫画
2. AI 视频配置
3. 视频预览编辑
4. 草稿箱
5. 设置页
6. 帮助反馈
7. 数据备份
8. PDF 导出配置

P2 页面最后完成：

1. 搜索页
2. 评论列表
3. 互动通知
4. 会员权益
5. 分享预览
6. 存储空间管理

## 重点文件

- `app/(tabs)/index.js`
- `app/(tabs)/couple.js`
- `app/(tabs)/workshop.js`
- `app/(tabs)/mine.js`
- `app/diary/editor.js`
- `app/diary/detail.js`
- `app/photo/upload.js`
- `app/photo/album.js`
- `app/anniversary/index.js`
- `app/ai/comic-config.js`
- `app/ai/progress.js`
- `src/store/useFairyStore.js`

## 具体做法

1. 先保证所有 P0 页面存在。
2. 页面顶部统一使用童话绘本风格标题区。
3. 页面背景统一使用月白纸感。
4. 卡片统一使用 `FairyCard`。
5. 按钮统一使用 `FairyButton`。
6. 输入统一使用 `FairyInput`。
7. 空数据统一使用 `FairyEmptyState`。
8. 操作后必须给用户反馈：保存成功、生成中、上传完成等。
9. 不接真实后端，仍使用 Zustand 和 mock 数据。

## 验收标准

- P0 页面全部能进入。
- 日记可以新建并出现在首页和情侣空间。
- 照片可以模拟上传并出现在首页和相册。
- 纪念日可以新增并出现在情侣空间。
- AI 漫画任务可以创建并进入进度页。
- 我的页面统计能随 mock 数据变化。

---

# Phase 3：组件系统完善

## 目标

把页面中重复 UI 抽成可复用组件，形成稳定的童话绘本组件库。

## 必须完善的组件

- `FairyCard`
- `FairyButton`
- `FairyTag`
- `FairyInput`
- `FairyDialog`
- `FairyEmptyState`
- `FairyTabBar`
- `FairyBackButton`
- `FairyImage`
- `MemoryWall`
- `CoupleTimeline`
- `WorkshopCard`
- `MemoryCard`

## 建议新增组件

- `FairyPage`
- `FairyHeader`
- `FairySectionTitle`
- `FairyLoading`
- `FairyToast`
- `FairyActionSheet`
- `FairyUploadCard`
- `FairyProgressCard`
- `FairyTimelineNode`
- `FairySticker`

## 具体做法

1. 建立 `FairyPage`：统一 SafeArea、ScrollView、背景色、底部留白。
2. 建立 `FairyHeader`：统一页面标题、副标题、右侧操作。
3. 建立 `FairyLoading`：用于 AI 生成、上传、页面加载。
4. 建立 `FairyToast`：用于保存成功、失败提示。
5. 建立 `FairyImage`：统一图片映射、fallback、圆角和 resizeMode。
6. 替换页面中重复 View、Text、TouchableOpacity 样式。
7. 每新增组件必须写清 props 和使用场景。

## 验收标准

- 新建页面时可以直接用组件搭建。
- 页面内重复样式明显减少。
- 组件风格统一，不出现突兀的默认系统 UI。

---

# Phase 4：API 层和 mock/real 模式

## 目标

在不破坏当前前端体验的前提下，把数据访问统一收口到 `src/api/`。

## 处理内容

1. 建立统一 API client。
2. 增加 mock/real 模式判断。
3. 页面逐步停止直接操作 mock 数据。
4. 为后续 Supabase 接入预留一致函数。

## 重点文件

- `src/api/client.js`
- `src/api/diaryApi.js`
- `src/api/photoApi.js`
- `src/api/anniversaryApi.js`
- `src/api/coupleApi.js`
- `src/api/aiApi.js`
- `src/api/storageApi.js`
- `.env.example`

## 具体做法

`src/api/client.js` 应包含：

```js
export const API_MODE = process.env.EXPO_PUBLIC_API_MODE || 'mock';
export const isMockMode = () => API_MODE !== 'real';
export const delay = (ms = 300) => new Promise((resolve) => setTimeout(resolve, ms));
export const requestMock = async (data, ms = 300) => {
  await delay(ms);
  return data;
};
```

每个 API 模块先提供 mock 函数，函数名保持真实后端可替换：

- `getDiaryList`
- `createDiary`
- `getDiaryDetail`
- `updateDiary`
- `deleteDiary`
- `uploadPhoto`
- `getAlbumList`
- `createAnniversary`
- `createComicJob`
- `getAiJobDetail`

## 验收标准

- 页面不直接知道 Supabase。
- API 模块 mock 返回的数据结构和未来真实接口一致。
- 后续切换真实接口时，页面改动最小。

---

# Phase 5：Supabase 后端接入

## 目标

接入真实登录、数据库、存储和权限规则。

## 处理内容

1. 创建 Supabase 项目。
2. 建立数据库表。
3. 开启 RLS。
4. 建立 Storage buckets。
5. 接入 Auth。
6. 改造 API 层为真实请求。

## 重点表

- `profiles`
- `couples`
- `diaries`
- `photos`
- `anniversaries`
- `ai_jobs`
- `comments`
- `notifications`

## 重点文件

- `src/api/client.js`
- `src/api/authApi.js`
- `src/api/coupleApi.js`
- `src/api/diaryApi.js`
- `src/api/photoApi.js`
- `src/api/anniversaryApi.js`
- `src/api/aiApi.js`
- `docs/backend-and-api-plan.md`
- `supabase/schema.sql`，建议新增
- `supabase/rls-policies.sql`，建议新增

## 具体做法

1. 安装 Supabase：

```bash
npm install @supabase/supabase-js
```

2. 在 `.env` 中配置：

```bash
EXPO_PUBLIC_API_MODE=real
EXPO_PUBLIC_SUPABASE_URL=xxx
EXPO_PUBLIC_SUPABASE_ANON_KEY=xxx
```

3. `src/api/client.js` 创建 Supabase client。
4. 登录页先支持最简单的邮箱验证码或邮箱密码。
5. 登录后创建或读取 profile。
6. 所有 couple 数据必须带 `couple_id`。
7. 所有表上线前必须开启 RLS。

## 验收标准

- 用户可以登录。
- 登录状态可以保持。
- 用户只能读取自己的 profile。
- 用户只能读取自己情侣关系内的数据。
- mock mode 仍然可用。

---

# Phase 6：核心业务真实化

## 目标

把日记、照片、纪念日、情侣空间从 mock 数据替换成真实数据。

## 处理内容

1. 日记 CRUD。
2. 照片上传。
3. 情侣绑定。
4. 纪念日 CRUD。
5. 情侣时间线聚合。
6. 我的页面统计真实化。

## 具体做法

### 日记

- `createDiary(payload)` 写入 `diaries`。
- `getDiaryList(coupleId)` 获取当前情侣记录。
- `getDiaryDetail(id)` 获取详情。
- `updateDiary(id, payload)` 编辑。
- `deleteDiary(id)` 删除。

### 照片

- 使用 Expo ImagePicker 选择图片。
- 上传到 Supabase Storage。
- 写入 `photos` 表。
- 相册从 `photos` 表读取。

### 情侣绑定

- A 用户生成邀请码。
- B 用户输入邀请码。
- B 用户确认绑定。
- `couples.status` 变为 `active`。
- 双方进入同一个 `couple_id` 数据空间。

### 纪念日

- 新增、编辑、删除纪念日。
- 自动计算已过天数或倒计时。

## 验收标准

- 两个真实账号可以绑定为情侣。
- 一方写日记，另一方能看到。
- 一方上传照片，另一方能看到。
- 刷新 App 数据不丢失。

---

# Phase 7：AI 创作系统

## 目标

把童话工坊从模拟入口变成真实 AI 生成能力。

## 处理内容

1. AI 任务表。
2. Edge Functions。
3. AI 供应商调用。
4. 前端进度轮询或 Realtime。
5. 结果存储和预览。
6. 失败重试。

## 重点文件

- `src/api/aiApi.js`
- `app/ai/comic-config.js`
- `app/ai/video-config.js`
- `app/ai/progress.js`
- `app/ai/video-preview.js`
- `supabase/functions/create-ai-comic-job/index.ts`
- `supabase/functions/create-ai-video-job/index.ts`

## 具体做法

1. 前端创建任务，只传素材、文本、风格，不传 AI Key。
2. Edge Function 验证用户身份。
3. Edge Function 验证用户是否属于当前 couple。
4. Edge Function 创建 `ai_jobs`。
5. Worker 或异步函数调用 AI 服务。
6. 生成结果上传 Storage。
7. 更新 `ai_jobs.status` 和 `progress`。
8. 前端进度页轮询或监听 Realtime。

## 验收标准

- 用户可以从日记生成漫画任务。
- 任务有真实状态变化。
- 生成成功后可以看到结果。
- 失败时有错误提示和重试入口。
- AI Key 不出现在前端。

---

# Phase 8：导出、备份与分享

## 目标

让用户可以把回忆导出、保存和分享。

## 处理内容

1. PDF 纪念册导出。
2. 数据备份。
3. 分享预览。
4. 存储空间管理。

## 具体做法

### PDF 导出

- 前端选择时间范围。
- 前端选择内容类型：日记、照片、纪念日、AI 作品。
- 前端选择模板。
- Edge Function 生成 PDF。
- PDF 上传到 `exports` bucket。
- 返回 signed URL。

### 分享预览

- 生成分享卡片。
- 支持单条日记、照片、纪念日、AI 作品。
- 优先实现图片分享，再做链接分享。

### 备份

- 支持查看数据量。
- 支持导出 JSON。
- 后续支持云端备份恢复。

## 验收标准

- 可以导出一本基础 PDF。
- 可以分享单条内容。
- 可以查看存储使用情况。

---

# Phase 9：上线准备

## 目标

达到内测或正式上架前状态。

## 处理内容

1. 用户协议。
2. 隐私政策。
3. 错误监控。
4. 性能优化。
5. 适配测试。
6. App 图标和启动页。
7. 内测分发。
8. 上架素材。

## 具体做法

1. 检查所有隐私权限说明。
2. 配置相册权限文案。
3. 配置通知权限文案。
4. 优化长列表性能。
5. 压缩图片资源。
6. 检查 Android 和 iOS 安全区。
7. 准备应用截图、介绍文案、隐私说明。

## 验收标准

- 核心流程无明显崩溃。
- 权限申请文案清晰。
- 用户数据有基本安全保障。
- 可以交给真实用户内测。

---

## 6. Codex 开发总原则

后续使用 Codex 时，必须遵守以下原则：

1. 不要让 Codex 一次性完成整个项目。
2. 每次只给 Codex 一个阶段或一个功能闭环。
3. 每次任务必须告诉 Codex：
   - 当前目标
   - 允许修改的文件
   - 不允许修改的文件
   - 验收标准
   - 提交信息
4. 让 Codex 修改前先读取相关文档。
5. 让 Codex 完成后更新文档。
6. 让 Codex 每次提交前运行项目或至少检查 import 路径。
7. 涉及后端密钥时，只能写 `.env.example`，不能写真实 key。
8. 涉及 AI 服务时，所有 key 必须在服务端。
9. 涉及数据库时，必须同步写 SQL 和 RLS 策略。
10. 涉及图片资产时，必须更新图片规范文档。

---

## 7. 当前下一步最建议执行

下一步不要直接接 AI，也不要直接做 PDF。建议从 Phase 1 开始：

```text
Phase 1：项目稳定化与运行检查
```

第一条 Codex 任务建议是：

```text
请读取 docs/project-development-master-plan.md、docs/project-file-structure.md、docs/design-system-v1.md、docs/backend-and-api-plan.md，然后只处理 Phase 1：项目稳定化与运行检查。请检查项目启动配置、路由结构、import 路径、缺失文件，新增 .env.example 和 docs/dev-runbook.md。不要接入真实后端，不要改视觉风格，不要重构大页面。完成后更新 docs/project-development-master-plan.md 的 Phase 1 状态，并给出验证步骤。
```

---

## 8. 文档维护规则

每次开发必须维护文档：

| 改动类型 | 必须更新的文档 |
| --- | --- |
| 新增页面 | `docs/project-file-structure.md` |
| 新增组件 | `docs/project-file-structure.md`、`docs/design-system-v1.md` |
| 新增图片 | `docs/image-assets-guideline.md` |
| 新增 API | `docs/backend-and-api-plan.md` |
| 新增数据库表 | `docs/backend-and-api-plan.md`、SQL 文件 |
| 新增阶段成果 | `docs/project-development-master-plan.md` |
| 新增 Codex 任务 | `docs/codex-development-roadmap.md` |

---

## 9. 当前任务看板

### Now

- [ ] Phase 1：运行检查
- [ ] 新增 `.env.example`
- [ ] 新增 `docs/dev-runbook.md`
- [ ] 检查所有 Tab 和 P0 页面
- [ ] 修复启动和路由问题

### Next

- [ ] Phase 2：前端 MVP 页面补齐
- [ ] Phase 3：组件系统完善
- [ ] Phase 4：API mock/real 模式

### Later

- [ ] Phase 5：Supabase 接入
- [ ] Phase 6：核心业务真实化
- [ ] Phase 7：AI 创作系统
- [ ] Phase 8：导出、备份与分享
- [ ] Phase 9：上线准备

---

## 10. 当前版本状态一句话

《独家童话》APP 当前已经完成产品方向、设计系统、核心页面结构、mock 数据闭环和后端规划；接下来应使用 Codex 按阶段推进，先做项目稳定化和前端 MVP，再逐步接入 Supabase、真实业务、AI 生成、导出分享和上线能力。

---

## Phase 1 进度记录

### 2026-05-26 Phase 1.1

- 已将 `package.json` 和 `package-lock.json` 中的浮动 `latest` 依赖固定为当前已解析的 Expo / React Native 版本，降低后续安装漂移风险。
- 已检查 `app/_layout.js`、`app/(tabs)/_layout.js` 和 `app/`、`src/` 下活动本地 import 路径。
- 已使用本机 Node 24.3.0 验证启动，并修复本机 `.expo/dev/logs/start.log` 缓存权限问题。
- 已重新启动 Expo，Metro 正常启动并输出 `http://localhost:8099`；`.expo/` 属于本地生成缓存，不提交仓库。

### 2026-05-26 Phase 1.2

- 已新增 `.env.example`，包含 mock API 模式和 Supabase 占位变量。
- 已确认 `.gitignore` 忽略 `.env` 和 `.env.local`。
- 未写入任何真实密钥。
