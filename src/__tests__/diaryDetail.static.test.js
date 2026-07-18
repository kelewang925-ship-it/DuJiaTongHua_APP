import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.resolve(__dirname, '../../app/diary/detail.js'), 'utf8');

describe('diary detail real-record guards', () => {
  test('requires the requested diary id and renders an empty state when missing', () => {
    expect(source).toMatch(/useLocalSearchParams/);
    expect(source).toMatch(/item\.id === diaryId && item\.type === '日记'/);
    expect(source).toMatch(/没有找到这篇日记/);
  });

  test('carries the diary id into edit, comic, share and comment routes', () => {
    expect(source).toMatch(/pathname: '\/diary\/editor', params: \{ id: diary\.id \}/);
    expect(source).toMatch(/pathname: '\/ai\/text-to-comic', params: \{ id: diary\.id \}/);
    expect(source).toMatch(/pathname: '\/share-preview', params: \{ id: diary\.id, type: 'diary' \}/);
    expect(source).toMatch(/pathname: '\/comments', params: \{ id: diary\.id, type: 'diary' \}/);
  });

  test('does not silently select the first diary or invent detail metadata', () => {
    expect(source).not.toMatch(/records\.find\(\(item\) => item\.type === '日记'\)/);
    expect(source).not.toMatch(/今天的小小童话/);
    expect(source).not.toMatch(/diary\.tags \|\| \['日记'\]/);
    expect(source).not.toMatch(/console\.log\(diary\)/);
  });
});
