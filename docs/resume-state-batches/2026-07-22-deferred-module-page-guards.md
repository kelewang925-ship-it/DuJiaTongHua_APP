# 2026-07-22 延迟模块页面请求态守卫

## 根因

`bootstrapApp` 在关系数据完成后会把日记、照片、纪念日、标签、时光胶囊、通知等放入 `loading.modules`，而多个 Real 页面只读取 `loading.bootstrap`。网络较慢时，这些页面会先把尚未返回的数组渲染成 0 条空数据。

## 修复

以下页面现在同时监听 `loading.bootstrap || loading.modules`，并合并 `errors.bootstrap || errors.modules`：

- 情侣空间
- 我的
- 通知
- 搜索
- 标签
- 时光胶囊

新增 `moduleLoadingGuards.static.test.js`，先验证旧实现失败，再验证修复后 7 项通过。

## 运行时观察

当前浏览器会话在重载期间仍可能长时间停留在首页确认加载层；这是第四阶段首屏性能问题。修复保证模块未完成时不展示误导性的 0 数据，但不把网络慢误报为业务成功。
