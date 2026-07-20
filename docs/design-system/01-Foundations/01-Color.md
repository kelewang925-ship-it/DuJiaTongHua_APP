# Fairy 色彩系统

> 色彩是《独家童话》视觉语言的基石。本规范定义了从基础色板到语义化 Token 的完整体系，确保全 App 色彩一致、可访问、可扩展。

---

## 1. 设计哲学

### 1.1 色彩情绪

《独家童话》的色彩源自**童话绘本**与**手账日记**的质感：

- **温暖**：像午后阳光透过窗帘的色调
- **柔和**：拒绝高饱和冲击，追求奶油般的温润
- **层次**：通过明度变化而非色相跳跃建立层次
- **故事感**：每种颜色都有名字，像童话里的角色

### 1.2 色彩比例（黄金法则）

任何页面必须遵循以下色彩比例：

```
70% 奶油纸色 / 背景色（月白、乳白）
20% 柔和桃粉 / 干玫瑰（桃夭、藕丝秋半）
10% 可可棕线条 / 琥珀金点缀（枯玫瑰、琥珀金）
```

> ⚠️ AI 生成 UI 时必须自检此比例，禁止打破平衡。

---

## 2. 基础色板（Primitive Colors）

基础色板定义色相、饱和度、明度的精确值，不直接使用于 UI，而是通过语义色板引用。

### 2.1 桃夭系列（Pink）

| Token | 色值 | 名称 | 情绪 |
|-------|------|------|------|
| `pink-50` | `#FEF2F4` | 桃夭浅 | 最淡的桃粉，用于悬停背景 |
| `pink-100` | `#FCE7EB` | 桃夭淡 | 标签背景、轻量高亮 |
| `pink-200` | `#FAD0D8` | 桃夭柔 | 卡片背景、选中状态 |
| `pink-300` | `#F6BEC8` | **桃夭** ⭐ | 主色，按钮、强调 |
| `pink-400` | `#DFA0AC` | 桃夭深 | 按下状态、深强调 |
| `pink-500` | `#C98A96` | 桃夭浓 | 文字强调、图标激活 |
| `pink-600` | `#A66D78` | 桃夭暗 | 暗色模式主色 |

### 2.2 藕丝秋半系列（Rose Dust）

| Token | 色值 | 名称 | 情绪 |
|-------|------|------|------|
| `rose-50` | `#FAF4F2` | 藕丝浅 | 最淡的玫瑰，大面积背景 |
| `rose-100` | `#F5EAE6` | 藕丝淡 | 次级卡片背景 |
| `rose-200` | `#E9D7D2` | **藕丝秋半** ⭐ | 次级色，次要按钮 |
| `rose-300` | `#D4BDB6` | 藕丝柔 | 边框、分割线 |
| `rose-400` | `#B08A8F` | **枯玫瑰** ⭐ | 强调色、图标默认 |
| `rose-500` | `#8B6E72` | 枯玫瑰深 | 暗色模式强调 |

### 2.3 月白系列（Cream Paper）

| Token | 色值 | 名称 | 情绪 |
|-------|------|------|------|
| `cream-50` | `#FFFFFF` | 纯白 | 极少数场景，如按钮文字 |
| `cream-100` | `#FFFDF9` | 乳白 | 卡片背景 |
| `cream-200` | `#FDFBF7` | **奶油纸** ⭐ | 页面背景 |
| `cream-300` | `#F8F6F2` | **月白** ⭐ | 标准页面背景 |
| `cream-400` | `#F0EDE6` | 月白深 | 暗色背景、分隔区 |

### 2.4 可可棕系列（Cocoa Brown）

| Token | 色值 | 名称 | 情绪 |
|-------|------|------|------|
| `cocoa-50` | `#C4A898` | 可可浅 | 禁用文字、占位符 |
| `cocoa-100` | `#9B7A7A` | **柔可可** ⭐ | 辅助文字 |
| `cocoa-200` | `#8B7355` | **可可棕** ⭐ | 线条、边框、图标 |
| `cocoa-300` | `#6B4F4F` | **可可棕深** ⭐ | 主文字 |
| `cocoa-400` | `#4A3636` | 可可浓 | 标题、暗色模式文字 |

### 2.5 琥珀金系列（Amber Gold）

| Token | 色值 | 名称 | 情绪 |
|-------|------|------|------|
| `gold-100` | `#F7E8D5` | 琥珀淡 | 标签背景、轻量点缀 |
| `gold-200` | `#D8B384` | **琥珀金** ⭐ | VIP、成就、重点点缀 |
| `gold-300` | `#B8965E` | 琥珀深 | 暗色模式金色 |

### 2.6 功能色系列（Semantic Primitives）

