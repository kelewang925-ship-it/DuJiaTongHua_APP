# 2026-07-17 登录会话服务端校验批次

## 范围
- `src/api/authApi.js`
- `src/__tests__/authSessionVerification.static.test.js`

## 已完成
- `getCurrentSession` 不再只信任本地缓存的 `getSession()`。
- 存在 Session 时额外调用 `getUser()` 验证服务端认可的当前用户。
- Session 用户 ID 与验证用户 ID 不一致时明确失败，不进入 Real 数据加载。
- 无 Session 继续返回明确的未登录状态。

## 验证状态
当前 GitHub Connector 环境未执行完整测试、构建、Android export 与真实过期 Session 验证，不记录为已通过。
