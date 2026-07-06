import { useEffect, useRef, useState } from 'react';
import { Animated, ImageBackground, Platform, ScrollView, StyleSheet, View } from 'react-native';
import { BlurTargetView, BlurView } from 'expo-blur';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import colors from '../theme/colors';
import spacing from '../theme/spacing';

const backgroundSourceMap = {
  creamPaper: require('../../assets/images/backgrounds/cream-paper-texture-v1.png'),
  softPink: require('../../assets/images/backgrounds/soft-pink-gradient-v1.png'),
  background1: require('../../assets/images/backgrounds/background1.png'),
  background2: require('../../assets/images/backgrounds/background2.png'),
};

const HEADER_MIN_HEIGHT = 55;
const AnimatedBlurView = Animated.createAnimatedComponent(BlurView);

export default function FairyPage({
  children,
  header,
  headerStyle,
  scroll = true,
  style,
  contentStyle,
  tabSafe = false,
  topSpace = 54,
  bottomSpace = 44,
  backgroundName,
  showsVerticalScrollIndicator = false,
}) {
  const insets = useSafeAreaInsets();
  const [headerElevated, setHeaderElevated] = useState(false);
  const headerShadowProgress = useRef(new Animated.Value(0)).current;
  const blurTargetRef = useRef(null);
  const mobileTopInset = Platform.OS === 'web' ? 0 : insets.top;
  const headerHeight = header ? HEADER_MIN_HEIGHT + mobileTopInset : 0;
  const contentTopSpace = topSpace + (header ? headerHeight : mobileTopInset);
  const headerTopInsetStyle = header && mobileTopInset ? { paddingTop: mobileTopInset } : null;
  const contentStyles = [
    styles.content,
    { paddingTop: contentTopSpace, paddingBottom: tabSafe ? 124 : bottomSpace },
    contentStyle,
  ];
  const backgroundSource = backgroundSourceMap[backgroundName];

  useEffect(() => {
    Animated.timing(headerShadowProgress, {
      toValue: headerElevated ? 1 : 0,
      duration: 180,
      useNativeDriver: false,
    }).start();
  }, [headerElevated, headerShadowProgress]);

  const renderBody = () => {
    const pageStyles = [styles.page, backgroundSource && styles.transparentPage, !backgroundSource && style];
    const restingBlurTargetStyle = StyleSheet.flatten([
      styles.blurTarget,
      styles.contentUnderHeader,
    ]);
    const scrollingBlurTargetStyle = StyleSheet.flatten([
      styles.blurTarget,
      styles.contentUnderHeader,
    ]);
    const headerBlurLayerStyle = StyleSheet.flatten([styles.headerBlurLayer, { opacity: headerShadowProgress }]);
    const headerBlurProps = Platform.OS === 'android'
      ? {
          blurMethod: 'dimezisBlurViewSdk31Plus',
          blurReductionFactor: 4,
          blurTarget: blurTargetRef,
        }
      : null;
    const headerNode = header ? (
      <View
        style={[
          styles.header,
          headerStyle,
          headerTopInsetStyle,
          headerElevated ? styles.headerElevated : styles.headerResting,
        ]}
      >
        <Animated.View
          pointerEvents="none"
          style={[
            styles.headerBaseLayer,
            {
              opacity: headerShadowProgress.interpolate({
                inputRange: [0, 1],
                outputRange: [1, 0],
              }),
            },
          ]}
        />
        <AnimatedBlurView
          pointerEvents="none"
          intensity={28}
          tint="light"
          {...headerBlurProps}
          style={headerBlurLayerStyle}
        />
        <Animated.View
          pointerEvents="none"
          style={[
            Platform.OS === 'web' ? styles.headerShadowLayer : styles.mobileHeaderShadowLayer,
            { opacity: headerShadowProgress },
          ]}
        />
        {Platform.OS === 'web' ? (
          <Animated.View
            pointerEvents="none"
            style={[styles.headerBottomTint, { opacity: headerShadowProgress }]}
          />
        ) : null}
        <View style={styles.headerContent}>{header}</View>
      </View>
    ) : null;

    const handleScroll = (event) => {
      if (!header) return;
      const shouldElevate = event.nativeEvent.contentOffset.y > 2;
      setHeaderElevated((current) => (current === shouldElevate ? current : shouldElevate));
    };

    if (!scroll) {
      return (
        <View style={pageStyles}>
          <BlurTargetView
            ref={blurTargetRef}
            style={restingBlurTargetStyle}
          >
            <View style={[styles.staticContent, ...contentStyles]}>{children}</View>
          </BlurTargetView>
          {headerNode}
        </View>
      );
    }

    return (
      <View style={pageStyles}>
        <BlurTargetView
          ref={blurTargetRef}
          style={scrollingBlurTargetStyle}
        >
          <ScrollView
            style={styles.scroll}
            contentContainerStyle={contentStyles}
            onScroll={handleScroll}
            scrollEventThrottle={16}
            showsVerticalScrollIndicator={showsVerticalScrollIndicator}
          >
            {children}
          </ScrollView>
        </BlurTargetView>
        {headerNode}
      </View>
    );
  };

  if (backgroundSource) {
    return (
      <ImageBackground
        source={backgroundSource}
        resizeMode="stretch"
        style={[styles.backgroundPage, style]}
        imageStyle={styles.backgroundImage}
      >
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
  backgroundPage: {
    width: '100%',
    height: '100%',
    flex: 1,
    backgroundColor: colors.background,
  },
  backgroundImage: {
    opacity: 0.45,
  },
  transparentPage: {
    flex: 1,
    backgroundColor: 'transparent',
  },
  content: {
    paddingHorizontal: spacing.page,
  },
  header: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    paddingHorizontal: spacing.page,
    borderBottomLeftRadius: 24,
    borderBottomRightRadius: 24,
  },
  headerResting: {
    zIndex: 100,
    elevation: 0,
  },
  headerElevated: {
    zIndex: 100,
    elevation: Platform.OS === 'android' ? 4 : 0,
  },
  headerBaseLayer: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: colors.background,
    borderBottomLeftRadius: 24,
    borderBottomRightRadius: 24,
  },
  headerBlurLayer: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(255, 248, 244, 0.78)',
    borderBottomLeftRadius: 24,
    borderBottomRightRadius: 24,
  },
  headerShadowLayer: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(255, 248, 244, 0.38)',
    borderBottomLeftRadius: 24,
    borderBottomRightRadius: 24,
    shadowColor: '#6F4F46',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 10,
    elevation: 3,
  },
  mobileHeaderShadowLayer: {
    position: 'absolute',
    left: spacing.page,
    right: spacing.page,
    bottom: -10,
    height: 22,
    backgroundColor: 'rgba(111, 79, 70, 0.14)',
    borderBottomLeftRadius: 28,
    borderBottomRightRadius: 28,
    shadowOpacity: 0,
    shadowRadius: 0,
    elevation: 0,
    zIndex: 0,
  },
  headerBottomTint: {
    position: 'absolute',
    left: spacing.page,
    right: spacing.page,
    bottom: 0,
    height: 1,
    backgroundColor: 'rgba(111, 79, 70, 0.12)',
    zIndex: 1,
  },
  headerContent: {
    position: 'relative',
    zIndex: 2,
  },
  blurTarget: {
    flex: 1,
  },
  contentOverRestingHeader: {
    zIndex: 0,
    elevation: 0,
  },
  contentUnderHeader: {
    zIndex: 0,
    elevation: 0,
  },
  scroll: {
    flex: 1,
  },
  staticContent: {
    paddingHorizontal: spacing.page,
  },
});
