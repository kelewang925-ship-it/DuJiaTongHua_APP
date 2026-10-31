# 共享组件规范与接入边界

本规范描述当前HTML原型可调用的共享实现。入口为`assets/prototype-ui.js`的`PrototypeUI.components`及`modal/sheet/toast/busy`；基础样式在`prototype-components.css`，反馈与导航样式在`prototype-ui.css`，基础热区／焦点在`ui-foundation.css`。组件预览为[components.html](components.html)。本阶段不迁移React Native／Expo。

原画板保留绘本插画、纸张、定位标题及有依据的局部样式，新增／动态部分优先复用共享工厂。逐页保留决定见[ORIGINAL_COMPONENT_DECISIONS](ORIGINAL_COMPONENT_DECISIONS.md)，不要为了统一类名再包一层Header或替换原稿素材。

## 14类组件

| 组件 | 当前API | 用途与尺寸 | 状态与交互 |
| --- | --- | --- | --- |
| Button | components.button(label, handler, options) | Primary / Secondary / Text / Icon / Danger；普通48px，Icon44px，热区≥44px | 原生disabled；pressed .8；focus；busy提交550ms并恢复子节点，禁止重复提交 |
| Input | components.field(options) | 标签、输入框、独立错误；48px、padding12、radius8 | focus / typing / filled / disabled / aria-invalid；错误清除和标签名称保持稳定 |
| Textarea | field({multiline:true,...}) | 最小96px，可垂直调整 | 与Input相同，按业务传maxLength |
| Card | components.card(options) | 基础padding16、radius12、纸色细边；title/message或可选content节点数组；模块布局差异见Card实施记录 | 普通article；有操作时才用button；可选aria-pressed |
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

## 调用与状态约定

Toast API保持两参数；原生dialog内的顶层挂载、关键操作避让及关闭交接见[TOAST_FEEDBACK](TOAST_FEEDBACK.md)。普通／危险按钮及业务回调继续使用下述既有接口。

- Button变体用`variant: 'primary'|'secondary'|'text'|'icon'|'danger'`显式指定，不根据按钮文字猜危险性。Modal最终危险确认用`danger:true`，取消优先获得焦点。
- 新建Input／Textarea／Select使用`components.field`，返回`{root,input,error,setError}`；`options`为`[value,label]`数组时生成Select，否则按`multiline/type`生成Textarea／Input。
- 适配原画板或既有dialog字段使用`field({element})`，保留节点、name、值、监听器、只读与禁用属性；已有共享字段不重复包裹。原画板字段保持原设计尺寸，最低热区44px；新建共享字段默认48px。文件、颜色、range、checkbox、radio保留专用原生语义。
- 共享错误关联`aria-invalid`及`aria-describedby`，标签名称保持稳定；输入后清除错误，业务校验由模块负责。默认未保存比较使用稳定节点键，辅助ID变化不当作内容修改。
- Card的`content`可接收原有节点数组；有操作才生成button，没有操作使用article。原有数据、图片和导航回调保持，不复制第二套列表渲染器。
- Tag默认`selected/onChange`为选择模式；`selected:null,onActivate`为纯动作，不设置`aria-pressed`。Avatar临近已有作者文字时可隐藏重复读屏语义，图片失败保留首字符。
- `modal({title,message,content,confirm,cancel,beforeClose,danger})`返回确认／取消结果；`sheet`复用该生命周期并返回动作值，取消为null。关闭与未保存保护按[交互规则](INTERACTION_RULES.md)执行。
- Loading、Empty、Error、Toast的使用条件见[状态规则](STATE_RULES.md)，不能用成功提示替代实际写入或用Spinner替代所有等待。

## Token与原稿尺寸

共享语义值直接读取CSS变量：纸色`#fdfbf7`、主字`#6b4f4f`、强调`#b08a8f`、边框`#d4bdb6`；Fairy字体。间距4／8／12／16／24／32px，正文16px、说明14px、标题20px；普通圆角8／12px，弹层20px，阴影复用`--prototype-shadow`。动效使用共享motion变量，详见[MOTION_RULES](MOTION_RULES.md)。

