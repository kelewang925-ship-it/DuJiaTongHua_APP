# 2026-07-17 Realtime 状态真值批次

## 范围
- `src/api/realtimeApi.js`
- `src/__tests__/realtimeStatusTruth.static.test.js`

## 已完成
- 统一识别 `SUBSCRIBED`、`CHANNEL_ERROR`、`TIMED_OUT` 与 `CLOSED`。
- 状态回调明确返回 `connected`、`failed` 和错误对象。
- 情侣空间与通知频道使用同一状态归一化逻辑。
- 取消订阅后旧频道状态不再回调。

## 验证状态
未执行 Supabase Realtime 在线、断网、重连、多账号和设备级测试。