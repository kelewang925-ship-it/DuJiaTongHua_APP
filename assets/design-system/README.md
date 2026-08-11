# DuJiaTongHua Design System Asset Library

本目录是《独家童话》的设计系统资产索引与交付规范。它只记录和组织资产，不自动移动或复制现有 `assets/` 文件。

## 目录用途

- `backgrounds/`：纸张纹理、渐变和页面背景。
- `illustrations/`：登录、引导、日记、情侣、工坊和空状态插画。
- `stickers/`：爱心、花朵、星星、胶带和拍立得装饰。
- `decorations/`：边框、角标、阴影和线条装饰。
- `icons/`：导航、操作和情绪图标。
- `components/`：组件相关的视觉资产与导出参考。
- `pages/`：页面级资产映射，说明页面使用哪些资产。
- `metadata/`：机器可读资产清单、Figma 映射和导出规则。

## 图片命名规范

使用小写 kebab-case：`{semantic-name}-{variant}-v{number}.{ext}`。

示例：`cream-paper-texture-v1.png`、`heart-sticker-v1.png`、`home-cover-v1.png`。

禁止使用 `final.png`、`new.png`、`test2.png` 等无语义名称。变更视觉内容时递增版本号，不覆盖已有版本。

## 尺寸规范

- Hero / Cover 插画：优先保持原始比例，建议长边不低于 1200 px。
- Sticker：建议 `512×512`，透明 PNG。
- Background Texture：建议 `1080×1920` 或可平铺纹理。
- Icon：建议 `24×24`、`32×32` 或 `48×48`，透明 PNG/SVG。
- 导出前不得改变主体比例、透明边缘或颜色。

## Figma Assets 映射规则

Figma 中的 Asset Key 必须与 `metadata/assets.json` 的 `id` 一致。Reference 中只引用 Asset Key，不直接复制一份新图片。图片应作为 Image Layer 使用，组件只负责布局、状态和交互。

## React Native 引用规则

代码引用使用项目实际路径，例如：`assets/images/stickers/heart-sticker-v1.png`。本目录中的分类目录是资产交付索引，不替代现有资源目录；在未完成迁移前，禁止修改 import 路径或移动源文件。

