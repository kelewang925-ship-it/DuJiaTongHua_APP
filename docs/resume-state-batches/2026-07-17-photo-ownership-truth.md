# 2026-07-17 相册与照片归属真值批次

## 范围
- `src/api/photoApi.js`
- `src/__tests__/photoOwnershipTruth.static.test.js`

## 已完成
- 相册列表与详情校验情侣空间归属。
- 嵌套照片校验 `couple_id` 与 `collection_id`。
- 创建照片集与照片行要求服务端返回完整且归属一致的记录。
- 删除前后均验证照片集属于当前用户和情侣空间。
- 保留 Storage 失败补偿与清理标记。

## 验证状态
未执行多账号 RLS、Storage 集成测试、Jest、Web 或 Android export。