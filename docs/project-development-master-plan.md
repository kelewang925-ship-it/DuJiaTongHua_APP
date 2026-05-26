# 《独家童话》APP 项目完整开发计划与进度记录

> 更新时间：2026-05-26  
> 仓库：`kelewang925-ship-it/DuJiaTongHua_APP`  
> 目标：让后续开发可以直接接着当前进度继续推进，避免重复梳理项目背景、设计方向、技术架构和待办任务。

---

## 1. 项目定位

《独家童话》是一款面向情侣的情感记录与 AI 创作 APP。核心不是普通相册或普通日记，而是把两个人的日常、照片、纪念日和互动记录，整理成具有童话绘本感的专属回忆空间，并进一步通过 AI 生成漫画、视频、PDF 绘本等可收藏内容。

产品关键词：

- 情侣共同记录
- 童话绘本视觉
- 奶油纸感 UI
- 桃粉 / 干玫瑰 / 可可棕 / 琥珀金
- 轻手绘贴纸组件
- AI 漫画 / AI 视频 / PDF 纪念册
- 双人时间线和回忆碎片墙

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

---

## 3. 当前项目进度判断

### 3.1 当前阶段结论

当前项目处于：

```text
MVP 前端原型已搭建 + 设计系统已建立 + mock 数据业务闭环已初步跑通 + 后端/API 仍处于规划阶段
```

也就是说，现在已经不是空项目，已经具备继续开发的基础。后续重点不是从零开始，而是按模块把 mock 原型逐步替换为真实功能。

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

`src/store/useFairyStore.js` 已经建立核心状态：

- couple：情侣资料
- records：记录流
- timeline：情侣动态
- creations：AI 作品
- anniversaries：纪念日
- draftDiary：日记草稿

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

已规划 API 模块：

- `src/api/client.js`
- `src/api/photoApi.js`
- `src/api/aiApi.js`
- `src/api/diaryApi.js`
- `src/api/anniversaryApi.js`
- `src/api/coupleApi.js`
- `src/api/storageApi.js`

---

## 4. 当前未完成内容

### 4.1 工程层未完成

- 尚未确认真实构建是否全部通过。
- 尚未补充 lint、format、类型检查或测试脚本。
- 尚未建立 `.env` 环境变量规范。
- 尚未建立正式的错误边界、加载态、空状态和失败重试统一机制。
- 尚未建立统一网络请求错误处理。

### 4.2 真实业务能力未完成

- 登录仍需接入真实 Auth。
- 情侣绑定流程仍需接入真实邀请码 / 二维码 / 关系状态。
- 日记、照片、纪念日、AI 作品仍主要依赖本地 mock 或 Zustand 内存状态。
- 照片上传还未接入真实相册权限、图片选择、压缩、上传和存储。
- AI 漫画 / AI 视频目前是生成任务原型，未接入真实 AI 服务。
- PDF 导出目前还未接入真实服务端生成逻辑。
- 评论、通知、分享、会员、搜索等功能仍需后续实现。

### 4.3 设计资产未完成

- 目前已有整块效果图和 SVG 设计稿，但真实页面插画资产仍需要拆分、生成、压缩和接入。
- `FairyImage` 当前可作为图片统一入口，但真实 PNG/WebP 资产仍需要补齐。
- 首页、情侣空间、童话工坊等核心插画需要逐步替换 fallback 绘制效果。

---

## 5. 后续开发总路线

建议按 8 个阶段推进。

---

## Phase 1：项目稳定化与运行检查

目标：确保当前代码可以稳定运行，并补齐基础工程规范。

任务：

1. 本地运行项目：
   - `npm install`
   - `npm run start`
   - 测试 iOS / Android / Web 至少一个端。
2. 检查 Expo Router 路由是否全部可访问。
3. 修复明显报错、依赖缺失和页面跳转问题。
4. 增加基础脚本：
   - lint
   - format
   - test，后续可选
5. 建立 `.env.example`。
6. 建立 `docs/dev-runbook.md`，记录启动、调试、常见问题。

完成标准：

- 首页能进入。
- 四个 Tab 能切换。
- 日记、照片、纪念日、AI 创建的 mock 闭环能跑通。
- 新人可以只看文档就启动项目。

---

