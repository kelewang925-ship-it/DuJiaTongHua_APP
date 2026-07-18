import fs from 'node:fs';
import path from 'node:path';

describe('auth session verification static guard', () => {
  const source = fs.readFileSync(path.join(process.cwd(), 'src/api/authApi.js'), 'utf8');

  test('cached sessions are verified with getUser', () => {
    expect(source).toContain('supabase.auth.getUser()');
    expect(source).toContain('withRequestTimeout(');
    expect(source).toContain('登录状态校验超时，请检查网络后重试');
    expect(source).toContain("verifiedUser.id !== session.user?.id");
    expect(source).toContain("createApiError('Session user mismatch'");
  });

  test('missing session remains an explicit signed-out result', () => {
    expect(source).toContain("if (!session) return createApiResponse({ session: null, user: null, requiresEmailConfirmation: false })");
  });
});
