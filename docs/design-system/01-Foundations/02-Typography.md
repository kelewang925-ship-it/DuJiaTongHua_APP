# Fairy 排版系统

> 文字是《独家童话》的叙事载体。排版系统确保每一段文字都像绘本中的手写体一样有温度、有节奏、有层次。

---

## 1. 设计哲学

### 1.1 字体情绪

《独家童话》的排版追求**"手写日记感"**：

- **温暖**：像恋人在日记本上写下的字迹
- **清晰**：保证移动端可读性，不牺牲功能
- **节奏**：通过字号、字重、行高建立视觉韵律
- **手绘感**：标题允许轻微不规则，正文保持规整

### 1.2 字体选择

| 层级 | 字体族 | 风格 | 用途 |
|------|--------|------|------|
| 标题字体 | `PingFang SC` / 系统圆体 | 无衬线、圆润 | 页面标题、模块标题 |
| 正文字体 | `PingFang SC` / `Noto Sans SC` | 无衬线、清晰 | 正文、说明、标签 |
| 数字字体 | `DIN Alternate` / 系统等宽 | 等宽、简洁 | 日期、时间、计数 |
| 装饰字体 | 手写体（未来扩展） | 手写、活泼 | 特殊标题、节日文案 |

> 💡 当前阶段使用系统字体，未来可引入自定义字体文件。

---

## 2. 字号阶梯（Type Scale）

基于 4px 基准网格，建立 8 级字号阶梯。

### 2.1 字号表

| Token | 字号 | 行高 | 字重 | 用途 | 中文适配 |
|-------|------|------|------|------|----------|
| `display` | 32px | 40px | 700 (Bold) | 页面大标题、空状态标题 | 适当加宽字距 |
| `h1` | 24px | 32px | 700 (Bold) | 页面标题、模块标题 | 适当加宽字距 |
| `h2` | 20px | 28px | 600 (SemiBold) | 卡片标题、章节标题 | 标准字距 |
| `h3` | 16px | 24px | 600 (SemiBold) | 小标题、列表标题 | 标准字距 |
| `body` | 14px | 22px | 400 (Regular) | 正文、描述 | 标准字距 |
| `body-lg` | 16px | 26px | 400 (Regular) | 大段正文、日记内容 | 标准字距 |
| `caption` | 12px | 18px | 400 (Regular) | 辅助说明、时间戳 | 标准字距 |
| `overline` | 10px | 14px | 500 (Medium) | 标签、徽章文字 | 适当加宽字距 |

### 2.2 特殊排版规则

#### 标题装饰
- **允许轻微旋转**：`-1° ~ 1°`，打破机械网格感
- **允许字距调整**：标题字距 `+0.02em`，增加呼吸感
- **禁止**：正文旋转、正文负字距

#### 正文规范
- **最小字号**：12px（caption），禁止更小
- **行高下限**：≥ 1.5（中文需要更多行高）
- **段间距**：`1em`（等于当前字号）
- **对齐**：中文正文左对齐，英文数字允许居中

#### 数字与日期
- **等宽显示**：日期、时间使用等宽字体
- **千分位**：大数字使用逗号分隔（如 1,234）
- **日期格式**：YYYY.MM.DD 或 MM月DD日，统一风格

---

## 3. 字重规范（Font Weight）

| 字重 | Token | 用途 | 注意 |
|------|-------|------|------|
| 400 | `regular` | 正文、说明 | 最常用，保证可读性 |
| 500 | `medium` | 按钮文字、标签 | 轻微强调，不刺眼 |
| 600 | `semibold` | 标题、选中项 | 清晰但不沉重 |
| 700 | `bold` | 大标题、关键数字 | 少量使用，避免视觉噪音 |

> ⚠️ 禁止使用 100/200/300（过细，移动端可读性差）和 800/900（过重，破坏温柔感）。

---

## 4. 行高与段落

### 4.1 行高规则

| 场景 | 行高倍数 | 说明 |
|------|----------|------|
| 标题 | 1.25 ~ 1.33 | 紧凑但不拥挤 |
| 正文 | 1.5 ~ 1.57 | 中文舒适阅读行高 |
| 大段文字 | 1.6 ~ 1.75 | 日记、长文本 |
| 标签/按钮 | 1.0 ~ 1.2 | 单行文字，垂直居中 |

### 4.2 段落间距

```
段落间距 = 当前字号 × 1.0（即 1em）
列表项间距 = 当前字号 × 0.75
标题与正文间距 = 标题字号 × 0.75
```

---

## 5. 文字颜色与对比度

