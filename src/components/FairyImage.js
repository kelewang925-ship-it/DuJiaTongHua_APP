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
  exportCover: 'cover',
  timeCapsuleCover: 'cover',
  emptyAlbum: 'album',
  emptyDiary: 'cover',
  emptySearch: 'cover',
  emptyNotification: 'cover',
};

const imageSourceMap = {
  homeCover: require('../../assets/images/illustrations/home-cover-v1.png'),
  coupleCover: require('../../assets/images/illustrations/couple-space-cover-v1.png'),
  workshopCover: require('../../assets/images/illustrations/workshop-cover-v1.png'),
  albumCover: require('../../assets/images/illustrations/album-cover-v1.png'),
  anniversaryCover: require('../../assets/images/illustrations/anniversary-cover-v1.png'),
  exportCover: require('../../assets/images/illustrations/export-cover-v1.png'),
  timeCapsuleCover: require('../../assets/images/illustrations/time-capsule-cover-v1.png'),
  emptyAlbum: require('../../assets/images/illustrations/empty-album-v1.png'),
  emptyDiary: require('../../assets/images/illustrations/empty-diary-v1.png'),
  emptySearch: require('../../assets/images/illustrations/empty-search-v1.png'),
  emptyNotification: require('../../assets/images/illustrations/empty-notification-v1.png'),
};

export default function FairyImage({
  name = 'homeCover',
  height = 168,
  radius = 28,
  framed = true,
  resizeMode = 'cover',
  source: customSource,
  style,
}) {
  const source = customSource || imageSourceMap[name] || getFairyImage(name)?.localSource;
  const scene = fallbackSceneMap[name] || getFairyImage(name)?.scene || 'cover';

  if (!source) {
    return (
      <View style={[styles.fallback, framed && styles.framed, { height, borderRadius: radius }, style]}>
        <FairyIllustration scene={scene} height={height} />
      </View>
    );
  }

  return (
    <View style={[styles.frame, framed && styles.framed, { height, borderRadius: radius }, style]}>
      <Image source={source} resizeMode={resizeMode} style={styles.image} />
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
