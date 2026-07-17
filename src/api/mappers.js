const camelize = (key) => key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
const snakeize = (key) => key.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);

function mapObject(value, keyMapper) {
  if (Array.isArray(value)) return value.map((item) => mapObject(item, keyMapper));
  if (!value || typeof value !== 'object' || value instanceof Date) return value;
  return Object.entries(value).reduce((result, [key, item]) => ({
    ...result,
    [keyMapper(key)]: mapObject(item, keyMapper),
  }), {});
}

export const fromDatabase = (value) => mapObject(value, camelize);
export const toDatabase = (value) => mapObject(value, snakeize);
export const normalizeRecord = (row) => fromDatabase(row);

export function normalizePhotoCollection(row) {
  const value = normalizeRecord(row);
  return { ...value, photos: (value.photos || []).map(normalizeRecord), photoCount: value.photoCount ?? value.photos?.length ?? 0 };
}
