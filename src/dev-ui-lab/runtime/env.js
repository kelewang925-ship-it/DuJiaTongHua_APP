import { Platform } from 'react-native';

export const isDev = process.env.NODE_ENV === 'development';
export const isMobile = Platform.OS === 'ios' || Platform.OS === 'android';
export const forceDevUI = process.env.EXPO_PUBLIC_DEV_UI === '1';
export const enableDevUI = isDev && (isMobile || forceDevUI);
export const devUIRuntimeInfo = {
  nodeEnv: process.env.NODE_ENV,
  platform: Platform.OS,
  forceDevUI,
  isDev,
  isMobile,
  enableDevUI,
};

export function canUseDevUI() {
  return enableDevUI;
}
