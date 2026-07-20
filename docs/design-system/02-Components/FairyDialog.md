# FairyDialog

> 弹窗组件。像童话书中的插页，温柔地询问、确认、提醒。

---

## 1. 结构

```
FairyDialog
├── 遮罩层（半透明）
├── 弹窗卡片
│   ├── 插画（可选，80-120px）
│   ├── 标题（h2, 20px）
│   ├── 描述（body, 14px）
│   ├── 操作按钮组
│   │   ├── 主要操作（FairyButton primary）
│   │   └── 次要操作（FairyButton ghost）
│   └── 关闭按钮（可选）
```

---

## 2. 类型

| 类型 | 插画 | 按钮 | 用途 |
|------|------|------|------|
| `confirm` | 小精灵 | 确认/取消 | 普通确认 |
| `destructive` | 伤心小熊 | 删除/保留 | 删除确认 |
| `alert` | 小信使 | 知道了 | 提醒 |
| `celebrate` | 小精灵撒星星 | 庆祝/分享 | 成功庆祝 |

---

## 3. 情绪化文案

| 场景 | 系统文案 | Fairy 文案 |
|------|----------|------------|
| 删除日记 | 确定删除？不可恢复 | 要把这段回忆悄悄藏进小黑屋吗？ |
| 退出编辑 | 未保存，确定退出？ | 故事还没写完，真的要离开吗？ |
| 解除绑定 | 确定解除情侣关系？ | 真的要解开这条红线吗？ |

---

## 4. 动效

```
出现：
  - 遮罩 opacity 0 → 0.4 (250ms)
  - 弹窗 scale 0.92 → 1.0, translateY 20px → 0 (300ms, spring)

消失：
  - 弹窗 scale 1.0 → 0.95, opacity 1 → 0 (200ms)
  - 遮罩 opacity 0.4 → 0 (200ms)
```

---

## 5. 代码实现

```javascript
// src/components/FairyDialog.js
import React from 'react';
import { Modal, View, Text, Pressable, StyleSheet } from 'react-native';
import { semanticColors } from '../theme/colors';
import { radius, shadows, spacing } from '../theme/layout';
import FairyButton from './FairyButton';

const FairyDialog = ({ visible, type = 'confirm', title, description, primaryText, secondaryText, onPrimary, onSecondary, onClose }) => {
  return (
    <Modal visible={visible} transparent animationType="fade">
      <View style={styles.overlay}>
        <View style={styles.dialog}>
          <Text style={styles.title}>{title}</Text>
          <Text style={styles.description}>{description}</Text>
          <View style={styles.buttons}>
            {secondaryText && (
              <FairyButton variant="ghost" size="md" onPress={onSecondary} style={styles.button}>
                {secondaryText}
              </FairyButton>
            )}
            <FairyButton variant="primary" size="md" onPress={onPrimary} style={styles.button}>
              {primaryText}
            </FairyButton>
          </View>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: semanticColors.surface.overlay,
    alignItems: 'center',
    justifyContent: 'center',
    padding: spacing.xl,
  },
  dialog: {
    backgroundColor: semanticColors.bg.tertiary,
    borderRadius: radius.xl,
    padding: spacing.xl,
    width: '100%',
    maxWidth: 320,
    ...shadows.xl,
  },
  title: { fontSize: 20, fontWeight: '600', color: semanticColors.text.primary, textAlign: 'center', marginBottom: spacing.sm },
  description: { fontSize: 14, color: semanticColors.text.secondary, textAlign: 'center', marginBottom: spacing.lg },
  buttons: { flexDirection: 'row', justifyContent: 'center', gap: spacing.sm },
  button: { flex: 1 },
});

export default FairyDialog;
```
