export const MOCK_STORAGE_KEY = 'dujia-tonghua-mock-v1';
export const REAL_STORAGE_PREFIX = 'dujia-tonghua-real-ui-v1';

export function getRealUserStorageKey(userId) {
  return `${REAL_STORAGE_PREFIX}:${userId || 'anonymous'}`;
}

export function getStorageKey(mode, userId) {
  return mode === 'real' ? getRealUserStorageKey(userId) : MOCK_STORAGE_KEY;
}
