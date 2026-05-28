# 《独家童话》项目专属图片资产规范与处理记录

本文档用于记录《独家童话》项目中所有图片资产的生成、命名、存放、接入和后续替换规则。后续凡是处理图片、插画、贴纸、AI生成图、图表、导出封面，都需要在本文档中追加记录。

---

## 1. 图片资产总原则

《独家童话》的图片资产不是普通装饰图，而是品牌体验的一部分。所有图片必须符合以下方向：

- 童话绘本
- 奶油纸感
- 桃粉 / 干玫瑰 / 可可棕 / 琥珀金
- 轻手绘
- 贴纸感
- 温柔、克制、有留白
- AI能力呈现为“魔法感”，不做赛博科技风

避免：

- 高饱和少女粉
- 低幼卡通
- 强科技蓝紫粒子风
- 复杂大图堆叠
- 真实照片风格与绘本风混杂
- 未经裁切的整块效果图直接放入页面

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

## 3. 命名规则

### 3.1 插画命名

```text
页面/模块名 + 用途 + 版本
```

示例：

```text
home-cover-v1.png
couple-space-cover-v1.png
workshop-cover-v1.png
anniversary-cover-v1.png
empty-album-v1.png
```

### 3.2 贴纸命名

```text
元素名 + 风格 + 版本
```

示例：

```text
heart-sticker-v1.png
flower-sticker-v1.png
tape-pink-v1.png
magic-wand-v1.png
star-sticker-v1.png
```

### 3.3 AI生成结果命名

```text
业务类型 + 时间戳 + 状态
```

示例：

```text
comic-20260526-preview.png
video-cover-20260526-draft.png
```

---

## 4. 图片尺寸建议

| 类型 | 建议尺寸 | 用途 |
| --- | --- | --- |
| 核心页面插画 | 1024 × 768 或 1200 × 900 | 首页、情侣空间、童话工坊 Hero 区域 |
| 空状态插画 | 800 × 600 | 空相册、无日记、无AI作品等 |
| 贴纸 | 256 × 256 / 512 × 512 | 小花、爱心、星星、胶带、魔法棒 |
| 页面背景纹理 | 1600 × 2400 | 月白纸感背景 |
| 分享卡片封面 | 1080 × 1440 | 分享预览、纪念日卡片 |
| PDF封面 | 1600 × 2260 | A4比例导出封面 |

> 当前 GitHub 工具只能确认文件存在与 SHA，不能直接读取二进制图片尺寸。下表尺寸按生成计划规格记录，后续可用本地图片工具再补充实际宽高。

---

## 5. 图片格式规范

| 类型 | 推荐格式 | 说明 |
| --- | --- | --- |
| 插画 | PNG / WebP | 保留透明或柔和边缘，适合移动端展示 |
| 贴纸 | PNG | 需要透明背景 |
| 背景纹理 | WebP / PNG | 控制体积，不要太大 |
| 图标 | SVG优先 | 若是手绘图标，也可用 PNG |
| 用户生成结果 | JPG / WebP | 图像体积更小 |

---

## 6. 接入方式规范

页面不直接散落 `Image` 引用，统一通过组件接入。

推荐组件：

```text
src/components/FairyImage.js
```

职责：

- 统一管理 image source
- 支持 `name` 映射，例如 `homeCover`、`coupleCover`、`workshopCover`
- 支持 fallback 到 `FairyIllustration`
- 支持圆角、描边、背景色、resizeMode
- 方便后续替换 PNG / WebP / 远程 CDN 图片

---

## 7. 当前已存在图片资产记录

### 7.1 `assets/images/illustrations/` 核心插画

| 资产 Key | 路径 | 来源 | 尺寸记录 | 格式 | 使用页面 | 是否已接入 FairyImage | 状态 | 说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `homeCover` | `assets/images/illustrations/home-cover-v1.png` | AI生成，依据首批提示词 | 计划 1200 × 900 | PNG | `app/(tabs)/index.js` | 是 | 已接入 | 首页 Hero 真实插画。 |
| `coupleCover` | `assets/images/illustrations/couple-space-cover-v1.png` | AI生成，依据首批提示词 | 计划 1200 × 900 | PNG | `app/(tabs)/couple.js` | 是 | 已接入 | 情侣空间 Hero 真实插画。 |
| `workshopCover` | `assets/images/illustrations/workshop-cover-v1.png` | AI生成，依据首批提示词 | 计划 1200 × 900 | PNG | `app/(tabs)/workshop.js` | 是 | 已接入 | 童话工坊 Hero 真实插画。 |
| `albumCover` | `assets/images/illustrations/album-cover-v1.png` | AI生成，依据下一批计划提示词 | 计划 1200 × 900 | PNG | `app/photo/album.js` / 照片模块 | 否 | 已存在，待接入 | 相册/照片模块核心插画。 |
| `anniversaryCover` | `assets/images/illustrations/anniversary-cover-v1.png` | AI生成，依据下一批计划提示词 | 计划 1200 × 900 | PNG | `app/anniversary/index.js` | 否 | 已存在，待接入 | 纪念日模块核心插画。 |
| `exportCover` | `assets/images/illustrations/export-cover-v1.png` | AI生成，依据下一批计划提示词 | 计划 1200 × 900 | PNG | `app/data/export-preview.js` / `app/data/pdf-export.js` | 否 | 已存在，待接入 | 数据导出/PDF预览核心插画。 |
| `timeCapsuleCover` | `assets/images/illustrations/time-capsule-cover-v1.png` | AI生成，依据下一批计划提示词 | 计划 1200 × 900 | PNG | `app/time-capsule/settings.js` | 否 | 已存在，待接入 | 时光胶囊核心插画。 |

