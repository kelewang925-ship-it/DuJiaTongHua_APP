import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(__dirname, '../..');
const source = fs.readFileSync(path.join(root, 'app/data/storage.js'), 'utf8');

describe('storage page real-data guards', () => {
  test('does not invent photo counts or minimum GB usage', () => {
    expect(source).not.toMatch(/item\.photoCount \|\| 3/);
    expect(source).not.toMatch(/Math\.max\(1\.2/);
    expect(source).not.toMatch(/Math\.max\(0\.8/);
    expect(source).not.toMatch(/totalStorage\s*=\s*10/);
  });

  test('derives visible counts from loaded store entities', () => {
    expect(source).toMatch(/records\.filter\(\(item\) => item\.type === '照片'\)/);
    expect(source).toMatch(/Number\.isFinite\(count\)/);
    expect(source).toMatch(/creations\.length/);
  });

  test('does not simulate cache deletion success', () => {
    expect(source).not.toMatch(/setCacheSize\(0\)/);
    expect(source).not.toMatch(/临时纸屑已经扫进小纸篓/);
    expect(source).toMatch(/缓存清理暂未开放/);
    expect(source).toMatch(/不会模拟清理成功/);
  });
});
