import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import FairyCard from '@/components/FairyCard';
import FairyEmptyState from '@/components/FairyEmptyState';
import FairyHeader from '@/components/FairyHeader';
import FairyImage from '@/components/FairyImage';
import FairyPage from '@/components/FairyPage';
import FairyTag from '@/components/FairyTag';
import FairyToast from '@/components/FairyToast';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import useFairyStore from '@/store/useFairyStore';

const filters = ['全部', '漫画', '视频', '生成中'];

export default function AiCreationHistoryPage() {
  const { width } = useWindowDimensions();
  const creations = useFairyStore((state) => state.creations);
  const selectAiJob = useFairyStore((state) => state.selectAiJob);
  const [filter, setFilter] = useState(filters[0]);
  const [toast, setToast] = useState(null);
  const compact = width < 620;

  const filtered = useMemo(() => creations.filter((item) => {
    if (filter === '全部') return true;
    if (filter === '生成中') return item.progress < 100;
    return item.type === filter;
  }), [creations, filter]);

  const openCreation = (item) => {
    selectAiJob(item.id);
    if (item.progress < 100) router.push('/ai/progress');
    else router.push(item.type === '视频' ? '/ai/video-preview' : '/ai/comic-result');
  };

  return (
    <FairyPage backgroundName="creamPaper" header={<FairyHeader showBack title="创作历史" right={<Ionicons name="options-outline" size={23} color={colors.textSoft} />} />} topSpace={18} bottomSpace={64}>
      <View style={styles.content}>
        <Text style={styles.subtitle}>作品会自动收藏在这里</Text>
        <View style={styles.filters}>
          {filters.map((item) => (
            <Pressable key={item} onPress={() => setFilter(item)} style={({ pressed }) => [styles.filter, filter === item && styles.filterActive, pressed && styles.pressed]}>
              <Text style={[styles.filterText, filter === item && styles.filterTextActive]}>{item}</Text>
            </Pressable>
          ))}
        </View>

        {filtered.length ? (
          <View style={styles.list}>
            {filtered.map((item, index) => {
              const done = item.progress >= 100;
              const imageName = item.type === '视频' ? 'homeCover' : index % 2 === 0 ? 'aiComicTriptych' : 'workshopCover';
              return (
                <FairyCard key={item.id} style={[styles.item, compact && styles.itemCompact]}>
                  <View style={[styles.thumbWrap, compact && styles.thumbWrapCompact]}>
                    <FairyImage name={imageName} height={170} radius={20} framed={false} />
                    {item.type === '视频' ? <View style={styles.playBadge}><Ionicons name="play" size={22} color={colors.white} /></View> : null}
                  </View>
                  <View style={styles.body}>
                    <View style={styles.meta}>
                      <FairyTag tone={item.type === '视频' ? 'gold' : 'default'}>{item.type}</FairyTag>
                      <FairyTag tone={done ? 'gold' : 'default'}>{done ? '已完成' : '生成中'}</FairyTag>
                    </View>
                    <Text style={styles.title}>{item.title}</Text>
                    <Text style={styles.text}>{item.source || '童话工坊'} · {item.styleName || '默认风格'}</Text>
                    <View style={styles.dateRow}><Ionicons name="time-outline" size={14} color={colors.textSoft} /><Text style={styles.date}>{formatCreationTime(item.createdAt)}</Text></View>
                    {!done ? <View style={styles.progressTrack}><View style={[styles.progressFill, { width: `${item.progress || 0}%` }]} /></View> : null}
                    <View style={styles.actions}>
                      <Pressable onPress={() => openCreation(item)} style={({ pressed }) => [styles.primaryAction, pressed && styles.pressed]}><Ionicons name={done ? 'eye-outline' : 'sparkles-outline'} size={17} color={colors.primaryDeep} /><Text style={styles.primaryActionText}>{done ? '查看作品' : '查看进度'}</Text></Pressable>
                      <Pressable onPress={() => setToast({ message: `《${item.title}》分享卡片已准备好`, tone: 'success' })} style={({ pressed }) => [styles.secondaryAction, pressed && styles.pressed]}><Ionicons name="share-social-outline" size={17} color={colors.textSoft} /><Text style={styles.secondaryActionText}>分享</Text></Pressable>
                    </View>
                  </View>
                </FairyCard>
              );
            })}
          </View>
        ) : (
          <FairyEmptyState imageName="emptyAiHistory" title={`还没有${filter === '全部' ? '' : filter}作品`} description="第一段回忆还在等待被施展魔法。可以先写一篇日记，或挑选一组照片。" actionTitle="去童话工坊" onAction={() => router.push('/(tabs)/workshop')} />
        )}

        <View style={styles.footer}><Ionicons name="color-wand-outline" size={18} color={colors.gold} /><Text style={styles.footerText}>每一次创作，都是我们独家童话的一页</Text></View>
      </View>
      <FairyToast visible={Boolean(toast)} message={toast?.message} tone={toast?.tone} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

function formatCreationTime(value) {
  if (!value) return '刚刚';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '刚刚';
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
}

const styles = StyleSheet.create({
  content: { width: '100%', maxWidth: 760, alignSelf: 'center' },
  subtitle: { marginBottom: spacing.lg, textAlign: 'center', color: colors.textSoft, fontSize: 14, fontWeight: '700' },
  filters: { flexDirection: 'row', padding: spacing.xs, marginBottom: spacing.xl, borderRadius: 20, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.card },
  filter: { flex: 1, minHeight: 44, alignItems: 'center', justifyContent: 'center', borderRadius: 16 },
  filterActive: { backgroundColor: colors.primary },
  filterText: { color: colors.text, fontSize: 13, fontWeight: '800' },
  filterTextActive: { color: colors.white },
  list: { gap: spacing.lg },
  item: { flexDirection: 'row', alignItems: 'stretch', gap: spacing.lg, padding: spacing.md },
  itemCompact: { flexDirection: 'column' },
  thumbWrap: { position: 'relative', width: '39%', minWidth: 180 },
  thumbWrapCompact: { width: '100%', minWidth: 0 },
  playBadge: { position: 'absolute', left: '50%', top: '50%', marginLeft: -23, marginTop: -23, width: 46, height: 46, borderRadius: 23, alignItems: 'center', justifyContent: 'center', backgroundColor: 'rgba(82,52,47,0.72)' },
  body: { flex: 1, minWidth: 0 },
  meta: { flexDirection: 'row', alignItems: 'center', flexWrap: 'wrap', gap: spacing.sm },
  title: { marginTop: spacing.md, color: colors.text, fontWeight: '900', fontSize: 18 },
  text: { marginTop: spacing.xs, color: colors.textSoft, fontSize: 12, lineHeight: 18 },
  dateRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.xs, marginTop: spacing.md },
  date: { color: colors.textSoft, fontSize: 10 },
  progressTrack: { height: 6, marginTop: spacing.md, overflow: 'hidden', borderRadius: 3, backgroundColor: colors.secondary },
  progressFill: { height: 6, borderRadius: 3, backgroundColor: colors.primaryDeep },
  actions: { flexDirection: 'row', gap: spacing.sm, marginTop: spacing.md },
  primaryAction: { flex: 1, minHeight: 40, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.xs, borderRadius: 15, borderWidth: 1, borderColor: colors.primary, backgroundColor: colors.cardPink },
  primaryActionText: { color: colors.primaryDeep, fontSize: 11, fontWeight: '900' },
  secondaryAction: { minWidth: 82, minHeight: 40, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.xs, borderRadius: 15, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.card },
  secondaryActionText: { color: colors.textSoft, fontSize: 11, fontWeight: '800' },
  footer: { marginTop: spacing.xl, minHeight: 56, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, borderRadius: 20, backgroundColor: colors.cardPink },
  footerText: { color: colors.textSoft, fontSize: 11, fontWeight: '700' },
  pressed: { opacity: 0.68 },
});
