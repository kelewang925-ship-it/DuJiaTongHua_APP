import fs from 'fs';
import path from 'path';

describe('diary attachment compensation ownership', () => {
  const source = fs.readFileSync(path.join(process.cwd(), 'src/api/diaryApi.js'), 'utf8');

  test('only operation-owned attachments are cleaned up', () => {
    expect(source).toContain('item?.storagePath && item.createdByOperation');
    expect(source).toContain('createdByOperation: false');
    expect(source).toContain('createdByOperation: true');
  });

  test('exception paths attempt cleanup and expose cleanup metadata', () => {
    expect(source).toContain('const cleanupFailures = await cleanupAttachments(uploaded);');
    expect(source).toContain('failedCleanupCount: cleanupFailures.length');
    expect(source).toContain("return createApiError(error, '创建日记失败'");
  });

  test('persisted attachment deletion remains explicit', () => {
    expect(source).toContain('persistedAttachments');
    expect(source).toContain("deleteFile('diary-attachments', item.storagePath)");
  });
});
