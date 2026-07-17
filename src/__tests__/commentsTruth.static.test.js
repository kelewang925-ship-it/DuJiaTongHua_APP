import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.join(process.cwd(), 'src/api/commentApi.js'), 'utf8');

describe('comment real-data truth guards', () => {
  test('accepts only supported backend target types', () => {
    expect(source).toContain("const validTargetTypes = new Set(['diary', 'photo'])");
    expect(source).toContain("return createApiError('Invalid comment target'");
  });

  test('returns the backend author profile for newly created comments', () => {
    expect(source).toContain("select('*,profiles:author_id(nickname,avatar_text,avatar_url)').single()");
    expect(source).toContain("return createApiError('Missing created comment'");
  });

  test('delete success requires a returned backend row', () => {
    expect(source).toContain("select('id').maybeSingle()");
    expect(source).toContain("return createApiError('Comment not deleted'");
  });
});
