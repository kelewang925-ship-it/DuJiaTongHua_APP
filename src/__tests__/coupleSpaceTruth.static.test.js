import fs from 'node:fs';
import path from 'node:path';
const source = fs.readFileSync(path.join(process.cwd(), 'app/(tabs)/couple.js'), 'utf8');
describe('couple space truth guards', () => {
  test('real binding requires persisted relation and partner ids', () => {
    expect(source).toContain("relation?.id && relation.status === 'active' && coupleState?.partner?.id");
  });
  test('missing names and dates are disclosed', () => {
    expect(source).toContain('昵称未提供');
    expect(source).toContain('恋爱起始日未提供或无效');
  });
  test('missing anniversaries are not invented', () => {
    expect(source).toContain('暂无纪念日数据');
    expect(source).not.toContain('新的重要章节');
  });
});