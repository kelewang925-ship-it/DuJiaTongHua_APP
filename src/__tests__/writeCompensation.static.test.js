import fs from 'node:fs';
import path from 'node:path';

function read(relativePath) {
  return fs.readFileSync(path.join(process.cwd(), relativePath), 'utf8');
}

const diary = read('src/api/diaryApi.js');
const photo = read('src/api/photoApi.js');

describe('write compensation contracts', () => {
  test('diary upload failure cleans prior operation-owned attachments', () => {
    expect(diary).toMatch(/if \(!result\.success\)[\s\S]*?cleanupAttachments\(uploaded\)/);
    expect(diary).toMatch(/createdByOperation/);
  });

  test('diary row failure reports cleanup risk and count', () => {
    expect(diary).toMatch(/创建日记失败/);
    expect(diary).toMatch(/cleanupRequired: cleanupFailures\.length > 0/);
    expect(diary).toMatch(/failedCleanupCount: cleanupFailures\.length/);
  });

  test('attachment row failure removes diary before cleaning uploaded objects', () => {
    const rollbackIndex = diary.indexOf("from('diaries').delete()");
    const cleanupIndex = diary.indexOf('cleanupAttachments(uploaded)', rollbackIndex);
    expect(rollbackIndex).toBeGreaterThan(-1);
    expect(cleanupIndex).toBeGreaterThan(rollbackIndex);
    expect(diary).toContain('保存日记附件失败，已尝试回滚日记');
  });

  test('photo upload and collection failures clean operation-owned objects', () => {
    expect(photo).toMatch(/if \(!result\.success\)[\s\S]*?cleanupFiles\(files\)/);
    expect(photo).toMatch(/创建照片集失败/);
    expect(photo).toMatch(/createdByOperation/);
    expect(photo).toMatch(/cleanupRequired/);
    expect(photo).toMatch(/failedCleanupCount/);
  });

  test('photo row failure deletes its collection before storage cleanup', () => {
    const rollbackIndex = photo.indexOf("from('photo_collections').delete()");
    const cleanupIndex = photo.indexOf('cleanupFiles(files)', rollbackIndex);
    expect(rollbackIndex).toBeGreaterThan(-1);
    expect(cleanupIndex).toBeGreaterThan(rollbackIndex);
    expect(photo).toContain('保存照片失败，已尝试回滚照片集');
  });

  test('database delete success with storage failure is not reported as success', () => {
    expect(diary).toMatch(/日记已删除，但部分附件清理失败/);
    expect(photo).toMatch(/照片集已删除，但部分云端文件清理失败/);
  });
});
