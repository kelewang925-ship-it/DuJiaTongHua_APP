import { useEffect } from 'react';
import { router } from 'expo-router';

export default function CoupleSettingsPage() {
  useEffect(() => {
    router.replace('/account/couple-info');
  }, []);

  return null;
}
