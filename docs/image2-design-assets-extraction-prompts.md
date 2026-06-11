# 《独家童话》assets/design 效果图装饰素材 image2 生成提示词

> 用途：后续交给 Codex 读取本文件，按 `assets/design/*.png` 效果图逐张生成前端可复用的 PNG 装饰素材。
>
> 核心目标：**不要重新生成完整页面**，只提取页面里无法或不适合用前端代码实现的手绘装饰、贴纸、插画、纹理、纸张折角、胶带、星光等素材。

---

## 0. Codex 执行约定

Codex 后续生成素材时，请按以下规则执行：

1. 每个效果图对应一个独立输出目录：
   - `assets/image2/design-assets/<效果图文件名去扩展名>/`
2. 每个装饰元素单独生成一张 PNG，不要做素材板，不要把多个元素合并在同一张图片里。
3. 每张 PNG 必须是透明背景，元素外部区域需要裁剪为透明，四周尽量紧凑，只保留少量安全留白。
4. 不要生成页面文字、按钮、列表、卡片、标题栏、TabBar、输入框等可由前端代码实现的 UI 结构。
5. 不要生成真实文字、Logo、水印。
6. 输出文件建议使用英文小写短横线命名，例如：`heart-sticker.png`、`paper-tape.png`、`magic-wand.png`。

统一视觉风格：童话绘本、奶油纸感、柔和桃粉、干玫瑰、可可棕线稿、琥珀金点缀、轻手绘、贴纸感、温柔治愈、留白充足。整体质感像手账贴纸和纸质拼贴。不要高饱和，不要科技蓝紫风，不要真实照片，不要低幼卡通，不要复杂背景。

通用透明裁切要求：生成单个图片素材，并把元素周围多余背景裁剪为透明；透明区域要干净，不能带浅色底块、棋盘格、水印或背景阴影污染。这样前端在改变页面背景色时，图标边缘不会显得突兀。

---

## 1. `assets/design/01-账号与关联.png`

输出目录：`assets/image2/design-assets/01-account-link/`

```text
请参考上传的《01-账号与关联》效果图，提取并重新绘制适合作为前端图片素材的装饰元素。不要生成完整 UI 页面，不要生成文字内容，不要生成按钮、列表卡片、标题栏等可用代码实现的界面结构。

需要生成的单个透明 PNG 素材包括：启动页童话绘本插画、双人头像贴纸、邀请函信封、邀请码丝带、绑定成功爱心光晕、情侣资料头像装饰、钥匙或锁形贴纸、零散星光小爱心。

输出要求：每个元素单独一张图，透明背景，元素周围内容裁剪成透明，只保留少量安全留白，适合放入 assets/image2/design-assets/01-account-link/。
```

## 2. `assets/design/02-首页-记录中心.png`

输出目录：`assets/image2/design-assets/02-home-record-center/`

```text
请参考上传的《02-首页-记录中心》效果图，提取并重新绘制适合作为前端图片素材的装饰元素。不要生成完整 UI 页面，不要生成文字内容，不要生成可用代码实现的卡片、按钮、列表或 TabBar。

需要生成的单个透明 PNG 素材包括：打开的回忆绘本、拍立得照片贴纸、纸胶带、手绘小花、恋爱天数装饰爱心、回忆碎片墙角标、羽毛笔、小星星、小丝带、奶油纸碎片装饰。

输出要求：每个元素单独一张图，透明背景，边缘干净，裁剪紧凑，适合放入 assets/image2/design-assets/02-home-record-center/。
```

## 3. `assets/design/03-情侣空间.png`

输出目录：`assets/image2/design-assets/03-couple-space/`

```text
请参考上传的《03-情侣空间》效果图，提取并重新绘制情侣空间页面中适合作为前端图片素材的装饰元素。不要生成完整页面，不要生成文字。

需要生成的单个透明 PNG 素材包括：双人头像贴纸组合、情侣小屋或共同主页插画、手绘时间轴节点、爱心节点、小花节点、星星节点、纪念日小日历、私密故事书、留言气泡、丝带和星光轨迹。

输出要求：每个元素单独一张透明 PNG，裁剪掉元素外部背景，四周留白少，适合放入 assets/image2/design-assets/03-couple-space/。
```

## 4. `assets/design/04-AI童话工坊.png`

输出目录：`assets/image2/design-assets/04-ai-fairy-workshop/`

