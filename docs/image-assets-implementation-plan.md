# 《独家童话》图片资产拆分 / 重新生成实施计划

> 任务状态：已纳入项目计划  
> 任务类型：视觉资产落地 / 高保真还原 / 图片资产库建设  
> 关联目录：`assets/images/illustrations/`  
> 关联组件：`src/components/FairyImage.js`  
> 关联规范：`docs/image-assets-guideline.md`、`docs/《独家童话》Design System v1.0.md`、`docs/《独家童话》UI设计总方向.md`

---

## 1. 任务背景

当前项目已经建立了 `FairyImage` 作为统一图片入口，并且首页、情侣空间、童话工坊已经接入：

```text
homeCover      → app/(tabs)/index.js
coupleCover    → app/(tabs)/couple.js
workshopCover  → app/(tabs)/workshop.js
```

但目前这些图片入口仍然使用 `FairyIllustration` fallback，因为项目中还没有从效果图拆分出来的独立 PNG/WebP 插画资源。

当前 `assets/design/png/` 下的文件：

```text
界面设计图.png
界面设计图2.png
界面设计风格图-2.png
```

属于整块效果展示图，不能直接放入 App 页面。正确做法是：

1. 从效果图中拆分局部插画；或
2. 根据效果图和设计规范重新生成独立插画；
3. 放入 `assets/images/illustrations/`；
4. 在 `FairyImage.js` 中维护映射；
5. 在页面中继续通过 `FairyImage name="xxx"` 使用。

---

## 2. 任务目标

建立项目专属插画资产库，让页面视觉从“SVG fallback / 组件模拟”升级为“真实 AI 绘本插画 + 组件化 UI”。

目标包括：

- 提升首页、情侣空间、童话工坊的视觉还原度；
- 让效果图中的 AI 配图真正进入项目；
- 避免直接引用整块大图；
- 建立可维护、可替换、可压缩的图片资产流程；
- 为后续所有页面插画、空状态图、贴纸图建立统一规范。

---

## 3. 本阶段范围

本阶段只处理核心三张插画：

| 映射名 | 目标文件 | 使用页面 | 说明 |
| --- | --- | --- | --- |
| `homeCover` | `assets/images/illustrations/home-cover-v1.png` | `app/(tabs)/index.js` | 首页 Hero 插画，表现恋爱绘本、回忆碎片、拍立得和贴纸。 |
| `coupleCover` | `assets/images/illustrations/couple-space-cover-v1.png` | `app/(tabs)/couple.js` | 情侣空间 Hero 插画，表现双人宇宙、爱心轨道、时间线和花朵贴纸。 |
| `workshopCover` | `assets/images/illustrations/workshop-cover-v1.png` | `app/(tabs)/workshop.js` | 童话工坊 Hero 插画，表现魔法工坊、绘本、漫画分镜和回忆放映机。 |

不在本阶段处理：

- 所有页面的完整插画替换；
- 用户生成图；
- AI 结果图；
- 贴纸资产库；
- PDF 封面；
- 分享图模板；
- 远程 CDN 图片。

---

## 4. 资产来源方式

### 方式 A：从效果图中拆分

适用情况：

- 效果图中已有清晰独立插画；
- 插画没有被多个页面遮挡；
- 裁切后边缘完整；
- 分辨率足够用于移动端展示。

处理步骤：

1. 打开 `assets/design/png/界面设计图.png` 和 `界面设计图2.png`；
2. 找到首页、情侣空间、童话工坊对应区域；
3. 裁切对应 Hero 插画；
4. 清理多余界面元素；
5. 必要时补透明或奶油纸背景；
6. 导出为 PNG；
7. 压缩体积；
8. 放入 `assets/images/illustrations/`。

优点：

- 与现有效果图最一致；
- 还原成本低。

缺点：

- 可能分辨率不足；
- 可能裁到 UI 元素；
- 后续扩展性一般。

---

### 方式 B：根据效果图重新生成

适用情况：

- 效果图是整块展示，无法干净裁切；
- 插画需要更高分辨率；
- 需要统一风格；
- 需要后续可持续生成同系列资产。

生成要求：

- 风格必须与 Design System 一致；
- 不要偏科技 AI；
- 不要高饱和粉色；
- 不要复杂大场景；
- 保持留白；
- 适合放入移动端 Hero 卡片中。

推荐尺寸：

```text
1200 × 900
```

最终进入项目前可压缩到：

```text
1024 × 768 或 900 × 675
```

---

## 5. 三张核心插画生成提示词

### 5.1 首页 Hero 插画

```text
一对情侣的恋爱绘本打开在奶油纸背景上，周围有小爱心、星星、胶带贴纸、拍立得照片角标、手写日记纸片，柔和桃粉和干玫瑰色，可可棕手绘线条，少量琥珀金点缀，温柔治愈，轻手绘童话绘本风，适合情侣情感记录APP首页Hero插画，留白充足，移动端UI插画，不要高饱和，不要科技风，不要真实照片风
```

建议文件名：

```text
assets/images/illustrations/home-cover-v1.png
```

---

### 5.2 情侣空间 Hero 插画

```text
两个人的小小宇宙，情侣头像、爱心轨道、双人故事时间线、花朵贴纸和星星点缀，奶油纸质感背景，桃粉、干玫瑰、琥珀金，可可棕手绘线条，温柔童话绘本风，像一本恋爱故事书里的插画，适合情侣空间页面Hero插画，留白充足，移动端UI插画，不要赛博科技感，不要复杂背景
```

