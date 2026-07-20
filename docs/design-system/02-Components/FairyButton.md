# FairyButton

> 统一的操作按钮组件。像童话书中的魔法按钮，每一次点击都有温柔反馈。

---

## 1. 概述

FairyButton 是《独家童话》的标准按钮组件，用于所有用户操作。它必须提供：

- 一致的视觉风格
- 温柔的按压反馈
- 清晰的状态表达
- 情绪化的加载状态

---

## 2. 变体（Variants）

### 2.1 Primary（主要按钮）

```
背景：bg-pink (桃夭)
文字：text-inverse (白色)
圆角：radius-lg (16px)
高度：52px
内边距：0 20px

状态：
  - Default: 标准桃夭背景
  - Hover: 背景加深到 pink-400
  - Pressed: scale 0.96, 阴影缩小
  - Disabled: 背景 40% 透明度, 文字 60% 透明度
  - Loading: 背景不变, 显示旋转动画 + "正在..."
```

### 2.2 Secondary（次要按钮）

```
背景：bg-secondary (藕丝秋半)
文字：text-primary (可可棕)
边框：1px border-default
圆角：radius-lg (16px)
高度：48px
内边距：0 20px

状态：
  - Default: 标准藕丝背景
  - Hover: 背景加深
  - Pressed: scale 0.96
  - Disabled: 背景 30% 透明度
```

### 2.3 Ghost（幽灵按钮）

```
背景：transparent
文字：text-accent (桃夭深)
圆角：radius-md (12px)
高度：44px
内边距：0 16px

状态：
  - Default: 透明背景
  - Hover: bg-pink-50 (最淡桃粉)
  - Pressed: scale 0.96
```

### 2.4 Text（文字按钮）

```
背景：transparent
文字：text-accent (桃夭深)
下划线：无
高度：40px
内边距：0 12px

状态：
  - Default: 标准强调色
  - Hover: 文字加深
  - Pressed: scale 0.98
```

---

## 3. 尺寸（Sizes）

| 尺寸 | 高度 | 内边距 | 字号 | 用途 |
|------|------|--------|------|------|
| `sm` | 40px | 0 16px | 14px | 小操作、标签内 |
| `md` | 48px | 0 20px | 16px | 标准按钮 |
| `lg` | 52px | 0 24px | 16px | 主要操作、底部固定 |
| `xl` | 56px | 0 28px | 18px | 全宽按钮、CTA |

---

## 4. 状态（States）

### 4.1 五态规范

| 状态 | 视觉表现 | 动效 |
|------|----------|------|
| **Default** | 标准样式 | 无 |
| **Hover** | 背景色加深 10% | 无（移动端无 hover）|
| **Pressed** | scale 0.96, 阴影缩小 | 100ms, standard easing |
| **Disabled** | 40% 透明度, 无阴影 | 无 |
| **Loading** | 背景不变, 显示旋转图标 + 文案 | 旋转动画 800ms loop |
| **Focus** | 外边框 2px border-focus | 无 |

### 4.2 加载状态

```
视觉：
  - 背景保持原色
  - 文字替换为旋转图标 + "正在..."
  - 禁止点击

文案：
  - 保存中："正在把回忆藏进故事书..."
  - 生成中："魔法正在发生..."
  - 提交中："小信使正在送信..."
```

---

## 5. 图标支持

### 5.1 图标位置

```
[图标] 文字      → 左图标（默认）
文字 [图标]      → 右图标
[图标]           → 图标按钮（无文字）
```

### 5.2 图标尺寸

| 按钮尺寸 | 图标尺寸 | 图标与文字间距 |
|----------|----------|----------------|
| sm | 16px | 6px |
| md | 20px | 8px |
| lg | 20px | 8px |
| xl | 24px | 10px |

---

## 6. 动效规范

