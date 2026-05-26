import { ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyIllustration from '../../src/components/FairyIllustration';
import WorkshopCard from '../../src/components/WorkshopCard';
import useFairyStore from '../../src/store/useFairyStore';

const entrances = [
  ['color-palette-outline', '恋爱漫画', '把故事画成漫画', '/ai/comic-config'],
  ['videocam-outline', '回忆放映机', '让回忆开始播放', '/ai/video-config'],
];

export default function WorkshopPage() {
  const creations = useFairyStore((state) => state.creations);

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <Text style={styles.eyebrow}>回忆魔法屋</Text>
      <Text style={styles.title}>童话工坊</Text>
      <LinearGradient colors={['#FFF9F4', '#FFF0F2']} style={styles.hero}>
        <View style={styles.heroCopy}>
          <View style={styles.magicIcon}>
            <Ionicons name="sparkles" size={28} color={colors.gold} />
          </View>
          <Text style={styles.heroTitle}>把回忆变成童话</Text>
          <Text style={styles.heroText}>日记、照片和纪念日，都可以变成漫画或纪念视频。</Text>
        </View>
        <FairyIllustration scene="workshop" height={150} />
      </LinearGradient>

      <Text style={styles.section}>创作入口</Text>
      <View style={styles.grid}>
        {entrances.map(([icon, title, description, href]) => (
          <Pressable key={title} style={{ flex: 1 }} onPress={() => router.push(href)}>
            <WorkshopCard icon={icon} title={title} description={description} />
          </Pressable>
        ))}
      </View>

      <Text style={styles.section}>创作历史</Text>
      {creations.map((item) => (
        <FairyCard key={item.id} style={styles.history}>
          <FairyIllustration scene={item.artwork} width={92} height={82} />
          <View style={{ flex: 1 }}>
            <Text style={styles.historyType}>{item.type}</Text>
            <Text style={styles.historyTitle}>{item.title}</Text>
            <Text style={styles.historyText}>{item.status}</Text>
          </View>
          <Ionicons name="chevron-forward" size={18} color={colors.textSoft} />
        </FairyCard>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  content: { padding: 20, paddingTop: 64, paddingBottom: 110 },
  eyebrow: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 6 },
  title: { color: colors.text, fontSize: 30, fontWeight: '900', marginBottom: 24 },
  hero: { borderRadius: 30, padding: 18, borderWidth: 1, borderColor: colors.border, marginBottom: 28 },
  heroCopy: { marginBottom: 8 },
  magicIcon: { width: 54, height: 54, borderRadius: 22, backgroundColor: '#FFF5DF', alignItems: 'center', justifyContent: 'center', marginBottom: 14 },
  heroTitle: { color: colors.text, fontSize: 24, fontWeight: '900' },
  heroText: { color: colors.textSoft, marginTop: 10, lineHeight: 22 },
  section: { color: colors.text, fontSize: 20, fontWeight: '900', marginBottom: 16 },
  grid: { flexDirection: 'row', gap: 14, marginBottom: 28 },
  history: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 14, padding: 14 },
  historyType: { color: colors.accent, fontSize: 12, fontWeight: '800', marginBottom: 3 },
  historyTitle: { color: colors.text, fontWeight: '900', fontSize: 15 },
  historyText: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
});
