import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../theme/colors';
import spacing from '../theme/spacing';
import FairyButton from './FairyButton';
import FairyCard from './FairyCard';
import FairyIllustration from './FairyIllustration';
import FairyImage from './FairyImage';

export default function FairyEmptyState({
  icon = 'sparkles-outline',
  scene = 'cover',
  imageName,
  title = '今天的故事，还没有开始。',
  description = '写下一点点小事，它就会成为你们童话里的一页。',
  actionTitle,
  onAction,
  compact = false,
  style,
}) {
  return (
    <FairyCard style={[styles.card, compact && styles.compactCard, style]}>
      {imageName && !compact ? (
        <FairyImage name={imageName} height={150} radius={24} />
      ) : compact ? (
        <View style={styles.compactIcon}>
          <Ionicons name={icon} size={24} color={colors.accent} />
        </View>
      ) : (
        <FairyIllustration scene={scene} height={150} />
      )}
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.description}>{description}</Text>
      {actionTitle ? <FairyButton title={actionTitle} onPress={onAction} style={styles.action} /> : null}
    </FairyCard>
  );
}

const styles = StyleSheet.create({
  card: {
    alignItems: 'center',
    backgroundColor: colors.cardPink,
    paddingVertical: spacing.xxl,
  },
  compactCard: {
    paddingVertical: spacing.xl,
  },
  compactIcon: {
    width: 58,
    height: 58,
    borderRadius: 22,
    backgroundColor: colors.card,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: colors.border,
    marginBottom: spacing.lg,
  },
  title: {
    color: colors.text,
    fontSize: 18,
    fontWeight: '900',
    textAlign: 'center',
    marginTop: spacing.md,
  },
  description: {
    color: colors.textSoft,
    fontSize: 13,
    lineHeight: 21,
    textAlign: 'center',
    marginTop: spacing.sm,
  },
  action: {
    alignSelf: 'stretch',
    marginTop: spacing.xl,
  },
});
