const fs = require('fs');
const path = require('path');

const store = fs.readFileSync(path.resolve(process.cwd(), 'src/store/useFairyStore.js'), 'utf8');

describe('Real module failure cache safety', () => {
  test('module request failures set an error without resetting loaded business arrays', () => {
    const failureStart = store.indexOf('const failed = [diaryResult');
    const failureEnd = store.indexOf('const diaries =', failureStart);
    expect(failureStart).toBeGreaterThanOrEqual(0);
    expect(failureEnd).toBeGreaterThan(failureStart);
    const failureBranch = store.slice(failureStart, failureEnd);
    expect(failureBranch).toContain('setRequestState(requestKey, false, failed.error);');
    expect(failureBranch).not.toContain('realInitialState');
    expect(failureBranch).not.toContain('records: []');
    expect(failureBranch).not.toContain('timeCapsules: []');
  });
});
