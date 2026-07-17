const UUID_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

function randomHex(length) {
  let value = '';
  for (let index = 0; index < length; index += 1) value += Math.floor(Math.random() * 16).toString(16);
  return value;
}

export function createStorageObjectId() {
  const nativeId = globalThis.crypto?.randomUUID?.();
  if (nativeId && UUID_PATTERN.test(nativeId)) return nativeId;
  return `${randomHex(8)}-${randomHex(4)}-4${randomHex(3)}-${['8', '9', 'a', 'b'][Math.floor(Math.random() * 4)]}${randomHex(3)}-${randomHex(12)}`;
}

export function isStorageObjectId(value) {
  return UUID_PATTERN.test(String(value || ''));
}

export function buildStoragePath(coupleId, userId, objectId = createStorageObjectId()) {
  if (!coupleId || !userId || !isStorageObjectId(objectId)) throw new Error('无法创建安全的文件路径');
  return `${coupleId}/${userId}/${objectId}`;
}

export function parseStoragePath(path) {
  const parts = String(path || '').split('/').filter(Boolean);
  if (parts.length !== 3 || !isStorageObjectId(parts[2])) return null;
  return { coupleId: parts[0], userId: parts[1], objectId: parts[2] };
}
