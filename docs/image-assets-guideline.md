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

建议使用以下目录结构：

```text
assets/images/
  illustrations/       # 页面核心插画，通常用于首页、情侣空间、童话工坊、空状态等
  stickers/            # 小贴纸、胶带、星星、爱心、花朵、魔法棒等
  backgrounds/         # 纸张纹理、柔和渐变、页面底纹
  covers/              # PDF导出封面、纪念册封面、分享预览封面
  generated/           # AI生成内容结果图，仅用于开发期或用户生成结果缓存
```

当前阶段优先接入：

```text
assets/images/illustrations/home-cover.png
assets/images/illustrations/couple-space-cover.png
assets/images/illustrations/workshop-cover.png
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
album-empty-v1.png
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
star-gold-v1.png
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

## 6. AI插画生成提示词规范

### 6.1 通用风格提示词

```text
童话绘本风格，奶油纸质感，柔和桃粉和干玫瑰色，可可棕线条，琥珀金点缀，轻手绘，温柔治愈，留白充足，贴纸感组件，不要强科技感，不要高饱和，不要复杂背景，适合情侣情感记录APP
```

### 6.2 首页核心插画提示词

```text
一对情侣的恋爱绘本打开在奶油纸背景上，周围有小爱心、星星、胶带贴纸、拍立得照片角标，柔和桃粉和可可棕线条，温柔治愈，轻手绘童话绘本风，适合移动端APP首页Hero插画，留白充足
```

### 6.3 情侣空间插画提示词

```text
两个人的小小宇宙，情侣头像、爱心轨道、故事时间线、花朵贴纸和星星点缀，奶油纸质感，桃粉、干玫瑰、琥珀金，可可棕手绘线条，温柔童话绘本风，适合情侣空间页面Hero插画
```

### 6.4 童话工坊插画提示词

```text
温柔的AI魔法工坊，打开的绘本、魔法棒、星光、漫画分镜卡片和回忆放映机，奶油纸质感，桃粉、琥珀金、可可棕线条，轻手绘童话风，不要赛博科技感，适合AI创作页面Hero插画
```

---

## 7. 接入方式规范

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

## 8. 当前接入记录

| 日期 | 资产 | 类型 | 接入页面 | 当前状态 | 说明 |
| --- | --- | --- | --- | --- | --- |
| 2026-05-26 | `homeCover` | 核心插画 | `app/(tabs)/index.js` | 已接入组件映射 | 当前使用 `FairyImage` fallback 绘制插画，后续可替换为 `assets/images/illustrations/home-cover-v1.png`。 |
| 2026-05-26 | `coupleCover` | 核心插画 | `app/(tabs)/couple.js` | 已接入组件映射 | 当前使用 `FairyImage` fallback 绘制插画，后续可替换为 `assets/images/illustrations/couple-space-cover-v1.png`。 |
| 2026-05-26 | `workshopCover` | 核心插画 | `app/(tabs)/workshop.js` | 已接入组件映射 | 当前使用 `FairyImage` fallback 绘制插画，后续可替换为 `assets/images/illustrations/workshop-cover-v1.png`。 |
| 2026-05-27 | `FairyImage` 真实资源通道 | 组件能力 | `src/components/FairyImage.js` | 已接入（待填充资产） | `FairyImage` 已支持 `source` 和 `localSource` 真图渲染分支；当资产为空时继续 fallback 到 `FairyIllustration`，可安全逐页替换 PNG/WebP。 |

---

## 9. 后续图片处理记录模板

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

## 10. 重要说明

当前 `assets/design/png/界面设计图.png`、`界面设计图2.png`、`界面设计风格图-2.png` 是整块效果展示图，不建议直接作为页面图片使用。正确做法是：

1. 以这些效果图作为视觉基准；
2. 重新生成或切出独立页面插画；
3. 放入 `assets/images/illustrations/`；
4. 通过 `FairyImage` 统一接入页面；
5. 在本文档追加处理记录。
