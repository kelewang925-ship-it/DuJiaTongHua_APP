# FairyTag

> 小巧的标签组件。像手账中的贴纸标签，可爱、醒目、有分类感。

---

## 1. 概述

FairyTag 用于标记内容类型、情绪状态、AI 状态等。它必须：

- 小巧精致，不喧宾夺主
- 色彩丰富但柔和
- 支持多种语义色调
- 可删除、可选中

---

## 2. 变体（Variants）

### 2.1 色调变体

| 变体 | 背景 | 文字 | 用途 |
|------|------|------|------|
| `default` | bg-pink | text-accent | 默认标签 |
| `gold` | bg-gold | text-gold | VIP、成就、重要 |
| `success` | state-success 20% | state-success | 完成、成功 |
| `warning` | state-warning 20% | state-warning | 提醒、注意 |
| `error` | state-error 20% | state-error | 错误、危险 |
| `info` | state-info 20% | state-info | 提示、新功能 |
| `mood` | 根据情绪变化 | 对应深色 | 心情标签 |

### 2.2 尺寸变体

| 尺寸 | 高度 | 内边距 | 字号 | 圆角 |
|------|------|--------|------|------|
| `sm` | 24px | 4px 10px | 10px | full |
| `md` | 28px | 6px 12px | 12px | full |
| `lg` | 32px | 8px 14px | 12px | full |

---

## 3. 状态

| 状态 | 表现 |
|------|------|
| **Default** | 标准样式 |
| **Selected** | 边框变为 2px border-focus |
| **Disabled** | 30% 透明度 |

---

## 4. 使用示例

```jsx
<FairyTag>日记</FairyTag>
<FairyTag tone="gold">VIP</FairyTag>
<FairyTag tone="success">已完成</FairyTag>
<FairyTag tone="mood" mood="happy">开心</FairyTag>
<FairyTag closable onClose={() => {}}>可删除</FairyTag>
```
