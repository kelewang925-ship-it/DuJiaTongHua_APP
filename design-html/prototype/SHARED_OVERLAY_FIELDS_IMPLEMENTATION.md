# 弹层共享Input/Textarea/Select接入

## 修改

复用既有components.field：设置通用edit、宠物成长edit、回忆册edit、时刻回应、宠物小心情五个构建函数采用统一字段。保留原值、字数/类型/必填规则、提交回调、protectSheet未保存保护、失败与重试。回忆册edit、时刻回应和宠物小心情的提交按钮同时复用共享Button。原稿内联表单和回忆册其他编辑器仍待单独处理。

工厂新增可选options数组以生成原生select，仍返回root/input/error/setError。选择器共用字段边框/padding/focus/disabled基础规则；不把maxlength错误施加到select。UI.fieldError在没有显式existing时优先使用当前共享字段的错误节点，维持aria-invalid和aria-describedby；字段input事件清除关联错误。显式错误节点和其他非共享字段的Toast回退保留。

## 实际验证

14个弹层入口：时刻回应、共同昵称、新建标签两个入口、动效、手机号、两步验证、反馈、宠物小心情、成长故事两个入口、故事回应、宠物提醒时间、回忆册名称。在320/360/390/414/430下实际输入、行内错误、错误纠正、重复提交、QuotaExceededError保留所有存储/候选输入、重试后检查实际保存结果，70项；另1项Select原生选项/初值/disabled与关联错误清除契约，共71项。修改前15项未通过共享字段检查，基线保留。

账号/宠物身份删除13项当前执行：成功、空白/错误身份、脏输入取消、语义失败重试、配额失败重试及账号第二次写入失败回滚。首轮10/13通过；3项仍查找旧Toast，但页面已按本批规则显示行内关联alert。原结果保留，修正测试位置后仅重放这3项，其余10项不变观察保留。测试没有修改生产源码或超时来迎合检查。

旧hidden-overlay-observations仅提供定位候选：字段与身份测试会重新进入页面/实际弹层、核对标题和字段并执行存储断言，不能据旧目录宣称隐藏状态已当前观察。身份脚本新增显式--locator-candidates模式；默认模式保留原严格源前提。候选模式仍核对未变HTML、完整现源码与HTTP字节、所有实际身份操作和边界；报告记录旧源差异和新源指纹。

实际终轮退出与报告/脚本/源哈希见shared-overlay-fields-checkpoint.json，校验入口verify_shared_fields_checkpoint.py。该专项不证明全部字段maxlength边界/blur/焦点/键盘、安全区或所有114页布局终验。全量运行/目录、752条初始点击及旧Card/Loading/状态证据保留历史属性，组件集中接入后刷新。

## 下一步

原稿内联Input/Textarea与其他编辑器、Header/Avatar/Tag/Divider、局部Token/明确保留理由继续；集中刷新114页清单、完整主要流程和适用失败矩阵。114页最终验收仍为0。
