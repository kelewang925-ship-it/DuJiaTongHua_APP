import { createStorageObjectPath, createUuid, isUuid } from '../api/storagePaths';

describe('storage path UUID helpers', () => {
  test('creates RFC 4122 compatible UUID values', () => {
    const value = createUuid();
    expect(isUuid(value)).toBe(true);
    expect(value).toMatch(/^[0-9a-f-]{36}$/i);
  });

  test('builds strict couple/user/uuid paths', () => {
    const path = createStorageObjectPath(
      '11111111-1111-4111-8111-111111111111',
      '22222222-2222-4222-8222-222222222222'
    );
    const parts = path.split('/');
    expect(parts).toHaveLength(3);
    expect(parts[0]).toBe('11111111-1111-4111-8111-111111111111');
    expect(parts[1]).toBe('22222222-2222-4222-8222-222222222222');
    expect(isUuid(parts[2])).toBe(true);
  });

  test('rejects missing scope identifiers', () => {
    expect(() => createStorageObjectPath('', 'user')).toThrow('情侣空间');
    expect(() => createStorageObjectPath('couple', '')).toThrow('用户');
  });
});
