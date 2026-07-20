# Fairy 动效系统

> 动效是《独家童话》的情感放大器。每一个动画都应该像童话书中的翻页一样自然、温暖、有仪式感。

---

## 1. 设计哲学

### 1.1 动效情绪

- **温柔**：像微风拂过书页，不突兀、不刺眼
- **有目的**：每个动画都服务于情感连接或功能引导
- **可预测**：用户能预期动画的结果，减少焦虑
- **有节奏**：像音乐一样有快慢变化，不单调

### 1.2 动效原则

```
1. 增强情感：动画让操作更有温度
2. 引导注意：动画指引用户视线
3. 反馈确认：动画确认操作已生效
4. 缓解等待：加载动画让等待不枯燥
5. 保持克制：禁止过度动画，避免视觉噪音
```

---

## 2. 动画时长（Duration）

### 2.1 时长阶梯

| Token | 时长 | 用途 | 感觉 |
|-------|------|------|------|
| `duration-instant` | 0ms | 无动画，立即响应 | 即时 |
| `duration-fast` | 100ms | 微交互（开关、选中） | 敏捷 |
| `duration-normal` | 200ms | 按钮点击、状态切换 | 流畅 |
| `duration-slow` | 300ms | 弹窗出现、页面转场 | 从容 |
| `duration-slower` | 400ms | 复杂转场、抽屉展开 | 优雅 |
| `duration-loading` | 800-1200ms | 加载动画循环周期 | 舒缓 |

### 2.2 时长使用规则

| 场景 | 推荐时长 | 说明 |
|------|----------|------|
| 按钮按下 | 100-150ms | 快速反馈，不拖沓 |
| 按钮释放 | 200-250ms | 弹性回弹，温柔感 |
| 弹窗出现 | 250-350ms | 有足够时间感知 |
| 弹窗消失 | 200ms | 比出现稍快，符合心理预期 |
| 页面转场 | 300-400ms | 从容但不慢 |
| 列表项进入 | 300ms + 50ms stagger | 错开进入，有节奏感 |
| 加载动画 | 800-1200ms/循环 | 舒缓，不焦虑 |

---

## 3. 缓动曲线（Easing）

### 3.1 标准缓动曲线

| Token | 曲线 | 用途 | 感觉 |
|-------|------|------|------|
| `ease-standard` | `cubic-bezier(0.4, 0.0, 0.2, 1)` | 标准过渡 | 自然流畅 |
| `ease-decelerate` | `cubic-bezier(0.0, 0.0, 0.2, 1)` | 元素出现 | 快速开始，缓慢结束 |
| `ease-accelerate` | `cubic-bezier(0.4, 0.0, 1, 1)` | 元素消失 | 缓慢开始，快速结束 |
| `ease-spring` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | 弹性反馈 | 活泼、有生命力 |
| `ease-overshoot` | `cubic-bezier(0.34, 1.8, 0.64, 1)` | 手绘感反馈 | 轻微 overshoot，像手绘 |
| `ease-linear` | `linear` | 循环动画 | 匀速，如加载旋转 |

### 3.2 缓动使用规则

| 场景 | 推荐缓动 | 说明 |
|------|----------|------|
| 按钮按下 | `ease-standard` | 自然 |
| 按钮释放 | `ease-spring` | 弹性回弹 |
| 弹窗出现 | `ease-decelerate` | 从下方滑入，减速停止 |
| 弹窗消失 | `ease-accelerate` | 加速消失 |
| 页面进入 | `ease-decelerate` | 新书页翻开 |
| 页面退出 | `ease-accelerate` | 旧书页合上 |
| 列表项 | `ease-decelerate` + stagger | 依次出现 |
| 加载旋转 | `ease-linear` | 匀速循环 |
| 心跳/爱心 | `ease-spring` | 弹性放大 |

---

## 4. 组件动效规范

### 4.1 按钮交互

