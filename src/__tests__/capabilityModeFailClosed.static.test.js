import fs from 'node:fs';
import path from 'node:path';

describe('capability mode fail closed static guard', () => {
  const source = fs.readFileSync(path.join(process.cwd(), 'src/config/capabilities.js'), 'utf8');

  test('unknown modes do not inherit mock capabilities', () => {
    expect(source).toContain("return value === 'real' || value === 'mock' ? value : 'disabled'");
    expect(source).toContain('const disabledCapabilities = Object.freeze');
    expect(source).toContain('return disabledCapabilities');
  });

  test('capability maps are immutable', () => {
    expect(source).toContain('const realCapabilities = Object.freeze');
    expect(source).toContain('const mockCapabilities = Object.freeze');
  });
});
