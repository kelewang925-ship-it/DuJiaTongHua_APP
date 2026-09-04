# 《独家童话》项目展示 HTML Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `项目资料/` 中交付一个可离线打开、可响应式浏览的单文件项目展示页，完整呈现品牌、产品结构、八个模块、代表设计稿、页面功能、设计体系与当前状态。

**Architecture:** 页面采用单个 HTML 文件，内嵌 CSS、JavaScript 和项目展示数据，所有图片与资料链接使用相对于 `项目资料/` 的路径。正文在 JavaScript 失效时仍可阅读，JavaScript 只增强模块筛选、功能展开、灯箱和导航状态。

**Tech Stack:** HTML5、原生 CSS、原生 JavaScript、项目内 PNG/Markdown 资料、PowerShell 静态核验、Chromium 浏览器人工与自动化检查。

**Spec:** `docs/superpowers/specs/2026-09-04-project-showcase-html-design.md`

## Global Constraints

- 最终展示文件必须是 `项目资料/独家童话-项目展示.html`。
- 不引入 npm 包、框架、CDN、在线字体或远程图片。
- 当前设计数据以 `项目资料/新模块分布/` 的八个模块为唯一基准。
- 正式数据为 114 张页面与状态稿、约 89 个逻辑页面。
- `历史未通过/`、旧 67/69 页设计稿、旧九模块资料和模块 03 的三张探索提案不得进入正式画廊。
- 第一版只展示约 20 张代表稿，不内嵌全部 114 张图片。
- 页面固定浅色主题，并使用月白、桃夭、枯玫瑰、可可棕和琥珀金品牌色。
- 页面内不得使用 em dash 字符 `—`。
- 所有图片使用相对路径并启用懒加载。
- 设计状态与代码实现状态必须分开表达。

---

### Task 1: 建立语义骨架与可信内容

**Files:**
- Create: `项目资料/独家童话-项目展示.html`

**Interfaces:**
- Consumes: 设计说明中的信息架构、当前八模块数据、当前选定 Logo 和用户流程图。
- Produces: 具备完整语义章节、锚点、基础正文和约 20 张代表稿路径的静态 HTML 文档。

- [ ] **Step 1: 写入失败的结构检查命令**

Run:

```powershell
$page = '项目资料/独家童话-项目展示.html'
if (-not (Test-Path -LiteralPath $page)) { throw 'showcase html missing' }
```

Expected: FAIL with `showcase html missing`。

- [ ] **Step 2: 创建 HTML 文档骨架**

创建标准 HTML5 文档，设置：

```html
<html lang="zh-CN">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>独家童话 | 项目全景</title>
```

建立以下稳定锚点：

```html
<section id="project"></section>
<section id="product"></section>
<section id="modules"></section>
<section id="journey"></section>
<section id="gallery"></section>
<section id="design-system"></section>
<section id="status"></section>
```

- [ ] **Step 3: 写入品牌封面与产品叙事**

封面使用：

```html
<img src="05-图片资产与生成/独家童话-App图标-当前选定版.png"
     alt="独家童话 App 图标" width="1254" height="1254">
```

正文必须包含核心表达、四个数据和四个核心价值：记录日常、共同创造、重新发现、长久收藏。

- [ ] **Step 4: 写入四个主 Tab 与八模块结构**

八模块数据必须使用：

```js
const modules = [
  { id: '01', name: '账号登录', screens: 8, logicalPages: 8 },
  { id: '02', name: '账号关联', screens: 9, logicalPages: 9 },
  { id: '03', name: '童话首页', screens: 12, logicalPages: 8 },
  { id: '04', name: '重要时刻', screens: 17, logicalPages: 11 },
  { id: '05', name: '童话工坊', screens: 10, logicalPages: 10 },
  { id: '06', name: '我的与设置', screens: 12, logicalPages: 12 },
  { id: '07', name: '情侣宠物', screens: 25, logicalPages: 10 },
  { id: '08', name: '共同回忆册', screens: 21, logicalPages: 21 }
];
```

四个主 Tab 与八模块不得放成同级导航。

- [ ] **Step 5: 写入代表设计稿清单**

每个模块选择以下代表稿：

```text
01: 01-引导页.png, 02-登录页.png
02: 01-建立情侣关系页.png, 04-情侣关系确认页.png, 05-情侣绑定成功页.png
03: 01-首页与共同记录-正常态.png, 03-日记编辑页.png, 06-照片相册页-网格状态.png
04: 01-重要时刻首页-正常态.png, 07-纪念日倒计时页-纪念日当天.png, 10-时光胶囊详情页-已开启.png
05: 01-童话工坊首页.png, 03-回忆转漫画编辑页.png, 08-作品详情页.png
06: 01-我的与设置首页.png, 03-我们的小世界页.png, 06-童话会员页.png
07: 60-宠物空间首页-正常态.png, 61-宠物互动页-互动成功.png, 66-成长故事页-章节详情.png
08: 01-书架.png, 16-沉浸翻阅页.png, 19-双人补页编辑.png
```

