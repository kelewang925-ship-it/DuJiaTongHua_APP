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

function isExactCalendarDate(year, month, day) {
  const date = new Date(Date.UTC(year, month - 1, day));
  return date.getUTCFullYear() === year && date.getUTCMonth() === month - 1 && date.getUTCDate() === day;
}

export function normalizeDateOnly(value) {
  if (!value) return null;
  if (value instanceof Date) {
    if (Number.isNaN(value.getTime())) return null;
    return value.toISOString().slice(0, 10);
  }

  const text = String(value).trim();
  const match = text.match(/^(\d{4})([-./])(\d{2})\2(\d{2})(?:(?:T|\s)(\d{2}):(\d{2})(?::(\d{2})(?:\.\d{1,9})?)?(?:Z|[+-]\d{2}:?\d{2})?)?$/);
  if (!match) return null;

  const year = Number(match[1]);
  const month = Number(match[3]);
  const day = Number(match[4]);
  if (!isExactCalendarDate(year, month, day)) return null;

  if (match[5] !== undefined) {
    const hour = Number(match[5]);
    const minute = Number(match[6]);
    const second = match[7] === undefined ? 0 : Number(match[7]);
    if (hour > 23 || minute > 59 || second > 59) return null;
  }

  return `${match[1]}-${match[3]}-${match[4]}`;
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
  return { ...value, photos, photoCount: value.photoCount ?? photos.length };
}
