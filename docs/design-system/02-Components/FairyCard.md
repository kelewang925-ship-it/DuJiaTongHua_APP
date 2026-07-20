# FairyCard

> 统一的内容容器。像童话书中的书页，温暖、有质感、有层次。

---

## 1. 概述

FairyCard 是《独家童话》的标准卡片组件，用于承载各类内容。它必须提供：

- 一致的纸张质感
- 清晰的层级表达
- 温柔的交互反馈
- 灵活的内容适配

---

## 2. 变体（Variants）

### 2.1 Standard（标准卡片）

```
背景：bg-tertiary (乳白)
圆角：radius-lg (16px)
内边距：space-lg (16px)
阴影：shadow-md
边框：1px border-default

用途：日记卡片、照片卡片、通用内容
```

### 2.2 Pink（桃粉卡片）

```
背景：bg-pink (桃粉)
圆角：radius-lg (16px)
内边距：space-lg (16px)
阴影：shadow-md
边框：1px border-default

用途：情绪卡片、选中状态、特殊内容
```

### 2.3 Elevated（浮起卡片）

```
背景：bg-tertiary (乳白)
圆角：radius-xl (20px)
内边距：space-xl (20px)
阴影：shadow-lg
边框：无

用途：重要内容、推荐、Featured
```

### 2.4 Compact（紧凑卡片）

```
背景：bg-tertiary (乳白)
圆角：radius-md (12px)
内边距：space-md (12px)
阴影：shadow-sm
边框：1px border-default

用途：列表项、标签、小内容
```

---

## 3. 状态（States）

| 状态 | 视觉表现 | 动效 |
|------|----------|------|
| **Default** | 标准样式 | 无 |
| **Pressed** | scale 0.98, 阴影缩小 | 150ms, standard |
| **Selected** | 边框变为 border-focus, 可选桃粉背景 | 200ms, spring |
| **Disabled** | 40% 透明度 | 无 |
| **Loading** | 骨架屏动画 | shimmer 效果 |

---

## 4. 结构规范

```
FairyCard
├── Header（可选）
│   ├── 图标/头像
│   ├── 标题
│   └── 操作按钮
├── Media（可选）
│   └── 图片/视频/插画
├── Content
│   ├── 标题
│   ├── 描述
│   └── 标签组
├── Footer（可选）
│   ├── 元信息（时间、地点）
│   └── 操作按钮组
└── 装饰元素（可选）
    └── 贴纸、角标、手绘线条
```

---

## 5. 使用示例

```jsx
// 标准卡片
<FairyCard>
  <FairyCard.Content>
    <Text style={typography.h3}>今天的日记</Text>
    <Text style={typography.body}>今天和他一起去看了樱花...</Text>
  </FairyCard.Content>
</FairyCard>

// 桃粉卡片
<FairyCard variant="pink">
  <FairyCard.Content>
    <Text>心情：开心 ❤️</Text>
  </FairyCard.Content>
</FairyCard>

// 带图片卡片
<FairyCard>
  <FairyCard.Media source={photoUri} />
  <FairyCard.Content>
    <Text style={typography.h3}>樱花下的约定</Text>
    <FairyTag tone="gold">纪念日</FairyTag>
  </FairyCard.Content>
  <FairyCard.Footer>
    <Text style={typography.caption}>2026.04.01</Text>
  </FairyCard.Footer>
</FairyCard>
```

---

## 6. 代码实现

```javascript
// src/components/FairyCard.js
import React from 'react';
import { View, StyleSheet } from 'react-native';
import { semanticColors } from '../theme/colors';
import { radius, shadows, spacing } from '../theme/layout';

const FairyCard = ({ children, variant = 'standard', style, onPress }) => {
  const variantStyles = {
    standard: {
      backgroundColor: semanticColors.bg.tertiary,
      borderRadius: radius.lg,
      padding: spacing.lg,
      ...shadows.md,
      borderWidth: 1,
      borderColor: semanticColors.border.default,
    },
    pink: {
      backgroundColor: semanticColors.bg.pink,
      borderRadius: radius.lg,
      padding: spacing.lg,
      ...shadows.md,
      borderWidth: 1,
      borderColor: semanticColors.border.default,
    },
    elevated: {
      backgroundColor: semanticColors.bg.tertiary,
      borderRadius: radius.xl,
      padding: spacing.xl,
      ...shadows.lg,
    },
    compact: {
      backgroundColor: semanticColors.bg.tertiary,
      borderRadius: radius.md,
      padding: spacing.md,
      ...shadows.sm,
      borderWidth: 1,
      borderColor: semanticColors.border.default,
    },
  };

  return (
    <View style={[styles.card, variantStyles[variant], style]}>
      {children}
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    overflow: 'hidden',
  },
});

export default FairyCard;
```
