import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyHeader from '@/components/FairyHeader';
import FairyPage from '@/components/FairyPage';
import FairySection from '@/components/FairySection';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import useFairyStore from '@/store/useFairyStore';

const filters = [
  { key: 'all', label: '全部纪念日' },
  { key: 'heart', label: '恋爱' },
  { key: 'travel', label: '旅行' },
  { key: 'gift', label: '惊喜' },
];

function getCategory(item) {
  if (item.icon?.includes('airplane') || item.title?.includes('旅行')) return 'travel';
  if (item.icon?.includes('gift') || item.title?.includes('礼物') || item.title?.includes('生日')) return 'gift';
  return 'heart';
}

function formatDate(value) {
  return value?.replaceAll('-', '.') || '待设置日期';
}

export default function AnniversaryPage() {
  const router = useRouter();
  const anniversaries = useFairyStore((state) => state.anniversaries);
  const [filter, setFilter] = useState('all');
  const featured = anniversaries[0];
  const next = anniversaries[1] || featured;
  const visibleItems = useMemo(() => anniversaries.filter((item) => filter === 'all' || getCategory(item) === filter), [anniversaries, filter]);

  return (
    <FairyPage topSpace={18} bottomSpace={60} contentStyle={styles.pageContent} showsVerticalScrollIndicator>
      <View style={styles.content}>
        <FairyHeader showBack title="纪念日管理" right={`${anniversaries.length} 个章节`} />
        <View style={styles.intro}><Text style={styles.eyebrow}>把重要的日子装进童话纪念册</Text><Text style={styles.subtitle}>每一个被记住的日期，都会在未来变成温柔的路标。</Text></View>

        <FairyCard style={styles.featureCard} contentStyle={styles.featureContent}>
          <View style={styles.featureOrb} />
          <Text style={styles.featureKicker}>我们的纪念日</Text>
          <Text style={styles.featureTitle}>{featured?.title || '新的重要章节'}</Text>
          <View style={styles.daysRow}><Text style={styles.days}>{featured?.days || 0}</Text><Text style={styles.daysUnit}>天</Text></View>
          <Text style={styles.featureNote}>每一天，都是对彼此的心动。</Text>
        </FairyCard>

        <FairyCard style={styles.summaryCard}>
          <View style={styles.summaryHeading}><View style={styles.summaryIcon}><Ionicons name="calendar-outline" size={22} color={colors.primaryDeep} /></View><View style={styles.summaryCopy}><Text style={styles.summaryTitle}>下一章值得期待</Text><Text style={styles.summaryText}>{next?.title || '一起创造新的回忆'}</Text></View></View>
          <View style={styles.summaryDivider} />
          <Text style={styles.summaryDate}>{formatDate(next?.date)}</Text>
          <Text style={styles.summaryHint}>打开详情，可以切换纪念日、设置提醒并生成分享封面。</Text>
          <FairyButton title="查看倒计时详情" onPress={() => router.push('/anniversary/countdown')} leftContent={<Ionicons name="hourglass-outline" size={19} color={colors.white} />} />
        </FairyCard>

        <FairySection title="纪念日列表" description="查看、筛选和编辑所有重要章节" actionLabel="添加" onAction={() => router.push('/anniversary/edit')}>
          <View style={styles.filters}>
            {filters.map((item) => {
              const active = item.key === filter;
              return <Pressable key={item.key} accessibilityRole="button" accessibilityState={{ selected: active }} onPress={() => setFilter(item.key)} style={({ pressed }) => [styles.filterChip, active && styles.filterChipActive, pressed && styles.pressed]}><Text style={[styles.filterText, active && styles.filterTextActive]}>{item.label}</Text></Pressable>;
            })}
          </View>
          <View style={styles.list}>
            {visibleItems.map((item) => (
              <FairyCard key={item.id} padding={spacing.lg} style={styles.itemCard} onPress={() => router.push(`/anniversary/edit?id=${item.id}`)} accessibilityRole="button">
                <View style={styles.itemRow}><View style={styles.itemIcon}><Ionicons name={item.icon || 'heart-outline'} size={22} color={colors.primaryDeep} /></View><View style={styles.itemCopy}><Text style={styles.itemTitle}>{item.title}</Text><Text style={styles.itemDate}>{formatDate(item.date)}</Text></View><View style={styles.itemMeta}><Text style={styles.itemDays}>{item.days ? `${item.days} 天` : '新章节'}</Text><Ionicons name="chevron-forward" size={18} color={colors.textSoft} /></View></View>
              </FairyCard>
            ))}
            {!visibleItems.length ? <FairyCard style={styles.emptyCard}><Ionicons name="heart-circle-outline" size={34} color={colors.primaryDeep} /><Text style={styles.emptyTitle}>这个分类还没有纪念日</Text><Text style={styles.emptyText}>添加一个新章节，让重要日子从今天开始被记住。</Text></FairyCard> : null}
          </View>
        </FairySection>
        <FairyButton title="添加新的纪念日" onPress={() => router.push('/anniversary/edit')} leftContent={<Ionicons name="heart-outline" size={19} color={colors.white} />} />
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' },
  content: { width: '100%', maxWidth: 860 },
  intro: { alignItems: 'center', marginTop: spacing.md, marginBottom: spacing.xl },
  eyebrow: { color: colors.text, fontSize: 17, fontWeight: '900', textAlign: 'center' },
  subtitle: { color: colors.textSoft, lineHeight: 21, marginTop: spacing.sm, textAlign: 'center' },
  featureCard: { marginBottom: spacing.lg, backgroundColor: colors.cardPink, overflow: 'hidden' },
  featureContent: { minHeight: 236, justifyContent: 'center', alignItems: 'center', position: 'relative' },
  featureOrb: { position: 'absolute', width: 220, height: 220, right: -70, top: -70, borderRadius: 110, backgroundColor: '#FAD0D8', opacity: 0.7 },
  featureKicker: { color: colors.textSoft, fontSize: 12, fontWeight: '800' },
  featureTitle: { color: colors.text, fontSize: 20, fontWeight: '900', marginTop: 5 },
  daysRow: { flexDirection: 'row', alignItems: 'flex-end' },
  days: { color: colors.primaryDeep, fontSize: 52, lineHeight: 60, fontWeight: '900' },
  daysUnit: { color: colors.text, fontSize: 15, fontWeight: '900', marginBottom: 9, marginLeft: 4 },
  featureNote: { color: colors.textSoft, fontSize: 12 },
  summaryCard: { marginBottom: spacing.xxl, backgroundColor: colors.card },
  summaryHeading: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  summaryIcon: { width: 48, height: 48, borderRadius: 18, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink },
  summaryCopy: { flex: 1 },
  summaryTitle: { color: colors.text, fontSize: 16, fontWeight: '900' },
  summaryText: { color: colors.textSoft, fontSize: 12, marginTop: 4 },
  summaryDivider: { height: 1, backgroundColor: colors.border, marginVertical: spacing.lg },
  summaryDate: { color: colors.primaryDeep, fontSize: 25, fontWeight: '900' },
  summaryHint: { color: colors.textSoft, lineHeight: 20, marginTop: spacing.sm, marginBottom: spacing.lg },
  filters: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginBottom: spacing.lg },
  filterChip: { minHeight: 38, paddingHorizontal: spacing.lg, borderRadius: 18, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border, backgroundColor: colors.card },
  filterChipActive: { borderColor: colors.primaryDeep, backgroundColor: colors.cardPink },
  filterText: { color: colors.textSoft, fontSize: 12, fontWeight: '800' },
  filterTextActive: { color: colors.primaryDeep },
  list: { marginBottom: spacing.lg },
  itemCard: { marginBottom: spacing.md },
  itemRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  itemIcon: { width: 46, height: 46, borderRadius: 17, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.cardPink },
  itemCopy: { flex: 1, minWidth: 0 },
  itemTitle: { color: colors.text, fontSize: 15, fontWeight: '900' },
  itemDate: { color: colors.textSoft, fontSize: 12, marginTop: 4 },
  itemMeta: { flexDirection: 'row', alignItems: 'center', gap: spacing.xs },
  itemDays: { color: colors.primaryDeep, fontSize: 12, fontWeight: '900' },
  emptyCard: { alignItems: 'center' },
  emptyTitle: { color: colors.text, fontWeight: '900', marginTop: spacing.md },
  emptyText: { color: colors.textSoft, lineHeight: 20, textAlign: 'center', marginTop: spacing.sm },
  pressed: { opacity: 0.7 },
});
