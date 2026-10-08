# 交互原型状态规则

## 本轮：编辑保存与留言已读

最终检查点：23项专项与242项指定回归共265项通过；114页空数据／有数据共228次观察，1696条观察控件、51次条件重定向，0脚本错误、0未绑定候选。HTTP114页／37共享资源与当前源码一致，报告SHA及实际执行来源核对通过。时刻控件最终单独55/55；同源成功布局／流程／状态14项保留原执行证明，两次准备失败原文保留。114页最终验收仍0，完整目标继续。

三类编辑保存核对当前正文，拒绝正文冲突或删除后的旧提交，独立的新留言保持；聚合已读读取当前共同来源和留言。声明23项专项与242项指定回归，最终结果见editor-current-checkpoint.json。完整114页终验继续。详见[编辑当前内容](EDITOR_CURRENT_CONTENT_IMPLEMENTATION.md)。

## 上一阶段：共同入口与个人展示

上一阶段e608d0b检查点：25项专项与217项回归共242项全部通过；114页空数据／有数据共228次运行观察，1696条观察控件、51次条件重定向，0脚本错误、0未绑定候选。HTTP114页／37共享资源与当前源码一致，报告SHA和实际退出均核对通过。114页仍0页最终验收，完整目标继续。

首页／搜索／日记／相册统一可访问读取和有效范围标记；自己的不可共同使用副本继续个人展示，已知他人的私密详情／编辑使用不可见状态。照片／时刻留言提交核对当前来源，外部变化保留草稿，来源恢复后可以继续发送。共同相册筛选及留言聚合核对有效范围；照片编辑／更多热区补到44px。声明25项专项及217项直接回归，最终结果以shared-display-checkpoint.json为准。 详见[页面展示范围](SHARED_DISPLAY_SCOPE_IMPLEMENTATION.md)。

胶囊→时刻→作品→相册图的现存来源在共同素材、备份、回忆册和宠物出口逐层核对；私密／封存／草稿／受损／循环引用不可共同使用。原正文保持，删除可选祖先后的独立副本遵守既有保留合同。工坊提交重新检查来源，回忆册与宠物只读页观察胶囊外部变化。声明19项专项及99项直接消费者回归，最终结果以derived-shared-checkpoint.json为准；此前341项属于旧源码，不相加。 详见[衍生内容共同出口](DERIVED_SHARED_CONTENT_IMPLEMENTATION.md)。

胶囊开启必须核对当前sealed、有效日期与约定时间；已opened仅导航，不重写openedAt。日期修正保持sealed，比较编辑前原文，失败保留输入和来源；保存期间锁定日期，关闭尝试取消本次提交，继续编辑后需重新点击保存。提醒只更改当前reminder。新收录核对capsuleId、保留无关ID并继承可见范围，使用既有事务。 详见[胶囊日期与收录关联](CAPSULE_SEMANTIC_RECOVERY_IMPLEMENTATION.md)。

宠物与回忆册受损原文只读，普通保存暂停；明确确认、保存副本并两次比较原文后恢复。未知宠物状态为pending且清除旧确认标记，未知册状态为draft；不补发资源。不存在／null／旧[]宠物是合法未领养，新的注销写null。 详见[宠物与回忆册结构恢复](PET_BOOK_RECOVERY_IMPLEMENTATION.md)。

手动和自动备份在原始集合受损时不替换现有备份；先明确恢复再重试。容量不足、不可访问存储、快照期间来源或备份变化均保留旧快照。自动备份失败不回滚已保存内容。合法空集合允许生成备份。 证据及边界见[备份保护与共享范围](BACKUP_PRESERVATION_IMPLEMENTATION.md)。

时刻／纪念日／胶囊结构受损时只提供可读视图，普通写入被阻止；原文下载、明确确认及副本保存后才能替换。配额、竞争和dirty失败保留原文／输入。真正缺失使用Empty；受损详情使用Error。 证据及边界见[时刻／纪念日／胶囊恢复实施记录](TIME_COLLECTION_RECOVERY_IMPLEMENTATION.md)。

