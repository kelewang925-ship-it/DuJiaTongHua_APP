const fs = require('fs');
const path = require('path');

const source = fs.readFileSync(path.resolve(__dirname, '..', 'store', 'useFairyStore.js'), 'utf8');

describe('Realtime targeted refresh guards', () => {
  test('uses the Realtime event table instead of bootstrapping all modules for every change', () => {
    expect(source).toContain('const refreshRealtimeTable = async (table) =>');
    expect(source).toContain("table === 'diaries' || table === 'diary_attachments'");
    expect(source).toContain("table === 'photo_collections' || table === 'photos'");
    expect(source).toContain('scheduleRealtimeRefresh(event?.table)');
    expect(source).not.toContain("get().loadCoreData({ force: true });\n                    }, 120);");
  });

  test('confirms a diary save from the server result without waiting for a full bootstrap refresh', () => {
    expect(source).toContain("runRealWrite('saveDiary', () => createDiary(payload), { refresh: false })");
    expect(source).toContain("const diary = { ...result.data, type: '日记' }");
    expect(source).toContain('draftDiary: emptyDraft');
  });
});
