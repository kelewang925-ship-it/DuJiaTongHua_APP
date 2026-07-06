# 《独家童话》页面设计图与路由索引

更新时间：2026-06-12

本文档根据 `assets/design/` 下当前所有 PNG 效果图，以及 `app/` 目录中的 Expo Router 页面文件整理。用途是快速确认项目中包含哪些页面、页面对应的设计图、实现文件地址和访问路由。

## 路由规则

本项目使用 Expo Router，页面路由由 `app/` 目录文件自动生成：

| 规则 | 示例 |
| --- | --- |
| `app/(tabs)/index.js` 对应首页根路由 | `/` |
| `app/(tabs)/couple.js` 对应 Tab 路由 | `/(tabs)/couple` |
| `app/login.js` 对应普通页面路由 | `/login` |
| `app/account/invite.js` 对应嵌套路由 | `/account/invite` |
| `app/xxx/index.js` 对应该目录根路由 | `/xxx` |
| `app/_layout.js`、`app/(tabs)/_layout.js` 是布局文件 | 不作为独立页面路由 |

## 设计图对应页面

| 模块 | 效果图 | 页面 | 页面文件地址 | 路由 | 备注 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| 账号与关联 | `assets/design/引导页.png` | 引导页 | `app/onboarding.js` | `/onboarding` | 启动引导入口 | 完成 |
| 账号与关联 | `assets/design/登录页.png` | 登录页 | `app/login.js` | `/login` | 登录/授权入口 | 完成 |
| 账号与关联 | `assets/design/情侣邀请页.png` | 情侣邀请页 | `app/account/invite.js` | `/account/invite` | 生成或输入邀请码 | 完成 |
| 账号与关联 | `assets/design/情侣绑定确认页.png` | 情侣绑定确认页 | `app/account/bind-confirm.js` | `/account/bind-confirm` | 确认绑定对象 | 完成 |
| 账号与关联 | `assets/design/情侣信息设置页.png` | 情侣信息设置页 | `app/account/couple-info.js` | `/account/couple-info` | 当前绑定流程中的主要设置页 | 完成 |
| 账号与关联 | `assets/design/情侣信息设置页.png` | 情侣信息设置页 | `app/account/couple-settings.js` | `/account/couple-settings` | FeaturePage 版本，属于同一设计方向的补充页 |  |
| 首页与记录中心 | `assets/design/02-首页-记录中心.png` | 首页 / 记录中心 | `app/(tabs)/index.js` | `/` | 首页 Tab |  |
| 首页与记录中心 | `assets/design/日记编辑器.png` | 日记编辑器 | `app/diary/editor.js` | `/diary/editor` | 新建/编辑日记 |  |
| 首页与记录中心 | `assets/design/日记详情页.png` | 日记详情页 | `app/diary/detail.js` | `/diary/detail` | 查看日记详情 |  |
| 首页与记录中心 | `assets/design/照片上传页.png` | 照片上传页 | `app/photo/upload.js` | `/photo/upload` | 上传照片记录 |  |
| 首页与记录中心 | `assets/design/相册浏览页.png` | 照片相册页 | `app/photo/album.js` | `/photo/album` | 当前主要相册浏览页 |  |
| 首页与记录中心 | `assets/design/相册浏览页.png` | 回忆相册页 | `app/album/index.js` | `/album` | 另一版相册入口 |  |
| 首页与记录中心 | `assets/design/时光胶囊设置页.png` | 时光胶囊设置页 | `app/time-capsule/settings.js` | `/time-capsule/settings` | 时光胶囊配置 |  |
| 首页与记录中心 | `assets/design/标签管理页.png` | 标签管理页 | `app/tags/index.js` | `/tags` | 标签维护 |  |
| 情侣空间与互动 | `assets/design/03-情侣空间.png` | 情侣空间 | `app/(tabs)/couple.js` | `/(tabs)/couple` | 情侣空间 Tab |  |
| 情侣空间与互动 | `assets/design/情侣动态详情页.png` | 情侣动态详情页 | `app/couple/activity-detail.js` | `/couple/activity-detail` | 动态/故事章节详情 |  |
| 情侣空间与互动 | `assets/design/评论列表页.png` | 评论列表页 | `app/comments/index.js` | `/comments` | 当前主要评论页 |  |
| 情侣空间与互动 | `assets/design/评论列表页.png` | 评论列表页 | `app/interaction/comments.js` | `/interaction/comments` | 互动模块下的另一版评论页 |  |
| 情侣空间与互动 | `assets/design/互动通知页.png` | 互动通知页 | `app/notifications/index.js` | `/notifications` | 当前主要通知页 |  |
| 情侣空间与互动 | `assets/design/互动通知页.png` | 互动通知兼容入口 | `app/interaction/notifications.js` | `/interaction/notifications` | 自动重定向到 `/notifications` |  |
| AI 童话工坊 | `assets/design/04-AI童话工坊.png` | 童话工坊 | `app/(tabs)/workshop.js` | `/(tabs)/workshop` | AI 创作 Tab |  |
| AI 童话工坊 | `assets/design/AI漫画生成配置页.png` | AI 漫画生成配置页 | `app/ai/comic-config.js` | `/ai/comic-config` | 漫画生成配置 |  |
| AI 童话工坊 | `assets/design/文本转漫画页.png` | 文本转漫画页 | `app/ai/text-to-comic.js` | `/ai/text-to-comic` | 文本生成漫画 |  |
| AI 童话工坊 | `assets/design/照片转漫画页.png` | 照片转漫画页 | `app/ai/photo-to-comic.js` | `/ai/photo-to-comic` | 照片生成漫画 |  |
| AI 童话工坊 | `assets/design/AI短视频配置页.png` | AI 短视频配置页 | `app/ai/video-config.js` | `/ai/video-config` | 视频生成配置 |  |
| AI 童话工坊 | `assets/design/视频预览编辑页.png` | 视频预览编辑页 | `app/ai/video-preview.js` | `/ai/video-preview` | 视频结果预览和编辑 |  |
| AI 童话工坊 | `assets/design/生成进度页.png` | 生成进度页 | `app/ai/progress.js` | `/ai/progress` | 当前主要 AI 生成进度页 |  |
| AI 童话工坊 | `assets/design/生成进度页.png` | 生成进度兼容页 | `app/ai/generation-progress.js` | `/ai/generation-progress` | 另一版生成进度入口 |  |
| AI 童话工坊 | `assets/design/创作历史展示页.png` | 创作历史展示页 | `app/ai/history.js` | `/ai/history` | AI 历史作品 |  |
| 纪念日管理 | `assets/design/06-纪念日管理.png` | 纪念日管理页 | `app/anniversary/index.js` | `/anniversary` | 纪念日列表和入口 |  |
| 纪念日管理 | `assets/design/纪念日添加编辑页.png` | 纪念日添加编辑页 | `app/anniversary/edit.js` | `/anniversary/edit` | 新增/编辑纪念日 |  |
| 纪念日管理 | `assets/design/纪念日倒计时页.png` | 纪念日倒计时页 | `app/anniversary/countdown.js` | `/anniversary/countdown` | 倒计时展示 |  |
| 纪念日管理 | `assets/design/纪念日专属记录模板页.png` | 纪念日专属记录模板页 | `app/anniversary/template.js` | `/anniversary/template` | 选择纪念日记录模板 |  |
| 数据与导出 | `assets/design/PDF导出配置页.png` | PDF 导出配置页 | `app/data/pdf-export.js` | `/data/pdf-export` | 导出范围和样式配置 |  |
| 数据与导出 | `assets/design/导出预览页.png` | 导出预览页 | `app/data/export-preview.js` | `/data/export-preview` | 导出前预览 |  |
| 数据与导出 | `assets/design/数据备份恢复页.png` | 数据备份恢复页 | `app/data/backup.js` | `/data/backup` | 备份/恢复入口 |  |
| 数据与导出 | `assets/design/存储空间管理页.png` | 存储空间管理页 | `app/data/storage.js` | `/data/storage` | 存储占用管理 |  |
| 更多功能 | `assets/design/搜索页.png` | 搜索页 | `app/search.js` | `/search` | 全局搜索 |  |
| 更多功能 | `assets/design/草稿箱.png` | 草稿箱 | `app/drafts.js` | `/drafts` | 草稿管理 |  |
| 更多功能 | `assets/design/分享预览页.png` | 分享预览页 | `app/share-preview.js` | `/share-preview` | 分享卡片预览 |  |
| 更多功能 | `assets/design/会员权益说明页.png` | 会员权益说明页 | `app/membership.js` | `/membership` | 会员权益展示 |  |
| 更多功能 | `assets/design/帮助与反馈页.png` | 帮助与反馈页 | `app/help-feedback.js` | `/help-feedback` | 帮助和反馈入口 |  |
| 更多功能 | `assets/design/设置页.png` | 设置页 | `app/settings.js` | `/settings` | 系统设置 |  |
| 更多功能 | `assets/design/空状态页.png` | 空状态页 | `app/empty-state.js` | `/empty-state` | 空状态示例/演示页 |  |