```
按下 (press):
  - scale: 1.0 → 0.96
  - opacity: 1.0 → 0.9
  - duration: 100ms
  - easing: ease-standard

释放 (release):
  - scale: 0.96 → 1.0
  - duration: 200ms
  - easing: ease-spring

可选反馈:
  - 爱心/星光从按钮中心扩散
  - scale: 0 → 1.2 → 0
  - opacity: 1 → 0
  - duration: 400ms
```

### 4.2 弹窗动效

```
出现 (enter):
  - opacity: 0 → 1
  - scale: 0.92 → 1.0
  - translateY: 20px → 0
  - duration: 300ms
  - easing: ease-decelerate

消失 (exit):
  - opacity: 1 → 0
  - scale: 1.0 → 0.95
  - duration: 200ms
  - easing: ease-accelerate

遮罩层:
  - opacity: 0 → 0.4
  - duration: 250ms
  - easing: ease-standard
```

### 4.3 页面转场

```
推荐方式 1 - 书页翻动:
  - 新页面从右侧滑入
  - translateX: 100% → 0
  - opacity: 0.8 → 1
  - duration: 400ms
  - easing: ease-decelerate

推荐方式 2 - 淡入淡出:
  - 旧页面 opacity: 1 → 0
  - 新页面 opacity: 0 → 1
  - duration: 300ms
  - easing: ease-standard

推荐方式 3 - 纸张滑动:
  - 新页面从底部滑入
  - translateY: 100% → 0
  - duration: 350ms
  - easing: ease-decelerate
```

### 4.4 卡片交互

```
按下:
  - scale: 1.0 → 0.98
  - shadow: md → sm
  - duration: 150ms
  - easing: ease-standard

释放:
  - scale: 0.98 → 1.0
  - shadow: sm → md
  - duration: 200ms
  - easing: ease-spring

长按:
  - scale: 1.0 → 1.02
  - shadow: md → lg
  - duration: 300ms
  - easing: ease-spring
  - 触发震动反馈 (haptics)
```

### 4.5 列表加载

```
进入动画:
  - 每个列表项依次出现
  - opacity: 0 → 1
  - translateY: 12px → 0
  - duration: 300ms
  - stagger: 50ms（每个间隔 50ms）
  - easing: ease-decelerate

刷新动画:
  - 顶部出现加载指示器
  - 旋转 + 轻微上下浮动
  - 内容更新时：旧内容淡出，新内容淡入
```

---

## 5. 加载与进度动效

### 5.1 魔法加载（AI 生成场景）

```
视觉:
  - 魔法画笔图标旋转
  - 星光粒子从中心向外扩散
  - 进度条像墨水在纸上晕染

文案:
  - 逐字显示故事化文案
  - "魔法画笔正在悄悄涂色..."
  - "小精灵正在整理你的回忆..."

时长:
  - 循环周期：1000ms
  - 进度更新：每 500ms 一次
```

### 5.2 标准加载

```
视觉:
  - 小信使拍翅膀动画
  - 虚线圈圈旋转

文案:
  - "传信的小信使正在赶路..."

时长:
  - 循环周期：800ms
```

### 5.3 进度条

```
视觉:
  - 背景：奶油色轨道
  - 进度：桃粉色填充
  - 填充动画：ease-decelerate
  - 允许轻微发光效果（glow）

文案:
  - 百分比 + 故事化描述
  - "已完成 60% - 故事即将成型..."
```

---

## 6. 情感动效

### 6.1 成功反馈

```
动画序列:
  1. 小精灵出现 (scale 0 → 1, spring, 300ms)
  2. 撒星星粒子 (从中心向外, 400ms)
  3. 文案淡入 ("回忆已收藏进故事书~", 200ms)
  4. 整体淡出 (500ms delay, 300ms fade)

震动:
  - 轻微成功震动 (haptics: light)
```

### 6.2 错误反馈

```
动画序列:
  1. 伤心小熊出现 (translateY: 10px → 0, 250ms)
  2. 轻微摇晃 (rotate: -3° → 3° → 0, 400ms)
  3. 文案显示 ("小信使迷路了，再试一次吧~")

震动:
  - 错误震动 (haptics: heavy)
```

