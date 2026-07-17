import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.resolve(process.cwd(), 'app/data/pdf-export.js'), 'utf8');

describe('PDF export real-data guards', () => {
  test('does not fabricate photo counts', () => {
    expect(source).not.toContain('item.photoCount || 3');
    expect(source).toContain('Number.isFinite(item.photoCount) ? item.photoCount : 0');
  });

  test('does not include a fixed custom date range', () => {
    expect(source).not.toContain('2022.05.20');
    expect(source).not.toContain('2026.07.16');
    expect(source).toContain("'尚未选择自定义日期'");
  });

  test('derives loaded range from actual entities', () => {
    expect(source).toContain('const loadedRange = useMemo');
    expect(source).toContain('[...records, ...creations, ...anniversaries]');
  });

  test('blocks preview when selected content is empty', () => {
    expect(source).toContain("if (selectedCount === 0)");
    expect(source).toContain("disabled={selectedCount === 0}");
  });

  test('blocks preview while custom dates are unset', () => {
    expect(source).toContain("if (range === 'custom')");
    expect(source).toContain("message.info('请先选择自定义日期范围。')");
  });

  test('only forwards non-empty content sections', () => {
    expect(source).toContain('contents[item.key] && counts[item.key] > 0');
  });
});
