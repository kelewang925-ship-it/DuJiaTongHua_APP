import fs from 'node:fs';
import path from 'node:path';

const authSource = fs.readFileSync(path.join(process.cwd(), 'src/api/authApi.js'), 'utf8');
const loginSource = fs.readFileSync(path.join(process.cwd(), 'app/login.js'), 'utf8');

describe('authentication contracts', () => {
  test('registration exposes email confirmation as data and metadata', () => {
    expect(authSource).toMatch(/requiresEmailConfirmation/);
    expect(authSource).toMatch(/createApiResponse\(normalized, \{ requiresEmailConfirmation:/);
  });

  test('login, registration and reset password return displayable errors', () => {
    expect(authSource).toContain('邮箱、密码或邮箱验证状态不正确');
    expect(authSource).toContain('注册失败，请检查邮箱或密码');
    expect(authSource).toContain('发送重置邮件失败');
  });

  test('login page blocks duplicate submissions and handles confirmation state', () => {
    expect(loginSource).toMatch(/submitting/);
    expect(loginSource).toMatch(/disabled=\{submitting\}/);
    expect(loginSource).toContain('注册成功，请先到邮箱完成验证');
  });

  test('auth state subscription returns an unsubscribe cleanup', () => {
    expect(authSource).toMatch(/return \(\) => data\.subscription\.unsubscribe\(\)/);
  });
});
