# 交互原型状态规则

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
