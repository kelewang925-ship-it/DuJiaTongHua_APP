import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useLocalSearchParams, useRouter } from 'expo-router';
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
import { hasCapability } from '@/config/capabilities';

const sectionMeta = {
  diary: { label: '日记', icon: 'book-outline', title: '日常 · 温暖的点滴' },
  photo: { label: '照片', icon: 'images-outline', title: '照片 · 贴在纸上的时光' },
  anniversary: { label: '纪念日', icon: 'calendar-outline', title: '纪念日 · 特别的时刻' },
  ai: { label: 'AI 作品', icon: 'sparkles-outline', title: 'AI 作品 · 魔法发生的地方' },
};
const coverMap = { romance: 'pdfMemoryBookCover', stars: 'anniversaryShareCover', garden: 'sharePreviewCover', watercolor: 'albumCover', journal: 'homeCover' };

export default function ExportPreviewPage() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const { width } = useWindowDimensions();
  const canExport = hasCapability('pdfExport');
  const records = useFairyStore((state) => state.records);
  const creations = useFairyStore((state) => state.creations);
  const anniversaries = useFairyStore((state) => state.anniversaries);
  const [selectedPage, setSelectedPage] = useState(0);
  const [exported, setExported] = useState(false);
  const [toast, setToast] = useState(null);
  const wide = width >= 760;
  const includedParam = Array.isArray(params.included) ? params.included[0] : params.included;
  const included = useMemo(() => { const values = includedParam?.split(',').filter((key) => sectionMeta[key]); return values?.length ? values : Object.keys(sectionMeta); }, [includedParam]);
  const coverKey = Array.isArray(params.cover) ? params.cover[0] : params.cover;
  const coverImage = coverMap[coverKey] || coverMap.romance;
  const paper = (Array.isArray(params.paper) ? params.paper[0] : params.paper) || 'A4';
  const quality = (Array.isArray(params.quality) ? params.quality[0] : params.quality) || '高清';
  const diaries = useMemo(() => records.filter((item) => item.type === '日记'), [records]);
  const counts = useMemo(() => ({
    diary: diaries.length,
    photo: records.filter((item) => item.type === '照片').reduce((sum, item) => sum + (Number(item.photoCount) || 0), 0),
    anniversary: anniversaries.length,
    ai: creations.length,
  }), [anniversaries.length, creations.length, diaries.length, records]);
  const itemCount = included.reduce((sum, key) => sum + counts[key], 0);
  const hasContent = itemCount > 0;
  const previewPages = hasContent ? Math.ceil(itemCount * 1.6) + 4 : 0;
  const fileSize = hasContent ? (previewPages * (quality === '超清' ? 0.62 : quality === '高清' ? 0.39 : 0.24)).toFixed(1) : null;
  const pageSamples = useMemo(() => {
    if (!hasContent) return [];
    const samples = [
      { key: 'cover', label: '封面', image: coverImage, title: '回忆绘本封面' },
      { key: 'toc', label: '目录页', image: 'exportCover', title: '回忆目录' },
    ];
    if (included.includes('diary') && counts.diary) samples.push({ key: 'diary', label: '日记页', image: 'homeCover', title: diaries[0]?.title || '未命名日记' });
    if (included.includes('photo') && counts.photo) samples.push({ key: 'photo', label: '照片页', image: 'albumCover', title: '照片章节预览' });
    if (included.includes('anniversary') && counts.anniversary) samples.push({ key: 'anniversary', label: '纪念日页', image: 'anniversaryCover', title: anniversaries[0]?.title || '未命名纪念日' });
    if (included.includes('ai') && counts.ai) samples.push({ key: 'ai', label: 'AI 作品页', image: 'workshopCover', title: creations[0]?.title || '未命名 AI 作品' });
    return samples;
  }, [anniversaries, counts, coverImage, creations, diaries, hasContent, included]);
  const activePage = pageSamples[Math.min(selectedPage, Math.max(pageSamples.length - 1, 0))];

  const showUnavailable = () => setToast({ tone: 'info', message: 'Real 模式暂未开放 PDF 生成、下载与分享。' });
  const confirmExport = () => {
    if (!hasContent) { setToast({ tone: 'info', message: '当前没有可导出的真实内容。' }); return; }
    if (!canExport) { setExported(false); showUnavailable(); return; }
    setExported(true);
    setToast({ tone: 'success', message: 'PDF 导出任务已加入 Mock 模拟队列。' });
  };

  return (
    <FairyPage backgroundName="creamPaper" header={<FairyHeader showBack title="导出预览" right={<View style={styles.headerActions}><Pressable accessibilityRole="button" disabled={!hasContent} onPress={() => canExport ? setToast({ tone: 'info', message: 'Mock 预览分享仅用于流程演示。' }) : showUnavailable()} style={({ pressed }) => [styles.headerButton, !hasContent && styles.disabled, pressed && styles.pressed]}><Ionicons name="share-social-outline" size={21} color={colors.text} /></Pressable><Pressable accessibilityRole="button" disabled={!hasContent} onPress={confirmExport} style={({ pressed }) => [styles.headerButton, !hasContent && styles.disabled, pressed && styles.pressed]}><Ionicons name="download-outline" size={23} color={colors.text} /></Pressable></View>} />} topSpace={28} bottomSpace={60} contentStyle={styles.pageContent} showsVerticalScrollIndicator>
      <View style={styles.content}>
        <View style={styles.intro}><Text style={styles.introTitle}>{hasContent ? canExport ? '翻看这本回忆册的封面与章节' : 'PDF 导出预览尚未开放' : '还没有可预览的回忆内容'}</Text><Text style={styles.introText}>{hasContent ? canExport ? '确认内容、页数和规格后，可体验 Mock 导出流程。' : '当前 Real 模式只展示版式配置，不会生成、下载或分享真实文件。' : '先创建日记、照片、纪念日或 AI 作品，再生成真实内容预览。'}</Text></View>
        {!hasContent ? <FairyEmptyState imageName="emptyDiary" title="没有可导出的内容" description="当前选择的内容类型中还没有真实记录。" actionTitle="返回修改选择" onAction={() => router.replace('/data/pdf-export')} /> : <>
          <FairyCard style={styles.previewBoard} padding={spacing.lg}>
            <View style={styles.previewGrid}>{pageSamples.map((page, index) => { const active = selectedPage === index; return <Pressable key={page.key} onPress={() => setSelectedPage(index)} style={({ pressed }) => [styles.pageSample, wide && styles.pageSampleWide, active && styles.pageSampleActive, pressed && styles.pressed]}><FairyImage name={page.image} height={wide ? 260 : 190} radius={14} framed={false} resizeMode="cover" /><View style={styles.pageShade} /><Text numberOfLines={2} style={styles.pageTitle}>{page.title}</Text><View style={styles.pageLabel}><Text style={styles.pageLabelText}>{page.label}</Text></View>{active ? <View style={styles.pageCheck}><Ionicons name="checkmark" size={18} color={colors.white} /></View> : null}</Pressable>; })}</View>
            <View style={styles.previewDetail}><View style={styles.detailHeading}><Ionicons name={activePage?.key === 'cover' ? 'book-outline' : activePage?.key === 'toc' ? 'list-outline' : sectionMeta[activePage?.key]?.icon || 'document-outline'} size={21} color={colors.primaryDeep} /><Text style={styles.detailTitle}>{activePage?.label}预览</Text></View>{activePage?.key === 'toc' ? <View style={styles.tocList}>{included.filter((key) => counts[key] > 0).map((key, index) => <View key={key} style={styles.tocRow}><Text style={styles.tocIndex}>{String(index + 1).padStart(2, '0')}</Text><Text style={styles.tocText}>{sectionMeta[key].title}</Text><View style={styles.tocDots} /><Text style={styles.tocPage}>{index * 8 + 1}</Text></View>)}</View> : <Text style={styles.detailText}>{activePage?.key === 'cover' ? '封面使用当前选择的绘本样式。' : `${activePage?.label}来自当前已加载的真实记录。`}</Text>}</View>
          </FairyCard>
          <FairyCard style={styles.summaryCard} padding={spacing.lg}><SummaryRow icon="book-outline" label="预计页数" value={`${previewPages} 页`} /><SummaryRow icon="calendar-outline" label="时间范围" value="由已加载记录计算" /><View style={styles.summaryRow}><View style={styles.summaryLabel}><Ionicons name="bookmark-outline" size={19} color={colors.gold} /><Text style={styles.summaryLabelText}>包含内容</Text></View><View style={styles.tags}>{included.filter((key) => counts[key] > 0).map((key) => <View key={key} style={styles.tag}><Text style={styles.tagText}>{sectionMeta[key].label}</Text></View>)}</View></View><SummaryRow icon="documents-outline" label="输出规格" value={`${paper} · ${quality}`} /><SummaryRow icon="cloud-download-outline" label="预计大小" value={`${fileSize} MB`} last /></FairyCard>
          {exported && canExport ? <FairyCard style={styles.doneCard} padding={spacing.lg}><Ionicons name="checkmark-circle" size={28} color={colors.gold} /><View style={styles.doneCopy}><Text style={styles.doneTitle}>Mock 导出任务已准备</Text><Text style={styles.doneText}>只展示本地流程，不会生成真实文件或触发系统下载。</Text></View></FairyCard> : null}
          {!canExport ? <FairyCard style={styles.unavailableCard} padding={spacing.lg}><Ionicons name="lock-closed-outline" size={25} color={colors.gold} /><Text style={styles.unavailableText}>Real 模式 PDF、下载和分享均未开放，不会模拟成功。</Text></FairyCard> : null}
          <View style={styles.actions}><FairyButton title="返回修改" variant="secondary" onPress={() => router.replace('/data/pdf-export')} style={styles.actionButton} /><FairyButton title={canExport ? '确认 Mock 导出' : 'PDF 暂未开放'} onPress={confirmExport} style={styles.actionButton} leftContent={<Ionicons name={canExport ? 'download-outline' : 'lock-closed-outline'} size={19} color={colors.white} />} /></View>
        </>}
      </View>
      <FairyToast visible={Boolean(toast)} tone={toast?.tone} message={toast?.message} onHide={() => setToast(null)} />
    </FairyPage>
  );
}