### 6.3 收藏/爱心

```
双击爱心:
  - 爱心从点击位置放大
  - scale: 0 → 1.3 → 1.0
  - opacity: 0 → 1 → 0.8
  - duration: 400ms
  - easing: ease-spring
  - 粒子向外扩散
```

---

## 7. 无障碍动效

### 7.1 减少动画模式

```
当用户开启系统"减少动态效果"时：

- 所有转场：opacity 切换，无位移
- 所有时长：≤ 100ms
- 循环动画：禁用或替换为静态图标
- 弹性效果：禁用，使用 linear
- 错开动画：禁用，同时出现
```

### 7.2 屏幕阅读器适配

```
- 动画开始/结束时播报状态变化
- 不依赖动画传达关键信息
- 加载状态必须有文字说明
```

---

## 8. AI 生成规则

1. **时长控制**：微交互 ≤ 200ms，转场 ≤ 400ms，加载 800-1200ms
2. **缓动选择**：出现用 decelerate，消失用 accelerate，反馈用 spring
3. **减少动画**：必须支持 prefers-reduced-motion
4. **禁止**：高频闪烁（> 3Hz）、无限循环（除加载外）、突然跳变
5. **情感优先**：加载动画必须有故事化文案，禁止 "Loading..."
6. **反馈完整**：每个操作必须有视觉反馈，不能无声无息

---

## 9. 代码实现

```javascript
// src/theme/motion.js
export const duration = {
  instant: 0,
  fast: 100,
  normal: 200,
  slow: 300,
  slower: 400,
  loading: 1000,
};

export const easing = {
  standard: [0.4, 0.0, 0.2, 1],
  decelerate: [0.0, 0.0, 0.2, 1],
  accelerate: [0.4, 0.0, 1, 1],
  spring: [0.34, 1.56, 0.64, 1],
  overshoot: [0.34, 1.8, 0.64, 1],
  linear: [0, 0, 1, 1],
};

export const animationPresets = {
  buttonPress: {
    scale: 0.96,
    opacity: 0.9,
    duration: duration.fast,
    easing: easing.standard,
  },
  buttonRelease: {
    scale: 1.0,
    opacity: 1.0,
    duration: duration.normal,
    easing: easing.spring,
  },
  dialogEnter: {
    opacity: 1,
    scale: 1.0,
    translateY: 0,
    duration: duration.slow,
    easing: easing.decelerate,
  },
  dialogExit: {
    opacity: 0,
    scale: 0.95,
    duration: duration.normal,
    easing: easing.accelerate,
  },
  pageEnter: {
    opacity: 1,
    translateX: 0,
    duration: duration.slower,
    easing: easing.decelerate,
  },
  listItemEnter: {
    opacity: 1,
    translateY: 0,
    duration: duration.slow,
    easing: easing.decelerate,
    stagger: 50,
  },
  heartBurst: {
    scale: [0, 1.3, 1.0],
    opacity: [0, 1, 0.8],
    duration: 400,
    easing: easing.spring,
  },
};

export const haptics = {
  light: 'light',      // 轻微反馈（按钮点击）
  medium: 'medium',  // 中等反馈（长按）
  heavy: 'heavy',      // 强烈反馈（错误）
  success: 'success',  // 成功反馈
  warning: 'warning',  // 警告反馈
};

export const loadingMessages = {
  aiComic: [
    '魔法画笔正在悄悄涂色...',
    '小精灵正在整理你的回忆...',
    '故事书正在一页页成型...',
    '彩色铅笔在纸上跳舞...',
  ],
  aiVideo: [
    '时光机正在运转...',
    '回忆正在变成电影...',
    '每一帧都是爱的瞬间...',
  ],
  network: [
    '传信的小信使正在赶路...',
    '小信使飞过山川河流...',
    '信件正在穿越云层...',
  ],
  save: [
    '回忆正在藏进故事书...',
    '小精灵正在装订书页...',
    '这段故事已被温柔收藏...',
  ],
};
```
