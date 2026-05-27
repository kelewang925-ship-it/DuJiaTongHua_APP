import { ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import colors from '../../src/theme/colors';
import FairyCard from '../../src/components/FairyCard';
import FairyImage from '../../src/components/FairyImage';
import FairyIllustration from '../../src/components/FairyIllustration';
import FairyTag from '../../src/components/FairyTag';
import WorkshopCard from '../../src/components/WorkshopCard';
import useFairyStore from '../../src/store/useFairyStore';

const entrances = [
  ['color-palette-outline', '恋爱漫画', '把日记或照片画成童话漫画', '/ai/comic-config'],
  ['videocam-outline', '回忆放映机', '生成带字幕和音乐的纪念视频', '/ai/video-config'],
  ['document-text-outline', '文字转漫画', '直接把一段故事变成绘本分镜', '/ai/text-to-comic'],
];

export default function WorkshopPage() {
  const creations = useFairyStore((state) => state.creations);
  const selectAiJob = useFairyStore((state) => state.selectAiJob);
  const latestJob = creations[0];

  const openCreation = (id) => {
    const current = creations.find((item) => item.id === id);
    selectAiJob(id);
    if (current?.type === '漫画') {
      router.push(`/ai/comic-result?id=${id}`);
      return;
    }
    router.push('/ai/progress');
  };

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
          <Text style={styles.heroText}>从日记、照片或一段文字开始，创建漫画和回忆短片。</Text>
          {latestJob ? (
            <Pressable style={styles.latestPill} onPress={() => openCreation(latestJob.id)}>
              <Ionicons name={latestJob.icon} size={16} color={colors.primaryDeep} />
              <Text style={styles.latestText}>最近作品：{latestJob.title}</Text>
            </Pressable>
          ) : null}
        </View>
        <FairyImage name="workshopCover" height={150} />
      </LinearGradient>

      <Text style={styles.section}>创作入口</Text>
      <View style={styles.grid}>
        {entrances.map(([icon, title, description, href]) => (
          <Pressable key={title} style={styles.entry} onPress={() => router.push(href)}>
            <WorkshopCard icon={icon} title={title} description={description} />
          </Pressable>
        ))}
      </View>

      <Text style={styles.section}>创作历史</Text>
      {creations.map((item) => (
        <Pressable key={item.id} onPress={() => openCreation(item.id)}>
          <FairyCard style={styles.history}>
            <FairyIllustration scene={item.artwork} width={92} height={82} />
            <View style={styles.historyBody}>
              <View style={styles.historyMeta}>
                <FairyTag tone={item.progress === 100 ? 'gold' : 'default'}>{item.type}</FairyTag>
                <Text style={styles.historyStatus}>{item.status}</Text>
              </View>
              <Text style={styles.historyTitle}>{item.title}</Text>
              <Text style={styles.historyText}>
                {item.source || '童话工坊'} · {item.styleName || '默认风格'}
              </Text>
            </View>
            <Ionicons name="chevron-forward" size={18} color={colors.textSoft} />
          </FairyCard>
        </Pressable>
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
  latestPill: { flexDirection: 'row', alignItems: 'center', gap: 8, marginTop: 14, paddingVertical: 9, paddingHorizontal: 12, borderRadius: 16, backgroundColor: colors.white, borderWidth: 1, borderColor: colors.border },
  latestText: { color: colors.text, fontSize: 12, fontWeight: '800', flex: 1 },
  section: { color: colors.text, fontSize: 20, fontWeight: '900', marginBottom: 16 },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: 14, marginBottom: 28 },
  entry: { width: '47.8%' },
  history: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 14, padding: 14 },
  historyBody: { flex: 1 },
  historyMeta: { flexDirection: 'row', alignItems: 'center', flexWrap: 'wrap', gap: 8, marginBottom: 7 },
  historyStatus: { color: colors.textSoft, fontSize: 12, fontWeight: '700' },
  historyTitle: { color: colors.text, fontWeight: '900', fontSize: 15 },
  historyText: { color: colors.textSoft, marginTop: 4, fontSize: 12 },
});
