import fs from 'node:fs';
import path from 'node:path';

describe('API client mode fail closed static guard', () => {
  const source = fs.readFileSync(path.join(process.cwd(), 'src/api/client.js'), 'utf8');

  test('unknown modes become disabled instead of mock', () => {
    expect(source).toContain("configuredMode === 'real' || configuredMode === 'mock' ? configuredMode : 'disabled'");
    expect(source).toContain("return API_MODE === 'mock'");
    expect(source).toContain("error.code = 'INVALID_API_MODE'");
  });

  test('mock requests cannot run outside mock mode', () => {
    expect(source).toContain('if (!isMockMode())');
    expect(source).toContain('Mock request is unavailable outside mock mode');
  });

  test('authenticated context verifies the server user', () => {
    expect(source).toContain('user.id !== sessionUser.id');
  });
});
