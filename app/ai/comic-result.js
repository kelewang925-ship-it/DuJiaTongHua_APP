import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, View, useWindowDimensions } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyEmptyState from '../../src/components/FairyEmptyState';
import FairyHeader from '../../src/components/FairyHeader';
import FairyImage from '../../src/components/FairyImage';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import FairyToast from '../../src/components/FairyToast';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import useFairyStore from '../../src/store/useFairyStore';
import { hasCapability } from '../../src/config/capabilities';
import { getApiMode } from '../../src/api/client';

export default function ComicResultPage() {
  const router = useRouter();
  const { width } = useWindowDimensions();
  const { id } = useLocalSearchParams();
  const comicId = Array.isArray(id) ? id[0] : id;
  const isReal = getApiMode() === 'real';
  const creations = useFairyStore((state) => state.creations);
  const selectAiJob = useFairyStore((state) => state.selectAiJob);
  const [selectedBeat, setSelectedBeat] = useState(0);
  const [toast, setToast] = useState(null);
  const canGenerate = hasCapability('aiGeneration');

  const comic = useMemo(() => comicId ? creations.find((item) => item.id === comicId && item.type === '漫画') : null, [comicId, creations]);
  const hasPersistedResult = Boolean(comic?.id && (comic.resultUrl || comic.previewImageName));
  const storyBeats = Array.isArray(comic?.storyBeats) ? comic.storyBeats.filter((beat) => beat && (beat.title || beat.copy)) : [];
  const activeBeat = storyBeats[selectedBeat] || storyBeats[0];
  const previewHeight = Math.min(240, Math.max(116, (Math.min(width, 760) - spacing.lg * 2) / 3));
  const unavailable = (message = '当前服务尚未提供这项真实写入能力。') => setToast({ message, tone: 'info' });

  const shareResult = () => {
    if (!hasPersistedResult) { unavailable('后端尚未返回可分享的漫画结果。'); return; }
    router.push({ pathname: '/share-preview', params: { id: comic.id, type: 'comic' } });
  };

  return (
    <FairyPage backgroundName="creamPaper" topSpace={28} bottomSpace={64} header={<FairyHeader showBack eyebrow="AI 童话工坊" title={comic ? '漫画作品详情' : '作品不存在'} subtitle={comic ? '仅展示当前 Store 中由真实结果字段支持的作品信息。' : '请从带有真实作品 ID 的入口进入。'} />}>
      <View style={styles.content}>
        {comic ? (
          <>
            <FairyCard style={styles.heroCard}>
              <View style={styles.titleRow}>
                <View style={styles.titleCopy}><Text style={styles.comicTitle}>{comic.title || '标题未提供'}</Text><Text style={styles.comicMeta}>{comic.styleName || '风格未提供'}</Text></View>
                <Pressable accessibilityRole="button" accessibilityLabel="收藏能力未开放" onPress={() => unavailable('收藏接口尚未接入，不会修改本地收藏状态。')} style={({ pressed }) => [styles.favoriteButton, pressed && styles.pressed]}><Ionicons name="heart-outline" size={22} color={colors.primaryDeep} /></Pressable>
              </View>
              <View style={styles.tagRow}><FairyTag tone="gold">漫画</FairyTag><Text style={styles.status}>{comic.status || '状态未提供'}</Text></View>
              {comic.previewImageName ? <FairyImage name={comic.previewImageName} height={previewHeight} radius={22} resizeMode="cover" style={styles.previewImage} /> : comic.resultUrl ? <Text style={styles.missingPreview}>后端已返回结果地址，但当前页面尚未接入远程图片渲染。</Text> : <Text style={styles.missingPreview}>后端尚未返回可展示的漫画结果。</Text>}
              {comic.imageCaption ? <Text style={styles.imageCaption}>{comic.imageCaption}</Text> : null}
            </FairyCard>

            {storyBeats.length ? <><Text style={styles.sectionEyebrow}>故事分镜</Text><View style={styles.beatGrid}>{storyBeats.map((beat, index) => { const active = selectedBeat === index; return <Pressable key={`${comic.id}-beat-${index}`} onPress={() => setSelectedBeat(index)} style={({ pressed }) => [styles.beatCard, active && styles.beatCardActive, pressed && styles.pressed]}><Ionicons name={beat.icon || 'image-outline'} size={20} color={active ? colors.primaryDeep : colors.textSoft} /><Text style={[styles.beatTitle, active && styles.beatTitleActive]}>{beat.title || '标题未提供'}</Text></Pressable>; })}</View>{activeBeat ? <FairyCard style={styles.storyCard}><Text style={styles.storyTitle}>{activeBeat.title || '标题未提供'}</Text><Text style={styles.storyText}>{activeBeat.copy || '分镜说明未提供'}</Text></FairyCard> : null}</> : <Text style={styles.missingPreview}>后端未提供分镜信息。</Text>}

            <View style={styles.actionRow}>
              <FairyButton title="保存能力未开放" onPress={() => unavailable('保存接口尚未接入，不会模拟保存成功。')} style={styles.actionButton} />
              <FairyButton title="分享预览" variant="secondary" disabled={!hasPersistedResult} onPress={shareResult} style={styles.actionButton} />
            </View>
            <FairyButton title={canGenerate && !isReal ? '调整故事并重新生成' : '重新生成未开放'} variant="link" onPress={() => { if (!canGenerate || isReal) { unavailable('真实重新生成接口尚未接入。'); return; } selectAiJob(comic.id); router.push('/ai/comic-config'); }} style={styles.editButton} />
            <FairyButton title="返回童话工坊" variant="secondary" onPress={() => router.replace('/(tabs)/workshop')} />
          </>
        ) : <FairyEmptyState imageName="emptyAiHistory" title={comicId ? '没有找到这份漫画' : '缺少作品 ID'} description={comicId ? '它可能尚未生成、已经删除，或当前账号无权访问。' : '请从童话工坊或创作历史选择一份真实作品。'} actionTitle="返回童话工坊" onAction={() => router.replace('/(tabs)/workshop')} />}
      </View>
      <FairyToast visible={Boolean(toast)} message={toast?.message} tone={toast?.tone} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  content: { width: '100%', maxWidth: 760, alignSelf: 'center', paddingHorizontal: spacing.lg }, heroCard: { padding: spacing.lg, backgroundColor: colors.cardPink, marginTop: spacing.sm }, titleRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.md }, titleCopy: { flex: 1 }, comicTitle: { color: colors.text, fontSize: 20, fontWeight: '900' }, comicMeta: { color: colors.textSoft, marginTop: 5, fontSize: 12 }, favoriteButton: { width: 44, height: 44, borderRadius: 16, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border }, tagRow: { flexDirection: 'row', alignItems: 'center', marginTop: spacing.md, gap: spacing.sm }, status: { color: colors.accent, fontSize: 12, fontWeight: '700' }, previewImage: { marginTop: spacing.md }, imageCaption: { marginTop: spacing.sm, textAlign: 'center', color: colors.textSoft, fontSize: 11 }, missingPreview: { marginTop: spacing.md, color: colors.textSoft, lineHeight: 21, textAlign: 'center' }, sectionEyebrow: { marginTop: spacing.xl, marginBottom: spacing.sm, color: colors.textSoft, fontSize: 13, fontWeight: '800' }, beatGrid: { flexDirection: 'row', gap: spacing.sm, flexWrap: 'wrap' }, beatCard: { flexGrow: 1, flexBasis: 120, minHeight: 92, padding: spacing.md, borderRadius: 20, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center' }, beatCardActive: { borderColor: colors.primary, backgroundColor: colors.cardPink }, beatTitle: { marginTop: spacing.sm, color: colors.textSoft, fontSize: 13, fontWeight: '800' }, beatTitleActive: { color: colors.text }, storyCard: { marginTop: spacing.md, marginBottom: spacing.xl }, storyTitle: { color: colors.text, fontSize: 17, fontWeight: '900' }, storyText: { marginTop: spacing.sm, color: colors.text, lineHeight: 24 }, actionRow: { flexDirection: 'row', gap: spacing.md }, actionButton: { flex: 1 }, editButton: { marginVertical: spacing.lg, alignSelf: 'center' }, pressed: { opacity: 0.68 },
});