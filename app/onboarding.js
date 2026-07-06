import { Image, StyleSheet, useWindowDimensions, View } from 'react-native';
import { router } from 'expo-router';
import FairyButton from '../src/components/FairyButton';
import FairyPage from '../src/components/FairyPage';
import spacing from '../src/theme/spacing';

export default function OnboardingPage() {
  const { height } = useWindowDimensions();
  const heroHeight = Math.min(Math.max(height * 0.58, 300), 430);

  return (
    <FairyPage
      backgroundName="softPink"
      topSpace={40}
      bottomSpace={80}
      contentStyle={styles.pageContent}
      showsVerticalScrollIndicator
    >
      <Image
        source={require('../assets/images/guide-page/imagebackground.png')}
        resizeMode="contain"
        style={[styles.backgroundImage, { height: heroHeight }]}
      />

      <View style={styles.actions}>
        <FairyButton
          title="开始书写"
          onPress={() => router.push('/login')}
          backgroundName="buttonBackground3"
          style={styles.startButton}
        />
        <View style={styles.linkWrap}>
          <FairyButton
            title="直接进入首页"
            variant="link"
            onPress={() => router.push('/(tabs)')}
          />
          <Image
            source={require('../assets/images/guide-page/image1.png')}
            resizeMode="contain"
            style={styles.linkUnderline}
          />
        </View>
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: {
    flexGrow: 1,
    justifyContent: 'space-between',
    paddingHorizontal: 0,
    // paddingBottom: 46,
  },
  backgroundImage: {
    width: '100%',
  },
  actions: {
    gap: spacing.md,
    paddingHorizontal: spacing.page,
    alignItems: 'center',
  },
  startButton: {
    width: 250,
    height: 60,
  },
  linkWrap: {
    alignItems: 'center',
  },
  linkUnderline: {
    width: 100,
    height: 10,
  },
});
