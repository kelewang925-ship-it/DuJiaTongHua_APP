import { useState } from 'react';
import { Image, StyleSheet, View } from 'react-native';
import colors from '../theme/colors';

export default function FairyMediaFrame({
  source,
  aspectRatio = 1.5,
  radius = 24,
  resizeMode = 'contain',
  fallback = null,
  style,
  imageStyle,
}) {
  const [failed, setFailed] = useState(false);
  const showFallback = !source || failed;

  return (
    <View style={[styles.frame, { aspectRatio, borderRadius: radius }, style]}>
      {showFallback ? (
        fallback || <View style={styles.fallback} />
      ) : (
        <Image
          source={source}
          resizeMode={resizeMode}
          onError={() => setFailed(true)}
          style={[styles.image, imageStyle]}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  frame: {
    width: '100%',
    overflow: 'hidden',
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
  },
  image: {
    width: '100%',
    height: '100%',
  },
  fallback: {
    flex: 1,
    minHeight: 96,
    backgroundColor: colors.cardPink,
  },
});
