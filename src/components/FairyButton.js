import { Image, Pressable, Text, StyleSheet, View } from 'react-native';
import colors from '../theme/colors';

const buttonImageSourceMap = {
  background1: require('../../assets/images/backgrounds/background1.png'),
  background2: require('../../assets/images/backgrounds/background2.png'),
  imagebackground: require('../../assets/images/guide-page/imagebackground.png'),
};

const buttonBackgroundSourceMap = {
  buttonBackground1: require('../../assets/images/buttonImages/buttonBackground1.png'),
  buttonBackground2: require('../../assets/images/buttonImages/buttonBackground2.png'),
  buttonBackground3: require('../../assets/images/buttonImages/buttonBackground3.png'),
  buttonBackground4: require('../../assets/images/buttonImages/buttonBackground4.png'),
  buttonBackground5: require('../../assets/images/buttonImages/buttonBackground5.png'),
  buttonBackground6: require('../../assets/images/buttonImages/buttonBackground6.png'),
  buttonBackground7: require('../../assets/images/buttonImages/buttonBackground7.png'),
  buttonBackground8: require('../../assets/images/buttonImages/buttonBackground8.png'),
  buttonBackground9: require('../../assets/images/buttonImages/buttonBackground9.png'),
  buttonBackground10: require('../../assets/images/buttonImages/buttonBackground10.png'),
};

export default function FairyButton({
  title,
  variant = 'primary',
  onPress,
  style,
  disabled = false,
  imageName,
  imageWidth = 22,
  imageHeight = 22,
  imagePosition = 'left',
  imageStyle,
  leftContent,
  rightContent,
  textStyle,
  backgroundName,
  backgroundResizeMode = 'stretch',
}) {
  const isPrimary = variant === 'primary';
  const isLink = variant === 'link';

  const imageSource = buttonImageSourceMap[imageName];
  const backgroundSource = buttonBackgroundSourceMap[backgroundName];

  const image = imageSource ? (
    <Image
      source={imageSource}
      resizeMode="contain"
      style={[
        styles.image,
        { width: imageWidth, height: imageHeight },
        imageStyle,
      ]}
    />
  ) : null;

  const leftSlot = leftContent || (imagePosition === 'left' ? image : null);
  const rightSlot = rightContent || (imagePosition === 'right' ? image : null);

  return (
    <Pressable
      onPress={onPress}
      disabled={disabled}
      style={({ pressed }) => [
        styles.button,
        hasBackground(backgroundSource)
          ? styles.imageBackgroundButton
          : isLink
          ? styles.link
          : isPrimary
          ? styles.primary
          : styles.secondary,
        pressed && !disabled && styles.pressed,
        pressed && !disabled && isLink && styles.linkPressed,
        disabled && styles.disabled,
        style,
      ]}
    >
      {/* ✅ 背景层 */}
      {backgroundSource ? (
        <Image
          pointerEvents="none"
          source={backgroundSource}
          resizeMode={backgroundResizeMode}
          style={styles.backgroundImage}
        />
      ) : null}

      {/* ✅ 内容层 */}
      <View style={isLink ? styles.linkContentLayer : styles.contentLayer}>
        {/* left（绝对定位，不影响居中） */}
        {leftSlot ? (
          <View style={styles.leftAbs}>
            {leftSlot}
          </View>
        ) : null}

        {/* center（真正视觉居中） */}
        <Text
          selectable={false}
          numberOfLines={1}
          style={[
            styles.text,
            isLink
              ? styles.linkText
              : isPrimary
              ? styles.primaryText
              : styles.secondaryText,
            disabled && styles.disabledText,
            textStyle,
          ]}
        >
          {title}
        </Text>

        {/* right（绝对定位，不影响居中） */}
        {rightSlot ? (
          <View style={styles.rightAbs}>
            {rightSlot}
          </View>
        ) : null}
      </View>
    </Pressable>
  );
}

function hasBackground(bg) {
  return Boolean(bg);
}

const styles = StyleSheet.create({
  button: {
    position: 'relative',
    height: 52,
    overflow: 'hidden',

    alignItems: 'center',
    justifyContent: 'center',
  },

  /* ✅ 背景真正铺满 */
  backgroundImage: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    width: '100%',
    height: '100%',
  },

  /* ✅ 内容层：统一居中 */
  contentLayer: {
    position: 'relative',
    width: '100%',
    height: '100%',

    justifyContent: 'center',
    alignItems: 'center',
  },
  linkContentLayer: {
    position: 'relative',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },

  /* ✅ 左右绝对定位 */
  leftAbs: {
    position: 'absolute',
    left: 0,
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
  },

  rightAbs: {
    position: 'absolute',
    right: 0,
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
  },

  image: {
    flexShrink: 0,
  },

  primary: {
    backgroundColor: colors.primary,
  },

  secondary: {
    backgroundColor: colors.secondary,
    borderWidth: 1,
    borderColor: colors.border,
  },

  imageBackgroundButton: {
    backgroundColor: 'transparent',
  },

  link: {
    height: 'auto',
    minHeight: 0,
    paddingHorizontal: 0,
    paddingVertical: 0,
    backgroundColor: 'transparent',
    overflow: 'visible',
  },

  pressed: {
    transform: [{ scale: 0.97 }],
    opacity: 0.9,
  },

  linkPressed: {
    transform: [{ scale: 1 }],
    opacity: 0.65,
  },

  disabled: {
    opacity: 0.48,
  },

  text: {
    fontSize: 16,
    fontWeight: '700',
    textAlign: 'center',
  },

  primaryText: {
    color: colors.white,
  },

  secondaryText: {
    color: colors.text,
  },

  linkText: {
    color: colors.accent,
  },

  disabledText: {
    color: colors.textSoft,
  },
});
