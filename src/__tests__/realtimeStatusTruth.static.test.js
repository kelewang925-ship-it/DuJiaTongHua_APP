import fs from 'node:fs';
import path from 'node:path';

describe('realtime status truth', () => {
  const source = fs.readFileSync(path.join(process.cwd(), 'src/api/realtimeApi.js'), 'utf8');

  test('normalizes subscribed and failed channel states', () => {
    expect(source).toContain("new Set(['CHANNEL_ERROR', 'TIMED_OUT', 'CLOSED'])");
    expect(source).toContain('function createStatusPayload');
    expect(source).toContain("connected: status === 'SUBSCRIBED'");
    expect(source).toContain('failed,');
    expect(source).toContain('subscribeWithStatus');
  });
});