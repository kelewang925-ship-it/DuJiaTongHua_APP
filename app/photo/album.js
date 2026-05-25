import { ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyTag from '../../src/components/FairyTag';
import FairyBackButton from '../../src/components/FairyBackButton';
import { mockPhotos } from '../../src/api/mockData';

export default function AlbumPage() {
  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.title}>回忆相册</Text>
      <Text style={styles.subtitle}>像翻看一本贴满照片的童话绘本。</Text>

      <View style={styles.switchRow}>
        <Pressable style={styles.switchActive}><Text style={styles.switchActiveText}>网格</Text></Pressable>
        <Pressable style={styles.switch}><Text style={styles.switchText}>时间线</Text></Pressable>
      </View>

      <View style={styles.grid}>
        {mockPhotos.map((item, index) => (
          <FairyCard key={item.id} style={[styles.photoCard, index % 2 === 0 && styles.tallCard]}>
            <View style={styles.photoMock}>
              <Ionicons name="image-outline" size={28} color={colors.accent} />
            </View>
            <Text style={styles.photoTitle}>{item.title}</Text>
            <Text style={styles.photoDate}>{item.date}</Text>
            <FairyTag>{item.type || '照片'}</FairyTag>
          </FairyCard>
        ))}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  switchRow: { flexDirection: 'row', gap: 10, marginBottom: 18 },
  switchActive: { paddingHorizontal: 18, paddingVertical: 10, borderRadius: 18, backgroundColor: colors.primary },
  switch: { paddingHorizontal: 18, paddingVertical: 10, borderRadius: 18, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border },
  switchActiveText: { color: colors.white, fontWeight: '800' },
  switchText: { color: colors.text, fontWeight: '700' },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: 14 },
  photoCard: { width: '47%', padding: 12, minHeight: 190 },
  tallCard: { minHeight: 220 },
  photoMock: { height: 100, borderRadius: 20, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center', marginBottom: 12 },
  photoTitle: { color: colors.text, fontWeight: '800', fontSize: 14, marginBottom: 4 },
  photoDate: { color: colors.textSoft, fontSize: 12, marginBottom: 10 },
});
