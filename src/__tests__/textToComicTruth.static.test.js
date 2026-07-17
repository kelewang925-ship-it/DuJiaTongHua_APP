import fs from 'node:fs';
import path from 'node:path';
const source = fs.readFileSync(path.join(process.cwd(), 'app/ai/text-to-comic.js'), 'utf8');
describe('text to comic truth guards', () => {
  test('does not inject a fallback story or fake diary metadata', () => {
    expect(source).not.toContain('fallbackStory');
    expect(source).not.toContain('晚霞散步');
    expect(source).not.toContain('一段温柔的日常回忆');
    expect(source).toContain('没有真实日记内容时，不会自动填充演示故事');
  });
  test('real mode cannot create local AI tasks', () => {
    expect(source).toContain('!canGenerate || isReal');
    expect(source).toContain('不会创建本地模拟任务');
  });
});