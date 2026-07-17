const fs = require('fs');
const path = require('path');

const source = fs.readFileSync(path.join(__dirname, '../api/tagApi.js'), 'utf8');

test('custom tags validate couple ownership and bounded fields', () => {
  expect(source).toContain('normalizeTag(value, coupleId)');
  expect(source).toContain('tag.coupleId !== coupleId');
  expect(source).toContain('MAX_TAG_NAME_LENGTH');
  expect(source).toContain('MAX_TAG_ICON_LENGTH');
  expect(source).toContain("tag.createdBy !== context.user.id");
  expect(source).toContain("select('id,couple_id')");
});
