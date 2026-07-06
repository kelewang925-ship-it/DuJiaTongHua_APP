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
        <View style={[styles.side, styles.left]}>
          {showBack ? <FairyBackButton name={backName} /> : null}
        </View>
        <View style={styles.center}>
          {renderTitle(title)}
        </View>
        <View style={[styles.side, styles.right]}>
          {typeof right === 'string' || typeof right === 'number' ? (
            <Text style={styles.rightText} numberOfLines={1}>
              {right}
            </Text>
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
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 55,
    position: 'relative',
  },
  side: {
    position: 'absolute',
    top: 0,
    bottom: 0,
    width: 64,
    minHeight: 55,
    justifyContent: 'center',
    zIndex: 2,
  },
  left: {
    left: 0,
    alignItems: 'flex-start',
  },
  center: {
    position: 'absolute',
    left: 64 + spacing.md,
    right: 64 + spacing.md,
    top: 0,
    bottom: 0,
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 1,
  },
  title: {
    color: colors.text,
    fontSize: 18,
    fontWeight: '900',
    lineHeight: 24,
    textAlign: 'center',
  },
  right: {
    right: 0,
    alignItems: 'flex-end',
  },
  rightText: {
    color: colors.text,
    fontSize: 14,
    fontWeight: '800',
    lineHeight: 20,
    maxWidth: 64,
    textAlign: 'right',
  },
});