```text
请参考上传的《04-AI童话工坊》效果图，提取并重新绘制 AI 工坊中适合作为前端图片素材的装饰元素。不要生成完整 UI，不要生成文字，不要生成科技蓝紫风。

需要生成的单个透明 PNG 素材包括：温柔魔法屋、绘本工坊小屋、魔法棒、星光粒子、AI 漫画小画板、AI 视频胶片、文本转漫画纸页、照片转漫画拍立得、创作历史收藏册、生成中小星云。

输出要求：每个元素单独一张透明 PNG，裁剪紧凑，边缘干净，适合放入 assets/image2/design-assets/04-ai-fairy-workshop/。
```

## 5. `assets/design/05-AI创作流程.png`

输出目录：`assets/image2/design-assets/05-ai-creation-flow/`

```text
请参考上传的《05-AI创作流程》效果图，提取并重新绘制 AI 创作流程里适合前端复用的装饰素材。不要生成完整流程图，不要生成文字和 UI 表单。

需要生成的单个透明 PNG 素材包括：素材选择拍立得、风格配置画笔、分镜纸张、生成进度魔法棒、墨水显影星点、漫画结果小绘本、视频胶片、完成状态星光徽章、失败/草稿温柔提示贴纸。

输出要求：每个元素单独一张透明 PNG，裁剪元素外部背景，适合放入 assets/image2/design-assets/05-ai-creation-flow/。
```

## 6. `assets/design/06-纪念日管理.png`

输出目录：`assets/image2/design-assets/06-anniversary-management/`

```text
请参考上传的《06-纪念日管理》效果图，提取并重新绘制纪念日管理相关装饰素材。不要生成完整页面，不要生成文字、列表和按钮。

需要生成的单个透明 PNG 素材包括：纪念册、桃粉日历、倒计时数字装饰框、干玫瑰、丝带、纪念日礼盒、小爱心标签、分享封面插画、花朵星星组合、纸质日期牌。

输出要求：每个元素单独一张透明 PNG，裁剪成透明边缘，适合放入 assets/image2/design-assets/06-anniversary-management/。
```

## 7. `assets/design/07-数据与导出.png`

输出目录：`assets/image2/design-assets/07-data-export/`

```text
请参考上传的《07-数据与导出》效果图，提取并重新绘制数据导出与备份相关装饰素材。不要生成完整页面，不要生成文字和图表 UI。

需要生成的单个透明 PNG 素材包括：回忆绘本封面、PDF 纸页、导出文件夹、云备份小云朵、数据保险箱、琥珀金书签、照片角标、装订线、存储空间小盒子、恢复数据信封。

输出要求：每个元素单独一张透明 PNG，外部背景裁剪为透明，适合放入 assets/image2/design-assets/07-data-export/。
```

## 8. `assets/design/08-更多功能.png`

输出目录：`assets/image2/design-assets/08-more-features/`

```text
请参考上传的《08-更多功能》效果图，提取并重新绘制更多功能/我的页面中适合前端复用的装饰素材。不要生成完整页面，不要生成文字、功能列表和设置项。

需要生成的单个透明 PNG 素材包括：用户资料头像框、会员琥珀金徽章、搜索放大镜绘本、草稿纸页、分享卡片、帮助小信封、设置小齿轮贴纸、空状态羽毛笔、小花星光、纸质分组角标。

输出要求：每个元素单独一张透明 PNG，裁剪干净，适合放入 assets/image2/design-assets/08-more-features/。
```

## 9. `assets/design/引导页.png`

输出目录：`assets/image2/design-assets/guide-page/`

```text
请参考上传的《引导页》效果图，提取并重新绘制引导页中不可用前端代码直接实现的插画和装饰元素。不要生成完整引导页，不要生成中文文案和按钮。

需要生成的单个透明 PNG 素材包括：打开的童话故事书、双人头像贴纸、星星丝带、漂浮爱心、奶油纸云朵、柔粉光晕装饰。

输出要求：每个元素单独一张透明 PNG，裁剪掉多余背景，适合放入 assets/image2/design-assets/guide-page/。
```

## 10. `assets/design/登录页.png`

输出目录：`assets/image2/design-assets/login-page/`

