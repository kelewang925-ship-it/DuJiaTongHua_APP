import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.resolve(__dirname, '../../app/data/export-preview.js'), 'utf8');

describe('export preview real-content guards', () => {
  test('requires a valid route configuration and real selected content', () => {
    expect(source).toMatch(/const hasContent = validConfig && itemCount > 0/);
    expect(source).toMatch(/previewPages = hasContent \?/);
    expect(source).toMatch(/fileSize = hasContent \?/);
    expect(source).toMatch(/没有可导出的内容/);
    expect(source).toMatch(/当前没有可导出的真实内容/);
    expect(source).not.toMatch(/Math\.max\(8/);
    expect(source).not.toMatch(/Math\.max\(6\.2/);
    expect(source).not.toMatch(/photoCount \|\| 3/);
  });

  test('rejects invalid route parameters instead of defaulting to every section', () => {
    expect(source).toContain("const allowedPapers = new Set(['A4', 'A5', '正方形'])");
    expect(source).toContain("const allowedQualities = new Set(['标准', '高清', '超清'])");
    expect(source).toMatch(/included\.length > 0/);
    expect(source).toMatch(/Boolean\(coverMap\[coverKey\]\)/);
    expect(source).toMatch(/allowedPapers\.has\(requestedPaper\)/);
    expect(source).toMatch(/allowedQualities\.has\(requestedQuality\)/);
  });

  test('builds chapter samples only when matching records exist', () => {
    expect(source).toMatch(/if \(!hasContent\) return \[\]/);
    expect(source).toMatch(/included\.includes\('diary'\) && counts\.diary/);
    expect(source).toMatch(/included\.filter\(\(key\) => counts\[key\] > 0\)/);
  });
});
