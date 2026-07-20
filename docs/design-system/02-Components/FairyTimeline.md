# FairyTimeline

> 时间线组件。像童话书中的故事线，记录爱情的每一个里程碑。

---

## 1. 概述

FairyTimeline 用于展示：
- 恋爱时间线
- 纪念日序列
- 回忆里程碑
- 成长轨迹

---

## 2. 结构

```
FairyTimeline
├── TimelineItem
│   ├── 节点（圆点/图标）
│   ├── 连接线
│   ├── 日期
│   ├── 标题
│   ├── 描述
│   └── 媒体（可选）
└── 当前节点高亮
```

---

## 3. 节点类型

| 类型 | 图标 | 颜色 | 用途 |
|------|------|------|------|
| `milestone` | 星星 | gold | 重要里程碑 |
| `memory` | 爱心 | pink | 美好回忆 |
| `anniversary` | 礼物 | rose | 纪念日 |
| `daily` | 圆点 | cocoa | 日常记录 |
| `future` | 独角兽 | accent | 未来计划 |

---

## 4. 代码实现

```javascript
// src/components/FairyTimeline.js
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { semanticColors } from '../theme/colors';
import { spacing } from '../theme/layout';

const FairyTimeline = ({ items }) => {
  return (
    <View style={styles.container}>
      {items.map((item, index) => (
        <TimelineItem
          key={index}
          {...item}
          isLast={index === items.length - 1}
        />
      ))}
    </View>
  );
};

const TimelineItem = ({ date, title, description, type, isLast }) => {
  const nodeColors = {
    milestone: '#D8B384',
    memory: '#F6BEC8',
    anniversary: '#B08A8F',
    daily: '#8B7355',
    future: '#A0C4E8',
  };

  return (
    <View style={styles.item}>
      <View style={styles.left}>
        <View style={[styles.node, { backgroundColor: nodeColors[type] }]} />
        {!isLast && <View style={styles.line} />}
      </View>
      <View style={styles.right}>
        <Text style={styles.date}>{date}</Text>
        <Text style={styles.title}>{title}</Text>
        {description && <Text style={styles.description}>{description}</Text>}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { paddingVertical: spacing.md },
  item: { flexDirection: 'row', marginBottom: spacing.lg },
  left: { width: 32, alignItems: 'center' },
  node: { width: 16, height: 16, borderRadius: 8, borderWidth: 2, borderColor: '#FFFFFF' },
  line: { width: 2, flex: 1, backgroundColor: semanticColors.border.divider, marginTop: 4 },
  right: { flex: 1, paddingLeft: spacing.sm },
  date: { fontSize: 12, color: semanticColors.text.secondary, marginBottom: 2 },
  title: { fontSize: 16, fontWeight: '600', color: semanticColors.text.primary },
  description: { fontSize: 14, color: semanticColors.text.secondary, marginTop: 4 },
});

export default FairyTimeline;
```
