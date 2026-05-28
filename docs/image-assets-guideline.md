# 《独家童话》项目专属图片资产规范与处理记录

本文档用于记录《独家童话》项目中所有图片资产的生成、命名、存放、接入和后续替换规则。后续凡是处理图片、插画、贴纸、AI生成图、图表、导出封面，都需要在本文档中追加记录。

---

## 1. 图片资产总原则

《独家童话》的图片资产不是普通装饰图，而是品牌体验的一部分。所有图片必须符合以下方向：童话绘本、奶油纸感、桃粉 / 干玫瑰 / 可可棕 / 琥珀金、轻手绘、贴纸感、温柔、克制、有留白。AI 能力呈现为“魔法感”，不做赛博科技风。

避免：高饱和少女粉、低幼卡通、强科技蓝紫粒子风、复杂大图堆叠、真实照片风格与绘本风混杂、未经裁切的整块效果图直接放入页面。

---

## 2. 图片资产目录规范

```text
assets/images/
  illustrations/       # 页面核心插画、空状态插画
  stickers/            # 小贴纸、胶带、星星、爱心、花朵、魔法棒等透明贴纸
  backgrounds/         # 纸张纹理、柔和渐变、页面底纹
  covers/              # PDF导出封面、纪念册封面、分享预览封面
  generated/           # AI生成内容结果图，仅用于开发期或用户生成结果缓存
```

---

## 3. 接入方式规范

页面不直接散落 `Image` 引用，统一通过组件接入。

| 组件 | 作用 |
| --- | --- |
| `src/components/FairyImage.js` | 页面 Hero 插画、封面图、空状态插画的统一入口。 |
| `src/components/FairyEmptyState.js` | 支持 `imageName`，可使用真实空状态图片。 |
| `src/components/FairySticker.js` | 贴纸图片统一入口。 |
| `src/components/FairyPage.js` | 支持 `backgroundName="creamPaper"` 和 `backgroundName="softPink"` 的背景纹理。 |
| `src/assets/fairyImages.js` | 插画、空状态、封面资产元数据映射。 |
| `src/assets/fairyStickers.js` | 贴纸资产元数据映射。 |

---

## 4. 当前已存在并已接入图片资产记录

### 4.1 `assets/images/illustrations/` 核心插画

| 资产 Key | 路径 | 来源 | 尺寸记录 | 格式 | 使用页面 | 接入组件 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `homeCover` | `assets/images/illustrations/home-cover-v1.png` | AI生成 | 计划 1200 × 900 | PNG | `app/(tabs)/index.js` | `FairyImage` | 已接入 |
| `coupleCover` | `assets/images/illustrations/couple-space-cover-v1.png` | AI生成 | 计划 1200 × 900 | PNG | `app/(tabs)/couple.js` | `FairyImage` | 已接入 |
| `workshopCover` | `assets/images/illustrations/workshop-cover-v1.png` | AI生成 | 计划 1200 × 900 | PNG | `app/(tabs)/workshop.js` | `FairyImage` | 已接入 |
| `albumCover` | `assets/images/illustrations/album-cover-v1.png` | AI生成 | 计划 1200 × 900 | PNG | `app/photo/album.js` | `FairyImage` | 已接入 |
| `anniversaryCover` | `assets/images/illustrations/anniversary-cover-v1.png` | AI生成 | 计划 1200 × 900 | PNG | `app/anniversary/index.js` | `FairyImage` | 已接入 |
| `exportCover` | `assets/images/illustrations/export-cover-v1.png` | AI生成 | 计划 1200 × 900 | PNG | `app/data/export-preview.js` | `FairyImage` | 已接入 |
| `timeCapsuleCover` | `assets/images/illustrations/time-capsule-cover-v1.png` | AI生成 | 计划 1200 × 900 | PNG | `app/time-capsule/settings.js` | `FairyImage` | 已接入 |

### 4.2 `assets/images/illustrations/` 空状态插画

| 资产 Key | 路径 | 来源 | 尺寸记录 | 格式 | 使用页面 | 接入组件 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `emptyAlbum` | `assets/images/illustrations/empty-album-v1.png` | AI生成 | 计划 800 × 600 | PNG | `app/photo/album.js` | `FairyEmptyState` + `FairyImage` | 已接入 |
| `emptyDiary` | `assets/images/illustrations/empty-diary-v1.png` | AI生成 | 计划 800 × 600 | PNG | `app/(tabs)/index.js`、`app/time-capsule/settings.js` | `FairyEmptyState` + `FairyImage` | 已接入 |
| `emptySearch` | `assets/images/illustrations/empty-search-v1.png` | AI生成 | 计划 800 × 600 | PNG | `app/search.js` | `FairyEmptyState` + `FairyImage` | 已接入 |
| `emptyNotification` | `assets/images/illustrations/empty-notification-v1.png` | AI生成 | 计划 800 × 600 | PNG | `app/notifications/index.js` | `FairyEmptyState` + `FairyImage` | 已接入 |
| `emptyAiHistory` | `assets/images/illustrations/empty-ai-history-v1.png` | AI生成 | 计划 800 × 600 | PNG | `app/ai/history.js` | `FairyEmptyState` + `FairyImage` | 已接入 |

