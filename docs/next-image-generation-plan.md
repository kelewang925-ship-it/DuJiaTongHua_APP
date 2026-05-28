# 《独家童话》下一批图片生成计划

> 用途：根据 `assets/images/` 当前真实文件状态，继续规划仍缺失的图片资产，并安排已存在图片的接入工作。  
> 参考文件：`assets/images/README.md`、`docs/image-assets-guideline.md`、`docs/image-assets-implementation-plan.md`、`assets/design/png/界面设计图.png`、`assets/design/png/界面设计图2.png`、`assets/design/png/界面设计风格图-2.png`。  
> 当前状态：首批核心插画已接入；第二批多张插画、空状态、贴纸和封面已存在但尚未全部接入；剩余少量图片仍需生成。

---

## 1. 已生成并已接入图片

| 文件 | 类型 | 使用页面 | 接入状态 |
| --- | --- | --- | --- |
| `assets/images/illustrations/home-cover-v1.png` | 首页 Hero 插画 | `app/(tabs)/index.js` | 已通过 `FairyImage homeCover` 接入 |
| `assets/images/illustrations/couple-space-cover-v1.png` | 情侣空间 Hero 插画 | `app/(tabs)/couple.js` | 已通过 `FairyImage coupleCover` 接入 |
| `assets/images/illustrations/workshop-cover-v1.png` | 童话工坊 Hero 插画 | `app/(tabs)/workshop.js` | 已通过 `FairyImage workshopCover` 接入 |

---

## 2. 已生成但尚未接入图片

### 2.1 页面核心插画

这些图片已经存在于 `assets/images/illustrations/`，下一步应优先接入页面。

| 文件 | 建议接入页面 | 建议组件 Key | 当前状态 |
| --- | --- | --- | --- |
| `assets/images/illustrations/album-cover-v1.png` | `app/photo/album.js`、照片相关页面 | `albumCover` | 已生成，待接入 |
| `assets/images/illustrations/anniversary-cover-v1.png` | `app/anniversary/index.js`、纪念日相关页面 | `anniversaryCover` | 已生成，待接入 |
| `assets/images/illustrations/export-cover-v1.png` | `app/data/export-preview.js`、`app/data/pdf-export.js` | `exportCover` | 已生成，待接入 |
| `assets/images/illustrations/time-capsule-cover-v1.png` | `app/time-capsule/settings.js` | `timeCapsuleCover` | 已生成，待接入 |

### 2.2 空状态插画

| 文件 | 建议使用场景 | 建议组件 Key | 当前状态 |
| --- | --- | --- | --- |
| `assets/images/illustrations/empty-album-v1.png` | 空相册、无照片 | `emptyAlbum` | 已生成，待接入 |
| `assets/images/illustrations/empty-diary-v1.png` | 空日记、草稿为空 | `emptyDiary` | 已生成，待接入 |
| `assets/images/illustrations/empty-search-v1.png` | 搜索无结果 | `emptySearch` | 已生成，待接入 |
| `assets/images/illustrations/empty-notification-v1.png` | 通知为空 | `emptyNotification` | 已生成，待接入 |

### 2.3 贴纸资产

| 文件 | 建议使用场景 | 建议组件 Key | 当前状态 |
| --- | --- | --- | --- |
| `assets/images/stickers/heart-sticker-v1.png` | 首页、时间轴、弹窗、分享图装饰 | `heartSticker` | 已生成，待接入 |
| `assets/images/stickers/star-sticker-v1.png` | 首页、AI工坊、空状态装饰 | `starSticker` | 已生成，待接入 |
| `assets/images/stickers/flower-sticker-v1.png` | 情侣空间、纪念日、封面装饰 | `flowerSticker` | 已生成，待接入 |
| `assets/images/stickers/tape-pink-v1.png` | 卡片胶带、回忆墙、时间轴装饰 | `tapePink` | 已生成，待接入 |
| `assets/images/stickers/magic-wand-v1.png` | AI工坊、AI流程页装饰 | `magicWand` | 已生成，待接入 |

### 2.4 封面资产

| 文件 | 建议使用场景 | 建议组件 Key | 当前状态 |
| --- | --- | --- | --- |
| `assets/images/covers/pdf-memory-book-cover-v1.png` | PDF导出预览、回忆册封面 | `pdfMemoryBookCover` | 已生成，待接入 |
| `assets/images/covers/share-preview-cover-v1.png` | 分享预览页 | `sharePreviewCover` | 已生成，待接入 |

---

## 3. 当前仍需生成图片

根据实际文件检查，目前仍缺失：

| 文件 | 类型 | 用途 | 优先级 |
| --- | --- | --- | --- |
| `assets/images/illustrations/empty-ai-history-v1.png` | 空状态插画 | AI创作历史为空 | P1 |
| `assets/images/stickers/tape-cream-v1.png` | 贴纸 | 奶油色胶带 | P2 |
| `assets/images/stickers/polaroid-corner-v1.png` | 贴纸 | 拍立得照片角标 | P2 |
| `assets/images/backgrounds/cream-paper-texture-v1.png` | 背景 | 月白纸感页面背景 | P3 |
| `assets/images/backgrounds/soft-pink-gradient-v1.png` | 背景 | 柔和桃粉渐变背景 | P3 |
| `assets/images/covers/anniversary-share-cover-v1.png` | 封面 | 纪念日分享封面 | P3 |

