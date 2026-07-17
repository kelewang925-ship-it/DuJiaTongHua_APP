import fs from 'node:fs';
import path from 'node:path';
const source = fs.readFileSync(path.join(process.cwd(), 'app/couple/story-detail.js'), 'utf8');
describe('story detail truth guards', () => {
  test('missing ids do not select the first timeline item', () => {
    expect(source).toContain("storyId ? timeline.find((item) => item.id === storyId) : null");
    expect(source).not.toContain('return timeline[0]');
  });
  test('comments require a real record target', () => {
    expect(source).toContain('disabled={!commentTarget}');
    expect(source).toContain("params: commentTarget");
  });
});