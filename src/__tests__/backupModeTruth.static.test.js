import fs from 'fs';
import path from 'path';

test('backup page distinguishes mock, real and invalid modes', () => {
  const source = fs.readFileSync(path.join(process.cwd(), 'app/data/backup.js'), 'utf8');
  expect(source).toContain("const mode = getApiMode()");
  expect(source).toContain("const isMockMode = mode === 'mock'");
  expect(source).toContain("mode === 'real' && hasCapability('cloudBackup', mode)");
  expect(source).toContain('Mock 模式不连接备份服务');
  expect(source).toContain('当前页面不会上传、覆盖或恢复任何本机数据');
  expect(source).not.toContain("backupAvailable ? '服务已接入' : 'Real 未开放'");
});
