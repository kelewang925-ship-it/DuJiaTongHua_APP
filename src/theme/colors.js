// src/theme/colors.js - Fairy Design System v2.0
// 完整语义化色彩系统

export const primitiveColors = {
  pink: {
    50: '#FEF2F4',
    100: '#FCE7EB',
    200: '#FAD0D8',
    300: '#F6BEC8',
    400: '#DFA0AC',
    500: '#C98A96',
    600: '#A66D78',
  },
  rose: {
    50: '#FAF4F2',
    100: '#F5EAE6',
    200: '#E9D7D2',
    300: '#D4BDB6',
    400: '#B08A8F',
    500: '#8B6E72',
  },
  cream: {
    50: '#FFFFFF',
    100: '#FFFDF9',
    200: '#FDFBF7',
    300: '#F8F6F2',
    400: '#F0EDE6',
  },
  cocoa: {
    50: '#C4A898',
    100: '#9B7A7A',
    200: '#8B7355',
    300: '#6B4F4F',
    400: '#4A3636',
  },
  gold: {
    100: '#F7E8D5',
    200: '#D8B384',
    300: '#B8965E',
  },
  semantic: {
    success: { 300: '#8FBC8F', 500: '#6B9E6B' },
    warning: { 300: '#E8C97A', 500: '#C4A55A' },
    error: { 300: '#E8A090', 500: '#C47A6A' },
    info: { 300: '#A0C4E8', 500: '#7AA0C4' },
  },
};

export const semanticColors = {
  bg: {
    primary: primitiveColors.cream[300],
    secondary: primitiveColors.cream[200],
    tertiary: primitiveColors.cream[100],
    elevated: primitiveColors.cream[50],
    sunken: primitiveColors.cream[400],
    pink: primitiveColors.pink[200],
    gold: primitiveColors.gold[100],
  },
  text: {
    primary: primitiveColors.cocoa[300],
    secondary: primitiveColors.cocoa[100],
    tertiary: primitiveColors.cocoa[50],
    inverse: primitiveColors.cream[50],
    accent: primitiveColors.pink[400],
    gold: primitiveColors.gold[200],
  },
  border: {
    default: `${primitiveColors.rose[300]}2E`,
    focus: primitiveColors.pink[300],
    error: primitiveColors.semantic.error[300],
    divider: `${primitiveColors.rose[200]}4D`,
  },
  surface: {
    card: primitiveColors.cream[100],
    cardPink: primitiveColors.pink[100],
    floating: primitiveColors.cream[50],
    overlay: `${primitiveColors.cocoa[300]}66`,
  },
  state: {
    success: primitiveColors.semantic.success[300],
    warning: primitiveColors.semantic.warning[300],
    error: primitiveColors.semantic.error[300],
    info: primitiveColors.semantic.info[300],
  },
};

export const darkColors = {
  bg: {
    primary: '#2A2520',
    secondary: '#332D28',
    tertiary: '#3D3630',
    elevated: '#4A423A',
    sunken: '#1E1A16',
  },
  text: {
    primary: '#E8DDD4',
    secondary: '#A89888',
    tertiary: '#6B5E52',
    inverse: '#2A2520',
    accent: '#DFA0AC',
    gold: '#D8B384',
  },
  border: {
    default: `${primitiveColors.rose[500]}40`,
    focus: primitiveColors.pink[400],
    error: primitiveColors.semantic.error[500],
    divider: `${primitiveColors.rose[500]}30`,
  },
  surface: {
    card: '#3D3630',
    cardPink: '#4A3630',
    floating: '#4A423A',
    overlay: '#1E1A1680',
  },
  state: {
    success: primitiveColors.semantic.success[500],
    warning: primitiveColors.semantic.warning[500],
    error: primitiveColors.semantic.error[500],
    info: primitiveColors.semantic.info[500],
  },
};

// 兼容旧版导出
export default {
  ...semanticColors,
  primitive: primitiveColors,
  dark: darkColors,
};
