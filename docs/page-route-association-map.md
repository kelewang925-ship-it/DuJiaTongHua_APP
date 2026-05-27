# 《独家童话》页面关联矩阵

更新时间：2026-05-27

本文档用于说明“从哪里进入某个页面”，帮助验收和后续迭代时快速检查是否存在孤立页面。

---

## 1. 全局入口

- `/onboarding` -> `/login` -> `/account/invite` -> `/account/bind-confirm` -> `/account/couple-info` -> `/(tabs)`
- `/(tabs)/mine` 作为管理中枢，集中承载大多数二级页面入口。
- `/settings` 作为辅助中枢，承载通知、存储、帮助等入口。

---

## 2. 主要业务关联

1. 记录链路  
`/(tabs)` -> `/diary/editor` -> `/diary/detail` -> `/ai/text-to-comic`  
`/(tabs)` -> `/photo/upload` -> `/photo/album` -> `/ai/photo-to-comic`

2. 情侣互动链路  
`/(tabs)/couple` -> `/couple/activity-detail`(兼容入口) -> `/couple/story-detail` -> `/comments` -> `/interaction/comments`

3. 通知链路  
`/notifications`  
点赞/评论 -> `/couple/activity-detail` 或 `/comments`  
AI 完成 -> `/(tabs)/workshop`  
纪念日 -> `/anniversary`  
历史入口 `/interaction/notifications` -> 自动重定向 `/notifications`

4. AI 创作链路  
`/(tabs)/workshop` -> `/ai/comic-config` -> `/ai/progress` -> `/ai/comic-result`  
`/(tabs)/workshop` -> `/ai/video-config` -> `/ai/progress` -> `/ai/video-preview`  
`/ai/comic-config` -> `/ai/character-profile`

5. 纪念日链路  
`/anniversary` -> `/anniversary/edit` -> `/anniversary/template`  
`/anniversary` -> `/anniversary/countdown`

6. 数据管理链路  
`/(tabs)/mine` 或 `/settings` -> `/data/pdf-export` -> `/data/export-preview`  
`/(tabs)/mine` 或 `/settings` -> `/data/backup`  
`/(tabs)/mine` 或 `/settings` -> `/data/storage`

7. 其他辅助链路  
`/(tabs)/mine` -> `/drafts`  
`/(tabs)/mine` -> `/search`  
`/(tabs)/mine` 或 `/settings` -> `/help-feedback`  
`/(tabs)/mine` -> `/share-preview`  
`/(tabs)/mine` -> `/membership`

---

## 3. 历史兼容入口（重定向）

- `/records/tags` -> `/tags`
- `/records/time-capsule` -> `/time-capsule/settings`
- `/interaction/notifications` -> `/notifications`

---

## 4. 验收建议

- 每次新增页面时，至少补充一个“主入口”与一个“回流入口”（返回上级功能页）。
- 每次调整路由命名时，若旧路径被外部引用，先加兼容重定向再移除旧入口。
