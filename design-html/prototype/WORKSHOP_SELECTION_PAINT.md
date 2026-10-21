# 照片漫画与影片的原生选择状态

> 后续宠物与回忆册五页修复后，最新初始覆盖由PET_BOOK_SELECTION_PAINT.md及其checkpoint维护。本文件保留照片／影片阶段执行证据。

## 已修复的问题

本次属于修复现有展示逻辑。m05-p04选择油画后，底图中的水彩红框仍显示；m05-p05选择清新自然后，底图中的温柔手帐红框和勾选仍显示。控制器与存储的值已改变，画面却像有两个选项被选中。分别记录为P1 PHOTO-STYLE-RASTER-01和FILM-MOOD-RASTER-01。

只修改这两页custom HTML及相同的pages镜像。选择组用现有纸色遮住底图状态，button使用原生边框与装饰勾选，状态只由aria-pressed决定。照片画风预览继续使用原画稿的局部背景，裁取区排除边框和勾选；影片叶片装饰使用小型SVG。没有修改共享JS/CSS、字段值、路由、保存或生成逻辑。

| 页面 | 字段 | 保留的选项 |
| --- | --- | --- |
| m05-p04 照片转漫画 | style | 水彩、素描、清新插画、油画 |
| m05-p05 回忆影片 | mood | 温柔手帐、治愈暖光、清新自然 |

两个选择组保留b文本供既有controls读取。SVG、预览和勾选均aria-hidden；原生button与共享focus-visible保留Tab、Space与独立焦点反馈。真实新建照片草稿的默认画风仍是水彩；没有根据测试种子的通用style值修改产品默认值。

## 实际验证

- 修复前相同脚本运行10项全部失败，原因均为透明选择组保留旧图片状态，进程51397退出1。
- 修复后320、375、390、414、430五宽度×两页，10项行为检查全部通过，进程68112退出0。
- 每项包含选择最后一项、保存、重入；逐选项Space与2px焦点；保存失败保持未保存的第一项和正文、存储不提前改变；保存重试；选择第二项后生成失败及重新生成成功，保留选择、正文和作品ID。没有页面脚本错误。
- 两页五宽度10项初始布局/命中/安全区检查通过，390px实际Tab可达且有焦点，进程46037退出0。
- 人工查看m05-p04的320/390px及m05-p05的320px最后一项截图：旧水彩选框及旧温柔手帐勾选已消失，预览与标签清楚。
- 检查点进程65238退出0：核对源指纹、相同脚本红绿结果、镜像和HTTP字节及布局记录组合。

行为脚本：`verify_workshop_selection_paint.py`。直接结果、20张当前截图及checkpoint位于`evidence/current/workshop-selection-paint/`；修复前结果和截图位于`evidence/baseline/workshop-selection-paint/`。

## 114页初始观察的来源

`evidence/history/pre-workshop-selection-paint-f08fa83/initial-quality-checkpoint.json`保存前批检查点。只有两页HTML改变，共享CSS/JS、图片、字体、固定数据和种子依赖均未变。检查器逐项比较这些输入，保留其他112页的560项实际初始观察，以本次两页10项新执行替换旧观察。

组合结果仍为114页×5宽度570项及114页390px键盘遍历。每条记录保留原报告与索引，未声称本轮重新执行了全部570项。最新相同检查点位于`evidence/current/workshop-selection-paint/checkpoint.json`与`evidence/current/initial-quality/checkpoint.json`。

重查命令（使用带Playwright的项目工具Python环境）：

```powershell
python design-html/prototype/verify_workshop_selection_paint.py
python design-html/prototype/audit_initial_quality.py --pages m05-p04,m05-p05 --widths 320,375,390,414,430
```

检查点要求传入实际执行的session与退出码，参数名见脚本。此证据组合只支持标准初始几何及上述两页选择流程；其他隐藏/长文/软键盘状态、全量主要流程和异常分支最终复验继续。当前114页最终验收仍为0，不结束目标。
