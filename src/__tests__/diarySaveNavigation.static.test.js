const fs = require('fs');
const path = require('path');

const source = fs.readFileSync(path.resolve(__dirname, '../../app/diary/editor.js'), 'utf8');

describe('diary save navigation', () => {
  test('opens the saved diary detail using the server result id', () => {
    expect(source).toContain('const diaryId = result.data?.id');
    expect(source).toContain("pathname: '/diary/detail', params: { id: diaryId }");
    expect(source).not.toContain("router.replace('/diary/detail');");
  });
});