标签真正缺失才初始化默认值，受损集合只读可用视图，合法空集合不初始化；标签与记录联动事务暂停到明确恢复。先存原文副本并两次检查竞争，失败保持原文。 证据边界见[TAG_RECOVERY_IMPLEMENTATION](TAG_RECOVERY_IMPLEMENTATION.md)。

工坊损坏与真实缺失分别显示Error／Empty；外部恢复后CTA重查状态。确认取消生成保持deciding，取消保存失败暂停推进直到用户重试或明确继续。 具体证据与边界见[WORK_ERROR_IMPLEMENTATION](WORK_ERROR_IMPLEMENTATION.md)。

工坊受损数据仅提供可读视图，不自动写回或当空数据覆盖；普通作品保存被阻止并提示恢复。明确保留原文副本后再替换，配额／竞争失败保持原文；无效生成时间保留输入为draft，不伪造完成结果。健康和缺失作品集合保持原行为。状态/观察/证据边界见[WORKSHOP_RECOVERY_IMPLEMENTATION](WORKSHOP_RECOVERY_IMPLEMENTATION.md)，其他集合及全部字段语义继续。

危险确认采用显式Danger共享变体；取消默认焦点，未保存放弃在同一Sheet确认。账号／宠物最终提交保持既有校验、Loading、失败可重试；普通说明仍为Primary。当前158项专项及业务状态回归、此前165项同源复验见[DANGER_COMPONENT_IMPLEMENTATION](DANGER_COMPONENT_IMPLEMENTATION.md)。其他集合损坏和全部动态状态仍待终验。

这是当前公共规则与已接入范围，完整114页状态验收仍未完成。逐页适用矩阵见STATE_MATRIX.md；该旧矩阵是实施前要求，不能当成通过报告。

| 状态 | 显示与恢复规则 | 现有共享实现 | 当前证明范围 |
| --- | --- | --- | --- |
| Empty | 图标、标题、说明、创建/清筛选CTA；缺少存储键与空数组都不自动填示例 | components.state(kind=empty) | 组件预览与回忆册blank；首次空数据专项覆盖12个入口；其余列表按模块记录 |
| Loading | 列表使用Skeleton；单次资料读取可Spinner；生成用Progress；提交用Button Loading | components.loading / busy | 预览三方式、回忆册加载；各模块有限加载/生成见模块报告 |
| Error | 明确下一步；读取失败可重试/返回；失败不改变成功数据 | components.state(kind=error) | 日记/照片/时刻失效内容、回忆册失败/失效与预览恢复 |
| Disabled | 原生disabled阻止操作；资源/权限不可用有说明；加载失败不开放未绑定的底层任务按钮 | components.button / field；模块条件 | 预览、回忆册错误后控件禁用/恢复、宠物资源和权限专项 |
| Submitting | 校验后550ms有限提交，按钮禁用、aria-busy，成功/失败都恢复原子节点 | busy | 账号与内容创建等已命名流程；不是全114页控件验收 |
| Field error | 标签名称保持稳定，具体提示与aria-invalid/aria-describedby关联；输入后清除错误 | components.field / fieldError | 新组件预览及既有表单模块证据；多数原稿输入仍需迁移 |
| Success | 成功才写本地集合；更新列表/详情或短Toast；不使用永久成功弹窗代替实际结果 | toast(success)，模块存储 | 记录/作品/宠物/回忆册命名主流程；整体首次端到端串联继续验证 |
| Content missing | 清楚说明记录不存在，提供实际上级入口；不自动把失效编辑ID当作新建 | shared ErrorState + 模块路由 | 日记/照片/时刻；回忆册p04～p21共用入口条件，代表页五宽度 |
| Image error | 保留正文/输入，可重新选择或重试；头像允许首字符fallback | Avatar与模块图片控制器 | 照片、回忆册图片专项为阶段证据；全部图片仍待覆盖 |
| Unsaved | 继续编辑/放弃修改；取消、选择器关闭和返回不静默丢输入 | guard / protectSheet | 账号/内容编辑等命名专项；系统返回的原生Android映射尚未执行 |
| Personal/relationship recovery | 可读显示不改原文；普通保存暂停，原始副本/确认恢复可执行；并发或容量失败保留数据；恢复刷新保护未保存输入 | UI.read / canWrite / recoverAccount | 20项资料专项、三类连续恢复与5种宽度；会话、邀请码和其他集合继续实施 |
| Record recovery | 保存前保护损坏集合；原始文件可下载，确认后先留副本再恢复可读内容；写入失败保留原始值，刷新遵循未保存保护 | PrototypeRecords.health / recover，UI.protectStorage，transaction预检查 | 日记/照片集合21项专项及16项正常回归；副本历史下载另有15项检查；其他集合待补 |

