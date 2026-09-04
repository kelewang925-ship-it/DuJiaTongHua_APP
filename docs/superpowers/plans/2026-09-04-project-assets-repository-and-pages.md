# 独家童话公开项目展示仓库 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在不上传本地完整项目资料的前提下，将《独家童话》项目展示页及其必要资源推送到独立 GitHub 仓库，并发布为公开 GitHub Pages 网站。

**Architecture:** `D:\projectCode\DuJiaTongHua\DuJiaTongHua_Project_Docs` 同时保存本地完整资料和独立 Git 工作区，但 `.gitignore` 默认忽略完整资料。Git 只显式跟踪 `index.html`、站点配置、验证脚本以及 HTML 实际引用的公开文件；GitHub Actions 从干净检出的已跟踪文件构建 Pages 发布物，因此不会读取或上传本地被忽略资料。

**Tech Stack:** 静态 HTML/CSS/JavaScript、PowerShell 7、Node.js、Git、GitHub Actions、GitHub Pages

**Spec:** `docs/superpowers/specs/2026-09-04-project-assets-repository-and-pages-design.md`

## Global Constraints

- 本地资料根目录固定为 `D:\projectCode\DuJiaTongHua\DuJiaTongHua_Project_Docs`。
- 远端仓库固定为 `https://github.com/kelewang925-ship-it/dujia-tonghua-project-assets.git`。
- 公网地址固定为 `https://kelewang925-ship-it.github.io/dujia-tonghua-project-assets/`。
- 本地完整资料保持原位，不删除，不上传。
- 只公开展示页运行所需文件，不上传历史未通过设计稿或无关生成资产。
- 不进行图片格式转换或有损压缩。
- 页面保留 89 个逻辑页面、图片灯箱、模块筛选和流程图 50%–500% 缩放能力。
- 所有文件修改使用 `apply_patch`；复制现有 HTML 为入口文件属于机械复制，可使用 `Copy-Item`。
- 每次提交前检查暂存文件列表，禁止使用未审查的 `git add .`。

---

## File Structure

在 `D:\projectCode\DuJiaTongHua\DuJiaTongHua_Project_Docs` 中创建或跟踪：

- `index.html`：公网唯一入口，由现有 `独家童话-项目展示.html` 复制并调整。
- `README.md`：仓库用途、线上地址、公开边界与本地维护方法。
- `.gitignore`：默认忽略根目录全部本地资料，只放行站点基础文件；资源通过清单显式强制暂存。
- `.nojekyll`：禁止 Jekyll 改写静态目录。
- `.github/workflows/pages.yml`：GitHub Pages 发布流程。
- `scripts/build-public-manifest.ps1`：从 `index.html` 提取并校验本地文件引用，生成 `public-files.txt`。
- `scripts/verify-public-site.ps1`：验证入口、引用、公开清单、Git 跟踪边界和敏感信息。
- `scripts/test-showcase.mjs`：运行展示页内联 JavaScript 的无浏览器行为测试。
- `public-files.txt`：唯一允许公开的文件清单。
- `09-流程图/...` 与 `新模块分布/...`：仅跟踪 `index.html` 实际引用的文件。

原有其他目录继续存在于磁盘，但保持忽略和未跟踪。

---

### Task 1: 建立公网入口并修复模块入口行为

**Files:**
- Create: `D:\projectCode\DuJiaTongHua\DuJiaTongHua_Project_Docs\index.html`
- Create: `D:\projectCode\DuJiaTongHua\DuJiaTongHua_Project_Docs\scripts\test-showcase.mjs`
- Read: `D:\projectCode\DuJiaTongHua\DuJiaTongHua_Project_Docs\独家童话-项目展示.html`

**Interfaces:**
- Consumes: 当前展示页及其现有 `[data-filter]`、`[data-gallery-module]`、`setGalleryFilter(moduleId)` 接口。
- Produces: 8 个 `a[data-gallery-jump]` 入口；点击后跳到 `#gallery` 并调用 `setGalleryFilter()`。

