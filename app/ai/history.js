import { Pressable, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import FairyCard from '../../src/components/FairyCard';
import FairyEmptyState from '../../src/components/FairyEmptyState';
import FairyHeader from '../../src/components/FairyHeader';
import FairyImage from '../../src/components/FairyImage';
import FairyPage from '../../src/components/FairyPage';
import FairyTag from '../../src/components/FairyTag';
import colors from '../../src/theme/colors';
import spacing from '../../src/theme/spacing';
import useFairyStore from '../../src/store/useFairyStore';

export default function AiCreationHistoryPage() {
  const creations = useFairyStore((state) => state.creations);
  const selectAiJob = useFairyStore((state) => state.selectAiJob);

  const openCreation = (id) => {
    selectAiJob(id);
    router.push('/ai/progress');
  };

  return (
    <FairyPage backgroundName="creamPaper">
      <FairyHeader
        showBack
        eyebrow="AI 童话工坊"
        title="创作历史"
        subtitle="集中查看已经生成或正在生成的漫画、视频和纪念册。"
        right={<FairyTag tone="gold">{creations.length} 件</FairyTag>}
      />

      {creations.length ? (
        <View style={styles.list}>
          {creations.map((item) => (
            <Pressable key={item.id} onPress={() => openCreation(item.id)}>
              <FairyCard style={styles.item}>
                <FairyImage name="workshopCover" height={86} radius={20} style={styles.thumb} />
                <View style={styles.body}>
                  <View style={styles.meta}>
                    <FairyTag tone={item.progress === 100 ? 'gold' : 'default'}>{item.type}</FairyTag>
                    <Text style={styles.status}>{item.status}</Text>
                  </View>
                  <Text style={styles.title}>{item.title}</Text>
                  <Text style={styles.text}>{item.source || '童话工坊'} · {item.styleName || '默认风格'}</Text>
                </View>
                <Ionicons name="chevron-forward" size={18} color={colors.textSoft} />
              </FairyCard>
            </Pressable>
          ))}
        </View>
      ) : (
        <FairyEmptyState
          imageName="emptyAiHistory"
          title="还没有 AI 作品"
          description="第一段回忆还在等待被施展魔法。可以先写一篇日记，或上传一组照片。"
          actionTitle="去童话工坊"
          onAction={() => router.push('/(tabs)/workshop')}
        />
      )}
    </FairyPage>
  );
}

const styles = StyleSheet.create({
  list: { gap: spacing.md },
  item: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, padding: spacing.md },
  thumb: { width: 92 },
  body: { flex: 1 },
  meta: { flexDirection: 'row', alignItems: 'center', flexWrap: 'wrap', gap: spacing.sm, marginBottom: spacing.xs },
  status: { color: colors.textSoft, fontSize: 12, fontWeight: '700' },
  title: { color: colors.text, fontWeight: '900', fontSize: 15 },
  text: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
});