## 本地演示边界

- 无真实后端。评审工具的fail-next按操作消费一次，用于加载/保存/图片/生成失败演示，不能冒充真实服务器响应。
- 本地容量不足与FileReader/图片解码失败需要保留内容；数据写入失败不能显示已保存。
- 读取异常JSON或不符合集合结构的内容必须进入可恢复状态。日记/照片共享集合已加入保留原始字符串的恢复流程，见RECORD_RECOVERY_IMPLEMENTATION.md；个人/关系资料另见ACCOUNT_RECOVERY_IMPLEMENTATION.md；其他read的JSON解析fallback仍不代表恢复成功。
- 重试不重复扣资源、领取奖励、打开胶囊或重建已保存内容；稳定ID、幂等操作及冲突检查按各模块合同执行。
- 空状态、错误状态和加载状态不共享一个Spinner。静态帮助、即时选择和开关不强行添加模拟等待。

## 相关证据

COMPONENTS.md记录工厂与逐页迁移边界；FIRST_VISIT_IMPLEMENTATION.md记录无存储首次场景；SHARED_STATES_IMPLEMENTATION.md记录实际状态接入；各模块IMPLEMENTATION和checkpoint记录命名测试。最终FLOW_TEST_REPORT将按完整要求汇总当前版本验证，不累加已过时的历史报告冒充全产品通过。

## 登录、邀请与临时验证码异常

登录/邀请损坏沿用原始下载、确认副本与恢复前暂停保存规则；损坏会话恢复后退出登录，重新登录。临时验证码异常保持原文并提供注册/找回出口；只有用户明确获取新码才替换。验证码必须用途一致且未过期。缺失挑战重发与未准备邀请不给成功反馈。范围与证据见SESSION_INVITE_IMPLEMENTATION.md。

## 时刻回应未发送保护

回应Sheet在取消、Escape、浏览器返回或拖动关闭时，输入改变需先确认是否放弃。继续编辑保持输入与焦点；确认放弃不改变记录。发送失败保持内容，发送成功追加回应后提交dirty基线并关闭。使用共享protectSheet；此证明范围是时刻回应，不涵盖其余全部Sheet。见MOMENT_CONTROL_EXECUTION.md。

## 日记与照片详情回应

未发送回应离开详情页（返回按钮/浏览器历史返回）复用guard，先确认继续编辑或放弃；失败保留输入与记录，成功清空并commit，关闭回应时输入/发送/表情均禁用。日期回退与caption搜索范围、控件和五宽度证据见RECORD_CONTROL_EXECUTION.md；其他表单、引用/格式和原生平台条件继续验收。

## 时间表单成功与关联记录

纪念日/胶囊保存成功使用guard.complete移除完成编辑任务的历史anchor/sentinel；写入失败不提交dirty，继续保留输入。胶囊封存只显示约定与提醒，开启成功才显示实际照片/信件；收录失败两个集合保持，删除胶囊保留已收录时刻。当天纪念日只显示匹配anniversaryId的shared且非draft记录；实际共同提醒入口在无数据时转空态。新连续使用、原有失败恢复与新增入口五宽度范围见TIME_PRODUCT_JOURNEY_IMPLEMENTATION.md，其他集合/全部状态仍开放。
