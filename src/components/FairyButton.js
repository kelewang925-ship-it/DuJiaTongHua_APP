import { Image, ImageBackground, Pressable, Text, StyleSheet, View } from 'react-native';
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
  const hasBackgroundImage = Boolean(backgroundSource);
  const image = imageSource ? (
    <Image
      source={imageSource}
      resizeMode="contain"
      style={[styles.image, { width: imageWidth, height: imageHeight }, imageStyle]}
    />
  ) : null;
  const leftSlot = leftContent || (imagePosition === 'left' ? image : null);
  const rightSlot = rightContent || (imagePosition === 'right' ? image : null);
  const content = (
    <View style={styles.contentLayer}>
      {leftSlot ? <View style={styles.slot}>{leftSlot}</View> : null}
      <Text
        selectable={false}
        style={[styles.text, isLink ? styles.linkText : isPrimary ? styles.primaryText : styles.secondaryText, disabled && styles.disabledText, textStyle]}
      >
        {title}
      </Text>
      {rightSlot ? <View style={styles.slot}>{rightSlot}</View> : null}
    </View>
  );

  return (
    <Pressable
      onPress={onPress}
      disabled={disabled}
      style={({ pressed }) => [
        styles.button,
        hasBackgroundImage ? styles.imageBackgroundButton : isLink ? styles.link : isPrimary ? styles.primary : styles.secondary,
        pressed && !disabled && styles.pressed,
        pressed && !disabled && isLink && styles.linkPressed,
        disabled && styles.disabled,
        style,
      ]}
    >
      {backgroundSource ? (
        <ImageBackground
          source={backgroundSource}
          resizeMode={backgroundResizeMode}
          style={styles.backgroundContent}
          imageStyle={styles.backgroundImage}
        >
          {content}
        </ImageBackground>
      ) : content}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    height: 52,
    // borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 20,
    overflow: 'hidden',
  },
  backgroundContent: {
    ...StyleSheet.absoluteFillObject,
    alignItems: 'center',
    justifyContent: 'center',
  },
  backgroundImage: {
    width: '100%',
    height: '100%',
  },
  contentLayer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    userSelect: 'none',
  },
  image: {
    flexShrink: 0,
  },
  slot: {
    flexShrink: 0,
    alignItems: 'center',
    justifyContent: 'center',
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
    borderWidth: 0,
  },
  link: {
    height: 'auto',
    minHeight: 0,
    paddingHorizontal: 0,
    paddingVertical: 0,
    borderRadius: 0,
    backgroundColor: 'transparent',
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
    userSelect: 'none',
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
