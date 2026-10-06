# 回忆册控件执行

## 范围与结果

2026-10-06执行：m08-p01至p21的声明条件下154个可用初始控件实际操作；补页返回专项2项、五宽度15项、既有流程39项，共210项通过。114页和37共享资源HTTP字节一致，custom/pages一致。只操作隔离测试context。

## 声明条件与数据核对

已登录、关系绑定；小满/阿舟、固定日期2026-10-06。默认共同测试册已发布、两章三页，分别引用共同日记/照片/时刻，已选素材为日记。空书架页使用空册集合；素材选择页使用尚未编排的宠物复合ID audit-pet:audit-story；预览页清空书页以保留待编排素材。三类专属编辑页分别使用真实照片/时刻/宠物来源；阅读、工具、补页使用page-second。详细fixture见verify_book_controls.py。

路由逐项检查目标页，声明参数的场景核对册/书页/来源ID。阅读会更新lastPage及updatedAt，纯路由比较允许这两个字段变化，其他本地数据须保持。实际提交检查新草稿册、选中素材、跳过素材、稳定页ID保存、章节/页面排列、书签、补页及归档；下载JSON核对文件名、格式、册ID。输入、筛选、预览、打开/取消弹层均核对未持久化。换模板检查会话草稿册ID及页ID。

## 修复与原始诊断

补页编辑顶部名为返回补页选择，但直接进入及脏输入确认放弃后的fallback均为阅读页。原失败见baseline/book-control-return-results.json（2项）；现为m08-p18并保留当前册/页ID，复用原UI.back及guard。浏览器真实历史仍优先返回上一个入口，修正的是直接进入时的fallback。

初轮154项报告保留在baseline/book-controls-initial-diagnostic.json：9个失败中1个为上述实际产品返回问题；其他为观察器/fixture错误（照片出口误写列表、工坊误写配置页，创建/封面按钮文案误分类，以及宠物来源没有使用petID:logID复合身份）。观察器和fixture修正后整个154项重跑。没有将观察器错误当作产品修复。

## 专项和回归

返回专项检查无修改直接返回，以及修改后继续保留输入、再确认放弃，均不写本地集合并保留册/页ID。五宽度320/360/390/414/430px ×补页编辑/日记编排/书名Sheet共15项：34px安全区、500字正文或20字书名、确认弹层及按钮在屏内，按钮至少44px，继续后输入保留且集合不变；人工查看320px补页和书名截图。实际软键盘和所有页面状态视觉仍待最终检查。

39项重新执行：建册/真实素材编排/阅读及删除4，保存/加载/权限/改名归档导出失败恢复6，照片裁剪贴纸/专属来源/三种补页/图片失败7，顺序编排/章节和页CRUD/冲突5，封面主题/私密同步4，全局备份/草稿/首页/来源日期6，完整跨模板草稿/稳定ID/冲突7。各报告SHA由book-control-regression-source.json绑定源码。旧回忆册JSON报告保留history/pre-book-controls-bd1e3b8；文件夹是归档时HEAD。历史截图并非本次重新拍摄，当前新截图统一book-control-layout前缀。

## 初始控件契约

