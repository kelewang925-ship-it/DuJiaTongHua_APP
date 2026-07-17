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

### 2026-07-14 AI 漫画结果页图片处理记录

- 处理类型：新增、生成、接入
- 资产 Key：`aiComicTriptych`
- 资产路径：`assets/images/illustrations/ai-comic-memory-triptych-v1.png`
- 来源：内置 imagegen 图片生成模型
- 使用页面：`app/ai/comic-result.js`
- 组件：`FairyImage`
- 尺寸：2172 × 724
- 格式：PNG，无透明通道
- 生成提示词：三联横向恋爱绘本漫画；同一对年轻中国情侣依次走在黄昏花树下、春雨中共撑奶油色雨伞、月夜萤火旁并肩而坐；手绘水彩和彩铅纸感；月白、桃粉、干玫瑰、可可棕和低饱和蓝紫配色；三格之间使用奶油纸分隔；禁止文字、气泡、数字、Logo、水印和赛博霓虹。
- 检查结果：人物在三格中保持一致，主体完整，无异常文字和水印，比例适合结果页横向预览。

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
---

## 8. 2026-06-10 Stage 2 image asset record

> This Stage 2 record adds reusable PNG assets only. No business page code was modified, and no full effect screenshot was placed directly into page assets.

### 8.1 Background assets

| Asset path | Source | Size | Format | Usage | Impacted routes | Component | Follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `assets/images/backgrounds/cream-paper-texture-v2.png` | Programmatic hand-drawn paper texture derived from `stage-0/00-visual-style-guide.png` | `1200x1800` | PNG | Global cream paper background | All `FairyPage` routes | `FairyPage` | Add metadata/key in Stage 3. |
| `assets/images/backgrounds/soft-pink-gradient-v2.png` | Programmatic soft pink paper background derived from Stage 0 and share/anniversary effects | `1200x1800` | PNG | Soft pink celebration/share background | `app/share-preview.js`, anniversary routes | `FairyPage` | Add metadata/key in Stage 3. |

### 8.2 TabBar and UI icon assets

| Asset path | Source | Size | Format | Usage | Impacted routes | Component | Follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `assets/images/icons/tabbar/story-v2.png` | Programmatic hand-drawn icon from Stage 0 TabBar reference | `256x256` | PNG | Story/home tab icon | `app/(tabs)/index.js` | `FairyTabBar` | Map in Stage 3/5. |
| `assets/images/icons/tabbar/mood-v2.png` | Programmatic hand-drawn icon from Stage 0 TabBar reference | `256x256` | PNG | Mood tab icon | `app/(tabs)/couple.js` | `FairyTabBar` | Map in Stage 3/5. |
| `assets/images/icons/tabbar/record-v2.png` | Programmatic hand-drawn icon from Stage 0 TabBar reference | `256x256` | PNG | Record tab icon | Main tab layout | `FairyTabBar` | Map in Stage 3/5. |
| `assets/images/icons/tabbar/us-v2.png` | Programmatic hand-drawn icon from Stage 0 TabBar reference | `256x256` | PNG | Couple/us tab icon | Couple tab and related tab slot | `FairyTabBar` | Map in Stage 3/5. |
| `assets/images/icons/tabbar/mine-v2.png` | Programmatic hand-drawn icon from Stage 0 TabBar reference | `256x256` | PNG | Mine tab icon | `app/(tabs)/mine.js` | `FairyTabBar` | Map in Stage 3/5. |
| `assets/images/icons/ui/pen-v2.png` | Programmatic hand-drawn input icon from Stage 0 input reference | `256x256` | PNG | Input/edit pen icon | Login, diary, AI config, help feedback | `FairyInput` | Add icon slot in Stage 3. |
| `assets/images/icons/ui/link-v2.png` | Programmatic hand-drawn utility icon from account invite effect | `256x256` | PNG | Invite/share link icon | `app/account/invite.js`, share routes | Future icon map | Add metadata in Stage 3. |
| `assets/images/icons/ui/copy-v2.png` | Programmatic hand-drawn utility icon from account invite effect | `256x256` | PNG | Copy action icon | `app/account/invite.js` | Future icon map | Add metadata in Stage 3. |

### 8.3 Core functional icon assets