原稿绝对位置、cqw比例和装饰皮肤按设计保留，不自动把所有数值替换成Token。动态12份CSS的504处等值接入记录见[SHARED_STYLE_TOKENS_IMPLEMENTATION](SHARED_STYLE_TOKENS_IMPLEMENTATION.md)；根节点变量存在不代表全部局部声明或视觉已经验收。

## 已接入范围与验收

- 共享Modal／Sheet动作使用统一Button；已识别的最终危险确认使用显式Danger和安全取消焦点。
- 10个实际列表load使用共享Loading；17个动态Empty／Error分支、13个动态Card渲染器复用共享组件。
- 29个原画板字段页面及五个弹层表单构建器已适配共享字段；动态选择／筛选／标签／两步验证弹层复用相同基础行为。不能再将这些已接入工作写为“尚未迁移”。
- 日记／照片动态作者行使用Avatar；标签管理使用动作Tag及分组Divider。原画板静态标题、装饰头像、标签按逐页决定保留。
- 最新初始／弹层／短视口及动效证据从[README](README.md)进入；各报告保留真实执行时源码指纹。具体接入范围已实现，不等于所有动态条件、原画板局部Token或人工视觉验收通过。

## 成就累计进度

m07-p20使用原生 `progress` 表达已有成就模型的累计进度，`max`取模型目标、`value`显示在0至目标内封顶，`aria-label`及`aria-valuetext`与名称／分数／状态一致。它是只读展示，不增加点击目标。与用于异步等待、带status面板的共享Loading区分用途，不能用加载动画表示已完成的照顾次数。四行纸面和领奖按钮保留原画板语义；实例及26项验证见[PET_ACHIEVEMENT_PROGRESS](PET_ACHIEVEMENT_PROGRESS.md)。

## UI名称模板与可访问标签

宠物页面通过 `PrototypePetNames.paint({pet,actor,peer})` 将原稿静态名称模板映射为真实姓名，文本、aria-label／alt／title及文档标题使用同一映射。使用一次正则回调，昵称含原稿姓名或`$&`等字符时仍保留字面值。首次收集的模板在节点／值被控制器改写后不再覆盖新内容；输入value和业务存储不参与替换。它不增加DOM控件、焦点目标或业务状态。25页及改名证据见[PET_NAMES](PET_NAMES.md)，不等于真实读屏／所有长文本布局验收。

## 完整姓名的页头分区

p11／p25的标题、双人姓名、宠物铭牌与照顾摘要按各自区域换行，支持现有12字宠物和20字个人昵称上限。只读姓名不新增焦点或点击目标，不通过截字／省略号隐藏合法姓名；头像和返回／更多入口保持独立。p11的每日／本周列表在预留的滚动区域显示，p25摘要随姓名行高排列。62项及原稿保留边界见[PET_HEADER_LAYOUT](PET_HEADER_LAYOUT.md)。

## 历史记录

此前组件实施和验证叙述完整保存在[evidence/history/pre-spec-cleanup-1420492/COMPONENTS.md](evidence/history/pre-spec-cleanup-1420492/COMPONENTS.md)，保留原字节SHA；历史通过记录按各自源码范围阅读，不作为当前全量验收。

## 成就总览展示

p21复用`PrototypePetAchievementProgress.paint`，在原七个按钮内追加只读SVG纪念章与原生progress；按钮保留原名称及详情回调，图形aria-hidden，计数／状态由同一成就模型输出。底部摘要是只读文本，按待领奖／未达成／全部领取说明下一步，不新增焦点或点击目标。卡片列表可滚动，最后一项可键盘到达。37项及边界见[PET_ACHIEVEMENT_COLLECTION](PET_ACHIEVEMENT_COLLECTION.md)。

## 资源说明与只读库存

p13／p16资源和说明放进正常流纸面容器，原操作节点保持；只读库存按同一catalog/owns渲染名称与分类，完整集合在限定区域滚动。分类使用文字，现有Tag为交互组件，不用于无业务动作的分类说明。Token复用paper／border／间距／圆角。38项及原图边界见[PET_RESOURCE_PANELS](PET_RESOURCE_PANELS.md)。
