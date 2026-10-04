# 114 页可编辑 HTML：UI 精修最终验收

日期：2026-10-04。分支：`codex/design-html-rebuild`。

## 交付范围

八个模块的 114 张正式页面与状态稿均完成逐页对照、差异记录、现有 HTML/CSS 修正和全套复核。正文、标题、表单、按钮、导航及主要状态由可编辑 DOM/CSS 实现；复杂插画、纸纹和少量极小装饰字使用局部 WebP 素材。

| 模块 | 页数 | 最终状态 |
| --- | ---: | --- |
| 账号登录 | 8 | 已验收 |
| 关联账号 | 9 | 已验收 |
| 童话首页与共同记录 | 12 | 已验收 |
| 重要时刻 | 17 | 已验收 |
| 童话工坊 | 10 | 已验收 |
| 我的与设置 | 12 | 已验收 |
| 宠物空间 | 25 | 已验收 |
| 共同回忆册 | 21 | 已验收 |
| **合计** | **114** | **全部通过** |

## 验收证据

| 要求 | 当前证据 | 结果 |
| --- | --- | --- |
| 每页先分析后修改 | [逐页差异与修正理由](README.md)，114 页修改前截图 | 已完成 |
| 原稿、当前 HTML/CSS、资源逐页对照 | `evidence/before/`、`evidence/after/` 的原稿并排图和页面截图；[页面清单](queue.json) | 114/114 |
| 五种手机宽度 | [全量结果](full-suite-results.json)，320/375/390/414/430px | 570 次通过 |
| 当前文件与验证结果一致 | 每页 `html_sha256`；`custom/` 与 `pages/` 字节一致；`verification/check_delivery.py` | 114/114 |
| 无横向滚动、文字溢出、破图、脚本异常或字体加载失败 | 全量浏览器结果的对应字段 | 全部通过 |
| 热区大小、边界与同级按钮交叠 | 全量 `smallTargets`、`clippedTargets`、`overlappingButtons`；密集内容在原区域内滚动 | 无非预期问题 |
| 安全区和底部区域 | 320px 模拟顶部 44px、底部 34px，页面可滚动 | 114/114 |
| 主要交互和长输入 | 八个 `*-interaction-results.json` 及 `verification/verify_*_ui.py` | 66 组通过 |
| 资源、路由、预览源文件 | 全量 `static` 结果；本地 HTTP 校验 | 无缺失或过期页面 |
| 全套视觉一致性 | [首页](evidence/after/full-suite/main.webp)、[表单](evidence/after/full-suite/forms.webp)、[阅读](evidence/after/full-suite/readers.webp)、[确认](evidence/after/full-suite/confirmation.webp)画廊及逐页原稿对照 | 已复核 |
| 前后截图与窄屏截图 | 114 份 before、114 份 after、114 份 320px PNG | 342 份齐全 |

## 主要修正

- 按原稿调整位置、字号、字重、行距、间距及信息分组，恢复纸纹、插画卡片和正确图片裁切。保留各模块原有布局差异。
- 标题与正文复用本地字体，数字保留合适的既有字体；移除不匹配的 emoji UI 图标和重复字符，复用原稿图标资源或原生 SVG。
- 共用安全区、最大宽度、按下、焦点、禁用及减少动效规则；透明点击区域与图标视觉尺寸分开处理，保持原稿按钮外观。
- 修正长书名、昵称、搜索词、日记、留言和补页的边界；补齐原生表单聚焦、上传控件访问和必要错误反馈。
- 覆盖位图中的固定勾选/描边，保证宠物、食物、装扮、地毯、回忆册主题和模板换选后能呈现正确状态。
- 全量复核额外发现并修正 15 页热区交叠或底部越界。具体修改前问题记录在逐页审计末尾；修正后逐页重拍并复查。
- 回忆册目录保留全部 12 项，在纸页内滚动，避免密集链接热区交叉；补页保留大图预览和横排表情选择，窄屏可水平滚动，SVG 预览随选择更新。补齐创建表单的合法月份检查。

## 交互回归范围

覆盖账号表单、密码显隐、验证码、错误禁用；邀请码/资料保存/邀请卡下载；记录搜索、日记及照片编辑/上传；纪念日、时光胶囊及留言演示；工坊素材、风格、预览、保存和分类；设置开关、资料、备份与 JSON 导出；宠物领养、精力/库存分支、装扮/房间、成长故事及提醒；回忆册创建、素材/主题/版式、书页编辑、页序、书签、补页、改名、归档和删除演示。

保持原有路由、示例数据及本地保存键。这是开发用 UI Demo，验证范围是页面内状态、路由、输入和演示反馈，未接入真实登录、关系、通知、生成、归档或删除服务。

## 使用与复查

预览：[114 页入口](http://127.0.0.1:8765/index.html) · [App 主页](http://127.0.0.1:8765/pages/m03-p02.html)。本地服务校验见 [preview-results.json](preview-results.json)。

修改源文件：`design-html/custom/{id}.html`；运行 `build.py --render-only` 更新 `pages/`。全量状态以本轮 [queue.json](queue.json) 为准，首次转换记录仍保留。

在仓库根目录、安装项目转换依赖与 `verification/requirements.txt` 后：

```powershell
python design-html/build.py --render-only
python design-html/full_suite_review.py
python design-html/verification/check_delivery.py
Get-ChildItem design-html/verification/verify_*_ui.py | ForEach-Object { python $_.FullName }
python design-html/verification/check_preview.py
```

验证脚本使用本机 Windows Chrome。本地服务可用 `python -m http.server 8765 --bind 127.0.0.1 --directory design-html` 启动。

全部工作在独立 worktree 中完成；原 `ui/optimize-layout` 工作区未执行修改、重置或清理。