```text
请参考上传的《登录页》效果图，提取并重新绘制登录页中适合作为前端图片素材的装饰元素。不要生成完整登录页，不要生成输入框、按钮、文字。

需要生成的单个透明 PNG 素材包括：小信封贴纸、钥匙贴纸、爱心锁、登录页顶部小插画、星光点缀、纸胶带、柔粉背景光斑。

输出要求：每个元素单独一张透明 PNG，元素外部裁剪成透明，适合放入 assets/image2/design-assets/login-page/。
```

## 11. `assets/design/情侣邀请页.png`

输出目录：`assets/image2/design-assets/couple-invite-page/`

```text
请参考上传的《情侣邀请页》效果图，提取并重新绘制情侣邀请页的装饰素材。不要生成完整页面，不要生成邀请码文字、按钮或步骤列表。

需要生成的单个透明 PNG 素材包括：奶油纸邀请函、信封、丝带、复制成功小贴纸、分享小纸飞机、爱心印章、星星和小花。

输出要求：每个元素单独一张透明 PNG，裁剪边缘透明，适合放入 assets/image2/design-assets/couple-invite-page/。
```

## 12. `assets/design/情侣绑定确认页.png`

输出目录：`assets/image2/design-assets/couple-bind-confirm-page/`

```text
请参考上传的《情侣绑定确认页》效果图，提取并重新绘制绑定确认页里的插画和装饰元素。不要生成完整页面、文字和按钮。

需要生成的单个透明 PNG 素材包括：对方头像贴纸框、双人连接爱心、绑定成功光晕、确认印章、星星花朵、柔粉丝带。

输出要求：每个元素单独一张透明 PNG，元素周围背景裁剪为透明，适合放入 assets/image2/design-assets/couple-bind-confirm-page/。
```

## 13. `assets/design/情侣信息设置页.png`

输出目录：`assets/image2/design-assets/couple-profile-setup-page/`

```text
请参考上传的《情侣信息设置页》效果图，提取并重新绘制情侣资料设置页中适合前端复用的装饰素材。不要生成表单、输入框、按钮或文字。

需要生成的单个透明 PNG 素材包括：两个人的头像贴纸框、头像编辑小笔、恋爱起始日日历、关系备注小纸条、爱心连接线、小花星光装饰。

输出要求：每个元素单独一张透明 PNG，裁剪干净，适合放入 assets/image2/design-assets/couple-profile-setup-page/。
```

## 14. `assets/design/日记编辑器.png`

输出目录：`assets/image2/design-assets/diary-editor/`

```text
请参考上传的《日记编辑器》效果图，提取并重新绘制日记编辑器里的装饰素材。不要生成完整编辑器、输入框、文字和工具栏。

需要生成的单个透明 PNG 素材包括：奶油纸日记页、羽毛笔、心情贴纸、小标签贴纸、图片入口拍立得、语音小气泡、位置小花标、保存成功星光。

输出要求：每个元素单独一张透明 PNG，元素外部背景裁剪为透明，适合放入 assets/image2/design-assets/diary-editor/。
```

## 15. `assets/design/日记详情页.png`

输出目录：`assets/image2/design-assets/diary-detail/`

```text
请参考上传的《日记详情页》效果图，提取并重新绘制日记详情页的纸感装饰和贴纸素材。不要生成文章内容、标题文字、按钮或完整页面。

需要生成的单个透明 PNG 素材包括：翻页纸张、日记页角标、心情标签贴纸、文本转漫画魔法小标、分享小信封、照片胶带、干玫瑰和星星。

输出要求：每个元素单独一张透明 PNG，裁剪成透明边缘，适合放入 assets/image2/design-assets/diary-detail/。
```

## 16. `assets/design/照片上传页.png`

输出目录：`assets/image2/design-assets/photo-upload/`

```text
请参考上传的《照片上传页》效果图，提取并重新绘制照片上传页面的装饰素材。不要生成上传表单、输入框、按钮或页面文字。

需要生成的单个透明 PNG 素材包括：拍立得占位框、照片角标、胶带、相机贴纸、干玫瑰、小花、标签贴纸、上传成功星光。

输出要求：每个元素单独一张透明 PNG，四周裁剪为透明，适合放入 assets/image2/design-assets/photo-upload/。
```

## 17. `assets/design/相册浏览页.png`

输出目录：`assets/image2/design-assets/photo-album/`