function SummaryRow({ icon, label, value, last = false }) { return <View style={[styles.summaryRow, last && styles.summaryRowLast]}><View style={styles.summaryLabel}><Ionicons name={icon} size={19} color={colors.gold} /><Text style={styles.summaryLabelText}>{label}</Text></View><Text style={styles.summaryValue}>{value}</Text></View>; }

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' }, content: { width: '100%', maxWidth: 900 }, headerActions: { flexDirection: 'row', alignItems: 'center' }, headerButton: { width: 30, height: 42, alignItems: 'center', justifyContent: 'center' }, intro: { alignItems: 'center', marginTop: spacing.md, marginBottom: spacing.xl }, introTitle: { color: colors.text, fontSize: 18, fontWeight: '900', textAlign: 'center' }, introText: { color: colors.textSoft, lineHeight: 21, marginTop: spacing.sm, textAlign: 'center' },
  previewBoard: { marginBottom: spacing.lg }, previewGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md }, pageSample: { width: '47.5%', position: 'relative', overflow: 'hidden', borderRadius: 18, borderWidth: 2, borderColor: 'transparent', backgroundColor: colors.background }, pageSampleWide: { width: '23.6%' }, pageSampleActive: { borderColor: colors.primaryDeep, transform: [{ translateY: -3 }] }, pageShade: { position: 'absolute', left: 0, right: 0, bottom: 0, height: 76, backgroundColor: 'rgba(82,52,47,0.46)' }, pageTitle: { position: 'absolute', left: spacing.md, right: spacing.md, bottom: 35, color: colors.white, fontSize: 13, fontWeight: '900', textAlign: 'center' }, pageLabel: { position: 'absolute', left: spacing.sm, bottom: spacing.sm, paddingHorizontal: spacing.md, paddingVertical: 4, borderRadius: 12, backgroundColor: 'rgba(255,249,244,0.92)' }, pageLabelText: { color: colors.text, fontSize: 10, fontWeight: '900' }, pageCheck: { position: 'absolute', top: spacing.sm, right: spacing.sm, width: 28, height: 28, borderRadius: 14, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.primaryDeep },
  previewDetail: { marginTop: spacing.lg, padding: spacing.lg, borderRadius: 20, backgroundColor: colors.background }, detailHeading: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginBottom: spacing.md }, detailTitle: { color: colors.text, fontSize: 16, fontWeight: '900' }, detailText: { color: colors.textSoft, lineHeight: 21 }, tocList: { gap: spacing.sm }, tocRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm }, tocIndex: { color: colors.primaryDeep, fontSize: 11, fontWeight: '900' }, tocText: { color: colors.text, fontSize: 12, fontWeight: '800' }, tocDots: { flex: 1, borderBottomWidth: 1, borderStyle: 'dotted', borderColor: colors.border }, tocPage: { color: colors.textSoft, fontSize: 11 },
  summaryCard: { marginBottom: spacing.lg }, summaryRow: { minHeight: 54, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.md, borderBottomWidth: 1, borderBottomColor: colors.border }, summaryRowLast: { borderBottomWidth: 0 }, summaryLabel: { flexDirection: 'row', alignItems: 'center', gap: spacing.md }, summaryLabelText: { color: colors.text, fontSize: 14, fontWeight: '900' }, summaryValue: { flexShrink: 1, color: colors.textSoft, fontSize: 13, fontWeight: '800', textAlign: 'right' }, tags: { flex: 1, flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'flex-end', gap: spacing.xs }, tag: { paddingHorizontal: spacing.md, paddingVertical: 5, borderRadius: 13, backgroundColor: colors.cardPink }, tagText: { color: colors.primaryDeep, fontSize: 10, fontWeight: '900' },
  doneCard: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, marginBottom: spacing.lg, backgroundColor: '#FFF8E8' }, doneCopy: { flex: 1 }, doneTitle: { color: colors.text, fontSize: 15, fontWeight: '900' }, doneText: { color: colors.textSoft, fontSize: 11, lineHeight: 17, marginTop: 3 }, unavailableCard: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, marginBottom: spacing.lg, backgroundColor: colors.cardPink }, unavailableText: { flex: 1, color: colors.textSoft, lineHeight: 20 }, actions: { flexDirection: 'row', gap: spacing.md }, actionButton: { flex: 1 }, pressed: { opacity: 0.68 }, disabled: { opacity: 0.35 },
});