- [ ] **Step 1: 机械复制当前展示页为公网入口**

Run:

```powershell
Copy-Item -LiteralPath '独家童话-项目展示.html' -Destination 'index.html'
```

Expected: `index.html` 与原展示页 SHA-256 相同。

- [ ] **Step 2: 创建会失败的模块入口行为测试**

使用 `apply_patch` 创建 `scripts/test-showcase.mjs`。测试必须读取真实 `index.html`，并验证 8 个模块入口与模块筛选的公开行为：

```javascript
import fs from 'node:fs';

const html = fs.readFileSync(new URL('../index.html', import.meta.url), 'utf8');
const links = [...html.matchAll(/<a(?=[^>]*href="#gallery")(?=[^>]*data-gallery-jump="(\d{2})")[^>]*>/g)]
  .map((match) => match[1]);
const expected = ['01', '02', '03', '04', '05', '06', '07', '08'];

if (JSON.stringify(links) !== JSON.stringify(expected)) {
  throw new Error(`Expected gallery jump links ${expected.join(',')}, got ${links.join(',')}`);
}

if (!/querySelectorAll\('\[data-gallery-jump\]'\)/.test(html)) {
  throw new Error('Gallery jump listener registration is missing');
}

if (!/setGalleryFilter\(link\.dataset\.galleryJump\)/.test(html)) {
  throw new Error('Gallery jump does not apply the requested module filter');
}

if (/href="新模块分布\//.test(html)) {
  throw new Error('A public page still links to an unpublished local directory');
}

console.log('PASS: all 8 module links jump to and filter the gallery');
```

- [ ] **Step 3: 运行测试并确认因新行为尚不存在而失败**

Run:

```powershell
node scripts/test-showcase.mjs
```

Expected: FAIL，错误包含 `Expected gallery jump links`。

- [ ] **Step 4: 修改 8 个模块入口**

使用 `apply_patch` 将每个模块卡片末尾的本地目录链接改为：

```html
<a href="#gallery" data-gallery-jump="01">查看模块设计稿</a>
```

模块编号依次为 `01` 至 `08`。

- [ ] **Step 5: 注册模块入口监听**

在现有筛选按钮监听之后添加：

```javascript
document.querySelectorAll('[data-gallery-jump]').forEach((link) => {
  link.addEventListener('click', () => setGalleryFilter(link.dataset.galleryJump));
});
```

- [ ] **Step 6: 验证测试与内联脚本语法**

Run:

```powershell
node scripts/test-showcase.mjs
$html = Get-Content -LiteralPath 'index.html' -Raw -Encoding UTF8
[regex]::Match($html, '<script>([\s\S]*?)</script>').Groups[1].Value | node --check -
```

Expected: 测试输出 `PASS: all 8 module links jump to and filter the gallery`，Node 语法检查退出码为 0。

---

### Task 2: 创建公开清单和防误传边界

**Files:**
- Create: `D:\projectCode\DuJiaTongHua\DuJiaTongHua_Project_Docs\.gitignore`
- Create: `D:\projectCode\DuJiaTongHua\DuJiaTongHua_Project_Docs\.nojekyll`
- Create: `D:\projectCode\DuJiaTongHua\DuJiaTongHua_Project_Docs\README.md`
- Create: `D:\projectCode\DuJiaTongHua\DuJiaTongHua_Project_Docs\scripts\build-public-manifest.ps1`
- Create: `D:\projectCode\DuJiaTongHua\DuJiaTongHua_Project_Docs\scripts\verify-public-site.ps1`
- Create: `D:\projectCode\DuJiaTongHua\DuJiaTongHua_Project_Docs\public-files.txt`

**Interfaces:**
- Consumes: `index.html` 中所有非外部、非锚点的 `src` 与文件型 `href`。
- Produces: UTF-8 `public-files.txt`；验证脚本退出码 0 表示引用完整且公开范围安全。

- [ ] **Step 1: 创建失败的公开清单验证入口**

