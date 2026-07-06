export const mockStates = ['empty', 'normal', 'loading', 'error'];

const mockRegistry = new Map();
const listeners = new Set();

function notify() {
  const snapshot = getAllMockStates();
  listeners.forEach((listener) => listener(snapshot));
}

export function switchMock(apiName, state) {
  if (!apiName || !mockStates.includes(state)) {
    return false;
  }

  mockRegistry.set(apiName, state);
  notify();
  return true;
}

export function getMockState(apiName, fallbackState = 'normal') {
  return mockRegistry.get(apiName) || fallbackState;
}

export function getAllMockStates() {
  return Array.from(mockRegistry.entries()).reduce((result, [apiName, state]) => {
    result[apiName] = state;
    return result;
  }, {});
}

export function subscribeMockStates(listener) {
  listeners.add(listener);
  listener(getAllMockStates());

  return () => {
    listeners.delete(listener);
  };
}
