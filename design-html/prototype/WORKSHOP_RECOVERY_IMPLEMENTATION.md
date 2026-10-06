# 工坊作品集合的结构恢复

## 实际问题与修复

18项基线全部失败，包含3次脚本错误：原UI.read会将坏JSON回退为无作品，正常保存可能覆盖原文；作品null／重复ID／错误正文和素材引用未经过结构检查。问题来自所有模块共享的作品读写，而不只来自工坊列表。

PrototypeUI现在提供workHealth与recoverWorks，UI.read在读取dujia-prototype-works时使用同一个结构分析结果。完整原文保持在localStorage；读取仅提供可用作品视图，不自动修复或写回。受损工坊集合暂时停止普通写入，明确提示“请先恢复作品，当前输入尚未保存”；其他健康集合继续保留原协议。

| 数据条件 | 可读视图与明确恢复 |
| --- | --- |
| 坏JSON／错误根结构 | 可读作品为空，原文不变；不是自动清空 |
| null／缺失ID／重复ID | 无法标识的条目暂不展示，重复保留第一条；完整原文仍在副本 |
| 错误name／story | 稳定ID保留，无法读的文字恢复为空；原始字段仍完整在副本 |
| 类型／状态不正确 | 恢复为漫画、自由来源或草稿；不伪造完成结果 |
| 错误sourceIds／共同主角 | 保留字符串素材ID和主角文字字段；不可读部分仍在副本 |
| 非数字时间／生成截止早于开始／错误结果标记 | 无效时间字段不用于生成；生成中作品恢复为保留输入的草稿 |
| 健康作品／没有作品集合 | 正常结果和fallback保持，不产生副本或恢复提示 |

恢复入口复用共享Button和Modal，可稍后处理、导出完整原文、重新检查或继续恢复。最终危险确认之后再次比对原文，先保存dujia-prototype-work-recovery-*原始字符串副本，再次比对，最后替换集合。副本空间不足不替换；替换失败保留原文及已经成功保存的副本。重试可能产生多份相同原文副本，不删除已保留副本。

无效生成时间不会自动转成ready。已有健康生成时间仍保留原3秒演示及离开后推进。作品内容源可见性、全部日期语义及跨窗口编辑冲突继续在I-03／I-04跟踪。

## 恢复顺序与编辑保护

联合损坏专项发现：工坊列表没有读取日记时，workHealth检测到坏记录后搁置自动作品恢复，但旧记录观察器也未被触发，导致顺序停住。现在主动触发原记录观察入口，依次恢复资料、记录、作品；恢复作品按钮也先调用已有高优先级恢复入口，原文不被替换。

恢复发生在正在编辑的工坊表单时，同URL重载继续经过原guard。选择继续编辑后输入保留；随后正常暂存仍使用原作品ID。没有新建未保存确认协议。

原始副本历史复用现有“数据与存储→存储空间管理→查看恢复原始副本”，增加工坊副本识别及说明；实际再次下载仍取得完整原始字符串，不导入、不覆盖当前作品。

## 当前证据

| 范围 | 项数 | 报告 |
| --- | ---: | --- |
| 6种损坏 × 工坊首页／历史／结果页 | 18 | workshop-recovery-results.json |
| 配额／竞争／dirty／重新检查／原文再次下载／不可用存储／健康保持／嵌套主角／生成时间与标记／7个其余状态页／五宽度 | 26 | workshop-recovery-state-results.json |
| 工坊10页全部声明fixture初始控件 | 92 | workshop-controls-results.json |
| 既有隐藏分支／五宽度／正常和异常业务流程 | 33 | workshop-hidden-results.json、workshop-control-layout-results.json、workshop-flow-results.json、workshop-state-results.json |
| 资料恢复／记录恢复／Sheet未保存保护／18类危险入口／回忆册全局联动 | 76 | workshop-recovery-regression-source.json引用报告 |
| 两条实际注册用户的八模块和时间连续流程 | 2 | product-journey-results.json、time-product-journey-results.json |

共247项按当前151份产品文件约束，来源、文件哈希及HTTP字节一致性见workshop-recovery-checkpoint.json。独立114页空／有数据观察228次，观察和回调绑定不计入247项实际检查。所有失败开关、配额/并发注入及数据fixture只在隔离浏览器context使用，用户应用内浏览器数据不变。

五宽度为320／360／390／414／430px，34px底部安全区；恢复入口实际中心命中、键盘Enter打开、取消默认焦点和Escape关闭，原文不写回。320px稳定截图人工确认文本换行及按钮完整可见。这个范围不代表114页全部状态视觉或虚拟键盘终验。

### 观察诊断保留

- workshop-recovery-first-fix-diagnostic.json：一次读取副本时与页面重载竞争；当前恢复成功步骤先等待真实load。
- workshop-recovery-state-first-diagnostic.json：测试恢复原生Storage方法时返回函数，Playwright尝试调用导致Illegal invocation；当前恢复方法用无返回值函数包裹，原产品配额保护未改变。
- workshop-recovery-priority-diagnostic.json：联合恢复顺序的真实缺陷，已修复并重新通过。
- workshop-recovery-capture-before-list-ready：最初截图底层列表还处于550ms Loading；当前等待实际aria-busy结束和字体就绪后截图。
- 原阶段证据和被覆盖图片保留evidence/history/pre-workshop-recovery-2651f8a，各报告保留自身files／source；目录HEAD不是所有历史报告的测试来源。

## 尚未完成

114页仍partial，0页最终验收，目标继续。时刻、纪念日、胶囊、宠物、回忆册和设置集合的完整结构／语义／引用恢复仍未全量完成；工坊来源引用、未来时间及其他编辑竞争也仍待核查。损坏集合暂不可读与“已删除”的底层详情措辞、其他错误组件一致性继续在I-05检查。本批不宣称全部数据恢复、全部状态或完整产品终验。

复查顺序：

```powershell
python design-html/prototype/verify_workshop_recovery.py
python design-html/prototype/verify_workshop_recovery_states.py
python design-html/prototype/verify_workshop_controls.py
python design-html/prototype/verify_workshop_hidden.py
python design-html/prototype/verify_workshop_control_layout.py
python design-html/prototype/verify_workshop_recovery_regressions.py
python design-html/prototype/audit_current_runtime.py
python design-html/prototype/verify_workshop_recovery_checkpoint.py
```

保留既有baseline；产品源码变化后重新执行相关检查，不修改旧来源使其看起来属于当前版本。
