# 2026-07-17 Codex 最终验证问题修复批次

## 基线与范围

- 仓库：`kelewang925-ship-it/DuJiaTongHua_APP`
- 分支：`codex/phase2-real-data`
- 起点：`2891472750853eb7446419efb542123ac15ef960`
- 类型：Codex 最终验证问题修复，不扩展第二阶段功能范围
- `main`：未修改
- `docs/resume-state.md`：按要求未覆盖或替换

## 实现缺陷修复

- 将历史占位路由 `app/account/couple-settings.js` 改为安全重定向到 `/account/couple-info`，移除 FeaturePage 模拟保存和“后续接入”文案。
- `normalizeDateOnly` 严格支持 `YYYY-MM-DD`、点号、斜杠、带时间输入和 ISO 日期时间，并通过 UTC 日历字段校验拒绝自动滚动的非法日期。
- `getCoupleInfo` 对缺失的后端情侣关系状态显式规范为 `null`。
- `app/ai/history.js` 在 Real 模式明确显示 AI 生成、历史同步和分享“暂未开放”，且不展示模拟成功结果。

## 审计脚本误报修复

- `audit-page-structure.mjs` 改为根据 `router.replace/router.push + return null + 无 JSX 页面输出` 识别 redirect-only 页面，不依赖组件命名。
- `audit-real-pages.mjs` 使用大小写不敏感的提交状态检测，支持 `isSaving`、`saving`、`submitting`、`uploading`。
- 保留 `audit-real-mode.mjs` 的 Real 模式“未开放”要求，通过修复 AI 历史页满足规则，没有降低审计标准。

## 过期测试同步

- Store 测试改为验证胶囊提醒和通知的项目级、时间戳条件式并发安全回滚。
- 日记与照片补偿测试验证回滚顺序、`createdByOperation`、`cleanupRequired` 和 `failedCleanupCount`，不再锁定旧中文文案。
- API 协议测试使用 `PERMISSION_DENIED`、`SESSION_EXPIRED`、`NETWORK_ERROR`、`CONFLICT` 公共错误码，并验证原始错误保存在 `raw`。
- Tag、Comment、Notification 测试允许用于归属确认的额外返回字段，不再锁定旧 `select` 字符串。
- Time Capsule 测试验证正文清除、情侣空间/创建者归属和 fail-closed 行为。
- Export Preview 测试接受 `validConfig && itemCount > 0` 的更严格语义。
- Backup 测试验证 Mock/Real 动态按钮标题下均为 disabled。
- Help Feedback 测试禁止真实 ticket ID、受理编号值和模拟成功状态，同时允许“不会生成受理编号”的说明文案。
- 日期行为测试新增所有要求格式及非法日期覆盖。

## 验证状态

当前执行环境无法解析 `github.com`，本地克隆失败，因此以下命令本批 **未运行**：

- `npm run test:final`
- `npm run check:web`
- `npx expo export --platform android --output-dir dist/android-check`
- `git diff main...HEAD --check`
- `npm run audit:pages`
- `npm run audit:real`
- `npm run audit:real-pages`
- `npm run audit:api`

Codex 上一轮的通过结果不冒充本批新 HEAD 的验证结果。需由 Codex 拉取最终 HEAD 后重新执行全部门禁。

## 交接状态

- `ready_for_codex_revalidation: yes`
- `ready_for_release: no`

发布状态继续受 Supabase 迁移、A/B/C 三账号权限矩阵、双账号 Web 闭环和 Android 真机闭环约束。
