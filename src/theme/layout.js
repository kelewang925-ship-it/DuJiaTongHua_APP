// src/theme/layout.js - Fairy Design System v2.0
// 布局系统：栅格、间距、圆角、阴影、层级、安全区域

export const grid = {
  columns: 4,
  gutter: 16,
  margin: {
    xs: 12,
    sm: 16,
    md: 20,
    lg: 24,
  },
};

export const spacing = {
  0: 0,
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  '2xl': 24,
  '3xl': 32,
  '4xl': 48,
};

export const radius = {
  none: 0,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  '2xl': 24,
  full: 9999,
};

export const shadows = {
  sm: {
    shadowColor: '#6B4F4F',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.04,
    shadowRadius: 8,
    elevation: 1,
  },
  md: {
    shadowColor: '#B08A8F',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.08,
    shadowRadius: 18,
    elevation: 3,
  },
  lg: {
    shadowColor: '#6B4F4F',
    shadowOffset: { width: 0, height: 12 },
    shadowOpacity: 0.12,
    shadowRadius: 30,
    elevation: 6,
  },
  xl: {
    shadowColor: '#4A3636',
    shadowOffset: { width: 0, height: 20 },
    shadowOpacity: 0.16,
    shadowRadius: 50,
    elevation: 10,
  },
};

export const zIndex = {
  background: 0,
  content: 10,
  floating: 50,
  drawer: 80,
  modal: 100,
  overlay: 150,
  toast: 200,
  loading: 300,
};

export const safeArea = {
  top: 44,
  bottom: 34,
  side: 16,
};

// 兼容旧版导出
export default {
  spacing,
  radius,
  shadows,
  zIndex,
  safeArea,
  grid,
};
