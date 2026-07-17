import fs from 'node:fs';
import path from 'node:path';

describe('authentication result identity', () => {
  const source = fs.readFileSync(path.join(process.cwd(), 'src/api/authApi.js'), 'utf8');

  test('checks session, user and submitted email consistency', () => {
    expect(source).toContain('function validateAuthIdentity');
    expect(source).toContain("return createApiError('Auth user mismatch'");
    expect(source).toContain("return createApiError('Auth email mismatch'");
    expect(source).toContain('{ requireSession: true }');
    expect(source).toContain('function normalizeSignupProfile');
  });
});