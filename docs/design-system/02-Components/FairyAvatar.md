# FairyAvatar

> 情侣头像组件。像童话书中的角色肖像，温暖、有辨识度、有状态表达。

---

## 1. 变体

### 1.1 尺寸

| 尺寸 | 大小 | 用途 |
|------|------|------|
| `xs` | 32px | 列表内、紧凑场景 |
| `sm` | 40px | 评论、小卡片 |
| `md` | 48px | 标准头像 |
| `lg` | 64px | 个人资料页 |
| `xl` | 80px | 大资料页、设置页 |

### 1.2 形状

| 形状 | 圆角 | 用途 |
|------|------|------|
| `circle` | full | 默认，人物头像 |
| `rounded` | 12px | 角色头像、插画 |
| `square` | 8px | 特殊场景 |

### 1.3 状态指示器

| 状态 | 指示器 | 位置 |
|------|--------|------|
| 在线 | 绿色圆点 | 右下角 |
| 离线 | 灰色圆点 | 右下角 |
| 忙碌 | 黄色圆点 | 右下角 |
| 情侣关联 | 小爱心 | 右下角 |

---

## 2. 代码实现

```javascript
// src/components/FairyAvatar.js
import React from 'react';
import { View, Image, StyleSheet } from 'react-native';

const FairyAvatar = ({ source, size = 'md', shape = 'circle', status, style }) => {
  const sizeMap = { xs: 32, sm: 40, md: 48, lg: 64, xl: 80 };
  const s = sizeMap[size];

  return (
    <View style={[styles.container, { width: s, height: s }, style]}>
      <Image
        source={source}
        style={[
          styles.image,
          { width: s, height: s, borderRadius: shape === 'circle' ? s/2 : shape === 'rounded' ? 12 : 8 }
        ]}
      />
      {status && (
        <View style={[styles.status, { backgroundColor: statusColors[status] }]} />
      )}
    </View>
  );
};

const statusColors = {
  online: '#8FBC8F',
  offline: '#C4A898',
  busy: '#E8C97A',
  couple: '#F6BEC8',
};

const styles = StyleSheet.create({
  container: { position: 'relative' },
  image: { borderWidth: 2, borderColor: '#FFF9F4' },
  status: {
    position: 'absolute',
    bottom: 0,
    right: 0,
    width: 12,
    height: 12,
    borderRadius: 6,
    borderWidth: 2,
    borderColor: '#FFFFFF',
  },
});

export default FairyAvatar;
```
