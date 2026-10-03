# 设计稿 HTML 转换工作区

当前范围为 `DuJiaTongHua_Project_Docs/新模块分布/` 八个模块根目录下的 114 张正式 PNG。`提案`、`历史未通过` 与旧版 `67页新版设计稿` 不进入本批。

## 当前转换层次

1. `assets/*-source.webp`：原稿对照，用于快速检查页面和图片资源。
2. `assets/*-art.webp`：OCR 去字后的视觉层，保留手绘插画、纸纹及复杂图形。
3. `pages/*.html`：每页独立 HTML；识别的文字由 `contenteditable` DOM 节点绘制，位置、颜色和置信度记录在 `manifest.json`。文字修改保存在浏览器本地。

首页 `index.html` 提供模块检索与逐页入口。单页默认展示原稿，点击“编辑文字层”查看和修改 HTML 层。这是批量转换基线，**不等同于逐页验收通过**。OCR 可能漏字、错字，去字层可能留下残影；按钮、表单和卡片仍需要继续按页面重建为原生 HTML/CSS 控件。

## 重建

在可用 Python 环境中安装 `requirements.txt`，然后运行：

```powershell
python design-html/build.py --source-root 'D:\projectCode\DuJiaTongHua\DuJiaTongHua_Project_Docs\新模块分布'
```

脚本严格检查正式稿数量为 114，输出至本目录。源 PNG 保留在资料目录，工作区只保存压缩 WebP 和 HTML。

## 校对要求

- 每页核对 OCR 文字、标点、字号、颜色和位置。
- 将可操作区域转成真正的按钮、输入框、开关、标签和导航，避免仅有文字层。
- 在设计稿原尺寸及常见手机宽度截图对照，消除错位、裁切和去字残影。
- `manifest.json` 的 OCR 置信度只用于排序，不代表文字正确。

原工作区 `ui/optimize-layout` 的未提交改动未移动或删除；本工作区使用 `codex/design-html-rebuild` 分支。
