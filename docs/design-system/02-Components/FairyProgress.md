# FairyProgress

> 进度组件。像童话书中的故事进度，温暖、有期待感、不焦虑。

---

## 1. 变体

### 1.1 Linear（线性进度条）

```
轨道：bg-sunken, 高度 8px, 圆角 full
进度：bg-pink, 高度 8px, 圆角 full
动画：宽度变化, ease-decelerate
文案：百分比 + 故事化描述
```

### 1.2 Circular（圆形进度）

```
轨道：bg-sunken, 线宽 4px
进度：bg-pink, 线宽 4px
中心：角色图标或百分比
动画：stroke-dashoffset 变化
```

### 1.3 Story（故事进度）

```
视觉：书页翻动动画
进度：当前页码 / 总页码
文案："第 X 章 - 故事正在展开..."
```

---

## 2. 代码实现

```javascript
// src/components/FairyProgress.js
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { semanticColors } from '../theme/colors';
import { radius } from '../theme/layout';

const FairyProgress = ({ progress = 0, total, variant = 'linear', message }) => {
  const percentage = Math.round((progress / total) * 100);

  if (variant === 'linear') {
    return (
      <View style={styles.container}>
        <View style={styles.track}>
          <View style={[styles.fill, { width: `${percentage}%` }]} />
        </View>
        <Text style={styles.text}>{message || `已完成 ${percentage}%`}</Text>
      </View>
    );
  }

  return (
    <View style={styles.circularContainer}>
      {/* SVG Circular Progress */}
      <Text style={styles.percentage}>{percentage}%</Text>
      <Text style={styles.text}>{message}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { width: '100%' },
  track: { height: 8, backgroundColor: semanticColors.bg.sunken, borderRadius: 4, overflow: 'hidden' },
  fill: { height: '100%', backgroundColor: semanticColors.bg.pink, borderRadius: 4 },
  text: { fontSize: 12, color: semanticColors.text.secondary, marginTop: 8, textAlign: 'center' },
  circularContainer: { alignItems: 'center' },
  percentage: { fontSize: 24, fontWeight: '700', color: semanticColors.text.primary },
});

export default FairyProgress;
```
