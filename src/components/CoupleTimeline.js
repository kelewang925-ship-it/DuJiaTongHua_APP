import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../theme/colors';
import spacing from '../theme/spacing';
import shadows from '../theme/shadows';
import FairyTag from './FairyTag';

const nodeDecorations = [
  { icon: 'heart', color: colors.primaryDeep, bg: colors.cardPink },
  { icon: 'sparkles', color: colors.gold, bg: '#FFF5DF' },
  { icon: 'flower-outline', color: colors.accent, bg: '#FFF7EF' },
  { icon: 'star', color: colors.gold, bg: colors.cardPink },
];

function StoryNode({ item, index, isLast }) {
  const decor = nodeDecorations[index % nodeDecorations.length];
  const isRightLean = index % 2 === 1;

  return (
    <View style={styles.row}>
      <View style={styles.railWrap}>
        <View style={[styles.nodeHalo, { backgroundColor: decor.bg }]}> 
          <View style={styles.nodeInner}>
            <Ionicons name={item.icon || decor.icon} size={18} color={decor.color} />
          </View>
        </View>
        {!isLast ? (
          <View style={styles.curveLineWrap}>
            <View style={[styles.curveLine, isRightLean && styles.curveLineReverse]} />
            <View style={[styles.curveDot, isRightLean && styles.curveDotReverse]} />
          </View>
        ) : null}
      </View>

      <View style={[styles.card, isRightLean && styles.cardLeanRight]}>
        <View style={[styles.tape, isRightLean && styles.tapeRight]} />
        <View style={styles.chapterRow}>
          <Text style={styles.chapter}>第 {String(index + 1).padStart(2, '0')} 章</Text>
          <FairyTag tone={item.tag === 'AI' ? 'gold' : 'default'}>{item.tag}</FairyTag>
        </View>
        <Text style={styles.title}>{item.title}</Text>
        <Text style={styles.time}>{item.time}</Text>
        <Text style={styles.description}>{item.description}</Text>
        <View style={styles.footerRow}>
          <View style={styles.miniSticker}>
            <Ionicons name="heart-outline" size={13} color={colors.primaryDeep} />
            <Text style={styles.miniText}>已收藏</Text>
          </View>
          <View style={styles.miniSticker}>
            <Ionicons name="chatbubble-ellipses-outline" size={13} color={colors.accent} />
            <Text style={styles.miniText}>留言</Text>
          </View>
        </View>
      </View>
    </View>
  );
}

export default function CoupleTimeline({ items = [] }) {
  if (!items.length) {
    return (
      <View style={styles.emptyBox}>
        <Ionicons name="heart-outline" size={28} color={colors.accent} />
        <Text style={styles.emptyTitle}>双人故事还在等待开始</Text>
        <Text style={styles.emptyText}>写一篇日记、上传一组照片，这里就会长出新的章节。</Text>
      </View>
    );
  }

  return (
    <View style={styles.timelineWrap}>
      {items.map((item, index) => (
        <StoryNode key={item.id} item={item} index={index} isLast={index === items.length - 1} />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  timelineWrap: {
    paddingTop: spacing.sm,
    paddingBottom: spacing.xl,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'stretch',
    minHeight: 160,
  },
  railWrap: {
    width: 54,
    alignItems: 'center',
  },
  nodeHalo: {
    width: 44,
    height: 44,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: colors.border,
    zIndex: 2,
    transform: [{ rotate: '-8deg' }],
    ...shadows.card,
  },
  nodeInner: {
    width: 30,
    height: 30,
    borderRadius: 12,
    backgroundColor: colors.card,
    alignItems: 'center',
    justifyContent: 'center',
  },
  curveLineWrap: {
    flex: 1,
    width: 30,
    alignItems: 'center',
    paddingVertical: 4,
  },
  curveLine: {
    flex: 1,
    width: 2,
    borderRadius: 4,
    backgroundColor: '#EAD6D1',
    transform: [{ rotate: '4deg' }],
  },
  curveLineReverse: {
    transform: [{ rotate: '-4deg' }],
  },
  curveDot: {
    position: 'absolute',
    top: '42%',
    left: 7,
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: colors.primary,
    opacity: 0.72,
  },
  curveDotReverse: {
    left: undefined,
    right: 7,
    backgroundColor: colors.gold,
  },
  card: {
    flex: 1,
    minHeight: 132,
    backgroundColor: colors.card,
    borderRadius: 26,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.lg,
    marginBottom: spacing.lg,
    transform: [{ rotate: '-0.8deg' }],
    ...shadows.card,
  },
  cardLeanRight: {
    backgroundColor: '#FFF7EF',
    transform: [{ rotate: '0.9deg' }, { translateX: 4 }],
  },
  tape: {
    position: 'absolute',
    top: -8,
    left: 26,
    width: 48,
    height: 16,
    borderRadius: 6,
    backgroundColor: '#F7E8D5',
    opacity: 0.9,
    transform: [{ rotate: '-8deg' }],
  },
  tapeRight: {
    left: undefined,
    right: 30,
    backgroundColor: colors.secondary,
    transform: [{ rotate: '8deg' }],
  },
  chapterRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: spacing.sm,
  },
  chapter: {
    color: colors.accent,
    fontSize: 12,
    fontWeight: '900',
  },
  title: {
    color: colors.text,
    fontSize: 17,
    fontWeight: '900',
    lineHeight: 24,
  },
  time: {
    color: colors.textSoft,
    fontSize: 12,
    marginTop: spacing.xs,
  },
  description: {
    color: colors.textSoft,
    fontSize: 13,
    lineHeight: 21,
    marginTop: spacing.sm,
  },
  footerRow: {
    flexDirection: 'row',
    gap: spacing.sm,
    marginTop: spacing.md,
  },
  miniSticker: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    paddingHorizontal: spacing.sm,
    paddingVertical: 5,
    borderRadius: 14,
    backgroundColor: colors.cardPink,
    borderWidth: 1,
    borderColor: colors.border,
  },
  miniText: {
    color: colors.textSoft,
    fontSize: 11,
    fontWeight: '700',
  },
  emptyBox: {
    alignItems: 'center',
    borderRadius: 28,
    backgroundColor: colors.cardPink,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.xxl,
  },
  emptyTitle: {
    color: colors.text,
    fontSize: 17,
    fontWeight: '900',
    marginTop: spacing.md,
  },
  emptyText: {
    color: colors.textSoft,
    textAlign: 'center',
    lineHeight: 21,
    marginTop: spacing.sm,
  },
});
