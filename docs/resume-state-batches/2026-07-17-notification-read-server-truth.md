# 2026-07-17 通知已读服务端真值批次

## 范围

- `src/api/notificationApi.js`
- `src/__tests__/notificationReadTruth.static.test.js`

## 完成项

- 单项已读操作增加通知 ID 校验。
- 更新后通过 `select('id, read_at').maybeSingle()` 获取服务端实际更新结果。
- RLS 拒绝、目标不存在或记录已删除导致零行更新时返回失败，允许 Store 回滚乐观状态。
- 全部已读操作返回服务端实际更新的 `updatedIds`，不再只返回客户端生成的时间戳。
- Mock 模式保持可用，并返回兼容的 `updatedIds` 字段。
- 新增静态测试，防止后续删除服务端更新确认。

## 风险与边界

- Store 当前已有乐观更新失败回滚，本批补齐 API 层零行更新识别。
- 本批没有执行真实 Supabase RLS 联调，仍需使用本人、伴侣和非成员账号验证通知只允许接收者更新。
- `updatedIds` 已提供给后续更细粒度状态同步使用；当前 Store 仍以请求成功为整体确认。

## 验证状态

当前 GitHub Connector 环境未执行：

- `npm run test:final`
- `npm run check:web`
- Android Expo export
- Supabase 三账号集成测试

因此本批只记录代码和静态守卫已提交，不宣称构建或云端联调通过。
