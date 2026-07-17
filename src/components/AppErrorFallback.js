import { Pressable, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../theme/colors';
import spacing from '../theme/spacing';

export default function AppErrorFallback({ error, retry }) {
  return (
    <View style={styles.page}>
      <View style={styles.iconWrap}>
        <Ionicons name="cloud-offline-outline" size={34} color={colors.primaryDeep} />
      </View>
      <Text style={styles.title}>这一页暂时迷路了</Text>
      <Text style={styles.description}>
        {__DEV__ && error?.message ? error.message : '请重新打开这一页，童话会从这里继续。'}
      </Text>
      <Pressable accessibilityRole="button" onPress={retry} style={({ pressed }) => [styles.button, pressed && styles.buttonPressed]}>
        <Ionicons name="refresh" size={18} color={colors.white} />
        <Text style={styles.buttonText}>重新打开</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  page: {
    flex: 1,
    paddingHorizontal: spacing.xl,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.background,
  },
  iconWrap: {
    width: 72,
    height: 72,
    borderRadius: 28,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.cardPink,
    borderWidth: 1,
    borderColor: colors.border,
  },
  title: {
    marginTop: spacing.lg,
    color: colors.text,
    fontSize: 24,
    fontWeight: '900',
  },
  description: {
    maxWidth: 360,
    marginTop: spacing.sm,
    color: colors.textSoft,
    fontSize: 14,
    lineHeight: 22,
    textAlign: 'center',
  },
  button: {
    minHeight: 48,
    marginTop: spacing.xl,
    paddingHorizontal: spacing.xl,
    borderRadius: 20,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
    backgroundColor: colors.primaryDeep,
  },
  buttonPressed: {
    opacity: 0.86,
    transform: [{ scale: 0.98 }],
  },
  buttonText: {
    color: colors.white,
    fontSize: 15,
    fontWeight: '900',
  },
});
