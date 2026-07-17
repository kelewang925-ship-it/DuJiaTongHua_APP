import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.join(process.cwd(), 'app/ai/character-profile.js'), 'utf8');

describe('AI character profile real-mode guards', () => {
  test('keeps demo identity inside mock-only profile data', () => {
    expect(source).toContain("const mockProfile = {");
    expect(source).toContain("const emptyProfile = {");
    expect(source).toContain("const initialProfile = isMockMode ? mockProfile : emptyProfile;");
  });

  test('real-mode empty profile does not include fabricated names or descriptions', () => {
    const emptyBlock = source.match(/const emptyProfile = \{([\s\S]*?)\n\};/)?.[1] || '';
    expect(emptyBlock).not.toContain('林小满');
    expect(emptyBlock).not.toContain('陆星河');
    expect(emptyBlock).not.toContain('喜欢散步');
    expect(emptyBlock).toContain("heroName: ''");
    expect(emptyBlock).toContain("partnerName: ''");
  });

  test('real mode explicitly avoids simulated persistence', () => {
    expect(source).toContain('不会预填演示姓名');
    expect(source).toContain('不会写入本地成功状态');
    expect(source).toContain('真实人设保存尚未开放');
  });
});
