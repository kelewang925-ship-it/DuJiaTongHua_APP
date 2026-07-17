import fs from 'node:fs';
import path from 'node:path';
const source = fs.readFileSync(path.join(process.cwd(), 'app/(tabs)/workshop.js'), 'utf8');
describe('workshop truth guards', () => {
  test('missing source and style are disclosed', () => {
    expect(source).toContain("未提供来源与风格");
    expect(source).not.toContain("item.source || '童话工坊'");
    expect(source).not.toContain("item.styleName || '默认风格'");
  });
  test('missing ids are not navigable', () => {
    expect(source).toContain('disabled={!item.id}');
  });
  test('empty history is explicit', () => {
    expect(source).toContain('还没有真实创作记录');
  });
});