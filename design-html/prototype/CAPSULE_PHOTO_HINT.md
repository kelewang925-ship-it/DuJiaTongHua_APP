# 胶囊照片提示遮挡修复

P2-VIS-CAPSULE-HINT：m04-p13 的“可选 · 留下一张照片”“1 张照片已选择”“正在读取照片…”被照片区遮罩盖住，原截图只露出文字下沿。

原因是 `.chosen` 先出现在 form 中，`.prototype-capsule-photo-slot` 后追加，后者占据64%～75%的垂直区域。提示原来位于74%，两者重叠且默认层级相同。只做命中检测会漏掉此问题，因为遮罩禁用了 pointer events，依然参与绘制。

本批只在 `custom/m04-p13.html` 增加一条局部 CSS 并镜像至 pages：提示移到照片操作右下方、提高到遮罩上方，并明确行高。与添加、移除、开启日期控件均无几何重叠，五宽度都完整显示，不通过裁掉文案或隐藏提示解决。DOM、插画、公共样式、选图、移除、保存、权限与返回脚本字节不变。

## 证据

- 原实现20项全失败，均定位为遮罩绘制在提示上方；实际基线与原生产脚本保留于 `evidence/baseline/capsule-photo-hint`。
- 修复后20项状态几何通过：320/360/390/414/430 × 未选图、选中真实图片、实际点击移除、暂停原生 FileReader 的真实读取中。检查层级、完整文字范围、控件避让、屏幕边界、存储不变，并释放读取验证完成状态。
- 原8个初态入口均通过，含返回、标题、正文、选图、日期选择、提醒、草稿和封存。
- 5项照片专项通过：只有照片修改时的按钮／浏览器返回继续和放弃、无效替换保留原照片、照片草稿持久化后实际移除并再保存、封存失败保留输入并成功重试且封存详情不提前展示照片。
- 第一轮为30/33，三个字段因测试错误读取精简清单中不存在的 `native_input` 而未执行，未判作产品 bug。原报告和生产脚本归档至 `capsule-photo-hint-before-control-metadata`；从实际控件读取类型后，新执行这三项通过。其余30项及四张截图通过原报告、生产脚本和完全相同依赖 SHA 证明后保留，**不是33项再次全部执行**。

当前合计33/33。报告及截图入口：[检查点](evidence/current/capsule-photo-hint/checkpoint.json)、[逐项结果](evidence/current/capsule-photo-hint/results.json)、[所选照片](evidence/current/capsule-photo-hint/selected.png)、[读取中](evidence/current/capsule-photo-hint/pending.png)。截图复制来源与逐图 SHA 见 `retained-captures.json`，未冒充新的截图采集。390宽未选、已选、读取中图像已实际查看。

复验使用现有 Playwright Python 环境及8765预览服务：

```powershell
python design-html/prototype/verify_capsule_photo_hint_checkpoint.py
```

完整浏览器运行器是 `verify_capsule_photo_hint.py --stage current`，会拒绝覆盖已有报告，应先保存其版本；`--resume` 仅接受已归档报告与当前依赖完全一致的通过项。

本批只关闭已复现的提示遮挡子问题。字体、控件皮肤及其他列表／宠物／工坊／回忆册的视觉或条件审计仍继续。114页原稿自检覆盖及人工验收状态保持，人工仍0，完整目标未完成。
