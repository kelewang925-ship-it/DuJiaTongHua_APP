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
import { hasCapability } from '@/config/capabilities';
import { getApiMode } from '@/api/client';

const filters = ['全部', '漫画', '视频', '生成中'];

export default function AiCreationHistoryPage() {
  const { width } = useWindowDimensions();
  const isReal = getApiMode() === 'real';
  const canGenerate = hasCapability('aiGeneration');
  const storedCreations = useFairyStore((state) => state.creations) || [];
  const creations = isReal ? storedCreations.filter((item) => item?.id) : storedCreations;
  const selectAiJob = useFairyStore((state) => state.selectAiJob);
  const [filter, setFilter] = useState(filters[0]);
  const [toast, setToast] = useState(null);
  const compact = width < 620;
  const filtered = useMemo(() => creations.filter((item) => { if (filter === '全部') return true; if (filter === '生成中') return Number(item.progress) < 100; return item.type === filter; }), [creations, filter]);
  const showUnavailable = (message = '当前服务尚未提供这项真实能力。') => setToast({ message, tone: 'info' });

  const openCreation = (item) => {
    if (!item?.id) { showUnavailable('缺少后端作品 ID，无法打开。'); return; }
    selectAiJob(item.id);
    if (Number(item.progress) < 100) { router.push('/ai/progress'); return; }
    if (item.type === '视频') router.push(`/ai/video-preview?id=${encodeURIComponent(item.id)}`);
    else if (item.type === '漫画') router.push(`/ai/comic-result?id=${encodeURIComponent(item.id)}`);
    else showUnavailable('后端返回了暂不支持的作品类型。');
  };

  return (
    <FairyPage backgroundName="creamPaper" header={<FairyHeader showBack title="创作历史" right={<Ionicons name="options-outline" size={23} color={colors.textSoft} />} />} topSpace={18} bottomSpace={64}>
      <View style={styles.content}>
        <Text style={styles.subtitle}>{isReal ? '仅展示当前账号真实返回的 AI 任务记录' : 'Mock 作品会自动收藏在这里'}</Text>
        <View style={styles.filters}>{filters.map((item) => <Pressable key={item} onPress={() => setFilter(item)} style={({ pressed }) => [styles.filter, filter === item && styles.filterActive, pressed && styles.pressed]}><Text style={[styles.filterText, filter === item && styles.filterTextActive]}>{item}</Text></Pressable>)}</View>
        {filtered.length ? <View style={styles.list}>{filtered.map((item) => { const progress = Number(item.progress); const done = Number.isFinite(progress) && progress >= 100; const imageName = item.previewImageName || null; const metadata = [item.source, item.styleName].filter(Boolean).join(' · '); const time = formatCreationTime(item.createdAt); return <FairyCard key={item.id} style={[styles.item, compact && styles.itemCompact]}>{imageName ? <View style={[styles.thumbWrap, compact && styles.thumbWrapCompact]}><FairyImage name={imageName} height={170} radius={20} framed={false} /></View> : <View style={[styles.thumbPlaceholder, compact && styles.thumbWrapCompact]}><Ionicons name="image-outline" size={30} color={colors.textSoft} /><Text style={styles.placeholderText}>预览未提供</Text></View>}<View style={styles.body}><View style={styles.meta}>{item.type ? <FairyTag>{item.type}</FairyTag> : <FairyTag>类型未提供</FairyTag>}<FairyTag tone={done ? 'gold' : 'default'}>{item.status || (Number.isFinite(progress) ? (done ? '已完成' : '生成中') : '状态未提供')}</FairyTag></View><Text style={styles.title}>{item.title || '标题未提供'}</Text><Text style={styles.text}>{metadata || '来源与风格未提供'}</Text>{time ? <View style={styles.dateRow}><Ionicons name="time-outline" size={14} color={colors.textSoft} /><Text style={styles.date}>{time}</Text></View> : <Text style={styles.date}>创建时间未提供</Text>}{!done && Number.isFinite(progress) ? <View style={styles.progressTrack}><View style={[styles.progressFill, { width: `${Math.max(0, Math.min(100, progress))}%` }]} /></View> : null}<View style={styles.actions}><Pressable onPress={() => openCreation(item)} style={({ pressed }) => [styles.primaryAction, pressed && styles.pressed]}><Text style={styles.primaryActionText}>{done ? '查看作品' : '查看进度'}</Text></Pressable><Pressable onPress={() => isReal ? showUnavailable('真实分享结果尚未接入。') : setToast({ message: `《${item.title || '未命名作品'}》Mock 分享卡片已准备好`, tone: 'success' })} style={({ pressed }) => [styles.secondaryAction, pressed && styles.pressed]}><Text style={styles.secondaryActionText}>分享</Text></Pressable></View></View></FairyCard>; })}</View> : <FairyEmptyState imageName="emptyAiHistory" title={filter === '全部' ? '暂无创作记录' : `暂无${filter}记录`} description={isReal ? '当前账号尚未返回符合条件的真实 AI 任务。' : '第一段回忆还在等待被施展 Mock 魔法。'} actionTitle="返回童话工坊" onAction={() => router.push('/(tabs)/workshop')} />}
        <View style={styles.footer}><Ionicons name={canGenerate ? 'color-wand-outline' : 'lock-closed-outline'} size={18} color={colors.gold} /><Text style={styles.footerText}>{canGenerate ? '作品状态以当前任务数据为准' : '等待真实 AI 服务接入后再开启生成'}</Text></View>
      </View>
      <FairyToast visible={Boolean(toast)} message={toast?.message} tone={toast?.tone} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

function formatCreationTime(value) { if (!value) return ''; const date = new Date(value); if (Number.isNaN(date.getTime())) return ''; return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`; }

const styles = StyleSheet.create({
  content: { width: '100%', maxWidth: 760, alignSelf: 'center' }, subtitle: { marginBottom: spacing.lg, textAlign: 'center', color: colors.textSoft, fontSize: 14, fontWeight: '700' }, filters: { flexDirection: 'row', padding: spacing.xs, marginBottom: spacing.xl, borderRadius: 20, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.card }, filter: { flex: 1, minHeight: 44, alignItems: 'center', justifyContent: 'center', borderRadius: 16 }, filterActive: { backgroundColor: colors.primary }, filterText: { color: colors.text, fontSize: 13, fontWeight: '800' }, filterTextActive: { color: colors.white }, list: { gap: spacing.lg }, item: { flexDirection: 'row', alignItems: 'stretch', gap: spacing.lg, padding: spacing.md }, itemCompact: { flexDirection: 'column' }, thumbWrap: { width: '39%', minWidth: 180 }, thumbWrapCompact: { width: '100%', minWidth: 0 }, thumbPlaceholder: { width: '39%', minWidth: 180, minHeight: 170, borderRadius: 20, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.background, borderWidth: 1, borderColor: colors.border }, placeholderText: { color: colors.textSoft, marginTop: spacing.sm, fontSize: 11 }, body: { flex: 1 }, meta: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm }, title: { marginTop: spacing.md, color: colors.text, fontWeight: '900', fontSize: 18 }, text: { marginTop: spacing.xs, color: colors.textSoft, fontSize: 12 }, dateRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.xs, marginTop: spacing.md }, date: { color: colors.textSoft, fontSize: 10, marginTop: spacing.sm }, progressTrack: { height: 6, marginTop: spacing.md, overflow: 'hidden', borderRadius: 3, backgroundColor: colors.secondary }, progressFill: { height: 6, borderRadius: 3, backgroundColor: colors.primaryDeep }, actions: { flexDirection: 'row', gap: spacing.sm, marginTop: spacing.md }, primaryAction: { flex: 1, minHeight: 40, alignItems: 'center', justifyContent: 'center', borderRadius: 15, borderWidth: 1, borderColor: colors.primary, backgroundColor: colors.cardPink }, primaryActionText: { color: colors.primaryDeep, fontSize: 11, fontWeight: '900' }, secondaryAction: { minWidth: 82, minHeight: 40, alignItems: 'center', justifyContent: 'center', borderRadius: 15, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.card }, secondaryActionText: { color: colors.textSoft, fontSize: 11, fontWeight: '800' }, footer: { marginTop: spacing.xl, minHeight: 56, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, borderRadius: 20, backgroundColor: colors.cardPink }, footerText: { color: colors.textSoft, fontSize: 11, fontWeight: '700' }, pressed: { opacity: 0.68 },
});