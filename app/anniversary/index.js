import { ScrollView, View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyButton from '../../src/components/FairyButton';
import FairyTag from '../../src/components/FairyTag';

const days = [
  { title: '第一次见面', date: '2025.03.23', left: '已过去 428 天', icon: 'flower-outline' },
  { title: '第一次旅行', date: '2025.06.18', left: '还有 24 天', icon: 'airplane-outline' },
  { title: '恋爱纪念日', date: '2025.05.20', left: '已过去 370 天', icon: 'heart-outline' },
];

export default function AnniversaryPage() {
  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <Text style={styles.title}>重要章节</Text>
      <Text style={styles.subtitle}>每个特别的日子，都是你们童话里的一章。</Text>

      <FairyCard style={styles.hero}>
        <FairyTag tone="gold">下一个纪念日</FairyTag>
        <Text style={styles.heroTitle}>第一次旅行</Text>
        <Text style={styles.heroNum}>还有 24 天</Text>
        <Text style={styles.heroText}>可以提前准备一页专属记录模板。</Text>
      </FairyCard>

      <FairyButton title="添加新的重要章节" style={styles.button} />

      <Text style={styles.section}>全部纪念日</Text>
      {days.map((item) => (
        <FairyCard key={item.title} style={styles.item}>
          <View style={styles.icon}><Ionicons name={item.icon} size={20} color={colors.accent} /></View>
          <View style={{ flex: 1 }}>
            <Text style={styles.itemTitle}>{item.title}</Text>
            <Text style={styles.itemDate}>{item.date}</Text>
          </View>
          <Text style={styles.left}>{item.left}</Text>
        </FairyCard>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 64, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  hero: { backgroundColor: colors.cardPink, marginBottom: 16 },
  heroTitle: { color: colors.text, fontSize: 22, fontWeight: '800', marginTop: 16 },
  heroNum: { color: colors.primaryDeep, fontSize: 34, fontWeight: '900', marginTop: 8 },
  heroText: { color: colors.textSoft, marginTop: 8 },
  button: { marginBottom: 26 },
  section: { color: colors.text, fontSize: 20, fontWeight: '800', marginBottom: 16 },
  item: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 14 },
  icon: { width: 42, height: 42, borderRadius: 16, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center' },
  itemTitle: { color: colors.text, fontWeight: '800', fontSize: 15 },
  itemDate: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
  left: { color: colors.accent, fontSize: 12, fontWeight: '700' },
});
