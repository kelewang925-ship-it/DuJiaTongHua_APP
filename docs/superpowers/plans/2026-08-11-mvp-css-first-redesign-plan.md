# MVP CSS-First Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将《独家童话》第一阶段 7 个 MVP 页面改造成 CSS/RN 原生布局主导、图片仅作内容与轻量装饰的跨设备界面。

**Architecture:** 先收敛 Fairy 主题 token、响应式容器和页面背景策略，再复用现有 Fairy 组件完成首页与童话工坊两个视觉验证样板，随后按情侣空间、我的、纪念日、写日记、登录的顺序迁移页面。媒体内容通过独立比例容器展示，页面结构不依赖图片；Figma 不在本计划内修改。

**Tech Stack:** Expo SDK 56, React Native 0.85, Expo Router, JavaScript/JSX, StyleSheet, Zustand, React Native Web, existing Fairy components, Ionicons/FairySvgIcon.

## Global Constraints

- 第一阶段只处理登录、首页、写日记、情侣空间、童话工坊、我的、纪念日 7 个 MVP 页面。
- 采用“CSS/RN 主体 + 轻量插画点缀”，页面背景、卡片、按钮、输入框、标签、时间线和导航不得依赖大图。
- 未经用户单独授权，不修改 Figma 文件。
- 不批量处理、抠图、透明化、裁切或压缩现有图片；图片资产只做引用边界和降级策略。
- 优先复用 `src/components/`、`src/theme/`、`src/store/`、`src/utils/` 与现有资产映射。
- 不覆盖工作区既有用户修改；每个任务开始前检查 `git status --short`，只编辑任务列出的文件。
- 任何页面都必须在移除非必要图片后仍能完整呈现。
- 任何固定高度媒体区域都必须使用明确比例或 `minHeight`/`maxHeight` 约束，禁止通过拉伸图片撑起页面。
- 使用 `npm run check:web` 作为 Web 构建/打包检查；没有引入新的测试框架。

---

## Task 1: 建立 CSS-first 主题与响应式基础

**Files:**
- Modify: `src/theme/colors.js`
- Modify: `src/theme/layout.js`
- Modify: `src/theme/typography.js`
- Create: `src/theme/responsive.js`
- Modify: `src/theme/index.js`
- Test/verify: `npm run check:web`

**Interfaces:**
- Consumes: 现有 Fairy color、layout、typography token，以及当前页面使用的 `compact`/`wide` 判定逻辑。
- Produces: `theme.colors`、`theme.layout`、`theme.typography` 和 `theme.responsive` 可供页面与公共组件使用。

- [ ] **Step 1: 检查现有 token 的调用点**

运行：

```powershell
rg "colors\.|spacing\.|radius\.|fontSize|compact|wide" app src
```

记录需要保持兼容的旧导出名，避免主题文件改名导致页面批量断裂。

- [ ] **Step 2: 定义 CSS-first 语义 token**

保留现有颜色导出，同时补齐或统一以下语义：主背景、次背景、分区背景、AI 背景、卡片表面、边框、主文字、辅助文字、强调文字和低透明度阴影色。布局 token 固定 4px 间距基准、16/24/32 圆角、16/20/24 页面内边距档位。

- [ ] **Step 3: 创建响应式 token**

在 `src/theme/responsive.js` 中提供稳定的尺寸分类和纯函数接口：

```js
export const BREAKPOINTS = {
  compact: 390,
  standard: 768,
};

export function getResponsiveMode(width) {
  if (width <= BREAKPOINTS.compact) return 'compact';
  if (width <= BREAKPOINTS.standard) return 'standard';
  return 'wide';
}
```

同时提供页面最大宽度、页面水平边距和双栏阈值 token，不在页面文件中重复写数字。

- [ ] **Step 4: 导出并验证 token**

从 `src/theme/index.js` 导出 `responsive`，运行 `npm run check:web`，确认现有页面仍可解析主题模块。

## Task 2: 收敛页面容器与媒体容器策略

**Files:**
- Modify: `src/components/FairyPage.js`
- Modify: `src/components/FairyCard.js`
- Modify: `src/components/FairyImage.js`
- Create: `src/components/FairyMediaFrame.js`
- Create: `src/components/FairySection.js`
- Test/verify: `npm run check:web`

**Interfaces:**
- Consumes: Task 1 的主题与响应式 token；现有 `FairyPage`、`FairyCard`、`FairyImage` 调用方式。
- Produces: CSS 背景默认模式、内容最大宽度、可选媒体比例容器，以及统一的页面分区组件。

- [ ] **Step 1: 为 `FairyPage` 增加 CSS 背景优先模式**

保留 `backgroundName` 的兼容行为，但让页面在未传入 `backgroundName` 时使用主题背景色；新增明确的背景色/表面色入口，不让普通页面隐式加载 `ImageBackground`。保留安全区、Tab 底部留白和滚动行为。

- [ ] **Step 2: 为页面内容增加最大宽度约束**