功能色经过"童话滤镜"处理，拒绝冰冷科技感：

| 功能 | Token | 色值 | 童话命名 | 使用场景 |
|------|-------|------|----------|----------|
| 成功 | `success-300` | `#8FBC8F` | 薄荷绿 | 保存成功、完成状态 |
| 成功 | `success-500` | `#6B9E6B` | 薄荷深 | 暗色模式成功 |
| 警告 | `warning-300` | `#E8C97A` | 暖黄 | 提醒、注意 |
| 警告 | `warning-500` | `#C4A55A` | 暖黄深 | 暗色模式警告 |
| 错误 | `error-300` | `#E8A090` | 珊瑚红 | 错误提示、删除确认 |
| 错误 | `error-500` | `#C47A6A` | 珊瑚深 | 暗色模式错误 |
| 信息 | `info-300` | `#A0C4E8` | 天空蓝 | 提示、说明 |
| 信息 | `info-500` | `#7AA0C4` | 天空深 | 暗色模式信息 |

---

## 3. 语义色板（Semantic Colors）

语义色板将基础色映射到具体的 UI 使用场景，是开发时**优先引用**的层级。

### 3.1 背景色（Background）

| Token | 基础色引用 | 使用场景 |
|-------|-----------|----------|
| `bg-primary` | `cream-300` (月白) | 标准页面背景 |
| `bg-secondary` | `cream-200` (奶油纸) | 次级背景、卡片底层 |
| `bg-tertiary` | `cream-100` (乳白) | 卡片背景、浮层 |
| `bg-elevated` | `cream-50` (纯白) | 弹出层、模态框 |
| `bg-sunken` | `cream-400` (月白深) | 输入框背景、暗色区域 |
| `bg-pink` | `pink-200` | 桃粉卡片、选中背景 |
| `bg-gold` | `gold-100` | VIP 标签、成就背景 |

### 3.2 文字色（Text）

| Token | 基础色引用 | 使用场景 | WCAG 对比度 |
|-------|-----------|----------|-------------|
| `text-primary` | `cocoa-300` | 主标题、正文 | ≥ 7:1 |
| `text-secondary` | `cocoa-100` | 辅助说明、时间戳 | ≥ 4.5:1 |
| `text-tertiary` | `cocoa-50` | 占位符、禁用文字 | ≥ 3:1 |
| `text-inverse` | `cream-50` | 深色背景上的文字 | ≥ 7:1 |
| `text-accent` | `pink-400` | 链接、可点击文字 | ≥ 4.5:1 |
| `text-gold` | `gold-200` | VIP 标识、特殊强调 | ≥ 4.5:1 |

### 3.3 边框与分割线（Border）

| Token | 基础色引用 | 使用场景 |
|-------|-----------|----------|
| `border-default` | `rose-300` 18% | 卡片边框、输入框默认 |
| `border-focus` | `pink-300` | 输入框聚焦、选中状态 |
| `border-error` | `error-300` | 表单错误状态 |
| `border-divider` | `rose-200` 30% | 列表分割线 |

### 3.4 表面色（Surface）

| Token | 基础色引用 | 使用场景 |
|-------|-----------|----------|
| `surface-card` | `cream-100` | 标准卡片 |
| `surface-card-pink` | `pink-100` | 桃粉卡片、情绪卡片 |
| `surface-floating` | `cream-50` | FAB、浮动按钮 |
| `surface-overlay` | `cocoa-300` 40% | 遮罩层、弹窗背景 |

### 3.5 状态色（State）

| Token | 基础色引用 | 使用场景 |
|-------|-----------|----------|
| `state-success` | `success-300` | 成功反馈、完成标记 |
| `state-warning` | `warning-300` | 提醒、待处理 |
| `state-error` | `error-300` | 错误、删除、危险操作 |
| `state-info` | `info-300` | 提示、新功能标记 |

---

## 4. 暗色模式（Dark Mode）

暗色模式不是简单的颜色反转，而是**月光下的童话书**——保持温暖感，降低亮度。

### 4.1 暗色映射规则

| 亮色 Token | 暗色映射 | 规则 |
|-----------|----------|------|
| `bg-primary` (月白) | `#2A2520` | 深棕黑，像旧书封面 |
| `bg-secondary` (奶油纸) | `#332D28` | 略浅，保持层次 |
| `bg-tertiary` (乳白) | `#3D3630` | 卡片背景 |
| `text-primary` (可可棕) | `#E8DDD4` | 暖白，像月光 |
| `text-secondary` (柔可可) | `#A89888` | 柔和灰棕 |
| `border-default` | `rose-500` 25% | 暗色边框 |
| `pink-300` (桃夭) | `pink-600` | 降低明度保持饱和 |
| `gold-200` (琥珀金) | `gold-300` | 暗色中更沉稳 |

