const fs = require('fs');
const path = require('path');

const read = (file) => fs.readFileSync(path.resolve(process.cwd(), file), 'utf8');

describe('Real module loading guards', () => {
  test.each([
    ['app/(tabs)/couple.js', 'couple'],
    ['app/(tabs)/mine.js', 'mine'],
    ['app/notifications/index.js', 'notifications'],
    ['app/search.js', 'search'],
    ['app/tags/index.js', 'tags'],
    ['app/time-capsule/settings.js', 'capsules'],
  ])('%s keeps content behind the deferred modules request', (file) => {
    const source = read(file);
    expect(source).toContain('state.loading?.modules');
    expect(source).toContain('state.errors?.modules');
  });

  test('the diary page remains the reference implementation', () => {
    const source = read('app/diary/index.js');
    expect(source).toContain('state.loading?.modules || state.loading?.bootstrap');
    expect(source).toContain('state.errors?.modules || state.errors?.bootstrap');
  });
});