```text
请参考上传的《相册浏览页》效果图，提取并重新绘制相册浏览页中不可由代码直接实现的装饰素材。不要生成照片网格、筛选 UI、按钮或文字。

需要生成的单个透明 PNG 素材包括：拍立得照片框、相册封面、胶带、照片角标、空相册插画、花朵贴纸、星星爱心、浮动添加贴纸图标。

输出要求：每个元素单独一张透明 PNG，背景裁剪透明，适合放入 assets/image2/design-assets/photo-album/。
```

## 18. `assets/design/时光胶囊设置页.png`

输出目录：`assets/image2/design-assets/time-capsule-settings/`

```text
请参考上传的《时光胶囊设置页》效果图，提取并重新绘制时光胶囊相关装饰素材。不要生成表单、开关、日期选择器或文字。

需要生成的单个透明 PNG 素材包括：玻璃瓶信封、软木塞、未来信件、日期牌、小星星、丝带、提醒铃铛贴纸、时间胶囊小徽章。

输出要求：每个元素单独一张透明 PNG，裁剪干净，适合放入 assets/image2/design-assets/time-capsule-settings/。
```

## 19. `assets/design/标签管理页.png`

输出目录：`assets/image2/design-assets/tag-management/`

```text
请参考上传的《标签管理页》效果图，提取并重新绘制标签管理页里的手绘贴纸素材。不要生成完整标签列表、输入框、文字或操作按钮。

需要生成的单个透明 PNG 素材包括：心情标签贴纸、地点小标、纪念小旗帜、AI 星星标签、小花标签、纸质胶囊标签底纹、编辑小铅笔贴纸。

输出要求：每个元素单独一张透明 PNG，元素外部透明裁剪，适合放入 assets/image2/design-assets/tag-management/。
```

## 20. `assets/design/情侣动态详情页.png`

输出目录：`assets/image2/design-assets/couple-activity-detail/`

```text
请参考上传的《情侣动态详情页》效果图，提取并重新绘制情侣动态详情页的装饰素材。不要生成完整动态卡片、文字、按钮或评论 UI。

需要生成的单个透明 PNG 素材包括：故事节点纸页、动态类型贴纸、点赞爱心、收藏书签、评论气泡、相关照片角标、返回情侣空间小路标、星光花朵。

输出要求：每个元素单独一张透明 PNG，裁剪元素周围背景，适合放入 assets/image2/design-assets/couple-activity-detail/。
```

## 21. `assets/design/评论列表页.png`

输出目录：`assets/image2/design-assets/comment-list/`

```text
请参考上传的《评论列表页》效果图，提取并重新绘制评论列表页中适合前端复用的装饰元素。不要生成完整列表、头像数据、输入框、发送按钮或文字。

需要生成的单个透明 PNG 素材包括：浅粉评论气泡、回复小气泡、三点气泡贴纸、小花气泡、空评论插画、发送纸飞机贴纸、爱心星星点缀。

输出要求：每个元素单独一张透明 PNG，背景裁剪透明，适合放入 assets/image2/design-assets/comment-list/。
```

## 22. `assets/design/互动通知页.png`

输出目录：`assets/image2/design-assets/notification-page/`

```text
请参考上传的《互动通知页》效果图，提取并重新绘制页面中适合作为前端图片素材的装饰元素。不要生成完整 UI 页面，不要生成文字内容，不要生成按钮、列表卡片、标题栏等可用代码实现的界面结构。

需要生成的单个透明 PNG 素材包括：圆形返回按钮装饰、桃粉爱心贴纸组合、评论气泡贴纸、玻璃瓶信封贴纸、魔法棒贴纸、日历贴纸、顶部斜贴纸胶带、右侧书签丝带贴纸、右下角纸张折角装饰、底部信封玫瑰装饰、零散星光装饰。

输出要求：每个元素单独一张透明 PNG，元素旁边的内容裁剪成透明，不能带浅色底块，这样在改变背景色时显示图标不会突兀。适合放入 assets/image2/design-assets/notification-page/。
```

## 23. `assets/design/AI漫画生成配置页.png`

输出目录：`assets/image2/design-assets/ai-comic-config/`

```text
请参考上传的《AI漫画生成配置页》效果图，提取并重新绘制 AI 漫画配置页的装饰素材。不要生成配置表单、按钮、文字或完整页面。

需要生成的单个透明 PNG 素材包括：童话绘本风格卡插画、拍立得漫画贴纸、温柔日记纸页、选择素材文件夹、角色头像贴纸、画面设置画笔、魔法棒星点。

输出要求：每个元素单独一张透明 PNG，边缘透明裁剪，适合放入 assets/image2/design-assets/ai-comic-config/。
```

