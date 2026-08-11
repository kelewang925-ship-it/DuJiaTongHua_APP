import { Pressable, StyleSheet, Text, View } from 'react-native';
import colors from '../theme/colors';
import spacing from '../theme/spacing';

export default function FairySection({
  title,
  description,
  actionLabel,
  onAction,
  children,
  style,
}) {
  return (
    <View style={[styles.section, style]}>
      {(title || description || actionLabel) ? (
        <View style={styles.header}>
          <View style={styles.copy}>
            {title ? <Text style={styles.title}>{title}</Text> : null}
            {description ? <Text style={styles.description}>{description}</Text> : null}
          </View>
          {actionLabel && onAction ? (
            <Pressable accessibilityRole="button" onPress={onAction} style={styles.action}>
              <Text style={styles.actionText}>{actionLabel}</Text>
            </Pressable>
          ) : null}
        </View>
      ) : null}
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  section: {
    width: '100%',
    marginBottom: spacing.xl,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: spacing.md,
    marginBottom: spacing.md,
  },
  copy: {
    flex: 1,
  },
  title: {
    color: colors.text,
    fontSize: 18,
    lineHeight: 24,
    fontWeight: '800',
  },
  description: {
    marginTop: spacing.xs,
    color: colors.textSoft,
    fontSize: 12,
    lineHeight: 18,
  },
  action: {
    minHeight: 36,
    justifyContent: 'center',
    paddingHorizontal: spacing.sm,
  },
  actionText: {
    color: colors.primaryDeep,
    fontSize: 12,
    fontWeight: '800',
  },
});