| Asset path | Source | Size | Format | Usage | Impacted routes | Component | Follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `assets/images/icons/home/record-v2.png` | Stage 2 home record center effect | `256x256` | PNG | Record card icon | `app/(tabs)/index.js`, diary routes | `MemoryCard` | Add icon metadata in Stage 3. |
| `assets/images/icons/home/tag-v2.png` | Stage 2 home and tag effects | `256x256` | PNG | Tag/category icon | Home, tags routes | `FairyTag` | Add icon metadata in Stage 3. |
| `assets/images/icons/home/mood-v2.png` | Stage 2 home/couple effects | `256x256` | PNG | Mood icon | Home, diary, couple routes | `FairyTag` | Add icon metadata in Stage 3. |
| `assets/images/icons/couple/timeline-v2.png` | Couple space and activity detail effects | `256x256` | PNG | Timeline/activity icon | `app/(tabs)/couple.js`, couple detail routes | `CoupleTimeline` | Add icon metadata in Stage 3. |
| `assets/images/icons/couple/reaction-v2.png` | Couple activity/comment effects | `256x256` | PNG | Reaction icon | Couple detail, comments routes | Future shared comments component | Add icon metadata in Stage 3. |
| `assets/images/icons/couple/comment-v2.png` | Comments list and couple detail effects | `256x256` | PNG | Couple comment icon | Couple detail, comments routes | Future shared comments component | Add icon metadata in Stage 3. |
| `assets/images/icons/ai/comic-v2.png` | Workshop and AI comic config effects | `256x256` | PNG | AI comic mode icon | Workshop and AI comic routes | `WorkshopCard` | Add icon metadata in Stage 3. |
| `assets/images/icons/ai/video-v2.png` | Workshop and AI video config effects | `256x256` | PNG | AI video mode icon | Workshop and AI video routes | `WorkshopCard` | Add icon metadata in Stage 3. |
| `assets/images/icons/ai/status-spark-v2.png` | AI progress/status effects | `256x256` | PNG | AI status/magic icon | AI progress, AI history | `FairyTag` | Add icon metadata in Stage 3. |
| `assets/images/icons/more/profile-v2.png` | Mine and more-feature effects | `256x256` | PNG | Profile menu icon | `app/(tabs)/mine.js` | `FeaturePage` | Add icon metadata in Stage 3. |
| `assets/images/icons/more/membership-v2.png` | Mine and membership effects | `256x256` | PNG | Membership menu icon | Mine, `app/membership.js` | `FeaturePage`, `FairyTag` | Add icon metadata in Stage 3. |
| `assets/images/icons/more/settings-v2.png` | Mine and settings effects | `256x256` | PNG | Settings menu icon | Mine, `app/settings.js` | `FeaturePage` | Add icon metadata in Stage 3. |
| `assets/images/icons/more/help-v2.png` | Mine and help feedback effects | `256x256` | PNG | Help menu icon | Mine, `app/help-feedback.js` | `FeaturePage` | Add icon metadata in Stage 3. |
| `assets/images/icons/diary/mood-v2.png` | Diary editor/detail effects | `256x256` | PNG | Diary mood icon | Diary routes | `FairyTag` | Add icon metadata in Stage 3. |
| `assets/images/icons/diary/tag-v2.png` | Diary editor/detail effects | `256x256` | PNG | Diary tag icon | Diary and tag routes | `FairyTag` | Add icon metadata in Stage 3. |
| `assets/images/icons/diary/attachment-v2.png` | Diary editor/photo upload effects | `256x256` | PNG | Attachment icon | Diary editor, photo upload | `FairyInput`, future icon map | Add icon metadata in Stage 3. |
| `assets/images/icons/diary/draft-v2.png` | Diary/drafts effects | `256x256` | PNG | Draft icon | `app/drafts.js`, diary editor | `FairyCard` | Add icon metadata in Stage 3. |
| `assets/images/icons/diary/save-v2.png` | Diary editor effects | `256x256` | PNG | Save action icon | Diary editor and forms | `FairyButton` | Add icon metadata in Stage 3. |
| `assets/images/icons/tags/tag-swatch-v2.png` | Tag management effect | `256x256` | PNG | Tag swatch/category icon | `app/tags/index.js` | `FairyTag` | Add icon metadata in Stage 3. |
| `assets/images/icons/notifications/unread-v2.png` | Interaction notification effect | `256x256` | PNG | Unread notification icon | `app/notifications/index.js` | Future icon map | Add icon metadata in Stage 3. |
| `assets/images/icons/notifications/action-required-v2.png` | Interaction notification effect | `256x256` | PNG | Action-required notification icon | `app/notifications/index.js` | Future icon map | Add icon metadata in Stage 3. |
| `assets/images/icons/comments/comment-v2.png` | Comments list effect | `256x256` | PNG | Comment icon | `app/comments/index.js`, `app/interaction/comments.js` | Future shared comments component | Add icon metadata in Stage 3. |
| `assets/images/icons/comments/reaction-v2.png` | Comments list and activity detail effects | `256x256` | PNG | Reaction icon | Comments and couple detail routes | Future shared comments component | Add icon metadata in Stage 3. |
| `assets/images/icons/comments/reply-v2.png` | Comments list effect | `256x256` | PNG | Reply icon | Comments routes | Future shared comments component | Add icon metadata in Stage 3. |

