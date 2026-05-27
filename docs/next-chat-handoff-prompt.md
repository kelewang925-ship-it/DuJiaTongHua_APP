# 《独家童话》新对话接手提示词与任务说明

> 用途：当打开新的 ChatGPT / Codex 对话时，先把本文档内容交给新对话，让它快速理解项目、当前状态、正在做什么、下一步该做什么。  
> 项目仓库：`kelewang925-ship-it/DuJiaTongHua_APP`  
> 项目名称：《独家童话》  
> 技术栈：React Native + Expo + Expo Router + Zustand + JavaScript

---

## 1. 项目简介

《独家童话》是一款面向情侣的移动端情感记录 APP 原型。

核心目标：

- 记录情侣日常；
- 沉淀照片、日记、纪念日；
- 构建情侣专属时间线；
- 通过轻量 AI 能力，把日记和照片转化为漫画或纪念视频；
- 最终形成一本“会持续生长的恋爱童话绘本”。

当前产品定位不是普通粉色社交 APP，也不是科技感 AI 工具，而是：

```text
一本会呼吸的恋爱故事书。
```

---

## 2. 视觉方向

当前视觉方向是“童话绘本”：

- 奶油纸感；
- 桃粉；
- 干玫瑰；
- 可可棕；
- 琥珀金点缀；
- 手绘图标；
- 贴纸式组件；
- 胶带、拍立得、纸页、花朵、星星、爱心等轻装饰；
- 不堆大图，优先通过轻量图标、插画、卡片、贴纸建立品牌识别。

视觉参考文件：

```text
assets/design/png/界面设计图.png
assets/design/png/界面设计图2.png
assets/design/png/界面设计风格图-2.png
```

设计规范文件：

```text
docs/《独家童话》Design System v1.0.md
docs/《独家童话》UI设计总方向.md
docs/visual-audit-and-next-steps.md
```

---

## 3. 新对话优先读取文档

新对话开始后，请优先读取：

```text
docs/project-file-structure.md
docs/pending-interfaces-implementation-plan.md
docs/image-assets-guideline.md
docs/image-assets-implementation-plan.md
docs/visual-audit-and-next-steps.md
docs/《独家童话》Design System v1.0.md
docs/《独家童话》UI设计总方向.md
docs/next-chat-handoff-prompt.md
```

---

## 4. 当前已完成的基础能力

### 4.1 组件层

当前已经有：

```text
src/components/FairyPage.js
src/components/FairyHeader.js
src/components/FairyCard.js
src/components/FairyButton.js
src/components/FairyTag.js
src/components/FairyInput.js
src/components/FairyEmptyState.js
src/components/FairyDialog.js
src/components/FairyToast.js
src/components/FairyTabBar.js
src/components/FairyImage.js
src/components/FairyIllustration.js
src/components/MemoryWall.js
src/components/CoupleTimeline.js
src/components/WorkshopCard.js
src/components/MemoryCard.js
```

### 4.2 状态层

当前主要状态集中在：

```text
src/store/useFairyStore.js
```

当前 mock 状态闭环包括：

- `records`：日记 / 照片 / AI记录；
- `timeline`：情侣空间动态；
- `creations`：AI创作历史；
- `anniversaries`：纪念日；
- `draftDiary`：日记草稿；
- `addDiaryRecord`；
- `addPhotoRecord`；
- `addAnniversary`；
- `addCreation`；
- `getStats`。

---

## 5. 当前已落地的主要页面

主 Tab：

```text
app/(tabs)/index.js       首页 / 记录中心
app/(tabs)/couple.js      情侣空间
app/(tabs)/workshop.js    AI童话工坊
app/(tabs)/mine.js        我的
```

业务页面：

```text
app/diary/editor.js
app/diary/detail.js
app/photo/upload.js
app/photo/album.js
app/ai/comic-config.js
app/ai/video-config.js
app/ai/text-to-comic.js
app/ai/photo-to-comic.js
app/ai/progress.js
app/ai/video-preview.js
app/anniversary/index.js
app/data/backup.js
app/data/pdf-export.js
app/search.js
app/couple/activity-detail.js
app/comments/index.js
app/notifications/index.js
app/tags/index.js
app/time-capsule/settings.js
app/data/export-preview.js
app/data/storage.js
```

