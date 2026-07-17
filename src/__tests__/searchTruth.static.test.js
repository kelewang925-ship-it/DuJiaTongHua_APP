import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.join(process.cwd(), 'app/search.js'), 'utf8');

describe('search real-data truth guards', () => {
  test('missing anniversary descriptions remain empty', () => {
    expect(source).toContain("description: item.description || item.note || ''");
    expect(source).not.toContain('这是你们童话里值得记住的一章。');
  });

  test('missing AI metadata is not replaced with workshop story copy', () => {
    expect(source).toContain("[item.source, item.status].filter(Boolean).join(' · ')");
    expect(source).toContain("tags: [item.type, item.styleName].filter(Boolean)");
    expect(source).not.toContain("item.styleName || '童话绘本'");
    expect(source).not.toContain("item.source || '童话工坊'");
  });

  test('missing dates remain absent', () => {
    expect(source).toContain("if (!value) return '';");
    expect(source).not.toContain("item.date || '值得纪念的一天'");
    expect(source).not.toContain("return '童话工坊'");
  });

  test('real results use category placeholders rather than unrelated design covers', () => {
    expect(source).toContain('isReal ? <View style={[styles.realThumbPlaceholder');
    expect(source).toContain("categoryIcons[item.category] || 'document-outline'");
  });

  test('missing summaries are disclosed', () => {
    expect(source).toContain('没有可展示的摘要');
  });
});
