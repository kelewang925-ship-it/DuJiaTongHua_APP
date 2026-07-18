import { useEffect, useRef, useState } from 'react';
import { ActivityIndicator, StyleSheet, Text, View } from 'react-native';
import { router, usePathname } from 'expo-router';
import colors from '../theme/colors';
import { getApiMode } from '../api/client';
import { getCurrentSession, subscribeToAuthState } from '../api/authApi';
import useFairyStore from '../store/useFairyStore';
import { enableDevUI } from '../dev-ui-lab/runtime/env';

const isCoupleOnboardingPath = (pathname) => ['/', '/account/invite', '/account/bind-confirm'].includes(pathname);
const hasActiveCouple = (couple) => Boolean(couple?.id && couple.status === 'active');

export default function AuthGate({ children }) {
  const pathname = usePathname();
  const pathnameRef = useRef(pathname);
  const [checking, setChecking] = useState(getApiMode() === 'real');
  const bootstrapApp = useFairyStore((state) => state.bootstrapApp);
  const resetForSession = useFairyStore((state) => state.resetForSession);

  // Route changes (especially bottom-tab switches) must not restart the
  // session bootstrap. Keep the latest path only for redirects triggered by a
  // genuine auth event.
  useEffect(() => {
    pathnameRef.current = pathname;
  }, [pathname]);

  useEffect(() => {
    let mounted = true;
    let sessionCheckId = 0;

    const isLatestCheck = (checkId) => mounted && checkId === sessionCheckId;

    const finishLatestCheck = (checkId) => {
      if (isLatestCheck(checkId)) setChecking(false);
    };

    async function checkSession() {
      const checkId = ++sessionCheckId;
      if (getApiMode() !== 'real') {
        finishLatestCheck(checkId);
        return;
      }

      setChecking(true);
      const result = await getCurrentSession();
      if (!isLatestCheck(checkId)) return;

      const hasSession = result.success && !!result.data?.session;
      const currentPath = pathnameRef.current;
      const isLoginPage = currentPath === '/login';
      const isDevUIPage = currentPath.startsWith('/dev-ui-lab');

      if (!hasSession && !isLoginPage && !(enableDevUI && isDevUIPage)) {
        router.replace('/login');
        finishLatestCheck(checkId);
        return;
      }

      // getCurrentSession() already verified this token with Supabase. Pass
      // that result through so bootstrapApp does not make a second auth.getUser
      // request before the first route can render.
      const bootstrapResult = hasSession ? await bootstrapApp({ sessionResult: result }) : null;
      if (!isLatestCheck(checkId)) return;

      // A local token is not enough to leave the login page. bootstrapApp
      // verifies that token against Supabase and loads the session-scoped
      // Store. Without this guard, a stale token can bounce /login to / and
      // immediately be redirected back to /login.
      const sessionReady = Boolean(hasSession && bootstrapResult?.success);
      if (sessionReady && isLoginPage) {
        router.replace('/');
      }
      if (sessionReady && !isLoginPage && !isCoupleOnboardingPath(currentPath) && !hasActiveCouple(bootstrapResult?.data?.couple)) {
        router.replace('/account/invite');
      }
      if (!sessionReady && hasSession && !isLoginPage && bootstrapResult?.error?.category === 'session') {
        router.replace('/login');
      }

      finishLatestCheck(checkId);
    }

    checkSession();
    const unsubscribe = subscribeToAuthState(async ({ event, session }) => {
      if (!mounted) return;
      // The initial session is already handled by checkSession above. Treating
      // it as a new event briefly resets the loading state and makes the login
      // page flicker with the bootstrap screen.
      if (event === 'INITIAL_SESSION') return;
      const checkId = ++sessionCheckId;
      setChecking(true);
      if (session) {
        const bootstrapResult = await bootstrapApp();
        if (!isLatestCheck(checkId)) return;
        if (bootstrapResult?.success && !isCoupleOnboardingPath(pathnameRef.current) && !hasActiveCouple(bootstrapResult.data?.couple)) {
          router.replace('/account/invite');
        }
      } else {
        await resetForSession(null);
        if (!isLatestCheck(checkId)) return;
        if (pathnameRef.current !== '/login') router.replace('/login');
      }
      finishLatestCheck(checkId);
    });

    return () => {
      mounted = false;
      unsubscribe();
    };
  }, [bootstrapApp, resetForSession]);

  if (checking) {
    return (
      <View style={styles.loadingPage}>
        <ActivityIndicator color={colors.accent} />
        <Text style={styles.loadingText}>正在打开你们的童话...</Text>
      </View>
    );
  }

  return children;
}

const styles = StyleSheet.create({
  loadingPage: {
    flex: 1,
    backgroundColor: colors.background,
    alignItems: 'center',
    justifyContent: 'center',
    gap: 12,
  },
  loadingText: {
    color: colors.textSoft,
    fontSize: 13,
    fontWeight: '700',
  },
});
