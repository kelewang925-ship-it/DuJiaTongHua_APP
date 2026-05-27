const fairyImages = {
  homeCover: {
    key: 'homeCover',
    title: '首页恋爱绘本封面',
    scene: 'cover',
    localSource: null,
    plannedPath: 'assets/images/illustrations/home-cover-v1.png',
    description: '首页顶部核心插画，表现一本正在展开的恋爱童话绘本。',
  },
  coupleCover: {
    key: 'coupleCover',
    title: '情侣空间双人宇宙',
    scene: 'cover',
    localSource: null,
    plannedPath: 'assets/images/illustrations/couple-space-cover-v1.png',
    description: '情侣空间顶部核心插画，表现两个人共同维护的小小宇宙。',
  },
  workshopCover: {
    key: 'workshopCover',
    title: '童话工坊魔法屋',
    scene: 'workshop',
    localSource: null,
    plannedPath: 'assets/images/illustrations/workshop-cover-v1.png',
    description: '童话工坊顶部核心插画，表现 AI 把回忆变成漫画和视频的魔法感。',
  },
  albumCover: {
    key: 'albumCover',
    title: '相册绘本封面',
    scene: 'album',
    localSource: null,
    plannedPath: 'assets/images/illustrations/album-cover-v1.png',
    description: '相册与照片模块的绘本封面图。',
  },
  anniversaryCover: {
    key: 'anniversaryCover',
    title: '纪念日封面',
    scene: 'anniversary',
    localSource: null,
    plannedPath: 'assets/images/illustrations/anniversary-cover-v1.png',
    description: '纪念日模块的核心插画封面。',
  },
};

export function getFairyImage(key) {
  return fairyImages[key] || fairyImages.homeCover;
}

export default fairyImages;
