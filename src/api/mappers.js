const camelize = (key) => key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
const snakeize = (key) => key.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);

function mapObject(value, keyMapper) {
  if (Array.isArray(value)) return value.map((item) => mapObject(item, keyMapper));
  if (value instanceof Date) return value.toISOString();
  if (!value || typeof value !== 'object') return value;
  return Object.entries(value).reduce((result, [key, item]) => {
    if (item === undefined) return result;
    result[keyMapper(key)] = mapObject(item, keyMapper);
    return result;
  }, {});
}

export const fromDatabase = (value) => mapObject(value, camelize);
export const toDatabase = (value) => mapObject(value, snakeize);
export const normalizeRecord = (row) => fromDatabase(row);

export function normalizeDateOnly(value) {
  if (!value) return null;
  if (value instanceof Date) return value.toISOString().slice(0, 10);
  const text = String(value).trim().replaceAll('.', '-').replaceAll('/', '-');
  const match = text.match(/^(\d{4})-(\d{2})-(\d{2})/);
  return match ? `${match[1]}-${match[2]}-${match[3]}` : null;
}

export function normalizeTimestamp(value) {
  if (!value) return null;
  const date = value instanceof Date ? value : new Date(value);
  return Number.isNaN(date.getTime()) ? null : date.toISOString();
}

export function compactPayload(value = {}) {
  return Object.entries(value).reduce((result, [key, item]) => {
    if (item !== undefined) result[key] = item;
    return result;
  }, {});
}

export function normalizePhotoCollection(row) {
  const value = normalizeRecord(row || {});
  const photos = Array.isArray(value.photos) ? value.photos.map(normalizeRecord) : [];
  return {
    ...value,
    photos,
    photoCount: value.photoCount ?? photos.length,
  };
}
