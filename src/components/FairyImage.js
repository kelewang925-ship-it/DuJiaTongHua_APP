import { View, StyleSheet, Image } from 'react-native';
import colors from '../theme/colors';
import spacing from '../theme/spacing';
import FairyIllustration from './FairyIllustration';
import { getFairyImage } from '../assets/fairyImages';

const fallbackSceneMap = {
  homeCover: 'cover',
  coupleCover: 'cover',
  workshopCover: 'workshop',
  albumCover: 'album',
  anniversaryCover: 'anniversary',
};

// 后续接入真实 PNG/WebP 图片时，在这里维护映射：
// const imageSourceMap = {
//   homeCover: require('../../assets/images/illustrations/home-cover-v1.png'),
//   coupleCover: require('../../assets/images/illustrations/couple-space-cover-v1.png'),
//   workshopCover: require('../../assets/images/illustrations/workshop-cover-v1.png'),
// };
const imageSourceMap = {};

export default function FairyImage({
  name = 'homeCover',
  height = 168,
  radius = 28,
  framed = true,
  source: customSource,
  style,
}) {
  const source = customSource || imageSourceMap[name] || getFairyImage(name)?.localSource;
  const scene = fallbackSceneMap[name] || 'cover';

  if (!source) {
    return (
      <View style={[styles.fallback, framed && styles.framed, { height, borderRadius: radius }, style]}>
        <FairyIllustration scene={scene} height={height} />
      </View>
    );
  }

  return (
    <View style={[styles.frame, framed && styles.framed, { height, borderRadius: radius }, style]}>
      <Image source={source} resizeMode="cover" style={styles.image} />
    </View>
  );
}

const styles = StyleSheet.create({
  fallback: {
    width: '100%',
    overflow: 'hidden',
    alignItems: 'center',
    justifyContent: 'center',
  },
  frame: {
    width: '100%',
    overflow: 'hidden',
  },
  image: {
    width: '100%',
    height: '100%',
  },
  framed: {
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.xs,
  },
});
