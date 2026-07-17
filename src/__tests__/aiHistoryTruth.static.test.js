import fs from 'node:fs';
import path from 'node:path';
const source = fs.readFileSync(path.join(process.cwd(), 'app/ai/history.js'), 'utf8');
describe('AI history truth guards', () => {
  test('missing metadata remains disclosed', () => {
    expect(source).toContain("metadata || '来源与风格未提供'");
    expect(source).toContain("return '';");
    expect(source).not.toContain("item.source || '童话工坊'");
    expect(source).not.toContain("item.styleName || '默认风格'");
  });
  test('real records require backend ids', () => {
    expect(source).toContain("storedCreations.filter((item) => item?.id)");
  });
});