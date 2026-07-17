# 2026-07-17 用户资料写入边界批次

## 已完成

- 限制昵称最大长度。
- 限制头像文字长度。
- 头像 URL 仅接受有效 HTTP/HTTPS 地址并限制长度。
- Profile upsert 返回必须匹配当前登录用户 ID。
- 新增静态守卫覆盖资料字段和账号归属确认。

## 待验证

当前环境未执行测试、Web 构建、Android export、diff check 和 Supabase Profile RLS 集成测试，不记录为已通过。
