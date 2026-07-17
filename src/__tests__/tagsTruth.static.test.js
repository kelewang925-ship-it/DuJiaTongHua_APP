import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.join(process.cwd(), 'src/api/tagApi.js'), 'utf8');

describe('tag real-data truth guards', () => {
  test('real writes require an explicit valid category', () => {
    expect(source).toContain("const validCategories = new Set(['心情', '地点', '纪念', 'AI'])");
    expect(source).toContain("return createApiError('Invalid tag category'");
    expect(source).not.toContain("category: payload.category || '心情'");
  });

  test('real writes do not invent an icon', () => {
    expect(source).toContain('if (payload.icon !== undefined');
    expect(source).not.toContain("icon: payload.icon || 'pricetag-outline'");
  });

  test('update and delete require a returned backend row', () => {
    expect(source).toContain("return createApiError('Tag not updated'");
    expect(source).toContain("return createApiError('Tag not deleted'");
    expect(source).toContain("select('id').maybeSingle()");
  });
});
