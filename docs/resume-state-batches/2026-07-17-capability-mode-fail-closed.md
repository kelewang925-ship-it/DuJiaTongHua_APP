# 2026-07-17 能力模式失败关闭批次

## 范围
- `src/config/capabilities.js`
- `src/__tests__/capabilityModeFailClosed.static.test.js`

## 已完成
- API 模式只接受 `real` 与 `mock`。
- 未知、空白或拼写错误的模式统一进入 `disabled`。
- `disabled` 能力矩阵全部关闭，避免异常环境变量继承 Mock 全开能力。
- 能力矩阵使用 `Object.freeze`，减少运行时误修改风险。

## 验证状态
当前 GitHub Connector 环境未执行完整测试、Web 构建、Android export 与真机验证，不记录为已通过。
