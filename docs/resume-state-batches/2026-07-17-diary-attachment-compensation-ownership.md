# 2026-07-17 日记附件补偿所有权批次

## 范围

- `src/api/diaryApi.js`
- `src/__tests__/diaryAttachmentCompensation.static.test.js`

## 已完成

- 将调用方传入的既有 `storagePath` 与本次新上传附件区分处理。
- 仅对 `createdByOperation: true` 的本次上传对象执行失败补偿删除。
- 上传中断、数据库写入失败、附件表写入失败和异常抛出路径均尝试清理本次新上传对象。
- 补偿失败时返回 `cleanupRequired` 与 `failedCleanupCount`。
- 删除已持久化日记时仍显式清理该日记关联的本人附件对象。
- 增加静态守卫，防止后续重新误删既有对象或遗漏异常补偿。

## 风险说明

- 本批只完成客户端补偿所有权边界，不代表 Supabase Storage/RLS 已完成真实云端验证。
- 仍需在 A/B 情侣账号和 C 非成员账号环境中验证上传、回滚、删除以及对象路径权限。
- 数据库删除成功但 Storage 清理失败时，API 会明确返回部分失败并标记需要后续清理。

## 验证状态

当前 GitHub Connector 环境未执行：

- `npm run test:final`
- `npm run check:web`
- `npx expo export --platform android --output-dir dist/android-check`
- `git diff --check`
- Supabase Storage 集成测试

以上项目保持待 Codex 或本地环境执行，不记录为已通过。
