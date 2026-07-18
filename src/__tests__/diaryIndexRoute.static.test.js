const fs = require('fs');
const path = require('path');

const read = (relativePath) => fs.readFileSync(path.join(process.cwd(), relativePath), 'utf8');

describe('diary index route', () => {
  const home = read('app/(tabs)/index.js');
  const diaryIndex = read('app/diary/index.js');

  test('keeps the home diary statistic on an existing diary route', () => {
    expect(home).toContain("href: '/diary'");
    expect(fs.existsSync(path.join(process.cwd(), 'app/diary/index.js'))).toBe(true);
  });

  test('lists loaded diaries and opens a concrete diary detail route', () => {
    expect(diaryIndex).toContain("records.filter((item) => item.type === '日记')");
    expect(diaryIndex).toContain("pathname: '/diary/detail'");
    expect(diaryIndex).toContain("router.push('/diary/editor')");
  });

  test('uses the shared page and header shell', () => {
    expect(diaryIndex).toContain('<FairyPage');
    expect(diaryIndex).toContain('<FairyHeader showBack title="日记" />');
  });
});