## 24. `assets/design/文本转漫画页.png`

输出目录：`assets/image2/design-assets/text-to-comic/`

```text
请参考上传的《文本转漫画页》效果图，提取并重新绘制文本转漫画页面的装饰素材。不要生成文本输入框、文字、按钮或完整页面。

需要生成的单个透明 PNG 素材包括：最近日记纸页、文字变漫画魔法箭头、分镜卡片、漫画风格小画板、羽毛笔、星光墨水、AI 温柔魔法贴纸。

输出要求：每个元素单独一张透明 PNG，裁剪干净，适合放入 assets/image2/design-assets/text-to-comic/。
```

## 25. `assets/design/照片转漫画页.png`

输出目录：`assets/image2/design-assets/photo-to-comic/`

```text
请参考上传的《照片转漫画页》效果图，提取并重新绘制照片转漫画页面的装饰素材。不要生成上传区 UI、选项、按钮、文字或完整页面。

需要生成的单个透明 PNG 素材包括：照片拍立得、照片转漫画魔法星光、人物保留小贴纸、背景风格画笔、预览卡角标、胶带、小花星星。

输出要求：每个元素单独一张透明 PNG，元素外部透明裁剪，适合放入 assets/image2/design-assets/photo-to-comic/。
```

## 26. `assets/design/AI短视频配置页.png`

输出目录：`assets/image2/design-assets/ai-video-config/`

```text
请参考上传的《AI短视频配置页》效果图，提取并重新绘制 AI 短视频配置页的装饰素材。不要生成完整配置页面、文字、按钮或选择项。

需要生成的单个透明 PNG 素材包括：温柔放映机、胶片卷、视频封面卡、音乐音符贴纸、字幕纸条、周年回顾小徽章、旅行回忆小星图、日常碎片拍立得。

输出要求：每个元素单独一张透明 PNG，背景裁剪透明，适合放入 assets/image2/design-assets/ai-video-config/。
```

## 27. `assets/design/视频预览编辑页.png`

输出目录：`assets/image2/design-assets/video-preview-edit/`

```text
请参考上传的《视频预览编辑页》效果图，提取并重新绘制视频预览编辑页的装饰素材。不要生成视频播放器 UI、时间轴、按钮、文字或完整页面。

需要生成的单个透明 PNG 素材包括：视频预览纸框、胶片片段、字幕小纸条、封面选择角标、保存成功星星、分享信封、播放小贴纸。

输出要求：每个元素单独一张透明 PNG，裁剪元素外部背景，适合放入 assets/image2/design-assets/video-preview-edit/。
```

## 28. `assets/design/生成进度页.png`

输出目录：`assets/image2/design-assets/generation-progress/`

```text
请参考上传的《生成进度页》效果图，提取并重新绘制 AI 生成进度页的插画素材。不要生成进度条、步骤文字、按钮或完整页面。

需要生成的单个透明 PNG 素材包括：魔法棒、绘本页、星点、墨水显影、分镜绘制小画板、上色颜料、装订成册小书、等待小云朵、完成星光徽章。

输出要求：每个元素单独一张透明 PNG，边缘透明裁剪，适合放入 assets/image2/design-assets/generation-progress/。
```

## 29. `assets/design/创作历史展示页.png`

输出目录：`assets/image2/design-assets/creation-history/`

```text
请参考上传的《创作历史展示页》效果图，提取并重新绘制创作历史页面的装饰素材。不要生成作品列表、文字、筛选标签或完整页面。

需要生成的单个透明 PNG 素材包括：收藏册、漫画作品贴纸、视频作品胶片、草稿纸页、失败状态温柔贴纸、空状态合上的小绘本、魔法棒、空白分镜卡片、星星。

输出要求：每个元素单独一张透明 PNG，元素外部透明裁剪，适合放入 assets/image2/design-assets/creation-history/。
```

## 30. `assets/design/纪念日添加编辑页.png`

输出目录：`assets/image2/design-assets/anniversary-edit/`

