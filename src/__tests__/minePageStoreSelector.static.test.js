const fs = require('fs');
const path = require('path');

const read = (file) => fs.readFileSync(path.resolve(__dirname, '..', '..', file), 'utf8');

describe('mine page store subscriptions', () => {
  test('does not create a new stats object from a Zustand selector', () => {
    const source = read('app/(tabs)/mine.js');

    expect(source).not.toContain('useFairyStore((state) => state.getStats())');
    expect(source).toContain('const records = useFairyStore((state) => state.records)');
    expect(source).toContain('const stats = useMemo(() => ({');
  });
});
