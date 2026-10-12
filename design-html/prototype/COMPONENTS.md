# 共享组件实现与接入范围

> 最新阶段：日记/照片动态留言Avatar、标签管理动作Tag及分组Divider已接入，17项当前检查通过。114页原画板Header/画像/标签静态保留决定已记录；局部Token与全量流程/视觉验收继续，0页终验。详见COMMENT_TAG_COMPONENTS_IMPLEMENTATION.md。


> 上一批选择器字段（4981f9a指纹）：动态选择/筛选/标签/两步验证弹层字段已接入共享行为，50项专项与146项原画板回归在当前源码通过。全量初始/隐藏/完整流程及视觉终验仍继续，0页终验。详见SHARED_PICKER_FIELDS_IMPLEMENTATION.md。


> 上一批原画板字段（88b5efd指纹）：原画板29页69个字段已接入共享行为，最终146项字段检查及日记320px实际错误避让检查通过。原节点/属性/控制器保留；两次59项保存与输入回归绑定历史指纹。完整114页最终流程与视觉验收仍继续，0页终验。详见NATIVE_SHARED_FIELDS_IMPLEMENTATION.md。


> 上一批弹层字段（a0fe932指纹）：五个弹层表单构建函数已接入共享Input/Textarea/Select，71项字段检查和13项身份删除回归通过；源/结果边界见SHARED_OVERLAY_FIELDS_IMPLEMENTATION.md及当前checkpoint。其他组件/Token、全量运行刷新与流程/视觉终验继续，0页最终验收。


> 上一批Card（9227657指纹）：13个动态列表渲染器已接入真实共享Card，content节点参数保持原信息与图片。66项Card检查及110项状态回归以SHARED_LIST_CARDS_IMPLEMENTATION.md和当前checkpoint为准。旧全量运行/目录和752条初始点击仍为历史，0页最终验收。


> 上一批共享状态（62f7d29指纹）：17处动态Empty/Error渲染分支已接入共享状态，22种状态在五宽度的实际动作验证见SHARED_LIST_STATES_IMPLEMENTATION.md及当前checkpoint。752条旧初始点击/身份删除等仍为历史；114页运行清单和目录待组件集中修改后刷新，0页最终验收。


> 上一批Loading证据（86e7bbe指纹）：80项曾通过；新源码的30项Loading行为回归及110项状态动作以本批checkpoint为准。


照片详情“编辑”和“更多”操作热区为44px，五宽度检查中心命中；不可见状态复用共享Error与返回CTA。 详见[页面展示范围](SHARED_DISPLAY_SCOPE_IMPLEMENTATION.md)。

异常胶囊日期复用共享Error、Field、Button、protectSheet、Loading反馈和Toast。页内已有可见集合恢复入口时隐藏同集合页后按钮；其他集合恢复不隐藏。恢复过程收尾后重新观察新损坏，取消同一原文不立即重弹。 详见[胶囊日期与收录关联](CAPSULE_SEMANTIC_RECOVERY_IMPLEMENTATION.md)。

宠物与回忆册复用集合恢复控制器、Error、Button、Danger Modal、Toast和副本Sheet；Error使用既有Token，无新增设计页面。内联／全局恢复CTA重复作为P2继续整理。 详见[宠物与回忆册结构恢复](PET_BOOK_RECOVERY_IMPLEMENTATION.md)。

备份状态使用role=status和原颜色／字号／间距／圆角Token，放在数据与存储画板之后以避免覆盖原稿操作；异常提示复用Toast。五宽度验证无横向溢出，备份按钮可用Enter触发。 证据及边界见[备份保护与共享范围](BACKUP_PRESERVATION_IMPLEMENTATION.md)。

三类时间集合恢复复用共享Button、Danger Modal、Error／Empty及原始副本Sheet；没有新增设计页面。五宽度检查包含44px热区、中心命中和键盘焦点，仍不证明全部页面访问性。 证据及边界见[时刻／纪念日／胶囊恢复实施记录](TIME_COLLECTION_RECOVERY_IMPLEMENTATION.md)。

