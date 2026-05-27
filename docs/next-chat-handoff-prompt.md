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

## 3. 重要项目文档

新对话开始后，建议优先读取这些文档：

```text
docs/project-file-structure.md
docs/pending-interfaces-implementation-plan.md
docs/image-assets-guideline.md
docs/image-assets-implementation-plan.md
docs/visual-audit-and-next-steps.md
docs/《独家童话》Design System v1.0.md
docs/《独家童话》UI设计总方向.md
```

这些文档分别说明：

| 文件 | 作用 |
| --- | --- |
| `docs/project-file-structure.md` | 当前项目文件结构，每个页面/组件/状态文件的作用。 |
| `docs/pending-interfaces-implementation-plan.md` | 未开发/半落地界面计划，P0 已完成，P1 是下一批任务。 |
| `docs/image-assets-guideline.md` | 图片资产规范和图片处理记录模板。 |
| `docs/image-assets-implementation-plan.md` | 从效果图拆分/重新生成独立插画的实施计划。 |
| `docs/visual-audit-and-next-steps.md` | 当前视觉还原差异和后续建议。 |
| `docs/《独家童话》Design System v1.0.md` | 设计系统规范。 |
| `docs/《独家童话》UI设计总方向.md` | 整体 UI 气质、边界和方向。 |

---

## 4. 当前已经完成的主要内容

### 4.1 基础架构

已建立：

```text
app/                 Expo Router 页面路由
src/components/      童话绘本风格组件
src/theme/           颜色、间距、字体、阴影 token
src/store/           Zustand 全局状态
src/data/            mock 数据
src/api/             API mock / 后续真实接口封装目录
assets/design/       设计稿和效果图
assets/images/       项目图片资产目录规划
```

---

### 4.2 已完成的视觉基础组件

已完成并可复用：

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
src/components/MemoryWall.js
src/components/CoupleTimeline.js
```

说明：

- `FairyTabBar` 已替换默认底部 TabBar；
- `MemoryWall` 已用于首页“回忆碎片墙”；
- `CoupleTimeline` 已用于情侣空间“手绘时间轴”；
- `FairyImage` 是统一图片入口，当前可 fallback 到 `FairyIllustration`，后续接入真实 AI 插画；
- `FairyInput`、`FairyEmptyState`、`FairyDialog` 已形成基础视觉组件层。

---

### 4.3 已完成核心页面

当前主 Tab：

```text
app/(tabs)/index.js       首页 / 记录中心
app/(tabs)/couple.js      情侣空间
app/(tabs)/workshop.js    AI童话工坊
app/(tabs)/mine.js        我的
```

当前较完整业务页面：

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
```

---

## 5. 当前业务闭环

目前已经有这些 mock MVP 闭环：

```text
写日记
→ app/diary/editor.js
→ useFairyStore.addDiaryRecord
→ 首页 records 更新
→ 情侣空间 timeline 更新
→ 我的统计更新
```

```text
传照片
→ app/photo/upload.js
→ useFairyStore.addPhotoRecord
→ 首页 records 更新
→ 相册更新
→ 情侣空间 timeline 更新
```

```text
文本转漫画
→ app/ai/text-to-comic.js
→ useFairyStore.addCreation
→ AI进度页
→ 童话工坊创作历史
→ 情侣空间 timeline
```

```text
照片转漫画
→ app/ai/photo-to-comic.js
→ 选择照片组
→ useFairyStore.addCreation
→ AI进度页
→ 童话工坊创作历史
→ 情侣空间 timeline
```

```text
情侣空间
→ CoupleTimeline 手绘时间轴
→ app/couple/activity-detail.js 动态详情
→ app/comments/index.js 评论列表
```

```text
搜索
→ app/search.js
→ 搜索 records / creations / anniversaries / timeline
→ 跳转日记详情 / 相册 / 纪念日 / 动态详情 / 童话工坊
```

---

## 6. 刚刚完成的 P0 页面

已完成：

```text
照片转漫画页 → 搜索页 → 情侣动态详情页 → 评论列表页
```

对应文件：

```text
app/ai/photo-to-comic.js
app/search.js
app/couple/activity-detail.js
app/comments/index.js
```

状态记录在：

```text
docs/pending-interfaces-implementation-plan.md
```

当前 P0 已全部标记为已完成。

---

## 7. 当前正在做什么

当前项目已经进入：

```text
P1 半落地页面补齐阶段
```

下一批建议开发顺序是：

```text
互动通知页 → 标签管理页 → 时光胶囊设置页 → 导出预览页 → 存储空间管理页
```

对应文件：

```text
app/notifications/index.js
app/tags/index.js
app/time-capsule/settings.js
app/data/export-preview.js
app/data/storage.js
```

这些页面当前大概率仍是 `FeaturePage` 骨架/说明页，需要改成真实 mock 页面。

