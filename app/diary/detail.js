import { ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyBackButton from '../../src/components/FairyBackButton';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyEmptyState from '../../src/components/FairyEmptyState';
import FairyTag from '../../src/components/FairyTag';
import FairyRichTextViewer from '../../src/components/FairyRichTextViewer';
import useFairyStore from '../../src/store/useFairyStore';

export default function DiaryDetailPage() {
  const records = useFairyStore((state) => state.records);
  const diary = records.find((item) => item.type === '日记');

  if (!diary) {
    return (
      <ScrollView style={styles.page} contentContainerStyle={styles.content}>
        <FairyBackButton />
        <Text style={styles.title}>日记详情</Text>
        <Text style={styles.subtitle}>这里会收藏你们写下的每一页。</Text>
        <FairyEmptyState
          icon="book-outline"
          title="还没有日记"
          description="先写下一点点今天的故事，再回来查看这一页。"
          actionTitle="去写日记"
          onAction={() => router.replace('/diary/editor')}
        />
      </ScrollView>
    );
  }

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.title}>日记详情</Text>
      <Text style={styles.subtitle}>这一页，是你们童话里被收藏的一天。</Text>

      <FairyCard style={styles.coverCard}>
        <View style={styles.coverIcon}>
          <Ionicons name={diary.icon || 'book-outline'} size={30} color={colors.gold} />
        </View>
        <Text style={styles.diaryTitle}>{diary.title || '今天的小小童话'}</Text>
        <Text style={styles.date}>{diary.date || '刚刚'}</Text>
        <View style={styles.tags}>
          {(diary.tags || ['日记']).map((tag) => <FairyTag key={tag}>{tag}</FairyTag>)}
        </View>
        {diary.mood ? (
          <View style={styles.moodPill}>
            <Ionicons name="heart-outline" size={14} color={colors.primaryDeep} />
            <Text style={styles.moodText}>{diary.mood}</Text>
          </View>
        ) : null}
      </FairyCard>

      <FairyCard style={styles.bodyCard}>
        <Text style={styles.sectionTitle}>正文</Text>
        <FairyRichTextViewer
          html={diary.content}
          fallback="今天的故事，还没有完全写完。"
          style={styles.bodyText}
        />
      </FairyCard>

      <FairyCard style={styles.magicCard}>
        <View style={styles.magicHeader}>
          <Ionicons name="sparkles-outline" size={22} color={colors.accent} />
          <Text style={styles.sectionTitle}>把这一页变成漫画</Text>
        </View>
        <Text style={styles.magicText}>AI 可以根据这篇日记生成专属童话漫画，并同步到童话工坊。</Text>
        <Pressable style={styles.inlineAction} onPress={() => router.push('/ai/text-to-comic')}>
          <Text style={styles.inlineActionText}>去生成漫画</Text>
          <Ionicons name="chevron-forward" size={16} color={colors.primaryDeep} />
        </Pressable>
      </FairyCard>

      <FairyButton title="继续写一页" onPress={() => router.push('/diary/editor')} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  coverCard: { alignItems: 'center', backgroundColor: colors.cardPink, marginBottom: 16 },
  coverIcon: { width: 64, height: 64, borderRadius: 24, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', marginBottom: 14 },
  diaryTitle: { color: colors.text, fontSize: 22, fontWeight: '900', textAlign: 'center' },
  date: { color: colors.textSoft, marginTop: 8 },
  tags: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginTop: 14, justifyContent: 'center' },
  moodPill: { flexDirection: 'row', alignItems: 'center', gap: 5, marginTop: 14, paddingHorizontal: 12, paddingVertical: 7, borderRadius: 18, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border },
  moodText: { color: colors.primaryDeep, fontSize: 12, fontWeight: '800' },
  bodyCard: { marginBottom: 16 },
  sectionTitle: { color: colors.text, fontSize: 17, fontWeight: '800' },
  bodyText: { color: colors.text, fontSize: 16, lineHeight: 27, marginTop: 14 },
  magicCard: { marginBottom: 22 },
  magicHeader: { flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 10 },
  magicText: { color: colors.textSoft, lineHeight: 22 },
  inlineAction: { marginTop: 14, flexDirection: 'row', alignItems: 'center', gap: 4 },
  inlineActionText: { color: colors.primaryDeep, fontWeight: '800' },
});