---

## 6. 当前业务闭环

```text
写日记 → addDiaryRecord → 首页 records → 情侣空间 timeline → 我的统计
```

```text
传照片 → addPhotoRecord → 首页 records → 相册 → 情侣空间 timeline
```

```text
文本转漫画 / 照片转漫画 → addCreation → AI进度页 → 童话工坊创作历史 → 情侣空间 timeline
```

```text
情侣空间 → CoupleTimeline → 动态详情 → 评论列表
```

```text
搜索页 → 搜索 records / creations / anniversaries / timeline → 跳转对应页面
```

P1 页面也已由 Codex 完成：

```text
互动通知页 → 标签管理页 → 时光胶囊设置页 → 导出预览页 → 存储空间管理页
```

---

## 7. 当前未完成 / 后续重点

### 7.1 图片资产真实替换

当前 `FairyImage` 已作为统一入口，但真实 PNG/WebP 图片资源首批替换还没有完成。

计划文件：

```text
docs/image-assets-implementation-plan.md
```

目标资源：

```text
assets/images/illustrations/home-cover-v1.png
assets/images/illustrations/couple-space-cover-v1.png
assets/images/illustrations/workshop-cover-v1.png
```

完成后需要在：

```text
src/components/FairyImage.js
```

打开真实图片映射。

### 7.2 下一批功能建议

可继续补齐：

```text
app/anniversary/edit.js              纪念日添加/编辑独立页
app/anniversary/template.js          纪念日专属记录模板页
app/ai/comic-result.js               AI漫画结果详情页
app/ai/characters.js                 AI人设管理页
app/share/preview.js                 分享预览页
app/membership.js                    会员权益说明页
```

### 7.3 工程化建议

- 接入 Zustand persist / AsyncStorage；
- 接入真实图片资产；
- 接入系统相册 ImagePicker；
- 接入 PDF 真实导出；
- 抽象真实 API client；
- 给核心页面补基础测试清单。

---

## 8. 新对话可直接复制的提示词

```text
请接手当前仓库项目：kelewang925-ship-it/DuJiaTongHua_APP。

项目名称是《独家童话》，这是一款面向情侣的 React Native + Expo + Expo Router + Zustand 移动端情感记录 APP 原型。视觉方向是童话绘本、奶油纸感、桃粉、干玫瑰、可可棕、琥珀金、手绘图标和贴纸式组件。项目不是普通粉色社交 App，也不是科技 AI 工具，而是“一本会呼吸的恋爱故事书”。

请先读取并理解这些文档：

1. docs/project-file-structure.md
2. docs/pending-interfaces-implementation-plan.md
3. docs/image-assets-guideline.md
4. docs/image-assets-implementation-plan.md
5. docs/visual-audit-and-next-steps.md
6. docs/《独家童话》Design System v1.0.md
7. docs/《独家童话》UI设计总方向.md
8. docs/next-chat-handoff-prompt.md

当前已经完成：

- Design System 基础组件层；
- 自定义 FairyTabBar；
- 首页 MemoryWall 回忆碎片墙；
- 情侣空间 CoupleTimeline 手绘时间轴；
- FairyImage 图片统一入口；
- 日记、照片、纪念日、AI创作的 Zustand mock 数据闭环；
- P0 页面：照片转漫画页、搜索页、情侣动态详情页、评论列表页；
- P1 页面：互动通知页、标签管理页、时光胶囊设置页、导出预览页、存储空间管理页。

当前还没有完成真实图片资源首批替换。后续视觉验收要参考 assets/design/png 中的效果图，但本阶段只能做功能和使用程度验收，不能要求真实图片完全还原。

请先检查当前页面运行状态和文档状态，再根据 docs/pending-interfaces-implementation-plan.md 和 docs/image-assets-implementation-plan.md 继续安排下一步。
```

---

## 9. 注意事项

1. 不要把 `assets/design/png/界面设计图*.png` 整图直接塞进页面。
2. 不要破坏 `FairyImage` 的统一图片入口。
3. 不要重做已经完成的页面，除非发现明显错误。
4. 新增页面后必须更新文档。
5. 若 GitHub 文件 SHA 冲突，先重新 fetch 当前文件，再基于最新 SHA update。
