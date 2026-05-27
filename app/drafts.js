import { useMemo } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import FairyCard from '../src/components/FairyCard';
import FairyEmptyState from '../src/components/FairyEmptyState';
import FairyHeader from '../src/components/FairyHeader';
import FairyPage from '../src/components/FairyPage';
import FairyTag from '../src/components/FairyTag';
import colors from '../src/theme/colors';
import spacing from '../src/theme/spacing';
import useFairyStore from '../src/store/useFairyStore';

export default function DraftsPage() {
  const draftDiary = useFairyStore((state) => state.draftDiary);
  const creations = useFairyStore((state) => state.creations);

  const drafts = useMemo(() => {
    const items = [];
    if (draftDiary?.title || draftDiary?.content) {
      items.push({ id: 'draft-diary', type: '日记草稿', title: draftDiary.title || '未命名日记', target: '/diary/editor' });
    }
    creations
      .filter((item) => item.status?.includes('草稿'))
      .forEach((item) => items.push({ id: item.id, type: `${item.type}草稿`, title: item.title, target: '/(tabs)/workshop' }));
    return items;
  }, [creations, draftDiary]);

  return (
    <FairyPage>
      <FairyHeader
        showBack
        eyebrow="特殊页面"
        title="草稿箱"
        subtitle="没写完的内容先放这里，故事不会丢。"
        right={<FairyTag>{drafts.length} 个草稿</FairyTag>}
      />

      {drafts.length ? (
        <View style={styles.list}>
          {drafts.map((item) => (
            <Pressable key={item.id} onPress={() => router.push(item.target)}>
              <FairyCard style={styles.item}>
                <Text style={styles.title}>{item.title}</Text>
                <View style={styles.meta}>
                  <FairyTag tone="gold">{item.type}</FairyTag>
                  <Text style={styles.tip}>点击继续编辑</Text>
                </View>
              </FairyCard>
            </Pressable>
          ))}
        </View>
      ) : (
        <FairyEmptyState compact title="草稿箱是空的" description="先去写一篇日记或创建一个作品草稿吧。" actionTitle="去首页" onAction={() => router.push('/(tabs)')} />
      )}
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  list: { gap: spacing.md },
  item: { padding: spacing.lg },
  title: { color: colors.text, fontSize: 16, fontWeight: '900' },
  meta: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm, marginTop: spacing.sm },
  tip: { color: colors.textSoft, fontSize: 12 },
});
