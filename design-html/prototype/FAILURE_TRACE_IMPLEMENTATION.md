# 失败操作实际追踪记录

## 结果与边界

五组共30个案例通过：宠物7、回忆册6、照片4、设置9、登录关联4。测试侧包装PrototypeUI.failNext，记录其实际返回true的操作名、URL和浏览器上下文序号，再关联原测试案例。没有修改151份产品源码。

实际26个不同失败操作已经触发，其所属案例断言通过：61个字面量候选中17个、动态入口另外9个。44个字面量候选未追踪，见FAILURE_OPERATION_MATRIX.md与对应JSON。静态引用只帮助寻找测试入口，不计作执行；已观察也不能外推为操作的全部权限、取消、超时、并发或布局验收。

照片案例还实际验证坏图片显示修复、换图后解码成功、加载失败重试、保存配额失败保持输入、留言及删除失败。这些语义断言来自verify_photo_states，失败钩子矩阵仅计其中实际触发的3个操作。

## 发现并修复的测试问题

1. 旧照片missing-photo案例等待有照片的m03-p10，但其独立上下文无记录，原型按既有规则重定向空相册m03-p09。保留原失败报告；改为断言空相册和添加入口实际到m03-p11。没有改变产品路由。
2. runpy原先透传追踪器参数，导致带argparse的登录脚本退出2。隔离被执行脚本的sys.argv并在finally恢复。前三份实际成功报告对应原v1追踪器，已保存原脚本字节并显式记录路径，不用新脚本哈希冒充旧执行。
3. 环境更新时预览服务停止，两组重试连接拒绝。确认无监听和原进程不存在后重开前台托管服务，会话64724；受影响报告归档，再执行照片和登录组，两组退出0。隐藏进程启动被工具策略拒绝，改用可观察的前台会话运行服务器。

## 可核对资料

- evidence/current/failure-operation-matrix.json：来源、逐操作实际事件、静态候选和未追踪项。
- evidence/current/*-failure-trace.json：事件与案例索引、脚本及报告哈希、实际子脚本退出码。
- evidence/current/failure-trace-executions.json：真实终端会话，包括失败父进程与最终受影响组的重跑。
- evidence/history/pre-failure-trace-7958d1f：旧报告、v1追踪器、旧照片断言与环境失败。

build_failure_operation_matrix.py核对所有最终报告通过、事件关联、脚本／报告哈希、当前151份源文件和HTTP提供字节。未启动真实服务/API或RN迁移。最终验收仍0页；目标继续。

## 前轮换行判断更正

对旧time-controls Git LF字节重建CRLF后，SHA256为d1d6bb46dea88e1582c9afd1f4701e9f40c68b540fffbde8f6f194cd5c43abfb，与原检查点完全一致。原先“报告引用不一致”属比较口径错误，已在EXCEPTION_REGRESSIONS_REFRESH更正。本轮用局部.gitattributes固定追踪器、对应报告和v1脚本的精确字节；其余源码不做换行改写。