标签恢复复用共享Button／Modal／Danger／Toast，恢复选择与确认在五宽度检查屏内热区及中心命中，Enter打开与Escape关闭焦点已验证。 证据边界见[TAG_RECOVERY_IMPLEMENTATION](TAG_RECOVERY_IMPLEMENTATION.md)。

工坊缺失页现复用共享State：损坏使用Error／alert，真实缺失使用Empty／region，共享CTA在五宽度检查焦点、热区和键盘。外部恢复后重新读取作品。 具体证据与边界见[WORK_ERROR_IMPLEMENTATION](WORK_ERROR_IMPLEMENTATION.md)。

作品恢复复用Button、Modal及原始副本Sheet；最终恢复显式Danger，取消默认焦点，新入口五宽度实际中心命中、Enter打开和Escape关闭，字面清单不是执行证据。44项专项、原工坊控件和共享回归见[WORKSHOP_RECOVERY_IMPLEMENTATION](WORKSHOP_RECOVERY_IMPLEMENTATION.md)。所有其他局部组件终验仍未完成。

当前以原生HTML/CSS/简单JS实现。新组件集中在PrototypeUI.components和prototype-components.css；既有反馈复用PrototypeUI.modal/sheet/toast/busy。这个清单证明共享实现已经存在，不代表全部114页的局部组件已经迁移。

## 危险确认的实际接入

Modal增加显式`danger:true`，工厂统一danger变体及标记；当前15处最终Modal、同Sheet的放弃修改、账号／宠物最终删除提交已接入。普通确认不根据文字推断Danger。18类入口、关闭／焦点／五宽度及失败重试证据见[DANGER_COMPONENT_IMPLEMENTATION](DANGER_COMPONENT_IMPLEMENTATION.md)。局部表单原有边框／圆角保留，危险文字与纸色背景复用token，热区≥44px；其他局部组件仍待全量规范。

## 可调用组件

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

## Token与当前原型选择

复用纸色#FDFBF7、主字#6B4F4F、强调#B08A8F、边框#D4BDB6和Fairy字体。新组件间距4/8/12/16/24/32，正文16、说明14、标题20；普通组件圆角8/12，弹层20。弹层阴影使用同一暖色12/32px阴影。

当前交互原型尺寸以INTERACTION_DESIGN.md及已实现共享反馈为准；旧FairyButton文档的52px/16px等值不直接替换已精修画面。原画板定位与切图保持既有尺寸；逐页迁移时分别验证热区、文本和画面，不能把所有绝对定位间距自动改成Token。

## 已接入与继续迁移

- 全部共享Modal/Sheet的动作按钮使用同一Button工厂，保留已有危险标记、默认安全焦点、历史关闭和未保存保护。
- m04-p03 缺失内容使用同一ErrorState工厂，并返回实际空/正常时刻列表。
- 后续日记/照片失效页和回忆册p04～p21失效ID接入ErrorState；回忆册blank和初始加载/重试接入Empty/Skeleton/Error。对应迁移、原行为变更与验证见SHARED_STATES_IMPLEMENTATION.md。
- components.html实际运行14种组件以及五种按钮、三种Loading；表单保存、标签选中、错误重试、空数据新建、反馈弹层均可操作。评审页不充当产品主导航。
- 原页面的内联表单/卡片/头像等多数仍保留原稿布局与模块控制器。后续迁移与逐控件验收继续进行；不因新增组件目录而把它们标记为统一完成。

## 当前证据

verify_components.py：组件表单、弹层、恢复与五宽度；实际失效时刻恢复页五宽度。首次七项缺少预览页面的失败基线保留，新追加用例不伪称有旧基线。账号八条与时刻三条主流程回归覆盖共享按钮/弹层行为。确切成功条数、截图和源码哈希见component-checkpoint.json。

组件预览：prototype/components.html。114页最终验收仍为0；完整页面/动态导航、隐藏弹层、组件逐页迁移、状态/动效覆盖与全产品测试尚未完成。

## 个人/关系恢复接入

