const fairyStickers = {
  heart: {
    key: 'heart',
    title: '爱心贴纸',
    localSource: require('../../assets/images/stickers/heart-sticker-v1.png'),
    path: 'assets/images/stickers/heart-sticker-v1.png',
    description: '用于情侣互动、点赞、时间轴和分享装饰的手绘爱心贴纸。',
  },
  star: {
    key: 'star',
    title: '星星贴纸',
    localSource: require('../../assets/images/stickers/star-sticker-v1.png'),
    path: 'assets/images/stickers/star-sticker-v1.png',
    description: '用于 AI 魔法、空状态和页面角标装饰的手绘星星贴纸。',
  },
  flower: {
    key: 'flower',
    title: '小花贴纸',
    localSource: require('../../assets/images/stickers/flower-sticker-v1.png'),
    path: 'assets/images/stickers/flower-sticker-v1.png',
    description: '用于纪念日、情侣空间和封面装饰的手绘小花贴纸。',
  },
  tapePink: {
    key: 'tapePink',
    title: '桃粉胶带贴纸',
    localSource: require('../../assets/images/stickers/tape-pink-v1.png'),
    path: 'assets/images/stickers/tape-pink-v1.png',
    description: '用于卡片顶部、回忆墙和时间轴的手账胶带贴纸。',
  },
  magicWand: {
    key: 'magicWand',
    title: '魔法棒贴纸',
    localSource: require('../../assets/images/stickers/magic-wand-v1.png'),
    path: 'assets/images/stickers/magic-wand-v1.png',
    description: '用于 AI 工坊和 AI 创作流程的魔法棒贴纸。',
  },
};

export function getFairySticker(key) {
  return fairyStickers[key] || fairyStickers.heart;
}

export default fairyStickers;
