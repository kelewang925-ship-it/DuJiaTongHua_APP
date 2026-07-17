import fs from 'fs';
import path from 'path';

test('next anniversary is derived from the next occurrence', () => {
  const source = fs.readFileSync(path.join(process.cwd(), 'src/api/anniversaryApi.js'), 'utf8');
  expect(source).toContain('function getNextOccurrence');
  expect(source).toContain('function selectNextAnniversary');
  expect(source).toContain("repeatType === 'none'");
  expect(source).toContain('nextOccurrence');
  expect(source).toContain('daysUntil');
  expect(source).not.toContain('result.data[0] || null');
});
