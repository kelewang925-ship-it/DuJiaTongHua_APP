import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../theme/colors';
import spacing from '../theme/spacing';
import FairyTag from './FairyTag';
import FairyCard from './FairyCard';
import { richTextToPlainText } from '../utils/richText';

const typeTone = {
  日记: {
    background: colors.card,
    tape: '#F7E8D5',
    iconBg: colors.cardPink,
    sticker: 'book-outline',
  },
  照片: {
    background: '#FFF7EF',
    tape: colors.secondary,
    iconBg: '#F7E8D5',
    sticker: 'images-outline',
  },
  漫画: {
    background: '#FFF4F1',
    tape: '#F8D9DF',
    iconBg: '#FFF5DF',
    sticker: 'sparkles-outline',
  },
  视频: {
    background: '#FFF4F1',
    tape: '#F7E8D5',
    iconBg: '#FFF5DF',
    sticker: 'film-outline',
  },
};

function Tape({ align = 'left', tone }) {
  return <View style={[styles.tape, align === 'right' && styles.tapeRight, { backgroundColor: tone }]} />;
}

function MemoryWallCard({ item, index, onPress }) {
  const tone = typeTone[item.type] || typeTone['日记'];
  const isWide = index % 5 === 0;
  const isTall = item.type === '照片' || index % 4 === 2;
  const rotate = index % 2 === 0 ? '-1.4deg' : '1.2deg';

  return (
    <FairyCard
      onPress={() => onPress?.(item)}
      padding={0}
      radius={24}
      backgroundColor="transparent"
      borderWidth={0}
      shadowStyle={[
        styles.card,
        isWide ? styles.wideCard : styles.halfCard,
        { transform: [{ rotate }] },
      ]}
      contentStyle={[
        styles.cardContent,
        isWide ? styles.wideCardContent : styles.halfCardContent,
        isTall && styles.tallCardContent,
        { backgroundColor: tone.background },
      ]}
    >
      <Tape align={index % 2 === 0 ? 'left' : 'right'} tone={tone.tape} />
      <View style={styles.cardHeader}>
        <View style={[styles.iconWrap, { backgroundColor: tone.iconBg }]}> 
          <Ionicons name={item.icon || tone.sticker} size={18} color={colors.accent} />
        </View>
        <FairyTag tone={item.type === '漫画' || item.type === '视频' ? 'gold' : 'default'}>{item.type}</FairyTag>
      </View>

      {item.type === '照片' ? (
        <View style={styles.polaroid}>
          <View style={styles.photoMock}>
            <Ionicons name="image-outline" size={30} color={colors.accent} />
          </View>
          <Text style={styles.photoCount}>{item.photoCount || 3} 张照片</Text>
        </View>
      ) : item.type === '漫画' || item.type === '视频' ? (
        <View style={styles.magicMock}>
          <Ionicons name={item.type === '视频' ? 'play-circle-outline' : 'sparkles-outline'} size={34} color={colors.gold} />
          <Text style={styles.magicText}>{item.type === '视频' ? '回忆放映机' : '童话漫画'}</Text>
        </View>
      ) : null}

      <Text style={styles.title} numberOfLines={2}>{item.title}</Text>
      <Text style={styles.content} numberOfLines={isTall ? 4 : 3}>{richTextToPlainText(item.content)}</Text>
      <View style={styles.footer}>
        <Text style={styles.date}>{item.date}</Text>
        <View style={styles.likeRow}>
          <Ionicons name="heart-outline" size={14} color={colors.primaryDeep} />
          <Text style={styles.likeText}>{item.likes || 0}</Text>
        </View>
      </View>
    </FairyCard>
  );
}

export default function MemoryWall({ records, onPress }) {
  if (!records?.length) return null;

  return (
    <View style={styles.wall}>
      {records.map((item, index) => (
        <MemoryWallCard key={item.id} item={item} index={index} onPress={onPress} />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  wall: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.md,
    paddingTop: spacing.xs,
    paddingBottom: spacing.xl,
  },
  card: {
    marginBottom: spacing.sm,
  },
  cardContent: {
    borderRadius: 24,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.lg,
    overflow: 'visible',
  },
  halfCard: {
    width: '47.8%',
  },
  halfCardContent: {
    minHeight: 210,
  },
  wideCard: {
    width: '100%',
  },
  wideCardContent: {
    minHeight: 188,
  },
  tallCardContent: {
    minHeight: 248,
  },
  tape: {
    position: 'absolute',
    top: -9,
    left: 22,
    width: 52,
    height: 18,
    borderRadius: 6,
    opacity: 0.86,
    transform: [{ rotate: '-8deg' }],
  },
  tapeRight: {
    left: undefined,
    right: 22,
    transform: [{ rotate: '8deg' }],
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: spacing.md,
  },
  iconWrap: {
    width: 38,
    height: 38,
    borderRadius: 15,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: colors.border,
  },
  polaroid: {
    backgroundColor: colors.white,
    borderRadius: 18,
    padding: spacing.sm,
    borderWidth: 1,
    borderColor: colors.border,
    marginBottom: spacing.md,
    transform: [{ rotate: '-1deg' }],
  },
  photoMock: {
    height: 96,
    borderRadius: 14,
    backgroundColor: colors.cardPink,
    alignItems: 'center',
    justifyContent: 'center',
  },
  photoCount: {
    color: colors.textSoft,
    fontSize: 11,
    marginTop: spacing.xs,
    textAlign: 'center',
  },
  magicMock: {
    height: 84,
    borderRadius: 18,
    backgroundColor: '#FFF5DF',
    borderWidth: 1,
    borderColor: colors.border,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.md,
  },
  magicText: {
    color: colors.accent,
    fontSize: 11,
    fontWeight: '800',
    marginTop: spacing.xs,
  },
  title: {
    color: colors.text,
    fontSize: 16,
    fontWeight: '900',
    lineHeight: 22,
  },
  content: {
    color: colors.textSoft,
    fontSize: 12,
    lineHeight: 19,
    marginTop: spacing.sm,
  },
  footer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginTop: spacing.md,
  },
  date: {
    color: colors.textSoft,
    fontSize: 11,
  },
  likeRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 3,
  },
  likeText: {
    color: colors.textSoft,
    fontSize: 11,
  },
});
