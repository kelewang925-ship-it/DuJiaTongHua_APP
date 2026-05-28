# 《独家童话》下一批图片生成计划

> 用途：首批首页、情侣空间、童话工坊 Hero 插画已经生成并接入后，本文件用于规划后续仍需要生成的图片资产。  
> 参考文件：`assets/images/README.md`、`docs/image-assets-guideline.md`、`docs/image-assets-implementation-plan.md`、`assets/design/png/界面设计图.png`、`assets/design/png/界面设计图2.png`、`assets/design/png/界面设计风格图-2.png`。  
> 当前状态：首批核心插画已完成；下一批应补齐相册、纪念日、导出、时光胶囊、空状态、贴纸、背景与封面。

---

## 1. 当前已完成图片

| 文件 | 类型 | 使用页面 | 接入状态 |
| --- | --- | --- | --- |
| `assets/images/illustrations/home-cover-v1.png` | 首页 Hero 插画 | `app/(tabs)/index.js` | 已通过 `FairyImage` 的 `homeCover` 接入 |
| `assets/images/illustrations/couple-space-cover-v1.png` | 情侣空间 Hero 插画 | `app/(tabs)/couple.js` | 已通过 `FairyImage` 的 `coupleCover` 接入 |
| `assets/images/illustrations/workshop-cover-v1.png` | 童话工坊 Hero 插画 | `app/(tabs)/workshop.js` | 已通过 `FairyImage` 的 `workshopCover` 接入 |

---

## 2. 下一批生成优先级

### P0：页面核心插画补齐

这些图片优先生成，因为它们对应当前已落地的功能页，生成后可继续扩展 `FairyImage` 映射。

| 文件 | 用途 | 建议尺寸 | 格式 |
| --- | --- | --- | --- |
| `assets/images/illustrations/album-cover-v1.png` | 相册 / 照片模块核心插画 | 1200 × 900 | PNG/WebP |
| `assets/images/illustrations/anniversary-cover-v1.png` | 纪念日模块核心插画 | 1200 × 900 | PNG/WebP |
| `assets/images/illustrations/export-cover-v1.png` | PDF 导出 / 数据导出核心插画 | 1200 × 900 | PNG/WebP |
| `assets/images/illustrations/time-capsule-cover-v1.png` | 时光胶囊核心插画 | 1200 × 900 | PNG/WebP |

---

### P1：空状态插画

这些图片用于替换当前 `FairyEmptyState` 的 SVG fallback，让空页面更贴近效果图。

| 文件 | 用途 | 建议尺寸 | 格式 |
| --- | --- | --- | --- |
| `assets/images/illustrations/empty-album-v1.png` | 空相册 | 800 × 600 | PNG/WebP |
| `assets/images/illustrations/empty-diary-v1.png` | 空日记 / 草稿为空 | 800 × 600 | PNG/WebP |
| `assets/images/illustrations/empty-search-v1.png` | 搜索无结果 | 800 × 600 | PNG/WebP |
| `assets/images/illustrations/empty-notification-v1.png` | 通知为空 | 800 × 600 | PNG/WebP |
| `assets/images/illustrations/empty-ai-history-v1.png` | AI 创作历史为空 | 800 × 600 | PNG/WebP |

---

### P2：贴纸资产

这些图片用于增强首页回忆墙、情侣时间轴、AI工坊、弹窗、分享图等贴纸感。所有贴纸要求透明背景。

| 文件 | 用途 | 建议尺寸 | 格式 |
| --- | --- | --- | --- |
| `assets/images/stickers/heart-sticker-v1.png` | 爱心贴纸 | 512 × 512 | PNG 透明背景 |
| `assets/images/stickers/star-sticker-v1.png` | 星星贴纸 | 512 × 512 | PNG 透明背景 |
| `assets/images/stickers/flower-sticker-v1.png` | 小花贴纸 | 512 × 512 | PNG 透明背景 |
| `assets/images/stickers/tape-pink-v1.png` | 粉色胶带 | 512 × 512 | PNG 透明背景 |
| `assets/images/stickers/tape-cream-v1.png` | 奶油色胶带 | 512 × 512 | PNG 透明背景 |
| `assets/images/stickers/magic-wand-v1.png` | AI 魔法棒 | 512 × 512 | PNG 透明背景 |
| `assets/images/stickers/polaroid-corner-v1.png` | 拍立得角标 | 512 × 512 | PNG 透明背景 |

---

### P3：背景与封面

| 文件 | 用途 | 建议尺寸 | 格式 |
| --- | --- | --- | --- |
| `assets/images/backgrounds/cream-paper-texture-v1.png` | 页面月白纸纹理背景 | 1600 × 2400 | PNG/WebP |
| `assets/images/backgrounds/soft-pink-gradient-v1.png` | 柔和桃粉渐变背景 | 1600 × 2400 | PNG/WebP |
| `assets/images/covers/pdf-memory-book-cover-v1.png` | PDF 回忆册封面 | 1600 × 2260 | PNG/WebP |
| `assets/images/covers/share-preview-cover-v1.png` | 分享预览封面 | 1080 × 1440 | PNG/WebP |
| `assets/images/covers/anniversary-share-cover-v1.png` | 纪念日分享封面 | 1080 × 1440 | PNG/WebP |

---

## 3. 通用生成要求

所有图片必须符合：

```text
童话绘本风格，奶油纸质感，柔和桃粉、干玫瑰、可可棕、琥珀金点缀，轻手绘线条，贴纸感，温柔治愈，留白充足，适合情侣情感记录 App，不要高饱和，不要科技蓝紫风，不要真实照片风，不要低幼卡通，不要复杂背景，不要出现真实文字，不要出现品牌 Logo。
```

