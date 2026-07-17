const fs = require('fs');
const path = require('path');

const source = fs.readFileSync(path.join(__dirname, '../api/commentApi.js'), 'utf8');

test('comments remain scoped to the active couple and target', () => {
  expect(source).toContain('normalizeComment(value, { coupleId, targetType, targetId } = {})');
  expect(source).toContain('comment.coupleId !== coupleId');
  expect(source).toContain('comment.targetType !== targetType');
  expect(source).toContain('comment.targetId !== targetId');
  expect(source).toContain('MAX_COMMENT_LENGTH');
  expect(source).toContain('comment.authorId !== context.user.id');
});
