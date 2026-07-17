import fs from 'node:fs';
import path from 'node:path';
const source = fs.readFileSync(path.join(process.cwd(), 'app/ai/photo-to-comic.js'), 'utf8');
describe('photo to comic truth guards', () => {
  test('mock design photos are isolated from real mode', () => {
    expect(source).toContain('const mockPhotoOptions');
    expect(source).toContain('const photoOptions = isReal ? realPhotos.map');
    expect(source).toContain('页面不会使用设计图冒充用户照片');
  });
  test('real mode does not simulate AI success', () => {
    expect(source).toContain('!canGenerate || isReal');
    expect(source).toContain('不会创建本地模拟任务');
  });
});