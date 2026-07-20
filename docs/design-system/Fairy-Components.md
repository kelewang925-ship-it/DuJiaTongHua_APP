# Fairy 组件指南

## FairyButton

用途：

统一的操作按钮组件。

类型：

- primary：重要操作
- secondary：备选操作
- ghost：轻量操作

要求：

- 圆润造型
- 柔和阴影
- 按压反馈
- 支持 loading 状态

示例：

```jsx
<FairyButton type="primary">
  保存回忆
</FairyButton>
```

## FairyDialog

适用于：

- 确认操作
- 破坏性操作
- 重要提醒

结构：

- 插画
- 标题
- 描述
- 操作按钮

## FairyToast

用于轻量反馈。

类型：

- success
- error
- info
- magic

## FairyCard

统一的内容容器。

规则：

- 一致的圆角
- 纸张背景
- 轻柔阴影

## FairyInput

统一的输入体验。

支持：

- 标签
- 辅助说明
- 错误状态
- 单行或多行

## FairyEmptyState

空页面应提供：

- 插画
- 标题
- 描述
- 可选操作

## AI 组件开发规则

创建新组件前：

1. 先检查已有 Fairy 组件。
2. 能扩展已有组件时优先扩展。
3. 新增组件时同步补充文档。
