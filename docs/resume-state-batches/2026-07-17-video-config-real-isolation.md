# AI 短视频配置 Real Mode 隔离批次

## 日期

- 2026-07-17（Asia/Shanghai）
- 分支：`codex/phase2-real-data`

## 本批修改

- `app/ai/video-config.js`
  - 使用 `getApiMode()` 明确区分 Mock/Real。
  - 演示标题、素材、风格、时长、音乐仅在 Mock Mode 初始化。
  - Real Mode 不再预填虚构内容。
  - Real Mode 禁用输入、素材、风格、时长、字幕和音乐配置。
  - Real Mode 不创建本地 AI 任务，不跳转模拟进度页。
  - 删除“预计完成并自动保存到创作历史”的误导承诺。
  - Mock Mode 的任务状态明确标记为流程演示。

- `src/__tests__/videoConfigTruth.static.test.js`
  - 增加 Mock 默认值隔离守卫。
  - 增加 Real 控件禁用守卫。
  - 增加禁止自动保存承诺的守卫。

## 数据库影响

- 无迁移。
- 无 Supabase 表、RPC、RLS 或 Storage 修改。

## 验证状态

- GitHub 端已创建代码、静态测试和批次记录提交。
- 本批未在本地执行 `npm run test:final`、`npm run check:web`、Android Expo export 或 `git diff --check`。
- 未进行 Chrome、Android 真机或真实 AI 服务验证。

## 剩余风险

- AI 视频真实生成服务仍未接入，这是第二阶段明确允许的未开放能力。
- 需由 Codex 在统一验证阶段执行构建、测试和设备级检查。