### 8.4 Illustration and placeholder assets

| Asset path | Source | Size | Format | Usage | Impacted routes | Component | Follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `assets/images/illustrations/account-onboarding-v2.png` | Programmatic illustration derived from onboarding/account effects | `1200x900` | PNG | Onboarding hero illustration | `app/onboarding.js` | `FairyImage`, `FairyHeroImage` | Add image metadata in Stage 3. |
| `assets/images/illustrations/account-login-v2.png` | Programmatic illustration derived from login/account effects | `1200x900` | PNG | Login/auth illustration | `app/login.js` | `FairyImage`, `FairySticker` | Add image metadata in Stage 3. |
| `assets/images/illustrations/couple-avatar-placeholder-v2.png` | Programmatic placeholder derived from couple bind/profile effects | `1200x900` | PNG | Couple avatar/pairing placeholder | Account and couple routes | `FairyImage` | Add image metadata in Stage 3. |
| `assets/images/illustrations/album-upload-placeholder-v2.png` | Programmatic placeholder derived from photo upload/album effects | `1200x900` | PNG | Upload/photo placeholder | `app/photo/upload.js`, `app/photo/album.js` | `FairyImage`, `FairyEmptyState` | Add image metadata in Stage 3. |
| `assets/images/illustrations/generation-progress-v2.png` | Programmatic illustration derived from generation progress effect | `1200x900` | PNG | AI generation progress placeholder | `app/ai/progress.js`, `app/ai/generation-progress.js` | `FairyImage`, `FairyIllustration` | Add image metadata in Stage 3. |
| `assets/images/illustrations/comic-result-placeholder-v2.png` | Programmatic placeholder derived from AI flow/history effects | `1200x900` | PNG | Comic result preview placeholder | `app/ai/comic-result.js` | `FairyImage` | Add image metadata in Stage 3. |
| `assets/images/illustrations/character-profile-placeholder-v2.png` | Programmatic placeholder derived from workshop/comic config effects | `1200x900` | PNG | AI character profile placeholder | `app/ai/character-profile.js`, `app/ai/comic-config.js` | `FairyImage`, `FairyTag` | Add image metadata in Stage 3. |
| `assets/images/illustrations/video-preview-placeholder-v2.png` | Programmatic placeholder derived from video config/preview effects | `1200x900` | PNG | Video preview placeholder | `app/ai/video-preview.js`, `app/ai/video-config.js` | `FairyImage` | Add image metadata in Stage 3. |
| `assets/images/illustrations/empty-no-network-v2.png` | Programmatic empty-state illustration derived from empty-state effect | `1200x900` | PNG | No-network state | All networked pages | `FairyEmptyState` | Add image metadata in Stage 3. |
| `assets/images/illustrations/empty-permission-v2.png` | Programmatic empty-state illustration derived from empty-state effect | `1200x900` | PNG | Permission-denied state | Photo upload, export, account flows | `FairyEmptyState` | Add image metadata in Stage 3. |
| `assets/images/illustrations/empty-error-v2.png` | Programmatic empty-state illustration derived from empty-state effect | `1200x900` | PNG | Error state | All routes | `FairyEmptyState` | Add image metadata in Stage 3. |
| `assets/images/illustrations/empty-loading-v2.png` | Programmatic loading illustration derived from empty-state/progress effects | `1200x900` | PNG | Loading state | AI and data routes | `FairyEmptyState` | Add image metadata in Stage 3. |

