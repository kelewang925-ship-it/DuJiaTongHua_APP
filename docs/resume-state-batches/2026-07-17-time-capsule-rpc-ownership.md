# 2026-07-17 时光胶囊 RPC 归属批次

- 读取、创建、更新、删除和提醒更新均要求当前存在有效情侣关系。
- 胶囊对象必须属于当前情侣空间。
- 创建结果必须属于当前创建者。
- 删除和提醒 RPC 返回 ID 必须与请求目标一致。
- 未解锁正文继续在 API 边界清空。
- 增加静态守卫测试。

未在 GitHub Connector 环境执行本地 Jest、Web、Android export、`git diff --check` 或 Supabase 集成测试。
