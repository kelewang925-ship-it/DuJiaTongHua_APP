# 当前动态列表Empty、Error及Loading复验

原41项G2发现，旧列表状态报告之后直接控制器和CSS存在变化。本批按原三组明确范围重新执行，产品HTML/CSS/JS保持不变。

| 入口脚本 | 实际范围 | 结果 |
| --- | --- | --- |
| verify_shared_list_states.py | 22个Empty／Error上下文×5宽度，实际CTA、清筛选、重试及几何 | 110通过 |
| verify_shared_list_loading.py | 10个实际load函数×空数据／有数据／失败重试，观察真实400ms瞬态Skeleton和语义 | 30通过 |
| verify_shared_loading_widths.py | 同10个Skeleton表面×5宽度的边界与正尺寸 | 50通过 |

实际进程73435退出0，三个子进程均退出0，合计190项；不是190页。五宽度使用原脚本320／360／390／414／430，具体fixture和高度保持原脚本声明，不将它们确认为项目最终视觉基准。

记录覆盖搜索、日记、照片、时刻、纪念日、胶囊、创作集、草稿箱、宠物及成长故事等声明场景。静态空稿如空书架、未领养、相册空态的创建入口另有原初始合同与主链证明，不因为没有列入这一组而声称缺失，也不将本组扩张为所有动态页面。

通过`run_suite_report_isolated.py`仅重定向QA报告，不替换计时器、页面操作或业务结果。三份旧报告字节SHA保持，当前新报告／日志保存在`evidence/current/list-state-refresh/`；执行、脚本、源码、全部CSS及原报告保持由同目录`executions.json`和`checkpoint.json`记录。

G2这组明确补证已完成。G3隐藏动作对应、G4Toast以及G5人工原稿对照仍按[ACCEPTANCE_REQUIREMENTS](ACCEPTANCE_REQUIREMENTS.md)执行；没有用190项局部自检宣称完整目标达成。
