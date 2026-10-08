# 全114页初始控件当前复验

## 范围与来源

本阶段在5b71c64之后复验剩余532条历史初始控件：时间54、工坊92、设置81、宠物151、回忆册154。产品HTML/CSS/JS保持不变，沿用登录与关系82、记录92、时刻46条当前初始控件证据。

refresh_initial_controls.py顺序执行既有验证器，每个控件使用独立浏览器上下文。初始环境和契约以各模块验证器为准；并未穷举所有业务条件。运行前后冻结151个产品文件，记录实际子进程退出、报告SHA、当前源码、每条成功和脚本错误数。旧报告和目录保存在evidence/history/pre-initial-refresh-5b71c64。

## 验证与目录更新

执行结果以initial-controls-refresh-source.json为准。build_page_contracts.py重建每页控件报告索引、当前落点、状态需求和队列；verify_page_contracts.py核对114页、267资源、228观察和1696条观察控件；verify_initial_controls_refresh.py核对所有五组实际退出与报告来源。最终检查点为initial-controls-refresh-checkpoint.json。

结果：五组532/532通过，实际子进程及运行进程退出0、0脚本错误。更新后全部752条初始控件对应当前源码、历史0；114页、267资源、228观察、1696观察控件以及767条不同导航记录保留。产品源码未改变。

## 实际限制与继续工作

初始控件通过仅证明对应种子环境、操作及契约。隐藏弹层、不同入口返回、失败/取消/空状态、组件和Token适用、五宽度与键盘状态仍按41项交付审计继续。114页flow_verified保持false，最终验收为0。INTERACTION_RULES更新过时的已实施范围描述，未改变产品行为。