复用共享Button/Modal/Sheet，无新画板或组件风格。UI.read与canWrite提供两种资料的结构检查和保存保护；hasAccountProblem/recoverAccount供记录恢复协调优先顺序。范围及20项专项见ACCOUNT_RECOVERY_IMPLEMENTATION.md，其他存储类型不声称已接入。
## 本阶段共享表单完成出口

PrototypeUI.guard的返回对象新增complete(url)，目前由纪念日保存、胶囊暂存/封存调用。写入成功后提交基线并消费guard sentinel，再替换anchor为目标；失败保持旧输入/基线。commit和普通未保存/弹层行为不变，设置保护和原时间异常重新验证。新增当天共同日记与提醒入口复用components.button，原画板后可滚动，不覆盖画面。当前边界与165项证据见TIME_PRODUCT_JOURNEY_IMPLEMENTATION.md。

## 114页组件与Token覆盖审计

已完成114页空/有数据共228次观察：225条原成功观察保留，3条工坊随机草稿ID按实际草稿契约重放通过。扫描14类组件、27项共享Token及页面CSS/controller依赖；覆盖矩阵见[COMPONENT_COVERAGE.md](COMPONENT_COVERAGE.md)、[TOKEN_COVERAGE.md](TOKEN_COVERAGE.md)，证据见evidence/current/component-coverage-checkpoint.json。

当前仅证明参与布局的组件类及根节点Token计算值。瞬态Loading、隐藏弹层、局部原画板组件的保留理由及视觉终验仍需执行。明确下一批：搜索/日记/相册/时刻/纪念日/胶囊/工坊/宠物列表的数据Loading接入共享组件；之后逐页处理表单、卡片、头像、标签和分隔线。产品源码本批未修改，752条初始控件证据继续有效；114页最终验收仍为0。

## 共享列表Loading本批接入

10个实际数据load函数已复用共享Skeleton，宠物成长加载层的零宽度问题已修正。30项状态与50项五宽度证据、原失败基线、实际执行及全量运行观察见SHARED_LIST_LOADING_IMPLEMENTATION.md和evidence/current/shared-list-loading-checkpoint.json。本批保持原错误/重试与数据规则，列表Empty/Error和其他局部组件接入继续。

当前源发生变化，752条既有初始点击和13条账号删除证据转为历史／待集中复验；不能以本批Loading检查代替这些动作证明。0页最终验收。

## 当前共享字段接口

components.field({label,name,value,placeholder,multiline,type,maxLength,disabled,required,options})返回root/input/error/setError。options为[value,label]数组时生成原生select，否则按multiline/type生成textarea/input；Select共用字段基础样式，无maxlength。UI.fieldError没有显式错误目标时关联当前共享字段的error，保持aria-describedby/invalid；输入事件自动清除。原稿内联字段及其他局部控件仍继续接入或明确保留。

## 原画板字段适配

`components.field({element})`接管已有文本/日期/密码/Select/Textarea节点，返回既有节点和关联错误；不要再次append root。值/监听器/只读/禁用/字数/标签保留。29页69字段及实际证据见NATIVE_SHARED_FIELDS_IMPLEMENTATION.md；Input/Textarea覆盖选择器已包含原画板适配节点。文件/颜色/range/checkbox/radio保留专用原生语义；动态日期弹层、其他组件及完整Token/布局验收继续。

## 动态原生弹层字段

已有节点模式也支持dialog：已有label复用，否则包裹共享label。modal只接管未共享的文本/日期/Select/Textarea，保留原节点/原生属性及业务回调；已有共享表单跳过，专用file/range/color/checkbox/radio保持。50项选择/取消/错误能力和本地两步验证分支，以及146项原画板回归见SHARED_PICKER_FIELDS_IMPLEMENTATION.md。

## 留言Avatar与动作Tag

日记/照片作者行使用共享Avatar，邻近作者文字可读，画像隐藏于辅助读屏以避免重复。Tag默认selected/onChange选择模式保持；selected:null/onActivate是无aria-pressed的动作模式，当前用于既有标签管理菜单。个人/共同标签组共享Divider。114页原标题/装饰的保留决定见ORIGINAL_COMPONENT_DECISIONS.md；局部Token和整体验收继续。
