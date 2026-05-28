# 《独家童话》剩余图片生成提示词

> 用途：当前已生成的大部分图片已经接入或进入接入流程，本文件只保留仍缺失的图片资产提示词。  
> 使用方式：打开新的图片生成对话，上传 `assets/design/png/界面设计图.png`、`界面设计图2.png`、`界面设计风格图-2.png` 作为风格参考，然后按本文档逐张生成。

---

## 1. 统一风格要求

所有图片必须符合：

```text
童话绘本风格，奶油纸质感，柔和桃粉、干玫瑰、可可棕、琥珀金点缀，轻手绘线条，贴纸感，温柔治愈，留白充足，适合情侣情感记录 App，不要高饱和，不要科技蓝紫风，不要真实照片风，不要低幼卡通，不要复杂背景，不要出现真实文字，不要出现品牌 Logo。
```

---

## 2. 仍需生成图片清单

```text
assets/images/illustrations/empty-ai-history-v1.png
assets/images/stickers/tape-cream-v1.png
assets/images/stickers/polaroid-corner-v1.png
assets/images/backgrounds/cream-paper-texture-v1.png
assets/images/backgrounds/soft-pink-gradient-v1.png
assets/images/covers/anniversary-share-cover-v1.png
```

---

## 3. 逐张生成提示词

### 3.1 AI 创作历史空状态

目标文件：

```text
assets/images/illustrations/empty-ai-history-v1.png
```

规格：

```text
800 × 600，PNG 或 WebP
```

提示词：

```text
一个安静的 AI 魔法工坊空桌面，奶油纸背景上有一本合上的小绘本、魔法棒、几颗星星和空白漫画分镜卡片，桃粉、干玫瑰、可可棕、琥珀金点缀，轻手绘童话绘本风，表达“还没有 AI 作品，等待第一段回忆被施展魔法”，留白充足，不要文字，不要 logo，不要科技蓝紫风
```

---

### 3.2 奶油色胶带贴纸

目标文件：

```text
assets/images/stickers/tape-cream-v1.png
```

规格：

```text
512 × 512，PNG 透明背景
```

提示词：

```text
透明背景，一段半透明奶油色纸胶带贴纸，带轻微纸张纹理，可可棕极细描边，温柔手账风，适合贴在恋爱绘本卡片边缘，512×512，PNG透明背景，不要文字，不要logo
```

---

### 3.3 拍立得角标贴纸

目标文件：

```text
assets/images/stickers/polaroid-corner-v1.png
```

规格：

```text
512 × 512，PNG 透明背景
```

提示词：

```text
透明背景，一个手绘拍立得照片角标贴纸，奶油白纸质感，可可棕细线，少量桃粉小爱心和琥珀金星星点缀，适合情侣相册和回忆墙装饰，512×512，PNG透明背景，不要文字，不要logo
```

---

### 3.4 月白纸感背景

目标文件：

```text
assets/images/backgrounds/cream-paper-texture-v1.png
```

规格：

```text
1600 × 2400，PNG 或 WebP
```

提示词：

```text
浅奶油白月白纸张纹理背景，柔和细腻，有轻微纸纤维和温暖颗粒感，低对比度，适合移动端情侣童话绘本App页面背景，1600×2400，不能有文字、logo、明显图案，不要高饱和
```

---

### 3.5 柔和桃粉渐变背景

目标文件：

```text
assets/images/backgrounds/soft-pink-gradient-v1.png
```

规格：

```text
1600 × 2400，PNG 或 WebP
```

提示词：

```text
柔和桃粉到奶油白的渐变背景，带非常轻微纸张纹理和温暖光晕，低饱和，适合移动端情侣童话绘本App的卡片背景或分享背景，1600×2400，不要文字，不要logo，不要复杂图案
```

---

### 3.6 纪念日分享封面

目标文件：

```text
assets/images/covers/anniversary-share-cover-v1.png
```

规格：

```text
1080 × 1440，PNG 或 WebP
```

提示词：

```text
一张适合情侣纪念日分享的竖版童话卡片封面，奶油纸背景，中心是打开的纪念册、日历小图标、干玫瑰花、丝带、爱心和星星贴纸，桃粉、干玫瑰、可可棕、琥珀金点缀，温柔治愈，留白充足，1080×1440，不要文字，不要logo
```

---

## 4. 新对话直接使用提示词

```text
我要继续为《独家童话》生成剩余项目图片资产。当前项目大部分 Hero 插画、空状态图、贴纸和封面已经生成并接入，现在只需要补齐以下 6 张图片：

1. empty-ai-history-v1.png
2. tape-cream-v1.png
3. polaroid-corner-v1.png
4. cream-paper-texture-v1.png
5. soft-pink-gradient-v1.png
6. anniversary-share-cover-v1.png

请参考我上传的效果图：界面设计图.png、界面设计图2.png、界面设计风格图-2.png。

统一风格：童话绘本、奶油纸感、柔和桃粉、干玫瑰、可可棕、琥珀金、轻手绘线条、贴纸感、温柔治愈、留白充足。不要高饱和，不要科技蓝紫风，不要真实照片风，不要低幼卡通，不要复杂背景，不要出现真实文字，不要出现品牌 Logo。

请按 docs/remaining-image-generation-prompts.md 的逐张提示词生成，并保持整体风格统一。
```
