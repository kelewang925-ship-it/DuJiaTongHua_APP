import fs from 'fs';
import path from 'path';

test('pdf preview fails closed for invalid params and non-mock mode', () => {
  const source = fs.readFileSync(path.join(process.cwd(), 'app/data/export-preview.js'), 'utf8');
  expect(source).toContain("const mode = getApiMode()");
  expect(source).toContain("mode === 'mock' && hasCapability('pdfExport', mode)");
  expect(source).toContain('const validConfig = included.length > 0');
  expect(source).toContain('allowedPapers.has(requestedPaper)');
  expect(source).toContain('allowedQualities.has(requestedQuality)');
  expect(source).toContain('导出配置无效');
});
