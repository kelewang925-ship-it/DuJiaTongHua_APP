# 2026-07-18 Real 首页情侣关系空值修复

## 范围

- 分支：`codex/phase2-real-data`
- 起点：`52c3c70965b2ebf8dd8b5100f81d4f3f92d0760e`
- 类型：真实云端联调缺陷修复，不扩展第二阶段功能
- 未修改：`main`、Supabase 001–006、`docs/resume-state.md`、第三阶段计划

## 根因

`app/(tabs)/index.js` 把 Store 的 `couple` 当作 Mock 扁平对象，直接读取 `couple.loveDays`、`couple.statusText`、`couple.spaceName`。Real Store 实际保存 `getCoupleInfo()` 的可空包装对象 `{ user, partner, couple, status }`，因此首次加载、Realtime 刷新、Session 切换或未绑定状态会出现 `couple === null` 并触发崩溃。

## 修复

- 新增 `src/utils/homeRelationshipView.js`，统一派生 Mock 与 Real 首页关系视图。
- Real 模式只读取 `coupleState?.couple`、真实用户/伴侣昵称和关系状态。
- 恋爱天数仅从合法 `startedAt` 派生；缺失、非法或未来日期返回 `null`。
- Real 模式不回退 Mock 的空间名、状态文案或恋爱天数。
- 首页接入 `loading.bootstrap`、`errors.bootstrap` 与 `refreshCoreData`。
- 未绑定或关系瞬态为空时展示安全空状态和 `/account/invite` 入口。
- 已绑定但资料不完整时展示“未提供”类真实空状态。

## 400 / 重复提交审查

`bind-confirm.js` 原有 `submitting` state 能阻止重渲染后的重复点击，但无法同步阻止同一渲染帧内的双击；并且绑定 RPC 成功、Store 刷新失败后，错误页重试会再次调用绑定 RPC。

本批新增：

- `submissionLock` 同步 ref 锁，阻止同帧重复请求。
- `bindingConfirmed` 标记服务端已确认关系。
- 绑定成功但刷新失败后，重试仅调用 `loadCoreData({ force: true })`，不会再次调用 `bindCoupleByCode`。

因此代码层已没有已知的重复绑定 RPC 路径。服务端仍应通过 006 的锁和 active 检查提供最终幂等/并发保护。

## 测试

新增：

- `src/__tests__/homeRelationshipView.test.js`
  - Real `couple=null`
  - Real active 包装对象
  - 未绑定包装对象
  - 缺失、非法、未来 `startedAt`
  - Mock 扁平对象行为保持
- `src/__tests__/homeRealDataShape.static.test.js`
  - 首页不直接读取 Mock 专用字段
  - 加载、失败重试和邀请入口
  - Real 模式不回退 Mock 文案
  - 同步提交锁
  - 绑定已确认后只重试刷新

## 验证状态

当前执行环境克隆仓库失败：`Could not resolve host: github.com`。

以下命令未运行：

- `npm run test:final`
- `npm run check:web`
- `npx expo export --platform android --output-dir dist/android-check`
- `npm run audit:pages`
- `npm run audit:real`
- `npm run audit:real-pages`
- `npm run audit:api`
- `git diff main...HEAD --check`

Codex 应在最终 HEAD 上执行上述门禁，并在 Real 双账号环境复验绑定成功后的首页、Realtime 刷新、Session 切换和 Store 刷新失败重试。
