# [已归档]《独家童话》剩余图片生成提示词

> 归档状态：已完成。  
> 归档原因：本文档中列出的 6 张剩余图片已放入对应目录，并已接入项目。  
> 当前图片资产状态请查看：`docs/image-assets-guideline.md`。  
> 原始用途：记录剩余缺失图片资产的生成提示词。

---

## 1. 已完成图片清单

```text
assets/images/illustrations/empty-ai-history-v1.png
assets/images/stickers/tape-cream-v1.png
assets/images/stickers/polaroid-corner-v1.png
assets/images/backgrounds/cream-paper-texture-v1.png
assets/images/backgrounds/soft-pink-gradient-v1.png
assets/images/covers/anniversary-share-cover-v1.png
```

---

## 2. 已接入位置

| 图片 | 接入位置 | 入口组件 |
| --- | --- | --- |
| `empty-ai-history-v1.png` | `app/ai/history.js` | `FairyEmptyState` + `FairyImage` |
| `tape-cream-v1.png` | PDF导出、分享预览、纪念日模板 | `FairySticker` |
| `polaroid-corner-v1.png` | `app/share-preview.js` | `FairySticker` |
| `cream-paper-texture-v1.png` | `app/ai/history.js`、`app/anniversary/template.js` | `FairyPage backgroundName="creamPaper"` |
| `soft-pink-gradient-v1.png` | `app/share-preview.js` | `FairyPage backgroundName="softPink"` |
| `anniversary-share-cover-v1.png` | `app/anniversary/template.js` | `FairyImage` |

---

## 3. 原始提示词归档说明

后续如果需要重新生成这些图片，可从 Git 历史中查看本文档归档前版本。当前版本不再作为执行计划使用。
