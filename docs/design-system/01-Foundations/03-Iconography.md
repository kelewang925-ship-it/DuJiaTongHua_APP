# Fairy 图标系统

> 图标是《独家童话》视觉语言中最具"手绘感"的元素。每一个图标都应该像手账中的贴纸一样可爱、温暖、有生命力。

---

## 1. 设计哲学

### 1.1 图标情绪

- **手绘感**：允许轻微不规则，拒绝完美几何
- **圆润**：所有端点圆角，线条柔和
- **简洁**：单图标不超过 3 个主要元素
- **统一**：全 App 图标风格一致，像出自同一支画笔

### 1.2 风格关键词

```
手绘线条 · 圆润端点 · 2px 描边 · 线性为主 · 小装饰点缀
```

---

## 2. 图标风格规范

### 2.1 描边规范

| 属性 | 规范 | 说明 |
|------|------|------|
| 笔画粗细 | 2px | 统一粗细，保证一致性 |
| 端点样式 | 圆角 (round cap) | 柔和，无尖锐感 |
| 连接样式 | 圆角 (round join) | 拐角处圆润 |
| 断点 | 允许 1-2 处 | 增加手绘感，但不可过多 |

### 2.2 填充规范

| 场景 | 规范 |
|------|------|
| 默认状态 | 线性描边，无填充 |
| 激活/选中状态 | 可填充主色（桃夭）或强调色（枯玫瑰） |
| 禁用状态 | 描边 30% 透明度 |
| 装饰点缀 | 小星星、小爱心可作为填充装饰 |

### 2.3 视觉修正

- **非对称平衡**：允许左右轻微不对称，增加手绘感
- **视觉重心**：图标重心略偏下，更稳定
- **留白**：图标内部留白 ≥ 20%，不拥挤
- **断点装饰**：断点处可添加小圆点或小星星

---

## 3. 图标尺寸规范

### 3.1 尺寸阶梯

| Token | 尺寸 | 用途 | 笔画粗细 |
|-------|------|------|----------|
| `icon-xs` | 16px | 内联文本、小标签 | 1.5px |
| `icon-sm` | 20px | 按钮内、列表项 | 2px |
| `icon-md` | 24px | 标准图标、导航项 | 2px |
| `icon-lg` | 32px | 功能入口、空状态 | 2.5px |
| `icon-xl` | 48px | 大功能图标、引导页 | 3px |

### 3.2 绘制网格

- **基础网格**：24×24px（标准图标）
- **安全区域**：2px 内边距（实际绘制区域 20×20px）
- **关键线**：中心十字线、对角线、圆形参考线
- **像素对齐**：关键节点对齐像素网格，避免模糊

---

## 4. 图标状态规范

### 4.1 颜色状态

| 状态 | 颜色 Token | 说明 |
|------|-----------|------|
| 默认 | `text-secondary` (柔可可) | 不抢注意力 |
| 激活 | `text-accent` (桃夭深) | 当前选中状态 |
| 禁用 | `text-tertiary` (可可浅) | 不可点击 |
| 错误 | `state-error` (珊瑚红) | 错误提示 |
| 成功 | `state-success` (薄荷绿) | 完成状态 |
| 强调 | `text-gold` (琥珀金) | VIP、特殊功能 |

### 4.2 动效状态

| 交互 | 动效 | 时长 |
|------|------|------|
| 点击 | scale 0.9 → 1.0 + 轻微旋转 ±3° | 150ms |
| 选中 | 填充色从中心扩散 | 200ms |
| 长按 | 轻微放大 1.1 + 震动反馈 | 300ms |
| 新消息 | 轻微摇摆 ±5° 循环 | 800ms |

---

## 5. 图标分类与命名

### 5.1 分类体系

