import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.join(process.cwd(), 'src/api/commentApi.js'), 'utf8');

describe('comment real-data truth guards', () => {
  test('accepts only supported backend target types', () => {
    expect(source).toContain("const validTargetTypes = new Set(['diary', 'photo'])");
    expect(source).toContain("return createApiError('Invalid comment target'");
  });

  test('verifies the target and confirms the created comment ownership', () => {
    expect(source).toContain('verifyCommentTarget');
    expect(source).toContain("select('*,profiles:author_id(nickname,avatar_text,avatar_url)').maybeSingle()");
    expect(source).toContain("return createApiError('Comment creation mismatch'");
    expect(source).toContain('comment.authorId !== context.user.id');
  });

  test('delete success requires a returned backend row owned by the caller', () => {
    expect(source).toMatch(/\.select\(['"]id,couple_id,author_id['"]\)\.maybeSingle\(\)/);
    expect(source).toContain("return createApiError('Comment not deleted'");
    expect(source).toContain('data.author_id !== context.user.id');
  });
});
