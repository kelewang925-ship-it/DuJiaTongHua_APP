# 2026-07-17 Realtime 订阅白名单批次

## 范围
- `src/api/realtimeApi.js`
- `src/__tests__/realtimeSubscriptionAllowlist.static.test.js`

## 已完成
- 移除 `table: '*'` 宽泛订阅。
- 对情侣关系及核心业务表建立明确订阅白名单。
- `couples` 使用 `id` 过滤，其余情侣业务表使用 `couple_id` 过滤。
- 通知继续按当前用户 `user_id` 独立订阅。
- 清理函数会停用回调并移除本次创建的全部频道。

## 验证状态
当前环境未执行双账号 Realtime、断线重连、解绑和 Session 切换集成测试，不记录为已通过。
