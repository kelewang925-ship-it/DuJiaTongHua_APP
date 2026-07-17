import {
  buildStoragePath,
  createStorageObjectId,
  isStorageObjectId,
  parseStoragePath,
} from '../api/storagePaths';

const objectId = '123e4567-e89b-42d3-a456-426614174000';

describe('storage UUID paths', () => {
  test('creates a valid UUID when native randomUUID is unavailable', () => {
    const generated = createStorageObjectId();
    expect(isStorageObjectId(generated)).toBe(true);
  });

  test('builds and parses the required couple/user/uuid namespace', () => {
    const path = buildStoragePath('couple-1', 'user-1', objectId);
    expect(path).toBe(`couple-1/user-1/${objectId}`);
    expect(parseStoragePath(path)).toEqual({ coupleId: 'couple-1', userId: 'user-1', objectId });
  });

  test.each([
    '',
    'couple/user',
    'couple/user/not-a-uuid',
    `couple/user/${objectId}/extra`,
  ])('rejects malformed path %s', (value) => {
    expect(parseStoragePath(value)).toBeNull();
  });

  test('rejects a non UUID object id at construction time', () => {
    expect(() => buildStoragePath('couple-1', 'user-1', 'unsafe-name.jpg')).toThrow('无法创建安全的文件路径');
  });
});
