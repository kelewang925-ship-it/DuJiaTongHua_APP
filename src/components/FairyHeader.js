import { View, Text, StyleSheet } from 'react-native';
import colors from '../theme/colors';
import spacing from '../theme/spacing';
import FairyBackButton from './FairyBackButton';

function renderTitle(title) {
  if (title === null || title === undefined) {
    return null;
  }

  if (typeof title === 'string' || typeof title === 'number') {
    return (
      <Text style={styles.title} numberOfLines={1}>
        {title}
      </Text>
    );
  }

  return title;
}

export default function FairyHeader({
  title,
  showBack = false,
  right,
  style,
  backName,
}) {
  return (
    <View style={[styles.wrap, style]}>
      <View style={styles.row}>
        <View style={styles.side}>
          {showBack ? <FairyBackButton name={backName} /> : null}
        </View>
        <View style={styles.center}>
          {renderTitle(title)}
        </View>
        <View style={[styles.side, styles.right]}>
          {typeof right === 'string' || typeof right === 'number' ? (
            <Text style={styles.rightText}>{right}</Text>
          ) : (
            right || null
          )}
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: {
    // marginBottom: spacing.xxl,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: spacing.md,
    minHeight: 55,
  },
  side: {
    width: 64,
    minHeight: 55,
    justifyContent: 'center',
  },
  center: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    color: colors.text,
    fontSize: 18,
    fontWeight: '900',
    lineHeight: 24,
    textAlign: 'center',
  },
  right: {
    alignItems: 'flex-end',
  },
  rightText: {
    color: colors.text,
    fontSize: 14,
    fontWeight: '800',
  },
});
