import { View, Text, StyleSheet, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import FairyPage from '../../src/components/FairyPage';
import FairyHeader from '../../src/components/FairyHeader';
import FairyCard from '../../src/components/FairyCard';
import FairyButton from '../../src/components/FairyButton';
import FairyTag from '../../src/components/FairyTag';
import FairyEmptyState from '../../src/components/FairyEmptyState';
import useFairyStore from '../../src/store/useFairyStore';

export default function CoupleActivityDetailPage() {
  const timeline = useFairyStore((state) => state.timeline);
  const records = useFairyStore((state) => state.records);
  const creations = useFairyStore((state) => state.creations);
  const activity = timeline[0];
  const relatedRecord = records[0];
  const relatedCreation = creations[0];

  if (!activity) {
    return (
      <FairyPage>
        <FairyHeader showBack eyebrow="情侣空间" title="情侣动态详情" subtitle="这里会展示某一章双人故事的细节。" />
        <FairyEmptyState
          compact
          icon="heart-outline"
          title="还没有故事节点"
          description="写一篇日记或上传一组照片，情侣空间就会长出新的章节。"
        />
      </FairyPage>
    );
  }

  return (
    <FairyPage>
      <FairyHeader
        showBack
        eyebrow="故事节点"
        title="情侣动态详情"
        subtitle="查看这一章背后的记录、互动和可以继续创作的入口。"
      />

      <FairyCard style={styles.heroCard}>
        <View style={styles.chapterBadge}>
          <Ionicons name={activity.icon || 'heart-outline'} size={24} color={colors.accent} />
        </View>
        <FairyTag tone={activity.tag === 'AI' ? 'gold' : 'default'}>{activity.tag}</FairyTag>
        <Text style={styles.title}>{activity.title}</Text>
        <Text style={styles.time}>{activity.time}</Text>
        <Text style={styles.description}>{activity.description}</Text>
      </FairyCard>

      <Text style={styles.section}>关联内容</Text>
      <FairyCard style={styles.relatedCard}>
        <View style={styles.relatedIcon}>
          <Ionicons name={relatedRecord?.icon || 'book-outline'} size={22} color={colors.primaryDeep} />
        </View>
        <View style={{ flex: 1 }}>
          <Text style={styles.relatedType}>{relatedRecord?.type || '记录'}</Text>
          <Text style={styles.relatedTitle}>{relatedRecord?.title || '还没有关联记录'}</Text>
          <Text style={styles.relatedText} numberOfLines={2}>{relatedRecord?.content || '新的故事正在等待被写下。'}</Text>
        </View>
      </FairyCard>

      {relatedCreation ? (
        <FairyCard style={styles.relatedCard}>
          <View style={styles.relatedIconGold}>
            <Ionicons name={relatedCreation.icon || 'sparkles-outline'} size={22} color={colors.gold} />
          </View>
          <View style={{ flex: 1 }}>
            <Text style={styles.relatedType}>AI作品</Text>
            <Text style={styles.relatedTitle}>{relatedCreation.title}</Text>
            <Text style={styles.relatedText}>{relatedCreation.status}</Text>
          </View>
        </FairyCard>
      ) : null}

      <Text style={styles.section}>互动</Text>
      <View style={styles.actionGrid}>
        <Pressable style={styles.actionCard}>
          <Ionicons name="heart-outline" size={22} color={colors.primaryDeep} />
          <Text style={styles.actionText}>收藏这一章</Text>
        </Pressable>
        <Pressable style={styles.actionCard} onPress={() => router.push('/comments')}>
          <Ionicons name="chatbubble-ellipses-outline" size={22} color={colors.accent} />
          <Text style={styles.actionText}>查看评论</Text>
        </Pressable>
      </View>

      <FairyButton title="去评论这一章" onPress={() => router.push('/comments')} />
      <FairyButton title="用这一章生成漫画" variant="secondary" style={styles.secondary} onPress={() => router.push('/ai/text-to-comic')} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  heroCard: { alignItems: 'center', backgroundColor: colors.cardPink, marginBottom: spacing.xl },
  chapterBadge: { width: 66, height: 66, borderRadius: 26, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, alignItems: 'center', justifyContent: 'center', marginBottom: spacing.md, transform: [{ rotate: '-8deg' }] },
  title: { color: colors.text, fontSize: 23, fontWeight: '900', textAlign: 'center', marginTop: spacing.md, lineHeight: 30 },
  time: { color: colors.textSoft, marginTop: spacing.sm, fontSize: 12 },
  description: { color: colors.textSoft, marginTop: spacing.md, lineHeight: 22, textAlign: 'center' },
  section: { color: colors.text, fontSize: 20, fontWeight: '900', marginBottom: spacing.md },
  relatedCard: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, marginBottom: spacing.md, padding: spacing.md },
  relatedIcon: { width: 46, height: 46, borderRadius: 18, backgroundColor: colors.cardPink, borderWidth: 1, borderColor: colors.border, alignItems: 'center', justifyContent: 'center' },
  relatedIconGold: { width: 46, height: 46, borderRadius: 18, backgroundColor: '#FFF5DF', borderWidth: 1, borderColor: colors.border, alignItems: 'center', justifyContent: 'center' },
  relatedType: { color: colors.accent, fontSize: 12, fontWeight: '900' },
  relatedTitle: { color: colors.text, fontSize: 15, fontWeight: '900', marginTop: 3 },
  relatedText: { color: colors.textSoft, fontSize: 12, lineHeight: 18, marginTop: 4 },
  actionGrid: { flexDirection: 'row', gap: spacing.md, marginBottom: spacing.xl },
  actionCard: { flex: 1, minHeight: 84, borderRadius: 24, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, alignItems: 'center', justifyContent: 'center', gap: spacing.sm },
  actionText: { color: colors.text, fontWeight: '800', fontSize: 13 },
  secondary: { marginTop: spacing.md },
});
