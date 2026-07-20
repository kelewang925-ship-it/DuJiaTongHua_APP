// src/theme/motion.js - Fairy Design System v2.0
// 动效系统

export const duration = {
  instant: 0,
  fast: 100,
  normal: 200,
  slow: 300,
  slower: 400,
  loading: 1000,
};

export const easing = {
  standard: [0.4, 0.0, 0.2, 1],
  decelerate: [0.0, 0.0, 0.2, 1],
  accelerate: [0.4, 0.0, 1, 1],
  spring: [0.34, 1.56, 0.64, 1],
  overshoot: [0.34, 1.8, 0.64, 1],
  linear: [0, 0, 1, 1],
};

export const animationPresets = {
  buttonPress: {
    scale: 0.96,
    opacity: 0.9,
    duration: duration.fast,
    easing: easing.standard,
  },
  buttonRelease: {
    scale: 1.0,
    opacity: 1.0,
    duration: duration.normal,
    easing: easing.spring,
  },
  dialogEnter: {
    opacity: 1,
    scale: 1.0,
    translateY: 0,
    duration: duration.slow,
    easing: easing.decelerate,
  },
  dialogExit: {
    opacity: 0,
    scale: 0.95,
    duration: duration.normal,
    easing: easing.accelerate,
  },
  pageEnter: {
    opacity: 1,
    translateX: 0,
    duration: duration.slower,
    easing: easing.decelerate,
  },
  pageExit: {
    opacity: 0,
    translateX: -20,
    duration: duration.normal,
    easing: easing.accelerate,
  },
  listItemEnter: {
    opacity: 1,
    translateY: 0,
    duration: duration.slow,
    easing: easing.decelerate,
    stagger: 50,
  },
  heartBurst: {
    scale: [0, 1.3, 1.0],
    opacity: [0, 1, 0.8],
    duration: 400,
    easing: easing.spring,
  },
  toastEnter: {
    translateY: 0,
    opacity: 1,
    duration: duration.slow,
    easing: easing.decelerate,
  },
  toastExit: {
    translateY: -20,
    opacity: 0,
    duration: duration.normal,
    easing: easing.accelerate,
  },
};

export const haptics = {
  light: 'light',
  medium: 'medium',
  heavy: 'heavy',
  success: 'success',
  warning: 'warning',
};

export const loadingMessages = {
  aiComic: [
    '魔法画笔正在悄悄涂色...',
    '小精灵正在整理你的回忆...',
    '故事书正在一页页成型...',
    '彩色铅笔在纸上跳舞...',
  ],
  aiVideo: [
    '时光机正在运转...',
    '回忆正在变成电影...',
    '每一帧都是爱的瞬间...',
  ],
  network: [
    '传信的小信使正在赶路...',
    '小信使飞过山川河流...',
    '信件正在穿越云层...',
  ],
  save: [
    '回忆正在藏进故事书...',
    '小精灵正在装订书页...',
    '这段故事已被温柔收藏...',
  ],
  delete: [
    '回忆正在藏进小黑屋...',
    '小精灵正在整理书架...',
  ],
};

export default {
  duration,
  easing,
  animationPresets,
  haptics,
  loadingMessages,
};
