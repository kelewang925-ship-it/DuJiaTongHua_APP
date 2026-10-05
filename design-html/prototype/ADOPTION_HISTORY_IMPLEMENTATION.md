# 领养完成后的浏览器历史（阶段记录）

## 已证实的问题与修复

1. 提交邀请后，浏览器返回会打开旧选择表单；已有pending宠物使该页再跳到等待页，形成循环。连续返回和“顶部回首页后再按浏览器返回”都有同一缺陷。
2. 仅识别普通back_forward重载不够。真实BFCache恢复保留原navigation类型navigate，需要在pageshow.persisted检查完成状态。
3. 缓存恢复还会收到此前排队的storage事件。原首次页的存储监听会执行reload，覆盖刚发起的首页跳转，再回到等待页。第一次局部修复的五次原生缓存探测四次失败；记录保存在baseline/adoption-bfcache-partial-fix-results.json。

在p02选择页、p04首次页，只有宠物已处于pending/active、且属于历史遍历或原生缓存恢复时，才进入首页。普通目录直达选择页仍按当前状态进入等待页；拒绝状态的首次领养仍可使用。识别已完成页面后设置离开标记，该页面后续storage事件不再抢占导航。没有修改共用Modal或dirty guard，不删除、再次创建或确认宠物。

## 验证

- `adoption-history-results.json`：五条有名行为，包括浏览器返回、连续三次返回、顶部返回后浏览器返回、未保存输入继续/放弃、正常目录直达条件路由。原前三条有独立失败基线。
- `adoption-bfcache-results.json`：同一条原生缓存历史流程独立运行五次，每次三次返回并比对完整宠物文档。移除本地Playwright已确认的禁用缓存启动参数，记录真实pageshow.persisted和storage事件；不以手工派发事件代替原生恢复。是否真正恢复缓存以各行bfcache_observed为准。
- `pet-flow-results.json`：三条领养确认/互动、喂食/库存/任务、每周奖励幂等回归。
- 13次执行、9条不同有名行为，不将五次缓存重复试验计为五种独立场景。最终成功结果与源文件哈希见adoption-history-checkpoint.json。
- 初次缓存探测的间歇失败、随后一次成功都保留；一次成功没有被用于结束修复。新增storage观察器曾因读取无persisted字段出现五次报告解析错误，保存在adoption-bfcache-observer-error.json；不将它们记作产品通过或产品脚本错误。

## 边界

本轮验证的是当前Chrome中这些HTML流程的浏览器返回，后续RN的Android返回仍按统一规则映射，未声称已在原生Android验证。缓存五次重复足以覆盖已重现的导航抢占，不能证明所有浏览器和全部缓存组合。

全部114页仍部分实施、最终验收0页。完整动态导航、隐藏弹层及每个控件的执行清单、其他提交任务的历史、异常数据恢复和全量视觉/访问性继续推进。此前228次全页观察仍以一级导航阶段的源码哈希为准。
