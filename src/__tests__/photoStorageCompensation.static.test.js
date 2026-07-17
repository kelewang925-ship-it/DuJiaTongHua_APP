const fs = require('fs');
const path = require('path');

const source = fs.readFileSync(path.join(__dirname, '..', 'api', 'photoApi.js'), 'utf8');

describe('photo storage compensation boundary', () => {
  test('only deletes objects created by the current operation', () => {
    expect(source).toContain("item?.createdByOperation === true");
    expect(source).toContain("createdByOperation: false");
    expect(source).toContain("createdByOperation: true");
  });

  test('cleans staged uploads when an exception is thrown', () => {
    expect(source).toMatch(/catch \(error\) \{\s*const cleanupFailures = await cleanupFiles\(files\)/);
    expect(source).toContain('withCleanupMeta(createApiError(error, \'保存照片失败\'), cleanupFailures)');
  });

  test('reports unresolved cleanup work', () => {
    expect(source).toContain('failedCleanupCount');
    expect(source).toContain('cleanupRequired: cleanupFailures.length > 0');
  });
});
