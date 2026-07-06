import { Image, StyleSheet, useWindowDimensions, View } from 'react-native';
import { router } from 'expo-router';
import FairyButton from '../src/components/FairyButton';
import FairyPage from '../src/components/FairyPage';
import spacing from '../src/theme/spacing';

export default function OnboardingPage() {
  const { width } = useWindowDimensions();
  const heroWidth = Math.min(width, 430);
  const heroHeight = heroWidth * (1402 / 1122);

  return (
    <FairyPage
      backgroundName="softPink"
      topSpace={40}
      bottomSpace={80}
      contentStyle={styles.pageContent}
      showsVerticalScrollIndicator
    >
      <View style={styles.heroWrap}>
        <Image
          source={require('../assets/images/guide-page/imagebackground.png')}
          resizeMode="contain"
          style={[styles.backgroundImage, { width: heroWidth, height: heroHeight }]}
        />
      </View>

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
    alignItems: 'center',
    paddingHorizontal: 0,
    // paddingBottom: 46,
  },
  heroWrap: {
    width: '100%',
    alignItems: 'center',
  },
  backgroundImage: {
    flexShrink: 0,
  },
  actions: {
    gap: spacing.md,
    width: '100%',
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