## 总览类与风格参考图

以下 PNG 是模块总览图或视觉风格参考图，不直接对应单个独立路由，但会影响对应模块页面实现。

| 效果图 | 对应范围 | 主要关联文件/路由 |
| --- | --- | --- |
| `assets/design/01-账号与关联.png` | 账号、登录、情侣绑定流程总览 | `/onboarding`、`/login`、`/account/invite`、`/account/bind-confirm`、`/account/couple-info` |
| `assets/design/02-首页-记录中心.png` | 首页与记录中心总览 | `/`、`/diary/editor`、`/diary/detail`、`/photo/upload`、`/photo/album`、`/tags` |
| `assets/design/03-情侣空间.png` | 情侣空间总览 | `/(tabs)/couple`、`/couple/activity-detail`、`/comments`、`/notifications` |
| `assets/design/04-AI童话工坊.png` | AI 工坊总览 | `/(tabs)/workshop`、`/ai/comic-config`、`/ai/text-to-comic`、`/ai/photo-to-comic`、`/ai/video-config` |
| `assets/design/05-AI创作流程.png` | AI 创作流程总览 | `/ai/progress`、`/ai/comic-result`、`/ai/video-preview`、`/ai/history` |
| `assets/design/06-纪念日管理.png` | 纪念日模块总览 | `/anniversary`、`/anniversary/edit`、`/anniversary/countdown`、`/anniversary/template` |
| `assets/design/07-数据与导出.png` | 数据与导出模块总览 | `/data/pdf-export`、`/data/export-preview`、`/data/backup`、`/data/storage` |
| `assets/design/08-更多功能.png` | 更多功能模块总览 | `/(tabs)/mine`、`/search`、`/drafts`、`/share-preview`、`/membership`、`/help-feedback`、`/settings` |
| `assets/design/png/界面设计图.png` | 全局视觉参考 | 全项目页面 |
| `assets/design/png/界面设计图2.png` | 全局视觉参考 | 全项目页面 |
| `assets/design/png/界面设计风格图-2.png` | 全局视觉风格参考 | 全项目页面 |

