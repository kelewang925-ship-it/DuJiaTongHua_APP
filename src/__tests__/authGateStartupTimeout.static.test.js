const fs = require('fs');
const path = require('path');

const authGate = fs.readFileSync(path.resolve(__dirname, '..', 'components', 'AuthGate.js'), 'utf8');
const authApi = fs.readFileSync(path.resolve(__dirname, '..', 'api', 'authApi.js'), 'utf8');

describe('AuthGate startup timeout', () => {
  test('bounds the whole session check before it can block routing', () => {
    expect(authGate).toContain('withRequestTimeout(\n        getCurrentSession(),\n        5000,');
    expect(authGate).toContain(".catch((error) => createApiError(error, '获取登录状态失败，请重新登录'))");
  });

  test('keeps the remote identity verification inside the startup budget', () => {
    expect(authApi).toContain('supabase.auth.getUser(),\n      4000,');
  });
});
