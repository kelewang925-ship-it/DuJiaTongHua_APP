# 时光胶囊未解锁正文边界

## 批次目标

在数据库 RPC 和 RLS 之外增加客户端 API 防御层，避免未解锁胶囊正文进入 Zustand、页面状态、调试工具或错误日志。

## 修改范围

- `src/api/timeCapsuleApi.js`
- `src/__tests__/timeCapsuleContentBoundary.static.test.js`

## 已完成

- 新增统一 `sanitizeCapsule` / `sanitizeCapsules` 映射。
- 只有服务端明确标记已解锁，或解锁日期已到达时才保留正文。
- 未解锁记录在 API 返回前把 `content` 设为 `null`。
- 列表、创建结果和更新结果都经过相同正文边界。
- 删除与提醒 RPC 行为未改变。
- Mock 模式仍保留原有演示行为，不影响第一阶段视觉体验。

## 安全说明

这是一层纵深防御，不能替代数据库 RPC 与 RLS。正式联调仍必须验证 `get_time_capsules`、更新 RPC 和表权限不会向未解锁用户返回正文。

## 验证状态

- 已新增静态守卫测试。
- 本批未在 GitHub Connector 环境中执行 `npm run test:final`。
- 本批未执行 Web 构建、Android export、Supabase dry-run 或三账号 RLS 测试。

## 下一步

继续审查 Store 是否会从历史缓存恢复旧版未解锁正文，并在 Supabase 项目可用后执行 A/B/C 三账号胶囊读取权限测试。
