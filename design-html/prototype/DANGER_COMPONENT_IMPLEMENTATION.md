# 共享危险确认组件接入

当前共享源码已加入工坊作品恢复；本文件保留此前阶段范围与结果，不能替代最新全产品终验。当前247项及同源证据见[WORKSHOP_RECOVERY_IMPLEMENTATION](WORKSHOP_RECOVERY_IMPLEMENTATION.md)，此前被覆盖报告／图片保留evidence/history/pre-workshop-recovery-2651f8a，各文件保留原来源。

## 实现范围

审查当前全部带明确title的Modal调用，共51处：15处最终危险确认显式传入`danger:true`，其余38处保留普通确认或选项行为。字面调用清单见`evidence/current/danger-modal-callsite-inventory.json`；它不计Sheet、表单及动态展开，也不代表交互已执行。

| 最终操作 | 实际入口 | 接入方式 |
| --- | --- | --- |
| 删除日记／照片 | m03-p08／m03-p12 的更多菜单 | Modal danger |
| 删除时刻／纪念日／胶囊 | m04-p03／m04-p10／m04-p14 的更多菜单 | Modal danger |
| 删除作品 | m05-p08 更多 | Modal danger |
| 删除回忆册／章节／书页 | m08-p21 显示删除；m08-p13 章节／页面操作 | Modal danger；章节／书页仍在保存后持久化 |
| 删除标签／请求解除关联／清理浏览记录缓存 | m06-p05 标签菜单；m06-p03 解除；m06-p11 缓存 | Modal danger |
| 恢复记录／恢复资料 | 损坏数据恢复选项→保留原始副本并恢复 | Modal danger；取消返回恢复选项，原始数据不变 |
| 放弃页面修改 | guard dirty 返回 | Modal danger；继续编辑保留输入 |
| 放弃Sheet修改 | protectSheet beforeClose | 同一Sheet内共享Secondary／Danger按钮；不新增弹层 |
| 注销账号／永久删除宠物 | 身份确认Sheet／输入宠物名字Sheet | 共享Danger表单提交；保留原校验、Loading、失败重试 |

共有18类实际入口。共享按钮工厂统一设置`data-variant=danger`和`data-danger=true`；Modal显式选项决定最终按钮变体，危险按钮不设置`data-primary`。Dirty Sheet、设置编辑与宠物编辑复用同一工厂。局部表单继续保留原边框、圆角和排版，危险文字和纸色背景使用共享token，热区至少44px。

`modal({title, cancel, confirm, danger:true})`只改变确认按钮样式；返回值、取消默认焦点、原生dialog、历史标记、关闭和beforeClose协议不变。业务代码必须明确传入danger，运行时不根据中文文字推断。普通身份确认说明、退出登录、暂停／恢复共同照顾、保留草稿取消生成仍采用普通确认，因为这些步骤不删除业务内容；实际注销和永久删除的最终提交采用Danger。

## 已复现与观察修正

基线`evidence/baseline/danger-confirmation-results.json`中18类入口均不符合共享危险按钮契约：15个Modal仍为Primary；Dirty Sheet、账号及宠物表单为独立按钮，颜色分散。第一轮三个选择器误用旧控件，另存`danger-selector-observer-diagnostic.json`；修正为实际更多／显示删除／页面操作后再采集18项基线。

修复后恢复确认的取消返回已有恢复选项，而不是直接关闭整个恢复流程。第一次观察器错误单独保留`evidence/current/danger-recovery-observer-diagnostic.json`；当前检查取消后选项仍可用，再点稍后处理，且存储完全不变。

最后的既有工坊取消测试出现一次ERR_ABORTED，旧报告／截图和失败包装器记录另存danger-workshop-deadline-original-*。单独延迟页面请求3.5秒可复现生成在取消弹窗打开前已完成并转结果页，表现为找不到取消按钮；这个复现证明原3秒fixture受加载耗时影响，没有证明与首次ERR_ABORTED完全相同的底层原因。测试现在预留加载时间，在实际取消Modal打开后设置并等待实际截止时间，仍断言截止后停留生成页、确认取消保留故事和draft；产品生成计时未改。延迟加载专项通过，再重跑完整32项产品回归。

## 验证与证据边界

| 检查 | 项数 | 证据 |
| --- | ---: | --- |
| 实际入口、Danger变体／class／token、取消默认焦点、不写存储 | 18 | danger-confirmation-results.json |
| 14类普通确认的Escape／遮罩／浏览器返回；直接入口恢复触发焦点 | 42 | danger-overlay-results.json |
| 删除确认／账号身份表单／宠物名字表单／Dirty Sheet × 5宽度 | 20 | danger-overlay-results.json、danger-layout截图 |
| 普通说明、退出、暂停及普通编辑仍采用Primary | 5 | danger-primary-contract-results.json |
| 设置流程／状态、宠物状态、章节／书页、记录恢复、资料恢复回归 | 72 | danger-regression-source.json引用6份报告 |
| 工坊取消测试在3.5秒延迟加载后仍跨过实际截止时间并保留草稿 | 1 | danger-workshop-delayed-load-results.json |

新增范围共158项，覆盖320／360／390／414／430px、34px底部安全区、按钮完整可见、无水平溢出和Tab／Shift+Tab循环。截图人工查看320px账号、Dirty Sheet和删除按钮完整显示。使用隔离浏览器上下文与声明fixture，不修改用户在应用内浏览器的数据。此阶段五宽度检查使用减少动效，不构成所有正常动画、虚拟键盘或全部隐藏状态的终验。

共享UI涉及历史和关闭行为，因此另按当前源码重跑此前165项时间/八模块连续流程与相关回归。最终同源检查见`danger-components-checkpoint.json`：323项，另有全114页空／有数据共228次观察、HTTP页面及共享资源字节核对。观察与字面调用清单不计入323项实际检查。所有报告由同一151份产品文件哈希约束，未加总旧提交测试结果。

旧报告及被覆盖图片保留`evidence/history/pre-danger-components-5249d75/`。目录名标记本轮开始的HEAD，不声称里面每个旧报告均产生于该提交；其原files／source文件保留。历史副本只保存报告及本轮会覆盖的图片。

114页依然全部partial、0页最终验收，I-01～I-07保持开放。此批覆盖当前识别的最终危险确认；其他局部表单／Empty／Loading组件、集合恢复、全部动态分支、视觉／可访问性／正常动效和历史恢复仍需继续。

## 复查顺序

在现有本地预览和验证依赖就绪后依次运行：

```powershell
python design-html/prototype/verify_danger_regressions.py
python design-html/prototype/verify_danger_overlays.py
python design-html/prototype/verify_danger_primary_contract.py
python design-html/prototype/verify_workshop_cancel_load.py
python design-html/prototype/audit_danger_modal_calls.py
python design-html/prototype/verify_time_journey_regressions.py
python design-html/prototype/verify_time_journeys.py
python design-html/prototype/audit_current_runtime.py
python design-html/prototype/verify_danger_checkpoint.py
```

保留已有baseline，产品源码变更后重新运行相关流程及最后的同源检查，不把历史报告改成当前证据。
