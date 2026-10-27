# 照片详情图片边界修复

问题P2-VIS-PHOTO-DETAIL：m03-p12照片框中的真实图片会越出下边缘，覆盖说明及日期。390宽竖图时框高363.30px、图高463.13px；粉色只是测试图颜色，缺陷在渲染尺寸。

## 原因与实现

`.photo`采用Grid，隐式auto轨道按图片固有宽高比计算，图片的100%高度随轨道撑大；横图不溢出，竖图及方图溢出。仅在`custom/m03-p12.html`增加一条作用于照片详情的Grid行列规则，均为`minmax(0,1fr)`，并镜像到`pages/m03-p12.html`。继续使用原有object-fit:contain，不裁掉用户照片。

共享CSS／JS、DOM正文、路由／保存／留言脚本及其余页面保持原字节。`verify_photo_image_bounds_checkpoint.py`通过删除这一条规则与保存的基线逐字比较确认。没有为修复叠加新的遮挡层。

## 实际验证

- 失败基线：session37542，exit1，15项中5通过、10失败；五宽度320／360／390／414／430下，横图通过，竖图与方图均越界。
- 修复后：session50763，exit0，25/25通过。15项图片几何和长说明滚动、1项真实HTTP图片失败后重试、原6个详情入口、2种未发送留言返回保护及1项关闭回应隐私。
- 运行环境：Chrome headless，DPR1，视口高度844、reduce；语言／时区使用浏览器默认，未声称与旧截图统一。该组是局部复验，不是114页全量重跑。
- 已查看修复后的390宽竖图长说明截图，图片下缘止于说明上方，长说明与日期分开。

证据：[失败基线](evidence/baseline/photo-detail-image-bounds/results.json)、[当前25项](evidence/current/photo-detail-image-bounds/results.json)、[范围校验](evidence/current/photo-detail-image-bounds/checkpoint.json)、[修复截图](evidence/current/photo-detail-image-bounds/390-portrait.png)。旧114张捕获保留，原稿图像自检仍34/114，人工验收0。

当前250隐藏控件对应通过新增局部源码保留链继续绑定原证据；不把这些历史报告标成新源码业务全量重跑。字体、控件皮肤、动态记录纸张层次及回忆册阅读布局等原有问题仍开放。
