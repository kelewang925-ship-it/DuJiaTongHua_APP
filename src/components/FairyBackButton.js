import { Image, Pressable, StyleSheet } from 'react-native';
import { router } from 'expo-router';

const defaultButtonSize = {
  width: 40,
  height: 40,
};

const buttonImages = {
  rollback1: require('../../assets/images/icons/arrow/rollback1.png'),
  rollback2: require('../../assets/images/icons/arrow/rollback2.png'),
  rollback3: require('../../assets/images/icons/arrow/rollback3.png'),
};

const buttonImageSizes = {
  rollback1: { width: 921, height: 964 },
  rollback2: { width: 721, height: 578 },
  rollback3: { width: 886, height: 895 },
};

function isPositiveNumber(value) {
  return typeof value === 'number' && Number.isFinite(value) && value > 0;
}

function getScaledSize(originalSize, targetWidth, targetHeight) {
  const hasWidth = isPositiveNumber(targetWidth);
  const hasHeight = isPositiveNumber(targetHeight);

  if (!originalSize || (!hasWidth && !hasHeight)) {
    return {
      width: targetWidth,
      height: targetHeight,
    };
  }

  if (hasWidth && hasHeight) {
    const scale = Math.min(targetWidth / originalSize.width, targetHeight / originalSize.height);

    return {
      width: originalSize.width * scale,
      height: originalSize.height * scale,
    };
  }

  if (hasWidth) {
    return {
      width: targetWidth,
      height: targetWidth * (originalSize.height / originalSize.width),
    };
  }

  if (hasHeight) {
    return {
      width: targetHeight * (originalSize.width / originalSize.height),
      height: targetHeight,
    };
  }

  return originalSize;
}

export default function FairyBackButton({
  name = 'rollback1',
  source,
  style,
  imageStyle,
  onPress,
  width,
  height,
}) {
  const imageSource = source || buttonImages[name] || buttonImages.rollback1;
  const flattenedStyle = StyleSheet.flatten(style) || {};
  const targetWidth = width ?? flattenedStyle.width ?? defaultButtonSize.width;
  const targetHeight = height ?? flattenedStyle.height ?? defaultButtonSize.height;
  const imageSize = getScaledSize(buttonImageSizes[name] || buttonImageSizes.rollback1, targetWidth, targetHeight);

  return (
    <Pressable style={[styles.button, style, imageSize]} onPress={onPress || (() => router.back())}>
      <Image source={imageSource} resizeMode="contain" style={[styles.image, imageSize, imageStyle]} />
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  image: {
    flexShrink: 0,
  },
});
