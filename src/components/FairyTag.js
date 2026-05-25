import { Text, StyleSheet } from 'react-native';
import colors from '../theme/colors';

export default function FairyTag({ children, tone, style }) {
  const isGold = tone === 'gold';
  return <Text style={[styles.tag, isGold ? styles.gold : null, style]}>{children}</Text>;
}

const styles = StyleSheet.create({
  tag: {
    alignSelf: 'flex-start',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 20,
    backgroundColor: colors.cardPink,
    color: colors.accent,
    fontSize: 12,
    overflow: 'hidden',
  },
  gold: {
    backgroundColor: '#F7E8D5',
    color: colors.gold,
  },
});
