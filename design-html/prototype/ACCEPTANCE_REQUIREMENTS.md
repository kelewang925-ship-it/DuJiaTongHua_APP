# 完整交互原型：逐项交付审计

依据用户提示词的41个章节及当前完整目标。本文保留全部范围，不把阶段通过数当作产品完成。当前114页均未最终验收。

当前页面职责、HTML字段、控制器、样式依赖、267个资源文件、228次运行观察及1696条观察控件由[页面合同目录](evidence/current/page-contracts.json)绑定。752条初始控件执行记录均对应当前源码；本轮重新执行其余532条，实际退出、报告SHA和源码哈希逐项绑定。隐藏分支必须另外验证，不能以初始控件通过替代状态终验。

| 提示词章节 | 要求及可证明完成的证据 | 当前证据与剩余工作 |
| --- | --- | --- |
| 1 扫描项目 | 全部HTML/CSS/JS、图片/Icon、组件和隐藏状态均列明 | PAGE_CATALOG、page-contracts的267资源及每页依赖已更新；隐藏状态仍需逐页条件清单 |
| 2 页面关系 | 每个入口、操作、条件、落点及返回明确，无死路 | CURRENT_NAVIGATION和PAGE_RELATIONSHIPS含114节点；候选和历史点击仍需条件执行证明 |
| 3 可点击元素 | Button/Icon/Card/List/Tab/Avatar/Image/Link/浮动/更多/InputAction/Switch/Checkbox都有明确实际行为 | 1696条观察保留原回调、selector、属性；752条初始执行证据均为当前源码通过；全部动态控件与无效果检查待复验 |
| 4 导航规范 | 一级Tab、详情Push、完整任务和临时选择一致 | INTERACTION_DESIGN、NAVIGATION和共享primaryNav；不同来源历史与条件入口待终验 |
| 5 返回 | 顶部、浏览器返回、Modal关闭、Sheet下滑、未保存确认均正确 | UI.back/guard/protectSheet及265项阶段证据；各来源和提交途中取消继续。HTML验证Android式返回语义，原生接入属于后续RN阶段 |
| 6 Modal | 统一宽度、圆角、文本、按钮、遮罩和进入/退出 | COMPONENTS、prototype-ui.css及共享modal；全部动态调用条件仍需对照 |
| 7 Sheet | 拖动条、圆角、背景、遮罩、安全区、85svh高度与滚动；取消/遮罩/下滑 | 共享sheet与各模块dirty/layout报告；全部动态内容和键盘遮挡待逐页终验 |
| 8 Empty | 每个列表为空时有图形、标题、说明、真实CTA | STATE_MATRIX、共享state、首次及空数据报告；不得用228次观察替代空CTA逐项点击 |
| 9 Loading | 页面/列表/图片/提交/分页/生成按意义选Skeleton/Spinner/Progress/Button | 共享loading、busy与工坊Progress；列表仍有文本加载，需逐页决定及统一，不强加无意义分页 |
| 10 Error | 模拟网络/服务器/超时/图片/提交/生成失败，提供重试或返回，失败保留输入 | STATE_RULES、失败注入和恢复专项；全部适用分支与误导性反馈仍待终验 |
| 11 Toast | 成功/error/info，简短非阻塞自动消失、不挡关键操作 | 共享toast2600ms、错误顶部；长文/键盘/全部页面关键按钮布局继续 |
| 12 表单 | Input/Textarea/Select/日期/Checkbox/Switch的focus/typing/filled/disabled/error/success与及时校验 | 共享field/fieldError及编辑专项；所有旧表单blur、输入限制和键盘状态仍需统一审计 |
| 13 按钮状态 | 主要按钮default/pressed/disabled/loading，提交正确反馈 | COMPONENTS及busy防重复；全部动态按钮状态仍需实际执行 |
| 14 列表交互 | 明确点击、长按、滑动、刷新、分页的适用性 | LIST_INTERACTIONS已列114页，其中44页声明集合／选择／回应区域；每页点击、刷新及不新增长按／滑动／分页理由明确。隐藏集合与条件执行继续 |
| 15 刷新 | 内容列表在有意义时提供刷新，无意义页面不强加 | LIST_INTERACTIONS列出显式按钮、storage或重入读取；选择任务保留候选。共同提醒当前仅重入读取；全部刷新失败／取消／来源变化条件继续 |
| 16 删除 | 重要内容有危险确认，取消无写入，成功更新列表 | Danger组件及模块删除回归；删除途中内容变化、不同来源返回继续；统一撤销不是本项目强制方案 |
| 17 动效方向 | 柔和克制，不新增复杂弹跳/光效/动画架构 | MOTION_RULES和共享CSS；原稿及动态控件一致性继续 |
| 18 页面进入 | opacity与8px位移，约200–300ms，不破坏原画板 | 共享220ms及motion专项；所有页面/重定向/历史恢复未全验 |
| 19 按钮反馈 | opacity或轻微scale，约100–150ms | ui-foundation的opacity .78/120ms；所有可点击非button区域需核查 |
| 20 卡片反馈 | 可点击Card有克制按下反馈 | 共享card使用button；各页局部Card接入或保留理由未全量记录 |
| 21 Modal动效 | opacity与scale .96→1，约200–250ms | 共享220ms进入/160ms退出；减少动效与全部调用待全验 |
| 22 Sheet动效 | translateY进入，约250–300ms | 共享280ms进入/220ms退出；拖动与未保存关闭的全部组合待终验 |
| 23 收藏喜欢 | 如果存在则状态真实、轻微反馈，装饰不伪装按钮 | MOTION_RULES采用普通按下反馈；逐页适用与刷新后的状态继续 |
| 24 成功反馈 | 重要首次操作可有短文案/插画，避免频繁打断 | 绑定/建册/宠物结果状态存在；全流程反馈频率及真实状态对应仍需审计 |
| 25 组件系统 | 14类组件都有用途/尺寸/样式/状态/交互并合理复用 | COMPONENTS有14类API表；页面局部实现、状态组件接入及保留理由仍待全量覆盖 |
| 26 Button变体 | Primary/Secondary/Text/Icon/Danger尺寸、padding、字体、禁用/加载/按下统一 | 共享button及Danger专项；局部按钮统一仍需核查 |
| 27 Input | Label/Placeholder/Border/Padding/Focus/Error/Disabled统一 | 共享field48px、textarea96px；旧业务表单继续接入或明确保留理由 |
| 28 Card | padding/radius/background/border/shadow/pressed统一 | 共享card16px/12px；局部Card仍需适用表 |
| 29 Header | 返回/标题/右侧操作、透明/普通、安全区统一 | 共享header56px与44px热区；原画板Header逐页差异与保留理由继续 |
| 30 AppModal | Alert/Confirm/Content支持统一 | UI.modal支持message/content/actions；全部业务入口状态继续 |
| 31 AppToast | success/error/info统一 | UI.toast与源码实现；长文/键盘布局见第11项 |
| 32 Token | Color/Typography/Spacing/Radius/Shadow统一、减少随机值 | COMPONENTS和prototype-ui.css有Token；原画板及局部CSS仍需审计和明确尺寸规则 |
| 33 热区 | 视觉Icon与点击尺寸分离，重要按钮约40–44px | 当前目标44px、指定五宽度检查；全部114页动态状态及焦点/命中未全验 |
| 34 连续流程 | 从入口到创建、Loading、保存、反馈、列表新增、编辑/删除无断点 | product/time-product-journey及当前265项；其他全部主要异常和来源条件继续 |
| 35 首次使用 | 首次打开、登录、绑定、首页和创建不依赖已有业务数据 | FIRST_VISIT/NEW_USER_JOURNEY和两条新用户连续链；八模块752条初始控件均当前通过，首次全条件和动态分支继续 |
| 36 空数据 | 新用户全部集合为空仍完整，CTA恢复到正常链 | 空数据114观察与首次专项；每个状态CTA、选择和返回仍需逐项证明 |
| 37 异常流程 | 断网/请求/图片/保存失败可理解并可继续 | 使用本地模拟，不引入真实API；既有命名失败专项分散，需完整适用矩阵与当前源复验 |
| 38 范围约束 | 不迁移RN/Expo、不真实API/db/auth/push/WebSocket/复杂AI/复杂动效 | 当前目录与分支只维护HTML原型；原工作区保持；最终diff与运行方式再核对 |
| 39 简单交互 | 原生JS和本地模拟，无额外复杂架构 | 共享UI与模块控制器；最终完整流程继续 |
| 40 七项输出 | 页面清单、导航、组件、交互、状态、动效、P0/P1/P2问题均准确且对应实际实现 | 七项文件均存在；页面类型本轮明确，导航候选不等于最终完整导航；其他规范中的旧范围需逐项刷新 |
| 41 执行顺序 | 扫描→清单→关系→交互→状态→组件→Demo→流程→规范 | 保留历史实施证据及当前计划；当前进入完整交付审计，未完成项继续执行 |

## 继续执行顺序

1. 初始控件当前复验已完成：532条新执行通过，全部752条绑定当前源码；保留实际退出、报告SHA和旧报告。继续逐项条件与状态审计。
2. 列表适用表已建立；继续逐页隐藏弹层、动态状态、返回来源和刷新失败／取消条件，修复明确断点。
3. 完成局部组件/Token、Loading/Empty/Error接入或保留理由；覆盖五宽度、安全区、键盘、命中和焦点。
4. 重跑完整主要流程及适用异常，逐项核对本表和七项交付，满足后才提升页面终验和结束目标。
