# 《独家童话》当前界面与子界面清单

> 文档说明：本文档用于记录《独家童话》当前已经存在的路由页面、子界面、页面状态，以及设计稿中已规划但仍待进一步落地的界面清单，是页面覆盖度检查和后续补页面任务的依据。
> 更新时间：2026-05-26  
> 依据：当前 `app/` 路由目录与 `docs/project-file-structure.md`。

---

## 1. 全局与导航

| 界面 | 路由/文件 | 说明 |
| --- | --- | --- |
| 全局布局 | `app/_layout.js` | Expo Router 根布局，隐藏默认 Header，接入 `AuthGate` 登录态检查。 |
| Tab 布局 | `app/(tabs)/_layout.js` | 四个主 Tab：首页、情侣空间、童话工坊、我的。 |

---

## 2. 账号与情侣关联

| 界面 | 路由/文件 | 当前状态 |
| --- | --- | --- |
| 登录/授权页 | `/login` / `app/login.js` | 已接入邮箱登录、注册、邮箱登录链接、mock/real 模式。 |
| 情侣邀请页 | `/account/invite` / `app/account/invite.js` | 用于生成或展示邀请码/绑定入口。 |
| 情侣绑定确认页 | `/account/bind-confirm` / `app/account/bind-confirm.js` | 用于确认对方身份并完成绑定。 |

---

## 3. 四个主 Tab

| 主界面 | 路由/文件 | 当前状态 |
| --- | --- | --- |
| 首页 / 记录中心 | `/` / `app/(tabs)/index.js` | 展示恋爱天数、快捷入口、最近记录、回忆碎片墙。 |
| 情侣空间 | `/(tabs)/couple` / `app/(tabs)/couple.js` | 展示情侣资料、统计、纪念日预览、双人故事线。 |
| 童话工坊 | `/(tabs)/workshop` / `app/(tabs)/workshop.js` | 展示 AI 漫画、AI 视频、文本转漫画入口和创作历史。 |
| 我的 | `/(tabs)/mine` / `app/(tabs)/mine.js` | 展示资料、统计、管理入口；已新增退出登录。 |

---

## 4. 日记与记录

| 子界面 | 路由/文件 | 当前状态 |
| --- | --- | --- |
| 日记编辑器 | `/diary/editor` / `app/diary/editor.js` | 支持标题、正文、心情、标签，保存到 mock store。 |
| 日记详情页 | `/diary/detail` / `app/diary/detail.js` | 展示最近日记，提供文本转漫画入口。 |

---

## 5. 照片与相册

| 子界面 | 路由/文件 | 当前状态 |
| --- | --- | --- |
| 照片上传页 | `/photo/upload` / `app/photo/upload.js` | 当前为模拟上传，支持标题、备注、标签和数量。 |
| 照片相册页 | `/photo/album` / `app/photo/album.js` | 读取照片记录，支持网格/时间线展示。 |
| 相册首页 | `/album` / `app/album/index.js` | 相册浏览入口，用于后续完整相册体验。 |

---

## 6. AI 童话工坊

| 子界面 | 路由/文件 | 当前状态 |
| --- | --- | --- |
| AI 漫画配置页 | `/ai/comic-config` / `app/ai/comic-config.js` | 创建 mock 漫画任务并进入进度页。 |
| AI 视频配置页 | `/ai/video-config` / `app/ai/video-config.js` | 创建 mock 视频任务并进入进度页。 |
| 文本转漫画页 | `/ai/text-to-comic` / `app/ai/text-to-comic.js` | 支持从最近日记或自由文本创建 mock 漫画任务。 |
| AI 生成进度页 | `/ai/progress` / `app/ai/progress.js` | 展示 active AI job 的生成状态、步骤和结果预览。 |
| 生成进度兼容页 | `/ai/generation-progress` / `app/ai/generation-progress.js` | 可能用于兼容另一版生成流程。 |
| 视频预览编辑页 | `/ai/video-preview` / `app/ai/video-preview.js` | 用于后续视频结果预览、字幕、封面编辑。 |

---

## 7. 纪念日

| 子界面 | 路由/文件 | 当前状态 |
| --- | --- | --- |
| 纪念日管理页 | `/anniversary` / `app/anniversary/index.js` | 展示纪念日列表，支持新增 mock 纪念日。 |
| 纪念日倒计时页 | `/anniversary/countdown` / `app/anniversary/countdown.js` | 用于展示重要日期倒计时/已过去天数。 |

---

## 8. 数据、导出与管理

| 子界面 | 路由/文件 | 当前状态 |
| --- | --- | --- |
| 数据备份页 | `/data/backup` / `app/data/backup.js` | 展示数据统计与备份/恢复入口。 |
| PDF 导出页 | `/data/pdf-export` / `app/data/pdf-export.js` | 展示导出范围、绘本样式和导出入口。 |

---

## 9. 更多功能

| 子界面 | 路由/文件 | 当前状态 |
| --- | --- | --- |
| 设置页 | `/settings` / `app/settings.js` | 使用 `FairyPage` + `FairyHeader`，展示通知、隐私、主题、缓存入口。 |
| 草稿箱 | `/drafts` / `app/drafts.js` | 用于承载未完成日记、照片说明、AI 草稿。 |
| 帮助与反馈 | `/help-feedback` / `app/help-feedback.js` | 展示常见问题、反馈入口和支持信息。 |

---

## 10. 设计稿中已规划但代码中待进一步落地的界面

以下界面在 `assets/design/` 中已有设计方向，部分还未形成独立路由或完整业务实现：

- 引导页
- 情侣信息设置页
- 时光胶囊设置页
- 标签管理页
- 情侣动态详情页
- 评论列表页
- 互动通知页
- 照片转漫画页
- 创作历史展示页
- 纪念日添加编辑页
- 纪念日专属记录模板页
- 导出预览页
- 存储空间管理页
- 搜索页
- 分享预览页
- 会员权益说明页
- 空状态页

---

## 11. 当前界面数量概览

已存在代码路由界面：

```text
全局/布局：2
账号与关联：3
主 Tab：4
日记：2
照片与相册：3
AI：6
纪念日：2
数据导出：2
更多功能：3
合计：27 个
```

设计稿已规划但待完整代码落地的界面：约 18 个。