---

## 8. 接下来应该做什么

### 8.1 下一步开发任务：P1 页面补齐

建议按顺序处理：

#### 任务 1：互动通知页

文件：

```text
app/notifications/index.js
```

目标：

- 展示点赞、评论、AI生成完成、纪念日提醒等通知；
- 支持已读/未读状态；
- 支持按类型筛选；
- 点击通知跳转对应页面；
- 使用 `FairyPage`、`FairyHeader`、`FairyCard`、`FairyTag`、`FairyEmptyState`。

---

#### 任务 2：标签管理页

文件：

```text
app/tags/index.js
```

目标：

- 从 records 中统计 tags；
- 展示标签列表和使用次数；
- 支持新增 mock 标签；
- 支持选择/筛选标签；
- 后续可扩展重命名/合并/删除。

---

#### 任务 3：时光胶囊设置页

文件：

```text
app/time-capsule/settings.js
```

目标：

- 创建 mock 时光胶囊；
- 选择封存内容类型；
- 设置解锁日期；
- 展示胶囊列表；
- 空状态引导创建。

---

#### 任务 4：导出预览页

文件：

```text
app/data/export-preview.js
```

目标：

- 展示 PDF 预览封面；
- 展示章节目录：日记、照片、AI作品、纪念日；
- 展示导出范围和样式；
- 提供确认导出 mock 按钮；
- 后续连接 PDF 真实导出。

---

#### 任务 5：存储空间管理页

文件：

```text
app/data/storage.js
```

目标：

- 展示 mock 存储用量；
- 分类展示照片、AI作品、PDF导出、缓存；
- 支持清理缓存 mock 操作；
- 使用统一卡片、进度条、空状态。

---

## 9. 图片资产任务也已纳入计划

当前已建立图片资产规范：

```text
docs/image-assets-guideline.md
docs/image-assets-implementation-plan.md
assets/images/README.md
```

下一阶段还需要：

```text
从 assets/design/png/界面设计图.png、界面设计图2.png、界面设计风格图-2.png 中参考或拆分/重新生成三张核心插画：

assets/images/illustrations/home-cover-v1.png
assets/images/illustrations/couple-space-cover-v1.png
assets/images/illustrations/workshop-cover-v1.png

然后在 src/components/FairyImage.js 中打开真实图片映射。
```

当前不要直接把整张效果图放进页面。

---

## 10. 新对话可直接复制的提示词

下面这段可以直接复制到新的 ChatGPT / Codex 对话中：

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
- P0 页面：照片转漫画页、搜索页、情侣动态详情页、评论列表页。

当前要继续做的是 P1 半落地页面补齐，顺序为：

1. 互动通知页：app/notifications/index.js
2. 标签管理页：app/tags/index.js
3. 时光胶囊设置页：app/time-capsule/settings.js
4. 导出预览页：app/data/export-preview.js
5. 存储空间管理页：app/data/storage.js

开发要求：

- 页面优先使用 FairyPage 和 FairyHeader；
- 输入统一用 FairyInput；
- 空状态统一用 FairyEmptyState；
- 卡片统一用 FairyCard；
- 操作用 FairyButton；
- 标签用 FairyTag；
- 文案保持童话绘本、情侣记录、温柔魔法感；
- 不接真实后端；
- 不接真实 AI；
- 不新增复杂依赖；
- 所有页面先完成 mock MVP 交互闭环；
- 完成后更新 docs/project-file-structure.md 和 docs/pending-interfaces-implementation-plan.md。

请先检查这 5 个 P1 页面当前文件状态，然后从 app/notifications/index.js 开始开发，按顺序完成：互动通知页 → 标签管理页 → 时光胶囊设置页 → 导出预览页 → 存储空间管理页。
```

---

## 11. 新对话开始后的推荐操作

新对话中建议先执行：

```text
1. 读取 docs/next-chat-handoff-prompt.md
2. 读取 docs/project-file-structure.md
3. 读取 docs/pending-interfaces-implementation-plan.md
4. 检查 app/notifications/index.js、app/tags/index.js、app/time-capsule/settings.js、app/data/export-preview.js、app/data/storage.js
5. 从互动通知页开始开发
6. 每完成一页，更新计划文档状态
7. 最后更新项目文件结构文档
```

---

## 12. 注意事项

1. 不要重做已经完成的 P0 页面，除非发现明显错误。
2. 不要把 `assets/design/png/界面设计图*.png` 整图直接放入页面。
3. 不要破坏 `FairyImage` 的统一图片入口。
4. 不要绕过 `useFairyStore` 随意新增全局状态文件，除非确实需要。
5. 页面风格必须继续贴合设计规范。
6. 开发完成后要同步更新文档。
7. 如果遇到 GitHub 文件 SHA 冲突，先重新 fetch 当前文件，再基于最新 SHA update。
