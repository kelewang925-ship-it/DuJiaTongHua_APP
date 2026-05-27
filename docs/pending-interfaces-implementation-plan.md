# 《独家童话》未开发 / 半落地界面实施计划

> 更新时间：2026-05-26  
> 任务类型：页面补齐 / 交互闭环 / mock MVP 完整化  
> 关联总计划：`docs/project-development-master-plan.md` Phase 2、Phase 3  
> 设计参考：`assets/design/png/界面设计图.png`、`assets/design/png/界面设计图2.png`、`assets/design/png/界面设计风格图-2.png`、`docs/《独家童话》Design System v1.0.md`、`docs/《独家童话》UI设计总方向.md`

---

## 1. 任务目标

将当前仍处于占位、骨架、半落地状态的界面逐步补齐为可演示的 mock MVP 页面。

本计划不接真实后端，不接真实 AI 服务，不做大规模 UI 重构，优先基于：

- `useFairyStore`
- `mockData`
- `FairyPage`
- `FairyHeader`
- `FairyCard`
- `FairyInput`
- `FairyButton`
- `FairyEmptyState`
- `FairyDialog`
- `FairyToast`
- `FairyImage`

完成页面可用性和视觉一致性。

---

## 2. 未开发 / 半落地界面总清单

### 2.1 P0：当前优先开发

| 优先级 | 页面 | 路由 | 当前状态 | 本阶段目标 |
| --- | --- | --- | --- | --- |
| P0-1 | 照片转漫画页 | `app/ai/photo-to-comic.js` | 已完成 | 接入照片记录选择、风格选择、生成任务、跳转进度页。 |
| P0-2 | 搜索页 | `app/search.js` | 已完成 | 接入记录、动态、纪念日、AI作品搜索，支持关键词和类型筛选。 |
| P0-3 | 情侣动态详情页 | `app/couple/activity-detail.js` | 已完成 | 读取最近动态，展示章节详情、关联内容、评论入口和互动入口。 |
| P0-4 | 评论列表页 | `app/comments/index.js` | 已完成 | 增加 mock 评论列表、输入框、发送评论、空状态。 |

---

### 2.2 P1：下一批补齐

| 页面 | 路由 | 当前状态 | 目标 |
| --- | --- | --- | --- |
| 互动通知页 | `app/notifications/index.js` | 骨架/说明页 | 展示点赞、评论、AI完成、纪念日提醒，支持已读状态。 |
| 标签管理页 | `app/tags/index.js` | 骨架/说明页 | 展示标签列表、使用次数、新增/编辑/删除标签。 |
| 时光胶囊设置页 | `app/time-capsule/settings.js` | 骨架/说明页 | 支持创建胶囊、选择解锁时间、封存记录。 |
| 导出预览页 | `app/data/export-preview.js` | 骨架/说明页 | 展示 PDF 封面、目录、章节预览和导出确认。 |
| 存储空间管理页 | `app/data/storage.js` | 骨架/说明页 | 展示存储用量、图片/视频/缓存分类和清理入口。 |

---

### 2.3 P2：后续扩展

| 页面 | 路由建议 | 当前状态 | 目标 |
| --- | --- | --- | --- |
| 纪念日添加/编辑独立页 | `app/anniversary/edit.js` | 未完整独立 | 从列表内嵌表单升级为独立编辑页。 |
| 纪念日专属记录模板页 | `app/anniversary/template.js` | 未完整落地 | 为纪念日生成专属日记/照片/AI模板。 |
| AI 漫画结果详情页 | `app/ai/comic-result.js` | 未完整落地 | 展示漫画分镜、重新生成、保存和分享。 |
| AI 人设管理页 | `app/ai/characters.js` | 未完整落地 | 管理情侣角色头像、发型、服装、常用表情。 |
| 分享预览页 | `app/share/preview.js` | 未确认完整 | 预览分享卡片，支持保存图片。 |
| 会员权益说明页 | `app/membership.js` | 未确认完整 | 展示会员权益、AI额度、导出能力。 |

---

## 3. 当前开发批次：P0 四页

本批次开发顺序：

```text
照片转漫画页 → 搜索页 → 情侣动态详情页 → 评论列表页
```

### 3.1 照片转漫画页

#### 状态

已完成。

#### 已实现

- 从 `records` 中筛选 `type === '照片'` 的记录；
- 展示可选照片组；
- 支持选择漫画风格；
- 支持输入作品名；
- 点击生成后调用 `addCreation`；
- 跳转 `app/ai/progress.js`；
- 无照片时展示 `FairyEmptyState` 并引导去上传照片。

---

### 3.2 搜索页

#### 状态

已完成。

#### 已实现

- 支持输入关键词；
- 支持筛选类型：全部、日记、照片、AI、纪念日、动态；
- 搜索范围包括：`records`、`creations`、`anniversaries`、`timeline`；
- 展示结果卡片；
- 结果为空时展示统一空状态；
- 点击不同结果跳转对应页面。

---

### 3.3 情侣动态详情页

#### 状态

已完成。

#### 已实现

- 从 `timeline[0]` 读取最近一条动态作为默认详情；
- 展示标题、时间、描述、标签；
- 展示关联记录和 AI 作品卡；
- 提供收藏、评论、生成漫画操作入口；
- 评论入口跳转 `app/comments/index.js`；
- 保持手绘故事章节视觉。

---

### 3.4 评论列表页

#### 状态

已完成。

#### 已实现

- 使用本地 mock 评论初始数据；
- 支持输入评论；
- 点击发送后追加评论；
- 支持空状态；
- 展示评论者、时间、内容；
- 保持贴纸卡片和温柔留言风格。

---

## 4. 统一开发要求

1. 页面优先使用 `FairyPage` 和 `FairyHeader`。
2. 输入统一使用 `FairyInput`。
3. 空状态统一使用 `FairyEmptyState`。
4. 主要操作使用 `FairyButton`。
5. 卡片使用 `FairyCard`。
6. 页面文案必须符合“童话绘本 / 情侣记录 / 温柔魔法”气质。
7. 不直接接真实后端。
8. 不直接调用真实 AI。
9. 不新增复杂依赖。
10. 完成后更新 `docs/project-file-structure.md`。

---

## 5. 后续维护

每完成一个页面，需要在本文件中更新：

```text
当前状态：未开始 → 开发中 → 已完成 → 已验收
```

并在 `docs/project-file-structure.md` 中更新页面职责。

---

## 6. 当前状态

```text
P0-1 照片转漫画页：已完成
P0-2 搜索页：已完成
P0-3 情侣动态详情页：已完成
P0-4 评论列表页：已完成

下一批建议进入 P1：互动通知页 → 标签管理页 → 时光胶囊设置页 → 导出预览页 → 存储空间管理页
```
