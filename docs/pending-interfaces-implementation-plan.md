# 《独家童话》待补页面实现计划

> 文档说明：本文档用于记录《独家童话》待补界面、半落地页面、实现优先级、完成状态、mock MVP 交互闭环、实现约束和连续推进记录。

本文档记录当前原型中待补界面的实现优先级、完成状态和交互范围。页面先以 mock MVP 闭环为目标，不接真实后端、不接真实 AI、不新增复杂依赖。

---

## P1 半落地页面补齐

| 页面 | 路由文件 | 当前状态 | MVP 交互闭环 |
| --- | --- | --- | --- |
| 互动通知页 | `app/notifications/index.js` | 已完成 | 使用页面内 mock 通知数据生成列表，覆盖点赞/评论/AI完成/纪念日/系统提醒；支持已读状态、类型筛选（全部/互动/AI/纪念日/系统）；点击通知自动标记已读并跳转对应页面。 |
| 标签管理页 | `app/tags/index.js` | 已完成 | 从 `useFairyStore.records` 统计标签名称、使用次数和关联类型；支持新增 mock 标签；支持点击标签筛选相关记录；含空状态。 |
| 时光胶囊设置页 | `app/time-capsule/settings.js` | 已完成 | 支持创建 mock 胶囊；支持填写标题、内容说明、解锁日期；支持选择封存内容类型（日记/照片/AI作品/纪念日）；展示胶囊列表和空状态。 |
| 导出预览页 | `app/data/export-preview.js` | 已完成 | 展示回忆册封面卡片、章节目录、导出范围/样式/页数 mock 信息；支持确认导出并通过 `FairyToast` 提示任务已加入。 |
| 存储空间管理页 | `app/data/storage.js` | 已完成 | 展示 mock 总用量和分类占比（照片/AI作品/PDF导出/缓存）；支持缓存清理 mock；清理前 `FairyDialog` 二次确认，清理后更新状态并提示。 |

---

## 实现约束

- 页面优先使用 `FairyPage` 和 `FairyHeader`。
- 输入统一使用 `FairyInput`。
- 空状态统一使用 `FairyEmptyState`。
- 卡片统一使用 `FairyCard`。
- 操作按钮统一使用 `FairyButton`。
- 标签统一使用 `FairyTag`。
- 文案保持童话绘本、情侣记录、温柔魔法感。
- 当前阶段仅使用本地 mock 状态或已有 Zustand mock 数据。

---

## 后续建议

1. 将旧占位路由 `app/interaction/notifications.js`、`app/records/tags.js`、`app/records/time-capsule.js` 迁移或跳转到新的目标路由，避免后续入口分散。
2. 等 P1 页面验收后，可把标签、通知、时光胶囊抽入 `useFairyStore`，形成跨页面状态闭环。
3. 导出预览和存储管理后续接入真实 PDF 生成、文件大小统计和缓存清理能力时，优先沉淀到 `src/api/storageApi.js` 或独立数据服务层。

---

## 连续推进记录（2026-05-27）

1. 已完成：纪念日添加/编辑独立页 `app/anniversary/edit.js`（mock MVP）。
2. 已完成：纪念日专属记录模板页 `app/anniversary/template.js`（mock MVP）。
3. 已完成：AI 漫画结果详情页 `app/ai/comic-result.js`，并接入工坊历史点击分流。
4. 已完成：AI 人设管理页 `app/ai/character-profile.js`，并接入漫画配置页入口。
5. 已完成：分享预览页 `app/share-preview.js`（mock MVP）。
6. 已完成：会员权益说明页 `app/membership.js`（mock MVP）。
7. 已完成：`FairyImage` 真实资源渲染通道接入（无资源时保持插画 fallback）。
8. 已完成：`useFairyStore` 持久化接入（`persist + AsyncStorage`）。
9. 已完成：历史骨架路由重定向（`/interaction/notifications`、`/records/tags`、`/records/time-capsule`）。
10. 已完成：账号链路页面落地（登录、引导、邀请、绑定确认、情侣信息设置）。
11. 已完成：辅助页面落地（草稿箱、搜索、帮助反馈、照片转漫画、情侣动态详情、评论列表、纪念日倒计时）。

---

## 全量盘点结论（2026-05-27）

- 当前 `app/` 路由中，`FeaturePage` 骨架页数量：`0`。
- “未落地主页面/子页面”数量：`0`（以现有路由清单为准）。
- 仍需后续补充的内容集中在：真实后端、真实 AI、真实图片资源、部分 mock 页面的深度编辑能力。
