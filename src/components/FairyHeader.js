import { View, Text, StyleSheet } from 'react-native';
import colors from '../theme/colors';
import spacing from '../theme/spacing';
import FairyBackButton from './FairyBackButton';

export default function FairyHeader({
  title,
  subtitle,
  eyebrow,
  showBack = false,
  right,
  style,
}) {
  return (
    <View style={[styles.wrap, style]}>
      {showBack ? <FairyBackButton /> : null}
      <View style={styles.row}>
        <View style={styles.textWrap}>
          {eyebrow ? <Text style={styles.eyebrow}>{eyebrow}</Text> : null}
          <Text style={styles.title}>{title}</Text>
          {subtitle ? <Text style={styles.subtitle}>{subtitle}</Text> : null}
        </View>
        {right ? <View style={styles.right}>{right}</View> : null}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: {
    marginBottom: spacing.xxl,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    justifyContent: 'space-between',
    gap: spacing.md,
  },
  textWrap: {
    flex: 1,
  },
  eyebrow: {
    color: colors.accent,
    fontSize: 12,
    fontWeight: '800',
    marginBottom: 6,
  },
  title: {
    color: colors.text,
    fontSize: 30,
    fontWeight: '900',
    lineHeight: 36,
  },
  subtitle: {
    color: colors.textSoft,
    marginTop: 8,
    lineHeight: 22,
  },
  right: {
    marginTop: 2,
  },
});
