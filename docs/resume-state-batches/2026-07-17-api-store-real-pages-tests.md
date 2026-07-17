# 第二阶段批次检查点：API、Store、Real 页面与测试

## 分支

`codex/phase2-real-data`

## 基线

`9f56f986338311d683f99d8c539fb9cd3ca5c26c`

## 本批完成

- 新增 `scripts/audit-page-structure.mjs`，扫描普通 app 路由的 FairyPage、FairyPage.header/FairyHeader 和页面直连 Supabase。
- 排除规则固定为 `_layout`、纯 Redirect 路由和 `dev-ui-lab` 包装文件。
- 新增 `scripts/audit-real-mode.mjs`，检查 AI、会员、PDF、备份、反馈、语音和位置 Capability，以及未守卫 Mock 写动作。
- 两个审计脚本已接入 `npm run test:final`。
- 新增 `FairyRequestState`，统一加载、Session 失效、权限失败、网络失败和重试 UI。
- 评论、通知、标签、时光胶囊页面补齐加载、错误重试、提交中和失败状态。
- 评论 Real 模式不再模拟点赞成功。
- 通知、胶囊乐观更新失败沿用 Store 回滚。
- 新增资料 API；情侣资料黄金页面保持视觉结构并接入真实资料、受控起始日更新、伴侣只读和未开放项提示。
- 邀请码页补齐生成失败重试、本人邀请码校验和准确复制/分享结果。
- 绑定确认页补齐缺失邀请码、无效/过期/重复绑定、绑定后刷新失败状态。
- 反馈提交和反馈附件拆分 Capability，Real 模式均不模拟成功。
- 日记语音和位置附件 Real 模式明确未开放，Mock 模式只保留视觉演示。
- 补充 Storage UUID、API 四字段协议、错误分类、日期 mapper、Store 竞态、上传补偿和迁移静态安全测试。

## 本批未运行验证

当前执行环境无法 clone 仓库，因此下列验证未在本批执行：

- `npm run test:final`
- `npm run check:web`
- Android Expo export
- `git diff main...HEAD --check`
- Supabase migration dry-run

Codex 对 `c315583` 的历史通过记录不覆盖本批新增提交。

## 云端阻塞

仍缺少 Supabase Project Ref、URL 和 Anon Key，因此迁移、三账号 RLS/Storage 和双账号闭环尚未执行。

## 下一步

- 继续扫描剩余 Real 页面和页面结构。
- 复核搜索、时间线、日记详情、照片页、纪念日列表和资料聚合状态。
- 补充 profile API、页面审计和锁定胶囊测试。
- 完成后再由 Codex 统一运行门禁并整合到 `docs/resume-state.md`。
