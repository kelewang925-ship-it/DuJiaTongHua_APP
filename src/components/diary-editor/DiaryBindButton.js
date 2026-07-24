import { Ionicons } from '@expo/vector-icons';
import { Pressable, StyleSheet, Text } from 'react-native';

import colors from '@/theme/colors';
import spacing from '@/theme/spacing';

export default function DiaryBindButton({ loading, onPress }) {
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityState={{ busy: loading, disabled: loading }}
      disabled={loading}
      onPress={onPress}
      style={({ pressed }) => [styles.button, pressed && !loading && styles.pressed, loading && styles.loading]}
    >
      <Ionicons name={loading ? 'book-outline' : 'sparkles-outline'} size={20} color={colors.text.inverse} />
      <Text style={styles.text}>{loading ? '正在装订...' : '装订进故事书'}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: { minHeight: 54, width: '100%', flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, borderRadius: 18, backgroundColor: colors.text.primary, paddingHorizontal: spacing.xl, shadowColor: colors.text.primary, shadowOpacity: 0.22, shadowRadius: 8, shadowOffset: { width: 0, height: 4 }, elevation: 3 },
  loading: { opacity: 0.72 },
  pressed: { opacity: 0.82, transform: [{ scale: 0.99 }] },
  text: { color: colors.text.inverse, fontSize: 16, fontWeight: '900' },
});