| 分类 | 前缀 | 示例 |
|------|------|------|
| 导航 | `nav-` | nav-home, nav-couple, nav-workshop, nav-mine |
| 操作 | `action-` | action-add, action-edit, action-delete, action-share |
| 状态 | `status-` | status-success, status-error, status-loading, status-empty |
| 内容 | `content-` | content-photo, content-diary, content-comic, content-video |
| 情绪 | `mood-` | mood-happy, mood-sad, mood-love, mood-surprised |
| 装饰 | `deco-` | deco-star, deco-heart, deco-sparkle, deco-flower |

### 5.2 命名规范

```
[fairy]-[分类前缀][具体名称]-[状态/变体]

示例：
- fairy-nav-home-active
- fairy-action-add-default
- fairy-mood-happy-filled
- fairy-deco-sparkle-animated
```

---

## 6. 角色图标系统

### 6.1 角色定义

每个角色有专属图标变体，用于不同场景：

| 角色 | 图标特征 | 使用场景 |
|------|----------|----------|
| **小信使** | 带翅膀的信封 | 通知、消息、网络状态 |
| **魔法画笔** | 带星光的画笔 | AI 创作、加载、生成中 |
| **伤心小熊** | 流泪的小熊 | 删除、错误、空状态 |
| **独角兽** | 带角的小马 | 新功能、彩蛋、VIP |
| **小精灵** | 带翅膀的小人 | 成功、收藏、庆祝 |

### 6.2 角色表情库

每个角色有 4 种表情状态：

- **开心**：眼睛弯弯，嘴角上扬
- **伤心**：眼泪、下垂嘴角
- **惊讶**：大眼睛、O 型嘴
- **睡觉**：闭眼睛、Zzz 符号

---

## 7. 图标使用规则

### 7.1 图标 + 文字组合

```
[图标 20px] [文字 14px, medium]
间距：8px
垂直对齐：居中对齐
```

### 7.2 图标按钮

```
[图标 24px] 或 [图标 20px + 文字]
背景：透明或 bg-tertiary
圆角：12px
内边距：8px 12px
```

### 7.3 图标列表

```
[图标 24px] [标题 16px, semibold]
              [描述 12px, secondary]
间距：图标与文字 12px，标题与描述 4px
```

---

## 8. AI 生成规则

1. **风格一致**：所有图标必须遵循 2px 圆角描边风格
2. **尺寸规范**：使用标准尺寸（16/20/24/32/48），禁止奇数尺寸
3. **颜色使用**：默认使用 `text-secondary`，激活使用 `text-accent`
4. **禁止**：3D 效果、渐变填充、阴影、发光、写实风格
5. **角色优先**：有对应角色场景时，优先使用角色图标

---

## 9. 代码实现

```javascript
// src/theme/icons.js
export const iconSize = {
  xs: 16,
  sm: 20,
  md: 24,
  lg: 32,
  xl: 48,
};

export const iconStroke = {
  xs: 1.5,
  sm: 2,
  md: 2,
  lg: 2.5,
  xl: 3,
};

export const iconColor = {
  default: 'text-secondary',
  active: 'text-accent',
  disabled: 'text-tertiary',
  error: 'state-error',
  success: 'state-success',
  emphasis: 'text-gold',
};

// 图标命名规范
export const iconNames = {
  navigation: {
    home: 'fairy-nav-home',
    couple: 'fairy-nav-couple',
    workshop: 'fairy-nav-workshop',
    mine: 'fairy-nav-mine',
  },
  action: {
    add: 'fairy-action-add',
    edit: 'fairy-action-edit',
    delete: 'fairy-action-delete',
    share: 'fairy-action-share',
    favorite: 'fairy-action-favorite',
  },
  mood: {
    happy: 'fairy-mood-happy',
    sad: 'fairy-mood-sad',
    love: 'fairy-mood-love',
    surprised: 'fairy-mood-surprised',
    sleepy: 'fairy-mood-sleepy',
  },
  character: {
    messenger: 'fairy-char-messenger',
    brush: 'fairy-char-brush',
    bear: 'fairy-char-bear',
    unicorn: 'fairy-char-unicorn',
    fairy: 'fairy-char-fairy',
  },
};
```
