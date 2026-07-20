// src/theme/typography.js - Fairy Design System v2.0
// 完整排版系统

export const fontFamily = {
  heading: 'System',
  body: 'System',
  mono: 'Courier',
};

export const fontSize = {
  display: 32,
  h1: 24,
  h2: 20,
  h3: 16,
  body: 14,
  bodyLg: 16,
  caption: 12,
  overline: 10,
};

export const lineHeight = {
  display: 40,
  h1: 32,
  h2: 28,
  h3: 24,
  body: 22,
  bodyLg: 26,
  caption: 18,
  overline: 14,
};

export const fontWeight = {
  regular: '400',
  medium: '500',
  semibold: '600',
  bold: '700',
};

export const typographyStyles = {
  display: {
    fontSize: fontSize.display,
    lineHeight: lineHeight.display,
    fontWeight: fontWeight.bold,
    letterSpacing: 0.02,
  },
  h1: {
    fontSize: fontSize.h1,
    lineHeight: lineHeight.h1,
    fontWeight: fontWeight.bold,
    letterSpacing: 0.01,
  },
  h2: {
    fontSize: fontSize.h2,
    lineHeight: lineHeight.h2,
    fontWeight: fontWeight.semibold,
    letterSpacing: 0,
  },
  h3: {
    fontSize: fontSize.h3,
    lineHeight: lineHeight.h3,
    fontWeight: fontWeight.semibold,
    letterSpacing: 0,
  },
  body: {
    fontSize: fontSize.body,
    lineHeight: lineHeight.body,
    fontWeight: fontWeight.regular,
    letterSpacing: 0,
  },
  bodyLg: {
    fontSize: fontSize.bodyLg,
    lineHeight: lineHeight.bodyLg,
    fontWeight: fontWeight.regular,
    letterSpacing: 0,
  },
  caption: {
    fontSize: fontSize.caption,
    lineHeight: lineHeight.caption,
    fontWeight: fontWeight.regular,
    letterSpacing: 0,
  },
  overline: {
    fontSize: fontSize.overline,
    lineHeight: lineHeight.overline,
    fontWeight: fontWeight.medium,
    letterSpacing: 0.04,
  },
};

// 兼容旧版导出
export default {
  title: { fontSize: fontSize.h1, lineHeight: lineHeight.h1, fontWeight: fontWeight.bold },
  sectionTitle: { fontSize: fontSize.h2, lineHeight: lineHeight.h2, fontWeight: fontWeight.semibold },
  subtitle: { fontSize: fontSize.h3, lineHeight: lineHeight.h3, fontWeight: fontWeight.semibold },
  body: { fontSize: fontSize.body, lineHeight: lineHeight.body, fontWeight: fontWeight.regular },
  caption: { fontSize: fontSize.caption, lineHeight: lineHeight.caption, fontWeight: fontWeight.regular },
  ...typographyStyles,
};
