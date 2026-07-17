# 2026-07-17 API、Storage 与 Realtime 审计批次

## 范围

- `src/api/realtimeApi.js`
- `src/api/storageApi.js`
- `src/api/photoApi.js`
- `src/api/diaryApi.js`
- `src/api/authApi.js`
- `src/api/client.js`
- `src/api/mappers.js`
- `src/store/useFairyStore.js`
- `src/components/AuthGate.js`
- `src/config/capabilities.js`

## 已完成

- Realtime Channel 名称加入用户维度，取消函数幂等；取消后旧回调不再刷新新 Session/情侣的数据。
- Storage 写入与删除在客户端强制校验允许的私有 Bucket 以及 `{coupleId}/{userId}/{fileName}` 路径。
- Signed URL 限制当前情侣空间，并把有效期限制为 60 秒至 24 小时。
- 照片删除语义修正为照片集级删除，与 Store 中照片集记录 ID 保持一致。
- 照片集多图上传补齐空文件校验、上传失败清理、照片行失败时删除照片集及文件，并通过 `meta.cleanupRequired` 暴露补偿失败。
- 日记附件上传、日记写入、附件行写入和删除流程增加所有者/情侣条件与补偿失败报告。
- 新增 `src/__tests__/storageApi.test.js`，覆盖合法路径、跨情侣、跨用户、非法 Bucket 与非法路径。
- 检查 Capability：Real 模式 AI 生成、支付、PDF、备份、语音、位置和反馈附件均配置为 false；页面运行行为仍需 Codex 本地验证。
- 检查 AuthGate：存在 Session 首次检查和 Auth 状态订阅；Store reset 会取消当前 Realtime。旧 Channel 回调竞态已在 API 层防护。

## 静态审查结论

- 页面目录代码搜索未返回直接 Supabase Client 调用结果；GitHub 代码索引对目标分支可能存在延迟，必须由 Codex 本地 grep 再确认。
- API 返回继续使用 `{ success, data, meta, error }`。
- mapper 递归处理 snake/camel 字段；本批未修改 mapper。
- 通知已读动作已有乐观更新失败回滚。
- Real Store 的核心写动作在服务端成功后重新加载数据，没有先写本地成功态。

## 未运行验证

以下均未执行，不得视为通过：

- `npm run test:final`
- `npm run check:web`
- `npx expo export --platform android --output-dir dist/android-check`
- `git diff --check`
- Mock/Real 运行检查
- Supabase migration dry-run/deploy
- 三账号 RLS/Storage 集成测试
- 双账号 Web 闭环
- Android 真机闭环
- Chrome 实时验证

原因：当前执行环境无法 clone/运行仓库；Supabase Project Ref、URL、Anon Key 尚未提供。

## Codex 复验重点

1. 运行新增 Storage 单元测试，确认 React Native `Platform` 和 Jest mock 兼容。
2. 验证删除照片集时嵌套 `photos(storage_path)` 查询与 RLS 行为。
3. 模拟照片行写入失败和 Storage 删除失败，检查 `meta.cleanupRequired`。
4. 快速切换账号、解绑/重新绑定，确认旧 Realtime 回调不再刷新。
5. 本地扫描所有 `app/` 页面是否直接引用 `src/api/client` 或 Supabase Client。
6. 验证所有 Real 未开放入口显示明确提示且不产生本地成功记录。
