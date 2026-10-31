# 交互原型状态规则

本规范说明当前本地mock原型的状态及恢复语义。组件API见[COMPONENTS](COMPONENTS.md)，导航、返回和未保存保护见[INTERACTION_RULES](INTERACTION_RULES.md)，逐页适用要求见[STATE_MATRIX](STATE_MATRIX.md)。实现与自动化检查不等于整页人工视觉验收；独立状态维护于唯一`queue.json`。

## 状态与下一步

| 状态 | 当前行为 | 共享实现／责任 |
| --- | --- | --- |
| Empty | 图形、标题、说明和真实创建／清筛选CTA；空数组或缺失键不自动填示例 | components.state(kind=empty)，模块提供CTA |
| Loading | 内容列表用Skeleton，单次等待按意义用Spinner，生成用Progress；静态帮助和即时开关不强加等待 | components.loading；列表加载与工坊任务控制器 |
| Submitting | 校验后按钮Loading、disabled、aria-busy；550ms准备期后才执行操作，成功或失败都恢复原按钮节点 | UI.busy；业务操作明确返回结果 |
| Disabled | 原生disabled阻止操作，说明权限／资源或加载原因；读取失败不开放未绑定任务按钮 | Button／Field与模块条件 |
| Field error | 标签名稳定，具体错误关联字段，首错按模块聚焦；用户继续输入后清错 | components.field／UI.fieldError；原画板29页和动态字段已适配 |
| Error | 保留可重试上下文，提供重试／返回；失效编辑ID不当作新建 | components.state(kind=error)与模块恢复入口 |
| Success | 实际写入成功后更新列表／详情和短反馈；返回列表可见新内容 | 模块存储／transaction／toast(success) |
| Toast | success／error／info，2600ms后隐藏，非阻塞；默认错误顶部／普通底部，按关键操作避让 | UI.toast，role=status／alert |
| Image reading | 读取／解码期间保留输入，保存等待已选图片；再次选择以最新请求为准，过期结果不覆盖新图 | 记录共享图片读取工具与各编辑器 |
| Image error | 正文／已有附件保持，可重新选图或明确重试；Avatar失败使用首字符 | 图片控制器／Avatar |
| Image timeout | 工坊相册写入前的图片准备最多15秒，失败恢复按钮，取消旧来源；用户再次点击才重试，迟到不写入 | workshop-store::decodedImage与UI.busy |
| Unsaved | 返回／取消／遮罩／下滑先判断修改；继续编辑保留字段与焦点，明确放弃才离开 | UI.guard／protectSheet／beforeClose |
| Content missing | 说明删除／不可见／来源失效，提供真实上级；不展示已失效的共同正文 | 各模块入口与共享ErrorState |
| Damaged storage | 原字符串保持并允许下载；确认后先留原始副本再恢复可读内容；容量或并发失败不替换 | protectStorage、集合health／recover和transaction预检查 |

Toast显示时进入当前原生dialog子树，确保顶层内可见；关闭后同一提示移回body继续剩余计时。当前位置与可见关键操作重叠时选择最近的可用间隔；API、色彩与2600ms保持。实际22项及20关闭回归见[TOAST_FEEDBACK](TOAST_FEEDBACK.md)。

## 保存、取消与并发

- 550ms准备期间允许按既有规则取消或继续编辑；取消的旧任务不得迟到写入。回调已开始时先阻止关闭，完成后恢复操作，不能承诺撤销已经发生的写入。
- 等待期间修改正文、日期或选图需要重新明确提交，不静默保存旧快照。一个编辑任务不保留多个待执行提交。
- 来源、身份／共同范围、当前记录及配额在写入前重新核对；外部变化时保留草稿并要求用户检查。成功后提交dirty基线或complete编辑任务，失败不清空输入。
- 删除使用稳定ID与明确危险确认，取消不写入；重试不重复奖励、扣资源、打开胶囊、建册或相册导出。
- 浏览器历史返回、Escape、遮罩和Sheet向下拖动复用同一关闭门。HTML中的浏览器返回代表Android式返回语义，未执行真实Android／IME／触屏时不声明设备验收。

## 身份、集合及来源恢复

