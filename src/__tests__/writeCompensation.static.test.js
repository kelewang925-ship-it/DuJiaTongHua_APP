import fs from 'node:fs';
import path from 'node:path';

function read(relativePath) {
  return fs.readFileSync(path.join(process.cwd(), relativePath), 'utf8');
}

const diary = read('src/api/diaryApi.js');
const photo = read('src/api/photoApi.js');

describe('write compensation contracts', () => {
  test('diary upload failure cleans prior attachments', () => {
    expect(diary).toMatch(/if \(!result\.success\)[\s\S]*?cleanupAttachments\(uploaded\)/);
  });

  test('diary row failure reports cleanup risk', () => {
    expect(diary).toMatch(/createApiError\(error, '创建日记失败'\)/);
    expect(diary).toMatch(/cleanupRequired: cleanupFailures\.length > 0/);
  });

  test('attachment row failure removes diary and uploaded objects', () => {
    expect(diary).toMatch(/from\('diaries'\)\.delete\(\)/);
    expect(diary).toMatch(/保存日记附件失败，已回滚日记/);
    expect(diary).toMatch(/cleanupAttachments\(uploaded\)/);
  });

  test('photo upload and collection failures clean uploaded objects', () => {
    expect(photo).toMatch(/if \(!result\.success\)[\s\S]*?cleanupFiles\(files\)/);
    expect(photo).toMatch(/创建照片集失败/);
    expect(photo).toMatch(/cleanupRequired: cleanupFailures\.length > 0/);
  });

  test('photo row failure deletes its collection before storage cleanup', () => {
    expect(photo).toMatch(/from\('photo_collections'\)\.delete\(\)/);
    expect(photo).toMatch(/保存照片失败，已回滚照片集/);
    expect(photo).toMatch(/cleanupFiles\(files\)/);
  });

  test('database delete success with storage failure is not reported as success', () => {
    expect(diary).toMatch(/日记已删除，但部分附件清理失败/);
    expect(photo).toMatch(/照片集已删除，但部分云端文件清理失败/);
  });
});
