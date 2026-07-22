# 2026-07-22 时光胶囊创建权限修复

## 问题

A/B 已绑定账号在 Real 模式创建时光胶囊时，页面提示“当前账号没有权限执行此操作”。

## 根因

`202607170004_security_hardening.sql` 已撤销 `time_capsules` 的客户端 `SELECT` 权限，但客户端创建逻辑仍使用 `insert(...).select('*')`。PostgREST 在返回插入行时需要 SELECT 权限，因此请求被规范化为 `PERMISSION_DENIED`，即使写入本身没有完成也不能作为成功处理。

## 修复

- `src/api/timeCapsuleApi.js` 的 Real 创建改为调用受控 `create_time_capsule` RPC。
- 新增 `supabase/migrations/202607220010_time_capsule_create_rpc.sql`：
  - 通过 `SECURITY DEFINER` 校验登录身份、active 情侣关系和创建字段；
  - 由服务端写入 `creator_id = auth.uid()` 并返回真实行；
  - 撤销 `PUBLIC`/`anon` 执行权限，仅授予 `authenticated`；
  - 撤销客户端对 `time_capsules` 的直接 INSERT，继续保持所有胶囊变更走受控 RPC。
- 增加 API 与迁移静态安全断言。

## 验证

- 目标 Jest：13/13 通过。
- `git diff --check`：通过（工作区另有用户未提交改动，未触碰）。
- Dashboard 尚需手动执行 `202607220010_time_capsule_create_rpc.sql`，再使用 A/B 各创建一次未来日期胶囊，确认创建成功且列表仍隐藏未解锁正文。

## 状态

代码修复已准备提交；云端迁移执行和 A/B 手动复验待完成。Android 真机验收仍未完成，第二阶段不得标记发布就绪。
