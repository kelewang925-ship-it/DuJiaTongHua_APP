# FairyInput

> 统一的输入体验。像在手账本上书写，温暖、有引导、有反馈。

---

## 1. 变体

### 1.1 Standard（标准输入）

```
背景：bg-sunken
圆角：radius-sm (8px)
高度：48px
内边距：0 16px
边框：1px border-default

聚焦：border-focus + shadow-sm glow
错误：border-error + 伤心小熊图标
```

### 1.2 TextArea（多行输入）

```
最小高度：80px
最大高度：200px
行高：1.6
可滚动
```

### 1.3 Search（搜索输入）

```
左侧：搜索图标
右侧：清除按钮（有内容时显示）
圆角：radius-md (12px)
```

---

## 2. 状态

| 状态 | 表现 |
|------|------|
| **Default** | 标准样式 |
| **Focus** | 边框 focus 色 + 轻微 glow |
| **Error** | 边框 error 色 + 错误文案 |
| **Disabled** | 40% 透明度 |
| **Filled** | 标准样式（有内容时）|

## 3. 情绪化文案

| 场景 | 系统文案 | Fairy 文案 |
|------|----------|------------|
| 必填 | 此项必填 | 这里需要填写哦~ |
| 太短 | 长度不能少于6位 | 我们的暗号太短啦，再多写几个字吧 |
| 格式错误 | 格式不正确 | 小信使看不懂这个格式呢 |
| 密码弱 | 密码强度不足 | 这个暗号太简单啦，换个复杂点的吧 |

---

## 4. 代码实现

```javascript
// src/components/FairyInput.js
import React, { useState } from 'react';
import { TextInput, View, Text, StyleSheet } from 'react-native';
import { semanticColors } from '../theme/colors';
import { radius, spacing, shadows } from '../theme/layout';

const FairyInput = ({
  label,
  placeholder,
  value,
  onChangeText,
  error,
  errorText,
  multiline = false,
  disabled = false,
  style,
}) => {
  const [focused, setFocused] = useState(false);

  return (
    <View style={style}>
      {label && <Text style={styles.label}>{label}</Text>}
      <TextInput
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        multiline={multiline}
        editable={!disabled}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        style={[
          styles.input,
          multiline && styles.textArea,
          focused && styles.focused,
          error && styles.error,
          disabled && styles.disabled,
        ]}
        placeholderTextColor={semanticColors.text.tertiary}
      />
      {error && errorText && (
        <Text style={styles.errorText}>{errorText}</Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  label: {
    fontSize: 14,
    fontWeight: '500',
    color: semanticColors.text.primary,
    marginBottom: spacing.xs,
  },
  input: {
    height: 48,
    backgroundColor: semanticColors.bg.sunken,
    borderRadius: radius.sm,
    paddingHorizontal: spacing.lg,
    borderWidth: 1,
    borderColor: semanticColors.border.default,
    fontSize: 16,
    color: semanticColors.text.primary,
  },
  textArea: {
    height: 80,
    minHeight: 80,
    maxHeight: 200,
    paddingTop: spacing.sm,
    lineHeight: 26,
  },
  focused: {
    borderColor: semanticColors.border.focus,
    ...shadows.sm,
  },
  error: {
    borderColor: semanticColors.border.error,
  },
  errorText: {
    fontSize: 12,
    color: semanticColors.state.error,
    marginTop: spacing.xs,
  },
  disabled: {
    opacity: 0.4,
  },
});

export default FairyInput;
```
