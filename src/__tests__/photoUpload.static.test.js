import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.join(process.cwd(), 'app/photo/upload.js'), 'utf8');

describe('photo upload real-data defaults', () => {
  test('keeps the mock tag default isolated', () => {
    expect(source).toContain("const mockDefaultTags = ['约会'];");
    expect(source).toContain('useState(() => isReal ? [] : mockDefaultTags)');
  });

  test('does not invent a fallback tag during persistence', () => {
    expect(source).toContain('tags: selectedTags');
    expect(source).not.toContain("selectedTags.length ? selectedTags : ['照片']");
  });

  test('labels tags as optional', () => {
    expect(source).toContain('标签（选填）');
  });
});
