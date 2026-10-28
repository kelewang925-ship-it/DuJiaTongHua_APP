# 六种书页版式缩略示意

P2-VIS-BOOK-TEMPLATE-PREVIEW的范围是m08-p08六张只有名称的版式卡。继续沿用现有奶油纸、可可棕和玫瑰灰，在原卡片内绘制六种可编辑HTML/CSS示意：日记行、照片排布、时刻时间线、作品、成长记录和章节页。图片区复用现有回忆册资源。卡片下明确说明“版式示意，内容由你选择的共同回忆填入”。

装饰层为aria-hidden，不改变六个按钮的无障碍名称、data-template、选中逻辑及使用版式的去向。没有新增用户数据、图片生成、运行时库或动效。样式均限定在book-page=8。生成器可只重建第8页，保留其他20页和原有图片资源。

## 验证

- [失败基线](evidence/baseline/book-template-previews/results.json)：五宽度均缺少六种预览。
- [最终11项](evidence/current/book-template-previews/results.json)：五宽度检查实际预览大小、可见图形、控件命中、选中切换、唯一选中、横向溢出与存储保持；六个独立案例执行原跳转或章节命名弹窗取消。
- [390宽最终截图](evidence/current/book-template-previews/390.png)已实际查看。首版CSS层级曾导致所有版式都显示照片层，已修正并补充计算样式检查；首版报告和截图保留在before-photo-visibility-fix目录，未用绿报告掩盖视觉问题。
- [源码范围核对](evidence/current/book-template-previews/checkpoint.json)：移除追加CSS并恢复原第8页内容后，与保存源码逐字节相等；其余20页生成内容、全部JS、资源及按钮去向保留。

检查环境与源码指纹见报告；390×844仍是临时检查条件，人工验收仍0。其他视觉问题及完整114页目标继续。

## 当前回忆册控件盘点

[21页初态清单](evidence/current/book-v2-controls/inventory.json)实际观察156个可操作入口，已排除禁用及模态背景控件。观察不等于执行通过；逐入口业务重放另存results.json，只有明确通过的案例才能支撑行为结论。V2隐藏控件、条件导航及异常状态仍需重新对应原41项要求，不把旧250控件证据改写成新版本。
