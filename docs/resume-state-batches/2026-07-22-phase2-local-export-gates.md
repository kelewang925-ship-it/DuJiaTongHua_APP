# 第二阶段批次记录：当前 HEAD 本地导出门禁

## 基线

- 分支：`codex/phase2-real-data`
- 基线提交：`2a25a6d`
- 工作区已有其他未提交测试文件改动与 `=0.2.6` 文件；本批未修改、暂存或删除它们。

## 已执行并通过

- `npm run test:final`：93 个测试套件、303 个测试通过；页面结构、Real 模式、Real 页面、API 审计均通过。
- `npm run check:web`：成功导出 `dist/web`，共 192 个文件。
- `npx expo export --platform android --output-dir dist/android-check`：成功导出 196 个 Android bundle/asset 文件。
- `git diff main...HEAD --check`：通过。
- `app/` 直接 Supabase Client 导入扫描：为空。

## 仍不构成通过

- 本机当前未运行项目，A/B/C 未登录；没有新的浏览器 A/B/C 权限或业务闭环证据。
- Android 静态 export 不是 Android 真机验收。
- 不得据此标记第二阶段发布就绪。
