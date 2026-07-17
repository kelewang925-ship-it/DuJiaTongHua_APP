import fs from 'node:fs';
import path from 'node:path';
const source = fs.readFileSync(path.join(process.cwd(), 'app/(tabs)/mine.js'), 'utf8');
describe('mine truth guards', () => {
  test('real profile uses backend profile data', () => {
    expect(source).toContain('profile || coupleState?.user');
    expect(source).toContain('昵称未提供');
  });
  test('membership is not claimed without checking', () => {
    expect(source).toContain('查看会员状态');
    expect(source).not.toContain('童话会员</FairyTag>');
  });
  test('binding requires persisted ids', () => {
    expect(source).toContain("relation?.id && relation?.status === 'active' && partnerProfile?.id");
  });
});