import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.join(process.cwd(), 'src/store/useFairyStore.js'), 'utf8').replace(/\r\n/g, '\n');

describe('startup progressive data loading', () => {
  test('limits the route-critical relationship request and defers noncritical modules', () => {
    expect(source).toContain("getCoupleInfo(),\n            5000,");
    expect(source).toContain("loading: { bootstrap: false, modules: Boolean(coupleState?.couple) }");
    expect(source).toContain("void get().loadCoreData({ force: true, background: true, coupleResult });");
    expect(source).toContain("return createApiResponse(coupleState, { modulesLoading: Boolean(coupleState?.couple) });");
  });

  test('keeps manual refresh blocking while background bootstrap work uses a separate state key', () => {
    expect(source).toContain("loadCoreData: async ({ force = false, background = false, coupleResult: knownCoupleResult = null } = {})");
    expect(source).toContain("const requestKey = background ? 'modules' : 'bootstrap';");
    expect(source).toContain("setRequestState(requestKey, true, null);");
    expect(source).toContain("setRequestState(requestKey, false, failed.error);");
  });
});