使用 `apply_patch` 创建 `scripts/verify-public-site.ps1`：

```powershell
param([string]$Root = (Split-Path $PSScriptRoot -Parent))
$ErrorActionPreference = 'Stop'

$required = @('index.html', 'README.md', '.gitignore', '.nojekyll',
  '.github/workflows/pages.yml', 'scripts/build-public-manifest.ps1',
  'scripts/verify-public-site.ps1', 'scripts/test-showcase.mjs', 'public-files.txt')
$manifestPath = Join-Path $Root 'public-files.txt'
if (-not (Test-Path -LiteralPath $manifestPath)) { throw 'public-files.txt is missing' }
$manifest = @(Get-Content -LiteralPath $manifestPath -Encoding UTF8 | Where-Object { $_.Trim() })
foreach ($path in $required) {
  if ($path -notin $manifest) { throw "Required public file is absent from manifest: $path" }
}
foreach ($path in $manifest) {
  $full = [IO.Path]::GetFullPath((Join-Path $Root $path))
  $rootFull = [IO.Path]::GetFullPath($Root) + [IO.Path]::DirectorySeparatorChar
  if (-not $full.StartsWith($rootFull, [StringComparison]::OrdinalIgnoreCase)) { throw "Path escapes root: $path" }
  if (-not (Test-Path -LiteralPath $full -PathType Leaf)) { throw "Missing public file: $path" }
}

$html = Get-Content -LiteralPath (Join-Path $Root 'index.html') -Raw -Encoding UTF8
$refs = [regex]::Matches($html, '(?:src|href)="([^"]+)"') |
  ForEach-Object { [uri]::UnescapeDataString($_.Groups[1].Value) } |
  Where-Object { $_ -notmatch '^(?:https?:|#|mailto:|javascript:)' } |
  Sort-Object -Unique
foreach ($ref in $refs) {
  if ($ref -notin $manifest) { throw "HTML reference is absent from manifest: $ref" }
}
if (Test-Path -LiteralPath (Join-Path $Root '.git')) {
  $tracked = @(git -C $Root ls-files)
  $unexpected = @($tracked | Where-Object { $_ -notin $manifest })
  if ($unexpected.Count) { throw "Unexpected tracked files: $($unexpected -join ', ')" }
}

$textFiles = $manifest | Where-Object { [IO.Path]::GetExtension($_) -in @('.html', '.md', '.mmd', '.json', '.yml', '.yaml', '.ps1', '.mjs', '') }
$secretPattern = '(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|SUPABASE_(?:ANON_KEY|SERVICE_ROLE_KEY)\s*[:=]\s*[^\s]+)'
foreach ($path in $textFiles) {
  $value = Get-Content -LiteralPath (Join-Path $Root $path) -Raw -Encoding UTF8
  if ($value -match $secretPattern) { throw "Potential secret in public file: $path" }
  if ($value -match '[A-Z]:\\(?:Users|projectCode)\\') { throw "Local absolute path in public file: $path" }
}

"PASS: $($manifest.Count) public files; $($refs.Count) local references; no path escape, unexpected tracked file, or secret pattern."
```

- [ ] **Step 2: 运行验证并确认清单缺失失败**

Run:

```powershell
pwsh -NoProfile -File scripts/verify-public-site.ps1
```

Expected: FAIL，错误为 `public-files.txt is missing`。

- [ ] **Step 3: 创建公开清单生成器**

使用 `apply_patch` 创建 `scripts/build-public-manifest.ps1`：

