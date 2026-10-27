# 纪念日倒计时的完整数值排版

P2-VIS-COUNTDOWN自检修复，人工确认仍待。原稿使用单个3，实际日期产生80／365／3650时，固定45cqw与left37%让末位越界，并与独立定位的天字相撞。不能改写真实日期或截断数字来解决。

## 当前实现与范围

仅修改m04-p10及其预览镜像：把原有number和days两个节点包入同组；使用基线对齐、水平／垂直居中及随位数缩放的字号。单页初始化脚本在原控制器之后读取已计算数字的位数，只设置CSS变量。cqw随窗口改变，不需要额外resize事件或状态架构。

`verify_countdown_layout_checkpoint.py`移除精确CSS、显示初始化和包裹div后，与保存的原HTML逐字相等。原两个p节点、所有原脚本与按钮均保留；共享CSS／JS和其他页面字节保持。初始化不参与日期计算、存储、校验或导航。原日期范围及重复／过去日期逻辑保持。

## 实际检查

- session64394，exit1：五宽度320／360／390／414／430 × 1／80／365／3650／36500／365000／2000000／过去36500天，共40项。原布局5项通过、35项失败。
- session48678，exit0：47项首次通过，图像对照发现多位数组偏上；报告／截图保存在top-aligned，不把几何通过当作视觉完成。
- session54504，exit0：补齐共同区域垂直居中后47/47通过。含40组真实存储日期的数字／单位分隔、日历区域约束、日期避让与存储不变，原五个操作入口、窗口缩放、当天跳转各自复验。
- 真实日期从2026-10-05计算，repeat=false，七位2000000天仍在现有日期工具允许的年份内。没有直接改DOM数字来生成测试条件。
- Chrome headless，DPR1，zh-CN／Asia/Shanghai，reduce，视口高度844；报告记录实际浏览器版本。已查看最终390宽1、80、2000000天截图，完整数字与单位在日历内。

证据：[失败基线](evidence/baseline/countdown-value-layout/results.json)、[当前47项](evidence/current/countdown-value-layout/results.json)、[源码范围](evidence/current/countdown-value-layout/checkpoint.json)、[80天截图](evidence/current/countdown-value-layout/390-80.png)。原114张截图不覆盖，首次对照记录保留，m04-p10另加follow_up。

累计原稿自检仍50/114、人工0；日历静态圈12、胶囊提示遮挡、动态卡片纸张层次、字体及回忆册阅读等问题继续。旧业务报告原执行指纹保留，经显示范围校验连接到当前源，不冒充114页全量重跑。
