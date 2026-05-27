import { useEffect } from 'react';
import { router } from 'expo-router';

export default function RecordTimeCapsuleRedirect() {
  useEffect(() => {
    router.replace('/time-capsule/settings');
  }, []);

  return null;
}
