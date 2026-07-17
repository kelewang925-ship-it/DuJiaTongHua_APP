import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.join(process.cwd(), 'app/ai/video-config.js'), 'utf8');

describe('AI video config Real Mode truth guards', () => {
  test('isolates mock defaults and disables unavailable Real controls', () => {
    expect(source).toContain("const isMockMode = mode === 'mock'");
    expect(source).toContain("useState(isMockMode ? mockDraft.title : '')");
    expect(source).toContain('disabled={!canGenerate}');
    expect(source).toContain('Real 模式不会创建任务、作品或成功状态');
  });

  test('does not promise real generation or automatic history persistence', () => {
    expect(source).not.toContain('预计 1–3 分钟完成 · 作品会自动保存到创作历史');
    expect(source).toContain('Mock 视频流程演示');
  });
});