### 8.5 Decorative sticker assets

| Asset path | Source | Size | Format | Usage | Impacted routes | Component | Follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `assets/images/stickers/branch-flower-v2.png` | Programmatic decorative sticker derived from Stage 0 style guide | `256x256` | PNG | Branch/flower decoration | Cards, headers, empty states | `FairySticker` | Add sticker metadata in Stage 3. |
| `assets/images/stickers/sparkle-sticker-v2.png` | Programmatic decorative sticker derived from Stage 0 style guide | `256x256` | PNG | Sparkle decoration | AI, empty states, card corners | `FairySticker` | Add sticker metadata in Stage 3. |
| `assets/images/stickers/crown-sticker-v2.png` | Programmatic decorative sticker derived from member/status effects | `256x256` | PNG | Membership/crown decoration | Mine, membership, tags | `FairySticker` | Add sticker metadata in Stage 3. |

## 9. 2026-06-11 Stage 2 correction record

> Correction: the 49 programmatically generated `*-v2.png` assets from the first Stage 2 pass are visually too simplified for the new effect target. They remain on disk for audit continuity, but their source status is changed to `deprecated-low-fi-generated`; do not connect them to routes, metadata, or shared components until replaced.

### 9.1 Corrected asset source labels

| Source label | Meaning | Stage 2 handling |
| --- | --- | --- |
| `code-vector` | Routine UI actions such as back, save, copy, settings, reply, search, filter, PDF, and storage. | Implement later with component/icon code or SVG/vector assets; no low-fidelity PNG generation. |
| `crop-from-effect` | Clear local sticker, paper, tape, texture, TabBar, or component-detail region cropped from `assets/page-effects` or `assets/design`. | Keep as high-fidelity reference or temporary reusable crop; transparent cleanup can happen later if needed. |
| `image2-regenerated` | High-fidelity transparent paper-texture stickers, soft illustrations, magic effects, avatars, and empty-state art that cannot be cleanly cropped. | Generate later from local crop references at `1024x1024` or higher, preserving paper grain, hand-drawn outline, sticker edge, and soft shadow. |
| `deprecated-low-fi-generated` | Existing first-pass Stage 2 batch PNGs that look like simplified icons/placeholders. | Retain only for audit; replace, crop, regenerate, or move to code-vector. |

### 9.2 Crop-from-effect reference assets

