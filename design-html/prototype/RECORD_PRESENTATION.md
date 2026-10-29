# 动态记录的真实缩略图与纸张层次

本批范围是 m03-p02 首页、p04 搜索、p06 日记列表、p10 相册。完整目标仍是八模块114页交互原型，原41项要求、七项交付物及人工验收标准不变。

## 实现与边界

- 继续使用现有 `PrototypeUI.components.card`。三个控制器仅加入四次展示辅助调用；原 Card、事件回调、排序、筛选、日期、存储、权限、Loading、Empty、Error、删除和返回代码保持。
- 首页和搜索显示记录自身的图片；无照片时显示原生 CSS 纸页图形。日记在标题下显示自身图片，无照片时保留文字纸卡。真实图片失败显示占位，原卡仍能打开正确详情。相册沿用既有图片与失败回调。
- 使用既有 `book-v2/paper.webp` 纸纹、共享颜色及间距 token 表现纸卡、底纸和胶带，新增装饰不增加点击目标。原按钮文字组成的可访问名称保留。相册正常照片的标题仅视觉隐藏，失败时可见，辅助技术始终能读到原名称。
- 相册底图的示例照片及胶带全部遮盖，数量只来自实际可见记录。去除原 `.grid` 的三行固定高度，让多条真实照片自然形成行并滚动；添加照片按钮仍在原位置。
- 图片只取可见记录的 `image`，不把原设计稿中的食物、人物或花束填充成用户数据。证据里的粉色图片是原测试 fixture，不是加载失败；溢出专项里的彩色横竖图片由测试 canvas 创建，只存在于隔离浏览器。

本批改善缩略图、纸张层次、相册残影和图片边界。搜索原稿的分组布局、日记心情／回应印章／花枝／撕边细节、字体及其他模块的动态列表皮肤仍待继续，**不将 P2-VIS-RECORD-SKIN 整体关闭，也不宣称四页达到原稿一比一验收**。

## 当前证据

| 范围 | 结果 |
| --- | --- |
| 四页 × 320/360/390/414/430 宽度：真实图片解码、纸页占位、长标题、卡片尺寸、图片边界和示例底图遮盖 | 20/20 |
| 四页原始初态控件，包含导航、返回、记录详情、筛选、Tab、刷新及新增入口 | 36/36 |
| 日记／照片筛选及危险删除：取消、模拟失败保留和重试成功 | 4/4 |
| 搜索／日记／相册加载失败并实际点击重试 | 3/3 |
| 四页图片请求失败，原卡仍打开正确详情 | 4/4 |
| 四页他人私密记录不可见且不请求其图片；搜索包含关键词，首页该记录时间最新，相册使用照片类型，避免假阴性 | 4/4 |
| 日记／相册各10条记录 × 五宽度：横竖图片、实际滚动、末项焦点与 Enter 打开精确 ID、存储不变 | 10/10 |

合计 **81 项新执行通过**。来源、生产脚本、fixture 和依赖 SHA 记录在 [主报告](evidence/current/record-presentation/results.json)、[多记录报告](evidence/current/record-collection-overflow/results.json) 及 [检查点](evidence/current/record-presentation/checkpoint.json)。四页390宽截图与两页滚动末项截图已实际查看。未重跑其他110页、未重写旧全量报告；自检覆盖仍114/114、人工验收仍0。

## 保留的失败与覆盖缺口

- `evidence/baseline/record-presentation`：原实现20项全失败，保留四页截图、原11个文件和实际生产脚本。
- `record-presentation-first-pass`：45/71；本批样式造成标题阻挡返回、底纸产生横向溢出，已修复。搜索图片 fixture 与多元素隐私断言的测试错误也分别修正，原结果和脚本保留。
- `record-presentation-before-album-bounds`：当时71/71，但人工图像自检发现相册残影及图片超出纸框。它只证明旧断言覆盖的范围，不证明完整视觉正确。
- `record-presentation-album-bounds`：加入图片纸框边界及背景遮盖条件后，五宽度全失败。修复固定网格行后仍有遮罩选择器优先级问题，下一轮 `record-presentation-before-mask-specificity` 为66/71；修正优先级后才得到当前71/71。
- 历史依赖中未变的二进制资源不重复保存，检查点以当前资源或历史源文件的实际 SHA 验证；变化过的 CSS 和每轮生产脚本都有原件。

## 复验

使用本项目现有 Playwright Python 环境，预览服务监听8765：

```powershell
python design-html/prototype/verify_record_presentation.py --stage current
python design-html/prototype/verify_record_collection_overflow.py
python design-html/prototype/verify_record_presentation_checkpoint.py
```

浏览器运行器拒绝覆盖已有报告；重新执行前应保存原报告及其源版本。检查点可直接重复运行，并验证11个既有文件去除展示接入后与原件字节完全相同、四页 custom/pages 镜像及四个脚本语法。
