# 2026-07-18 私有照片签名 URL 读取验证

## 验证范围

- 分支：`codex/phase2-real-data`
- 代码基线：`10805ba fix(storage): validate object UUID as filename`
- 云端前置：001–009 迁移已在 Supabase 开发项目执行；009 修正 Storage Policy 对 `storage.foldername(name)` 与 `storage.filename(name)` 的路径解析。

## 实际证据

在已登录的 A/B 情侣会话中，从首页打开“回忆相册”，进入照片集“Storage 验证”。页面显示 1 张照片，浏览器实际加载了以下私有 Bucket 签名对象：

- Bucket：`photos`
- 路径：`a59f7a31-649d-44c5-ae11-cf026a5128af/b753864f-feb8-4a01-8e6c-0b7332b29cd1/69c1ece8-c19f-4d72-bbd6-56c66371df4d`
- URL 类型：`/storage/v1/object/sign/photos/...`
- 图片自然尺寸：`640 × 427`
- 浏览器控制台：未观察到图片读取 error。

这证明上传后的私有对象可以通过短期签名 URL 在情侣会话中实际显示，不只是 Realtime 的照片计数更新。

## 仍待完成

1. 明确以 B（非上传者）会话确认同一张图片可显示，并尝试删除 A 的照片集，必须被 RLS 拒绝且不删除任何数据。
2. 以 C（未绑定）会话确认无法读取、上传或删除 A/B 情侣空间的照片对象。
3. 执行上传/数据库写入失败补偿的受控场景，并记录对象是否残留。

本检查点不等同于完整 A/B/C Storage 权限矩阵通过，也不改变 Android 真机仍待验的结论。
