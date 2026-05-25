import { ScrollView, Text, StyleSheet, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyBackButton from '../../src/components/FairyBackButton';
import FairyButton from '../../src/components/FairyButton';
import FairyCard from '../../src/components/FairyCard';
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
        <View style={styles.coverIcon}>
          <Ionicons name="book-outline" size={30} color={colors.gold} />
        </View>
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

      <FairyButton title="预览导出效果" />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  coverCard: { alignItems: 'center', backgroundColor: colors.cardPink, marginBottom: 18 },
  coverIcon: { width: 62, height: 62, borderRadius: 24, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', marginBottom: 14 },
  coverTitle: { color: colors.text, fontSize: 20, fontWeight: '800' },
  coverText: { color: colors.textSoft, marginTop: 8 },
  tags: { flexDirection: 'row', gap: 8, marginTop: 16 },
  option: { marginBottom: 14 },
  optionTitle: { color: colors.text, fontWeight: '800', fontSize: 15 },
  optionText: { color: colors.textSoft, marginTop: 6, lineHeight: 20 },
});
