import { Text, StyleSheet } from 'react-native';
import colors from '../theme/colors';

export default function FairyTag({ children, tone, style }) {
  const isGold = tone === 'gold';
  return <Text style={[styles.tag, isGold ? styles.gold : null, style]}>{children}</Text>;
}

const styles = StyleSheet.create({
  tag: {
    alignSelf: 'flex-start',
    paddingHorizontal: 11,
    paddingVertical: 5,
    borderRadius: 20,
    backgroundColor: '#FFF7FA',
    borderWidth: 1,
    borderColor: '#F5C6CE',
    color: colors.accent,
    fontSize: 12,
    fontWeight: '700',
    lineHeight: 16,
    overflow: 'hidden',
  },
  gold: {
    backgroundColor: '#FFF8EA',
    borderColor: '#EED39A',
    color: colors.gold,
  },
});
