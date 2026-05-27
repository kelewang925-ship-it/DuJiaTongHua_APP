import { useMemo, useState } from 'react';
import { View, Text, StyleSheet, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../src/theme/colors';
import spacing from '../src/theme/spacing';
import FairyPage from '../src/components/FairyPage';
import FairyHeader from '../src/components/FairyHeader';
import FairyCard from '../src/components/FairyCard';
import FairyInput from '../src/components/FairyInput';
import FairyTag from '../src/components/FairyTag';
import FairyEmptyState from '../src/components/FairyEmptyState';
import useFairyStore from '../src/store/useFairyStore';

const filters = ['全部', '日记', '照片', 'AI', '纪念日', '动态'];

function normalizeText(value) {
  return String(value || '').toLowerCase();
}

export default function SearchPage() {
  const records = useFairyStore((state) => state.records);
  const creations = useFairyStore((state) => state.creations);
  const anniversaries = useFairyStore((state) => state.anniversaries);
  const timeline = useFairyStore((state) => state.timeline);
  const [keyword, setKeyword] = useState('');
  const [filter, setFilter] = useState('全部');

  const allItems = useMemo(() => [
    ...records.map((item) => ({ ...item, sourceType: item.type, routeType: item.type })),
    ...creations.map((item) => ({ ...item, sourceType: 'AI', routeType: 'AI', content: item.status, date: '创作历史' })),
    ...anniversaries.map((item) => ({ ...item, sourceType: '纪念日', routeType: '纪念日', content: item.note || item.date, date: item.date })),
    ...timeline.map((item) => ({ ...item, sourceType: '动态', routeType: '动态', content: item.description, date: item.time })),
  ], [records, creations, anniversaries, timeline]);

  const results = useMemo(() => {
    const q = normalizeText(keyword.trim());
    return allItems.filter((item) => {
      const typeMatched = filter === '全部' || item.sourceType === filter || item.type === filter;
      const text = normalizeText(`${item.title} ${item.content} ${item.description} ${item.status} ${(item.tags || []).join(' ')}`);
      const keywordMatched = !q || text.includes(q);
      return typeMatched && keywordMatched;
    });
  }, [allItems, filter, keyword]);

  const openResult = (item) => {
    if (item.routeType === '日记') router.push('/diary/detail');
    else if (item.routeType === '照片') router.push('/photo/album');
    else if (item.routeType === '纪念日') router.push('/anniversary');
    else if (item.routeType === '动态') router.push('/couple/activity-detail');
    else router.push('/(tabs)/workshop');
  };

  return (
    <FairyPage>
      <FairyHeader
        showBack
        eyebrow="回忆索引"
        title="记录搜索"
        subtitle="按关键词、标签和类型，找回你们童话里的某一页。"
      />

      <FairyInput
        label="搜索关键词"
        icon="search-outline"
        value={keyword}
        onChangeText={setKeyword}
        placeholder="输入地点、事件、心情或一句话"
        helper="会同时搜索日记、照片、纪念日、AI作品和情侣动态。"
      />

      <View style={styles.filterRow}>
        {filters.map((item) => (
          <Pressable key={item} onPress={() => setFilter(item)}>
            <FairyTag tone={filter === item ? 'gold' : 'default'}>{item}</FairyTag>
          </Pressable>
        ))}
      </View>

      <View style={styles.resultHeader}>
        <Text style={styles.section}>搜索结果</Text>
        <Text style={styles.count}>{results.length} 条</Text>
      </View>

      {results.length === 0 ? (
        <FairyEmptyState
          compact
          icon="search-outline"
          title="没有找到这一页"
          description="换一个关键词，或者先记录一段新的故事。"
        />
      ) : (
        <View style={styles.list}>
          {results.map((item, index) => (
            <Pressable key={`${item.sourceType}-${item.id || index}`} onPress={() => openResult(item)}>
              <FairyCard style={styles.resultCard}>
                <View style={styles.iconWrap}>
                  <Ionicons name={item.icon || 'document-text-outline'} size={20} color={colors.accent} />
                </View>
                <View style={{ flex: 1 }}>
                  <View style={styles.titleRow}>
                    <Text style={styles.resultTitle} numberOfLines={1}>{item.title}</Text>
                    <FairyTag tone={item.sourceType === 'AI' ? 'gold' : 'default'}>{item.sourceType}</FairyTag>
                  </View>
                  <Text style={styles.resultText} numberOfLines={2}>{item.content || item.description || item.status || item.date}</Text>
                  <Text style={styles.date}>{item.date || item.time || '回忆'}</Text>
                </View>
                <Ionicons name="chevron-forward" size={18} color={colors.textSoft} />
              </FairyCard>
            </Pressable>
          ))}
        </View>
      )}
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  filterRow: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginBottom: spacing.xl },
  resultHeader: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: spacing.md },
  section: { color: colors.text, fontSize: 20, fontWeight: '900' },
  count: { color: colors.textSoft, fontSize: 12, fontWeight: '800' },
  list: { gap: spacing.md },
  resultCard: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, padding: spacing.md },
  iconWrap: { width: 42, height: 42, borderRadius: 16, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  titleRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.sm },
  resultTitle: { flex: 1, color: colors.text, fontSize: 15, fontWeight: '900' },
  resultText: { color: colors.textSoft, fontSize: 12, lineHeight: 18, marginTop: 5 },
  date: { color: colors.textSoft, fontSize: 11, marginTop: 6 },
});
