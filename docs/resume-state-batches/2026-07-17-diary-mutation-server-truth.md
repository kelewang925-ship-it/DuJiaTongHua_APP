# 2026-07-17 日记写入服务端真值批次

## 范围
- `src/api/diaryApi.js`
- `src/__tests__/diaryMutationTruth.static.test.js`

## 已完成
- 创建、更新、删除均要求服务端返回真实记录。
- 校验日记 ID、情侣空间和作者归属。
- 零行更新或删除不再报告成功。
- 日记列表与详情增加情侣空间归属验证。
- 保留附件失败补偿和 Storage 清理边界。

## 验证状态
GitHub Connector 环境未执行 Jest、Web、Android export、Supabase RLS/Storage 集成测试，不记录为已通过。