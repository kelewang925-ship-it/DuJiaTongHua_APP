# [已归档]《独家童话》项目图片生成提示词总表

> 归档状态：已完成首批核心图片生成与放置。  
> 归档原因：首批图片已按本文档生成并放入 `assets/images/illustrations/`，后续不再以本文档作为新的图片生成计划。  
> 后续使用：新的图片需求请查看 `docs/next-image-generation-plan.md`。  
> 原始用途：用于在新的 ChatGPT 图片生成对话中，批量生成《独家童话》项目所需的独立图片资产。  
> 目标目录：`assets/images/`  
> 重要说明：不要直接把 `assets/design/png/界面设计图*.png` 整图放进页面。效果图只作为视觉方向参考，最终需要生成或拆分为独立 PNG/WebP 图片资源。

---

## 1. 首批已完成图片

```text
assets/images/illustrations/home-cover-v1.png
assets/images/illustrations/couple-space-cover-v1.png
assets/images/illustrations/workshop-cover-v1.png
```

上述图片已由 `src/components/FairyImage.js` 接入：

```text
homeCover     → 首页 Hero 插画
coupleCover   → 情侣空间 Hero 插画
workshopCover → 童话工坊 Hero 插画
```

---

## 2. 后续不要继续使用本文档作为执行计划

新的图片生成需求请使用：

```text
docs/next-image-generation-plan.md
```

该文档会根据 `assets/images/README.md` 中的完整图片目录规划，继续补充相册、纪念日、空状态、贴纸、背景、封面、分享图等后续图片资产。
