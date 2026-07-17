import { Image, Platform, Pressable, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import FairyBackButton from '../src/components/FairyBackButton';
import FairyPage from '../src/components/FairyPage';
import colors from '../src/theme/colors';
import spacing from '../src/theme/spacing';

const emptyDiarySource = require('../assets/images/illustrations/empty-diary-v1.png');
const ILLUSTRATION_RATIO = 1440 / 1086;

function HeaderDecoration() {
  return (
    <View pointerEvents="none" style={styles.headerDecoration}>
      <Ionicons name="star" size={17} color="#EAB765" />
      <View style={styles.dashedLine} />
      <Ionicons name="heart-outline" size={18} color="#EFA09C" />
      <View style={[styles.dashedLine, styles.shortLine]} />
      <Ionicons name="sparkles" size={16} color="#EAB765" />
    </View>
  );
}

export default function EmptyStatePage() {
  const { width } = useWindowDimensions();
  const contentWidth = Math.min(Math.max(width - spacing.page * 2, 280), 620);
  const illustrationHeight = Math.min(contentWidth / ILLUSTRATION_RATIO, 430);
  const compact = width < 380;

  return (
    <FairyPage
      backgroundName="creamPaper"
      topSpace={Platform.OS === 'web' ? 28 : 18}
      bottomSpace={56}
      contentStyle={styles.pageContent}
      showsVerticalScrollIndicator
    >
      <View style={[styles.content, { maxWidth: 680 }]}>
        <View style={styles.header}>
          <FairyBackButton name="rollback2" width={44} height={44} style={styles.backButton} />
          <Text style={[styles.pageTitle, compact && styles.pageTitleCompact]}>回忆记录</Text>
          <HeaderDecoration />
        </View>

        <View style={styles.heroWrap}>
          <Image
            accessibilityLabel="打开的回忆册、羽毛笔与花朵插画"
            source={emptyDiarySource}
            resizeMode="contain"
            style={{ width: contentWidth, height: illustrationHeight }}
          />
        </View>

        <View style={styles.message}>
          <Text style={[styles.emptyTitle, compact && styles.emptyTitleCompact]}>这里还没有故事</Text>
          <View style={styles.subtitleRow}>
            <Ionicons name="heart-outline" size={17} color="#EFA09C" />
            <Text style={styles.subtitle}>写下第一段回忆，让童话开始生长</Text>
            <Ionicons name="heart-outline" size={17} color="#EFA09C" />
          </View>
        </View>

        <Pressable
          accessibilityRole="button"
          accessibilityLabel="去记录第一段回忆"
          onPress={() => router.push('/diary/editor')}
          style={({ pressed }) => [styles.action, compact && styles.actionCompact, pressed && styles.actionPressed]}
        >
          <View pointerEvents="none" style={styles.actionInset} />
          <View pointerEvents="none" style={styles.actionStars}>
            <Ionicons name="star" size={25} color="#F6C967" />
            <Ionicons name="star" size={15} color="#F6C967" />
          </View>
          <Text style={styles.actionText}>去记录</Text>
          <Ionicons name="heart-outline" size={25} color="#FFF8F1" style={styles.actionHeart} />
        </Pressable>
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: {
    alignItems: 'center',
  },
  content: {
    width: '100%',
    alignSelf: 'center',
    alignItems: 'center',
  },
  header: {
    width: '100%',
    minHeight: 60,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  backButton: {
    position: 'absolute',
    left: 0,
    zIndex: 2,
  },
  pageTitle: {
    color: '#664331',
    fontSize: 29,
    lineHeight: 38,
    fontWeight: '800',
    textAlign: 'center',
  },
  pageTitleCompact: {
    fontSize: 26,
  },
  headerDecoration: {
    position: 'absolute',
    top: 44,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 7,
  },
  dashedLine: {
    width: 34,
    borderTopWidth: 1.5,
    borderStyle: 'dashed',
    borderColor: '#EFB797',
    transform: [{ rotate: '-8deg' }],
  },
  shortLine: {
    width: 23,
    transform: [{ rotate: '10deg' }],
  },
  heroWrap: {
    width: '100%',
    marginTop: 74,
    alignItems: 'center',
    justifyContent: 'center',
  },
  message: {
    marginTop: 36,
    alignItems: 'center',
  },
  emptyTitle: {
    color: '#724832',
    fontSize: 32,
    lineHeight: 42,
    fontWeight: '800',
    textAlign: 'center',
  },
  emptyTitleCompact: {
    fontSize: 29,
  },
  subtitleRow: {
    marginTop: spacing.sm,
    paddingHorizontal: spacing.sm,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
  },
  subtitle: {
    flexShrink: 1,
    color: '#B47C69',
    fontSize: 17,
    lineHeight: 25,
    textAlign: 'center',
  },
  action: {
    width: '72%',
    maxWidth: 390,
    minWidth: 260,
    minHeight: 76,
    marginTop: 40,
    paddingHorizontal: 70,
    borderRadius: 38,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#EE8E8B',
    borderWidth: 1.5,
    borderColor: '#C86765',
    shadowColor: '#8C5146',
    shadowOffset: { width: 0, height: 7 },
    shadowOpacity: 0.18,
    shadowRadius: 9,
    elevation: 5,
  },
  actionCompact: {
    width: '82%',
    minWidth: 0,
  },
  actionInset: {
    ...StyleSheet.absoluteFillObject,
    margin: 6,
    borderWidth: 1.5,
    borderStyle: 'dashed',
    borderColor: 'rgba(255, 248, 241, 0.72)',
    borderRadius: 32,
  },
  actionStars: {
    position: 'absolute',
    left: 16,
    top: -12,
    flexDirection: 'row',
    alignItems: 'center',
  },
  actionText: {
    color: colors.white,
    fontSize: 25,
    lineHeight: 34,
    fontWeight: '800',
    textAlign: 'center',
  },
  actionHeart: {
    position: 'absolute',
    right: 26,
    bottom: 18,
    transform: [{ rotate: '-12deg' }],
  },
  actionPressed: {
    opacity: 0.9,
    transform: [{ scale: 0.98 }],
  },
});