```powershell
param([string]$Root = (Split-Path $PSScriptRoot -Parent))
$ErrorActionPreference = 'Stop'
$rootFull = [IO.Path]::GetFullPath($Root)
$html = Get-Content -LiteralPath (Join-Path $Root 'index.html') -Raw -Encoding UTF8
$refs = [regex]::Matches($html, '(?:src|href)="([^"]+)"') |
  ForEach-Object { [uri]::UnescapeDataString($_.Groups[1].Value) } |
  Where-Object { $_ -notmatch '^(?:https?:|#|mailto:|javascript:)' } |
  Sort-Object -Unique
foreach ($ref in $refs) {
  $full = [IO.Path]::GetFullPath((Join-Path $rootFull $ref))
  if (-not $full.StartsWith($rootFull + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw "Path escapes root: $ref" }
  if (-not (Test-Path -LiteralPath $full -PathType Leaf)) { throw "Missing referenced file: $ref" }
}
$infrastructure = @('index.html', 'README.md', '.gitignore', '.nojekyll',
  '.github/workflows/pages.yml', 'scripts/build-public-manifest.ps1',
  'scripts/verify-public-site.ps1', 'scripts/test-showcase.mjs', 'public-files.txt')
@($infrastructure + $refs | Sort-Object -Unique) |
  Set-Content -LiteralPath (Join-Path $Root 'public-files.txt') -Encoding utf8NoBOM
"Generated public-files.txt with $((@($infrastructure + $refs | Sort-Object -Unique)).Count) files."
```

- [ ] **Step 4: 创建忽略规则和站点说明**

`.gitignore` 内容：

```gitignore
# This directory also contains private/local project material.
# Public files are force-added from public-files.txt only.
*
```

`.nojekyll` 为空文件。

`README.md` 内容至少包括：

```markdown
# 独家童话 · 项目展示

这是《独家童话》情侣应用的公开项目展示仓库，仅包含展示页运行所需的精选设计资料。

- 在线展示：https://kelewang925-ship-it.github.io/dujia-tonghua-project-assets/
- App 代码仓库：https://github.com/kelewang925-ship-it/DuJiaTongHua_APP

本仓库不包含完整项目资料、历史设计归档、密钥或用户数据。
```

- [ ] **Step 5: 创建 Pages 工作流**

使用 `apply_patch` 创建 `.github/workflows/pages.yml`：

```yaml
name: Deploy GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: .
      - name: Deploy
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 6: 生成清单并验证**

Run:

```powershell
pwsh -NoProfile -File scripts/build-public-manifest.ps1
pwsh -NoProfile -File scripts/verify-public-site.ps1
```

Expected: 两条命令均退出 0；清单包含基础文件和全部本地文件引用，总体积约 195 MB，不包含目录引用。

---

### Task 3: 初始化独立仓库并推送受控公开内容

**Files:**
- Track: `public-files.txt` 中列出的全部文件
- Git metadata: `D:\projectCode\DuJiaTongHua\DuJiaTongHua_Project_Docs\.git`

**Interfaces:**
- Consumes: Task 2 生成且验证通过的 `public-files.txt`。
- Produces: `main` 分支首次提交和远端 `origin/main`。

- [ ] **Step 1: 初始化独立仓库并配置远端**

Run:

```powershell
git init -b main
git remote add origin https://github.com/kelewang925-ship-it/dujia-tonghua-project-assets.git
git remote -v
```

Expected: `origin` 的 fetch/push 地址均为目标仓库。

- [ ] **Step 2: 只强制暂存公开清单文件**

Run:

```powershell
$publicFiles = Get-Content -LiteralPath 'public-files.txt' -Encoding UTF8 | Where-Object { $_.Trim() }
git add -f -- $publicFiles
git diff --cached --name-only
```

Expected: 暂存列表与 `public-files.txt` 完全一致；没有本地完整资料目录中的额外文件。

- [ ] **Step 3: 验证暂存范围、大小和敏感信息**

Run:

```powershell
pwsh -NoProfile -File scripts/verify-public-site.ps1
$manifest = @(Get-Content -LiteralPath 'public-files.txt' -Encoding UTF8 | Where-Object { $_.Trim() } | Sort-Object)
$staged = @(git diff --cached --name-only | Sort-Object)
if (Compare-Object $manifest $staged) { throw 'Staged files differ from public-files.txt' }
$size = ($manifest | ForEach-Object { (Get-Item -LiteralPath $_).Length } | Measure-Object -Sum).Sum
if ($size -ge 1GB) { throw "Public payload is too large: $size bytes" }
if (@($manifest | Where-Object { (Get-Item -LiteralPath $_).Length -ge 100MB }).Count) { throw 'A public file is at least 100 MB' }
"PASS: staged manifest matches; size=$([math]::Round($size / 1MB, 2)) MB"
```

Expected: 验证退出 0；总体积小于 1 GB；单文件均小于 100 MB。

- [ ] **Step 4: 创建首次提交**

Run:

```powershell
git commit -m "feat: publish DuJia TongHua project showcase"
git status --short
```

Expected: 提交成功；未公开本地资料不出现在普通状态列表中。

- [ ] **Step 5: 推送 main 分支**

Run:

```powershell
git push -u origin main
```

Expected: `origin/main` 创建成功。若认证失败，停止并保留本地提交，不重复创建提交或修改远端 URL。

---

### Task 4: 启用 GitHub Pages 并完成公网验收

**Files:**
- Verify: `.github/workflows/pages.yml`
- Verify URL: `https://kelewang925-ship-it.github.io/dujia-tonghua-project-assets/`