### 4.3 `assets/images/stickers/` 贴纸资产

| 资产 Key | 路径 | 来源 | 尺寸记录 | 格式 | 使用页面 | 接入组件 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `heart` | `assets/images/stickers/heart-sticker-v1.png` | AI生成 | 计划 512 × 512 | PNG | 首页、情侣空间、童话工坊 | `FairySticker` | 已接入 |
| `star` | `assets/images/stickers/star-sticker-v1.png` | AI生成 | 计划 512 × 512 | PNG | 首页、情侣空间、童话工坊 | `FairySticker` | 已接入 |
| `flower` | `assets/images/stickers/flower-sticker-v1.png` | AI生成 | 计划 512 × 512 | PNG | 情侣空间、童话工坊 | `FairySticker` | 已接入 |
| `tapePink` | `assets/images/stickers/tape-pink-v1.png` | AI生成 | 计划 512 × 512 | PNG | 首页、童话工坊 | `FairySticker` | 已接入 |
| `tapeCream` | `assets/images/stickers/tape-cream-v1.png` | AI生成 | 计划 512 × 512 | PNG | PDF导出、分享预览、纪念日模板 | `FairySticker` | 已接入 |
| `magicWand` | `assets/images/stickers/magic-wand-v1.png` | AI生成 | 计划 512 × 512 | PNG | 童话工坊 | `FairySticker` | 已接入 |
| `polaroidCorner` | `assets/images/stickers/polaroid-corner-v1.png` | AI生成 | 计划 512 × 512 | PNG | 分享预览 | `FairySticker` | 已接入 |

### 4.4 `assets/images/backgrounds/` 背景资产

| 资产 Key | 路径 | 来源 | 尺寸记录 | 格式 | 使用页面 | 接入组件 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `creamPaper` | `assets/images/backgrounds/cream-paper-texture-v1.png` | AI生成 | 计划 1600 × 2400 | PNG | `app/ai/history.js`、`app/anniversary/template.js` | `FairyPage` | 已接入 |
| `softPink` | `assets/images/backgrounds/soft-pink-gradient-v1.png` | AI生成 | 计划 1600 × 2400 | PNG | `app/share-preview.js` | `FairyPage` | 已接入 |

### 4.5 `assets/images/covers/` 封面资产

| 资产 Key | 路径 | 来源 | 尺寸记录 | 格式 | 使用页面 | 接入组件 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `pdfMemoryBookCover` | `assets/images/covers/pdf-memory-book-cover-v1.png` | AI生成 | 计划 1600 × 2260 | PNG | `app/data/pdf-export.js` | `FairyImage` | 已接入 |
| `sharePreviewCover` | `assets/images/covers/share-preview-cover-v1.png` | AI生成 | 计划 1080 × 1440 | PNG | `app/share-preview.js` | `FairyImage` | 已接入 |
| `anniversaryShareCover` | `assets/images/covers/anniversary-share-cover-v1.png` | AI生成 | 计划 1080 × 1440 | PNG | `app/anniversary/template.js` | `FairyImage` | 已接入 |

---

## 5. 当前图片资产状态

```text
已生成图片：全部已登记
已生成插画：全部已接入
已生成空状态：全部已接入
已生成贴纸：全部已接入统一 FairySticker
已生成背景：全部已接入 FairyPage
已生成封面：全部已接入 FairyImage
当前无已知缺失图片资产
```

---

## 6. 后续图片处理记录模板

```markdown
### YYYY-MM-DD 图片处理记录

- 处理类型：新增 / 替换 / 压缩 / 裁切 / 接入 / 删除
- 资产路径：`assets/images/...`
- 来源：AI生成 / 设计稿切图 / 手绘 / 用户上传 / 临时占位
- 使用页面：`app/...`
- 组件：`src/components/...`
- 尺寸：宽 × 高
- 格式：PNG / JPG / WebP / SVG
- 说明：
- 后续待办：
```

---

## 7. 重要说明

当前 `assets/design/png/界面设计图.png`、`界面设计图2.png`、`界面设计风格图-2.png` 是整块效果展示图，不建议直接作为页面图片使用。正确做法是：以这些效果图作为视觉基准，重新生成或切出独立页面插画，再通过统一组件接入。
