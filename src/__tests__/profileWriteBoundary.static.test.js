import fs from 'fs';
import path from 'path';

const source = fs.readFileSync(path.join(process.cwd(), 'src/api/authApi.js'), 'utf8');

describe('profile write boundaries', () => {
  test('validates profile fields and confirms current user result', () => {
    expect(source).toContain('MAX_NICKNAME_LENGTH');
    expect(source).toContain('MAX_AVATAR_TEXT_LENGTH');
    expect(source).toContain('MAX_AVATAR_URL_LENGTH');
    expect(source).toContain('normalizeAvatarUrl');
    expect(source).toContain('Profile write mismatch');
    expect(source).toContain('data.id !== userId');
  });
});
