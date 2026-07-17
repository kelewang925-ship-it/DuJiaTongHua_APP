import { createApiError, createApiResponse, normalizeError } from '../api/client';
import {
  compactPayload,
  fromDatabase,
  normalizeDateOnly,
  normalizePhotoCollection,
  normalizeTimestamp,
  toDatabase,
} from '../api/mappers';

describe('API response contract', () => {
  test('success response always includes the four protocol fields', () => {
    expect(createApiResponse({ id: 1 }, { cached: false })).toEqual({
      success: true,
      data: { id: 1 },
      meta: { cached: false },
      error: null,
    });
  });

  test('error response is page-displayable and exposes normalized public codes', () => {
    const input = { message: 'permission denied', code: '42501' };
    const response = createApiError(input, '保存失败');
    expect(response.success).toBe(false);
    expect(response.data).toBeNull();
    expect(response.meta).toBeNull();
    expect(response.error).toMatchObject({ message: '当前账号没有权限执行此操作', code: 'PERMISSION_DENIED', category: 'permission' });
    expect(response.error.raw).toBe(input);
  });

  test.each([
    [{ message: 'JWT expired', status: 401 }, 'SESSION_EXPIRED'],
    [{ message: 'permission denied', status: 403 }, 'PERMISSION_DENIED'],
    [{ message: 'Failed to fetch' }, 'NETWORK_ERROR'],
    [{ message: 'duplicate key value', code: '23505' }, 'CONFLICT'],
  ])('classifies common errors for page state handling', (input, expectedCode) => {
    expect(normalizeError(input).code).toBe(expectedCode);
  });
});

describe('database mapper and dates', () => {
  test('maps nested snake_case and camelCase consistently', () => {
    expect(fromDatabase({ created_at: '2026-07-17', nested_value: { user_id: 'u1' } })).toEqual({
      createdAt: '2026-07-17',
      nestedValue: { userId: 'u1' },
    });
    expect(toDatabase({ createdAt: '2026-07-17', nestedValue: { userId: 'u1' } })).toEqual({
      created_at: '2026-07-17',
      nested_value: { user_id: 'u1' },
    });
  });

  test.each([
    ['2026-07-17', '2026-07-17'],
    ['2026.07.17', '2026-07-17'],
    ['2026/07/17', '2026-07-17'],
    ['2026/07/17 12:00', '2026-07-17'],
    ['2026-07-17T08:00:00Z', '2026-07-17'],
  ])('normalizes supported date input %s', (input, expected) => {
    expect(normalizeDateOnly(input)).toBe(expected);
  });

  test.each(['not-a-date', '2026-02-30', '2026/13/01', '2026/07/17 25:00'])('rejects invalid date input %s', (input) => {
    expect(normalizeDateOnly(input)).toBeNull();
  });

  test('normalizes timestamps and rejects invalid timestamps', () => {
    expect(normalizeTimestamp('2026-07-17T08:00:00Z')).toBe('2026-07-17T08:00:00.000Z');
    expect(normalizeTimestamp('invalid')).toBeNull();
  });

  test('drops undefined write fields and safely normalizes photo collections', () => {
    expect(compactPayload({ title: 'story', note: undefined, tags: [] })).toEqual({ title: 'story', tags: [] });
    expect(normalizePhotoCollection({ id: 'c1', photos: [{ storage_path: 'x' }] })).toMatchObject({
      id: 'c1',
      photoCount: 1,
      photos: [{ storagePath: 'x' }],
    });
  });
});
