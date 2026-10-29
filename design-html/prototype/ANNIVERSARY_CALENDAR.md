# 纪念日真实月历显示修复

P2-VIS-TIME-CALENDAR：m04-p07左侧已更新真实纪念日，右侧背景图仍画着旧数字和圈选12。日期计算本身并未在此问题中出错。

本次保留原插画、线圈、纸张、花朵和原有按钮，在日历纸面的数字区域覆盖可编辑HTML月历。仅本页加载的显示脚本复用PrototypeDates.parse，读取已有控制器输出的实际发生日期，绘制当月及选中日。它不新增日期状态、不写存储、不代替日期计算，也不增加不可用的点击控件。主标题和倒计时限制在左侧区域，避免与月历重叠。

## 实际证据

- [静态冲突基线](evidence/baseline/anniversary-calendar/results.json)：20个日期/宽度组合均缺少真实月历；已保留原源码和当时执行脚本。
- [最终39项](evidence/current/anniversary-calendar/results.json)：五宽度×六类日期30项，覆盖今天、六周月份、闰日、年度重复的2月29日夹取、9999年及过去日期；再执行原9个页面入口。检查真实月份/星期/完整天数/唯一选中、布局边界、原导航/提醒/刷新及存储行为。
- [最终6项更新流程](evidence/current/anniversary-calendar-updates/results.json)：刷新、失败重试、实际日期Sheet选择保存、实际页面返回、缓存生命周期模拟以及无效日期恢复。
- [范围核对](evidence/current/anniversary-calendar/checkpoint.json)：剥离声明的CSS、figure及本页脚本引用后，可逐字节还原原HTML；镜像相等。原插画、共享UI、纪念日控制器、日期工具保持原字节，脚本消费方只有m04-p07。
- 已实际查看[当前日期](evidence/current/anniversary-calendar/2026-10-05.png)、[闰日](evidence/current/anniversary-calendar/2028-02-29.png)、[远期日期](evidence/current/anniversary-calendar/9999-12-31.png)及[无效日期占位](evidence/current/anniversary-calendar-updates/invalid-placeholder.png)截图。390×844仍为临时检查条件。

## 修复中发现的显示层边界

第一版月历在pagehide时断开观察器，缓存恢复后没有重新连接；生命周期模拟复现左侧已刷新而月历未更新。补上pageshow重新观察后通过。模拟事件不等于真实设备缓存验收。

另补查无效日期：第一版直接隐藏显示层会再次露出旧背景数字，恢复相同日期也可能命中缓存。现改为明确的“日期待确认”占位并清除旧显示值，恢复有效日期后重新绘制。两个失败阶段及执行脚本保存在baseline/anniversary-calendar-updates与baseline/anniversary-calendar-invalid；34项和39项中间绿报告保留原源码指纹，不改称最终结果。

本批只自检修复该日历问题，其他字体、动态记录皮肤等差异继续。原稿自检114/114、人工验收0及全部页面验收维度保持，完整41项目标未完成。