| 页面 | 控件 | 实际契约 |
| --- | --- | --- |
| m08-p01 | ♡ / 共同测试册 / 花园午后 | route:m08-p15 |
| m08-p01 | 继续阅读 › | route:m08-p15 |
| m08-p01 | 新建回忆册 | route:m08-p04 |
| m08-p01 | 本月推荐 | route:m08-p03 |
| m08-p01 | 归档与草稿 | sheet:归档与草稿 |
| m08-p01 | 返回首页 | route:m03-p02 |
| m08-p02 | 返回 | route:m03-p02 |
| m08-p02 | 新建第一本回忆册 | route:m08-p04 |
| m08-p03 | 返回回忆册 | route:m08-p01 |
| m08-p03 | 查看并确认素材 | route:m08-p04 |
| m08-p03 | 返回书架 | route:m08-p01 |
| m08-p03 | 共同日记 · 2026-10-04 | route:m03-p08?id=audit-diary |
| m08-p03 | 共同照片 · 2026-10-04 | route:m03-p12?id=audit-photo |
| m08-p03 | 共同重要时刻 · 2026-10-04 | route:m04-p03?id=audit-moment |
| m08-p03 | 实际工坊作品 · 2026-10-05 | route:m05-p08?id=audit-work |
| m08-p03 | 实际成长故事 · 2026-10-04 | route:m07-p19?id=audit-story |
| m08-p04 | 返回 | route:m08-p01 |
| m08-p04 | 书名 | input |
| m08-p04 | 开始月份 | input |
| m08-p04 | 结束月份 | input |
| m08-p04 | 从共同素材开始 | pressed |
| m08-p04 | 空白回忆册 | pressed |
| m08-p04 | 下一步：选择主题 | create |
| m08-p05 | 返回上一步 | route:m08-p04 |
| m08-p05 | 花园午后 | pressed |
| m08-p05 | 旅行手札 | pressed |
| m08-p05 | 暖灯日常 | pressed |
| m08-p05 | 使用封面照片 | sheet:选择共同素材 |
| m08-p05 | 下一步：选择素材 | theme-save |
| m08-p06 | 返回上一步 | route:m08-p05 |
| m08-p06 | 全部 | tab |
| m08-p06 | 日记 | tab |
| m08-p06 | 照片 | tab |
| m08-p06 | 时刻 | tab |
| m08-p06 | 工坊 | tab |
| m08-p06 | 宠物 | tab |
| m08-p06 | 共同日记 · 日记 · 2026-10-04 | source-toggle |
| m08-p06 | 共同照片 · 照片 · 2026-10-04 | source-toggle |
| m08-p06 | 共同重要时刻 · 时刻 · 2026-10-04 | source-toggle |
| m08-p06 | 实际工坊作品 · 工坊 · 2026-10-05 | source-toggle |
| m08-p06 | 实际成长故事 · 宠物 · 2026-10-04 | source-toggle |
| m08-p06 | 开始编排 | select-save |
| m08-p07 | 返回素材选择 | route:m08-p06 |
| m08-p07 | 暂不放入 | skip |
| m08-p07 | 放入回忆册 | route:m08-p08 |
| m08-p07 | 重新选择素材 | route:m08-p06 |
| m08-p08 | 返回素材预览 | route:m08-p07 |
| m08-p08 | 2024.04.21　周日 / 今天一起去了海边， / 风很温柔，你在笑， / 我也觉得整个世界 / 都亮了起来。 / 日记摘录 | pressed |
| m08-p08 | 那天的晚霞 / 好美呀～ / 照片故事 | pressed |
| m08-p08 | 我们的重要时刻 / 2023.05.20 / 第一次约会 / 2023.08.10 / 一起旅行 / 2024.02.14 / 确定关系 / 重要时刻 | pressed |
| m08-p08 | 一起完成的小作品 / 工坊作品 | pressed |
| m08-p08 | 小家伙的成长日记 / 2个月　　 6个月　　 1岁 / 宠物成长 | pressed |
| m08-p08 | · 第三章 · / 平凡的日子 / 也闪闪发光 / 章节扉页 | pressed |
| m08-p08 | 使用这个模板 | route:m08-p09 |
| m08-p09 | 返回版式选择 | route:m08-p08 |
| m08-p09 | 书页标题 | input |
| m08-p09 | 日记摘录 | input |
| m08-p09 | 书页日期 | input |
| m08-p09 | 书页寄语 | input |
| m08-p09 | 换摘录 / 换一段日记 | sheet:选择共同素材 |
| m08-p09 | 换照片 / 换一张照片 | sheet:选择共同素材 |
| m08-p09 | 换版式 / 换一种排版 | stash |
| m08-p09 | 完成这一页 | page-save |
| m08-p10 | 返回 | route:m08-p08 |
| m08-p10 | 预览 | modal:共同照片 |
| m08-p10 | 书页标题 | input |
| m08-p10 | 书页日期 | input |
| m08-p10 | 裁剪/替换 | sheet:照片1 |
| m08-p10 | 裁剪/替换 | sheet:选择共同素材 |
| m08-p10 | 裁剪/替换 | sheet:选择共同素材 |
| m08-p10 | 这一页的想法 | input |
| m08-p10 | 完成这一页 | page-save |
| m08-p10 | 添加照片 | sheet:选择共同素材 |
| m08-p10 | 添加文字 | focus:这一页的想法 |
| m08-p10 | 添加贴纸 | sheet:选择贴纸 |
| m08-p10 | 保留草稿换模板 | stash |
| m08-p11 | 返回版式选择 | route:m08-p08 |
| m08-p11 | 书页标题 | input |
| m08-p11 | 书页日期 | input |
| m08-p11 | 更换照片 | sheet:选择共同素材 |
| m08-p11 | 选择时刻 › | sheet:选择共同素材 |
| m08-p11 | 添加一句话 | sheet:一句话 |
| m08-p11 | 完成这一页 ♡ | page-save |
| m08-p11 | 保留草稿换模板 | stash |
| m08-p12 | 返回版式选择 | route:m08-p08 |
| m08-p12 | 工坊作品 | sheet:选择共同素材 |
| m08-p12 | 宠物成长 | tab |
| m08-p12 | 成长说明 | input |
| m08-p12 | 换内容 | sheet:选择共同素材 |
| m08-p12 | 换照片 | sheet:选择共同素材 |
| m08-p12 | 添加说明 | focus:成长说明 |
| m08-p12 | 完成这一页 | page-save |
| m08-p12 | 保留草稿换模板 | stash |
| m08-p13 | 返回编排 | route:m08-p06 |
| m08-p13 | 新增章节 | sheet:章节 |
| m08-p13 | 保存排列 | structure-save |
| m08-p13 | 章节操作「第一章」 | sheet:第一章 · 章节操作 |
| m08-p13 | 共同日记 | route:m08-p09?id=book-state&page=page-state |
| m08-p13 | 页面操作「共同日记」 | sheet:共同日记 · 页面操作 |
| m08-p13 | 共同照片 | route:m08-p10?id=book-state&page=page-second |
| m08-p13 | 页面操作「共同照片」 | sheet:共同照片 · 页面操作 |
| m08-p13 | 章节操作「第二章」 | sheet:第二章 · 章节操作 |
| m08-p13 | 共同重要时刻 | route:m08-p11?id=book-state&page=page-third |
| m08-p13 | 页面操作「共同重要时刻」 | sheet:共同重要时刻 · 页面操作 |
| m08-p13 | 添加书页 | route:m08-p08 |
| m08-p14 | 开始翻阅 | route:m08-p15 |
| m08-p14 | 继续整理 | route:m08-p13 |
| m08-p14 | 返回书架 | route:m08-p01 |
| m08-p15 | 返回书架 | route:m08-p01 |
| m08-p15 | 从第 1 页开始 → | route:m08-p16?id=book-state&page=page-state |
| m08-p15 | 管理这本回忆册 | route:m08-p21 |
| m08-p15 | 共同日记 | route:m08-p16?id=book-state&page=page-state |
| m08-p15 | 共同照片 | route:m08-p16?id=book-state&page=page-second |
| m08-p15 | 共同重要时刻 | route:m08-p16?id=book-state&page=page-third |
| m08-p16 | 返回 | route:m08-p15 |
| m08-p16 | 目录 | route:m08-p15 |
| m08-p16 | 书签 | bookmark |
| m08-p16 | 下一页 | route:m08-p16?id=book-state&page=page-third |
| m08-p16 | 查看原始共同记录 | route:m03-p12?id=audit-photo |
| m08-p16 | 上一页 | route:m08-p16?id=book-state&page=page-state |
| m08-p16 | 阅读工具 | route:m08-p17 |
| m08-p17 | 返回阅读 | route:m08-p16 |
| m08-p17 | 目录 / 查看全书目录和章节 | route:m08-p15 |
| m08-p17 | 书签 / 查看和管理我的书签 | sheet:我的书签 |
| m08-p17 | 添加补页 / 在书中添加新的补充页 | route:m08-p18 |
| m08-p17 | 整理这本书 / 调整页序、重命名、导出等 | route:m08-p13 |
| m08-p17 | 管理这本书 · 书名、归档、导出与删除 | route:m08-p21 |
| m08-p18 | 返回阅读 | route:m08-p16 |
| m08-p18 | 回到目录 | route:m08-p15 |
| m08-p18 | 写几句话 / 记录此刻的想法与心情 | pressed |
| m08-p18 | 送一个表情 / 用一个表情传达你的心意 | pressed |
| m08-p18 | 附上一张照片 / 用一张照片定格这份回忆 | pressed |
| m08-p18 | 选择回应方式 | route:m08-p19?id=book-state&page=page-second&kind=写几句话 |
| m08-p19 | 返回补页选择 | route:m08-p18 |
| m08-p19 | 补页文字 | input |
| m08-p19 | 爱心 | pressed |
| m08-p19 | 星星 | pressed |
| m08-p19 | 微笑 | pressed |
| m08-p19 | 花朵 | pressed |
| m08-p19 | INPUT | file |
| m08-p19 | 放进回忆书 | supplement |
| m08-p20 | 返回阅读工具 | route:m08-p17 |
| m08-p20 | 目录 | route:m08-p15 |
| m08-p20 | 书签 | bookmark |
| m08-p20 | 查看原始共同记录 | route:m03-p12?id=audit-photo |
| m08-p20 | 上一页 | route:m08-p16?id=book-state&page=page-state |
| m08-p20 | 阅读工具 | route:m08-p17 |
| m08-p21 | 返回阅读 | route:m08-p15 |
| m08-p21 | 修改书名 | sheet:书名 |
| m08-p21 | 整理页序 | route:m08-p13 |
| m08-p21 | 修改主题与封面 | route:m08-p05?id=book-state&origin=manage |
| m08-p21 | 归档回忆册 | archive |
| m08-p21 | 删除这本回忆册 | modal:确定删除《共同测试册》？ |
| m08-p21 | 导出这本回忆册 | export |

## 验收边界

源码指纹 `a1d252faa3a29b27c061d5069c32bee75fcf0f1f567ea4b22c1c41a300c6c4d3`，210项报告绑定当前源码。114页均已建立各阶段的声明初始控件契约；这些阶段不全是当前源码的全模块重跑。宠物202项及其他模块历史来源保持原指纹。

114页最终验收0。全产品串行新用户/退出重登录/跨模块流程、全部隐藏动态状态、其他集合恢复及引用、共用组件热区/视觉/键盘/安全区/动效的当前源码综合复核仍需推进，目标保持active。
