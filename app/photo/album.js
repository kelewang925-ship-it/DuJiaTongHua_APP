import { useMemo, useState } from 'react';
import { ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyButton from '../../src/components/FairyButton';
import FairyTag from '../../src/components/FairyTag';
import FairyBackButton from '../../src/components/FairyBackButton';
import FairyEmptyState from '../../src/components/FairyEmptyState';
import useFairyStore from '../../src/store/useFairyStore';

export default function AlbumPage() {
  const records = useFairyStore((state) => state.records);
  const [viewMode, setViewMode] = useState('grid');
  const photoRecords = useMemo(
    () => records.filter((item) => item.type === '照片'),
    [records]
  );

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <FairyBackButton />
      <Text style={styles.title}>回忆相册</Text>
      <Text style={styles.subtitle}>像翻看一本贴满照片的童话绘本。</Text>

      <FairyCard style={styles.heroCard}>
        <View style={styles.heroIcon}>
          <Ionicons name="albums-outline" size={28} color={colors.accent} />
        </View>
        <View style={styles.heroTextWrap}>
          <Text style={styles.heroTitle}>照片会自动长成回忆章节</Text>
          <Text style={styles.heroText}>模拟上传后的记录，会同步到首页和情侣空间时间线。</Text>
        </View>
      </FairyCard>

      <View style={styles.summaryRow}>
        <FairyCard style={styles.summaryCard}>
          <Text style={styles.summaryNum}>{photoRecords.reduce((sum, item) => sum + (item.photoCount || 3), 0)}</Text>
          <Text style={styles.summaryText}>张照片</Text>
        </FairyCard>
        <FairyCard style={styles.summaryCard}>
          <Text style={styles.summaryNum}>{photoRecords.length}</Text>
          <Text style={styles.summaryText}>组回忆</Text>
        </FairyCard>
      </View>

      <FairyButton title="新增一组照片" onPress={() => router.push('/photo/upload')} style={styles.addButton} />

      <View style={styles.switchRow}>
        <Pressable style={viewMode === 'grid' ? styles.switchActive : styles.switch} onPress={() => setViewMode('grid')}>
          <Text style={viewMode === 'grid' ? styles.switchActiveText : styles.switchText}>网格</Text>
        </Pressable>
        <Pressable style={viewMode === 'timeline' ? styles.switchActive : styles.switch} onPress={() => setViewMode('timeline')}>
          <Text style={viewMode === 'timeline' ? styles.switchActiveText : styles.switchText}>时间线</Text>
        </Pressable>
      </View>

      {photoRecords.length === 0 ? (
        <FairyEmptyState
          icon="images-outline"
          scene="album"
          title="还没有照片"
          description="把幸福留在这一页吧。先模拟上传一组照片，就能在相册里看到它。"
          actionTitle="上传照片"
          onAction={() => router.push('/photo/upload')}
          compact
        />
      ) : viewMode === 'grid' ? (
        <View style={styles.grid}>
          {photoRecords.map((item, index) => (
            <FairyCard key={item.id} style={[styles.photoCard, index % 2 === 0 && styles.tallCard]}>
              <View style={styles.photoMock}>
                <Ionicons name="image-outline" size={28} color={colors.accent} />
                <Text style={styles.photoCount}>{item.photoCount || 3} 张</Text>
              </View>
              <Text style={styles.photoTitle}>{item.title}</Text>
              <Text style={styles.photoDate}>{item.date}</Text>
              <View style={styles.tagRow}>
                {(item.tags?.length ? item.tags.slice(0, 2) : ['照片']).map((tag) => (
                  <FairyTag key={`${item.id}-${tag}`}>{tag}</FairyTag>
                ))}
              </View>
            </FairyCard>
          ))}
        </View>
      ) : (
        <View style={styles.timeline}>
          {photoRecords.map((item) => (
            <FairyCard key={item.id} style={styles.timelineItem}>
              <View style={styles.timelineDot} />
              <View style={{ flex: 1 }}>
                <Text style={styles.photoTitle}>{item.title}</Text>
                <Text style={styles.photoDate}>{item.date} · {item.photoCount || 3} 张</Text>
                <Text style={styles.timelineText}>{item.content}</Text>
                <View style={styles.timelineTags}>
                  {(item.tags?.length ? item.tags : ['照片']).map((tag) => (
                    <FairyTag key={`${item.id}-${tag}`}>{tag}</FairyTag>
                  ))}
                </View>
              </View>
            </FairyCard>
          ))}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 54, paddingBottom: 40 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800' },
  subtitle: { color: colors.textSoft, marginTop: 8, marginBottom: 24, lineHeight: 22 },
  heroCard: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 16, backgroundColor: colors.cardPink },
  heroIcon: { width: 58, height: 58, borderRadius: 22, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: colors.border },
  heroTextWrap: { flex: 1 },
  heroTitle: { color: colors.text, fontSize: 16, fontWeight: '900' },
  heroText: { color: colors.textSoft, fontSize: 12, lineHeight: 18, marginTop: 5 },
  summaryRow: { flexDirection: 'row', gap: 12, marginBottom: 18 },
  summaryCard: { flex: 1, alignItems: 'center', padding: 16, backgroundColor: colors.cardPink },
  summaryNum: { color: colors.primaryDeep, fontSize: 28, fontWeight: '900' },
  summaryText: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
  addButton: { marginBottom: 18 },
  switchRow: { flexDirection: 'row', gap: 10, marginBottom: 18 },
  switchActive: { paddingHorizontal: 18, paddingVertical: 10, borderRadius: 18, backgroundColor: colors.primary },
  switch: { paddingHorizontal: 18, paddingVertical: 10, borderRadius: 18, backgroundColor: colors.card, borderWidth: 1, borderColor: colors.border },
  switchActiveText: { color: colors.white, fontWeight: '800' },
  switchText: { color: colors.text, fontWeight: '700' },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: 14 },
  photoCard: { width: '47%', padding: 12, minHeight: 190 },
  tallCard: { minHeight: 220 },
  photoMock: { height: 100, borderRadius: 20, backgroundColor: colors.cardPink, alignItems: 'center', justifyContent: 'center', marginBottom: 12 },
  photoCount: { color: colors.textSoft, fontSize: 11, marginTop: 6 },
  photoTitle: { color: colors.text, fontWeight: '800', fontSize: 14, marginBottom: 4 },
  photoDate: { color: colors.textSoft, fontSize: 12, marginBottom: 10 },
  tagRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
  timeline: { gap: 14 },
  timelineItem: { flexDirection: 'row', gap: 14 },
  timelineDot: { width: 12, height: 12, borderRadius: 6, backgroundColor: colors.primary, marginTop: 4 },
  timelineText: { color: colors.textSoft, fontSize: 12, lineHeight: 18 },
  timelineTags: { flexDirection: 'row', flexWrap: 'wrap', gap: 6, marginTop: 10 },
});