建议文件名：

```text
assets/images/illustrations/couple-space-cover-v1.png
```

---

### 5.3 童话工坊 Hero 插画

```text
温柔的AI魔法工坊，打开的绘本、魔法棒、星光、漫画分镜卡片、回忆放映机和小贴纸，奶油纸质感背景，桃粉、干玫瑰、琥珀金点缀，可可棕线条，轻手绘童话绘本风，不要赛博科技感，不要蓝紫粒子风，适合AI创作页面Hero插画，留白充足，移动端UI插画
```

建议文件名：

```text
assets/images/illustrations/workshop-cover-v1.png
```

---

## 6. 接入步骤

### 6.1 创建目录

确认目录存在：

```text
assets/images/illustrations/
```

如不存在，需要创建。

---

### 6.2 放入图片

将三张图片放入：

```text
assets/images/illustrations/home-cover-v1.png
assets/images/illustrations/couple-space-cover-v1.png
assets/images/illustrations/workshop-cover-v1.png
```

---

### 6.3 修改 `FairyImage.js`

在 `src/components/FairyImage.js` 中打开图片映射：

```js
const imageSourceMap = {
  homeCover: require('../../assets/images/illustrations/home-cover-v1.png'),
  coupleCover: require('../../assets/images/illustrations/couple-space-cover-v1.png'),
  workshopCover: require('../../assets/images/illustrations/workshop-cover-v1.png'),
};
```

并将当前 fallback 分支改为真实 `Image` 渲染：

```js
<Image source={source} resizeMode="contain" style={styles.image} />
```

注意：

- fallback 仍要保留；
- 图片缺失时不能导致页面崩溃；
- 所有页面继续使用 `FairyImage`，不要直接散落 `Image require`。

---

## 7. 验收标准

### 7.1 文件验收

- [ ] `assets/images/illustrations/home-cover-v1.png` 存在；
- [ ] `assets/images/illustrations/couple-space-cover-v1.png` 存在；
- [ ] `assets/images/illustrations/workshop-cover-v1.png` 存在；
- [ ] 图片不是整块效果图裁切残留；
- [ ] 图片尺寸适合移动端；
- [ ] 单张图片体积建议控制在 300KB - 800KB 内；
- [ ] 图片命名符合规范。

### 7.2 代码验收

- [ ] `FairyImage.js` 中已配置三张图片映射；
- [ ] 首页仍使用 `<FairyImage name="homeCover" />`；
- [ ] 情侣空间仍使用 `<FairyImage name="coupleCover" />`；
- [ ] 童话工坊仍使用 `<FairyImage name="workshopCover" />`；
- [ ] 图片缺失时 fallback 不崩溃；
- [ ] 页面不直接写散落的 `require('../../assets/...')`。

### 7.3 视觉验收

- [ ] 首页 Hero 插画与“恋爱绘本 / 回忆记录”主题一致；
- [ ] 情侣空间插画与“双人宇宙 / 故事线”主题一致；
- [ ] 童话工坊插画与“AI魔法 / 漫画 / 视频”主题一致；
- [ ] 三张插画颜色统一；
- [ ] 三张插画都符合奶油纸感、桃粉、干玫瑰、可可棕、琥珀金体系；
- [ ] 不出现强科技风、真实照片风、低幼卡通风；
- [ ] 与 `assets/design/png/界面设计风格图-2.png` 中的设计风格一致。

---

## 8. 文档记录要求

完成图片生成或拆分后，必须更新：

```text
docs/image-assets-guideline.md
```

追加记录格式：

```markdown
### YYYY-MM-DD 图片处理记录

- 处理类型：新增 / 替换 / 压缩 / 裁切 / 接入 / 删除
- 资产路径：`assets/images/illustrations/home-cover-v1.png`
- 来源：AI生成 / 设计稿切图 / 手绘 / 用户上传 / 临时占位
- 使用页面：`app/(tabs)/index.js`
- 组件：`src/components/FairyImage.js`
- 尺寸：宽 × 高
- 格式：PNG / WebP
- 说明：
- 后续待办：
```

同时需要更新：

```text
docs/project-file-structure.md
```

说明新增图片文件和 `FairyImage` 映射关系。

---

## 9. 建议 Codex 执行提示词

```text
请读取 docs/image-assets-implementation-plan.md、docs/image-assets-guideline.md、docs/project-file-structure.md、docs/《独家童话》Design System v1.0.md、docs/《独家童话》UI设计总方向.md。

本次只处理图片资产落地任务：从 assets/design/png/界面设计图.png、界面设计图2.png、界面设计风格图-2.png 中参考或拆分/重新生成三张核心插画：home-cover-v1.png、couple-space-cover-v1.png、workshop-cover-v1.png，并放入 assets/images/illustrations/。

然后修改 src/components/FairyImage.js，将 homeCover、coupleCover、workshopCover 映射到真实 PNG 图片，并保留 fallback。不要改页面结构，不要改业务逻辑，不要直接把整张效果图放入页面。

完成后更新 docs/image-assets-guideline.md 和 docs/project-file-structure.md，记录图片来源、尺寸、路径、使用页面和验收结果。
```

---

## 10. 当前状态

```text
任务已纳入项目计划。
图片规范已建立。
FairyImage 统一入口已建立。
首页 / 情侣空间 / 童话工坊已通过 FairyImage 接入。
真实独立插画文件尚未生成或放入 assets/images/illustrations/。
下一步需要生成或拆分三张核心插画，并打开 FairyImage 的真实图片映射。
```
