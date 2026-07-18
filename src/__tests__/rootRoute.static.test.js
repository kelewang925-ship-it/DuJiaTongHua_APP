import fs from 'node:fs';
import path from 'node:path';

const read = (relativePath) => fs.readFileSync(path.join(process.cwd(), relativePath), 'utf8');

describe('root route relationship decision', () => {
  const rootRoute = read('app/index.js');
  const login = read('app/login.js');
  const authGate = read('src/components/AuthGate.js');

  test('uses the loaded Real relationship to choose the home or invite route', () => {
    expect(rootRoute).toContain("getApiMode() === 'real'");
    expect(rootRoute).toContain('const relationship = coupleState?.couple');
    expect(rootRoute).toContain("relationship.status === 'active'");
    expect(rootRoute).toContain("? '/(tabs)'");
    expect(rootRoute).toContain(": '/account/invite'");
    expect(rootRoute).toContain('router.replace(destination)');
    expect(rootRoute).not.toContain('/diary/detail');
  });

  test('does not treat bootstrap or realtime null state as an unbound relationship', () => {
    expect(rootRoute).toContain('loading || (coupleState === null && !loadError)');
    expect(rootRoute).toContain('? null');
    expect(rootRoute).toContain('if (destination) router.replace(destination)');
    expect(rootRoute).toContain('FairyPage');
    expect(rootRoute).toContain('FairyRequestState');
    expect(rootRoute).toContain('onRetry={refreshCoreData}');
  });

  test('routes successful sign-in and session restoration through the root decision', () => {
    expect(login).toContain("router.replace('/')");
    expect(authGate).toContain("router.replace('/')");
    expect(authGate).toContain('setChecking(true)');
    expect(authGate).toContain('let sessionCheckId = 0');
    expect(authGate).toContain('checkId === sessionCheckId');
    expect(authGate).toContain('finishLatestCheck(checkId)');
    expect(authGate).toContain("if (event === 'INITIAL_SESSION') return");
    expect(authGate).toContain('const sessionReady = Boolean(hasSession && bootstrapResult?.success)');
    expect(authGate).toContain('if (sessionReady && isLoginPage)');
    expect(authGate).toContain("import { router, usePathname } from 'expo-router'");
    expect(authGate).not.toContain('useRouter');
    expect(authGate).toContain('const pathnameRef = useRef(pathname)');
    expect(authGate).toContain('pathnameRef.current = pathname');
    expect(authGate).toContain('const currentPath = pathnameRef.current');
    expect(authGate).toContain('}, [bootstrapApp, resetForSession]);');
    expect(authGate).not.toContain('}, [bootstrapApp, pathname, resetForSession]);');
  });
});
