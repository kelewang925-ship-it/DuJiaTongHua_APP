import { useEffect } from 'react';
import { router } from 'expo-router';

export default function InteractionNotificationsRedirect() {
  useEffect(() => {
    router.replace('/notifications');
  }, []);

  return null;
}