---

## 4. 当前最优先任务：接入已生成图片

在继续生成新图片前，优先完成接入：

```text
1. 扩展 src/assets/fairyImages.js
2. 扩展 src/components/FairyImage.js 的 imageSourceMap
3. 扩展 FairyEmptyState 支持 imageName 或 imageSource
4. 新增 FairySticker 组件，统一接入 stickers
5. 将 album / anniversary / export / time-capsule 页面 Hero 替换为真实图片
6. 将 search / notifications / album 等空状态替换为真实空状态图
7. 将 PDF导出和分享预览页面接入 covers 图片
```

---

## 5. 接入建议顺序

### P0 接入

```text
album-cover-v1.png → app/photo/album.js
anniversary-cover-v1.png → app/anniversary/index.js
export-cover-v1.png → app/data/export-preview.js / app/data/pdf-export.js
time-capsule-cover-v1.png → app/time-capsule/settings.js
```

### P1 接入

```text
empty-album-v1.png → FairyEmptyState / app/photo/album.js
empty-search-v1.png → FairyEmptyState / app/search.js
empty-notification-v1.png → FairyEmptyState / app/notifications/index.js
empty-diary-v1.png → drafts / diary empty related pages
```

### P2 接入

```text
heart-sticker-v1.png
star-sticker-v1.png
flower-sticker-v1.png
tape-pink-v1.png
magic-wand-v1.png
```

建议新增：

```text
src/components/FairySticker.js
src/assets/fairyStickers.js
```

---

## 6. 剩余图片生成提示词

### 6.1 AI 创作历史空状态

目标文件：

```text
assets/images/illustrations/empty-ai-history-v1.png
```

提示词：

```text
一个安静的 AI 魔法工坊空桌面，奶油纸背景上有一本合上的小绘本、魔法棒、几颗星星和空白漫画分镜卡片，桃粉、干玫瑰、可可棕、琥珀金点缀，轻手绘童话绘本风，表达“还没有 AI 作品，等待第一段回忆被施展魔法”，留白充足，不要文字，不要 logo，不要科技蓝紫风
```

---

### 6.2 奶油色胶带贴纸

目标文件：

```text
assets/images/stickers/tape-cream-v1.png
```

提示词：

```text
透明背景，一段半透明奶油色纸胶带贴纸，带轻微纸张纹理，可可棕极细描边，温柔手账风，适合贴在恋爱绘本卡片边缘，512×512，PNG透明背景，不要文字，不要logo
```

---

### 6.3 拍立得角标贴纸

目标文件：

```text
assets/images/stickers/polaroid-corner-v1.png
```

提示词：

```text
透明背景，一个手绘拍立得照片角标贴纸，奶油白纸质感，可可棕细线，少量桃粉小爱心和琥珀金星星点缀，适合情侣相册和回忆墙装饰，512×512，PNG透明背景，不要文字，不要logo
```

---

### 6.4 月白纸感背景

目标文件：

```text
assets/images/backgrounds/cream-paper-texture-v1.png
```

提示词：

```text
浅奶油白月白纸张纹理背景，柔和细腻，有轻微纸纤维和温暖颗粒感，低对比度，适合移动端情侣童话绘本App页面背景，1600×2400，不能有文字、logo、明显图案，不要高饱和
```

---

### 6.5 柔和桃粉渐变背景

目标文件：

```text
assets/images/backgrounds/soft-pink-gradient-v1.png
```

提示词：

```text
柔和桃粉到奶油白的渐变背景，带非常轻微纸张纹理和温暖光晕，低饱和，适合移动端情侣童话绘本App的卡片背景或分享背景，1600×2400，不要文字，不要logo，不要复杂图案
```

---

### 6.6 纪念日分享封面

目标文件：

```text
assets/images/covers/anniversary-share-cover-v1.png
```

提示词：

```text
一张适合情侣纪念日分享的竖版童话卡片封面，奶油纸背景，中心是打开的纪念册、日历小图标、干玫瑰花、丝带、爱心和星星贴纸，桃粉、干玫瑰、可可棕、琥珀金点缀，温柔治愈，留白充足，1080×1440，不要文字，不要logo
```

---

## 7. 新对话使用方法

打开新的图片生成对话后：

1. 上传参考图：

```text
assets/design/png/界面设计图.png
assets/design/png/界面设计图2.png
assets/design/png/界面设计风格图-2.png
```

2. 说明项目风格：

```text
我要继续为《独家童话》生成项目图片资产。当前大部分页面核心插画、空状态图、贴纸和封面已经生成；现在只需要补齐 docs/next-image-generation-plan.md 第 3 节列出的缺失图片。所有图片必须符合童话绘本、奶油纸感、桃粉、干玫瑰、可可棕、琥珀金、轻手绘、贴纸感、温柔治愈、有留白的方向。不要生成页面截图，不要出现文字，不要 logo。
```

3. 生成完成后，把图片放入对应目录，并更新：

```text
docs/image-assets-guideline.md
docs/project-file-structure.md
src/assets/fairyImages.js
src/components/FairyImage.js
```

贴纸接入时，建议新增：

```text
src/assets/fairyStickers.js
src/components/FairySticker.js
```