### 4.2 暗色模式禁用

以下元素在暗色模式中**保持原色或微调**，不反转：

- 插画与角色：保持原色，可加 10% 暗角
- 照片内容：保持原色
- 琥珀金点缀：保持金色，增加发光感

---

## 5. 可访问性（Accessibility）

### 5.1 对比度标准

| 场景 | 最小对比度 | 推荐对比度 |
|------|-----------|-----------|
| 正文文字（< 18px） | 4.5:1 | 7:1 |
| 大标题（≥ 18px bold） | 3:1 | 4.5:1 |
| 图标、按钮 | 3:1 | 4.5:1 |
| 仅装饰元素 | 无要求 | — |

### 5.2 色盲友好

- 错误状态**不仅依赖红色**，必须配合图标（如伤心小熊）
- 成功状态**不仅依赖绿色**，必须配合动画（如小精灵庆祝）
- 信息层级通过**明度差异**而非色相差异建立

---

## 6. AI 生成规则

AI 生成 UI 时必须遵守：

1. **先查 Token**：任何颜色必须使用语义 Token，禁止硬编码 `#F6BEC8`
2. **比例自检**：生成后检查 70/20/10 色彩比例
3. **对比度自检**：文字与背景对比度 ≥ 4.5:1
4. **状态完整**：必须定义 default / hover / pressed / disabled / focus 五态色
5. **暗色预留**：即使当前不做暗色模式，Token 命名需预留 dark 变体

---

## 7. 代码实现

```javascript
// src/theme/colors.js
export const primitiveColors = {
  pink: {
    50: '#FEF2F4', 100: '#FCE7EB', 200: '#FAD0D8',
    300: '#F6BEC8', 400: '#DFA0AC', 500: '#C98A96', 600: '#A66D78',
  },
  rose: {
    50: '#FAF4F2', 100: '#F5EAE6', 200: '#E9D7D2',
    300: '#D4BDB6', 400: '#B08A8F', 500: '#8B6E72',
  },
  cream: {
    50: '#FFFFFF', 100: '#FFFDF9', 200: '#FDFBF7',
    300: '#F8F6F2', 400: '#F0EDE6',
  },
  cocoa: {
    50: '#C4A898', 100: '#9B7A7A', 200: '#8B7355',
    300: '#6B4F4F', 400: '#4A3636',
  },
  gold: {
    100: '#F7E8D5', 200: '#D8B384', 300: '#B8965E',
  },
  semantic: {
    success: { 300: '#8FBC8F', 500: '#6B9E6B' },
    warning: { 300: '#E8C97A', 500: '#C4A55A' },
    error: { 300: '#E8A090', 500: '#C47A6A' },
    info: { 300: '#A0C4E8', 500: '#7AA0C4' },
  },
};

export const semanticColors = {
  bg: {
    primary: primitiveColors.cream[300],
    secondary: primitiveColors.cream[200],
    tertiary: primitiveColors.cream[100],
    elevated: primitiveColors.cream[50],
    sunken: primitiveColors.cream[400],
    pink: primitiveColors.pink[200],
    gold: primitiveColors.gold[100],
  },
  text: {
    primary: primitiveColors.cocoa[300],
    secondary: primitiveColors.cocoa[100],
    tertiary: primitiveColors.cocoa[50],
    inverse: primitiveColors.cream[50],
    accent: primitiveColors.pink[400],
    gold: primitiveColors.gold[200],
  },
  border: {
    default: `${primitiveColors.rose[300]}2E`, // 18% opacity
    focus: primitiveColors.pink[300],
    error: primitiveColors.semantic.error[300],
    divider: `${primitiveColors.rose[200]}4D`, // 30% opacity
  },
  surface: {
    card: primitiveColors.cream[100],
    cardPink: primitiveColors.pink[100],
    floating: primitiveColors.cream[50],
    overlay: `${primitiveColors.cocoa[300]}66`, // 40% opacity
  },
  state: {
    success: primitiveColors.semantic.success[300],
    warning: primitiveColors.semantic.warning[300],
    error: primitiveColors.semantic.error[300],
    info: primitiveColors.semantic.info[300],
  },
};

export const darkColors = {
  bg: {
    primary: '#2A2520',
    secondary: '#332D28',
    tertiary: '#3D3630',
    elevated: '#4A423A',
    sunken: '#1E1A16',
  },
  text: {
    primary: '#E8DDD4',
    secondary: '#A89888',
    tertiary: '#6B5E52',
    inverse: '#2A2520',
    accent: primitiveColors.pink[400],
    gold: primitiveColors.gold[200],
  },
  // ... 其他暗色映射
};
```