共 23 张代表稿。模块 03 的三张提案不得进入清单。

- [ ] **Step 6: 写入流程、设计体系、状态和资料入口**

流程图使用：

```html
<img src="09-流程图/用户使用流程.png" alt="独家童话用户使用流程" loading="lazy">
```

状态区域必须明确“待视觉审批”和“是否已开发”是独立维度。

- [ ] **Step 7: 运行静态结构检查**

Run:

```powershell
$html = Get-Content -Raw -LiteralPath '项目资料/独家童话-项目展示.html'
$required = 'id="project"','id="product"','id="modules"','id="journey"','id="gallery"','id="design-system"','id="status"','114','89'
foreach ($token in $required) { if (-not $html.Contains($token)) { throw "missing token: $token" } }
if ($html.Contains('历史未通过/')) { throw 'historical path leaked into gallery' }
if ($html.Contains('共读故事书V2提案.png') -or $html.Contains('可开发视觉基线提案.png') -or $html.Contains('轻绘本V1.1提案.png')) { throw 'module 03 proposal leaked into gallery' }
```

Expected: exit 0。

- [ ] **Step 8: Commit**

```powershell
git add -- '项目资料/独家童话-项目展示.html'
git commit -m 'feat: add project showcase content'
```

---

### Task 2: 建立品牌化响应式视觉系统

**Files:**
- Modify: `项目资料/独家童话-项目展示.html`

**Interfaces:**
- Consumes: Task 1 的稳定章节 ID 和语义内容。
- Produces: 统一浅色主题、编辑型版式、桌面与移动端响应式布局。

- [ ] **Step 1: 写入失败的 CSS 令牌检查**

Run:

```powershell
$html = Get-Content -Raw -LiteralPath '项目资料/独家童话-项目展示.html'
$required = '--paper:','--peach:','--rose:','--cocoa:','--gold:','@media (max-width: 760px)','prefers-reduced-motion'
foreach ($token in $required) { if (-not $html.Contains($token)) { throw "missing style token: $token" } }
```

Expected: FAIL，至少缺少一个样式令牌。

- [ ] **Step 2: 增加全局设计令牌**

在页面内嵌 CSS 中定义：

```css
:root {
  --paper: #f8f6f2;
  --paper-warm: #f2e8dc;
  --peach: #f6bec8;
  --rose: #b08a8f;
  --cocoa: #6b4f4f;
  --gold: #d8b384;
  --ink-soft: #8c7472;
  --radius-sm: 14px;
  --radius-md: 24px;
  --radius-lg: 36px;
}
```

- [ ] **Step 3: 完成封面、章节和模块版式**

要求：

- 封面一屏内出现 Logo、标题、核心表达和关键数据。
- 四个主 Tab 使用关系布局，不使用四张等宽功能卡。
- 八个模块使用交替排版，不连续复用同一图片方向。
- 画廊采用 `grid-template-columns: repeat(auto-fit, minmax(...))`。
- 状态信息使用文本加颜色，不能只靠颜色。

- [ ] **Step 4: 完成响应式与降级样式**

至少实现：

```css
@media (max-width: 760px) { /* 单列、缩小标题、导航横向滚动 */ }
@media (prefers-reduced-motion: reduce) { /* 关闭平滑滚动和过渡 */ }
```

所有页面不得使用固定 `height: 100vh`，封面使用 `min-height: 100dvh` 或内容驱动高度。

- [ ] **Step 5: 运行 CSS 和禁用模式检查**

Run:

```powershell
$html = Get-Content -Raw -LiteralPath '项目资料/独家童话-项目展示.html'
$required = '--paper:','--peach:','--rose:','--cocoa:','--gold:','@media (max-width: 760px)','prefers-reduced-motion','loading="lazy"'
foreach ($token in $required) { if (-not $html.Contains($token)) { throw "missing token: $token" } }
if ($html.Contains('https://') -or $html.Contains('http://')) { throw 'remote dependency found' }
if ($html.Contains('—')) { throw 'em dash found' }
```

Expected: exit 0。

- [ ] **Step 6: Commit**

```powershell
git add -- '项目资料/独家童话-项目展示.html'
git commit -m 'style: add editorial showcase design'
```

---

### Task 3: 增加筛选、功能展开和无障碍灯箱

**Files:**
- Modify: `项目资料/独家童话-项目展示.html`

**Interfaces:**
- Consumes: Task 1 的画廊数据、模块 ID 和图片按钮。
- Produces: `setGalleryFilter(moduleId)`、`openLightbox(index)`、`closeLightbox()`、`moveLightbox(delta)` 四个稳定函数。

- [ ] **Step 1: 写入失败的交互接口检查**

Run:

