import { useMemo } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import FairyBackButton from '../../src/components/FairyBackButton';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyTag from '../../src/components/FairyTag';
import colors from '../../src/theme/colors';
import useFairyStore from '../../src/store/useFairyStore';

export default function ComicResultPage() {
  const router = useRouter();
  const { id } = useLocalSearchParams();
  const creations = useFairyStore((state) => state.creations);
  const selectAiJob = useFairyStore((state) => state.selectAiJob);

  const comic = useMemo(() => {
    if (id) {
      return creations.find((item) => item.id === id && item.type === '漫画');
    }
    return creations.find((item) => item.type === '漫画');
  }, [creations, id]);

  const title = comic?.title || '新的恋爱漫画';
  const status = comic?.status || '已生成 · 可预览';
  const styleName = comic?.styleName || '童话绘本';
  const source = comic?.source || '童话工坊';

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.eyebrow}>AI创作结果</Text>
      <Text style={styles.title}>漫画结果详情</Text>
      <Text style={styles.subtitle}>这一页收纳了生成信息、分镜预览和后续可继续创作的入口。</Text>

      <FairyCard style={styles.heroCard}>
        <View style={styles.heroTop}>
          <View style={styles.iconWrap}>
            <Ionicons name="albums-outline" size={26} color={colors.gold} />
          </View>
          <View style={styles.heroTextWrap}>
            <Text style={styles.comicTitle}>{title}</Text>
            <Text style={styles.comicMeta}>{source} · {styleName}</Text>
          </View>
          <FairyTag tone="gold">漫画</FairyTag>
        </View>
        <Text style={styles.status}>{status}</Text>
      </FairyCard>

      <FairyCard style={styles.previewCard}>
        <Text style={styles.sectionTitle}>分镜预览</Text>
        <View style={styles.previewGrid}>
          <View style={styles.previewPage}><Text style={styles.pageNo}>01</Text></View>
          <View style={styles.previewPage}><Text style={styles.pageNo}>02</Text></View>
          <View style={styles.previewPage}><Text style={styles.pageNo}>03</Text></View>
        </View>
        <Text style={styles.previewHint}>当前为 mock 预览占位，后续会替换为真实漫画页图像。</Text>
      </FairyCard>

      <FairyCard style={styles.noteCard}>
        <Text style={styles.sectionTitle}>章节说明</Text>
        <Text style={styles.noteText}>
          这组漫画以温柔绘本线条记录你们的一段小故事，适合继续补充台词、封面和分享卡片。
        </Text>
      </FairyCard>

      <View style={styles.actions}>
        <FairyButton
          title="继续编辑生成流程"
          onPress={() => {
            if (comic?.id) selectAiJob(comic.id);
            router.push('/ai/progress');
          }}
        />
        <FairyButton title="返回童话工坊" variant="secondary" onPress={() => router.push('/(tabs)/workshop')} />
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  eyebrow: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 6 },
  title: { color: colors.text, fontSize: 30, fontWeight: '900' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 22, lineHeight: 22 },
  heroCard: { backgroundColor: colors.cardPink, marginBottom: 16 },
  heroTop: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  iconWrap: {
    width: 50,
    height: 50,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#FFF5DF',
    borderWidth: 1,
    borderColor: colors.border,
  },
  heroTextWrap: { flex: 1 },
  comicTitle: { color: colors.text, fontSize: 17, fontWeight: '900' },
  comicMeta: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
  status: { color: colors.accent, marginTop: 12, fontSize: 13, fontWeight: '700' },
  previewCard: { marginBottom: 16 },
  sectionTitle: { color: colors.text, fontSize: 16, fontWeight: '900', marginBottom: 10 },
  previewGrid: { flexDirection: 'row', gap: 10 },
  previewPage: {
    flex: 1,
    aspectRatio: 0.72,
    borderRadius: 18,
    backgroundColor: colors.white,
    borderWidth: 1,
    borderColor: colors.border,
    alignItems: 'center',
    justifyContent: 'center',
  },
  pageNo: { color: colors.gold, fontWeight: '900', fontSize: 20 },
  previewHint: { color: colors.textSoft, marginTop: 10, fontSize: 12 },
  noteCard: { marginBottom: 22 },
  noteText: { color: colors.textSoft, lineHeight: 22 },
  actions: { gap: 12 },
});
