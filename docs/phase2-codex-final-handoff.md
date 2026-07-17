# 《独家童话》第二阶段 Codex 最终交接

## 交接状态

- 分支：`codex/phase2-real-data`
- `main`：未修改
- ChatGPT 代码开发：完成并停止扩展范围
- 发布状态：未就绪，等待最终门禁、Supabase 云端联调和真机验证
- 主恢复基线：`docs/resume-state.md`
- 详细修复证据：`docs/resume-state-batches/`

## 第一组：本地最终门禁

按以下顺序执行并保存完整输出：

```bash
npm install
npm run test:final
npm run check:web
npx expo export --platform android --output-dir dist/android-check
git diff --check
```

同时执行：

- 扫描 `app/` 是否直接导入 Supabase Client。
- 分别验证 `EXPO_PUBLIC_API_MODE=mock`、`real` 和无效值。
- 确认 `.env`、生成目录、测试账号凭据和密钥未进入 Git。
- 确认工作区在验证完成后保持可解释，不删除用户已有成果。

## 第二组：Supabase 迁移

仅在获得开发项目 Project Ref、URL 和 Anon Key 后执行：

1. 将 URL 和 Anon Key 写入本地 `.env`，不得提交。
2. 检查 Supabase CLI；同类启动方案最多尝试两次。
3. 执行 `supabase link`。
4. 执行迁移 dry-run。
5. 审核 SQL 顺序、RLS、函数权限、触发器和私有 Bucket。
6. 执行正式迁移。
7. 保存迁移输出和远端 schema 证据。

## 第三组：三账号权限矩阵

准备：

- A：情侣成员 A
- B：情侣成员 B
- C：非成员账号

必须覆盖：

- 未登录访问全部 public 业务表。
- A/B 读取同一情侣空间记录。
- C 无法读取或修改 A/B 的记录。
- 本人和伴侣的允许写入边界。
- 解绑、inactive 和异常关系状态。
- 通知不能由客户端任意伪造。
- 未解锁时光胶囊正文不可读取。
- Storage 路径只能使用 `{coupleId}/{userId}/{uuid}`。
- 用户只能删除本人拥有的对象。
- 签名 URL 只能访问当前情侣空间允许的对象。

## 第四组：双账号 Web 闭环

A/B 两个浏览器会话完成：

1. 注册并确认邮箱。
2. A 创建邀请码。
3. B 使用邀请码绑定。
4. A 创建日记和图片附件。
5. B 刷新或通过 Realtime 看到日记。
6. A 创建多图照片集。
7. B 看到照片集并创建评论。
8. A 收到评论通知。
9. A 单项已读、全部已读。
10. 验证断网、刷新失败、重复提交防护和错误提示。
11. 退出 A，确认旧 Realtime 不再更新。
12. 切换账号，确认缓存和草稿命名空间隔离。

## 第五组：失败补偿与并发

必须主动制造并验证：

- 附件上传成功但日记写入失败。
- 多图部分上传成功后后续上传失败。
- 照片集创建成功但照片行写入失败。
- 数据库删除成功但 Storage 删除失败。
- 服务端写入成功但核心数据刷新失败。
- 两条通知并发标记已读，其中一条失败。
- 胶囊提醒并发修改，其中一条失败。
- Realtime 频道错误、超时、关闭和恢复。
- AsyncStorage 部分 key 删除失败后的退出状态。

## 第六组：Android 真机

至少复验：

- 注册、登录、Session 恢复和退出。
- 邀请码复制、输入与绑定。
- 相册权限和多图选择。
- 日记图片附件上传。
- 键盘遮挡、返回行为和 Safe Area。
- 私有图片签名 URL 展示。
- 网络断开、超时和重试。
- App 重启后的账号数据隔离。
- 分享面板的分享、取消和失败结果。

## 成功标准

只有以下项目全部通过，才可将第二阶段标记为“发布就绪”：

- 当前最终 HEAD 本地门禁通过。
- 迁移 dry-run 和正式迁移通过。
- A/B/C 权限矩阵通过。
- Storage 上传、签名 URL、删除和失败补偿通过。
- 双账号 Web 闭环通过。
- Realtime 清理和并发回滚通过。
- Android 真机核心闭环通过。

## 禁止误报

不得把以下情况写成已完成：

- 代码存在等于云端联调通过。
- 静态测试存在等于 Jest 已执行。
- Expo export 通过等于 Android 真机通过。
- RLS SQL 存在等于三账号权限已验证。
- 系统分享面板打开等于用户已经分享。
- 服务端写入成功后刷新失败等于写入失败。
- Mock 演示等于 Real 能力已接入。

验证发现缺陷时，只做与缺陷直接相关的修复；每个修复独立 Commit，并同步 `docs/resume-state.md`。
