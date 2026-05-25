import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import colors from '../theme/colors';
import spacing from '../theme/spacing';
import typography from '../theme/typography';
import shadows from '../theme/shadows';

export default function WorkshopCard({ icon, title, description }) {
  return (
    <LinearGradient colors={['#FFF9F4', '#FFF0F2']} style={styles.card}>
      <View style={styles.iconWrap}>
        <Ionicons name={icon} size={24} color={colors.gold} />
      </View>
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.description}>{description}</Text>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  card: {
    flex: 1,
    minHeight: 152,
    borderRadius: 28,
    padding: spacing.xl,
    borderWidth: 1,
    borderColor: colors.border,
    ...shadows.card,
  },
  iconWrap: {
    width: 44,
    height: 44,
    borderRadius: 18,
    backgroundColor: '#FFF5DF',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.lg,
  },
  title: {
    ...typography.subtitle,
    color: colors.text,
    fontWeight: '800',
    marginBottom: spacing.xs,
  },
  description: {
    ...typography.caption,
    color: colors.textSoft,
  },
});
