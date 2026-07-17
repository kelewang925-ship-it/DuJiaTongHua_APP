# 2026-07-17 API 客户端模式失败关闭批次

## 范围
- `src/api/client.js`
- `src/__tests__/apiModeFailClosed.static.test.js`

## 已完成
- API 模式仅接受 `real` 与 `mock`，未知值进入 `disabled`。
- `isMockMode` 仅在明确 Mock 时返回 true。
- `requestMock` 在非 Mock 环境中明确失败，不再产生演示成功。
- 无效模式归类为不可重试的配置错误。
- `getAuthenticatedContext` 验证服务端用户与 Session 用户一致。

## 验证状态
当前环境未执行完整测试、Web 构建、Android export、无效环境变量启动测试和真实 Session 失效测试，不记录为已通过。
