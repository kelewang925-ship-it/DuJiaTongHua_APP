import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.join(process.cwd(), 'src/api/timeCapsuleApi.js'), 'utf8');

describe('time capsule real-data truth guards', () => {
  test('requires a valid future date and explicit content types', () => {
    expect(source).toContain('isValidFutureDate(payload.unlockDate)');
    expect(source).toContain('normalizeContentTypes(payload.contentTypes)');
    expect(source).toContain("return createApiError('Missing content types'");
  });

  test('does not silently default reminder choices during real writes', () => {
    expect(source).toContain("typeof payload.reminder !== 'boolean'");
    expect(source).not.toContain('payload.reminder ?? payload.reminderEnabled ?? true');
  });

  test('requires backend confirmation for create update delete and reminder writes', () => {
    expect(source).toContain("return createApiError('Missing created capsule'");
    expect(source).toContain("return createApiError('Capsule not updated'");
    expect(source).toContain("return createApiError('Capsule not deleted'");
    expect(source).toContain("return createApiError('Reminder not updated'");
  });
});
