# FairyBadge

> 徽标组件。像手账中的奖励贴纸，小巧、醒目、有成就感。

---

## 1. 变体

### 1.1 类型

| 类型 | 样式 | 用途 |
|------|------|------|
| `dot` | 小圆点 | 新消息、未读 |
| `number` | 数字 | 消息数量 |
| `text` | 文字 | 状态标签 |

### 1.2 颜色

| 颜色 | 背景 | 用途 |
|------|------|------|
| `error` | state-error | 错误、紧急 |
| `warning` | state-warning | 提醒 |
| `success` | state-success | 完成 |
| `primary` | bg-pink | 默认 |
| `gold` | bg-gold | VIP、成就 |

---

## 2. 代码实现

```javascript
// src/components/FairyBadge.js
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const FairyBadge = ({ type = 'dot', count, text, color = 'error', style }) => {
  if (type === 'dot') {
    return <View style={[styles.dot, { backgroundColor: colorMap[color] }, style]} />;
  }

  return (
    <View style={[styles.badge, { backgroundColor: colorMap[color] }, style]}>
      <Text style={styles.text}>
        {type === 'number' ? (count > 99 ? '99+' : count) : text}
      </Text>
    </View>
  );
};

const colorMap = {
  error: '#E8A090',
  warning: '#E8C97A',
  success: '#8FBC8F',
  primary: '#F6BEC8',
  gold: '#D8B384',
};

const styles = StyleSheet.create({
  dot: { width: 8, height: 8, borderRadius: 4 },
  badge: {
    minWidth: 18,
    height: 18,
    borderRadius: 9,
    paddingHorizontal: 5,
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: { color: '#FFFFFF', fontSize: 10, fontWeight: '600' },
});

export default FairyBadge;
```
