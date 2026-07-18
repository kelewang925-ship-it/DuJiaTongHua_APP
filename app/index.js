import { useEffect } from 'react';
import { router } from 'expo-router';
import { getApiMode } from '../src/api/client';
import useFairyStore from '../src/store/useFairyStore';

export default function Index() {
  const isReal = getApiMode() === 'real';
  const coupleState = useFairyStore((state) => state.couple);
  const loading = useFairyStore((state) => Boolean(state.loading?.bootstrap));

  // AuthGate completes bootstrap before revealing this route. Keep the route
  // blank during any later session or realtime refresh instead of treating a
  // transient null value as an unbound relationship.
  const relationship = coupleState?.couple;
  const bound = Boolean(relationship?.id && relationship.status === 'active');
  const destination = !isReal
    ? '/(tabs)'
    : loading || coupleState === null
      ? null
      : bound
        ? '/(tabs)'
        : '/account/invite';

  useEffect(() => {
    if (destination) router.replace(destination);
  }, [destination]);

  return null;
}
