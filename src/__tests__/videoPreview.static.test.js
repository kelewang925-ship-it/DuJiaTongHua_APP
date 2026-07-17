import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.resolve(__dirname, '../../app/ai/video-preview.js'), 'utf8');

describe('video preview real-record guards', () => {
  test('requires the requested video id and renders an empty state when missing', () => {
    expect(source).toMatch(/useLocalSearchParams/);
    expect(source).toMatch(/item\.id === videoId && item\.type === '视频'/);
    expect(source).toMatch(/没有找到这份视频/);
    expect(source).toMatch(/!video \? showMissing\(\)/);
  });

  test('does not reintroduce fabricated preview metadata', () => {
    expect(source).not.toMatch(/我们的晚霞小电影/);
    expect(source).not.toMatch(/把晚霞藏进回忆里/);
    expect(source).not.toMatch(/晚风与心事/);
    expect(source).not.toMatch(/00:30/);
    expect(source).not.toMatch(/00:17/);
    expect(source).not.toMatch(/const clips = \[/);
  });
});
