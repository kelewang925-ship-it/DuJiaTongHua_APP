import fs from 'fs';
import path from 'path';

const source = fs.readFileSync(path.join(process.cwd(), 'src/api/anniversaryApi.js'), 'utf8');

describe('anniversary mutation truth', () => {
  test('validates dates and confirms affected server rows', () => {
    expect(source).toContain('isValidDate');
    expect(source).toContain("select('*').maybeSingle()");
    expect(source).toContain("select('id').maybeSingle()");
    expect(source).toContain('Anniversary not created');
    expect(source).toContain('Anniversary not updated');
    expect(source).toContain('Anniversary not deleted');
  });
});
