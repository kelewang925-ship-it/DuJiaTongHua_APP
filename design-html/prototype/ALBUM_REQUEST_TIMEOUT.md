# 工坊相册请求超时与恢复

本批修复原提示词Error State中的“请求超时”缺口。此前实际挂起图片HTTP响应后，保存持续禁用。仅修改`assets/prototype-workshop-store.js::decodedImage`，不改页面、CSS、数据结构或后端边界。

## 实际执行

| 检查 | 结果 | 证据 |
| --- | --- | --- |
| 修改前真实HTTP挂起 | 1通过、2失败；超时后按钮未恢复 | evidence/baseline/album-timeout/results.json；进程73490退出1 |
| 修改后三个原生请求案例 | 3通过，明确重试只存一次，迟到不写入，正常慢响应成功 | evidence/current/album-timeout/results.json；进程12936退出0 |
| 修改范围 | 函数外代码一致；两处私有调用均属于album，唯一应用调用来自m05-p08 | evidence/current/album-timeout/source-scope.json；静态检查，不替代运行验收 |

测试采用Chrome、私有浏览器上下文、390×844 CSS px、真实Image.decode及真实计时器；路由仅控制本地图片HTTP响应何时返回，不替换解码Promise。390×844是本次条件，未据此认定最终截图基准。

## 产品行为

图片准备15秒未完成即失败，提示“图片准备超时，请重试保存”，恢复按钮并取消该图片来源。原内容保持，用户再次点击才开始新任务。成功及普通失败均清理计时器。既有来源校验、并发检查、相册去重和容量失败保护继续复用。

## 相关回归与证据边界

受影响范围按现有测试复验：原生解码10项、工坊控件92项、正常流程3项、状态8项、八模块22阶段连续流程1项。114项全部通过，实际进程4316退出0；执行结果记录于`evidence/current/album-timeout/regressions.json`。`verify_album_timeout_checkpoint.py`核对报告、脚本、源码、原证据保持和HTTP实际服务字节，通过结果见`evidence/current/album-timeout/checkpoint.json`。

旧报告和截图保留原字节及原源码指纹；不改哈希冒充重新执行。单函数范围检查仅证明变更边界，不能证明全部动态条件。114页完整目标仍执行中；人工视觉验收人和黄金页面名单待核实，不宣称已通过人工验收。
