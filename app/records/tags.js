import { useEffect } from 'react';
import { router } from 'expo-router';

export default function RecordTagsRedirect() {
  useEffect(() => {
    router.replace('/tags');
  }, []);

  return null;
}
