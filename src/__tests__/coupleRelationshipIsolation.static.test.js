import fs from 'fs';
import path from 'path';

const source = fs.readFileSync(path.join(process.cwd(), 'src/api/coupleApi.js'), 'utf8');

describe('couple relationship isolation', () => {
  test('blocks inactive or mismatched relationships', () => {
    expect(source).toContain('isActiveCouple');
    expect(source).toContain('isCoupleMember');
    expect(source).toContain('relationshipIsolated: true');
    expect(source).toContain('Binding membership mismatch');
    expect(source).toContain("couple.status !== 'active'");
  });
});
