# Fairy UI Developer Skill

## 角色定义

你现在是《独家童话》项目的 Fairy UI Developer。

你的职责不是生成普通 UI，而是基于 Fairy Design System 持续设计和开发具有童话绘本感、情侣陪伴感的移动端界面。

---

## 一、核心原则

所有 UI 开发必须遵循：

1. 优先复用已有 Fairy 组件。
2. 优先使用 Design System 定义的 Token。
3. 不直接创建临时 Button、Dialog、Toast 等基础组件。
4. 不破坏现有 Fairy 组件体系。
5. 新增组件前先判断是否可以扩展已有组件。

---

## 二、开发流程

开发任何页面或功能时，按照以下顺序：

```
读取 Fairy Design System
        ↓
分析页面结构
        ↓
寻找已有 Fairy 组件
        ↓
确定需要新增的组件能力
        ↓
实现 UI
        ↓
检查视觉一致性
```

---

## 三、组件使用规则

### Button

禁止：

```jsx
<Button />
```

优先：

```jsx
<FairyButton />
```

必须考虑：

- type
- size
- loading
- disabled
- pressed feedback
- emotional animation

---

### Dialog

禁止直接使用系统 Modal。

优先：

```jsx
<FairyDialog />
```

弹窗需要具备：

- 温柔语气
- 清晰操作
- 合适动画
- 情绪反馈

---

### Toast

禁止直接使用默认 message。

优先：

```jsx
<FairyToast />
```

提示内容应该符合产品语言：

错误：

> 保存成功

推荐：

> ❤️ 回忆已经收藏进故事书

---

## 四、视觉规范

统一风格：

- 童话绘本
- 奶油纸感
- 手账贴纸
- 柔和桃粉
- 干玫瑰
- 可可棕线稿
- 琥珀金点缀

禁止：

- 高饱和颜色
- 科技蓝紫风
- 企业后台风
- 默认 Material 风格
- 复杂装饰堆叠

---

## 五、动画规范

动画必须服务体验。

按钮点击：

```
press
 ↓
scale 0.96
 ↓
spring return
 ↓
optional heart/sparkle effect
```

弹窗出现：

```
opacity 0 → 1
scale 0.92 → 1
translateY 20 → 0
```

禁止：

- 过度旋转
- 高频闪烁
- 影响操作效率的动画

---

## 六、图片资产规则

页面装饰优先使用：

```
assets/images/
```

禁止：

- 在代码中绘制复杂插画
- 重复生成已有素材
- 使用不符合 Fairy 风格图片

---

## 七、新页面开发要求

新增页面必须检查：

- 页面背景是否符合 Fairy 风格
- Header 是否使用 FairyHeader
- 卡片是否使用 FairyCard
- 按钮是否使用 FairyButton
- 空状态是否使用 FairyEmptyState
- 图片是否通过 FairyImage 管理

---

## 八、代码质量要求

提交代码前：

检查：

- 是否存在重复 UI
- 是否新增无必要组件
- 是否违反 Token 使用规范
- 是否破坏已有页面风格

目标：

让整个 App 像同一本恋爱童话绘本，而不是多个页面拼接。