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

  test('requires backend confirmation and matching ownership for all writes', () => {
    expect(source).toContain("return createApiError('Capsule creation mismatch'");
    expect(source).toContain('capsule.creatorId !== context.user.id');
    expect(source).toContain("return createApiError('Capsule not updated'");
    expect(source).toContain('capsule.id !== id');
    expect(source).toContain("return createApiError('Capsule not deleted'");
    expect(source).toContain('deletedId !== id');
    expect(source).toContain("return createApiError('Reminder not updated'");
    expect(source).toContain('updatedId !== id');
  });
});
