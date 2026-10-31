# 独家童话：114页HTML交互原型

完整目标保持执行中：在独立worktree和`codex/design-html-rebuild`分支，将八模块114页可编辑HTML Demo完善为能指导后续React Native＋Expo开发的完整交互原型。当前仅HTML／原生JavaScript／本地mock；不迁移RN，不连接真实API、数据库、登录、推送、WebSocket或复杂AI。原D盘工作区保持不变。

## 浏览器预览

[全部页面](http://127.0.0.1:8765/) · [演示数据与故障控制](http://127.0.0.1:8765/prototype/review.html) · [共享组件](http://127.0.0.1:8765/prototype/components.html)

在仓库根目录运行`python design-html/prototype/serve_preview.py`。已有服务时不重复启动。review仅操作本地模拟数据，自动化使用独立浏览器上下文。

## 七项交付入口

| 交付 | 文档与机器证据 |
| --- | --- |
| 页面名称、类型、入口、出口 | [PAGE_CATALOG](PAGE_CATALOG.md)／[初态合同](evidence/current/initial-controls-20261031-accessible/contracts.json) |
| 页面关系与条件导航 | [当前统一索引](CURRENT_NAVIGATION_ATLAS.md)／[当前关系图](CURRENT_NAVIGATION_ATLAS.mmd)／[初态逐行](CURRENT_NAVIGATION.md)；PAGE_RELATIONSHIPS保留历史范围 |
| 组件与Token | [COMPONENTS](COMPONENTS.md)／[原画板保留决定](ORIGINAL_COMPONENT_DECISIONS.md)／[TOKEN_COVERAGE](TOKEN_COVERAGE.md) |
| 点击、返回、删除、保存、取消 | [INTERACTION_RULES](INTERACTION_RULES.md)／[CONTROL_BEHAVIORS](CONTROL_BEHAVIORS.md) |
| Loading、Empty、Error、Disabled、Success | [STATE_RULES](STATE_RULES.md)／[STATE_MATRIX](STATE_MATRIX.md) |
| 页面、控件与弹层动效 | [MOTION_RULES](MOTION_RULES.md) |
| 优先问题与逐项验收 | [ISSUES](ISSUES.md)／[原41项](ACCEPTANCE_REQUIREMENTS.md) |

## 最近实际证据

| 范围 | 结果与来源 |
| --- | --- |
| 114页初态控件 | [754项](CURRENT_INITIAL_REPLAY.md)：753本轮成功＋1弹层稳定后新执行；393条实际跨页结果，原10背景拦截失败保留 |
| 首次使用与连续流程 | [4条54阶段](CURRENT_CONTINUOUS_JOURNEYS.md)：八模块22阶段新执行，三条32阶段同源码保留；真实导出、退出重登和删除保留原素材 |
| 命名异常 | [14组110案例](CURRENT_EXCEPTION_REPLAY.md)：全部新执行，79次真实失败消费涉及77个操作；名称不代替所有条件覆盖 |
| 五宽度与键盘 | [570布局＋5照片流程](CURRENT_QUALITY_REFRESH.md)：565不受局部CSS影响的结果保留、5补页布局新执行，114页762次Tab观察；修复原生照片入口26px高度 |
| 弹层与短视口 | [112项](CURRENT_QUALITY_FOLLOWUPS.md)：97同源码成功保留＋15修正V1位置定位后新执行；80真实表单页宽、4共享焦点、5搜索、18危险及5普通确认 |
| 当前手动弹层关闭 | [104入口571项](CURRENT_OVERLAY_LIFECYCLE.md)：570首轮成功保留＋1实际按钮补跑；80修改后继续／放弃，290次隐藏控件出现单列，不冒充业务提交结果 |
| 隐藏操作业务结果 | [282业务／选择器案例](CURRENT_HIDDEN_BUSINESS.md)：231业务＋50选择器＋1生日清空；另补6个目录Sheet的30项关闭，110弹层302次控件出现逐项关联实际结果 |
| 回忆册V2等待边界 | [34项当前新执行](CURRENT_BOOK_PENDING.md)：主题、寄语／章节／书名、选图取消／解码和读取中返回；旧270项中的其余236项不冒称当前重跑 |
| 共享组件与Token | [56组件契约＋114页观察](CURRENT_COMPONENT_CONTRACTS.md)：14类四配置新执行，43项共享根变量一致；局部接入和其他状态另行核对 |
| 后续样式Token接入 | [10 CSS／191声明](CURRENT_STYLE_TOKEN_ADOPTION.md)：复用18既有变量；151修改前观察、72受影响场景修改后计算／几何完全一致，HTML／JS／资源未改 |
| 原稿对照 | [114页自检记录](VISUAL_SELF_REVIEW.md)／[回忆册及V2](BOOK_VISUAL_REVIEW.md)；仍有视觉差异，人工验收0 |

照片热区修复批次只追加补页照片输入框的两条44px样式，后续Token批次又接入10 CSS的191处同值声明。行为报告保留采集时的原始指纹，不冒充修改后全组重跑；版本对应见CURRENT_QUALITY_REFRESH及CURRENT_STYLE_TOKEN_ADOPTION。旧报告目录里的“current”是采集分类，判断时以执行时依赖、案例范围和实际结果为准。

## 明确剩余

当前已观察110弹层、302次控件出现的关闭与具名业务结果已对应，已观察导航和条件案例已统一索引；后续动态CSS的同值Token接入已补齐。接下来按原41项逐项核对提交／等待证据的版本对应及其他明确条件，处理已登记的字体、控件皮肤、列表和原稿视觉差异。自检、实现、流程验证与人工验收分开；真实Android设备、系统IME、触屏及读屏未执行时不声明通过。

唯一逐页队列是[queue.json](queue.json)，本批没有改写整页验收状态。主要流程及异常验证和完整41项要求未全部证明完成前，不结束完整目标。

## 验收目标

- 114 页全部列出页面名称、类型、入口、出口；隐藏弹层与状态另列，页面关系标注触发控件与条件。
- 每个可点击元素说明实际行为，不能以“以后实现”或仅更改选中样式代替操作结果。
- 一级导航、详情 push、临时任务、返回、未保存编辑、危险操作遵循明确规则。
- 复用现有原稿与 Fairy 规范，以简单共享 HTML/CSS/JS 实现 Modal、Bottom Sheet、Toast、表单反馈及状态组件。
- 主要流程使用本地数据完整闭环：输入、Loading、保存、反馈、返回、看到结果、再次编辑、删除。
- 首次使用与无数据状态可以操作；失败模拟具备恢复入口，保留未提交内容。
- 主要流程、取消/返回、空/加载/失败、刷新及五种手机宽度有可重复浏览器证据。
- 交付页面/行为/导航清单、组件规范、交互/状态/动效规范、P0/P1/P2问题及修复/验收记录。

## 执行顺序

1. **扫描与基线**：遍历所有页面、内联脚本/样式、资源、可操作节点、弹层、路由及本地键；在隔离浏览器观察全部事件绑定。静态候选不直接认定为真实缺陷。
2. **关系与行为审计**：逐模块匹配控件与处理函数，区分示例状态稿/正常页面/条件分支，补充动态路由及真实用户起止流程。
3. **状态补齐设计**：按页面职责明确 normal/loading/empty/error，表单 disabled/validation/submitting/success，失败与空数据的恢复 CTA。
4. **共享组件**：现有 Fairy 文档及 ui-foundation.css 是基础；增加原生 JS 共享交互组件，保留页面绘画布局，避免全面替换 DOM。
5. **逐模块闭环**：先修账号/绑定与首页记录，再纪念日/胶囊、工坊、设置、宠物、回忆册；每模块完成后运行流程回归。
6. **整体验收**：首次空数据→登录绑定→内容创建→详情编辑→列表→删除，以及跨模块数据关联、失败重试、弹层返回、窄屏/安全区检查。

## 历史与恢复点

此前578行阶段记录已[完整归档](evidence/history/pre-quality-overview-cfee1bf/README.md)，原字节和来源SHA见同目录manifest.json；归档内相对链接仍以本prototype目录为基准。旧阶段报告、失败基线与专项实施文档均保留，不以累计检查数替代最终验收。

[基线页面](BASELINE_PAGES.md)／[静态导航基线](BASELINE_NAVIGATION.md)／[原扫描](baseline-inventory.json)／[交互设计与验收规范](INTERACTION_DESIGN.md)保留扫描→清单→关系→交互→状态→组件→Demo→流程→规范的历史顺序。
