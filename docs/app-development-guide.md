# 《独家童话》App 开发指南

> 文档说明：本文档是《独家童话》App 的前端开发指南，用于说明技术栈、目录规则、代码风格、当前主路由、UI 一致性检查项和后续工程能力建设方向。

## 目标

使用 React Native、Expo 和 JavaScript 构建同时支持 iOS 与 Android 的移动端 App。

## 技术栈

- React Native
- Expo
- Expo Router
- JavaScript
- React Native SVG
- Expo Linear Gradient
- Zustand，用于后续状态管理

## 目录规则

- `app`：路由页面和页面栈。
- `src/components`：可复用视觉组件。
- `src/theme`：设计 token，包括颜色、间距、字体、阴影等。
- `src/screens`：当某个路由页面过大时，可拆分复杂页面实现。
- `assets/design`：设计参考图、效果图和设计稿。
- `docs`：产品、设计、开发和交接文档。

## 代码风格

- 页面文件保持清晰、可读、模块化。
- 优先使用项目自定义组件，不优先引入通用 UI 组件库。
- 页面颜色应尽量来自 `src/theme/colors.js`。
- 所有主页面使用温暖纸感背景。
- 内容区块优先使用 `FairyCard`。
- 文案可以有情绪价值，但要克制，不要过度煽情。

## 当前主要路由

- `app/(tabs)/index.js`：首页 / 记录中心。
- `app/(tabs)/couple.js`：情侣空间。
- `app/(tabs)/workshop.js`：童话工坊。
- `app/(tabs)/mine.js`：我的。
- `app/diary/editor.js`：日记编辑器。
- `app/anniversary/index.js`：纪念日列表。
- `app/ai/comic-config.js`：AI 漫画配置页。

## UI 一致性检查清单

完成任意页面前，需要检查：

- 页面背景是否使用 `#F8F6F2` 或对应主题背景色。
- 主要卡片是否使用暖纸色或浅桃粉卡片。
- 文本是否使用可可棕色系。
- 强调色是否使用干玫瑰或琥珀金。
- 圆角是否足够柔和。
- 页面是否保留足够留白。
- AI 页面是否更像“温柔魔法”，而不是冰冷科技工具。
- 情侣页面是否有私密感，而不是社交平台信息流。

## 后续工程能力需求

- 增加本地状态 store。
- 增加 mock 数据层。
- 增加页面跳转行为。
- 增加表单校验。
- 接入图片选择能力。
- 增加数据持久化。
- 增加 API client。
- 增加认证流程。
- 接入真实设计图片资产。
