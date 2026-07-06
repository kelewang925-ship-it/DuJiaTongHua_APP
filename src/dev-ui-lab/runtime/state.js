export const pageStates = ['empty', 'loading', 'hasData', 'error'];

const pageStateRegistry = new Map();
const listeners = new Set();

function notify() {
  const snapshot = getAllPageStates();
  listeners.forEach((listener) => listener(snapshot));
}

export function setPageState(pageName, state) {
  if (!pageName || !pageStates.includes(state)) {
    return false;
  }

  pageStateRegistry.set(pageName, state);
  notify();
  return true;
}

export function getPageState(pageName, fallbackState = 'hasData') {
  return pageStateRegistry.get(pageName) || fallbackState;
}

export function getAllPageStates() {
  return Array.from(pageStateRegistry.entries()).reduce((result, [pageName, state]) => {
    result[pageName] = state;
    return result;
  }, {});
}

export function subscribePageStates(listener) {
  listeners.add(listener);
  listener(getAllPageStates());

  return () => {
    listeners.delete(listener);
  };
}
