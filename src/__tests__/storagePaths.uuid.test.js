import { buildStoragePath, createStorageObjectId, isStorageObjectId, parseStoragePath } from '../api/storagePaths';

describe('storage path UUID helpers', () => {
  test('creates RFC 4122 compatible UUID values', () => {
    const value = createStorageObjectId();
    expect(isStorageObjectId(value)).toBe(true);
    expect(value).toMatch(/^[0-9a-f-]{36}$/i);
  });

  test('builds and parses strict couple/user/uuid paths', () => {
    const path = buildStoragePath(
      '11111111-1111-4111-8111-111111111111',
      '22222222-2222-4222-8222-222222222222'
    );
    const parsed = parseStoragePath(path);
    expect(parsed.coupleId).toBe('11111111-1111-4111-8111-111111111111');
    expect(parsed.userId).toBe('22222222-2222-4222-8222-222222222222');
    expect(isStorageObjectId(parsed.objectId)).toBe(true);
  });

  test('rejects missing scope identifiers and malformed object ids', () => {
    expect(() => buildStoragePath('', 'user')).toThrow('安全的文件路径');
    expect(() => buildStoragePath('couple', '')).toThrow('安全的文件路径');
    expect(parseStoragePath('couple/user/not-a-uuid')).toBeNull();
  });
});
