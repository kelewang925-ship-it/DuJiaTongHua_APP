# 2026-07-18 Pending 邀请持有者绑定修复

## 范围

本批只修复第二阶段真实 Supabase 联调发现的邀请绑定规则，不修改 `main`、`docs/resume-state.md`、001-005 迁移或第三阶段计划。

## 问题

旧 `bind_couple_by_invite` 会在当前用户拥有 pending 邀请时直接拒绝绑定其他用户的邀请码，导致“每个未绑定用户自动拥有邀请码”与“用户可接受他人邀请”两个产品规则冲突。

## 实现

新增迁移：

- `supabase/migrations/202607180006_allow_pending_invite_holder_to_bind.sql`

006 仅 replace `public.bind_couple_by_invite(text)`：

1. 校验登录、邀请码格式、有效期和非本人邀请码。
2. 解析目标邀请所有者 A。
3. 按 A/B UUID 文本排序，获取两个 `pg_advisory_xact_lock`，与 `create_couple_invite` 的用户锁保持一致。
4. 锁后重新检查 A、B 均未处于 active 情侣关系。
5. 使用 `FOR UPDATE` 重新确认并锁定 A 的 pending 邀请。
6. 锁定 B 自己的全部 pending 邀请行。
7. 先将 B 的 pending 行更新为 `disconnected`，并清空邀请码与过期时间。
8. 再将 A 的目标行更新为 active，写入 `user_b`，并清空邀请码与过期时间。
9. 返回 A 的 active couples 行。

所有状态转换都在同一次 RPC 事务中完成。B 的旧邀请码在提交后为 null，不能再被其他账号使用。

权限保持：

- `SECURITY DEFINER`
- `set search_path = public`
- PUBLIC/anon execute revoke
- 仅 authenticated execute grant
- authenticated 对 `public.couples` 的直接 insert/update/delete 仍由 005 revoke

## 客户端

- `app/account/invite.js` 保持页面进入后自动调用 `createInviteCode()`。
- 页面仍允许用户在拥有自己的邀请码时输入并确认他人邀请码。
- `src/api/coupleApi.js` 仅更新绑定失败的统一可展示文案，不暴露数据库内部错误。

## 测试

新增：

- `src/__tests__/pendingInviteHolderBinding.static.test.js`

覆盖：

- 邀请页自动创建/复用邀请码。
- B 持有 pending 邀请时可绑定 A。
- B 原 pending 邀请先被关闭并清空 code/expiry。
- A 目标邀请变为 active 并清空 code/expiry。
- active 用户不能创建或绑定其他邀请。
- 双用户确定性 advisory lock 和目标/自有 pending 行锁。
- 客户端仍不能直接修改 couples。

## 本地门禁

当前执行环境无法解析 `github.com`，仓库克隆失败：

```text
Could not resolve host: github.com
```

因此以下命令在本批最终 HEAD 上均未运行：

- `npm run test:final`
- `npm run check:web`
- `npx expo export --platform android --output-dir dist/android-check`
- `git diff main...HEAD --check`

## Dashboard 执行要求

开发项目已手动执行 001-005。Codex 复验代码后，只需在 Supabase Dashboard SQL Editor 单独执行：

- `supabase/migrations/202607180006_allow_pending_invite_holder_to_bind.sql`

执行后使用 A/B/C 账号验证：B 先生成自己的邀请码，再绑定 A；确认 B 旧邀请码不可用，A/B 只有一条 active 关系，active 用户继续被 RPC 拒绝。