### 7.2 `assets/images/illustrations/` 空状态插画

| 资产 Key | 路径 | 来源 | 尺寸记录 | 格式 | 使用页面 | 是否已接入 FairyImage | 状态 | 说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `emptyAlbum` | `assets/images/illustrations/empty-album-v1.png` | AI生成，依据下一批计划提示词 | 计划 800 × 600 | PNG | `app/photo/album.js`、照片相关空状态 | 否 | 已存在，待接入 | 空相册插画。 |
| `emptyDiary` | `assets/images/illustrations/empty-diary-v1.png` | AI生成，依据下一批计划提示词 | 计划 800 × 600 | PNG | 日记/草稿相关空状态 | 否 | 已存在，待接入 | 空日记插画。 |
| `emptySearch` | `assets/images/illustrations/empty-search-v1.png` | AI生成，依据下一批计划提示词 | 计划 800 × 600 | PNG | `app/search.js` | 否 | 已存在，待接入 | 搜索无结果插画。 |
| `emptyNotification` | `assets/images/illustrations/empty-notification-v1.png` | AI生成，依据下一批计划提示词 | 计划 800 × 600 | PNG | `app/notifications/index.js` | 否 | 已存在，待接入 | 通知为空插画。 |

### 7.3 `assets/images/stickers/` 贴纸资产

| 资产 Key | 路径 | 来源 | 尺寸记录 | 格式 | 使用页面 | 是否已接入 FairyImage | 状态 | 说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `heartSticker` | `assets/images/stickers/heart-sticker-v1.png` | AI生成，依据下一批计划提示词 | 计划 512 × 512 | PNG | 首页、时间轴、弹窗、分享图装饰 | 否 | 已存在，待接入 | 爱心贴纸。 |
| `starSticker` | `assets/images/stickers/star-sticker-v1.png` | AI生成，依据下一批计划提示词 | 计划 512 × 512 | PNG | 首页、AI工坊、空状态装饰 | 否 | 已存在，待接入 | 星星贴纸。 |
| `flowerSticker` | `assets/images/stickers/flower-sticker-v1.png` | AI生成，依据下一批计划提示词 | 计划 512 × 512 | PNG | 情侣空间、纪念日、封面装饰 | 否 | 已存在，待接入 | 小花贴纸。 |
| `tapePink` | `assets/images/stickers/tape-pink-v1.png` | AI生成，依据下一批计划提示词 | 计划 512 × 512 | PNG | 卡片胶带、回忆墙、时间轴装饰 | 否 | 已存在，待接入 | 桃粉胶带贴纸。 |
| `magicWand` | `assets/images/stickers/magic-wand-v1.png` | AI生成，依据下一批计划提示词 | 计划 512 × 512 | PNG | AI工坊、AI流程页装饰 | 否 | 已存在，待接入 | 魔法棒贴纸。 |

### 7.4 `assets/images/covers/` 封面资产

| 资产 Key | 路径 | 来源 | 尺寸记录 | 格式 | 使用页面 | 是否已接入 FairyImage | 状态 | 说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `pdfMemoryBookCover` | `assets/images/covers/pdf-memory-book-cover-v1.png` | AI生成，依据下一批计划提示词 | 计划 1600 × 2260 | PNG | `app/data/export-preview.js` / PDF导出流程 | 否 | 已存在，待接入 | PDF回忆册封面。 |
| `sharePreviewCover` | `assets/images/covers/share-preview-cover-v1.png` | AI生成，依据下一批计划提示词 | 计划 1080 × 1440 | PNG | `app/share-preview.js` | 否 | 已存在，待接入 | 分享预览封面。 |

---

## 8. 当前仍缺失的图片资产

按 `docs/next-image-generation-plan.md` 计划，目前仍未确认存在：

```text
assets/images/illustrations/empty-ai-history-v1.png
assets/images/stickers/tape-cream-v1.png
assets/images/stickers/polaroid-corner-v1.png
assets/images/backgrounds/cream-paper-texture-v1.png
assets/images/backgrounds/soft-pink-gradient-v1.png
assets/images/covers/anniversary-share-cover-v1.png
```

---

## 9. 后续图片接入建议

下一步不是继续生成大量新图，而是先把已存在但未接入的图片接入项目：

```text
1. 扩展 src/assets/fairyImages.js，登记 albumCover、exportCover、timeCapsuleCover、emptyAlbum、emptyDiary、emptySearch、emptyNotification 等 key。
2. 扩展 src/components/FairyImage.js 的 imageSourceMap。
3. 在 app/photo/album.js、app/anniversary/index.js、app/data/export-preview.js、app/time-capsule/settings.js 中替换对应 Hero 插画。
4. 扩展 FairyEmptyState，使其可以通过 imageName 使用真实空状态插画。
5. 贴纸类建议新增 FairySticker 组件统一接入，不要散落 Image require。
```

---

## 10. 后续图片处理记录模板

每次新增、替换、压缩、裁切或接入图片时，按以下格式追加：

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

## 11. 重要说明

当前 `assets/design/png/界面设计图.png`、`界面设计图2.png`、`界面设计风格图-2.png` 是整块效果展示图，不建议直接作为页面图片使用。正确做法是：

1. 以这些效果图作为视觉基准；
2. 重新生成或切出独立页面插画；
3. 放入 `assets/images/illustrations/`、`assets/images/stickers/`、`assets/images/backgrounds/` 或 `assets/images/covers/`；
4. 通过 `FairyImage`、`FairyEmptyState` 或后续 `FairySticker` 统一接入页面；
5. 在本文档追加处理记录。