```text
请参考上传的《纪念日添加编辑页》效果图，提取并重新绘制纪念日添加编辑页面的装饰素材。不要生成表单、日期选择器、开关、按钮或文字。

需要生成的单个透明 PNG 素材包括：纪念日名称小纸条、日期日历、纪念类型标签贴纸、提醒铃铛、封面选择拍立得、保存星光、小花丝带。

输出要求：每个元素单独一张透明 PNG，背景裁剪透明，适合放入 assets/image2/design-assets/anniversary-edit/。
```

## 31. `assets/design/纪念日倒计时页.png`

输出目录：`assets/image2/design-assets/anniversary-countdown/`

```text
请参考上传的《纪念日倒计时页》效果图，提取并重新绘制纪念日倒计时页面的装饰素材。不要生成数字 UI、文字、按钮或完整页面。

需要生成的单个透明 PNG 素材包括：大数字倒计时装饰框、纪念日标题丝带、双人头像贴纸、日历、花朵、星星、爱心光晕、分享图小封面。

输出要求：每个元素单独一张透明 PNG，裁剪干净，适合放入 assets/image2/design-assets/anniversary-countdown/。
```

## 32. `assets/design/纪念日专属记录模板页.png`

输出目录：`assets/image2/design-assets/anniversary-template/`

```text
请参考上传的《纪念日专属记录模板页》效果图，提取并重新绘制纪念日记录模板页的装饰素材。不要生成模板列表、输入框、按钮或文字。

需要生成的单个透明 PNG 素材包括：第一次见面模板贴纸、生日小蛋糕、周年丝带、旅行行李贴纸、照片入口拍立得、纪念日纸页、小花星星。

输出要求：每个元素单独一张透明 PNG，外部背景裁剪为透明，适合放入 assets/image2/design-assets/anniversary-template/。
```

## 33. `assets/design/PDF导出配置页.png`

输出目录：`assets/image2/design-assets/pdf-export-config/`

```text
请参考上传的《PDF导出配置页》效果图，提取并重新绘制 PDF 导出配置页的装饰素材。不要生成选项列表、开关、按钮、文字或完整页面。

需要生成的单个透明 PNG 素材包括：回忆册封面、PDF 文件纸页、导出范围小日历、绘本样式贴纸、拍立得样式贴纸、纪念册样式贴纸、生成预览魔法星光。

输出要求：每个元素单独一张透明 PNG，裁剪透明边缘，适合放入 assets/image2/design-assets/pdf-export-config/。
```

## 34. `assets/design/导出预览页.png`

输出目录：`assets/image2/design-assets/export-preview/`

```text
请参考上传的《导出预览页》效果图，提取并重新绘制导出预览页中的装饰素材。不要生成完整预览页、文字、按钮或页面缩略图列表。

需要生成的单个透明 PNG 素材包括：绘本封面预览、页面缩略纸页、导出 PDF 小图标、分享信封、保存书签、琥珀金书签、照片角标、纸页纹理边角。

输出要求：每个元素单独一张透明 PNG，背景透明裁剪，适合放入 assets/image2/design-assets/export-preview/。
```

## 35. `assets/design/数据备份恢复页.png`

输出目录：`assets/image2/design-assets/data-backup-restore/`

```text
请参考上传的《数据备份恢复页》效果图，提取并重新绘制备份恢复页面的装饰素材。不要生成统计卡、按钮、文字或完整页面。

需要生成的单个透明 PNG 素材包括：云备份小云朵、恢复数据小盒子、安全锁、日记数据小本子、照片数据拍立得、AI 作品星星册、纪念日日历、温柔安全提示盾牌。

输出要求：每个元素单独一张透明 PNG，元素周围背景裁剪为透明，适合放入 assets/image2/design-assets/data-backup-restore/。
```

## 36. `assets/design/存储空间管理页.png`

输出目录：`assets/image2/design-assets/storage-management/`

```text
请参考上传的《存储空间管理页》效果图，提取并重新绘制存储空间管理页面的装饰素材。不要生成进度条、分类列表、按钮、文字或完整页面。

需要生成的单个透明 PNG 素材包括：存储空间小盒子、照片文件夹、视频胶片、AI 作品小书、缓存清理扫帚、会员空间星星徽章、温柔纸感容量装饰。

输出要求：每个元素单独一张透明 PNG，裁剪干净透明，适合放入 assets/image2/design-assets/storage-management/。
```

## 37. `assets/design/搜索页.png`

输出目录：`assets/image2/design-assets/search-page/`

