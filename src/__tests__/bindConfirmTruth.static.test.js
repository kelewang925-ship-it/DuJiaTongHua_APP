import fs from 'node:fs';
import path from 'node:path';
const source = fs.readFileSync(path.join(process.cwd(), 'app/account/bind-confirm.js'), 'utf8');
describe('bind confirm truth guards', () => {
  test('real mode does not trust inviter profile params or design avatar', () => {
    expect(source).toContain("suppliedName || '邀请人资料未提供'");
    expect(source).toContain('绑定前无法验证邀请人昵称或头像');
    expect(source).not.toContain("assets/images/avatar/man.png");
  });
  test('binding requires a persisted relationship id', () => {
    expect(source).toContain("!result.data?.bound || !result.data?.couple?.id");
    expect(source).toContain('后端没有确认情侣关系已创建');
  });
});