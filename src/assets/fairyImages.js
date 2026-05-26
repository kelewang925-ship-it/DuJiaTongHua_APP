const fairyImages = {
  homeHero: {
    key: 'homeHero',
    title: '首页恋爱绘本封面',
    scene: 'cover',
    localSource: null,
    plannedPath: 'assets/images/illustrations/home-hero.png',
    description: '首页顶部核心插画，表现一本正在展开的恋爱童话绘本。',
  },
  coupleHero: {
    key: 'coupleHero',
    title: '情侣空间双人宇宙',
    scene: 'cover',
    localSource: null,
    plannedPath: 'assets/images/illustrations/couple-hero.png',
    description: '情侣空间顶部核心插画，表现两个人共同维护的小小宇宙。',
  },
  workshopHero: {
    key: 'workshopHero',
    title: '童话工坊魔法屋',
    scene: 'workshop',
    localSource: null,
    plannedPath: 'assets/images/illustrations/workshop-hero.png',
    description: '童话工坊顶部核心插画，表现 AI 把回忆变成漫画和视频的魔法感。',
  },
};

export function getFairyImage(key) {
  return fairyImages[key] || fairyImages.homeHero;
}

export default fairyImages;
