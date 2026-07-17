# 照片 Storage 补偿所有权批次

- 日期：2026-07-17
- 分支：`codex/phase2-real-data`
- 范围：`src/api/photoApi.js`

## 完成内容

1. 为上传流程中的文件增加 `createdByOperation` 标记。
2. 数据库创建照片集或照片行失败时，只删除本次操作新上传的对象。
3. 调用方传入的既有 `storagePath` 仅校验路径，不作为本次失败补偿的删除目标。
4. 捕获异常时也会清理已经上传成功但尚未持久化的对象。
5. 补偿失败时统一返回 `cleanupRequired` 和 `failedCleanupCount`。
6. 删除已持久化照片集时，仍会清理该记录关联的 Storage 对象。

## 测试

新增：`src/__tests__/photoStorageCompensation.static.test.js`

静态守卫覆盖：

- 仅清理当前操作创建的对象；
- 异常路径执行补偿；
- 补偿失败元数据不会丢失。

## 未执行验证

当前 GitHub Connector 不提供仓库命令执行环境，因此本批未实际执行：

- `npm run test:final`
- `npm run check:web`
- `npx expo export --platform android`
- `git diff --check`
- Supabase Storage/RLS 集成测试

本批不能标记为云端联调通过。后续需使用真实项目验证多图上传中途失败、数据库失败、对象删除失败和既有路径复用场景。
