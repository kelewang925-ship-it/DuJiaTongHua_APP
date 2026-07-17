import fs from 'node:fs';
import path from 'node:path';
const source = fs.readFileSync(path.join(process.cwd(), 'app/ai/comic-result.js'), 'utf8');
describe('comic result truth guards', () => {
  test('requires an explicit work id', () => {
    expect(source).toContain("comicId ? creations.find");
    expect(source).not.toContain("return creations.find((item) => item.type === '漫画')");
  });
  test('does not simulate favorite or save success', () => {
    expect(source).toContain('收藏接口尚未接入，不会修改本地收藏状态');
    expect(source).toContain('保存接口尚未接入，不会模拟保存成功');
    expect(source).not.toContain('作品已保存到童话工坊');
  });
});