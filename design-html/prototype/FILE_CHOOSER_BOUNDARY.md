# 选图结果尚未返回时的提交保护

## 已复现问题与修复

P1 `FILE-CHOOSER-PENDING-01`：UI只监听文件change，选图请求已经打开但尚未选中文件时，旧保存仍会写入并离开。日记、照片顶部完成、个人资料与补页的4项基线均复现。

P1 `FILE-CHOOSER-STARTED-01`：受保护的业务回调已经开始、尚未commit时，文件入口仍可打开。2种保护范围×成功／失败的4项共享基线均观察到打开事件。

共享UI沿用同一submissionScope，在捕获阶段监听文件click和change：

- 等待提交时点击文件入口，立即取消旧任务，再打开选图。
- 回调已开始且未commit时，提示正在完成保存并阻止文件点击默认行为；操作结束后恢复入口。
- change继续覆盖直接选择文件的既有路径。

取消选图不恢复旧提交；字段和原图保持，需明确重新保存。新选图成功后保存新图，解码失败保留原图及字段。

## 当前实测

| 检查 | 当前结果 |
| --- | --- |
| 8个实际保存入口×选图取消／成功／解码失败 | 24/24；先接收Chromium filechooser事件，在未返回任何文件前释放保存等待，确认不写入且字段保持，再明确保存并刷新 |
| 操作开始后的文件激活 | 4/4共享夹具；不同root结构下不打开选择请求，成功／失败后入口恢复 |
| 原有文件change路径 | 16/16原生读取／解码成功／失败回归通过 |
| 合计 | 同源码44项：40项实际任务／图片观察、4项共享夹具；HTTP字节及114份页面镜像核对通过 |

实际入口为日记发布／顶部草稿、照片正文保存／顶部完成、时刻封面、胶囊草稿、个人头像及回忆册补页。通过原按钮或label触发文件输入；没有直接替换业务保存函数。空文件选择模拟取消，真实有效SVG／损坏数据验证成功和原生解码失败。

共享夹具用可控异步操作区分等待与已经开始，不把4个夹具计为实际应用页面，也不声称锁定了所有类型的编辑。

## 证据与运行

- evidence/baseline/file-chooser-pending：4项旧失败及9bc47dc原UI脚本。
- evidence/baseline/file-chooser-started/results.json：4项共享旧失败。
- evidence/current/file-chooser-pending/results.json：24项当前结果。
- evidence/current/file-chooser-started/results.json：4项当前共享结果。
- evidence/current/pending-image-read/results.json：16项当前change回归。
- evidence/current/file-chooser-pending/checkpoint.json：原始／当前源码和报告哈希、实际执行引用、HTTP字节与页面镜像核对。

串行运行verify_file_chooser_pending.py、verify_file_chooser_started.py和verify_pending_image_reads.py，然后执行verify_file_chooser_checkpoint.py。--baseline用于记录旧失败，默认当前模式检查完整24／4项。

## 边界与后续

验证的是headless Chromium的实际文件选择请求事件；未展示或实测Windows／手机原生文件窗口。保护范围内的文件入口已有上述阶段契约，业务回调开始后的普通文本编辑、共同头像的权限／资料变化、其他来源与异常仍需继续审计。

旧96／46／234等完整矩阵保留原源码指纹；本批只将44项建立为当前证据，最终运行／目录／布局／连续流程在阶段状态修复完成后统一回放。114页最终验收0页，完整目标继续。
