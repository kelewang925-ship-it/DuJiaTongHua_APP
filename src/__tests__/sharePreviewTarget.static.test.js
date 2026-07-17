import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.resolve(__dirname, '../../app/share-preview.js'), 'utf8');

describe('share preview target guards', () => {
  test('resolves the requested entity from route id and type', () => {
    expect(source).toMatch(/useLocalSearchParams/);
    expect(source).toMatch(/if \(!targetId \|\| !targetType\) return null/);
    expect(source).toMatch(/creations\.find\(\(item\) => item\.id === targetId/);
    expect(source).toMatch(/records\.find\(\(item\) => item\.id === targetId\)/);
  });

  test('shows an empty state instead of falling back to the first record', () => {
    expect(source).toMatch(/没有找到要分享的内容/);
    expect(source).not.toMatch(/const latest = records\[0\]/);
    expect(source).not.toMatch(/每段回忆，都值得被收藏/);
  });

  test('does not fabricate privacy metadata', () => {
    expect(source).not.toMatch(/小满与阿舟/);
    expect(source).not.toMatch(/我们的秘密花园/);
    expect(source).not.toMatch(/latest\?\.date \|\| '今天'/);
  });
});