在 `FairyPage` 的内容层加入响应式最大宽度与居中逻辑。移动端保持全宽，宽屏避免内容无限拉伸。确认顶部 Header、ScrollView、Tab Safe 区域的 padding 不重复计算。

- [ ] **Step 3: 新增 `FairyMediaFrame`**

组件接口固定为：

```js
<FairyMediaFrame
  source={source}
  aspectRatio={1.5}
  radius={24}
  resizeMode="contain"
  fallback={<FairyIllustration scene="cover" />}
/>
```

组件负责比例、圆角、裁剪和 fallback，不负责决定页面布局；图片加载失败或 source 缺失时仍输出可用的原生占位内容。

- [ ] **Step 4: 新增 `FairySection` 并减少页面重复样式**

组件提供标题、辅助文案、右侧操作和 children 插槽；不内置具体页面业务。只在至少两个 MVP 页面复用时保留该组件。

- [ ] **Step 5: 验证媒体降级**

在开发环境临时传入空 source，确认媒体区域仍有稳定尺寸、可读占位和不溢出布局；运行 `npm run check:web`。

## Task 3: 重做首页与童话工坊验证样板

**Files:**
- Modify: `app/(tabs)/index.js`
- Modify: `app/(tabs)/workshop.js`
- Modify: `src/components/MemoryCard.js`
- Modify: `src/components/WorkshopCard.js`
- Modify: `src/components/MemoryWall.js`
- Test/verify: `npm run check:web`

**Interfaces:**
- Consumes: Task 1 的 token、Task 2 的页面容器和媒体容器；现有 `useFairyStore` 的 `couple`、`records`、`creations`、`anniversaries` 数据。
- Produces: 无大 Hero 图片依赖的首页，以及 CSS 卡片主导的童话工坊入口和历史区域。

- [ ] **Step 1: 绘制现有页面的数据与路由依赖**

运行：

```powershell
rg "useFairyStore|router\.|FairyImage|FairySticker|FairyCard" "app/(tabs)/index.js" "app/(tabs)/workshop.js" src/components/MemoryCard.js src/components/WorkshopCard.js src/components/MemoryWall.js
```

保留现有跳转、状态读取和交互回调，只替换布局与视觉层。

- [ ] **Step 2: 将首页主视觉改为今日状态卡**

保留日期、情侣空间名、记录数量和主要 CTA；将大 Hero 图替换为 CSS 情绪/恋爱天数卡，图片仅作为可选小型内容缩略图或贴纸。首页在 `records` 为空时仍展示完整的今日入口和空状态。

- [ ] **Step 3: 将首页快捷入口改为 CSS action grid**

日记、照片、AI 作品入口使用原生卡片、Ionicons/FairySvgIcon 和文案组成。点击目标与现有路由保持一致。

- [ ] **Step 4: 将回忆区改为内容驱动卡片流**

`MemoryCard` 和 `MemoryWall` 中的图片使用 `FairyMediaFrame` 或独立缩略图，不再让图片决定卡片整体高度；文本、标签和操作区域必须可独立布局。

- [ ] **Step 5: 将童话工坊入口改为创作卡片**

保留漫画、视频/回忆放映和历史入口；用浅金/奶油表面、魔法状态文字和小装饰表达 AI，不使用科技面板或大幅背景图。

- [ ] **Step 6: 验证两页交互与降级**

分别验证有数据、无数据、创建历史存在和历史为空四种状态；运行 `npm run check:web`，并在窄屏与宽屏检查没有水平溢出。

## Task 4: 重做情侣空间与“我的”页面

**Files:**
- Modify: `app/(tabs)/couple.js`
- Modify: `app/(tabs)/mine.js`
- Modify: `src/components/CoupleTimeline.js`
- Modify: `src/components/FairyIllustration.js` only if fallback sizing is required
- Test/verify: `npm run check:web`

**Interfaces:**
- Consumes: Task 1/2 的公共系统；现有 `couple`、`timeline`、`records`、`creations`、`anniversaries` 和统计方法。
- Produces: CSS 时间线主导的情侣空间与结构化私人收藏页。

- [ ] **Step 1: 迁移情侣空间头部和统计卡**

使用 CSS profile/summary card 表达情侣信息、关系状态和恋爱天数；保留现有纪念日、记录和详情路由，不将封面图作为头部高度来源。

- [ ] **Step 2: 重构 `CoupleTimeline` 的连接线和节点**

连接线、节点、标签和内容摘要使用 View/Text/Pressable 完成；节点可以使用小贴纸，但贴纸不得影响时间线主结构或点击区域。

- [ ] **Step 3: 迁移“我的”页面资料与统计模块**

将个人资料、会员状态、四类统计和功能菜单改成稳定的 CSS 卡片/列表；保留会员、设置、备份、草稿和退出登录路由与对话框行为。

- [ ] **Step 4: 验证数据空值和长文本**

使用 mock 数据验证空 timeline、0 条记录、长昵称和多行菜单标题不会撑破布局；运行 `npm run check:web`。

## Task 5: 重做纪念日、写日记与登录页

