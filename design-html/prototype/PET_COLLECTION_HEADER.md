# 收藏图鉴顶部文字避让

P2-VIS-PET-INLINE 的 m07-p22 子范围：原“认识小伙伴”44px按钮与收藏数量位于同一右上区域，五宽度、三种姓名下均实际相交。数量移到返回右侧的信息区，按钮保持原位置。宠物名称单独成行，保留完整12字中文及长英文换行；“收藏图鉴”保持标题层级。标题限制在原宠物插画左侧。

本批只修改 custom/pages 两份 HTML 的局部 CSS 和标题 span，继续使用现有姓名替换层。业务回调、模型、目录、领取条件和原画资源保持原字节；收藏数量继续由真实本地模型计算。

当前28项全部新执行通过：320/360/390/414/430五宽度 × 短名、12字中文、长英文共15项；原13个入口包括三种分类、八个物品、返回、伙伴Sheet打开／Escape关闭与焦点恢复。布局检查覆盖完整文字、数量与按钮／标题避让、返回、说明及分类边界，确认显示不改变存储。

基线15项均因数量与按钮实际相交失败。保留原文件、生产脚本、六张截图及结果，不以新增span存在作为旧版失败条件。当前320/390两宽度三种姓名截图已查看；检查点反向撤销精确变更，验证两份HTML镜像及直接依赖不变。

- [当前结果](evidence/current/pet-collection-header/results.json)
- [检查点](evidence/current/pet-collection-header/checkpoint.json)
- [320px长中文](evidence/current/pet-collection-header/320-1.png)
- [原始失败证据](evidence/baseline/pet-collection-header/results.json)

复验：`python design-html/prototype/verify_pet_collection_header_checkpoint.py`。浏览器运行器为 `verify_pet_collection_header.py --stage current`，拒绝覆盖历史结果；需先保留历史报告再重新执行。

本批不包含图鉴卡片封面／静态底图残影皮肤、其他宠物页文字避让或114页终审。人工验收仍0，完整目标继续。
