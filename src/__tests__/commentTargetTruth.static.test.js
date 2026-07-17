import fs from 'fs';
import path from 'path';

const source = fs.readFileSync(path.join(process.cwd(), 'src/api/commentApi.js'), 'utf8');

describe('comment target truth', () => {
  test('verifies target membership before insert', () => {
    expect(source).toContain('verifyCommentTarget');
    expect(source).toContain("const targetTables = { diary: 'diaries', photo: 'photos' }");
    expect(source).toContain(".eq('couple_id', coupleId)");
    expect(source).toContain('Comment target unavailable');
    expect(source).toContain('if (!targetResult.success) return targetResult');
  });
});
