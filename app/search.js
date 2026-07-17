import { useMemo, useState } from 'react';
import { Pressable, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';

import FairyCard from '@/components/FairyCard';
import FairyEmptyState from '@/components/FairyEmptyState';
import FairyHeader from '@/components/FairyHeader';
import FairyImage from '@/components/FairyImage';
import FairyInput from '@/components/FairyInput';
import FairyPage from '@/components/FairyPage';
import FairyRequestState from '@/components/FairyRequestState';
import FairyTag from '@/components/FairyTag';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import useFairyStore from '@/store/useFairyStore';
import { richTextToPlainText } from '@/utils/richText';
import { getApiMode } from '@/api/client';

const mockPopularKeywords = [
  { label: '旅行', icon: 'airplane-outline' },
  { label: '生日', icon: 'gift-outline' },
  { label: '晚霞', icon: 'sunny-outline' },
  { label: '第一次', icon: 'heart-outline' },
  { label: 'AI 漫画', icon: 'book-outline' },
];
const filters = ['全部', '日记', '照片', '纪念日', 'AI 作品'];
const mockRecent = ['一起散步', '纪念日', 'AI 漫画'];
const normalize = (value) => String(value || '').toLocaleLowerCase().replace(/\s+/g, ' ').trim();

export default function SearchPage() {
  const router = useRouter();
  const { width } = useWindowDimensions();
  const isReal = getApiMode() === 'real';
  const records = useFairyStore((state) => state.records);
  const anniversaries = useFairyStore((state) => state.anniversaries);
  const creations = useFairyStore((state) => state.creations);
  const customTags = useFairyStore((state) => state.customTags) || [];
  const loading = useFairyStore((state) => Boolean(state.loading?.bootstrap));
  const loadError = useFairyStore((state) => state.errors?.bootstrap || null);
  const refreshCoreData = useFairyStore((state) => state.refreshCoreData);
  const selectAiJob = useFairyStore((state) => state.selectAiJob);
  const [keyword, setKeyword] = useState('');
  const [activeFilter, setActiveFilter] = useState('全部');
  const [recentKeywords, setRecentKeywords] = useState(isReal ? [] : mockRecent);
  const compact = width < 640;

  const popularKeywords = useMemo(() => {
    if (!isReal) return mockPopularKeywords;
    const candidates = [
      ...customTags.map((item) => item.name),
      ...records.flatMap((item) => item.tags || []),
      ...anniversaries.map((item) => item.title),
    ].filter(Boolean);
    return Array.from(new Set(candidates)).slice(0, 5).map((label, index) => ({
      label,
      icon: ['heart-outline', 'star-outline', 'book-outline', 'images-outline', 'calendar-outline'][index] || 'search-outline',
    }));
  }, [anniversaries, customTags, isReal, records]);

  const searchableItems = useMemo(() => [
    ...records.map((item) => ({
      ...item,
      category: item.type === '漫画' || item.type === '视频' ? 'AI 作品' : item.type,
      description: richTextToPlainText(item.content),
      imageName: item.type === '照片' ? 'albumCover' : item.type === '漫画' || item.type === '视频' ? 'workshopCover' : 'homeCover',
      target: item.type === '日记' ? `/diary/detail?id=${item.id}` : item.type === '照片' ? `/photo/album?id=${item.id}` : '/ai/history',
    })),
    ...anniversaries.map((item) => ({
      ...item,
      category: '纪念日',
      description: item.description || item.note || '这是你们童话里值得记住的一章。',
      tags: ['纪念日', item.repeatType === 'none' || item.repeatYearly === false ? '单次提醒' : '每年提醒'],
      imageName: 'anniversaryCover',
      target: `/anniversary/countdown?id=${item.id}`,
    })),
    ...creations.map((item) => ({
      ...item,
      category: 'AI 作品',
      description: item.resultSummary || `${item.source || '童话工坊'} · ${item.status || '等待施展魔法'}`,
      tags: [item.type, item.styleName || '童话绘本'],
      date: formatCreationDate(item.createdAt),
      imageName: item.type === '视频' ? 'homeCover' : 'workshopCover',
      target: item.status?.includes('草稿') ? (item.type === '视频' ? '/ai/video-config' : '/ai/comic-config') : '/ai/history',
      creationId: item.id,
    })),
  ], [anniversaries, creations, records]);

  const result = useMemo(() => {
    const key = normalize(keyword);
    if (!key) return [];
    return searchableItems.filter((item) => {
      const text = normalize([item.title, item.description, item.category, item.mood, ...(item.tags || [])].join(' '));
      return text.includes(key) && (activeFilter === '全部' || item.category === activeFilter);
    });
  }, [activeFilter, keyword, searchableItems]);

  const searchFor = (value) => {
    const next = value.trim();
    if (!next) return;
    setKeyword(next);
    setActiveFilter('全部');
    setRecentKeywords((items) => [next, ...items.filter((item) => item !== next)].slice(0, 5));
  };

  const openResult = (item) => {
    searchFor(keyword);
    if (item.creationId) selectAiJob(item.creationId);
    router.push(item.target);
  };

  return (
    <FairyPage backgroundName="creamPaper" header={<FairyHeader showBack title="记录搜索" />} topSpace={24} bottomSpace={64} contentStyle={styles.pageContent} keyboardShouldPersistTaps="handled" keyboardDismissMode="on-drag" automaticallyAdjustKeyboardInsets showsVerticalScrollIndicator>
      <View style={styles.content}>
        {isReal ? <FairyRequestState loading={loading} error={loadError} onRetry={refreshCoreData} /> : null}
        {!loading && !loadError ? (
          <>
            <FairyCard style={styles.searchCard} padding={spacing.md}>
              <FairyInput icon="search-outline" value={keyword} onChangeText={setKeyword} onSubmitEditing={() => searchFor(keyword)} returnKeyType="search" placeholder="搜索我们的回忆" containerStyle={styles.inputWrap} />
              {keyword ? <Pressable accessibilityLabel="清空搜索" onPress={() => setKeyword('')} style={({ pressed }) => [styles.clearSearch, pressed && styles.pressed]}><Ionicons name="close-circle" size={22} color={colors.textSoft} /></Pressable> : null}
            </FairyCard>

            {popularKeywords.length ? <><View style={styles.sectionTitleRow}><Ionicons name="flame-outline" size={20} color={colors.primaryDeep} /><Text style={styles.sectionTitle}>{isReal ? '故事线索' : '热门搜索'}</Text></View><View style={styles.chipRow}>{popularKeywords.map((item) => <Pressable key={item.label} onPress={() => searchFor(item.label)} style={({ pressed }) => [styles.keywordChip, pressed && styles.pressed]}><Ionicons name={item.icon} size={17} color={colors.accent} /><Text style={styles.keywordText}>{item.label}</Text></Pressable>)}</View></> : null}

            {!keyword.trim() ? (
              <>
                <FairyCard style={[styles.heroCard, compact && styles.heroCardCompact]} padding={spacing.md}>
                  <View style={[styles.heroImage, compact && styles.heroImageCompact]}><FairyImage name="emptySearch" height={compact ? 178 : 220} radius={22} framed={false} resizeMode="cover" /></View>
                  <View style={styles.heroCopy}><Text style={styles.heroTitle}>每一滴回忆，都能被重新找到</Text><Text style={styles.heroText}>搜索日记、照片、纪念日与 AI 作品中的标题、正文和标签。</Text><View style={styles.heroTrail}><Ionicons name="heart-outline" size={15} color={colors.primaryDeep} /><Text style={styles.heroTrailText}>输入一个熟悉的词，沿着纸页回到那一天</Text></View></View>
                </FairyCard>
                <FairyCard style={styles.recentCard} padding={spacing.lg}>
                  <View style={styles.recentHeader}><View style={styles.sectionTitleRow}><Ionicons name="time-outline" size={19} color={colors.accent} /><Text style={styles.sectionTitle}>本次搜索</Text></View><Pressable onPress={() => setRecentKeywords([])} style={({ pressed }) => [styles.clearRecent, pressed && styles.pressed]}><Text style={styles.clearRecentText}>清空记录</Text></Pressable></View>
                  {recentKeywords.length ? <View style={styles.chipRow}>{recentKeywords.map((item) => <Pressable key={item} onPress={() => searchFor(item)} style={({ pressed }) => [styles.recentChip, pressed && styles.pressed]}><Text style={styles.recentText}>{item}</Text></Pressable>)}</View> : <Text style={styles.noRecent}>新的搜索词会收藏在这里。</Text>}
                </FairyCard>
              </>
            ) : (
              <>
                <View style={styles.resultHeader}><View style={styles.sectionTitleRow}><Ionicons name="search-outline" size={20} color={colors.accent} /><Text style={styles.sectionTitle}>搜索结果</Text></View><Text style={styles.resultCount}>{result.length} 条</Text></View>
                <View style={styles.filters}>{filters.map((item) => <Pressable key={item} onPress={() => setActiveFilter(item)} style={({ pressed }) => [styles.filter, activeFilter === item && styles.filterActive, pressed && styles.pressed]}><Text style={[styles.filterText, activeFilter === item && styles.filterTextActive]}>{item}</Text></Pressable>)}</View>
                {result.length ? <View style={styles.list}>{result.map((item) => <FairyCard key={`${item.category}-${item.id}`} onPress={() => openResult(item)} style={[styles.resultCard, compact && styles.resultCardCompact]} padding={spacing.md} accessibilityRole="button"><View style={[styles.thumb, compact && styles.thumbCompact]}><FairyImage name={item.imageName} height={compact ? 138 : 156} radius={18} framed={false} resizeMode="cover" /></View><View style={styles.resultBody}><View style={styles.resultMeta}><FairyTag tone={item.category === 'AI 作品' ? 'default' : 'gold'}>{item.category}</FairyTag><Text style={styles.resultDate}>{item.date || '值得纪念的一天'}</Text></View><Text numberOfLines={2} style={styles.resultTitle}>{item.title}</Text><Text numberOfLines={compact ? 2 : 3} style={styles.resultDescription}>{item.description}</Text><View style={styles.tagRow}>{(item.tags || []).slice(0, 3).map((tag) => <View key={tag} style={styles.inlineTag}><Text style={styles.inlineTagText}>{tag}</Text></View>)}</View><View style={styles.openRow}><Text style={styles.openText}>打开这页回忆</Text><Ionicons name="chevron-forward" size={17} color={colors.primaryDeep} /></View></View></FairyCard>)}</View> : <FairyEmptyState imageName="emptySearch" title="没有找到相关内容" description="换个词或分类试试看，故事可能藏在别的章节里。" actionTitle="清空搜索" onAction={() => { setKeyword(''); setActiveFilter('全部'); }} />}
              </>
            )}
          </>
        ) : null}
      </View>
    </FairyPage>
  );
}

function formatCreationDate(value) {
  if (!value) return '童话工坊';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? '童话工坊' : date.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' });
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' }, content: { width: '100%', maxWidth: 820 }, pressed: { opacity: 0.65 },
  searchCard: { marginBottom: spacing.xl, position: 'relative', backgroundColor: 'rgba(255,249,244,0.96)' }, inputWrap: { marginBottom: 0 }, clearSearch: { position: 'absolute', right: 24, top: 22, width: 40, height: 40, alignItems: 'center', justifyContent: 'center' },
  sectionTitleRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm }, sectionTitle: { color: colors.text, fontSize: 18, fontWeight: '900' }, chipRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginTop: spacing.md },
  keywordChip: { minHeight: 42, paddingHorizontal: spacing.lg, borderRadius: 18, flexDirection: 'row', alignItems: 'center', gap: spacing.sm, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border }, keywordText: { color: colors.text, fontWeight: '800' },
  heroCard: { marginTop: spacing.xl, flexDirection: 'row', gap: spacing.xl, backgroundColor: 'rgba(255,249,244,0.92)' }, heroCardCompact: { flexDirection: 'column' }, heroImage: { width: '48%' }, heroImageCompact: { width: '100%' }, heroCopy: { flex: 1, justifyContent: 'center', padding: spacing.md }, heroTitle: { color: colors.text, fontSize: 22, lineHeight: 30, fontWeight: '900' }, heroText: { color: colors.textSoft, lineHeight: 22, marginTop: spacing.md }, heroTrail: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginTop: spacing.xl }, heroTrailText: { flex: 1, color: colors.primaryDeep, fontSize: 12, fontWeight: '800' },
  recentCard: { marginTop: spacing.xl, backgroundColor: 'rgba(255,249,244,0.94)' }, recentHeader: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.md }, clearRecent: { minHeight: 40, justifyContent: 'center', paddingHorizontal: spacing.sm }, clearRecentText: { color: colors.textSoft, fontSize: 12, fontWeight: '800' }, recentChip: { paddingHorizontal: spacing.lg, paddingVertical: 9, borderRadius: 18, backgroundColor: colors.cardPink }, recentText: { color: colors.accent, fontSize: 12, fontWeight: '800' }, noRecent: { color: colors.textSoft, marginTop: spacing.md },
  resultHeader: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginTop: spacing.xl }, resultCount: { color: colors.textSoft, fontSize: 12, fontWeight: '800' }, filters: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginVertical: spacing.lg }, filter: { minHeight: 40, paddingHorizontal: spacing.lg, borderRadius: 18, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border }, filterActive: { backgroundColor: colors.primary, borderColor: colors.primaryDeep }, filterText: { color: colors.textSoft, fontSize: 12, fontWeight: '800' }, filterTextActive: { color: colors.white },
  list: { gap: spacing.md }, resultCard: { flexDirection: 'row', gap: spacing.lg, backgroundColor: 'rgba(255,249,244,0.96)' }, resultCardCompact: { flexDirection: 'column' }, thumb: { width: 190 }, thumbCompact: { width: '100%' }, resultBody: { flex: 1, minWidth: 0, padding: spacing.sm }, resultMeta: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm }, resultDate: { color: colors.textSoft, fontSize: 11 }, resultTitle: { color: colors.text, fontSize: 18, fontWeight: '900', marginTop: spacing.sm }, resultDescription: { color: colors.textSoft, lineHeight: 20, marginTop: spacing.sm }, tagRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 6, marginTop: spacing.md }, inlineTag: { paddingHorizontal: spacing.sm, paddingVertical: 4, borderRadius: 10, backgroundColor: colors.cardPink }, inlineTagText: { color: colors.accent, fontSize: 10, fontWeight: '800' }, openRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'flex-end', gap: 4, marginTop: spacing.md }, openText: { color: colors.primaryDeep, fontSize: 12, fontWeight: '900' },
});
