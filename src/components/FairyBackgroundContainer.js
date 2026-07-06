import { ImageBackground, StyleSheet, View } from 'react-native';

function normalizeImageSource(source) {
  if (!source) return null;
  return typeof source === 'string' ? { uri: source } : source;
}

export default function FairyBackgroundContainer({
  children,
  source,
  resizeMode = 'stretch',
  style,
  imageStyle,
}) {
  const imageSource = normalizeImageSource(source);

  if (!imageSource) {
    return <View style={[styles.container, style]}>{children}</View>;
  }

  return (
    <ImageBackground
      source={imageSource}
      resizeMode={resizeMode}
      style={[styles.container, style]}
      imageStyle={[styles.image, imageStyle]}
    >
      {children}
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  container: {
    width: '100%',
    height: '100%',
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
  },
  image: {
    width: '100%',
    height: '100%',
  },
});
