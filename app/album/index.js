import { ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyBackButton from '../../src/components/FairyBackButton';
import FairyTag from '../../src/components/FairyTag';

const photos = [
  ['奶油蛋糕和你', '2026.05.24'],
  ['一起散步的傍晚', '2026.05.23'],
  ['路边的小花', '2026.05.21'],
  ['第一次旅行', '2026.05.18'],
  ['雨后的街角', '2026.05.16'],
  ['晚餐和电影', '2026.05.12'],
];

export default function AlbumPage() {
  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <View style={styles.header}>
        <View>
          <Text style={styles.title}>回忆相册</Text>
          <Text style={styles.subtitle}>把一张张照片，贴成你们的故事墙。</Text>
        </View>
        <Pressable style={styles.addBtn} onPress={() => router.push('/photo/upload')}>
          <Ionicons name="add" size={22} color={colors.white} />
        </Pressable>
      </View>

      <FairyCard style={styles.summary}>
        <FairyTag tone="gold">本月回忆</FairyTag>
        <Text style={styles.summaryTitle}>已经收藏 128 张照片</Text>
        <Text style={styles.summaryText}>最近一次更新：昨天 16:42</Text>
      </FairyCard>

      <Text style={styles.section}>照片墙</Text>
      <View style={styles.grid}>
        {photos.map((item, index) => (
          <View key={item[0]} style={[styles.photo, index % 3 === 0 && styles.largePhoto]}>
            <Ionicons name="image-outline" size={26} color={colors.accent} />
            <Text style={styles.photoTitle}>{item[0]}</Text>
            <Text style={styles.photoDate}>{item[1]}</Text>
          </View>
        ))}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 24 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, lineHeight: 22, maxWidth: 250 },
  addBtn: { width: 44, height: 44, borderRadius: 18, backgroundColor: colors.primary, alignItems: 'center', justifyContent: 'center' },
  summary: { backgroundColor: colors.cardPink, marginBottom: 26 },
  summaryTitle: { color: colors.text, fontSize: 22, fontWeight: '800', marginTop: 14 },
  summaryText: { color: colors.textSoft, marginTop: 8 },
  section: { color: colors.text, fontSize: 20, fontWeight: '800', marginBottom: 16 },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: 12 },
  photo: { width: '48%', minHeight: 150, borderRadius: 24, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border, padding: 14, justifyContent: 'flex-end' },
  largePhoto: { minHeight: 180, backgroundColor: colors.cardPink },
  photoTitle: { color: colors.text, fontWeight: '800', marginTop: 12 },
  photoDate: { color: colors.textSoft, fontSize: 12, marginTop: 4 },
});
