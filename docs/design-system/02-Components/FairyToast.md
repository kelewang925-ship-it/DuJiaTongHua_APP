# FairyToast

> 轻量反馈组件。像童话书中的旁白，温柔地告诉你发生了什么。

---

## 1. 类型

| 类型 | 图标 | 背景 | 用途 |
|------|------|------|------|
| `success` | 小精灵 | state-success | 操作成功 |
| `error` | 伤心小熊 | state-error | 操作失败 |
| `info` | 小信使 | state-info | 一般提示 |
| `magic` | 魔法画笔 | bg-pink | AI 相关 |

---

## 2. 情绪化文案

| 场景 | 系统文案 | Fairy 文案 |
|------|----------|------------|
| 保存成功 | 保存成功 | ❤️ 回忆已经收藏进故事书 |
| 删除成功 | 删除成功 | 🌙 这段回忆已藏进月光里 |
| 网络错误 | 网络连接失败 | 小信使迷路了，再试一次吧~ |
| AI 完成 | 生成完成 | ✨ 你的童话画好了~ |

---

## 3. 动效

```
出现：
  - translateY: -20px → 0
  - opacity: 0 → 1
  - duration: 250ms
  - easing: ease-decelerate

停留：
  - 2-3 秒（根据文案长度）

消失：
  - translateY: 0 → -20px
  - opacity: 1 → 0
  - duration: 200ms
  - easing: ease-accelerate
```

---

## 4. 代码实现

```javascript
// src/components/FairyToast.js
import React, { useEffect } from 'react';
import { View, Text, StyleSheet, Animated } from 'react-native';
import { semanticColors } from '../theme/colors';
import { radius, spacing } from '../theme/layout';

const FairyToast = ({ visible, type = 'success', message, onHide, duration = 2500 }) => {
  const translateY = new Animated.Value(-20);
  const opacity = new Animated.Value(0);

  useEffect(() => {
    if (visible) {
      Animated.parallel([
        Animated.timing(translateY, { toValue: 0, duration: 250, useNativeDriver: true }),
        Animated.timing(opacity, { toValue: 1, duration: 250, useNativeDriver: true }),
      ]).start();

      const timer = setTimeout(() => {
        Animated.parallel([
          Animated.timing(translateY, { toValue: -20, duration: 200, useNativeDriver: true }),
          Animated.timing(opacity, { toValue: 0, duration: 200, useNativeDriver: true }),
        ]).start(onHide);
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [visible]);

  const bgColors = {
    success: semanticColors.state.success,
    error: semanticColors.state.error,
    info: semanticColors.state.info,
    magic: semanticColors.bg.pink,
  };

  return (
    <Animated.View style={[styles.container, { transform: [{ translateY }], opacity, backgroundColor: bgColors[type] }]}>
      <Text style={styles.text}>{message}</Text>
    </Animated.View>
  );
};

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: 60,
    left: 20,
    right: 20,
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.lg,
    borderRadius: radius.md,
    alignItems: 'center',
    zIndex: 200,
  },
  text: { color: '#FFFFFF', fontSize: 14, fontWeight: '500' },
});

export default FairyToast;
```
