import { Image, StyleSheet } from 'react-native';
import { getFairySticker } from '../assets/fairyStickers';

export default function FairySticker({ name = 'heart', size = 44, rotate = '0deg', style }) {
  const sticker = getFairySticker(name);

  return (
    <Image
      source={sticker.localSource}
      resizeMode="contain"
      style={[styles.sticker, { width: size, height: size, transform: [{ rotate }] }, style]}
    />
  );
}

const styles = StyleSheet.create({
  sticker: {
    position: 'absolute',
    zIndex: 2,
  },
});
