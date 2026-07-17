const fs = require('fs');
const path = require('path');

const source = fs.readFileSync(path.join(__dirname, '../api/timeCapsuleApi.js'), 'utf8');

test('time capsule results remain scoped to the active couple', () => {
  expect(source).toContain('sanitizeCapsule(value, coupleId = null)');
  expect(source).toContain('capsule.coupleId !== coupleId');
  expect(source).toContain('const coupleId = requireCouple(context)');
  expect(source).toContain("capsule.creatorId !== context.user.id");
  expect(source).toContain('deletedId !== id');
  expect(source).toContain('updatedId !== id');
});