---

## 4. P0 图片生成提示词

### 4.1 相册核心插画

目标文件：

```text
assets/images/illustrations/album-cover-v1.png
```

提示词：

```text
一组拍立得照片散落在奶油纸背景上，照片内容是抽象情侣剪影、花朵、晚霞和小星星，周围有胶带、爱心和贴纸装饰，桃粉、干玫瑰、可可棕和琥珀金配色，轻手绘童话绘本风，适合情侣相册页面 Hero 插画，留白充足，不要真实照片风，不要出现文字，不要logo
```

---

### 4.2 纪念日核心插画

目标文件：

```text
assets/images/illustrations/anniversary-cover-v1.png
```

提示词：

```text
一本打开的恋爱纪念册，页面上有日历、小爱心、干玫瑰花、丝带、星星贴纸和一枚小小戒指符号，奶油纸质感背景，桃粉、干玫瑰、琥珀金点缀，可可棕手绘线条，温柔童话绘本风，适合情侣纪念日管理页面 Hero 插画，留白充足，不要出现文字，不要logo
```

---

### 4.3 数据导出核心插画

目标文件：

```text
assets/images/illustrations/export-cover-v1.png
```

提示词：

```text
一本正在装订的恋爱回忆绘本，页面里夹着日记纸、照片贴纸、星星和小爱心，旁边有温柔丝带和琥珀金书签，奶油纸质感背景，桃粉、干玫瑰、可可棕线条，轻手绘童话绘本风，适合 PDF 导出和数据备份页面 Hero 插画，留白充足，不要出现文字，不要logo
```

---

### 4.4 时光胶囊核心插画

目标文件：

```text
assets/images/illustrations/time-capsule-cover-v1.png
```

提示词：

```text
一个温柔的时光胶囊玻璃瓶，里面装着小纸条、星星、爱心、拍立得照片和一束小花，放在奶油纸背景上，桃粉、干玫瑰、琥珀金点缀，可可棕手绘线条，轻手绘童话绘本风，适合情侣时光胶囊设置页面插画，留白充足，不要科技感，不要出现文字，不要logo
```

---

## 5. P1 空状态提示词

### 5.1 空相册

```text
一个空的拍立得相册页面，旁边有小爱心、胶带、花朵和星星贴纸，奶油纸质感背景，桃粉和可可棕手绘线条，温柔童话绘本风，表达“还没有照片但等待被填满”的感觉，留白充足，不要文字，不要logo
```

目标文件：`assets/images/illustrations/empty-album-v1.png`

### 5.2 空日记

```text
一张空白的奶油纸日记页，旁边有羽毛笔、小花、爱心和星星贴纸，桃粉、干玫瑰、可可棕配色，轻手绘童话绘本风，表达“今天的故事还没有开始”，留白充足，不要文字，不要logo
```

目标文件：`assets/images/illustrations/empty-diary-v1.png`

### 5.3 空搜索

```text
一个小小的放大镜正在奶油纸绘本页面上寻找星星和爱心，周围有轻微贴纸装饰，桃粉、干玫瑰、可可棕、琥珀金点缀，轻手绘童话绘本风，表达“没有找到这一页”，留白充足，不要文字，不要logo
```

目标文件：`assets/images/illustrations/empty-search-v1.png`

### 5.4 空通知

```text
一个温柔的小信封放在奶油纸背景上，旁边有爱心、星星和小花贴纸，桃粉、干玫瑰、可可棕配色，轻手绘童话绘本风，表达“暂时没有新的消息”，留白充足，不要文字，不要logo
```

目标文件：`assets/images/illustrations/empty-notification-v1.png`

---

## 6. 新对话使用方法

打开新的图片生成对话后：

1. 上传参考图：

```text
assets/design/png/界面设计图.png
assets/design/png/界面设计图2.png
assets/design/png/界面设计风格图-2.png
```

2. 说明项目风格：

```text
我要继续为《独家童话》生成项目图片资产。首批首页、情侣空间、童话工坊 Hero 插画已经完成。现在请根据 docs/next-image-generation-plan.md 中 P0/P1 的提示词，继续生成相册、纪念日、数据导出、时光胶囊和空状态插画。所有图片必须符合童话绘本、奶油纸感、桃粉、干玫瑰、可可棕、琥珀金、轻手绘、贴纸感、温柔治愈、有留白的方向。不要生成页面截图，不要出现文字，不要 logo。
```

3. 分批生成，建议顺序：

```text
P0 页面核心插画 → P1 空状态插画 → P2 贴纸资产 → P3 背景与封面
```

4. 图片生成后，放入对应目录，并更新：

```text
docs/image-assets-guideline.md
docs/project-file-structure.md
src/assets/fairyImages.js
src/components/FairyImage.js
```

---

## 7. 接入建议

### 7.1 扩展 `src/assets/fairyImages.js`

新增映射：

```js
albumCover: {
  key: 'albumCover',
  title: '相册绘本封面',
  scene: 'album',
  localSource: require('../../assets/images/illustrations/album-cover-v1.png'),
  plannedPath: 'assets/images/illustrations/album-cover-v1.png',
  description: '相册与照片模块的绘本封面图。',
},
```

### 7.2 扩展 `src/components/FairyImage.js`

新增：

```js
albumCover: require('../../assets/images/illustrations/album-cover-v1.png'),
anniversaryCover: require('../../assets/images/illustrations/anniversary-cover-v1.png'),
```

### 7.3 页面替换优先级

```text
app/photo/album.js
app/anniversary/index.js
app/data/export-preview.js
app/time-capsule/settings.js
FairyEmptyState 相关页面
```
