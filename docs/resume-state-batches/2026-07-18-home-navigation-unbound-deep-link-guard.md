# 2026-07-18 首页统计导航与未绑定深链守卫

## 触发证据

第二阶段 A/B/C 实际联调发现：

1. 首页的日记、照片数量是展示卡片，点击不会进入对应内容页。
2. C 已登录但尚未绑定；手动访问业务 URL 时未被导向邀请码页，页面持续处于初始化加载状态。
3. B 能读取 A 上传的私有照片；B 尝试删除时由服务端拒绝，提示“照片集不存在、无权限或已被删除”。

## 本批修复

- 首页四张统计卡改为可访问的 `Pressable`：日记、照片、作品、纪念日分别跳转至对应页面；原有数量计算和视觉卡片内容保持不变。
- `AuthGate` 在 Real 模式的会话 bootstrap 成功后检查情侣关系。已登录但未绑定的用户若直接访问任意业务深链，统一 `replace('/account/invite')`。
- 根入口、邀请码页和绑定确认页保留为未绑定用户可进入的引导路径；已绑定用户与未登录用户原有分流不变。
- 新增静态回归测试，覆盖首页日记/照片统计导航与未绑定用户的深链重定向条件。

## 验证

- 当前提交 `e1e64a2` 的 `npm run test:final`：通过；完整 Jest 套件与其后的四项审计链均以成功状态结束。
- `src/__tests__/homeStatsNavigation.static.test.js`、`src/__tests__/rootRoute.static.test.js`：2 suites、6 tests 通过。
- `npm run audit:pages`：通过（44 条路由，13 个布局/重定向/开发包装文件排除）。
- `npm run audit:real`：18 项能力检查通过。
- `npm run audit:real-pages`：12 条关键路由检查通过。
- `npm run audit:api`：13 个 API 模块契约检查通过。
- `npm run check:web`：通过。
- Android export 生成了 196 个文件，`git diff --check` 通过。
- `EXPO_PUBLIC_API_MODE=mock` 的 Web export 通过，并生成 `index.html`；本批未改变 Mock/Real 隔离约束。
- 仍需在 C 的实际会话中验证“任意业务 URL → 邀请码页”的最终可视路由结果。

## 未改变的边界

- 非上传者照片删除按钮的可见性按产品决定记录到第四阶段，不在本批降低作者删除 API、RLS 或 Storage 所有者约束。
- C 的业务数据访问仍须以真实 C 会话完成 RLS/Storage 拒绝测试；本批只修复前端深链分流。
- 本检查点不代表 Android 真机或完整 A/B/C 权限矩阵完成。