个人／关系、会话／邀请、标签、记录、作品、时刻／纪念日／胶囊、宠物／回忆册已建立对应恢复与写入保护；不能再把后来完成的集合全部列为“待接入”。结构恢复不等于所有字段语义、失效引用和并发条件都通过。

损坏会话恢复后需重新登录；验证码与用途、手机号和有效期对应，缺失／受损挑战保留原文，用户明确重新获取才替换。失败不显示验证码已准备。各业务来源和共同可见约束在读取、回应、收录、导出时保持。

## 演示与证据边界

无真实API、数据库或真实登录服务。评审工具的fail-next只消费指定操作一次，用来演示失败／重试，不冒充服务器响应。请求超时目前具体落实于相册图片准备，不能把该时限扩展宣称为所有本地选择器或网络操作的统一超时。

已贯通的新用户／八模块／时间业务主链、失败矩阵和专项证据从[README](README.md)进入。最近表单压力与共名失败入口见[CURRENT_FORM_PRESSURE](CURRENT_FORM_PRESSURE.md)，相册超时见[ALBUM_REQUEST_TIMEOUT](ALBUM_REQUEST_TIMEOUT.md)。命名操作被触发不等于每个调用条件都完成；字段自检、截图或路径齐全不构成人工视觉通过。

## 宠物成就进度与领取

成就行、所选成就与领奖按钮继续读取同一个 `PrototypePetLife.achievements` 模型。未达成显示实际分数和空／部分原生条；达成显示满条并可领取；已领取显示明确状态且禁用领取，重载后不重复增加星星。显示封顶不改变日志计数、目标或奖励。领取失败保持原数据并可重试，实际玩耍／喂食及其他标签页更新后反映新进度，不依据底图比例判断达成。四行可见摘要不取代全部七项成就汇总。当前26项证据与源边界见[PET_ACHIEVEMENT_PROGRESS](PET_ACHIEVEMENT_PROGRESS.md)。

## 姓名变更与内容所有权

静态UI中的宠物、本人与伙伴称呼及浏览器标题同步真实值；从原模板刷新，不能把新昵称中的“小满／阿舟／糯米”再解释为占位符。修改宠物名字失败保留原数据及原朗读名，成功后立即刷新名称和现有页面内容，重载／其他标签页更新仍正确。控制器已改写的节点或字符串以及后来新增的用户内容不以旧模板重新覆盖；这不改变原存储、输入或dirty规则。具体104项名称证据与未覆盖边界见[PET_NAMES](PET_NAMES.md)。

## 历史记录

此前完整状态实施记录保存在[evidence/history/pre-spec-cleanup-1420492/STATE_RULES.md](evidence/history/pre-spec-cleanup-1420492/STATE_RULES.md)，保留原字节及各阶段边界。当前规则以上述实现为准，未覆盖项仍按41项验收要求与问题记录推进。

## 成就总览下一步

优先显示首项done且未claimed成就与其真实奖励；若无待领，显示首项未达成成就的封顶进度／目标／奖励；全部已领显示完成说明。不能把达成数当领取数，也不显示无数据支持的双方个人照顾天数。状态由既有模型计算，显示不改写claims或库存；实际领奖与跨标签照顾后更新。37项证据见[PET_ACHIEVEMENT_COLLECTION](PET_ACHIEVEMENT_COLLECTION.md)。

## 资源条件与已拥有

解锁页优先判断owns：已拥有显示无需再次解锁；未拥有按原价格和当前余额显示真实差额。展示不扣资源、不改变已拥有状态，原返回选择后才通过既有确认／解锁流程处理。零装扮与四件免费小屋物品分别按原模型显示，不以固定图中数量推断库存。38项及未关闭的目标插画锁状态见[PET_RESOURCE_PANELS](PET_RESOURCE_PANELS.md)。


p13/p16所选物品示意优先 owns→已拥有，否则 allowed 且余额足够→可解锁，其余→未解锁。免费小屋物品沿用原模型已拥有逻辑；围巾仍按原照顾奖励获取，不新增手动购买。房间主画的锁只是氛围示例，实际状态以独立物品卡为准。见[PET_ITEM_PREVIEWS](PET_ITEM_PREVIEWS.md)。