## Phase 2：前端 MVP 页面补齐

目标：让 APP 在 mock 数据下形成可演示的完整产品。

优先级 P0：

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

优先级 P1：

1. 文本转漫画
2. AI 视频配置
3. 视频预览编辑
4. 草稿箱
5. 设置页
6. 帮助反馈
7. 数据备份
8. PDF 导出配置

优先级 P2：

1. 搜索页
2. 评论列表
3. 互动通知
4. 会员权益
5. 分享预览
6. 存储空间管理

完成标准：

- 所有 P0 页面视觉一致。
- 所有 P0 页面能走通基本交互。
- 页面内不再大量散落重复样式。
- 主要输入框、按钮、卡片、标签、空状态使用统一组件。

---

## Phase 3：组件系统完善

目标：把当前童话绘本风格沉淀成稳定组件库。

需要继续完善的组件：

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

新增建议组件：

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

完成标准：

- 页面内硬编码视觉样式明显减少。
- 新页面可以通过组件快速搭建。
- 每个组件都有明确 props 和使用场景。

---

## Phase 4：真实后端接入

目标：从 mock 模式切换到真实数据服务。

建议使用 Supabase。

任务：

1. 创建 Supabase 项目。
2. 建立数据库表：
   - profiles
   - couples
   - diaries
   - photos
   - anniversaries
   - ai_jobs
   - comments
   - notifications
3. 开启 Row Level Security。
4. 创建 Storage buckets：
   - avatars
   - photos
   - ai-comics
   - ai-videos
   - exports
5. 接入 Auth：
   - 手机号 / 邮箱 / 第三方登录，按产品需求选择。
6. 改造 `src/api/client.js`。
7. 保持页面只调用 `src/api/*`，不要在页面里直接写 Supabase 查询。

完成标准：

- 登录后能拿到用户 session。
- 用户只能访问自己和情侣关系内的数据。
- mock 数据可以通过 API 层平滑替换。

---

## Phase 5：核心业务真实化

目标：让日记、照片、纪念日、情侣空间真正可用。

任务：

1. 日记真实 CRUD：
   - 新增
   - 列表
   - 详情
   - 编辑
   - 删除
2. 照片真实上传：
   - 选择图片
   - 权限处理
   - 压缩
   - 上传 Storage
   - 写入 photos 表
3. 情侣绑定：
   - 创建邀请码
   - 输入邀请码绑定
   - 绑定确认
   - 解除关系或异常状态处理
4. 纪念日真实 CRUD。
5. 情侣时间线聚合：
   - 日记
   - 照片
   - 纪念日
   - AI 作品
6. 我的页面统计改为真实数据。

完成标准：

- 两个账号可以绑定为情侣。
- 一方新增日记/照片后，另一方能看到。
- 数据刷新后不丢失。

---

## Phase 6：AI 创作系统

目标：把童话工坊从模拟入口变成真实生成能力。

任务：

1. 建立 `ai_jobs` 表。
2. 建立 Edge Function：
   - `create-ai-comic-job`
   - `create-ai-video-job`
3. AI Key 只放服务端，不能放 APP。
4. 前端创建任务后进入进度页。
5. 支持任务状态：
   - pending
   - processing
   - done
   - failed
6. 支持轮询或 Supabase Realtime 更新进度。
7. 结果写入 Storage：
   - 漫画图片
   - 视频文件
   - 封面图
8. 支持生成历史。
9. 支持失败重试。

完成标准：

- 用户能从日记或照片发起漫画生成。
- 进度页能显示真实进度。
- 完成后能查看结果并保存到创作历史。

---

## Phase 7：导出、备份与分享

目标：让回忆内容可以被保存、导出、分享。

任务：

1. PDF 纪念册导出：
   - 选择时间范围
   - 选择内容类型
   - 选择绘本模板
   - 服务端生成 PDF
   - 上传 exports bucket
   - 返回下载链接
2. 数据备份：
   - 用户数据统计
   - 导出 JSON 或服务端备份
3. 分享预览：
   - 单条日记分享卡片
   - AI 作品分享卡片
   - 纪念日分享卡片
4. 存储空间管理：
   - 图片占用
   - 视频占用
   - 导出文件占用

完成标准：

