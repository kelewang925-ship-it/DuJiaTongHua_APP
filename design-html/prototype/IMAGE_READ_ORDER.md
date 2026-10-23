# 连续换图、移除与失败保留

## 已确认问题

原始249b5b7源码的16项旧图晚完成／旧请求晚报错／移除后完成检查全部失败；另7项旧请求先完成检查也全部失败。旧回调会覆盖最新图片、显示过期错误或提前清除最新请求的读取标记，移除后还可能重新填回图片。

- P1 `IMAGE-REQUEST-ORDER-01`：7个图片入口的过期完成／错误干扰最新选择。
- P1 `IMAGE-REMOVE-REVIVE-01`：日记和胶囊移除后，尚在读取的图片恢复。
- P1 `BOOK-IMAGE-RETAIN-01`：补页替换图片失败会清空已有有效图片；继承旧行为的首次helper版本补测复现1项失败。

## 修复

在既有PrototypeRecords.readImage旁复用同一原生读取／解码工具，增加imageInput绑定：每个input保存自己的请求序号，只有最新请求可以回填图片、显示错误或清理reading状态。cancel使在途请求过期；日记和胶囊移除同时调用cancel。已经开始的原生读取允许结束，其过期回调不再影响页面。

7个入口统一接入：日记、照片、时刻封面、胶囊、个人头像、补页图片与共同头像。各页原有onValue／onError／onBusy回调保留业务落点与反馈；公共helper仅协调顺序。补页新图解码失败时保留原有效附件及预览，提示原照片仍保留。

## 当前实测

| 条件 | 当前结果 |
| --- | --- |
| 第二张先完成，第一张稍后成功 | 7/7，最新图片保持，保存与刷新一致 |
| 第二张成功，第一张稍后报错 | 7/7，不覆盖新图，不显示旧错误 |
| 第一张先完成，第二张仍在读取 | 7/7，不清除最新读取状态；手动保存仍被阻止，共同头像不提前写入 |
| 原图有效，最新替换图失败 | 7/7，保留已有有效图片，保存／刷新保持 |
| 日记／胶囊移除后旧读取完成 | 2/2，不复活，保存结果无图片 |
| 保存等待期间换图成功／解码失败 | 既有16/16重新执行通过 |
| 合计 | 同源码46项；114份HTML镜像及HTTP字节核对通过 |

使用真实FileReader与Image事件，按指定次序释放文件读取，观察真实预览、原生解码成功／失败、本地数据、业务保存与刷新。共同头像沿原有直接保存方式验证，没有把手动保存强加到该页面。23项首次helper检查是修复中间版本，不计入当前46项。

## 证据

- evidence/baseline/image-read-order/first-results.json：原始16失败，verifier-first.py为对应脚本。
- 同目录loading-results.json：原始7项读取标记失败，verifier-loading.py为对应脚本。
- 同目录results.json：首次helper版本的补页失败保留基线；verifier-retain.py和book-editors-before-retain.js保留对应输入。
- evidence/history/image-order-before-retain-fix：23项中间结果，明确保存当时源码指纹。
- evidence/current/image-read-order/results.json：当前30项顺序／移除／保留结果。
- evidence/current/pending-image-read/results.json：当前16项保存等待回归。
- evidence/current/image-read-order/checkpoint.json：来源／脚本／报告哈希、实际会话与静态HTTP／镜像核对。

运行verify_image_read_order.py和verify_pending_image_reads.py，之后执行verify_image_order_checkpoint.py。首组原源码执行249b5b7，补页保留基线来自尚未提交的helper草稿；两者分别记录，不能把中间23项当成最终源码已覆盖全部条件。

## 继续审计

仅换图且仍在读取时的返回保护、原生选图对话框尚未选文件、业务回调开始后的编辑、共同头像的权限／资料变化及其他异常仍未终验。旧47项、234项完整矩阵保留各自源码指纹，完整运行／目录／初始布局／连续流程待阶段状态审计后统一复验。最终验收0页，完整目标继续。
