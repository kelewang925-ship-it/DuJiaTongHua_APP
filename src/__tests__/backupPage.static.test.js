import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.resolve(process.cwd(), 'app/data/backup.js'), 'utf8');

describe('backup page real-data guards', () => {
  test('does not ship fixed backup history', () => {
    expect(source).not.toContain('backup-today');
    expect(source).not.toContain('今天 20:18');
    expect(source).not.toContain('昨天 22:06');
  });

  test('does not estimate or fabricate cloud storage usage', () => {
    expect(source).not.toContain('usedStorage');
    expect(source).not.toContain('storagePercent');
    expect(source).not.toContain('GB / 5 GB');
  });

  test('does not simulate backup completion with timers', () => {
    expect(source).not.toContain('setTimeout');
    expect(source).not.toContain('所有故事都已安心收好');
    expect(source).not.toContain('已模拟恢复最近一次备份');
  });

  test('keeps both Mock and Real backup actions disabled', () => {
    const disabledButtons = source.match(/<FairyButton[\s\S]*?\sdisabled(?:\s|>)/g) || [];
    expect(disabledButtons.length).toBeGreaterThanOrEqual(2);
    expect(source).toContain("title={isMockMode ? 'Mock 仅展示' : '暂未开放'}");
    expect(source).toContain('Mock 模式仅展示页面，不上传任何数据');
    expect(source).toContain('不会上传、覆盖或恢复任何本机数据');
  });
});