| Asset path | Source | Size | Format | Usage | Impacted routes | Component | Follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `assets/images/crops/stage-0/paper-texture-sample-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `863x1822` | PNG | Paper texture and grain reference | All routes | `FairyPage`, theme backgrounds | Use as crop reference; generate seamless/clean asset later if needed. |
| `assets/images/crops/stage-0/torn-paper-flower-corner-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `570x450` | PNG | Torn paper corner with floral decoration | Cards, headers, empty states | `FairyCard`, `FairySticker` | Clean background or regenerate transparent version before component use. |
| `assets/images/crops/stage-0/pink-ribbon-bookmark-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `360x660` | PNG | Ribbon/bookmark decoration reference | Headers, cards, account flows | `FairySticker` | Regenerate transparent paper sticker if used globally. |
| `assets/images/crops/stage-0/palette-heart-peach-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `420x420` | PNG | Peach-pink heart palette reference | Theme, stickers | Theme, `FairySticker` | Use for visual QA, not direct UI unless transparent cleanup is done. |
| `assets/images/crops/stage-0/palette-heart-rose-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `420x420` | PNG | Dry-rose heart palette reference | Theme, stickers | Theme, `FairySticker` | Use for visual QA, not direct UI unless transparent cleanup is done. |
| `assets/images/crops/stage-0/palette-heart-cocoa-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `420x420` | PNG | Cocoa-brown heart palette reference | Theme, stickers | Theme, `FairySticker` | Use for visual QA, not direct UI unless transparent cleanup is done. |
| `assets/images/crops/stage-0/palette-heart-gold-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `420x420` | PNG | Amber-gold heart palette reference | Theme, stickers | Theme, `FairySticker` | Use for visual QA, not direct UI unless transparent cleanup is done. |
| `assets/images/crops/stage-0/flower-sticker-corner-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `392x344` | PNG | Small floral corner sticker reference | Cards, headers | `FairySticker` | Crop is high-fidelity but has background; clean/regenerate before broad use. |
| `assets/images/crops/stage-0/component-heart-sticker-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `270x336` | PNG | Heart sticker on component sample | Buttons, cards, tags | `FairySticker` | Regenerate transparent sticker if used outside same background. |
| `assets/images/crops/stage-0/component-star-sticker-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `270x288` | PNG | Star sticker on component sample | Cards, AI states | `FairySticker` | Regenerate transparent sticker if used outside same background. |
| `assets/images/crops/stage-0/component-flower-card-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `275x375` | PNG | Floral card/corner reference | Cards, empty states | `FairySticker`, `FairyCard` | Use as image2 reference for transparent floral sticker. |
| `assets/images/crops/stage-0/primary-button-flower-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `290x275` | PNG | Button flower decoration reference | Buttons, forms | `FairyButton` | Prefer component/vector treatment plus optional sticker. |
| `assets/images/crops/stage-0/input-pen-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `304x368` | PNG | Pen/input visual reference | Login, diary, AI config, help | `FairyInput` | Implement pen as code-vector or cleaned transparent asset. |
| `assets/images/crops/stage-0/branch-flower-tape-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `420x690` | PNG | Branch, flower, tape sticker reference | Cards, headers, empty states | `FairySticker` | Best candidate for image2 transparent high-fidelity regeneration. |
| `assets/images/crops/stage-0/bottom-heart-sticker-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `280x300` | PNG | Bottom heart sticker reference | Tabs, cards, tags | `FairySticker` | Regenerate transparent sticker if reused. |
| `assets/images/crops/stage-0/tab-story-icon-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `360x280` | PNG | Story TabBar icon reference | `app/(tabs)/index.js` | `FairyTabBar` | Use as visual reference; final icon may be vector/code or transparent refined asset. |
| `assets/images/crops/stage-0/tab-mood-icon-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `350x280` | PNG | Mood TabBar icon reference | Mood/couple tab route | `FairyTabBar` | Use as visual reference; final icon may be vector/code or transparent refined asset. |
| `assets/images/crops/stage-0/tab-record-icon-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `390x360` | PNG | Record TabBar icon reference | Main tab layout | `FairyTabBar` | Use as visual reference; final icon may be vector/code or transparent refined asset. |
| `assets/images/crops/stage-0/tab-us-icon-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `390x340` | PNG | Us/couple TabBar icon reference | Couple/us tab route | `FairyTabBar` | Use as visual reference; final icon may be vector/code or transparent refined asset. |
| `assets/images/crops/stage-0/tab-mine-icon-crop.png` | `assets/page-effects/stage-0/00-visual-style-guide.png` | `350x310` | PNG | Mine TabBar icon reference | `app/(tabs)/mine.js` | `FairyTabBar` | Use as visual reference; final icon may be vector/code or transparent refined asset. |

### 9.3 Image2 regeneration constraints

Use crop references first. Only regenerate when direct cropping is not clean enough for transparent-background component reuse. Prompts must emphasize: reference effect screenshot, high-fidelity, cream paper grain, soft shadow, hand-drawn outline, sticker edge, transparent background, warm fairy-tale journal style, and 1024x1024 or higher output. Avoid wording such as `simple icon`, `flat icon`, `minimal icon`, or `basic vector icon`.

## 10. 2026-06-11 Stage 2 generated image deletion record

> User review conclusion: the Stage 2 generated images cannot be used directly in the project. All Stage 2 generated image files have been deleted from `assets/images`.

| Deleted group | Deleted files | Current asset status | Follow-up |
| --- | ---: | --- | --- |
| First-pass generated `*-v2.png` assets | 49 | Deleted; do not reference or wire. | Re-plan with code/SVG implementation or source-quality design assets before any new generation. |
| Stage 0 crop reference PNG assets | 20 | Deleted; do not reference or wire. | Re-crop only after confirming exact asset specs and final usage path. |

The records in sections 8 and 9 are now historical audit notes only. They are not an implementation asset manifest.
