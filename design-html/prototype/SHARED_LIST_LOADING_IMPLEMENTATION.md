# 共享列表Loading接入

## 实际修改

复用PrototypeUI.components.loading({mode: skeleton})，覆盖搜索、日记、相册、时刻、纪念日、胶囊、我的创作、草稿箱、宠物照顾、宠物成长10个load函数。保留原文案、400ms本地等待、aria-busy及既有刷新禁用/恢复逻辑，保留各模块现有失败/重试与最终绘制。没有引入API、状态框架或新画板。

宠物现有.pet-load为居中flex层。成长页的原稿绝对定位段落让新Skeleton根宽度收缩为32px、子行宽度0。五宽度实测发现后，在既有prototype-pet.css将共享Loading限制为min(100%,360px)，其段落恢复普通流，避免原画板段落定位影响状态提示。规则仅作用于宠物加载层。

## 有限验证范围

verify_shared_list_loading.py：10处×正常/空数据/失败重试=30项；观察真实400ms过程中插入的status/live、3条aria-hidden Skeleton、aria-busy、原有刷新禁用与恢复。相册/时刻/纪念日集合为空时验证原独立空页面和CTA，没有虚构其Loading。

verify_shared_loading_widths.py：10个实际加载页面×320/360/390/414/430=50项；检查根容器横向范围和三条Skeleton正尺寸及边界。此前45/50，宠物成长5个宽度均失败，原报告已保留；修正后结果写入当前报告。此检查不替代整页安全区、键盘、焦点、长文和原稿视觉验收。

原30项修改前报告：1项通过，27项缺少共享Skeleton，2项空页面CTA测试定位错误。后者修改测试后仅重放3条空页面，3/3通过，原报告未覆盖。接入后首轮30/30通过；几何修复后的实际终轮与运行清单，以shared-list-loading-checkpoint.json记录为准。

## 证据维护

原源码、运行清单、组件/Token观察及初始控件checkpoint保留在evidence/history/pre-shared-list-loading-6284939。由于全局产品指纹改变，752条旧初始控件、13条账号删除与旧隐藏专项均保持历史属性，等待组件集中迁移后复验。当前新增Loading和运行观察独立绑定当前指纹；没有用视觉或DOM观察宣称点击流程终验。114页最终验收仍为0。

下一步：列表Empty/Error、局部表单/卡片/头像/标签/分隔线与Token按实际控制器和原稿约束接入或明确保留理由；再集中复验主要连续流程和异常矩阵。
