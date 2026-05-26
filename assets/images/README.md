# 《独家童话》图片资产目录

本目录用于存放项目专属图片资产，包括 AI 生成插画、贴纸、背景纹理、分享封面和用户生成结果缓存。

目录规划：

```text
assets/images/
  illustrations/       # 页面核心插画：首页、情侣空间、童话工坊、纪念日、空状态等
  stickers/            # 爱心、星星、胶带、小花、魔法棒等透明贴纸
  backgrounds/         # 月白纸感背景、柔和渐变、纹理底图
  covers/              # PDF导出封面、分享卡片封面、纪念册封面
  generated/           # 开发期或用户生成结果缓存
```

当前核心插画映射由 `src/components/FairyImage.js` 管理：

```text
homeCover       → 首页 Hero 插画
coupleCover     → 情侣空间 Hero 插画
workshopCover   → 童话工坊 Hero 插画
albumCover      → 相册相关插画
anniversaryCover→ 纪念日相关插画
```

注意：

- 不要直接把 `assets/design/png/界面设计图*.png` 整张效果图放进页面。
- 应从效果图中拆出独立插画，或重新生成单张 AI 插画后放入对应目录。
- 每次新增、替换、压缩、裁切或接入图片，都要更新 `docs/image-assets-guideline.md`。
