import { useEffect, useState } from 'react';
import { ActivityIndicator, StyleSheet, Text, View } from 'react-native';
import { usePathname, useRouter } from 'expo-router';
import colors from '../theme/colors';
import { getApiMode } from '../api/client';
import { getCurrentSession } from '../api/authApi';
import { enableDevUI } from '../dev-ui-lab/runtime/env';

export default function AuthGate({ children }) {
  const router = useRouter();
  const pathname = usePathname();
  const [checking, setChecking] = useState(getApiMode() === 'real');

  useEffect(() => {
    let mounted = true;

    async function checkSession() {
      if (getApiMode() !== 'real') {
        setChecking(false);
        return;
      }

      const result = await getCurrentSession();
      if (!mounted) return;

      const hasSession = result.success && !!result.data?.session;
      const isLoginPage = pathname === '/login';
      const isDevUIPage = pathname.startsWith('/dev-ui-lab');

      if (!hasSession && !isLoginPage && !(enableDevUI && isDevUIPage)) {
        router.replace('/login');
      }

      if (hasSession && isLoginPage) {
        router.replace('/(tabs)');
      }

      setChecking(false);
    }

    checkSession();

    return () => {
      mounted = false;
    };
  }, [pathname, router]);

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