```
按下：
  - scale: 1.0 → 0.96
  - shadow: 原阴影 → shadow-sm
  - duration: 100ms
  - easing: ease-standard
  - haptics: light

释放：
  - scale: 0.96 → 1.0
  - shadow: shadow-sm → 原阴影
  - duration: 200ms
  - easing: ease-spring

可选反馈：
  - 爱心/星光从按钮中心扩散
  - scale: 0 → 1.2 → 0
  - opacity: 1 → 0
  - duration: 400ms
```

---

## 7. 使用示例

```jsx
// 主要按钮
<FairyButton variant="primary" size="lg" onPress={handleSave}>
  保存回忆
</FairyButton>

// 次要按钮
<FairyButton variant="secondary" size="md">
  再看看
</FairyButton>

// 带图标按钮
<FairyButton variant="primary" iconLeft="fairy-action-add">
  添加日记
</FairyButton>

// 加载状态
<FairyButton variant="primary" loading loadingText="正在把回忆藏进故事书...">
  保存中...
</FairyButton>

// 禁用状态
<FairyButton variant="primary" disabled>
  请先填写内容
</FairyButton>

// 全宽按钮
<FairyButton variant="primary" size="xl" fullWidth>
  开始创作
</FairyButton>
```

---

## 8. 代码实现

```javascript
// src/components/FairyButton.js
import React from 'react';
import { Pressable, Text, ActivityIndicator, StyleSheet } from 'react-native';
import { semanticColors } from '../theme/colors';
import { radius } from '../theme/layout';
import { duration, easing } from '../theme/motion';

const FairyButton = ({
  title,
  variant = 'primary',
  size = 'md',
  onPress,
  disabled = false,
  loading = false,
  loadingText,
  iconLeft,
  iconRight,
  fullWidth = false,
  style,
}) => {
  const isPrimary = variant === 'primary';
  const isSecondary = variant === 'secondary';
  const isGhost = variant === 'ghost';
  const isText = variant === 'text';

  const sizeStyles = {
    sm: { height: 40, paddingHorizontal: 16, fontSize: 14 },
    md: { height: 48, paddingHorizontal: 20, fontSize: 16 },
    lg: { height: 52, paddingHorizontal: 24, fontSize: 16 },
    xl: { height: 56, paddingHorizontal: 28, fontSize: 18 },
  };

  const variantStyles = {
    primary: {
      backgroundColor: semanticColors.bg.pink,
      color: semanticColors.text.inverse,
    },
    secondary: {
      backgroundColor: semanticColors.bg.secondary,
      color: semanticColors.text.primary,
      borderWidth: 1,
      borderColor: semanticColors.border.default,
    },
    ghost: {
      backgroundColor: 'transparent',
      color: semanticColors.text.accent,
    },
    text: {
      backgroundColor: 'transparent',
      color: semanticColors.text.accent,
    },
  };

  return (
    <Pressable
      onPress={onPress}
      disabled={disabled || loading}
      style={({ pressed }) => [
        styles.button,
        sizeStyles[size],
        variantStyles[variant],
        fullWidth && styles.fullWidth,
        pressed && !disabled && !loading && styles.pressed,
        (disabled || loading) && styles.disabled,
        style,
      ]}
    >
      {loading ? (
        <>
          <ActivityIndicator size="small" color={variantStyles[variant].color} />
          <Text style={[styles.text, { color: variantStyles[variant].color, marginLeft: 8 }]}>
            {loadingText || '正在...'}
          </Text>
        </>
      ) : (
        <Text style={[styles.text, { color: variantStyles[variant].color, fontSize: sizeStyles[size].fontSize }]}>
          {title}
        </Text>
      )}
    </Pressable>
  );
};

const styles = StyleSheet.create({
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: radius.lg,
  },
  fullWidth: {
    width: '100%',
  },
  pressed: {
    transform: [{ scale: 0.96 }],
    opacity: 0.9,
  },
  disabled: {
    opacity: 0.4,
  },
  text: {
    fontWeight: '600',
  },
});

export default FairyButton;
```
