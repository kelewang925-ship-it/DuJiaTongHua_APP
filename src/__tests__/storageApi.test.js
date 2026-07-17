import { validateStoragePath } from '../api/storageApi';

describe('validateStoragePath', () => {
  const context = { coupleId: '11111111-1111-4111-8111-111111111111', user: { id: '22222222-2222-4222-8222-222222222222' } };
  const objectId = '33333333-3333-4333-8333-333333333333';

  it('accepts the required couple/user/uuid path', () => {
    expect(validateStoragePath('photos', `${context.coupleId}/${context.user.id}/${objectId}`, context)).toMatchObject({ objectId });
  });

  it('rejects another couple path', () => {
    expect(() => validateStoragePath('photos', `44444444-4444-4444-8444-444444444444/${context.user.id}/${objectId}`, context)).toThrow('文件不属于当前情侣空间');
  });

  it('rejects another user path for writes and deletes', () => {
    expect(() => validateStoragePath('diary-attachments', `${context.coupleId}/55555555-5555-4555-8555-555555555555/${objectId}`, context)).toThrow('只能操作当前用户拥有的文件');
  });

  it('rejects unsupported buckets and malformed paths', () => {
    expect(() => validateStoragePath('exports', `${context.coupleId}/${context.user.id}/${objectId}`, context)).toThrow('不支持的文件存储类型');
    expect(() => validateStoragePath('photos', `${context.coupleId}/${context.user.id}/photo.jpg`, context)).toThrow('文件路径必须符合');
  });
});
