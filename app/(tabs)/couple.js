import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import CoupleTimeline from '@/components/CoupleTimeline';
import FairyCard from '@/components/FairyCard';
import FairyEmptyState from '@/components/FairyEmptyState';
import FairyImage from '@/components/FairyImage';
import FairyPage from '@/components/FairyPage';
import FairyRequestState from '@/components/FairyRequestState';
import FairySticker from '@/components/FairySticker';
import FairyTag from '@/components/FairyTag';
import FairyToast from '@/components/FairyToast';
import useFairyStore from '@/store/useFairyStore';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import { getApiMode } from '@/api/client';

function daysTogether(value) {
  if (!value) return null;
  const start = new Date(`${value}T00:00:00`);
  if (Number.isNaN(start.getTime()) || start.getTime() > Date.now()) return null;
  return Math.floor((Date.now() - start.getTime()) / 86400000) + 1;
}

export default function CouplePage() {
  const { width } = useWindowDimensions();
  const compact = width < 680;
  const isReal = getApiMode() === 'real';
  const coupleState = useFairyStore((state) => state.couple);
  const timeline = useFairyStore((state) => state.timeline) || [];
  const records = useFairyStore((state) => state.records) || [];
  const creations = useFairyStore((state) => state.creations) || [];
  const anniversaries = useFairyStore((state) => state.anniversaries) || [];
  const loading = useFairyStore((state) => Boolean(state.loading?.bootstrap || state.loading?.modules));
  const loadError = useFairyStore((state) => state.errors?.bootstrap || state.errors?.modules || null);
  const refreshCoreData = useFairyStore((state) => state.refreshCoreData);
  const [toast, setToast] = useState(null);

  const view = useMemo(() => {
    if (!isReal) return { bound: Boolean(coupleState), userName: coupleState?.userName || '我', partnerName: coupleState?.partnerName || 'TA', loveDays: coupleState?.loveDays ?? null, statusText: coupleState?.statusText || '演示状态' };
    const relation = coupleState?.couple;
    const bound = Boolean(relation?.id && relation.status === 'active' && coupleState?.partner?.id);
    return {
      bound,
      userName: coupleState?.user?.nickname || '',
      partnerName: coupleState?.partner?.nickname || '',
      loveDays: daysTogether(relation?.startedAt),
      statusText: relation?.status || null,
    };
  }, [coupleState, isReal]);

  const stats = [
    { label: '恋爱天数', value: view.loveDays ?? '未提供', icon: 'heart-outline' },
    { label: '共同记录', value: records.length, icon: 'library-outline' },
    { label: 'AI 作品', value: creations.length, icon: 'color-wand-outline' },
  ];
  const nextAnniversary = anniversaries.find((item) => item?.id && item?.date);

  const openMiss = () => setToast({ tone: 'info', message: isReal ? 'Real 模式暂未开放“想你”写入，不会模拟成功。' : '演示模式已记录互动。' });

  return (
    <FairyPage backgroundName="creamPaper" tabSafe topSpace={28} contentStyle={styles.pageContent} showsVerticalScrollIndicator>
      <View style={styles.content}>
        <View style={styles.titleBlock}><Text style={styles.eyebrow}>只属于两个人的私密故事书</Text><Text style={styles.title}>情侣空间</Text></View>
        {isReal ? <FairyRequestState loading={loading} error={loadError} onRetry={refreshCoreData} /> : null}
        {!loading && !loadError ? view.bound ? (
          <>
            <FairyCard style={[styles.profile, !compact && styles.profileWide]}>
              <FairySticker name="flower" size={44} rotate="-8deg" style={styles.flowerSticker} />
              <View style={[styles.coverWrap, compact && styles.coverWrapCompact]}><FairyImage name="coupleCover" height={compact ? 190 : 270} framed={false} radius={22} resizeMode="cover" /></View>
              <View style={styles.profileCopy}>
                <View style={styles.avatarRow}><View style={styles.avatar}><Text style={styles.avatarText}>{view.userName ? view.userName.slice(0, 1) : '?'}</Text></View><View style={styles.heartBridge}><Ionicons name="heart" size={20} color={colors.white} /></View><View style={styles.avatar}><Text style={styles.avatarText}>{view.partnerName ? view.partnerName.slice(0, 1) : '?'}</Text></View></View>
                <Text style={styles.names}>{view.userName || '昵称未提供'} 和 {view.partnerName || '伴侣昵称未提供'}</Text>
                <Text style={styles.desc}>{view.loveDays == null ? '恋爱起始日未提供或无效' : `第 ${view.loveDays} 天`}</Text>
                <View style={styles.profileTags}>{view.statusText ? <FairyTag tone="gold">{view.statusText}</FairyTag> : null}<FairyTag>共同记录 {records.length} 条</FairyTag></View>
              </View>
            </FairyCard>
            <View style={styles.statsRow}>{stats.map((item) => <FairyCard key={item.label} style={[styles.statCard, compact && styles.statCardCompact]}><Ionicons name={item.icon} size={18} color={colors.accent} /><Text style={styles.statValue}>{item.value}</Text><Text style={styles.statLabel}>{item.label}</Text></FairyCard>)}</View>
            <View style={styles.interactions}>
              <Pressable style={styles.interaction} onPress={openMiss}><Ionicons name="heart-outline" size={21} color={colors.accent} /><Text style={styles.interactionText}>想你</Text></Pressable>
              <Pressable style={styles.interaction} onPress={() => router.push('/anniversary')}><Ionicons name="calendar-outline" size={21} color={colors.accent} /><Text style={styles.interactionText}>纪念日</Text></Pressable>
              <Pressable style={styles.interaction} onPress={() => router.push('/time-capsule/settings')}><Ionicons name="hourglass-outline" size={21} color={colors.accent} /><Text style={styles.interactionText}>时光胶囊</Text></Pressable>
            </View>
            <FairyCard style={styles.anniversaryCard}>
              <View style={styles.anniversaryIcon}><Ionicons name="calendar-outline" size={24} color={colors.primaryDeep} /></View>
              <View style={styles.anniversaryText}><Text style={styles.anniversaryLabel}>纪念日入口</Text><Text style={styles.anniversaryTitle}>{nextAnniversary?.title || '暂无纪念日数据'}</Text><Text style={styles.anniversaryDesc}>{nextAnniversary?.date || '未提供日期'}</Text></View>
              <Pressable style={styles.anniversaryBtn} onPress={() => router.push('/anniversary')}><Ionicons name="chevron-forward" size={18} color={colors.accent} /></Pressable>
            </FairyCard>
            <View style={styles.sectionRow}><View><Text style={styles.section}>双人故事线</Text><Text style={styles.sectionHint}>仅展示真实记录派生的章节</Text></View></View>
            {timeline.length ? <CoupleTimeline items={timeline} /> : <FairyEmptyState compact icon="book-outline" title="故事线暂无数据" description="真实记录加载后会显示在这里。" />}
          </>
        ) : <FairyEmptyState imageName="emptyDiary" title="尚未完成情侣绑定" description="只有后端确认有效情侣关系后，双人空间才会展示共同数据。" actionTitle="去邀请" onAction={() => router.push('/account/invite')} /> : null}
      </View>
      <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' }, content: { width: '100%', maxWidth: 980 }, titleBlock: { alignItems: 'center', marginBottom: spacing.xl }, eyebrow: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 6 }, title: { color: colors.text, fontSize: 30, fontWeight: '900' }, profile: { alignItems: 'center', marginBottom: 18, backgroundColor: colors.cardPink, overflow: 'visible' }, profileWide: { flexDirection: 'row', gap: spacing.xxl, padding: spacing.xxl }, coverWrap: { width: '50%', minWidth: 320 }, coverWrapCompact: { width: '100%', minWidth: 0 }, profileCopy: { flex: 1, alignItems: 'center', padding: spacing.lg }, flowerSticker: { top: -16, left: 20 }, avatarRow: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 14 }, avatar: { width: 58, height: 58, borderRadius: 24, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border }, avatarText: { color: colors.text, fontWeight: '900', fontSize: 18 }, heartBridge: { width: 34, height: 34, borderRadius: 14, backgroundColor: colors.primaryDeep, alignItems: 'center', justifyContent: 'center' }, names: { color: colors.text, fontSize: 20, fontWeight: '900' }, desc: { color: colors.textSoft, marginTop: 8 }, profileTags: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'center', gap: 8, marginTop: 14 }, statsRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginBottom: 18 }, statCard: { flex: 1, minWidth: 180, minHeight: 112, alignItems: 'center', justifyContent: 'center', padding: 12 }, statCardCompact: { minWidth: 96 }, statValue: { color: colors.text, fontSize: 21, fontWeight: '900', marginTop: 8 }, statLabel: { color: colors.textSoft, fontSize: 11, marginTop: 3 }, interactions: { flexDirection: 'row', flexWrap: 'wrap', gap: 12, marginBottom: 18 }, interaction: { flex: 1, minWidth: 150, height: 64, borderRadius: 20, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8 }, interactionText: { color: colors.text, fontWeight: '800', fontSize: 13 }, anniversaryCard: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 28, backgroundColor: colors.cardPink }, anniversaryIcon: { width: 52, height: 52, borderRadius: 20, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center' }, anniversaryText: { flex: 1 }, anniversaryLabel: { color: colors.accent, fontSize: 12, fontWeight: '900' }, anniversaryTitle: { color: colors.text, fontSize: 16, fontWeight: '900', marginTop: 4 }, anniversaryDesc: { color: colors.textSoft, fontSize: 12, marginTop: 4 }, anniversaryBtn: { width: 36, height: 36, alignItems: 'center', justifyContent: 'center' }, sectionRow: { marginBottom: 16 }, section: { color: colors.text, fontSize: 20, fontWeight: '900' }, sectionHint: { color: colors.textSoft, fontSize: 12, marginTop: 4 },
});
