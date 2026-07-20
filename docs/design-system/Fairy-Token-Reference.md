# Fairy Token 参考

## 颜色 Token

主色：

- fairyPink
- roseDust

中性色：

- creamPaper
- moonWhite

文本：

- cocoaBrown
- softCocoa

强调色：

- amberGold

## 间距 Token

使用 4px 基准间距。

- xs: 4
- sm: 8
- md: 12
- lg: 16
- xl: 24
- xxl: 32
- xxxl: 48

## 圆角 Token

- small: 8
- medium: 16
- large: 24
- fairy: 32

## 阴影 Token

纸张阴影：

用于卡片和容器。

浮层阴影：

用于重要操作。

## 代码规则

优先使用主题 token。

避免硬编码值：

```js
color: '#EFA7B8'
```

推荐：

```js
colors.fairyPink
```
