const fs = require('fs');
const path = require('path');

const source = fs.readFileSync(path.resolve(__dirname, '../../app/(tabs)/index.js'), 'utf8');

describe('home record navigation', () => {
  test('passes a record id to diary and album detail routes', () => {
    expect(source).toContain("pathname: '/diary/detail', params: { id: record.id }");
    expect(source).toContain("pathname: '/photo/album', params: { id: record.id }");
    expect(source).not.toContain("router.push('/diary/detail');");
  });
});