- 用户能导出一本基础 PDF 绘本。
- 用户能分享单条内容。
- 用户能查看自己存储使用情况。

---

## Phase 8：产品完善与上线准备

目标：达到可内测或上架准备状态。

任务：

1. 账号安全和隐私说明。
2. 用户协议和隐私政策。
3. 推送通知。
4. Crash 日志和错误监控。
5. 埋点分析。
6. 性能优化：
   - 图片懒加载
   - 列表性能
   - 动画性能
   - 启动速度
7. 适配：
   - 小屏手机
   - iPhone 刘海屏
   - Android 安全区
8. App 图标、启动页、应用名。
9. 内测分发。
10. 上架素材准备。

完成标准：

- 可交给真实用户测试。
- 核心流程无明显崩溃。
- 数据权限和隐私边界清晰。

---

## 6. 下一步最建议处理的任务

当前最应该继续做的是：

```text
先保证前端 MVP 在 mock 数据下完整可演示，再接后端。
```

建议下一批任务按这个顺序做：

1. 本地运行检查，修复所有启动和路由错误。
2. 完善 `FairyImage`，接入真实插画目录结构。
3. 完善首页、情侣空间、童话工坊三大主页面视觉。
4. 补齐日记详情、相册、AI 进度页的真实 mock 交互。
5. 建立 `.env.example` 和 API mock/real 切换开关。
6. 新建 Supabase 项目并先接登录。
7. 再逐步接日记、照片、情侣绑定、纪念日。

---

## 7. 开发时必须遵守的规则

1. 页面层不要直接请求后端，统一通过 `src/api/`。
2. 页面层不要直接写大量重复样式，优先沉淀组件。
3. 新增页面必须更新 `docs/project-file-structure.md`。
4. 新增图片必须更新 `docs/image-assets-guideline.md`。
5. 新增后端表或接口必须更新 `docs/backend-and-api-plan.md`。
6. 新增重要阶段成果必须更新本文档。
7. AI Key、服务端密钥、Supabase service role key 不能出现在前端代码里。
8. 情侣数据必须带 `couple_id`，并通过 RLS 限制访问。
9. 视觉必须保持童话绘本、奶油纸感、桃粉/干玫瑰/可可棕体系。
10. 先做可运行闭环，再做复杂效果。

---

## 8. 任务看板建议

### Now：当前立即处理

- [ ] 运行项目并记录启动结果
- [ ] 检查所有 Tab 页面
- [ ] 检查日记、照片、纪念日、AI 创建流程
- [ ] 修复当前报错
- [ ] 补充 `.env.example`
- [ ] 补充 `docs/dev-runbook.md`

### Next：下一阶段处理

- [ ] 完善 P0 页面视觉
- [ ] 替换真实插画资产
- [ ] 统一加载态、空状态、弹窗
- [ ] 接入 Supabase Auth
- [ ] 接入日记真实 CRUD
- [ ] 接入照片上传

### Later：后续处理

- [ ] AI 漫画真实生成
- [ ] AI 视频真实生成
- [ ] PDF 导出
- [ ] 评论和通知
- [ ] 会员权益
- [ ] 分享卡片
- [ ] 上线准备

---

## 9. 当前项目交接摘要

后续开发者接手时，优先阅读以下文档：

1. `docs/project-development-master-plan.md`：项目总计划与当前进度。
2. `docs/project-file-structure.md`：当前文件结构和页面说明。
3. `docs/design-system-v1.md`：视觉系统。
4. `docs/image-assets-guideline.md`：图片资产规范。
5. `docs/backend-and-api-plan.md`：后端和 API 规划。
6. `docs/app-development-guide.md`：开发规则。

接手后的第一件事：

```text
先跑项目，再看首页 / 情侣空间 / 童话工坊 / 我的页面，再检查 useFairyStore 的 mock 闭环。
```

如果项目能正常运行，下一步不要急着改后端，应该先把前端 MVP 体验做完整；如果项目不能运行，优先修复依赖、路由和组件引用问题。

---

## 10. 当前版本状态一句话

《独家童话》APP 当前已经完成了产品方向、设计系统、核心页面结构、mock 数据闭环和后端规划，下一阶段应进入“前端 MVP 稳定化 + 真实后端逐步接入”的开发阶段。