# 《独家童话》Codex 建立 Figma 基础 Design System Prompt

> 目标：在 `ui/optimize-layout` 分支中，由 Codex 负责建立《独家童话》Figma Design System 基础配置。
>
> 注意：本阶段不是进行效果图自动转稿，不负责页面视觉还原，不负责生成图片资产。
> 当前任务目标是建立后续 GPT + Figma 页面还原所依赖的设计基础。

---

# 一、项目背景

项目：独家童话（DuJiaTongHua）

产品定位：

> 一本会呼吸的恋爱故事书。

视觉方向：

- 童话绘本
- 奶油纸感
- 温柔治愈
- 手账拼贴
- 回忆收藏
- AI魔法感（非科技感）

禁止方向：

- 高饱和粉色
- 科技蓝紫风
- 赛博 AI 风
- 普通社交 App 风格
- 低幼卡通风

---

# 二、执行范围

本阶段只完成 Figma 基础 Design System。

必须完成：

1. Figma Variables
2. Color Tokens
3. Typography Tokens
4. Spacing Tokens
5. Radius Tokens
6. Shadow Tokens
7. 基础 Components
8. Component Variants
9. 命名规范
10. Code Connect 准备结构

不要执行：

- 不还原任何页面
- 不导入整张效果图
- 不创建页面截图组件
- 不生成 PNG 素材
- 不修改业务代码逻辑
- 不替代人工设计资产

---

# 三、Figma 文件结构

创建以下 Page：

```
00 Cover
01 Design Tokens
02 Components
03 Assets Reference
04 Templates
```

---

# 四、Color Tokens

建立 Variables：

## Primary

桃夭

```
primary-500
#F6BEC8
```

用途：

- 主按钮
- Tab 激活
- AI入口
- 重点强调

---

## Secondary

藕丝秋半

```
secondary-300
#E9D7D2
```

用途：

- 卡片背景
- 输入框
- Tag

---

## Accent

枯玫瑰

```
accent-500
#B08A8F
```

用途：

- 标题
- Icon强调
- 时间信息

---

## Text

可可棕

```
text-primary
#6B4F4F
```

用途：

- 正文
- 边框
- 手绘线条

---

## Background

月白

```
background-primary
#F8F6F2
```

禁止使用纯白作为主要背景。

---

## AI Accent

琥珀金

```
ai-gold
#D8B384
```

用途：

- AI生成
- 魔法效果
- 会员

---

# 五、Typography

建立字体 Style。

## Display

名称：

```
Fairy Display
```

用途：

- 页面标题
- Hero文字
- 纪念日标题

推荐：

霞鹜文楷

---

## Body

名称：

```
Fairy Body
```

用途：

- 正文
- Button
- Input

推荐：

HarmonyOS Sans

---

# 六、Spacing Tokens

建立：

```
space-4
space-8
space-12
space-16
space-20
space-24
space-32
space-40
```

核心规范：

页面边距：20px

模块间距：24px

Card Padding：16/20px

---

# 七、Radius Tokens

建立：

```
radius-sm
12px

radius-md
20px

radius-lg
28px
```

用途：

12:
Tag/Input

20:
Card

28:
BottomSheet/AI Card

---

# 八、Shadow Tokens

建立：

## Card Shadow

```
0 6px 18px rgba(176,138,143,0.08)
```

---

## Floating Shadow

```
0 12px 30px rgba(107,79,79,0.12)
```

---

# 九、基础 Components

在 Components 页面创建：

## FairyButton

Variants:

```
Primary
Secondary
Disabled
Loading
```

规格：

- Height:52
- Radius:18
- Font:16 Medium

---

## FairyCard

Variants:

```
Paper Card
Image Card
Diary Card
AI Card
```

特点：

- 奶油纸背景
- 轻阴影
- 大圆角

---

## FairyInput

Variants:

```
Default
Focus
Error
Disabled
```

---

## FairyTag

Variants:

```
Mood
Category
AI
Date
```

---

## FairyHeader

Variants:

```
Default
Back
Title
Action
```

---

## FairyTabBar

Variants:

```
Active
Inactive
```

要求：

Active：桃粉胶囊感

Inactive：可可棕线性图标

---

# 十、Component 命名规范

统一：

```
Fairy + ComponentName
```

例如：

```
FairyButton
FairyCard
FairyHeader
FairyInput
FairyTabBar
```

---

# 十一、Code Connect准备

所有核心组件增加说明：

对应 React Native：

```
src/components/
```

预留：

```
Figma Component
↓
React Native Component
```

映射关系。

---

# 十二、验收标准

完成后必须满足：

- [ ] Figma Variables 创建完成
- [ ] Color Token 完成
- [ ] Typography 完成
- [ ] Spacing 完成
- [ ] Radius 完成
- [ ] Shadow 完成
- [ ] Button Component 完成
- [ ] Card Component 完成
- [ ] Input Component 完成
- [ ] Header Component 完成
- [ ] TabBar Component 完成
- [ ] 命名统一
- [ ] 无页面截图组件
- [ ] 无临时占位设计

---

# 十三、Git要求

工作分支：

```
ui/optimize-layout
```

禁止：

- 修改 main
- 创建新分支

完成后提交：

```
feat(ui): create fairy design system foundation
```

---

# 十四、最终目标

本阶段完成后：

GPT + Figma 后续负责：

> 基于 Design System 还原页面。

人工负责：

> 提供真实图片资产。

Codex负责：

> 维护 Design System 与代码映射。

不要继续尝试自动把效果图转换成设计稿。
