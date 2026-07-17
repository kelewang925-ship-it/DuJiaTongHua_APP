import fs from 'node:fs';
import path from 'node:path';

const pagePath = path.join(process.cwd(), 'app/ai/comic-config.js');
const source = fs.readFileSync(pagePath, 'utf8');

describe('comic config real-mode guards', () => {
  test('demo story stays inside mock draft', () => {
    expect(source).toContain('const mockDraft = {');
    expect(source).toContain("const isMockMode = mode === 'mock';");
    expect(source).toContain("useState(isMockMode ? mockDraft.title : '')");
    expect(source).toContain("useState(isMockMode ? mockDraft.prompt : '')");
  });

  test('real mode starts without a selected source', () => {
    expect(source).toContain('useState(isMockMode ? mockDraft.source : null)');
    expect(source).toContain("if (!source)");
  });

  test('real mode does not claim generation has started', () => {
    expect(source).toContain('Real 模式不会创建本地模拟作品');
    expect(source).not.toContain('离开页面后仍会继续');
    expect(source).not.toContain('预计需要 1–2 分钟');
  });

  test('mock task is explicitly labelled', () => {
    expect(source).toContain('Mock 分镜演示');
    expect(source).toContain('仅创建本地 Mock 流程，不代表真实 AI 已开始处理');
  });
});
