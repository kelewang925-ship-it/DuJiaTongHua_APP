import { ScrollView, Text, StyleSheet, View } from 'react-native';
import { router } from 'expo-router';
import colors from '../../src/theme/colors';
import FairyBackButton from '../../src/components/FairyBackButton';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
import FairyImage from '../../src/components/FairyImage';
import FairySticker from '../../src/components/FairySticker';
import FairyTag from '../../src/components/FairyTag';
import useFairyStore from '../../src/store/useFairyStore';

export default function PdfExportPage() {
  const records = useFairyStore((state) => state.records);

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.title}>PDF 导出</Text>
      <Text style={styles.subtitle}>把一段时间的故事装订成一本可以收藏的恋爱绘本。</Text>

      <FairyCard style={styles.coverCard}>
        <FairySticker name="tapeCream" size={76} rotate="-8deg" style={styles.tapeSticker} />
        <FairyImage name="pdfMemoryBookCover" height={230} radius={26} />
        <Text style={styles.coverTitle}>我们的恋爱回忆册</Text>
        <Text style={styles.coverText}>预计包含 {records.length} 条记录</Text>
        <View style={styles.tags}>
          <FairyTag>日记</FairyTag>
          <FairyTag>照片</FairyTag>
          <FairyTag tone="gold">AI作品</FairyTag>
        </View>
      </FairyCard>

      <FairyCard style={styles.option}>
        <Text style={styles.optionTitle}>导出范围</Text>
        <Text style={styles.optionText}>最近 30 天 · 包含日记、照片与漫画摘要</Text>
      </FairyCard>

      <FairyCard style={styles.option}>
        <Text style={styles.optionTitle}>绘本样式</Text>
        <Text style={styles.optionText}>奶油纸感封面 · 桃粉章节页 · 可可棕正文</Text>
      </FairyCard>

      <FairyButton title="预览导出效果" onPress={() => router.push('/data/export-preview')} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  coverCard: { backgroundColor: colors.cardPink, marginBottom: 18, overflow: 'visible' },
  tapeSticker: { top: -22, left: 28 },
  coverTitle: { color: colors.text, fontSize: 20, fontWeight: '800', marginTop: 14, textAlign: 'center' },
  coverText: { color: colors.textSoft, marginTop: 8, textAlign: 'center' },
  tags: { flexDirection: 'row', gap: 8, marginTop: 16, justifyContent: 'center' },
  option: { marginBottom: 14 },
  optionTitle: { color: colors.text, fontWeight: '800', fontSize: 15 },
  optionText: { color: colors.textSoft, marginTop: 6, lineHeight: 20 },
});
