import { View, StyleSheet, Image } from 'react-native';
import colors from '../theme/colors';
import spacing from '../theme/spacing';
import FairyIllustration from './FairyIllustration';
import { getFairyImage } from '../assets/fairyImages';

const fallbackSceneMap = {
  homeCover: 'cover',
  coupleCover: 'cover',
  workshopCover: 'workshop',
  aiComicTriptych: 'workshop',
  albumCover: 'album',
  anniversaryCover: 'anniversary',
  exportCover: 'cover',
  timeCapsuleCover: 'cover',
  emptyAlbum: 'album',
  emptyDiary: 'cover',
  emptySearch: 'cover',
  emptyNotification: 'cover',
  emptyAiHistory: 'workshop',
  pdfMemoryBookCover: 'cover',
  sharePreviewCover: 'cover',
  anniversaryShareCover: 'anniversary',
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
  const asset = getFairyImage(name);
  const source = customSource || asset?.localSource;
  const scene = fallbackSceneMap[name] || asset?.scene || 'cover';

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
