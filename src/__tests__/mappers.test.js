import {
  compactPayload,
  fromDatabase,
  normalizeDateOnly,
  normalizePhotoCollection,
  normalizeTimestamp,
  toDatabase,
} from '../api/mappers';

describe('database mappers', () => {
  test('recursively maps snake_case and camelCase without undefined fields', () => {
    expect(fromDatabase({ created_at: 'now', nested_rows: [{ user_id: 'u1' }] })).toEqual({ createdAt: 'now', nestedRows: [{ userId: 'u1' }] });
    expect(toDatabase({ createdAt: 'now', ignored: undefined, userProfile: { avatarUrl: 'x' } })).toEqual({ created_at: 'now', user_profile: { avatar_url: 'x' } });
  });

  test('normalizes collection photos', () => {
    const value = normalizePhotoCollection({ id: 'c1', photos: [{ storage_path: 'a/b' }] });
    expect(value.photos[0].storagePath).toBe('a/b');
    expect(value.photoCount).toBe(1);
  });

  test.each([
    ['2026-07-17', '2026-07-17'],
    ['2026.07.17', '2026-07-17'],
    ['2026/07/17', '2026-07-17'],
    ['2026-02-30', null],
    ['not-a-date', null],
  ])('normalizes date-only value %s', (input, expected) => {
    expect(normalizeDateOnly(input)).toBe(expected);
  });

  test('normalizes timestamps and rejects invalid values', () => {
    expect(normalizeTimestamp('2026-07-17T08:00:00Z')).toBe('2026-07-17T08:00:00.000Z');
    expect(normalizeTimestamp('invalid')).toBeNull();
  });

  test('compacts write payloads without removing explicit nulls', () => {
    expect(compactPayload({ title: 'A', optional: undefined, cleared: null })).toEqual({ title: 'A', cleared: null });
  });
});
