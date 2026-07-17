# 2026-07-17 Store 服务端真值与回滚批次

## 范围
- `src/store/useFairyStore.js`
- `src/__tests__/storeServerTruth.static.test.js`

## 已完成
- 服务端写入成功但核心数据刷新失败时，返回成功并标记 `refreshFailed`，避免重复提交。
- 通知和胶囊提醒失败仅回滚目标记录，不覆盖其他并发成功状态。
- 全部通知已读失败只回滚仍处于本次乐观时间戳的记录。
- 本地数据清理使用 `Promise.allSettled`，部分删除失败也会退出旧 Session 状态。
- Realtime 频道失败进入 Store 的 `errors.realtime`，连接恢复时清除错误。

## 验证状态
未执行 Jest、Web、Android export、并发交互、断网重连或多账号 Session 切换集成测试。