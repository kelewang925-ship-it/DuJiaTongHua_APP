import { useEffect, useRef } from 'react';
import { Linking } from 'react-native';
import { openDevUI } from '../runtime/router';
import { canUseDevUI } from '../runtime/env';

const LONG_PRESS_MS = 2000;

function hasDevParam(url) {
  if (!url || typeof url !== 'string') {
    return false;
  }

  try {
    const parsedUrl = new URL(url);
    return parsedUrl.searchParams.get('dev') === '1';
  } catch (error) {
    return /[?&]dev=1(?:&|$)/.test(url);
  }
}

export function useDevUI() {
  const timerRef = useRef(null);
  const openedRef = useRef(false);

  const clearGestureTimer = () => {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
  };

  const openOnce = () => {
    if (!canUseDevUI() || openedRef.current) {
      return;
    }

    openedRef.current = true;
    openDevUI();
    setTimeout(() => {
      openedRef.current = false;
    }, 800);
  };

  useEffect(() => {
    if (!canUseDevUI()) {
      return undefined;
    }

    globalThis.__OPEN_DEV_UI__ = openDevUI;

    Linking.getInitialURL().then((url) => {
      if (hasDevParam(url)) {
        openOnce();
      }
    });

    const subscription = Linking.addEventListener('url', ({ url }) => {
      if (hasDevParam(url)) {
        openOnce();
      }
    });

    return () => {
      clearGestureTimer();
      if (globalThis.__OPEN_DEV_UI__ === openDevUI) {
        delete globalThis.__OPEN_DEV_UI__;
      }
      subscription?.remove?.();
    };
  }, []);

  const handleTouchStart = (event) => {
    if (!canUseDevUI()) {
      return;
    }

    const touchCount = event?.nativeEvent?.touches?.length || 0;
    if (touchCount >= 2) {
      clearGestureTimer();
      timerRef.current = setTimeout(openOnce, LONG_PRESS_MS);
    }
  };

  const handleTouchEnd = () => {
    clearGestureTimer();
  };

  return {
    onTouchStart: handleTouchStart,
    onTouchEnd: handleTouchEnd,
    onTouchCancel: handleTouchEnd,
  };
}
