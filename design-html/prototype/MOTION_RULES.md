# 动效规则

> 来源时效更新：总清单的752项“当前源码通过”属于历史采集版本；本次发现71处依赖变化、23个新增文件。七项交付入口及114页ID齐全，但不等于最新全量验收。当前局部证据与完整待办见[DELIVERABLE_FRESHNESS](DELIVERABLE_FRESHNESS.md)。

2026-10-26按当前源码复验：原有6项共享动效合同及2项普通／减少动态效果计算样式比较全部通过，实际进程52006退出0。新结果保存在`evidence/current/final-motion/`；原报告逐字保持。该范围覆盖下述明确场景，不扩张为114页全部状态或硬件设备验收。

本规范依据当前HTML实现。整体方向为柔和、轻盈、自然、克制；后续原生端沿用语义，具体导航实现仍由RN阶段决定。旧Fairy文档中的复杂弹跳和插画循环不属于本轮范围。

## 当前共享行为

| 对象 | 动效与时长 | 实现与边界 |
| --- | --- | --- |
| 页面首次显示 | opacity 0→1，translateY 8px→0，220ms ease-out | prototype-ui.css 的.screen与--prototype-motion-enter；不设置forwards，结束后使用原画板transform。文档加载产生进入动画，原生浏览器缓存恢复不刻意重放；所有页面历史恢复仍需整体验证 |
| 按钮、可点击卡片 | 按下opacity .78或共享Button .8，120ms ease；释放恢复 | ui-foundation.css覆盖原生button，共享Card只有可点击时创建button；静态article无按下反馈。没有增加全页缩放 |
| 不可用按钮 | .48透明度，不响应提交 | 原生disabled；外观本身不能替代行为保护 |
| Modal | opacity与scale .96→1，220ms ease-out；关闭160ms | prototype-modal；完成关闭后卸载dialog并恢复触发焦点 |
| Bottom Sheet | translateY 100%→0，280ms ease-out；关闭220ms | 原生dialog，拖动条实际向下拖超过80px触发关闭；未保存表单仍经beforeClose决定是否允许 |
| 弹层遮罩 | opacity 0→1，220ms ease-out | 原生::backdrop，不独立创建覆盖层；dialog移除时遮罩同时移除，当前不单独播放遮罩退出动画 |
| Toast | opacity淡入淡出160ms，显示2600ms | 非阻塞live region，无缩放；普通提示在底部导航之上，错误在顶部。长文与键盘布局覆盖仍需逐页检查 |
| Spinner | 900ms线性旋转 | 仅共享Loading的spinner模式；Skeleton无闪烁，Progress根据任务值变化，非任意循环进度 |
| 收藏、喜欢 | 状态/文字即时更新，普通按钮按下反馈 | 当前未增加单独弹性缩放；后续不以动效代替真实收藏结果 |

## 减少动态效果

- 系统prefers-reduced-motion与“我的→设置→显示与外观→减少动态效果”任一启用，关闭页面进入、Modal/Sheet进入和关闭过渡、遮罩淡入、Toast过渡、共享Spinner旋转。状态、等待说明、Loading任务本身仍保留。
- 应用偏好由dujia-prototype-preferences.reduceMotion持久化，页面加载时写入html属性；设置页面保存时立即更新属性。应用属性规则同时覆盖::before、::after、::backdrop。
- 关闭逻辑依设置使用0ms卸载延迟；取消关闭、焦点恢复、浏览器返回与任务数据语义不应因减少动效而改变。
- 当前没有证明所有跨标签页偏好更新立即同步，也没有原生设备验证；这些不能按HTML检查自动认定完成。

## 本阶段证据

verify_motion.py有六项检查：日记编辑页进入及结束后布局、Modal/Sheet与遮罩时长和关闭焦点、系统减少动效、已保存应用偏好、普通与减少动效下实际鼠标拖动Sheet关闭。实现前页面和遮罩两项缺失；其他四项原行为已通过。首次观察器选取多个按钮的错误另存motion-observer-error.json，不算产品缺陷。

当前结果见evidence/current/motion-results.json。该证据验证共享层及一个实际编辑入口，不代表114页全部状态的视觉、历史、键盘、触屏手势或Android验收已完成。
