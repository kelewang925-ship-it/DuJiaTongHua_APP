# FairyEmptyState

> 空状态组件。像翻开一本空白的故事书，温柔引导，不让人失落。

---

## 1. 结构

```
FairyEmptyState
├── 插画/角色（120-160px）
├── 标题（h2, 20px, semibold）
├── 描述（body, 14px, secondary）
└── 操作按钮（可选）
```

---

## 2. 场景配置

| 场景 | 角色 | 标题 | 描述 | 按钮 |
|------|------|------|------|------|
| 无日记 | 伤心小熊 | 这里还没有故事呢 | 来写第一篇日记吧~ | 写日记 |
| 无照片 | 伤心小熊 | 相册还是空的 | 去添加一些美好瞬间吧~ | 添加照片 |
| 无网络 | 小信使 | 小信使迷路了 | 检查一下网络，再试一次吧~ | 重试 |
| 无收藏 | 小精灵 | 书架还是空的 | 去收藏一些回忆吧~ | 去浏览 |
| 无通知 | 小信使 | 没有新消息 | 小信使会第一时间通知你~ | — |
| 搜索无结果 | 独角兽 | 独角兽也没找到 | 换个关键词试试？ | — |

---

## 3. 代码实现

```javascript
// src/components/FairyEmptyState.js
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { semanticColors } from '../theme/colors';
import { spacing } from '../theme/layout';
import FairyButton from './FairyButton';

const FairyEmptyState = ({ character, title, description, actionText, onAction }) => {
  return (
    <View style={styles.container}>
      <View style={styles.character}>{/* 角色插画 */}</View>
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.description}>{description}</Text>
      {actionText && (
        <FairyButton variant="primary" size="md" onPress={onAction} style={styles.button}>
          {actionText}
        </FairyButton>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: spacing.xl,
  },
  character: { width: 140, height: 140, marginBottom: spacing.lg },
  title: { fontSize: 20, fontWeight: '600', color: semanticColors.text.primary, marginBottom: spacing.sm },
  description: { fontSize: 14, color: semanticColors.text.secondary, textAlign: 'center', marginBottom: spacing.lg },
  button: { marginTop: spacing.md },
});

export default FairyEmptyState;
```