## 当前存在但没有独立设计 PNG 的页面

这些页面在 `app/` 中已有实现，但 `assets/design/` 下没有同名的单页 PNG 效果图，通常复用模块总览图或相关页面设计方向。

| 页面 | 页面文件地址 | 路由 | 说明 |
| --- | --- | --- | --- |
| 我的 | `app/(tabs)/mine.js` | `/(tabs)/mine` | 更多功能和个人中心入口，主要参考 `08-更多功能.png` |
| AI 人设管理 | `app/ai/character-profile.js` | `/ai/character-profile` | 从漫画配置页进入，用于角色资料设置 |
| AI 漫画结果页 | `app/ai/comic-result.js` | `/ai/comic-result` | AI 生成完成后的漫画结果展示 |
| 情侣故事详情页 | `app/couple/story-detail.js` | `/couple/story-detail` | 情侣动态详情的故事版详情页 |

## 兼容入口与重定向路由

| 兼容入口文件 | 兼容路由 | 当前跳转目标 | 说明 |
| --- | --- | --- | --- |
| `app/records/tags.js` | `/records/tags` | `/tags` | 旧标签管理入口 |
| `app/records/time-capsule.js` | `/records/time-capsule` | `/time-capsule/settings` | 旧时光胶囊入口 |
| `app/interaction/notifications.js` | `/interaction/notifications` | `/notifications` | 旧互动通知入口 |

## 布局文件

| 文件地址 | 作用 | 路由 |
| --- | --- | --- |
| `app/_layout.js` | 全局 Stack 布局、状态栏、AuthGate | 不生成独立页面 |
| `app/(tabs)/_layout.js` | 四个底部 Tab：首页、情侣空间、童话工坊、我的 | 不生成独立页面 |
