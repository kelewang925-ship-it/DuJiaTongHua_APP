import { ScrollView, View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import WorkshopCard from '../../src/components/WorkshopCard';

export default function WorkshopPage() {
  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <Text style={styles.title}>童话工坊</Text>
      <LinearGradient colors={['#FFF9F4', '#FFF0F2']} style={styles.hero}>
        <View style={styles.magicIcon}>
          <Ionicons name="sparkles" size={28} color={colors.gold} />
        </View>
        <Text style={styles.heroTitle}>把回忆变成童话</Text>
        <Text style={styles.heroText}>日记、照片和纪念日，都可以变成漫画或纪念视频。</Text>
      </LinearGradient>

      <Text style={styles.section}>创作入口</Text>
      <View style={styles.grid}>
        <WorkshopCard icon="color-palette-outline" title="恋爱漫画" description="把故事画成漫画" />
        <WorkshopCard icon="videocam-outline" title="回忆视频" description="让回忆开始播放" />
      </View>

      <Text style={styles.section}>创作历史</Text>
      <FairyCard style={styles.history}>
        <Ionicons name="albums-outline" size={22} color={colors.accent} />
        <View style={{ flex: 1 }}>
          <Text style={styles.historyTitle}>第一次约会的小漫画</Text>
          <Text style={styles.historyText}>已生成 · 3页绘本</Text>
        </View>
      </FairyCard>
      <FairyCard style={styles.history}>
        <Ionicons name="film-outline" size={22} color={colors.accent} />
        <View style={{ flex: 1 }}>
          <Text style={styles.historyTitle}>春天散步纪念视频</Text>
          <Text style={styles.historyText}>草稿中 · 可继续编辑</Text>
        </View>
      </FairyCard>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 64, paddingBottom: 110 },
  title: { color: colors.text, fontSize: 30, fontWeight: '800', marginBottom: 24 },
  hero: { borderRadius: 30, padding: 22, borderWidth: 1, borderColor: colors.border, marginBottom: 28 },
  magicIcon: { width: 54, height: 54, borderRadius: 22, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', marginBottom: 16 },
  heroTitle: { color: colors.text, fontSize: 24, fontWeight: '800' },
  heroText: { color: colors.textSoft, marginTop: 10, lineHeight: 22 },
  section: { color: colors.text, fontSize: 20, fontWeight: '800', marginBottom: 16 },
  grid: { flexDirection: 'row', gap: 14, marginBottom: 28 },
  history: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 14 },
  historyTitle: { color: colors.text, fontWeight: '800', fontSize: 15 },
  historyText: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
});
