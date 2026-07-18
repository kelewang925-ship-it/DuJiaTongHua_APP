# 2026-07-18 Storage 路径策略修复

## 根因

真实 A 用户上传照片时，私有 Storage 写入被 RLS 拒绝。受控 SQL 验证确认 A 的认证上下文和活跃情侣关系均正确。

`storage.foldername(name)` 只返回目录数组，不包含对象文件名。对于 `{coupleId}/{userId}/{uuid}`，它返回两个元素；005 错误地要求三段并从第三段读取 UUID，使所有合规上传都被拒绝。

## 修复

新增 `202607180009_fix_storage_object_path_policies.sql`：

- 目录数量严格为两段；
- 第三部分改由 `storage.filename(name)` 读取并验证为 UUID；
- 保持情侣成员读取、本人上传和本人删除的既有权限边界。

## 部署与复验

在 Dashboard SQL Editor 单独执行 009 后，使用 A 上传一张照片；再使用 B 验证可读取签名 URL，使用 C 验证不能访问或上传。不得重跑 001–008。