```powershell
$html = Get-Content -Raw -LiteralPath '项目资料/独家童话-项目展示.html'
$required = 'function setGalleryFilter','function openLightbox','function closeLightbox','function moveLightbox','aria-modal="true"','aria-expanded'
foreach ($token in $required) { if (-not $html.Contains($token)) { throw "missing interaction: $token" } }
```

Expected: FAIL。

- [ ] **Step 2: 实现模块筛选**

`setGalleryFilter(moduleId)` 必须：

- `all` 显示全部代表稿。
- 模块 ID 只显示对应代表稿。
- 更新筛选按钮的 `aria-pressed`。
- 不删除 DOM 节点，只切换 `hidden`。

- [ ] **Step 3: 实现功能明细展开**

展开按钮必须同步更新：

```js
button.setAttribute('aria-expanded', String(expanded));
panel.hidden = !expanded;
```

- [ ] **Step 4: 实现灯箱与键盘操作**

灯箱必须具备：

- `role="dialog"`
- `aria-modal="true"`
- 图片、标题、路径
- 上一张、下一张和关闭按钮
- `Escape` 关闭
- `ArrowLeft` 与 `ArrowRight` 切换
- 关闭后焦点回到原图片按钮

- [ ] **Step 5: 实现图片错误降级**

每张图片的 `error` 事件将对应容器标记为失败，并显示原文件名与相对路径；不得让脚本抛出未捕获异常。

- [ ] **Step 6: 运行交互静态检查**

Run:

```powershell
$html = Get-Content -Raw -LiteralPath '项目资料/独家童话-项目展示.html'
$required = 'function setGalleryFilter','function openLightbox','function closeLightbox','function moveLightbox','aria-modal="true"','aria-expanded','ArrowLeft','ArrowRight','Escape','aria-pressed'
foreach ($token in $required) { if (-not $html.Contains($token)) { throw "missing interaction token: $token" } }
```

Expected: exit 0。

- [ ] **Step 7: Commit**

```powershell
git add -- '项目资料/独家童话-项目展示.html'
git commit -m 'feat: add showcase browsing interactions'
```

---

### Task 4: 完整验证与交付

**Files:**
- Verify: `项目资料/独家童话-项目展示.html`

**Interfaces:**
- Consumes: Tasks 1–3 的最终页面。
- Produces: 可离线打开、无缺图、无远程依赖、响应式可浏览的交付文件。

- [ ] **Step 1: 检查所有本地图片路径**

使用 PowerShell 从 `src` 属性中提取 PNG 相对路径，并以 `项目资料/` 为基准验证：

```powershell
$root = (Resolve-Path '项目资料').Path
$html = Get-Content -Raw -LiteralPath '项目资料/独家童话-项目展示.html'
$matches = [regex]::Matches($html, 'src="([^"]+\.png)"')
foreach ($match in $matches) {
  $relative = [System.Net.WebUtility]::HtmlDecode($match.Groups[1].Value)
  $path = Join-Path $root ($relative -replace '/', '\')
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "missing asset: $relative" }
}
"Verified $($matches.Count) local PNG references"
```

Expected: 所有 PNG 均存在。

- [ ] **Step 2: 检查 HTML 基本完整性**

Run:

```powershell
$html = Get-Content -Raw -LiteralPath '项目资料/独家童话-项目展示.html'
if (($html | Select-String '<html' -AllMatches).Matches.Count -ne 1) { throw 'invalid html root count' }
if (-not $html.Contains('</html>')) { throw 'missing closing html tag' }
if ($html.Contains('http://') -or $html.Contains('https://')) { throw 'remote dependency found' }
if ($html.Contains('历史未通过/')) { throw 'historical asset path found' }
if ($html.Contains('—')) { throw 'em dash found' }
```

Expected: exit 0。

- [ ] **Step 3: 在浏览器中检查桌面版**

打开本地 HTML，确认：

- 首屏 Logo、核心表达和关键数据位于第一屏。
- 吸顶导航可跳转所有章节。
- 八模块数据与设计说明一致。
- 筛选、展开和灯箱可操作。
- 23 张代表稿均可显示。
- 浏览器控制台无未处理异常。

- [ ] **Step 4: 在浏览器中检查移动版**

使用约 390 × 844 视口确认：

- 无横向溢出。
- 导航可水平滚动。
- 标题、正文、按钮和图片可读。
- 灯箱按钮不会超出屏幕。

- [ ] **Step 5: 检查 Git 变更范围**

Run:

```powershell
git status --short -- '项目资料/独家童话-项目展示.html'
git diff --stat -- '项目资料/独家童话-项目展示.html'
```

Expected: 只显示目标 HTML 的任务变更；其他用户已有改动不被纳入提交。

- [ ] **Step 6: 最终提交**

若上一个任务提交后仍有验证修正：

```powershell
git add -- '项目资料/独家童话-项目展示.html'
git commit -m 'fix: polish project showcase verification'
```

若无修正，不创建空提交。

