import { fromDatabase, toDatabase, normalizePhotoCollection } from '../api/mappers';

describe('database mappers', () => {
  test('recursively maps snake_case and camelCase', () => {
    expect(fromDatabase({ created_at: 'now', nested_rows: [{ user_id: 'u1' }] })).toEqual({ createdAt: 'now', nestedRows: [{ userId: 'u1' }] });
    expect(toDatabase({ createdAt: 'now', userProfile: { avatarUrl: 'x' } })).toEqual({ created_at: 'now', user_profile: { avatar_url: 'x' } });
  });

  test('normalizes collection photos', () => {
    expect(normalizePhotoCollection({ id: 'c1', photos: [{ storage_path: 'a/b' }] }).photos[0].storagePath).toBe('a/b');
  });
});
