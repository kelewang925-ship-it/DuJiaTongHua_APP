# 稳定开发基线

更新时间：2026-07-14

## 入口与运行方式

- 生产默认入口：`app/index.js` 重定向到 `/diary/detail`。这是当前产品入口，不受 Dev UI 环境变量影响。
- 首次启动入口：`/onboarding`。当前不主动修改首次启动判断或受保护页面业务。
- Mock API：默认 `EXPO_PUBLIC_API_MODE=mock`；真实 API 仅在明确设置 `real` 且 Supabase 环境变量完整时启用。
- Web Dev UI：运行 `npm run web:dev-ui`，脚本仅为该开发进程设置 `EXPO_PUBLIC_DEV_UI=1` 与 Mock API。
- Web 构建检查：运行 `npm run check:web`，输出到已忽略的 `dist/web`。

## 正式路由与兼容别名

| 业务 | 正式路由 | 兼容别名 | 处理方式 |
| --- | --- | --- | --- |
| 相册 | `/photo/album` | `/album` | `Redirect` |
| 评论 | `/comments` | `/interaction/comments` | `Redirect` |
| 通知 | `/notifications` | `/interaction/notifications` | `Redirect` |
| AI 生成进度 | `/ai/progress` | `/ai/generation-progress` | `Redirect` |
| 标签 | `/tags` | `/records/tags` | `Redirect` |
| 时光胶囊 | `/time-capsule/settings` | `/records/time-capsule` | `Redirect` |

正式路由按 `assets/design` 的独立效果图和当前业务实现确定；兼容入口不再维护第二套页面。

## 数据职责与确定性 Mock

- `src/data/mockData.js`：应用与 UI 使用的领域初始数据，是 Zustand 重置后的唯一种子来源。
- `src/api/mockData.js`：API 适配层的接口级返回数据，不负责 UI Store 持久化。
- `src/store/useFairyStore.js`：保存用户在本地交互产生的状态；旧 AsyncStorage 可能覆盖初始种子。
- `src/dev-ui-lab/runtime/mock.js`：仅保存当前开发会话的接口状态切换，不写入生产持久化。
- 一键重置：Dev UI 的 Mock Center 调用 `clearPersistedData()`，清理当前和遗留 Store key 后恢复 `src/data/mockData.js`。

## 图片与大型 SVG 基线

- 单一正式图片注册表：`src/assets/fairyImages.js`；图片 key、用途、正式路径和静态 `require` 均在此维护。
- `FairyImage`、`FairyHeroImage` 从注册表读取，不再维护第二份路径映射。
- `assets/images` 是运行时正式资源区；`assets/design`、`assets/design-assets`、`assets/page-effects` 是参考或阶段产物区。
- 当前盘点：`assets` 共 360 个文件、约 539 MiB；其中 `assets/images` 78 个、约 91 MiB。
- 大型 SVG 迁移候选：`FairyIllustration` 及其在 `FeaturePage`、`FairyHeroImage`、`FairyEmptyState`、`MemoryCard`、主 Tab 页中的 fallback 使用。页面进入批次时，若其承担主视觉，替换为正式位图；小型功能图标继续使用 Ionicons 或 `FairySvgIcon`。
- 不在阶段 0 批量移动或删除既有资源；每次迁移先扫描所有静态引用，再构建验证。

## 高风险共享基础设施

- `app/_layout.js`：全局字体、图标字体保护、SafeAreaProvider、AuthGate、路由错误边界。
- `src/components/FairyPage.js`：顶部 Safe Area、滚动头部模糊与阴影。
- `src/components/FairyTabBar.js` 与 `FairyPage tabSafe`：底部导航和页面内容避让必须一起检查。
- `src/components/AuthGate.js`：正式鉴权与 Dev UI 例外。
- `src/assets/fairyImages.js`：正式图片注册表。

共享基础设施只做向后兼容调整；页面视觉优先使用页面级样式或可选属性。2026-07-17 首页批次已为 `FairyTabBar` 叠加移动端 `insets.bottom`，Web 的 bottom inset 继续维持为 0；实际手势区效果保留为 Android/iOS 人工验证项。

## 构建产物和日志

- `dist/`、`build-check-*/`、`debug.log` 已加入忽略规则。
- 当前 `build-check-empty-state/` 是上一轮 Web 静态导出，四个 `debug.log` 是 Chromium crashpad 日志。
- 阶段 0 发现仍有 Node 进程运行，未删除这些在途文件；确认相关进程不再使用后再清理。
- 项目当前没有 lint、test 或 typecheck 脚本；不能把未配置的检查写成已通过。每批至少执行 Web export、`git diff --check`、新增 DOM API 扫描和浏览器冒烟检查。

## 错误隔离

`app/_layout.js` 导出 Expo Router `ErrorBoundary`，单页运行错误会展示可重试的温和错误页，避免整个开发流程只剩白屏。开发环境显示错误消息，生产环境只展示用户友好文案。
