# 2026-07-17 第二阶段安全加固批次

## 分支

- `codex/phase2-real-data`
- 未修改 `main`
- 未创建额外分支

## 已完成

- 新增迁移 `supabase/migrations/202607170004_security_hardening.sql`。
- 收口全部第二阶段 `SECURITY DEFINER` 函数的默认 `PUBLIC` 执行权限，只向 `authenticated` 开放客户端所需 RPC。
- 显式撤销客户端直接更新或删除情侣关系表的权限，情侣成员和状态继续只允许受控 RPC 修改。
- 拆分自定义标签 RLS，禁止伪造 `created_by`，并限制为当前仍处于 active 情侣关系的创建者修改或删除。
- 修正照片集、日记附件在解绑后仍可更新或删除的问题。
- 将时光胶囊读取、更新、删除保持在受控 RPC 后，避免客户端绕过锁定读取规则。
- 新增安全 UUID 解析函数，Storage RLS 对错误路径返回拒绝而不是因 UUID 强制转换报错。
- Storage 写入路径强制为 `{coupleId}/{userId}/{filename...}`，删除同时校验对象所有者、路径用户和 active 情侣关系。

## 审计依据

- `202607170002_initial_rls.sql` 曾允许情侣成员直接更新 `couples`，并曾允许客户端插入通知；迁移 003 已移除对应策略，本批进一步收口表权限与函数权限。
- `202607170003_real_data_core.sql` 的照片集、附件和 Storage 删除策略未统一校验 active 情侣关系；本批补齐解绑状态。
- `custom_tags_member_all` 允许 active 成员写入任意 `created_by`；本批改为不可伪造的创建者策略。

## 验证状态

当前 ChatGPT 执行环境无法解析 `github.com`，本地 clone 失败，因此以下固定门禁未在本批冒充执行成功：

- `npm run test:final`：待 Codex 执行
- `npm run check:web`：待 Codex 执行
- `npx expo export --platform android --output-dir dist/android-check`：待 Codex 执行
- `git diff --check`：待 Codex 执行
- `supabase db push --dry-run`：待提供 Project Ref、URL、Anon Key，并修复/替换 CLI 后执行
- 三账号 RLS / Storage 集成测试：待 Supabase 开发项目

## 外部阻塞

- 尚未提供 Supabase 开发项目 Project Ref、URL、Anon Key。
- 当前环境无法建立 GitHub 本地 checkout，只能通过 GitHub Connector 修改远端文件。
- `docs/resume-state.md` 的完整文件替换接口不支持安全的追加式 patch；为避免覆盖其中约 400 行历史记录，本批状态先写入此独立检查点。Codex 拉取后应把本节摘要合并到 `docs/resume-state.md`，再执行统一验证。

## 下一步

1. Codex 拉取 `codex/phase2-real-data`，审查迁移 004 的 PostgreSQL/Supabase 兼容性。
2. 执行固定门禁和 SQL 静态检查。
3. 提供开发项目参数后运行 `link → db push --dry-run → db push`。
4. 使用 A/B 情侣账号与 C 非成员账号覆盖 pending、active、解绑、标签创建者、照片附件、Storage 非法路径、胶囊锁定和通知伪造场景。
