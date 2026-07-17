# 2026-07-17 页面结构与 Capability 批次

## 基线

- 分支：`codex/phase2-real-data`
- Codex 基线：`c3155838c80fc0e266b0da219d41789fdd0521c7`
- 未修改 `main`，未创建额外开发分支。

## 已完成

- `app/ai/character-profile.js`
  - 改为 `FairyPage` 根容器。
  - 返回与标题改为 `FairyPage.header={<FairyHeader ... />}`。
  - Real 模式通过 `aiGeneration` Capability 显示“未开放”，不再模拟保存成功。
  - Mock 模式保留本地演示保存 Toast。
- `app/settings.js`
  - 将 `FairyHeader` 移入 `FairyPage.header`，主体业务与视觉内容保持不变。
- `app/data/backup.js`
  - 将 `FairyHeader` 移入 `FairyPage.header`。
  - 保留既有云备份 Capability 拦截。
- `app/anniversary/index.js`
  - 将 `FairyHeader` 移入 `FairyPage.header`。
- `app/anniversary/countdown.js`
  - 将 `FairyHeader` 移入 `FairyPage.header`。

## 验证状态

本环境无法 clone 仓库，原因：`Could not resolve host: github.com`。本批未运行：

- `npm run test:final`
- `npm run check:web`
- Android Expo export
- `git diff main...HEAD --check`

上述命令需要 Codex 拉取最新远端提交后统一执行。

## 仍在继续

- 其余指定 Header 页面整改。
- 全量 `app/` 页面结构扫描。
- API、Store、Real 页面与 Capability 全量审查。
- 测试补充与迁移静态审计。
