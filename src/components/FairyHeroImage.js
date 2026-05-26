import { Image, StyleSheet, View, Text } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../theme/colors';
import spacing from '../theme/spacing';
import FairyIllustration from './FairyIllustration';
import { getFairyImage } from '../assets/fairyImages';

export default function FairyHeroImage({ imageKey = 'homeHero', height = 160, showCaption = false, style }) {
  const asset = getFairyImage(imageKey);

  return (
    <View style={[styles.wrap, { minHeight: height }, style]}>
      {asset.localSource ? (
        <Image source={asset.localSource} style={[styles.image, { height }]} resizeMode="contain" />
      ) : (
        <View style={[styles.fallback, { minHeight: height }]}> 
          <FairyIllustration scene={asset.scene} height={height - 18} />
          <View style={styles.assetBadge}>
            <Ionicons name="image-outline" size={13} color={colors.accent} />
            <Text style={styles.assetText}>等待接入 AI 配图</Text>
          </View>
        </View>
      )}
      {showCaption ? <Text style={styles.caption}>{asset.title}</Text> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: {
    width: '100%',
  },
  image: {
    width: '100%',
  },
  fallback: {
    width: '100%',
    borderRadius: 24,
    backgroundColor: 'rgba(255, 255, 255, 0.22)',
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
  },
  assetBadge: {
    position: 'absolute',
    right: spacing.sm,
    bottom: spacing.sm,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    borderRadius: 14,
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.border,
    paddingHorizontal: spacing.sm,
    paddingVertical: 5,
  },
  assetText: {
    color: colors.textSoft,
    fontSize: 10,
    fontWeight: '700',
  },
  caption: {
    color: colors.textSoft,
    fontSize: 11,
    textAlign: 'center',
    marginTop: spacing.xs,
  },
});
