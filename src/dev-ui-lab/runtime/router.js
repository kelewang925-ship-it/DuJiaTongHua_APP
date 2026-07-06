import { router } from 'expo-router';
import { canUseDevUI } from './env';

export const DEV_UI_HOME_PATH = '/dev-ui-lab';

export function navigateTo(path, params) {
  if (!canUseDevUI()) {
    return false;
  }

  router.push(params ? { pathname: path, params } : path);
  return true;
}

export function openDevUI() {
  return navigateTo(DEV_UI_HOME_PATH);
}
