import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyEmptyState from '@/components/FairyEmptyState';
import FairyHeader from '@/components/FairyHeader';
import FairyImage from '@/components/FairyImage';
import FairyPage from '@/components/FairyPage';
import FairyToast from '@/components/FairyToast';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import useFairyStore from '@/store/useFairyStore';

export default function CoupleActivityDetailPage() {
  const router = useRouter();
  const timeline = useFairyStore((state) => state.timeline);
  const records = useFairyStore((state) => state.records);
  const activity = timeline[0];
  const relatedRecord = records[0];
  const [liked, setLiked] = useState(false);
  const [saved, setSaved] = useState(false);
  const [toast, setToast] = useState(null);
  const header = <FairyHeader showBack title="故事详情" right={<Pressable accessibilityRole="button" onPress={() => setToast({ tone: 'info', message: '更多故事管理功能会在后续业务阶段接入。' })} style={({ pressed }) => [styles.headerAction, pressed && styles.pressed]}><Ionicons name="ellipsis-horizontal" size={23} color={colors.text} /></Pressable>} />;

  if (!activity) {
    return (
      <FairyPage backgroundName="creamPaper" header={header} topSpace={28} contentStyle={styles.pageContent}>
        <View style={styles.content}><FairyEmptyState compact icon="heart-outline" title="还没有故事节点" description="写一篇日记或上传一组照片，情侣空间就会长出新的章节。" /></View>
        <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
      </FairyPage>
    );
  }

  return (
    <FairyPage backgroundName="creamPaper" header={header} topSpace={28} bottomSpace={60} contentStyle={styles.pageContent} showsVerticalScrollIndicator>
      <View style={styles.content}>
        <FairyCard style={styles.storyCard} padding={spacing.xl}>
          <View style={styles.storyTag}><Ionicons name={activity.icon || 'book-outline'} size={18} color={colors.primaryDeep} /><Text style={styles.storyTagText}>{activity.tag || '日记'}</Text></View>
          <Text style={styles.storyTitle}>{activity.title || '雨后散步'}</Text>
          <View style={styles.metaRow}><Ionicons name="calendar-outline" size={17} color={colors.accent} /><Text style={styles.metaText}>{relatedRecord?.date || activity.time}</Text><View style={styles.metaDivider} /><Ionicons name="rainy-outline" size={18} color="#91AFC5" /><Text style={styles.metaText}>多云</Text></View>
          <View style={styles.storyDivider} />
          <Text style={styles.storyText}>{activity.description || relatedRecord?.content || '我们踩着还没干透的小路慢慢走，路灯把影子拉得很长。'}</Text>
          <Text style={styles.storyText}>这一页，想和你一起收藏。</Text>
        </FairyCard>

        <Text style={styles.sectionTitle}>相关回忆</Text>
        <FairyCard style={styles.memoryCard} padding={spacing.md}>
          <FairyImage name="homeCover" height={260} radius={22} framed={false} resizeMode="cover" />
          <View style={styles.memoryOverlay}><Text style={styles.memoryTitle}>{relatedRecord?.title || '一起散步的傍晚'}</Text><Text style={styles.memoryText}>属于我们两个人的温柔片段</Text></View>
        </FairyCard>

        <FairyCard style={styles.statsCard} padding={0}>
          <StatButton icon={liked ? 'heart' : 'heart-outline'} label="喜欢" value={liked ? 27 : 26} active={liked} onPress={() => setLiked((value) => !value)} />
          <View style={styles.statDivider} />
          <StatButton icon={saved ? 'star' : 'star-outline'} label="收藏" value={saved ? 19 : 18} active={saved} onPress={() => setSaved((value) => !value)} />
          <View style={styles.statDivider} />
          <StatButton icon="chatbubble-ellipses-outline" label="评论" value={7} onPress={() => router.push('/comments')} />
        </FairyCard>

        <FairyCard style={styles.partnerCard} padding={spacing.lg}>
          <View style={styles.partnerAvatar}><Text style={styles.partnerAvatarText}>舟</Text></View>
          <View style={styles.partnerCopy}><View style={styles.partnerNameRow}><Text style={styles.partnerName}>阿舟</Text><View style={styles.partnerTag}><Text style={styles.partnerTagText}>TA</Text></View></View><Text style={styles.partnerText}>和你一起走的路，都很喜欢。</Text><Text style={styles.partnerTime}>今天 21:36</Text></View>
          <Ionicons name="heart" size={26} color={colors.primary} />
        </FairyCard>

        <View style={styles.actions}>
          <FairyButton title="去评论这一章" onPress={() => router.push('/comments')} style={styles.actionButton} leftContent={<Ionicons name="chatbubble-outline" size={19} color={colors.white} />} />
          <FairyButton title="生成漫画" variant="secondary" onPress={() => router.push('/ai/text-to-comic')} style={styles.actionButton} />
        </View>
        <FairyButton title="返回情侣空间" variant="secondary" onPress={() => router.replace('/(tabs)/couple')} style={styles.backButton} />
      </View>
      <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

function StatButton({ icon, label, value, active, onPress }) {
  return <Pressable accessibilityRole="button" onPress={onPress} style={({ pressed }) => [styles.statButton, pressed && styles.pressed]}><Ionicons name={icon} size={25} color={active ? colors.primaryDeep : colors.accent} /><View><Text style={styles.statLabel}>{label}</Text><Text style={styles.statValue}>{value}</Text></View></Pressable>;
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' }, content: { width: '100%', maxWidth: 760 }, headerAction: { width: 44, height: 44, alignItems: 'center', justifyContent: 'center' }, pressed: { opacity: 0.65 },
  storyCard: { marginBottom: spacing.xl, backgroundColor: 'rgba(255,249,244,0.96)' }, storyTag: { alignSelf: 'flex-start', flexDirection: 'row', alignItems: 'center', gap: spacing.sm, paddingHorizontal: spacing.md, paddingVertical: 7, borderRadius: 14, backgroundColor: colors.cardPink }, storyTagText: { color: colors.primaryDeep, fontSize: 12, fontWeight: '900' }, storyTitle: { color: colors.text, fontSize: 28, fontWeight: '900', marginTop: spacing.xl },
  metaRow: { flexDirection: 'row', alignItems: 'center', flexWrap: 'wrap', gap: spacing.sm, marginTop: spacing.lg }, metaText: { color: colors.textSoft, fontSize: 12, fontWeight: '800' }, metaDivider: { width: 1, height: 18, backgroundColor: colors.border, marginHorizontal: spacing.sm }, storyDivider: { height: 1, backgroundColor: colors.primary, marginVertical: spacing.lg }, storyText: { color: colors.text, fontSize: 15, lineHeight: 26, marginBottom: spacing.md },
  sectionTitle: { color: colors.text, fontSize: 20, fontWeight: '900', marginBottom: spacing.md }, memoryCard: { position: 'relative', marginBottom: spacing.lg, overflow: 'hidden' }, memoryOverlay: { position: 'absolute', left: spacing.xl, right: spacing.xl, bottom: spacing.xl, padding: spacing.md, borderRadius: 18, backgroundColor: 'rgba(255,249,244,0.9)' }, memoryTitle: { color: colors.text, fontSize: 17, fontWeight: '900' }, memoryText: { color: colors.textSoft, fontSize: 11, marginTop: 3 },
  statsCard: { flexDirection: 'row', alignItems: 'stretch', marginBottom: spacing.lg, backgroundColor: colors.cardPink }, statButton: { flex: 1, minHeight: 82, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm }, statDivider: { width: 1, marginVertical: spacing.md, backgroundColor: colors.border }, statLabel: { color: colors.text, fontSize: 12, fontWeight: '900' }, statValue: { color: colors.textSoft, fontSize: 11, marginTop: 2 },
  partnerCard: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, marginBottom: spacing.lg }, partnerAvatar: { width: 52, height: 52, borderRadius: 21, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink }, partnerAvatarText: { color: colors.primaryDeep, fontSize: 18, fontWeight: '900' }, partnerCopy: { flex: 1 }, partnerNameRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm }, partnerName: { color: colors.text, fontSize: 15, fontWeight: '900' }, partnerTag: { paddingHorizontal: spacing.sm, paddingVertical: 2, borderRadius: 9, backgroundColor: '#FFF0C9' }, partnerTagText: { color: colors.gold, fontSize: 9, fontWeight: '900' }, partnerText: { color: colors.text, marginTop: 4 }, partnerTime: { color: colors.textSoft, fontSize: 10, marginTop: 4 },
  actions: { flexDirection: 'row', gap: spacing.md }, actionButton: { flex: 1 }, backButton: { marginTop: spacing.md },
});
