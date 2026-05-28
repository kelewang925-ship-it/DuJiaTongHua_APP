import { ImageBackground, ScrollView, StyleSheet, View } from 'react-native';
import colors from '../theme/colors';
import spacing from '../theme/spacing';

const backgroundSourceMap = {
  creamPaper: require('../../assets/images/backgrounds/cream-paper-texture-v1.png'),
  softPink: require('../../assets/images/backgrounds/soft-pink-gradient-v1.png'),
};

export default function FairyPage({
  children,
  scroll = true,
  style,
  contentStyle,
  tabSafe = false,
  topSpace = 54,
  bottomSpace = 44,
  backgroundName,
}) {
  const contentStyles = [
    styles.content,
    { paddingTop: topSpace, paddingBottom: tabSafe ? 124 : bottomSpace },
    contentStyle,
  ];
  const backgroundSource = backgroundSourceMap[backgroundName];

  const renderBody = () => {
    if (!scroll) {
      return <View style={[styles.page, styles.staticContent, style]}>{children}</View>;
    }

    return (
      <ScrollView style={[styles.page, style]} contentContainerStyle={contentStyles} showsVerticalScrollIndicator={false}>
        {children}
      </ScrollView>
    );
  };

  if (backgroundSource) {
    return (
      <ImageBackground source={backgroundSource} resizeMode="cover" style={styles.backgroundImage} imageStyle={styles.backgroundImageInner}>
        {renderBody()}
      </ImageBackground>
    );
  }

  return renderBody();
}

const styles = StyleSheet.create({
  page: {
    flex: 1,
    backgroundColor: colors.background,
  },
  backgroundImage: {
    flex: 1,
    backgroundColor: colors.background,
  },
  backgroundImageInner: {
    opacity: 0.45,
  },
  content: {
    paddingHorizontal: spacing.page,
  },
  staticContent: {
    paddingHorizontal: spacing.page,
  },
});
