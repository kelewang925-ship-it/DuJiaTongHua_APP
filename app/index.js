import { useEffect } from 'react';
import { router } from 'expo-router';
import { ActivityIndicator, StyleSheet, Text, View } from 'react-native';
import { getApiMode } from '../src/api/client';
import FairyPage from '../src/components/FairyPage';
import FairyRequestState from '../src/components/FairyRequestState';
import useFairyStore from '../src/store/useFairyStore';
import colors from '../src/theme/colors';

export default function Index() {
  const isReal = getApiMode() === 'real';
  const coupleState = useFairyStore((state) => state.couple);
  const loading = useFairyStore((state) => Boolean(state.loading?.bootstrap));
  const loadError = useFairyStore((state) => state.errors?.bootstrap || null);
  const refreshCoreData = useFairyStore((state) => state.refreshCoreData);

  // AuthGate completes bootstrap before revealing this route. Keep the route
  // blank during any later session or realtime refresh instead of treating a
  // transient null value as an unbound relationship.
  const relationship = coupleState?.couple;
  const bound = Boolean(relationship?.id && relationship.status === 'active');
  const destination = !isReal
    ? '/(tabs)'
    : loading || (coupleState === null && !loadError)
      ? null
      : bound
        ? '/(tabs)'
        : '/account/invite';

  useEffect(() => {
    if (destination) router.replace(destination);
  }, [destination]);

  if (isReal && (loading || (coupleState === null && !loadError))) {
    return (
      <FairyPage backgroundName="creamPaper" contentStyle={styles.pageContent}>
        <View style={styles.loadingCard}>
          <ActivityIndicator color={colors.accent} />
          <Text style={styles.loadingText}>正在确认你的童话空间…</Text>
        </View>
      </FairyPage>
    );
  }

  if (isReal && loadError) {
    return (
      <FairyPage backgroundName="creamPaper" contentStyle={styles.pageContent}>
        <FairyRequestState error={loadError} onRetry={refreshCoreData} />
      </FairyPage>
    );
  }

  return null;
}

const styles = StyleSheet.create({
  pageContent: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  loadingCard: { alignItems: 'center', gap: 12, padding: 24 },
  loadingText: { color: colors.textSoft, fontSize: 13, fontWeight: '700' },
});
