import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.resolve(__dirname, '../../app/settings.js'), 'utf8');

describe('settings real session guards', () => {
  test('uses the auth API instead of only navigating to login', () => {
    expect(source).toMatch(/import \{ signOut \} from ['"]\.\.\/src\/api\/authApi['"]/);
    expect(source).toMatch(/const result = await signOut\(\)/);
    expect(source).toMatch(/if \(!result\.success\)/);
  });

  test('clears session-scoped store data only after successful sign-out', () => {
    expect(source).toMatch(/resetForSession/);
    expect(source).toMatch(/await resetForSession\(null\)/);
    expect(source.indexOf('await resetForSession(null)')).toBeGreaterThan(source.indexOf('if (!result.success)'));
    expect(source.indexOf("router.replace('/login')")).toBeGreaterThan(source.indexOf('await resetForSession(null)'));
  });

  test('does not describe local preview switches as persisted server settings', () => {
    expect(source).toMatch(/仅当前设备预览/);
    expect(source).toMatch(/不会改变服务端访问权限/);
    expect(source).not.toMatch(/已开启双人私密空间/);
    expect(source).not.toMatch(/已关闭私密空间/);
  });
});