**Files:**
- Modify: `app/anniversary/index.js`
- Modify: `app/diary/editor.js`
- Modify: `app/login.js`
- Test/verify: `npm run check:web`

**Interfaces:**
- Consumes: Task 1/2 的公共容器、卡片、媒体和表单能力；现有周年纪念日 store 操作、日记编辑回调和认证流程。
- Produces: CSS 倒计时章节卡、低压力日记编辑页和轻量插画登录入口。

- [ ] **Step 1: 重构纪念日首页**

将最近纪念日倒计时设计为 CSS 数字与日期卡；纪念日列表使用章节卡片。封面图仅通过 `FairyMediaFrame` 作为可选内容，缺失时显示 CSS/文本占位。

- [ ] **Step 2: 重构写日记编辑器外壳**

保留当前富文本编辑器与保存逻辑，只替换页面外壳、日期/情绪/标签布局、照片缩略图区域和 AI 入口。编辑区使用 CSS 纸张表面，不把背景图作为编辑器依赖。

- [ ] **Step 3: 重构登录页**

使用暖米白背景、品牌标题、欢迎文案、表单卡片、主按钮和可选小型透明插画；保留认证校验、登录提交和导航行为。表单必须在没有插画时保持完整。

- [ ] **Step 4: 验证表单状态**

分别验证默认、输入中、校验错误、提交中和提交失败状态；运行 `npm run check:web`。

如果验证发现登录页和日记页无法通过现有 `FairyInput` 或 `FairyHeader` 表达已批准的状态，才允许分别修改 `src/components/FairyInput.js` 或 `src/components/FairyHeader.js`；没有失败证据时不修改这两个公共组件。

## Task 6: 统一底部导航、空状态和状态反馈

**Files:**
- Modify: `src/components/FairyTabBar.js`
- Modify: `src/components/FairyEmptyState.js`
- Modify: `src/components/FairyToast.js`
- Modify: `src/components/FairyDialog.js`
- Test/verify: `npm run check:web`

**Interfaces:**
- Consumes: Task 1 的颜色、圆角、阴影和文字 token；所有 7 个 MVP 页面现有状态调用。
- Produces: 跨页面一致的导航、空状态、Toast 和 Dialog 视觉反馈。

- [ ] **Step 1: 调整 Tab Bar 的尺寸和响应式行为**

保留四个路由和导航事件，统一安全区、内容最大宽度、激活态颜色、图标尺寸和文字层级；确认窄屏不因标签宽度产生截断，宽屏不无限拉伸。

- [ ] **Step 2: 统一空状态降级**

空状态优先使用 CSS 结构和可选小插画；`imageName` 缺失时不能出现空白高度或异常 import。保留 action callback。

- [ ] **Step 3: 统一状态反馈**

Toast 和 Dialog 使用同一表面、边框、阴影和文案层级；不引入新的业务文案或改变已有确认/取消行为。

- [ ] **Step 4: 运行跨页面 smoke check**

启动 Web 开发检查并依次访问 7 个页面及主要跳转；记录控制台错误、红屏、布局溢出和缺失资源。

## Task 7: 跨设备验收与设计资产边界收口

**Files:**
- Modify: none by default; if a verification failure is found, modify only the exact file from Tasks 1–6 responsible for that failure
- Do not modify: Figma files and raw image files under `assets/linshi`, `assets/design`, `assets/generated`
- Verify: `npm run check:web`

**Interfaces:**
- Consumes: Tasks 1–6 的完整页面实现、当前 mock 数据和现有资源映射。
- Produces: 可复现的跨设备验证记录和已知资产待处理清单，不改变用户图片内容。

- [ ] **Step 1: 验证三类尺寸**

在 Web 开发环境验证：窄屏手机约 360–390px、普通手机约 390–430px、平板/Web 宽屏至少 768px。重点检查横向溢出、标题换行、卡片高度、媒体比例、底部 Tab 和安全区。

- [ ] **Step 2: 验证图片可移除**

临时屏蔽非必要图片引用，确认每个页面仍具备完整结构；恢复引用后确认图片没有成为布局尺寸来源。

- [ ] **Step 3: 验证状态矩阵**

至少检查：有内容/无内容、长文案、空图片、加载中、错误、提交中和提交失败。每个状态都必须使用已有组件和同一 token 系统。

- [ ] **Step 4: 整理待处理图片清单**

只记录需要用户后续处理的透明背景、裁切、压缩和命名问题，不编辑原图、不移动文件、不生成 Figma 资产。

- [ ] **Step 5: 运行最终 Web 检查**

运行：

```powershell
npm run check:web
```

Expected: 命令完成且无构建错误；若存在既有环境问题，记录完整错误与受影响页面，不将未验证内容标记为完成。

## Execution Handoff

实现时严格按 Task 1 → Task 2 → Task 3 → Task 4 → Task 5 → Task 6 → Task 7 顺序执行。每个任务完成后单独运行该任务的验证命令，再进入下一任务。Figma 设计、图片透明化和批量资产处理属于后续独立工作流，必须取得单独授权后再规划。
