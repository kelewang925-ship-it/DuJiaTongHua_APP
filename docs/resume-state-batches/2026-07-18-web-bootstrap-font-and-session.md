# 2026-07-18 Web 启动字体与会话校验修复

## 触发问题

已登录的 A 用户在刷新 Web 页面时，长时间停留在“正在准备你们的童话...”或出现空白页。Metro 服务保持可用，控制台未报告业务运行时异常。

## 修复

- Web 端只注册一次自定义基础字体；原生端继续保留既有字重映射，避免 Web 首次渲染为同一个约 10 MB 字体文件等待重复请求。
- `AuthGate` 将已校验的 `getCurrentSession()` 结果传给 `bootstrapApp`，避免启动时重复执行一次 `auth.getUser()` 校验。
- `bootstrapApp` 保持默认自行校验的行为，认证状态变化等其他调用点不受影响。

## 验证

- `npx jest src/__tests__/rootRoute.static.test.js src/__tests__/fontLoadingFallback.static.test.js --runInBand --ci`：通过（2 suites / 5 tests）。
- `npm run audit:pages`：通过。
- 私有字体资源 `http://localhost:8081/assets/?unstable_path=...ttf`：HTTP 200，10,125,356 bytes。
- Chrome 自动化在刷新后读取页面 DOM 超时，未将其作为浏览器验收通过；需由 A 用户在最新代码下常规刷新一次，确认能在合理时间内进入首页。

## 后续

- 若仍出现启动异常，优先记录 AuthGate / Supabase 请求的实际失败响应；不要继续以重启或强刷替代根因证据。
