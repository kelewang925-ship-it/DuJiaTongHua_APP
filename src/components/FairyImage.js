import { View, StyleSheet } from 'react-native';
import colors from '../theme/colors';
import spacing from '../theme/spacing';
import FairyIllustration from './FairyIllustration';

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
  style,
}) {
  const source = imageSourceMap[name];
  const scene = fallbackSceneMap[name] || 'cover';

  if (!source) {
    return (
      <View style={[styles.fallback, framed && styles.framed, { height, borderRadius: radius }, style]}>
        <FairyIllustration scene={scene} height={height} />
      </View>
    );
  }

  // 当前未启用真实 Image 资源映射；保留结构，后续替换时只需要打开此分支。
  return (
    <View style={[styles.fallback, framed && styles.framed, { height, borderRadius: radius }, style]}>
      <FairyIllustration scene={scene} height={height} />
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
  framed: {
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.xs,
  },
});
