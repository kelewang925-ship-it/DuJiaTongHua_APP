# 2026-07-17 认证返回身份一致性批次

## 范围
- `src/api/authApi.js`
- `src/__tests__/authResultIdentity.static.test.js`

## 已完成
- 登录结果必须同时包含有效 Session 与用户。
- Session 用户、返回用户和提交邮箱必须一致。
- 注册资料只传递允许的昵称、头像文字和头像 URL 字段。
- 注册无 Session 时保留邮箱验证状态，但仍要求返回用户身份。

## 验证状态
未执行真实邮箱登录、邮箱确认、Supabase Auth 集成测试、Jest、Web 或 Android export。