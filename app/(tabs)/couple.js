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

const quickLinks = [
  { icon: 'heart-outline', label: '想你', action: 'miss' },
  { icon: 'calendar-outline', label: '纪念日', href: '/anniversary' },
  { icon: 'hourglass-outline', label: '时光胶囊', href: '/time-capsule/settings' },
  { icon: 'chatbubble-ellipses-outline', label: '留言', href: '/comments' },
];

function daysTogether(value) {
  if (!value) return 0;
  const start = new Date(`${value}T00:00:00`);
  if (Number.isNaN(start.getTime())) return 0;
  return Math.max(0, Math.floor((Date.now() - start.getTime()) / 86400000) + 1);
}

export default function CouplePage() {
  const { width } = useWindowDimensions();
  const compact = width < 680;
  const isReal = getApiMode() === 'real';
  const coupleState = useFairyStore((state) => state.couple);
  const timeline = useFairyStore((state) => state.timeline);
  const records = useFairyStore((state) => state.records);
  const creations = useFairyStore((state) => state.creations);
  const anniversaries = useFairyStore((state) => state.anniversaries);
  const loading = useFairyStore((state) => Boolean(state.loading?.bootstrap));
  const loadError = useFairyStore((state) => state.errors?.bootstrap || null);
  const refreshCoreData = useFairyStore((state) => state.refreshCoreData);
  const [toast, setToast] = useState(null);

  const view = useMemo(() => {
    if (!isReal) {
      return {
        bound: Boolean(coupleState),
        userName: coupleState?.userName || '我',
        partnerName: coupleState?.partnerName || 'TA',
        spaceName: coupleState?.spaceName || '双人宇宙',
        loveDays: coupleState?.loveDays || 0,
        statusText: coupleState?.statusText || '已绑定',
      };
    }
    const relation = coupleState?.couple;
    const bound = Boolean(relation && relation.status === 'active' && coupleState?.partner);
    return {
      bound,
      userName: coupleState?.user?.nickname || '我',
      partnerName: coupleState?.partner?.nickname || '等待 TA 加入',
      spaceName: '只属于我们的故事空间',
      loveDays: daysTogether(relation?.startedAt),
      statusText: bound ? '已绑定' : '等待绑定',
    };
  }, [coupleState, isReal]);

  const stats = [
    { label: '恋爱天数', value: view.loveDays, icon: 'heart-outline' },
    { label: '共同记录', value: records.length, icon: 'library-outline' },
    { label: 'AI 作品', value: creations.length, icon: 'color-wand-outline' },
  ];
  const nextAnniversary = anniversaries[0];

  const openQuickLink = (item) => {
    if (item.action === 'miss') {
      setToast({ tone: 'info', message: isReal ? 'Real 模式暂未开放“想你”互动。' : `一颗“想你”的小爱心已经送给${view.partnerName}。` });
      return;
    }
    if (item.href === '/comments') {
      setToast({ tone: 'info', message: '请从具体日记或照片进入评论页。' });
      return;
    }
    router.push(item.href);
  };

  return (
    <FairyPage backgroundName="creamPaper" tabSafe topSpace={28} contentStyle={styles.pageContent} showsVerticalScrollIndicator>
      <View style={styles.content}>
        <View style={styles.titleBlock}><Text style={styles.eyebrow}>只属于两个人的私密故事书</Text><Text style={styles.title}>情侣空间</Text></View>
        {isReal ? <FairyRequestState loading={loading} error={loadError} onRetry={refreshCoreData} /> : null}
        {!loading && !loadError ? view.bound ? (
          <>
            <FairyCard style={[styles.profile, !compact && styles.profileWide]}>
              <FairySticker name="flower" size={44} rotate="-8deg" style={styles.flowerSticker} />
              <FairySticker name="heart" size={36} rotate="10deg" style={styles.heartSticker} />
              <View style={[styles.coverWrap, compact && styles.coverWrapCompact]}><FairyImage name="coupleCover" height={compact ? 190 : 270} framed={false} radius={22} resizeMode="cover" /></View>
              <View style={styles.profileCopy}>
                <View style={styles.avatarRow}>
                  <View style={styles.avatar}><Text style={styles.avatarText}>{view.userName.slice(0, 1)}</Text></View>
                  <View style={styles.heartBridge}><Ionicons name="heart" size={20} color={colors.white} /></View>
                  <View style={styles.avatar}><Text style={styles.avatarText}>{view.partnerName.slice(0, 1)}</Text></View>
                </View>
                <Text style={styles.names}>{view.userName} 和 {view.partnerName}</Text>
                <Text style={styles.desc}>{view.spaceName} · 第 {view.loveDays} 天</Text>
                <View style={styles.profileTags}><FairyTag tone="gold">{view.statusText}</FairyTag><FairyTag>共同记录 {records.length} 条</FairyTag></View>
              </View>
            </FairyCard>

            <View style={styles.statsRow}>{stats.map((item) => <FairyCard key={item.label} style={[styles.statCard, compact && styles.statCardCompact]}><Ionicons name={item.icon} size={18} color={colors.accent} /><Text style={styles.statValue}>{item.value}</Text><Text style={styles.statLabel}>{item.label}</Text></FairyCard>)}</View>
            <View style={styles.interactions}>{quickLinks.map((item) => <Pressable key={item.label} accessibilityRole="button" style={({ pressed }) => [styles.interaction, !compact && styles.interactionWide, pressed && styles.pressed]} onPress={() => openQuickLink(item)}><Ionicons name={item.icon} size={21} color={colors.accent} /><Text style={styles.interactionText}>{item.label}</Text></Pressable>)}</View>

            <FairyCard style={styles.anniversaryCard}>
              <View style={styles.anniversaryIcon}><Ionicons name={nextAnniversary?.icon || 'calendar-outline'} size={24} color={colors.primaryDeep} /></View>
              <View style={styles.anniversaryText}><Text style={styles.anniversaryLabel}>纪念日入口</Text><Text style={styles.anniversaryTitle}>{nextAnniversary?.title || '新的重要章节'}</Text><Text style={styles.anniversaryDesc}>{nextAnniversary ? `${nextAnniversary.date}` : '把重要日子写进你们的故事。'}</Text></View>
              <Pressable style={styles.anniversaryBtn} onPress={() => router.push('/anniversary')}><Ionicons name="chevron-forward" size={18} color={colors.accent} /></Pressable>
            </FairyCard>

            <View style={styles.sectionRow}><View><Text style={styles.section}>双人故事线</Text><Text style={styles.sectionHint}>每一次记录，都会长成新的章节</Text></View><View style={styles.stickerMark}><FairySticker name="star" size={30} rotate="8deg" style={styles.inlineSticker} /></View></View>
            {timeline.length ? <CoupleTimeline items={timeline} /> : <FairyEmptyState compact icon="book-outline" title="故事线还没有新章节" description="写一篇日记、上传照片或添加纪念日后，这里会自动出现。" />}
          </>
        ) : <FairyEmptyState imageName="emptyDiary" title="先邀请 TA 加入故事" description="完成情侣绑定后，双人时间线和共同回忆会在这里展开。" actionTitle="去邀请" onAction={() => router.push('/account/invite')} /> : null}
      </View>
      <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' }, content: { width: '100%', maxWidth: 980 }, pressed: { opacity: 0.68 },
  titleBlock: { alignItems: 'center', marginBottom: spacing.xl }, eyebrow: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 6 }, title: { color: colors.text, fontSize: 30, fontWeight: '900' },
  profile: { alignItems: 'center', marginBottom: 18, backgroundColor: colors.cardPink, overflow: 'visible' }, profileWide: { flexDirection: 'row', gap: spacing.xxl, padding: spacing.xxl }, coverWrap: { width: '50%', minWidth: 320 }, coverWrapCompact: { width: '100%', minWidth: 0 }, profileCopy: { flex: 1, alignItems: 'center', padding: spacing.lg }, flowerSticker: { top: -16, left: 20 }, heartSticker: { top: 118, right: 20 },
  avatarRow: { flexDirection: 'row', alignItems: 'center', gap: 12, marginTop: 4, marginBottom: 14 }, avatar: { width: 58, height: 58, borderRadius: 24, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border }, avatarText: { color: colors.text, fontWeight: '900', fontSize: 18 }, heartBridge: { width: 34, height: 34, borderRadius: 14, backgroundColor: colors.primaryDeep, alignItems: 'center', justifyContent: 'center', transform: [{ rotate: '-8deg' }] }, names: { color: colors.text, fontSize: 20, fontWeight: '900' }, desc: { color: colors.textSoft, marginTop: 8 }, profileTags: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'center', gap: 8, marginTop: 14 },
  statsRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginBottom: 18 }, statCard: { flex: 1, minWidth: 180, minHeight: 112, alignItems: 'center', justifyContent: 'center', padding: 12 }, statCardCompact: { minWidth: 96 }, statValue: { color: colors.text, fontSize: 21, fontWeight: '900', marginTop: 8 }, statLabel: { color: colors.textSoft, fontSize: 11, marginTop: 3, fontWeight: '700', textAlign: 'center' },
  interactions: { flexDirection: 'row', flexWrap: 'wrap', gap: 12, marginBottom: 18 }, interaction: { width: '47.8%', height: 64, borderRadius: 20, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8 }, interactionWide: { width: '23.5%', flexGrow: 1 }, interactionText: { color: colors.text, fontWeight: '800', fontSize: 13 },
  anniversaryCard: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 28, backgroundColor: colors.cardPink }, anniversaryIcon: { width: 52, height: 52, borderRadius: 20, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, alignItems: 'center', justifyContent: 'center' }, anniversaryText: { flex: 1 }, anniversaryLabel: { color: colors.accent, fontSize: 12, fontWeight: '900', marginBottom: 4 }, anniversaryTitle: { color: colors.text, fontSize: 16, fontWeight: '900' }, anniversaryDesc: { color: colors.textSoft, fontSize: 12, marginTop: 4 }, anniversaryBtn: { width: 36, height: 36, borderRadius: 14, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, alignItems: 'center', justifyContent: 'center' },
  sectionRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }, section: { color: colors.text, fontSize: 20, fontWeight: '900', marginBottom: 4 }, sectionHint: { color: colors.textSoft, fontSize: 12 }, stickerMark: { width: 38, height: 38, borderRadius: 16, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border, transform: [{ rotate: '8deg' }] }, inlineSticker: { position: 'relative' },
});
