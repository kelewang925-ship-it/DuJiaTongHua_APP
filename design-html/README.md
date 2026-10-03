# 设计稿 HTML 转换工作区

本目录覆盖 `DuJiaTongHua_Project_Docs/新模块分布/` 八个模块根目录下的 114 张正式 PNG。`提案`、`历史未通过` 与旧版 `67页新版设计稿` 不在本批范围。

## 文件说明

- `manifest.json`：114 张正式稿的顺序、原文件、画布尺寸和初始 OCR 信息。
- `assets/*-source.webp`：压缩后的原稿，用于逐页对照。
- `assets/*-art.webp`：去除 OCR 文字后的纸纹、插画与复杂装饰。去字结果仍可能有局部残影。
- `custom/*.html`：逐页手写的可编辑 HTML。标题、正文、表单、按钮和导航由 DOM/CSS 实现；插画与复杂纸纹使用素材。
- `pages/*.html`：可直接在浏览器打开的页面，由 `build.py --render-only` 从 `custom/` 复制。
- `index.html`：114 张页面的检索入口。
- `review-queue.json` 与 `WORKLIST.md`：逐页与逐模块的验收记录。`handcrafted-preview` 表示已重建，仍需通过最终人工校对。

用户选择了 **114 张逐页可编辑** 的交付范围。目前 114 张页面都有手写 HTML 和原稿对照，首轮页面渲染已完成。最终验收仍包括文字、布局、控件及浏览器两种尺寸的逐页复核，以 `WORKLIST.md` 和验收记录为准。

## 重新生成和检查

使用安装了 `requirements.txt` 依赖的 Python 环境：

```powershell
python design-html/build.py --render-only
python design-html/audit.py
```

重新从正式 PNG 生成 OCR 与素材时，使用：

```powershell
python design-html/build.py --source-root 'D:\projectCode\DuJiaTongHua\DuJiaTongHua_Project_Docs\新模块分布'
```

`build.py` 会优先复制 `custom/{id}.html`，不会用 OCR 基线覆盖手写页面。若增改了手写页面，运行 `--render-only` 更新 `pages/`。

原工作区 `ui/optimize-layout` 的未提交修改没有移动或删除；本工作区使用 `codex/design-html-rebuild` 分支。