```text
请参考上传的《搜索页》效果图，提取并重新绘制搜索页中的装饰素材。不要生成搜索框、结果列表、分类标签、文字或完整页面。

需要生成的单个透明 PNG 素材包括：放大镜在绘本页上寻找星星和爱心的空状态插画、搜索小星星、最近搜索纸条、结果卡角标、小花爱心、柔粉光晕。

输出要求：每个元素单独一张透明 PNG，元素外部裁剪透明，适合放入 assets/image2/design-assets/search-page/。
```

## 38. `assets/design/草稿箱.png`

输出目录：`assets/image2/design-assets/drafts-page/`

```text
请参考上传的《草稿箱》效果图，提取并重新绘制草稿箱页面的装饰素材。不要生成草稿列表、文字、按钮或完整页面。

需要生成的单个透明 PNG 素材包括：空白纸页、羽毛笔、草稿小夹子、未完成日记纸条、照片说明拍立得、AI 草稿魔法星、删除清理小扫帚、小花星光。

输出要求：每个元素单独一张透明 PNG，裁剪为透明边缘，适合放入 assets/image2/design-assets/drafts-page/。
```

## 39. `assets/design/分享预览页.png`

输出目录：`assets/image2/design-assets/share-preview/`

```text
请参考上传的《分享预览页》效果图，提取并重新绘制分享预览页里的装饰素材。不要生成分享预览 UI、隐私选项、按钮、文字或完整页面。

需要生成的单个透明 PNG 素材包括：分享封面卡、童话绘本样式封面、拍立得样式封面、纪念册样式封面、隐私小锁、隐藏昵称小贴纸、生成分享图星光、信封玫瑰。

输出要求：每个元素单独一张透明 PNG，外部背景裁剪透明，适合放入 assets/image2/design-assets/share-preview/。
```

## 40. `assets/design/会员权益说明页.png`

输出目录：`assets/image2/design-assets/membership-page/`

```text
请参考上传的《会员权益说明页》效果图，提取并重新绘制会员权益页中的装饰素材。不要生成方案卡、权益文字、按钮或完整页面。

需要生成的单个透明 PNG 素材包括：琥珀金会员徽章、皇冠贴纸、更多 AI 次数魔法星、高清导出书签、云备份小云、专属封面小册子、温柔金色光晕。

输出要求：每个元素单独一张透明 PNG，背景裁剪透明，适合放入 assets/image2/design-assets/membership-page/。
```

## 41. `assets/design/帮助与反馈页.png`

输出目录：`assets/image2/design-assets/help-feedback/`

```text
请参考上传的《帮助与反馈页》效果图，提取并重新绘制帮助反馈页的装饰素材。不要生成 FAQ 列表、输入框、文字、按钮或完整页面。

需要生成的单个透明 PNG 素材包括：帮助小问号贴纸、反馈信封、客服小花、常见问题纸条、联系支持小纸飞机、温柔提示星星、奶油纸便签。

输出要求：每个元素单独一张透明 PNG，裁剪干净，适合放入 assets/image2/design-assets/help-feedback/。
```

## 42. `assets/design/设置页.png`

输出目录：`assets/image2/design-assets/settings-page/`

```text
请参考上传的《设置页》效果图，提取并重新绘制设置页中的装饰素材。不要生成设置列表、开关、箭头、文字或完整页面。

需要生成的单个透明 PNG 素材包括：通知铃铛贴纸、隐私小锁、主题调色盘、缓存清理扫帚、账号小头像、设置齿轮贴纸、纸感分组角标、小星光。

输出要求：每个元素单独一张透明 PNG，元素外部透明裁剪，适合放入 assets/image2/design-assets/settings-page/。
```

## 43. `assets/design/空状态页.png`

输出目录：`assets/image2/design-assets/empty-state-page/`

```text
请参考上传的《空状态页》效果图，提取并重新绘制统一空状态页面中的插画和装饰素材。不要生成完整页面、标题、说明文字或按钮。

需要生成的单个透明 PNG 素材包括：空白奶油纸、羽毛笔、小花、星星、爱心贴纸、空日记插画、空相册拍立得、空搜索放大镜、空 AI 历史小绘本。

输出要求：每个元素单独一张透明 PNG，裁剪元素周围背景为透明，边缘不能带浅色底块，适合放入 assets/image2/design-assets/empty-state-page/。
```
