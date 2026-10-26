# 当前隐藏弹层与关闭路径复验

2026年10月26日恢复完整目标后，从已推送的7275a1a继续。产品HTML、JavaScript和全部CSS保持与初始复验检查点一致。本批只更新证据、校验脚本及交付说明。

## 已完成的实际执行

| 范围 | 数量 | 实际执行 | 结果 |
| --- | ---: | --- | --- |
| 候选直接触发观察 | 133 | session96097，退出0（上批已完成） | 99个实际弹层、250个隐藏控件；Escape关闭保持存储和焦点 |
| 无修改关闭 | 368 | session22336，退出0 | 按钮／浏览器返回／遮罩；Sheet另测下滑 |
| 修改后的关闭保护 | 64 | 同一432项关闭进程 | 继续编辑保持候选值，放弃不写入，保留底层页面及触发焦点 |
| 二层危险／身份确认取消 | 66 | session92693，退出0 | 22个入口×按钮／返回／遮罩；取消不写入，安全焦点恢复 |

关闭与二层取消合计498项，全部通过，无页面脚本错误。该数量不包括133次触发观察。全部既有752个初始合同仍由未变的产品／样式和原843项检查组合证明，不重复计入本批数量。

## 证据和修正

- `evidence/current/fresh-hidden-inventory-checkpoint.json`：133次观察、当前索引、实际种子脚本和原触发目录的SHA。
- `evidence/current/fresh-overlay-exit-checkpoint.json`：432项和66项的真实进程、报告与脚本SHA。
- `evidence/history/pre-overlay-exits-7275a1a/`：覆盖前的报告、状态、校验脚本和本次触发目录的原始字节。
- `HIDDEN_OVERLAYS.md`、`OVERLAY_EXIT_PATHS.md`、`HIDDEN_CONTROL_BEHAVIORS.md`：114页索引、关闭方法、隐藏控件的当前证据与剩余动作。

原隐藏目录校验器固定引用a75e9e0阶段目录，已实际复现其SHA校验失败。增加`--probe-catalog`选择本次原始目录，仍严格核对目录SHA、源码SHA和仓库内路径；旧默认值保留以支持历史复跑。正确目录的校验已退出0，未放宽产品验证。关闭校验器同时记录本批真实进程编号，替换旧状态中的执行编号。

## 复跑

先运行`audit_hidden_overlays.py`，保存真实进程号和退出码；使用`build_hidden_overlay_index.py`生成索引，再给`verify_fresh_hidden_inventory.py`传入`--session`、`--exit-code`和指向该次原始目录的`--probe-catalog`。

串行运行`verify_overlay_exit_paths.py`和`verify_nested_confirmations.py`，分别记录真实退出。运行`build_overlay_exit_summary.py`，然后给`verify_fresh_overlay_exits.py`传入这两个真实进程及退出码。本批汇总与HTTP源码核对为chunk9508d5，退出0。

## 验收边界与下一步

本批使用390×844、减少动效和各模块明确种子。浏览器返回验证原型的返回约定，不等于Android真机系统返回。未观察到弹层不代表其他条件不存在；关闭通过不等于保存、删除、选择回填或提交中取消已全部验证。

继续47项表单保存、45项记录删除、13项身份删除和25项候选编排删除；随后核对完整连续流程、全部命名异常、图片／提交竞争、组件／Token、五宽度、键盘和41项交付要求。114页最终验收仍为0，目标继续。
