# 本地存储用量说明排版

P2-VIS-STORAGE-CARD已自检修复，人工确认仍待。m06-p11动态控制器在quantity里写真实本地字节数和small说明，共享CSS把small设成block，而quantity固定top48%。说明第二行进入原纸卡进度条的绘制区域。

只在m06-p11及其预览镜像增加两条更精确的单页CSS：用量略上移、字号随画板缩放，说明同行并复用现有字体Token。没有删除本地范围提示，也没有把真实用量改回设计稿的1.2GB／5GB。

原DOM、控制器、导出／备份／清理逻辑和全部共享资源字节保持。范围脚本删除精确CSS后与保存的原HTML逐字相等。原画进度条保留为装饰，没有给它增加真实浏览器配额或使用比例的语义。

验证：session88393 exit1，15项全部复现第二行进入进度条区域；session75022 exit0，21/21通过。五宽度320／360／390／414／430 × 原有本地数据／额外300000字／额外1500000字，共15组合，真实KB／MB格式按PrototypePreferences.bytes核对，读数不写入新数据；测试填充仅在私有浏览器上下文中。其余6项复验返回、真实导出下载、共同备份、自动备份切换、空间管理和清理确认入口。

比较保留原画板约52%高度开始的进度条区域，文字需停在51.5%之前；该几何条件辅以实际截图对照，不把它当成像素全图验收。已查看390宽4.3KB和2.9MB截图，说明位于条上方，标题／数值／条层次清晰。Chrome headless，DPR1，zh-CN／Asia/Shanghai，reduce，高844，版本见实际报告。

证据：[失败基线](evidence/baseline/storage-quantity-layout/results.json)、[21项结果](evidence/current/storage-quantity-layout/results.json)、[源码保留](evidence/current/storage-quantity-layout/checkpoint.json)、[2.9MB截图](evidence/current/storage-quantity-layout/390-1500000.png)。旧捕获与首次观察不覆盖，m06-p11另加follow_up。累计自检仍70/114、人工0，其他差异继续；旧报告保留原执行指纹，不冒充新源码114页全量重跑。
