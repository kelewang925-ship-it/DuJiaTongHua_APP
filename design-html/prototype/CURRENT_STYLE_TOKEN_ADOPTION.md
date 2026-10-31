# 当前动态样式的同值Token接入

原41项第32项核对发现，后续新增动态样式未完全沿用既有Token。本批将10份CSS的191处声明接入18个已经存在的变量，不增加Token定义，不改变原画板位置、插画、主题颜色方案、文本、HTML或JavaScript。

| 样式 | 接入声明数 |
| --- | ---: |
| prototype-book-v2.css | 161 |
| prototype-film-timeline.css | 3 |
| prototype-pet-achievement-collection.css | 6 |
| prototype-pet-achievement-progress.css | 3 |
| prototype-pet-draft-preview.css | 4 |
| prototype-pet-item-preview.css | 3 |
| prototype-pet-resource-presentation.css | 3 |
| prototype-pet-result-illustration.css | 3 |
| prototype-pet-room-comparison.css | 4 |
| prototype-record-presentation.css | 1 |

复用既有字体、颜色、间距、圆角及40／44／48px控件尺寸。例如`gap:4px`接入`--prototype-space-xs`，`font-size:14px`接入`--prototype-font-note`。复用现有迁移函数，只处理语义类别内的精确同值；插画比例、独有主题与特定几何值仍按原稿保留。191是声明数量，单个padding声明可包含多个替换。

## 实际浏览器证据

- 修改前：114页声明初态，加31个回忆册手动弹层和6个宠物目录解锁Sheet，共151个场景实际观察全部成功。
- 按实际加载的样式选择受影响场景：35页初态、37个弹层，共72项修改后新执行，与修改前完全相同。
- 比较26项计算属性、可见元素类型／类、几何位置与尺寸、before／after伪元素、滚动尺寸及18项根变量。环境为Chrome、390×844、zh-CN、Asia/Shanghai、减少动效。
- 全201项产品依赖中只有这10份CSS改变；每份当前CSS均严格等于原字节经既有同值替换函数得到的结果。其他HTML、JavaScript和资源保持原字节。
- 18个变量的定义均位于`:root`且值等于原字面量，没有同名嵌套覆盖或显式JavaScript setter。151个修改前场景及72个修改后场景的实际变量值一致。
- 22份动态CSS按既有同值接入政策检查，剩余可替换声明0；这不声称所有原稿几何、主题专色或数值都应改成同一变量。

[计划与逐处替换](evidence/current/style-tokens-20261101/plan.json)／[修改前151项](evidence/current/style-tokens-20261101/before.json)／[修改后72项](evidence/current/style-tokens-20261101/after.json)／[实际应用记录](evidence/current/style-tokens-20261101/applied.json)。原源码、递归夹具及修改后10份样式分别在同目录before-archive和after-styles中保存原字节。

## 复验

在仓库根目录配置现有Playwright工具环境后运行：

```powershell
python design-html/prototype/verify_current_style_tokens.py
python design-html/prototype/migrate_shared_style_tokens.py --check
```

采集器的before／apply／after均拒绝覆盖已有阶段。本次before进程40524、apply退出0、after进程6423均实际完成；不能只用迁移函数预期值代替浏览器观察。

## 与其他证据的关系

本批没有重跑282个业务案例。它们的原CSS依赖指纹保持，JavaScript／HTML／资源与本批一致；通过本次精确同值、常量别名及受影响场景计算样式证明组合使用，不把旧报告改绑到新CSS。单独要求旧报告完整依赖相等的校验器会如实指出这10份CSS差异，本批的复合校验入口是verify_current_style_tokens.py。

本批补的是统一Token接入，不以计算样式一致声称原稿视觉差异消失，也不替代其他种子、设备或完整41项审计。继续核对导航条件图、提交／等待证据的版本对应及已登记原稿差异。人工验收0只是记录，不新增人工审批前置条件；完整目标仍执行中。
