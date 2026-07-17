import { validateStoragePath } from '../api/storageApi';

describe('validateStoragePath', () => {
  const context = { coupleId: '11111111-1111-1111-1111-111111111111', user: { id: '22222222-2222-2222-2222-222222222222' } };

  it('accepts the required couple/user/file path', () => {
    expect(validateStoragePath('photos', `${context.coupleId}/${context.user.id}/photo.jpg`, context)).toBe(true);
  });

  it('rejects another couple path', () => {
    expect(() => validateStoragePath('photos', `33333333-3333-3333-3333-333333333333/${context.user.id}/photo.jpg`, context)).toThrow('文件不属于当前情侣空间');
  });

  it('rejects another user path for writes and deletes', () => {
    expect(() => validateStoragePath('diary-attachments', `${context.coupleId}/33333333-3333-3333-3333-333333333333/photo.jpg`, context)).toThrow('只能操作当前用户拥有的文件');
  });

  it('rejects unsupported buckets and malformed paths', () => {
    expect(() => validateStoragePath('exports', `${context.coupleId}/${context.user.id}/file.pdf`, context)).toThrow('不支持的文件存储类型');
    expect(() => validateStoragePath('photos', `${context.coupleId}/${context.user.id}`, context)).toThrow('文件路径必须符合');
  });
});
