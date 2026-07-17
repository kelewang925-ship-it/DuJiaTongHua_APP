import { fromDatabase, normalizePhotoCollection, toDatabase } from '../api/mappers';

describe('database mappers', () => {
  test('recursively converts snake_case to camelCase', () => {
    expect(fromDatabase({ created_at: '2026-07-17T00:00:00.000Z', nested_value: { user_id: 'u1' } })).toEqual({
      createdAt: '2026-07-17T00:00:00.000Z',
      nestedValue: { userId: 'u1' },
    });
  });

  test('recursively converts camelCase to snake_case and removes undefined writes', () => {
    expect(toDatabase({ repeatType: 'yearly', optionalValue: undefined, nestedValue: { userId: 'u1' } })).toEqual({
      repeat_type: 'yearly',
      nested_value: { user_id: 'u1' },
    });
  });

  test('keeps ISO dates stable for UI and API boundaries', () => {
    const value = fromDatabase({ unlock_date: '2026-12-31', created_at: '2026-07-17T08:09:10.000Z' });
    expect(value.unlockDate).toBe('2026-12-31');
    expect(value.createdAt).toBe('2026-07-17T08:09:10.000Z');
  });

  test('normalizes nested photo rows and count', () => {
    expect(normalizePhotoCollection({ id: 'c1', photos: [{ storage_path: 'a/b/c' }] })).toMatchObject({
      id: 'c1',
      photoCount: 1,
      photos: [{ storagePath: 'a/b/c' }],
    });
  });
});
