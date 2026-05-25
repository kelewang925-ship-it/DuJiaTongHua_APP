import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../theme/colors';
import spacing from '../theme/spacing';
import typography from '../theme/typography';
import FairyCard from './FairyCard';
import FairyTag from './FairyTag';

export default function MemoryCard({ type, title, content, date, icon }) {
  return (
    <FairyCard style={styles.card}>
      <View style={styles.header}>
        <View style={styles.iconWrap}>
          <Ionicons name={icon || 'heart-outline'} size={18} color={colors.accent} />
        </View>
        <View style={styles.headerText}>
          <Text style={styles.title}>{title}</Text>
          <Text style={styles.date}>{date}</Text>
        </View>
        <FairyTag>{type}</FairyTag>
      </View>
      <Text style={styles.content}>{content}</Text>
    </FairyCard>
  );
}

const styles = StyleSheet.create({
  card: {
    marginBottom: spacing.lg,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  iconWrap: {
    width: 36,
    height: 36,
    borderRadius: 14,
    backgroundColor: colors.cardPink,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: spacing.md,
  },
  headerText: {
    flex: 1,
  },
  title: {
    ...typography.subtitle,
    color: colors.text,
    fontWeight: '700',
  },
  date: {
    ...typography.caption,
    color: colors.textSoft,
    marginTop: 2,
  },
  content: {
    ...typography.body,
    color: colors.text,
  },
});
