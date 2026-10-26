# 当前提交、返回与选图等待边界

后续补证：本文末尾原列为待办的动态列表G2已另以190项通过，见[CURRENT_LIST_STATE_CONTRACTS](CURRENT_LIST_STATE_CONTRACTS.md)。当前剩余以41项表为准，本文270项执行范围保持不变。

41项审计发现，旧提交保护报告之后共享UI及多个编辑器已有变化。本批仅复验这组具体风险，未修改产品代码，也未重复初始控件或截图采集。

## 实际结果

| 原入口脚本 | 检查数 | 结果 |
| --- | ---: | --- |
| verify_pending_form_cancel.py | 96 | 通过：16弹层表单的取消／继续等等待边界 |
| verify_pending_form_contract.py | 8 | 通过：合成共享表单合同 |
| verify_pending_page_guard.py | 52 | 通过：整页任务等待时返回／继续／放弃 |
| verify_pending_guard_contract.py | 12 | 通过：合成共享页面合同 |
| verify_submission_changes.py | 19 | 通过：等待中继续编辑、日期选择、保存／生成竞争 |
| verify_capsule_date_pending.py | 3 | 通过：日期提交关闭／继续／输入锁定 |
| verify_image_pending_exit.py | 36 | 通过：6编辑器的仅换图退出、继续、失败与放弃 |
| verify_file_chooser_pending.py | 24 | 通过：8真实上传入口的chooser前提交保护 |
| verify_file_chooser_started.py | 4 | 通过：合成共享chooser合同 |
| verify_pending_image_reads.py | 16 | 通过：8保存入口的原生读取／解码等待 |

合计270项，其中246项来自实际页面操作案例，24项是合成共享辅助合同，不是270个页面。实际编排进程43692退出0，十个子进程均退出0。按原脚本精确控制550ms等待／原生解码释放，检查取消不迟到写入、继续编辑不丢值、明确重试及已有操作开始后的保护；不假称所有计时器都是真实壁钟等待，也不假称验证了操作系统文件窗口或真实移动IME。

## 报告隔离与真实失败记录

首次进程49922被Windows的报告文件写入EINVAL打断，只留下4项已通过观察，没有完成一组，也不计入本批270项。旧报告已从执行前字节恢复，诊断与实际旧编排脚本保存在`submit-boundary-refresh/forms/`。

随后使用`run_suite_report_isolated.py`，只把指定QA JSON报告重定向到独立路径，并用临时文件原子替换和有限文件访问重试；不替换页面操作、业务存储或断言结果。新结果与日志保存在`evidence/current/submit-boundary-refresh/`，旧报告和PNG逐字保持。成功案例没有新增截图时不复制旧截图冒充本次执行。

`refresh_submit_boundaries.py`保留逐组真实退出、源码／CSS／脚本／报告SHA；`verify_submit_boundary_refresh.py --session 43692 --exit-code 0`核对270项及原证据保持，检查点为同目录`checkpoint.json`。

## 对原目标的影响

这组明确的提交边界缺口已补证，原41项仍完整保留。动态列表状态、隐藏控件与导航条件对应、Toast反馈专项及人工原稿对照分别见[ACCEPTANCE_REQUIREMENTS](ACCEPTANCE_REQUIREMENTS.md)的G2–G5；没有以本批270项替代全114页终验。