**Interfaces:**
- Consumes: 已推送的 `origin/main` 与 Pages 工作流。
- Produces: 可公开访问并经过资源与交互验收的 GitHub Pages 网站。

- [ ] **Step 1: 在 GitHub 设置 Pages 发布源**

通过已登录 GitHub 网页打开：

```text
https://github.com/kelewang925-ship-it/dujia-tonghua-project-assets/settings/pages
```

将 `Build and deployment > Source` 设置为 `GitHub Actions`。如果已是 GitHub Actions，保持不变。

- [ ] **Step 2: 触发或等待 Pages 工作流**

打开：

```text
https://github.com/kelewang925-ship-it/dujia-tonghua-project-assets/actions
```

Expected: `Deploy GitHub Pages` 工作流完成，`deploy` job 为绿色。若未自动触发，使用 `Run workflow` 在 `main` 上手动触发一次。

- [ ] **Step 3: 验证公网响应和核心资源**

Run:

```powershell
$base = 'https://kelewang925-ship-it.github.io/dujia-tonghua-project-assets/'
$response = Invoke-WebRequest -Uri $base -UseBasicParsing
if ($response.StatusCode -ne 200) { throw "Homepage status: $($response.StatusCode)" }
if ($response.Content -notmatch '89 个逻辑页面') { throw 'Homepage content is not the expected showcase' }
if ($response.Content -notmatch '支持滚轮缩放') { throw 'Published page is missing the latest journey interaction copy' }
"PASS: public homepage returns 200 and contains the latest showcase"
```

- [ ] **Step 4: 浏览器交互验收**

打开公网地址并逐项确认：

1. Logo 比例正常。
2. 8 个模块入口跳转到设计稿区域并筛选正确模块。
3. 89 张逻辑页面设计稿可以筛选和打开灯箱。
4. 流程图可以通过按钮、键盘和滚轮缩放到 50%–500%。
5. 放大后的流程图可以拖动查看。
6. 浏览器控制台无资源 404。
7. 移动宽度下页面没有不可操作的横向溢出。

- [ ] **Step 5: 最终仓库边界核验**

Run:

```powershell
pwsh -NoProfile -File scripts/verify-public-site.ps1
git status --short
git log -1 --oneline
git ls-remote origin refs/heads/main
```

Expected: 本地验证通过；工作区没有已跟踪修改；远端 `main` 指向本地最新提交。

---

## Completion Evidence

完成时必须向用户提供：

- GitHub 仓库链接；
- GitHub Pages 公网链接；
- 首次公开提交哈希；
- 公开文件数量与总体积；
- Pages 工作流成功证据；
- 首页 HTTP 200、无缺图、模块筛选与流程图缩放验收结果；
- 明确说明完整本地资料未上传且仍保留在原位置。
