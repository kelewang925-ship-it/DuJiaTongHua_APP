import { Pressable, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import FairyButton from '@/components/FairyButton';
import FairyCard from '@/components/FairyCard';
import FairyEmptyState from '@/components/FairyEmptyState';
import FairyHeader from '@/components/FairyHeader';
import FairyPage from '@/components/FairyPage';
import FairyRequestState from '@/components/FairyRequestState';
import FairyTag from '@/components/FairyTag';
import { getApiMode } from '@/api/client';
import useFairyStore from '@/store/useFairyStore';
import colors from '@/theme/colors';
import spacing from '@/theme/spacing';
import { formatDiaryDate } from '@/utils/date';
import { richTextToPlainText } from '@/utils/richText';

export default function DiaryIndexPage() {
  const { width } = useWindowDimensions();
  const compact = width < 680;
  const isReal = getApiMode() === 'real';
  const records = useFairyStore((state) => state.records) || [];
  const loading = useFairyStore((state) => Boolean(state.loading?.modules || state.loading?.bootstrap));
  const loadError = useFairyStore((state) => state.errors?.modules || state.errors?.bootstrap || null);
  const refreshCoreData = useFairyStore((state) => state.refreshCoreData);
  const diaries = records.filter((item) => item.type === '日记');

  return (
    <FairyPage
      backgroundName="creamPaper"
      header={<FairyHeader showBack title="日记" />}
      topSpace={20}
      bottomSpace={64}
      contentStyle={styles.pageContent}
      showsVerticalScrollIndicator
    >
      <View style={styles.content}>
        <View style={styles.intro}>
          <Text style={styles.eyebrow}>你们一起写下的日常</Text>
          <Text style={styles.title}>日记收藏</Text>
          <Text style={styles.description}>每一篇日记都会成为两个人故事里的温柔章节。</Text>
        </View>

        {isReal ? <FairyRequestState loading={loading} error={loadError} onRetry={refreshCoreData} /> : null}

        {!loading && !loadError ? diaries.length ? (
          <View style={styles.list}>
            {diaries.map((diary) => {
              const content = richTextToPlainText(diary.content || '').trim() || '正文未提供';
              return (
                <Pressable
                  key={diary.id}
                  accessibilityRole="button"
                  accessibilityLabel={`查看日记：${diary.title || '未命名日记'}`}
                  onPress={() => router.push({ pathname: '/diary/detail', params: { id: diary.id } })}
                  style={({ pressed }) => [pressed && styles.pressed]}
                >
                  <FairyCard style={[styles.diaryCard, !compact && styles.diaryCardWide]} padding={spacing.lg}>
                    <View style={styles.iconWrap}><Ionicons name="book-outline" size={22} color={colors.accent} /></View>
                    <View style={styles.copy}>
                      <View style={styles.titleRow}>
                        <Text numberOfLines={1} style={styles.diaryTitle}>{diary.title || '未命名日记'}</Text>
                        <Text style={styles.date}>{formatDiaryDate(diary)}</Text>
                      </View>
                      <Text numberOfLines={2} style={styles.diaryContent}>{content}</Text>
                      {diary.tags?.length ? <View style={styles.tags}>{diary.tags.slice(0, 3).map((tag) => <FairyTag key={`${diary.id}-${tag}`}>{tag}</FairyTag>)}</View> : null}
                    </View>
                    <Ionicons name="chevron-forward" size={20} color={colors.textSoft} />
                  </FairyCard>
                </Pressable>
              );
            })}
          </View>
        ) : (
          <FairyEmptyState
            imageName="emptyDiary"
            title="还没有日记"
            description="写下第一篇日记，让今天成为你们故事的开场。"
            actionTitle="写一篇日记"
            onAction={() => router.push('/diary/editor')}
          />
        ) : null}

        {!loading && !loadError ? <FairyButton title="写一篇日记" onPress={() => router.push('/diary/editor')} style={styles.writeButton} leftContent={<Ionicons name="create-outline" size={20} color={colors.white} />} /> : null}
      </View>
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  pageContent: { alignItems: 'center' },
  content: { width: '100%', maxWidth: 860 },
  intro: { alignItems: 'center', marginBottom: spacing.xl },
  eyebrow: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 6 },
  title: { color: colors.text, fontSize: 28, fontWeight: '900' },
  description: { color: colors.textSoft, fontSize: 13, textAlign: 'center', marginTop: 8 },
  list: { gap: 12 },
  diaryCard: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  diaryCardWide: { paddingHorizontal: spacing.xl },
  iconWrap: { width: 46, height: 46, borderRadius: 16, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center' },
  copy: { flex: 1, minWidth: 0 },
  titleRow: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  diaryTitle: { flex: 1, color: colors.text, fontSize: 16, fontWeight: '900' },
  date: { color: colors.textSoft, fontSize: 11 },
  diaryContent: { color: colors.textSoft, fontSize: 13, lineHeight: 20, marginTop: 6 },
  tags: { flexDirection: 'row', flexWrap: 'wrap', gap: 6, marginTop: 10 },
  writeButton: { marginTop: spacing.xl },
  pressed: { opacity: 0.82, transform: [{ scale: 0.99 }] },
});