文字颜色必须使用语义 Token，禁止硬编码。

| 场景 | 颜色 Token | 最小对比度 |
|------|-----------|-----------|
| 主标题 | `text-primary` | 7:1 |
| 正文 | `text-primary` | 7:1 |
| 辅助说明 | `text-secondary` | 4.5:1 |
| 占位符 | `text-tertiary` | 3:1 |
| 深色背景文字 | `text-inverse` | 7:1 |
| 可点击文字 | `text-accent` | 4.5:1 |

---

## 6. 特殊文本样式

### 6.1 情绪化文案样式

| 场景 | 样式 | 示例 |
|------|------|------|
| 成功反馈 | `text-accent` + 小图标 | ❤️ 回忆已收藏 |
| 安慰文案 | `text-secondary` + 斜体 | 没关系，明天又是新的一天~ |
| 神秘预告 | `text-gold` + 闪烁动画 | ✨ 独角兽正在孵化... |
| 加载文案 | `text-secondary` + 逐字动画 | 魔法画笔正在涂色... |

### 6.2 标签与徽章

```
标签文字：caption (12px) + medium (500)
徽章文字：overline (10px) + medium (500) + 全大写（英文）
按钮文字：body (14px) + semibold (600) 或 medium (500)
```

---

## 7. 排版模式

### 7.1 页面标题模式

```
[返回按钮]  [页面标题 - h1, 24px, bold]
            [副标题 - caption, 12px, secondary]（可选）
```

### 7.2 卡片标题模式

```
[卡片标题 - h2, 20px, semibold]
[辅助说明 - caption, 12px, secondary]
[内容 - body, 14px, regular]
```

### 7.3 空状态文案模式

```
[插画]
[标题 - h2, 20px, semibold, 可旋转 -1°]
[描述 - body, 14px, secondary]
[操作按钮]
```

---

## 8. AI 生成规则

1. **先选字号**：根据内容层级选择 Token，禁止随意使用 15px、17px 等非标准值
2. **保证行高**：中文正文行高 ≥ 1.5
3. **控制字重**：正文不用 bold，标题不用 regular
4. **检查对比度**：文字与背景对比度 ≥ 4.5:1
5. **预留字体**：使用 `fontFamily: 'System'` 而非具体字体名，便于未来替换

---

## 9. 代码实现

```javascript
// src/theme/typography.js
export const fontFamily = {
  heading: 'System',      // 未来替换为自定义字体
  body: 'System',
  mono: 'Courier',        // 数字等宽
};

export const fontSize = {
  display: 32,
  h1: 24,
  h2: 20,
  h3: 16,
  body: 14,
  bodyLg: 16,
  caption: 12,
  overline: 10,
};

export const lineHeight = {
  display: 40,    // 1.25
  h1: 32,         // 1.33
  h2: 28,         // 1.4
  h3: 24,         // 1.5
  body: 22,       // 1.57
  bodyLg: 26,     // 1.625
  caption: 18,    // 1.5
  overline: 14,   // 1.4
};

export const fontWeight = {
  regular: '400',
  medium: '500',
  semibold: '600',
  bold: '700',
};

export const typographyStyles = {
  display: {
    fontSize: fontSize.display,
    lineHeight: lineHeight.display,
    fontWeight: fontWeight.bold,
    letterSpacing: 0.02,
  },
  h1: {
    fontSize: fontSize.h1,
    lineHeight: lineHeight.h1,
    fontWeight: fontWeight.bold,
    letterSpacing: 0.01,
  },
  h2: {
    fontSize: fontSize.h2,
    lineHeight: lineHeight.h2,
    fontWeight: fontWeight.semibold,
    letterSpacing: 0,
  },
  h3: {
    fontSize: fontSize.h3,
    lineHeight: lineHeight.h3,
    fontWeight: fontWeight.semibold,
    letterSpacing: 0,
  },
  body: {
    fontSize: fontSize.body,
    lineHeight: lineHeight.body,
    fontWeight: fontWeight.regular,
    letterSpacing: 0,
  },
  bodyLg: {
    fontSize: fontSize.bodyLg,
    lineHeight: lineHeight.bodyLg,
    fontWeight: fontWeight.regular,
    letterSpacing: 0,
  },
  caption: {
    fontSize: fontSize.caption,
    lineHeight: lineHeight.caption,
    fontWeight: fontWeight.regular,
    letterSpacing: 0,
  },
  overline: {
    fontSize: fontSize.overline,
    lineHeight: lineHeight.overline,
    fontWeight: fontWeight.medium,
    letterSpacing: 0.04,
  },
};
```
