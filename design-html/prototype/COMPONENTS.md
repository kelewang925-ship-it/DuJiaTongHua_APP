# 共享组件实现与接入范围

当前以原生HTML/CSS/简单JS实现。新组件集中在PrototypeUI.components和prototype-components.css；既有反馈复用PrototypeUI.modal/sheet/toast/busy。这个清单证明共享实现已经存在，不代表全部114页的局部组件已经迁移。

## 可调用组件

| 组件 | 当前API | 用途与尺寸 | 状态与交互 |
| --- | --- | --- | --- |
| Button | components.button(label, handler, options) | Primary / Secondary / Text / Icon / Danger；普通48px，Icon44px，热区≥44px | 原生disabled；pressed .8；focus；busy提交550ms并恢复子节点，禁止重复提交 |
| Input | components.field(options) | 标签、输入框、独立错误；48px、padding12、radius8 | focus / typing / filled / disabled / aria-invalid；错误清除和标签名称保持稳定 |
| Textarea | field({multiline:true,...}) | 最小96px，可垂直调整 | 与Input相同，按业务传maxLength |
| Card | components.card(options) | padding16、radius12、纸色细边；可选标题/正文 | 普通article；有操作时才用button；可选aria-pressed |
| Header | components.header(options) | 56px + 顶部安全区；20px标题，44px返回与可选右侧操作 | 普通/透明；返回处理由调用方传入统一back/go规则 |
| AppModal | modal(options) | 原生dialog，max360px、radius20、遮罩、滚动内容 | alert / confirm / content；取消、Escape、遮罩、焦点循环/恢复、浏览器返回 |
| BottomSheet | sheet(options) | max431px、最大85svh、顶部圆角20、底部安全区 | 动作/选择/取消；遮罩、下滑80px关闭；可传beforeClose保护输入 |
| Toast | toast(message, kind) | 简短文本、非阻塞live region、2600ms | success / error / info；error顶部避免遮挡底部操作 |
| EmptyState | components.state({kind:'empty',...}) | 图标、标题、说明、CTA；padding24 | region有明确名称；CTA进入真实创建流程 |
| Loading | components.loading(options) | skeleton三行 / spinner24px / native progress | role=status；progress有明确名称、0–100值；减少动效时不旋转 |
| ErrorState | components.state({kind:'error',...}) | 说明和恢复CTA，柔和警示色 | role=alert；retry / 返回列表由调用方提供 |
| Avatar | components.avatar({name,src}) | 48px圆形，实际图片或名字首字符 | role=img + 名称；图片失败移除图片，显示首字符 |
| Tag | components.tag(options) | ≥44px、radius8、紧凑文字 | aria-pressed；点击更新状态并通知onChange；disabled不执行 |
| Divider | components.divider() | 原生hr，暖色1px，上下16px | 静态分隔，不进入点击或焦点流程 |

## Token与当前原型选择

复用纸色#FDFBF7、主字#6B4F4F、强调#B08A8F、边框#D4BDB6和Fairy字体。新组件间距4/8/12/16/24/32，正文16、说明14、标题20；普通组件圆角8/12，弹层20。弹层阴影使用同一暖色12/32px阴影。

当前交互原型尺寸以INTERACTION_DESIGN.md及已实现共享反馈为准；旧FairyButton文档的52px/16px等值不直接替换已精修画面。原画板定位与切图保持既有尺寸；逐页迁移时分别验证热区、文本和画面，不能把所有绝对定位间距自动改成Token。

## 已接入与继续迁移

- 全部共享Modal/Sheet的动作按钮使用同一Button工厂，保留已有危险标记、默认安全焦点、历史关闭和未保存保护。
- m04-p03 缺失内容使用同一ErrorState工厂，并返回实际空/正常时刻列表。
- components.html实际运行14种组件以及五种按钮、三种Loading；表单保存、标签选中、错误重试、空数据新建、反馈弹层均可操作。评审页不充当产品主导航。
- 原页面的内联表单/卡片/头像等多数仍保留原稿布局与模块控制器。后续迁移与逐控件验收继续进行；不因新增组件目录而把它们标记为统一完成。

## 当前证据

verify_components.py：组件表单、弹层、恢复与五宽度；实际失效时刻恢复页五宽度。首次七项缺少预览页面的失败基线保留，新追加用例不伪称有旧基线。账号八条与时刻三条主流程回归覆盖共享按钮/弹层行为。确切成功条数、截图和源码哈希见component-checkpoint.json。

组件预览：prototype/components.html。114页最终验收仍为0；完整页面/动态导航、隐藏弹层、组件逐页迁移、状态/动效覆盖与全产品测试尚未完成。
