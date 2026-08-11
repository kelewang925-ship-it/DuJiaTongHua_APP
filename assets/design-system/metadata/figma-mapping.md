# Figma Mapping

Figma Asset Key 必须与 `metadata/assets.json` 的 `id` 一致。

| Figma Asset Key | Figma 页面 | React Native 源路径 |
| --- | --- | --- |
| `home-cover-v1` | `03 Assets / Illustrations` | `assets/images/illustrations/home-cover-v1.png` |
| `workshop-cover-v1` | `03 Assets / Illustrations` | `assets/images/illustrations/workshop-cover-v1.png` |
| `heart-sticker-v1` | `03 Assets / Stickers` | `assets/images/stickers/heart-sticker-v1.png` |
| `flower-sticker-v1` | `03 Assets / Stickers` | `assets/images/stickers/flower-sticker-v1.png` |
| `tape-pink-v1` | `03 Assets / Stickers` | `assets/images/stickers/tape-pink-v1.png` |
| `cream-paper-texture-v1` | `03 Assets / Backgrounds` | `assets/images/backgrounds/cream-paper-texture-v1.png` |
| `share-preview-cover-v1` | `03 Assets / Covers` | `assets/images/covers/share-preview-cover-v1.png` |

Reference 页面只能引用已有 Asset Key。若资源尚未导入，使用 `pending` 状态，不创建虚假映射。

